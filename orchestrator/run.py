#!/usr/bin/env python3
"""
Entrypoint to run the Vibe Coder Agentic Orchestrator.
"""
import sys
import os
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

# Configure Windows UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def main():
    try:
        import uvicorn
    except ImportError:
        print("❌ Error: 'uvicorn' is not installed.")
        print("Please run: pip install -r orchestrator/backend/requirements.txt")
        sys.exit(1)

    port = int(os.getenv("ORCHESTRATOR_PORT", "4040"))
    host = os.getenv("ORCHESTRATOR_HOST", "0.0.0.0")
    print(f"🚀 Starting Vibe Coder Agentic Orchestrator on http://{host}:{port} (PID: {os.getpid()})")
    uvicorn.run("app.main:app", host=host, port=port, reload=False, app_dir=str(backend_dir))

if __name__ == "__main__":
    main()
