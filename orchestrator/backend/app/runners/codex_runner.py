import os
import shutil
from typing import Dict, Any, Optional
from app.runners.base import BaseAgentRunner
from app.schemas.task import TaskDefinition
from app.core.process_manager import StreamChunk

class CodexRunner(BaseAgentRunner):
    @property
    def agent_id(self) -> str:
        return "codex"

    @property
    def display_name(self) -> str:
        return "OpenAI Codex CLI (@openai/codex)"

    async def run(
        self,
        task: TaskDefinition,
        compiled_prompt: str,
        working_dir: str
    ) -> int:
        codex_bin = shutil.which("codex")
        if not codex_bin:
            await self.process_manager.broadcast(StreamChunk(
                task_id=task.task_id,
                stream="stderr",
                content="[CODEX RUNNER] ⚠️ 'codex' CLI binary not found in PATH.\nMake sure OpenAI Codex is installed (`npm i -g @openai/codex`) or run inside the container.\n"
            ))
            return 1

        cmd = [codex_bin, "--prompt", compiled_prompt]
        return await self.process_manager.execute_command(
            task_id=task.task_id,
            cmd=cmd,
            cwd=working_dir,
            timeout_seconds=task.constraints.timeout_seconds if task.constraints else 300
        )
