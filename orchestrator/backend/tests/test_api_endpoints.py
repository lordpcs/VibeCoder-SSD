import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from starlette.testclient import TestClient
from app.main import app

def test_api():
    client = TestClient(app)
    
    # 1. Health check
    res_health = client.get("/api/agents/health")
    assert res_health.status_code == 200
    data_health = res_health.json()
    assert data_health["status"] in ["healthy", "degraded"]
    print(f"✅ /api/agents/health: OK (Tools: {data_health['tools_installed_count']}/{data_health['tools_total_count']})")

    # 2. Blueprint
    res_bp = client.get("/api/specs/blueprint")
    assert res_bp.status_code == 200
    data_bp = res_bp.json()
    assert "components" in data_bp
    print(f"✅ /api/specs/blueprint: OK (Project: {data_bp['project']['name']})")

    # 3. Spec Validation
    res_val = client.post("/api/specs/validate")
    assert res_val.status_code == 200
    data_val = res_val.json()
    assert data_val["valid"] is True
    print("✅ /api/specs/validate: OK (All specs valid)")

    # 4. Static frontend index.html
    res_index = client.get("/")
    assert res_index.status_code == 200
    assert "Vibe Coder" in res_index.text
    print("✅ Static Web Dashboard served at /: OK")

    print("🎉 All API and static routes verified successfully!")

if __name__ == "__main__":
    test_api()
