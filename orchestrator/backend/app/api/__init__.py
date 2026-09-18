from .routes_tasks import router as tasks_router
from .routes_specs import router as specs_router
from .routes_agents import router as agents_router
from .routes_ws import router as ws_router

__all__ = [
    "tasks_router",
    "specs_router",
    "agents_router",
    "ws_router",
]
