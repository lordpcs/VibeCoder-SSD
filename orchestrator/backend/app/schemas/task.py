from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    VERIFYING = "verifying"
    SELF_HEALING = "self_healing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskConstraints(BaseModel):
    max_iterations: int = Field(default=3, ge=1, le=10)
    strict_types: bool = True
    preserve_tests: bool = True
    timeout_seconds: int = Field(default=300, ge=30, le=1800)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    intent_vibe: str = Field(..., min_length=5)
    target_component: str
    target_spec: Optional[str] = "specs/contracts/api-v1.yaml"
    affected_files: Optional[List[str]] = Field(default_factory=list)
    assigned_agent: str = Field(default="claude-code")
    constraints: Optional[TaskConstraints] = Field(default_factory=TaskConstraints)
    acceptance_criteria: List[str] = Field(..., min_length=1)
    verification_commands: Optional[List[str]] = Field(default_factory=list)

class TaskDefinition(TaskCreate):
    task_id: str

class VerificationResult(BaseModel):
    passed: bool
    command: str
    exit_code: int
    output: str
    duration_ms: float

class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus
    definition: TaskDefinition
    logs: List[str] = Field(default_factory=list)
    iterations_run: int = 0
    verification_results: List[VerificationResult] = Field(default_factory=list)
    error_message: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None
