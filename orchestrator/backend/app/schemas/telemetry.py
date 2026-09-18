from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ToolStatus(BaseModel):
    name: str
    command: str
    installed: bool
    version: Optional[str] = None
    purpose: str

class SystemMetrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_free_gb: float
    platform: str
    python_version: str

class SystemHealth(BaseModel):
    status: str
    timestamp: str
    tools: List[ToolStatus]
    tools_installed_count: int
    tools_total_count: int
    metrics: SystemMetrics
    environment: Dict[str, bool]
