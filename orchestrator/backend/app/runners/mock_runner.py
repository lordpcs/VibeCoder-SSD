import asyncio
import time
from typing import Dict, Any, Optional
from app.runners.base import BaseAgentRunner
from app.schemas.task import TaskDefinition
from app.core.process_manager import StreamChunk

class MockRunner(BaseAgentRunner):
    @property
    def agent_id(self) -> str:
        return "mock-runner"

    @property
    def display_name(self) -> str:
        return "SDD Simulation / Test Runner"

    async def run(
        self,
        task: TaskDefinition,
        compiled_prompt: str,
        working_dir: str
    ) -> int:
        steps = [
            ("stdout", f"🚀 [MOCK AGENT] Starting mission '{task.title}' (ID: {task.task_id})...\n"),
            ("stdout", f"📖 Reading contract specs: {task.target_spec or 'default specs'}...\n"),
            ("stdout", f"🎯 Target Component: {task.target_component}\n"),
            ("stdout", f"⚡ Parsing acceptance criteria: {len(task.acceptance_criteria)} items found.\n"),
            ("stdout", "✨ Synthesizing implementation according to SDD blueprint...\n"),
            ("stdout", "🔍 Performing local type-checking and syntax verification...\n"),
            ("stdout", "🎉 Code synthesis complete! Passing to SDD automated verification loop.\n")
        ]

        for stream, content in steps:
            await self.process_manager.broadcast(StreamChunk(
                task_id=task.task_id,
                stream=stream,
                content=content
            ))
            await asyncio.sleep(0.6)

        return 0
