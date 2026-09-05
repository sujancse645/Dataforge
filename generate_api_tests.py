import os

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "tests/api/__init__.py": "",
    "tests/api/test_health.py": """
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
""",
    "tests/api/test_configurations.py": """
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_configurations():
    response = client.get("/api/v1/configurations")
    assert response.status_code == 200
    data = response.json()
    assert data["task_family"] == "Transitive Inference"
    assert "deterministic" in data["evaluator_types"]
""",
    "tests/api/test_experiments.py": """
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
""",
    "tests/integration/__init__.py": "",
    "tests/integration/test_api_engine.py": """
from fastapi.testclient import TestClient
from src.api.main import app
from src.engine.runner import ExperimentRunner
from src.engine.schemas import ExperimentConfig
import uuid

client = TestClient(app)

def test_cli_api_parity():
    # 1. API request
    payload = {
        "master_seed": 123,
        "demonstration_count": 2,
        "demonstration_complexity": 2,
        "extrapolation_levels": [0, 1],
        "tasks_per_level": 2,
        "evaluator_type": "deterministic"
    }
    api_resp = client.post("/api/v1/experiments", json=payload)
    assert api_resp.status_code == 200
    api_data = api_resp.json()
    
    # 2. Engine Runner directly
    config = ExperimentConfig(
        experiment_id="test-id",
        task_family="Transitive Inference",
        demonstration_count=2,
        demonstration_complexity=2,
        extrapolation_levels=[0, 1],
        tasks_per_level=2,
        master_seed=123,
        evaluator="deterministic"
    )
    runner = ExperimentRunner(config)
    engine_data = runner.run().model_dump()
    
    # Verify scientific parity
    assert api_data["demonstration_coverage"] == engine_data["demonstration_coverage"]
    assert api_data["cliff_detected"] == engine_data["cliff_detected"]
    
    # Verify first raw result prediction
    api_pred = api_data["raw_results"][0]["prediction"]
    engine_pred = engine_data["raw_results"][0]["prediction"]
    assert api_pred == engine_pred
"""
}

for path, content in files.items():
    write_file(path, content)
