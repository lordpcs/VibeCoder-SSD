#!/usr/bin/env bash
# ==============================================================================
# Launch Vibe Coder Agentic Orchestrator & Web Dashboard
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Starting Agentic Orchestrator & Web Dashboard on http://localhost:4040..."

export ORCHESTRATOR_PORT="${ORCHESTRATOR_PORT:-4040}"
export ORCHESTRATOR_HOST="${ORCHESTRATOR_HOST:-0.0.0.0}"

PYTHON_BIN="python3"
if ! command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python"
fi

cd "$ROOT_DIR"
exec "$PYTHON_BIN" orchestrator/run.py
