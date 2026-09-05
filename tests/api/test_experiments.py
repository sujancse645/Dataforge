from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_valid_experiment():
    payload = {
        "master_seed": 42,
        "demonstration_count": 3,
        "demonstration_complexity": 2,
        "extrapolation_levels": [0, 1],
        "tasks_per_level": 2,
        "evaluator_type": "deterministic"
    }
    response = client.post("/api/v1/experiments", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "experiment_id" in data
    assert data["demonstration_coverage"] == 2
    assert "0" in data["level_metrics"]

def test_invalid_evaluator():
    payload = {
        "master_seed": 42,
        "demonstration_count": 3,
        "demonstration_complexity": 2,
        "extrapolation_levels": [0, 1],
        "tasks_per_level": 2,
        "evaluator_type": "gpt-4"
    }
    response = client.post("/api/v1/experiments", json=payload)
    assert response.status_code == 400

def test_invalid_request_schema():
    payload = {
        "master_seed": 42,
        "demonstration_count": -5,
        "demonstration_complexity": 2,
        "extrapolation_levels": [0, 1],
        "tasks_per_level": 2,
        "evaluator_type": "deterministic"
    }
    response = client.post("/api/v1/experiments", json=payload)
    assert response.status_code == 422
