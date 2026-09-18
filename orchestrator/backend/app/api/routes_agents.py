import os
import shutil
import subprocess
import sys
import platform
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter

from app.schemas.telemetry import SystemHealth, ToolStatus, SystemMetrics

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

router = APIRouter(prefix="/api/agents", tags=["Agents & Health"])

KNOWN_TOOLS = [
    {"name": "Git", "command": "git", "version_arg": "--version", "purpose": "Version control"},
    {"name": "Node.js", "command": "node", "version_arg": "--version", "purpose": "JavaScript/TypeScript runtime"},
    {"name": "NPM", "command": "npm", "version_arg": "--version", "purpose": "Package manager"},
    {"name": "PNPM", "command": "pnpm", "version_arg": "--version", "purpose": "Fast disk-efficient package manager"},
    {"name": "Bun", "command": "bun", "version_arg": "--version", "purpose": "Fast all-in-one JavaScript runtime"},
    {"name": "GitHub CLI", "command": "gh", "version_arg": "--version", "purpose": "GitHub CLI workflow"},
    {"name": "Railway CLI", "command": "railway", "version_arg": "--version", "purpose": "Cloud deployment platform"},
    {"name": "Claude Code", "command": "claude", "version_arg": "--version", "purpose": "Anthropic AI terminal agent"},
    {"name": "OpenAI Codex", "command": "codex", "version_arg": "--version", "purpose": "OpenAI coding assistant"},
    {"name": "Lazygit", "command": "lazygit", "version_arg": "--version", "purpose": "Terminal Git UI"},
    {"name": "Eza", "command": "eza", "version_arg": "--version", "purpose": "Modern ls with icons"},
    {"name": "Bat", "command": "bat", "version_arg": "--version", "purpose": "Cat with syntax highlighting"},
    {"name": "FZF", "command": "fzf", "version_arg": "--version", "purpose": "Fuzzy interactive finder"},
]

def check_tool(tool_info: Dict[str, str]) -> ToolStatus:
    cmd = tool_info["command"]
    path = shutil.which(cmd)
    if not path and sys.platform == "win32":
        path = shutil.which(f"{cmd}.cmd") or shutil.which(f"{cmd}.exe")
    
    installed = path is not None
    version_str = None
    if installed:
        try:
            res = subprocess.run(
                [path, tool_info["version_arg"]],
                capture_output=True,
                text=True,
                timeout=2,
                shell=(sys.platform == "win32")
            )
            out = res.stdout.strip() or res.stderr.strip()
            version_str = out.splitlines()[0] if out else "installed"
        except Exception:
            version_str = "installed"

    return ToolStatus(
        name=tool_info["name"],
        command=cmd,
        installed=installed,
        version=version_str,
        purpose=tool_info["purpose"]
    )

@router.get("/health", response_model=SystemHealth)
async def get_system_health():
    tools = [check_tool(t) for t in KNOWN_TOOLS]
    installed_count = sum(1 for t in tools if t.installed)

    if HAS_PSUTIL:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").free / (1024 ** 3)
    else:
        cpu = 0.0
        mem = 0.0
        disk = 0.0

    metrics = SystemMetrics(
        cpu_percent=cpu,
        memory_percent=mem,
        disk_free_gb=round(disk, 2),
        platform=f"{platform.system()} {platform.release()}",
        python_version=platform.python_version()
    )

    env_status = {
        "ANTHROPIC_API_KEY": bool(os.getenv("ANTHROPIC_API_KEY")),
        "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
        "GH_TOKEN": bool(os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")),
        "RAILWAY_TOKEN": bool(os.getenv("RAILWAY_TOKEN")),
    }

    status_str = "healthy" if installed_count >= 5 else "degraded"

    return SystemHealth(
        status=status_str,
        timestamp=datetime.utcnow().isoformat(),
        tools=tools,
        tools_installed_count=installed_count,
        tools_total_count=len(KNOWN_TOOLS),
        metrics=metrics,
        environment=env_status
    )
