import asyncio
import time
from typing import List, Dict, Any, Optional
from app.config import PROJECT_ROOT
from app.schemas.task import VerificationResult

class SDDVerifier:
    def __init__(self, project_root=PROJECT_ROOT):
        self.project_root = project_root

    async def run_command(self, cmd_str: str, timeout_seconds: int = 60) -> VerificationResult:
        start_time = time.time()
        try:
            proc = await asyncio.create_subprocess_shell(
                cmd_str,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(self.project_root)
            )

            stdout_data, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout_seconds)
            duration_ms = (time.time() - start_time) * 1000.0
            output = stdout_data.decode("utf-8", errors="replace") if stdout_data else ""
            exit_code = proc.returncode or 0

            return VerificationResult(
                passed=(exit_code == 0),
                command=cmd_str,
                exit_code=exit_code,
                output=output,
                duration_ms=round(duration_ms, 2)
            )
        except asyncio.TimeoutError:
            duration_ms = (time.time() - start_time) * 1000.0
            return VerificationResult(
                passed=False,
                command=cmd_str,
                exit_code=-1,
                output=f"Timed out after {timeout_seconds}s",
                duration_ms=round(duration_ms, 2)
            )
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000.0
            return VerificationResult(
                passed=False,
                command=cmd_str,
                exit_code=1,
                output=f"Execution error: {str(e)}",
                duration_ms=round(duration_ms, 2)
            )

    async def verify_task(self, verification_commands: List[str]) -> List[VerificationResult]:
        results: List[VerificationResult] = []
        for cmd in verification_commands:
            if not cmd.strip():
                continue
            res = await self.run_command(cmd)
            results.append(res)
        return results
