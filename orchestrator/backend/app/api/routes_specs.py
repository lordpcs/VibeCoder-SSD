from fastapi import APIRouter
from typing import Dict, Any

from app.schemas.spec import SpecValidationResult, CompilePromptRequest, CompilePromptResponse
from app.core.dispatcher import dispatcher

router = APIRouter(prefix="/api/specs", tags=["Specifications"])

@router.get("/blueprint")
async def get_system_blueprint():
    return dispatcher.sdd_compiler.get_blueprint()

@router.get("/invariants")
async def get_system_invariants():
    return dispatcher.sdd_compiler.get_invariants()

@router.get("/task-schema")
async def get_task_schema():
    return dispatcher.sdd_compiler.get_task_schema()

@router.post("/validate", response_model=SpecValidationResult)
async def validate_specifications():
    return dispatcher.sdd_compiler.validate_specs()

@router.post("/compile-prompt", response_model=CompilePromptResponse)
async def compile_prompt(req: CompilePromptRequest):
    return dispatcher.sdd_compiler.compile_prompt_from_vibe(
        intent_vibe=req.intent_vibe,
        target_component=req.target_component,
        target_spec=req.target_spec,
        assigned_agent=req.assigned_agent or "claude-code",
        affected_files=req.affected_files
    )
