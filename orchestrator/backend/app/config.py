import os
from pathlib import Path

# Paths
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
ORCHESTRATOR_DIR = BACKEND_DIR.parent
PROJECT_ROOT = ORCHESTRATOR_DIR.parent
SPECS_DIR = PROJECT_ROOT / "specs"
TASKS_DIR = SPECS_DIR / "tasks"
TASK_HISTORY_DIR = TASKS_DIR / "history"
STATIC_DIR = BACKEND_DIR / "static"

# Ensure directories exist
TASK_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Configuration
PORT = int(os.getenv("ORCHESTRATOR_PORT", "4040"))
HOST = os.getenv("ORCHESTRATOR_HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PROJECT_NAME = "Proyecto-Coder Next Orchestrator"
VERSION = "1.0.0"
