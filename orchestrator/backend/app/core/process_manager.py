import asyncio
import os
import sys
import time
from typing import Dict, Any, List, Optional, Callable, Awaitable
from dataclasses import dataclass, field

@dataclass
class StreamChunk:
    task_id: str
    stream: str # 'stdout', 'stderr', 'system'
    content: str
    timestamp: float = field(default_factory=time.time)

class ProcessManager:
    def __init__(self):
        self._active_processes: Dict[str, asyncio.subprocess.Process] = {}
        self._listeners: Dict[str, List[Callable[[StreamChunk], Awaitable[None]]]] = {}
        self._logs: Dict[str, List[str]] = {}

    def subscribe(self, task_id: str, callback: Callable[[StreamChunk], Awaitable[None]]):
        if task_id not in self._listeners:
            self._listeners[task_id] = []
        self._listeners[task_id].append(callback)

    def unsubscribe(self, task_id: str, callback: Callable[[StreamChunk], Awaitable[None]]):
        if task_id in self._listeners and callback in self._listeners[task_id]:
            self._listeners[task_id].remove(callback)

    async def broadcast(self, chunk: StreamChunk):
        if chunk.task_id not in self._logs:
            self._logs[chunk.task_id] = []
        self._logs[chunk.task_id].append(chunk.content)

        callbacks = self._listeners.get(chunk.task_id, [])
        for cb in callbacks:
            try:
                await cb(chunk)
            except Exception:
                pass

    def get_logs(self, task_id: str) -> List[str]:
        return self._logs.get(task_id, [])

    async def execute_command(
        self,
        task_id: str,
        cmd: List[str] | str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout_seconds: int = 300
    ) -> int:
        await self.broadcast(StreamChunk(
            task_id=task_id,
            stream="system",
            content=f"\n[ORCHESTRATOR] 🚀 Spawning process: {cmd}\n"
        ))

        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        merged_env["PYTHONUNBUFFERED"] = "1"

        try:
            if isinstance(cmd, list):
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd,
                    env=merged_env
                )
            else:
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd,
                    env=merged_env
                )

            self._active_processes[task_id] = proc

            async def read_stream(stream, name: str):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    decoded = line.decode("utf-8", errors="replace")
                    await self.broadcast(StreamChunk(task_id=task_id, stream=name, content=decoded))

            try:
                await asyncio.wait_for(
                    asyncio.gather(
                        read_stream(proc.stdout, "stdout"),
                        read_stream(proc.stderr, "stderr"),
                        proc.wait()
                    ),
                    timeout=timeout_seconds
                )
                exit_code = proc.returncode or 0
            except asyncio.TimeoutError:
                await self.broadcast(StreamChunk(
                    task_id=task_id,
                    stream="system",
                    content=f"\n[ORCHESTRATOR] ⚠️ Process timed out after {timeout_seconds}s. Terminating...\n"
                ))
                proc.kill()
                exit_code = -1

            await self.broadcast(StreamChunk(
                task_id=task_id,
                stream="system",
                content=f"\n[ORCHESTRATOR] 🏁 Process finished with exit code {exit_code}\n"
            ))
            return exit_code

        except Exception as e:
            await self.broadcast(StreamChunk(
                task_id=task_id,
                stream="system",
                content=f"\n[ORCHESTRATOR] ❌ Execution error: {e}\n"
            ))
            return 1
        finally:
            self._active_processes.pop(task_id, None)

    async def cancel_task(self, task_id: str) -> bool:
        proc = self._active_processes.get(task_id)
        if proc:
            try:
                proc.terminate()
                await asyncio.sleep(0.5)
                if proc.returncode is None:
                    proc.kill()
                await self.broadcast(StreamChunk(
                    task_id=task_id,
                    stream="system",
                    content="\n[ORCHESTRATOR] 🛑 Task successfully cancelled by user.\n"
                ))
                return True
            except Exception:
                return False
        return False
