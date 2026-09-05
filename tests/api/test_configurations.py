from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_configurations():
    response = client.get("/api/v1/configurations")
    assert response.status_code == 200
    data = response.json()
    assert data["task_family"] == "Transitive Inference"
    assert "deterministic" in data["evaluator_types"]
