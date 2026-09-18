import os
import shutil
from typing import Dict, Any, Optional
from app.runners.base import BaseAgentRunner
from app.schemas.task import TaskDefinition
from app.core.process_manager import StreamChunk

class ClaudeRunner(BaseAgentRunner):
    @property
    def agent_id(self) -> str:
        return "claude-code"

    @property
    def display_name(self) -> str:
        return "Claude Code CLI (@anthropic-ai/claude-code)"

    async def run(
        self,
        task: TaskDefinition,
        compiled_prompt: str,
        working_dir: str
    ) -> int:
        claude_bin = shutil.which("claude")
        if not claude_bin:
            await self.process_manager.broadcast(StreamChunk(
                task_id=task.task_id,
                stream="stderr",
                content="[CLAUDE RUNNER] ⚠️ 'claude' CLI binary not found in PATH.\nMake sure Claude Code is installed (`npm i -g @anthropic-ai/claude-code`) or run inside the container.\n"
            ))
            return 1

        cmd = [claude_bin, "-p", compiled_prompt]
        return await self.process_manager.execute_command(
            task_id=task.task_id,
            cmd=cmd,
            cwd=working_dir,
            timeout_seconds=task.constraints.timeout_seconds if task.constraints else 300
        )
