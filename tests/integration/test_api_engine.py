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
