import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

from app.config import PROJECT_NAME, VERSION, STATIC_DIR
from app.api import tasks_router, specs_router, agents_router, ws_router

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="Agentic Orchestrator & SDD Platform for Vibe Coder Next"
)

# Enable CORS for local development (Vite dev server, localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(tasks_router)
app.include_router(specs_router)
app.include_router(agents_router)
app.include_router(ws_router)

# Mount static files if present
index_html = STATIC_DIR / "index.html"

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    if index_html.exists():
        return FileResponse(index_html)
    return HTMLResponse(
        content="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Vibe Coder Orchestrator API</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }
    .card { background: #1e293b; padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #334155; max-width: 650px; margin: 0 auto; }
    h1 { color: #38bdf8; margin-top: 0; }
    a { color: #a855f7; text-decoration: none; }
    a:hover { text-decoration: underline; }
    code { background: #0f172a; padding: 0.2rem 0.4rem; border-radius: 4px; color: #34d399; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🚀 Vibe Coder Orchestrator</h1>
    <p>Agentic Orchestration & SDD Platform is running.</p>
    <ul>
      <li>API Documentation: <a href="/docs">Interactive OpenAPI Swagger UI</a></li>
      <li>System Health: <a href="/api/agents/health"><code>/api/agents/health</code></a></li>
      <li>SDD Blueprint: <a href="/api/specs/blueprint"><code>/api/specs/blueprint</code></a></li>
      <li>Tasks: <a href="/api/tasks"><code>/api/tasks</code></a></li>
    </ul>
    <p>The Mission Control Web Dashboard frontend is ready to build with <code>cd orchestrator/dashboard && npm run build</code>.</p>
  </div>
</body>
</html>"""
    )

assets_dir = STATIC_DIR / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="static_assets")
