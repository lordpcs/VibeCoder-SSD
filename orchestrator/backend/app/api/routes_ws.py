import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.dispatcher import dispatcher
from app.core.process_manager import StreamChunk

router = APIRouter(tags=["WebSockets"])

@router.websocket("/ws/terminal/{task_id}")
async def websocket_terminal(websocket: WebSocket, task_id: str):
    await websocket.accept()

    # Send existing backlog logs
    existing_logs = dispatcher.process_manager.get_logs(task_id)
    for line in existing_logs:
        try:
            await websocket.send_json({
                "task_id": task_id,
                "stream": "stdout",
                "content": line
            })
        except Exception:
            return

    # Callback for new streaming chunks
    async def log_callback(chunk: StreamChunk):
        try:
            await websocket.send_json({
                "task_id": chunk.task_id,
                "stream": chunk.stream,
                "content": chunk.content,
                "timestamp": chunk.timestamp
            })
        except Exception:
            pass

    dispatcher.process_manager.subscribe(task_id, log_callback)

    try:
        while True:
            # Keep connection alive, listen for client messages (e.g. cancel, input)
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "cancel":
                    await dispatcher.cancel_task(task_id)
            except Exception:
                pass
    except WebSocketDisconnect:
        pass
    finally:
        dispatcher.process_manager.unsubscribe(task_id, log_callback)

@router.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            tasks = dispatcher.get_all_tasks()
            active_count = sum(1 for t in tasks if t.status in ["running", "verifying", "self_healing"])
            await websocket.send_json({
                "active_tasks_count": active_count,
                "total_tasks_count": len(tasks),
                "tasks": [
                    {
                        "task_id": t.task_id,
                        "title": t.definition.title,
                        "status": t.status,
                        "agent": t.definition.assigned_agent
                    } for t in tasks[:10]
                ]
            })
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
