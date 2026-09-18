import asyncio
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.config import PROJECT_ROOT, TASK_HISTORY_DIR
from app.schemas.task import TaskDefinition, TaskStatus, TaskResult, VerificationResult
from app.core.process_manager import ProcessManager, StreamChunk
from app.core.sdd_compiler import SDDCompiler
from app.core.verifier import SDDVerifier
from app.runners import BaseAgentRunner, ClaudeRunner, CodexRunner, SubagentRunner, MockRunner

class TaskDispatcher:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root
        self.process_manager = ProcessManager()
        self.sdd_compiler = SDDCompiler(project_root)
        self.verifier = SDDVerifier(project_root)
        
        # Initialize runners
        self.runners: Dict[str, BaseAgentRunner] = {
            "claude-code": ClaudeRunner(self.process_manager),
            "codex": CodexRunner(self.process_manager),
            "autonomous-subagent": SubagentRunner(self.process_manager),
            "mock-runner": MockRunner(self.process_manager),
        }

        self.tasks: Dict[str, TaskResult] = {}
        self._load_persisted_tasks()

    def _load_persisted_tasks(self):
        if not TASK_HISTORY_DIR.exists():
            return
        for file in TASK_HISTORY_DIR.glob("*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                result = TaskResult(**data)
                self.tasks[result.task_id] = result
            except Exception:
                pass

    def _persist_task(self, task_result: TaskResult):
        try:
            file_path = TASK_HISTORY_DIR / f"{task_result.task_id}.json"
            file_path.write_text(task_result.model_dump_json(indent=2), encoding="utf-8")
        except Exception:
            pass

    def get_all_tasks(self) -> List[TaskResult]:
        return sorted(list(self.tasks.values()), key=lambda t: t.created_at, reverse=True)

    def get_task(self, task_id: str) -> Optional[TaskResult]:
        return self.tasks.get(task_id)

    async def cancel_task(self, task_id: str) -> bool:
        if task_id in self.tasks and self.tasks[task_id].status in [TaskStatus.RUNNING, TaskStatus.VERIFYING]:
            cancelled = await self.process_manager.cancel_task(task_id)
            if cancelled:
                self.tasks[task_id].status = TaskStatus.CANCELLED
                self.tasks[task_id].completed_at = datetime.utcnow().isoformat()
                self._persist_task(self.tasks[task_id])
            return cancelled
        return False

    async def submit_task(self, task: TaskDefinition) -> TaskResult:
        task_result = TaskResult(
            task_id=task.task_id,
            status=TaskStatus.QUEUED,
            definition=task,
            logs=[],
            iterations_run=0,
            verification_results=[],
            created_at=datetime.utcnow().isoformat()
        )
        self.tasks[task.task_id] = task_result
        self._persist_task(task_result)

        # Run execution asynchronously in background task
        asyncio.create_task(self._execute_task_lifecycle(task.task_id))
        return task_result

    async def _execute_task_lifecycle(self, task_id: str):
        task_result = self.tasks.get(task_id)
        if not task_result:
            return

        task = task_result.definition
        agent_id = task.assigned_agent
        runner = self.runners.get(agent_id, self.runners.get("mock-runner"))

        max_iterations = task.constraints.max_iterations if task.constraints else 3
        iteration = 0
        success = False

        # Initial prompt compilation
        compiled = self.sdd_compiler.compile_prompt_from_vibe(
            intent_vibe=task.intent_vibe,
            target_component=task.target_component,
            target_spec=task.target_spec,
            assigned_agent=agent_id,
            affected_files=task.affected_files
        )
        current_prompt = compiled.compiled_prompt

        while iteration < max_iterations and not success:
            iteration += 1
            task_result.iterations_run = iteration

            # 1. RUNNING PHASE
            task_result.status = TaskStatus.RUNNING
            self._persist_task(task_result)

            await self.process_manager.broadcast(StreamChunk(
                task_id=task_id,
                stream="system",
                content=f"\n--- [SDD CYCLE] Iteration {iteration}/{max_iterations} with Agent: {runner.display_name} ---\n"
            ))

            exit_code = await runner.run(
                task=task,
                compiled_prompt=current_prompt,
                working_dir=str(self.project_root)
            )

            if exit_code != 0 and agent_id != "mock-runner":
                # Runner failed
                task_result.status = TaskStatus.FAILED
                task_result.error_message = f"Agent runner exited with code {exit_code}"
                task_result.completed_at = datetime.utcnow().isoformat()
                self._persist_task(task_result)
                return

            # 2. VERIFICATION GATES PHASE
            task_result.status = TaskStatus.VERIFYING
            self._persist_task(task_result)

            await self.process_manager.broadcast(StreamChunk(
                task_id=task_id,
                stream="system",
                content="\n🛡️ [SDD GATES] Running post-task automated verification suite...\n"
            ))

            verification_cmds = task.verification_commands or ["python bin/sdd.py lint"]
            ver_results = await self.verifier.verify_task(verification_cmds)
            task_result.verification_results = ver_results

            all_passed = all(r.passed for r in ver_results)
            for r in ver_results:
                status_icon = "✅" if r.passed else "❌"
                await self.process_manager.broadcast(StreamChunk(
                    task_id=task_id,
                    stream="system",
                    content=f"{status_icon} Command: `{r.command}` ({r.duration_ms}ms) -> exit code {r.exit_code}\n"
                ))
                if not r.passed and r.output:
                    await self.process_manager.broadcast(StreamChunk(
                        task_id=task_id,
                        stream="stderr",
                        content=f"Failure trace:\n{r.output[:500]}...\n"
                    ))

            if all_passed:
                success = True
                task_result.status = TaskStatus.COMPLETED
                task_result.completed_at = datetime.utcnow().isoformat()
                await self.process_manager.broadcast(StreamChunk(
                    task_id=task_id,
                    stream="system",
                    content="\n🎉 [SDD SUCCESS] All verification gates passed! Task completed successfully.\n"
                ))
                self._persist_task(task_result)
                break
            else:
                # 3. SELF-HEALING LOOP
                if iteration < max_iterations:
                    task_result.status = TaskStatus.SELF_HEALING
                    self._persist_task(task_result)
                    
                    failed_details = "\n".join([f"Command: {r.command}\nError Output:\n{r.output}" for r in ver_results if not r.passed])
                    await self.process_manager.broadcast(StreamChunk(
                        task_id=task_id,
                        stream="system",
                        content=f"\n🔄 [SELF-HEALING] Preparing recovery prompt for iteration {iteration + 1}...\n"
                    ))

                    current_prompt = f"""# RECOVERY INSTRUCTION: FIX VERIFICATION FAILURES
The previous implementation for task '{task.title}' failed automated verification gates:

{failed_details}

Please analyze the failure trace above, fix all issues, ensure all system invariants hold, and re-run.
"""
                else:
                    task_result.status = TaskStatus.FAILED
                    task_result.error_message = "Max iterations reached without passing all verification gates."
                    task_result.completed_at = datetime.utcnow().isoformat()
                    await self.process_manager.broadcast(StreamChunk(
                        task_id=task_id,
                        stream="system",
                        content="\n💥 [SDD FAILED] Max iterations exceeded. Please inspect errors.\n"
                    ))
                    self._persist_task(task_result)

# Singleton instance
dispatcher = TaskDispatcher()
