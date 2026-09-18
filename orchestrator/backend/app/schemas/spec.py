from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ComponentDefinition(BaseModel):
    id: str
    name: str
    path: str
    type: str
    description: str
    runtime: Optional[str] = None
    port: Optional[int] = None
    dependencies: Optional[List[str]] = Field(default_factory=list)
    invariants: Optional[List[str]] = Field(default_factory=list)

class AgentProfile(BaseModel):
    id: str
    cli_command: str
    provider: str
    strengths: List[str]
    env_key: Optional[str] = None

class BlueprintSchema(BaseModel):
    version: str
    project: Dict[str, Any]
    architecture: Dict[str, Any]
    components: List[ComponentDefinition]
    agent_profiles: List[AgentProfile]
    verification_gates: Dict[str, Any]

class ValidationError(BaseModel):
    file: str
    message: str
    severity: str = "error"

class SpecValidationResult(BaseModel):
    valid: bool
    errors: List[ValidationError] = Field(default_factory=list)
    warnings: List[ValidationError] = Field(default_factory=list)
    blueprint_summary: Optional[Dict[str, Any]] = None

class CompilePromptRequest(BaseModel):
    intent_vibe: str
    target_component: str
    target_spec: Optional[str] = "specs/contracts/api-v1.yaml"
    assigned_agent: Optional[str] = "claude-code"
    affected_files: Optional[List[str]] = Field(default_factory=list)

class CompilePromptResponse(BaseModel):
    task_id: str
    compiled_prompt: str
    synthesized_manifest: Dict[str, Any]
