from fastapi import APIRouter, HTTPException, status
from typing import List
import time

from app.schemas.task import TaskCreate, TaskDefinition, TaskResult
from app.core.dispatcher import dispatcher

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.get("", response_model=List[TaskResult])
async def list_tasks():
    return dispatcher.get_all_tasks()

@router.post("", response_model=TaskResult, status_code=status.HTTP_202_ACCEPTED)
async def submit_task(task_input: TaskCreate):
    timestamp_str = time.strftime("%Y%m%d")
    slug = "_".join(task_input.title.lower().split()[:3])
    slug = "".join(c for c in slug if c.isalnum() or c == "_")
    task_id = f"task_{timestamp_str}_{slug or 'task'}_{int(time.time()) % 10000}"

    task_def = TaskDefinition(
        task_id=task_id,
        **task_input.model_dump()
    )
    return await dispatcher.submit_task(task_def)

@router.get("/{task_id}", response_model=TaskResult)
async def get_task(task_id: str):
    task = dispatcher.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    return task

@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    success = await dispatcher.cancel_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Unable to cancel task (it may not be running)")
    return {"message": "Task cancellation signal sent", "task_id": task_id}

@router.post("/{task_id}/verify")
async def manual_verify_task(task_id: str):
    task = dispatcher.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    results = await dispatcher.verifier.verify_task(task.definition.verification_commands)
    task.verification_results = results
    return results
