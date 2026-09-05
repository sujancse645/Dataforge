import os

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "src/api/__init__.py": "",
    "src/api/routes/__init__.py": "",
    "src/api/schemas/__init__.py": "",
    "src/api/schemas/requests.py": """
from pydantic import BaseModel, Field
from typing import List

class ExperimentRequest(BaseModel):
    master_seed: int = Field(..., description="Master seed for deterministic generation")
    demonstration_count: int = Field(..., gt=0, le=10, description="Number of demonstrations")
    demonstration_complexity: int = Field(..., gt=0, le=5, description="Complexity of demonstrations")
    extrapolation_levels: List[int] = Field(..., description="List of extrapolation distances")
    tasks_per_level: int = Field(..., gt=0, le=50, description="Tasks to evaluate per level")
    evaluator_type: str = Field(..., description="Type of evaluator to use")
""",
    "src/api/schemas/responses.py": """
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    engine: str

class ConfigurationResponse(BaseModel):
    task_family: str
    supported_complexity_range: List[int]
    supported_extrapolation_levels: List[int]
    default_demonstration_count: int
    evaluator_types: List[str]
    engine_version: str
""",
    "src/api/routes/health.py": """
from fastapi import APIRouter
from src.api.schemas.responses import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def get_health():
    engine_status = "available"
    try:
        import src.engine
    except ImportError:
        engine_status = "unavailable"
        
    return HealthResponse(
        status="ok",
        service="coverage-cliff-api",
        version="1.0.0",
        engine=engine_status
    )
""",
    "src/api/routes/configurations.py": """
from fastapi import APIRouter
from src.api.schemas.responses import ConfigurationResponse

router = APIRouter()

@router.get("/configurations", response_model=ConfigurationResponse)
def get_configurations():
    return ConfigurationResponse(
        task_family="Transitive Inference",
        supported_complexity_range=[1, 2, 3, 4, 5],
        supported_extrapolation_levels=[0, 1, 2, 3, 4, 5],
        default_demonstration_count=3,
        evaluator_types=["deterministic"],
        engine_version="1.0.0"
    )
""",
    "src/api/routes/experiments.py": """
from fastapi import APIRouter, HTTPException
from src.api.schemas.requests import ExperimentRequest
from src.engine.schemas import ExperimentConfig, ExperimentResult
from src.engine.runner import ExperimentRunner
import uuid

router = APIRouter()

@router.post("/experiments", response_model=ExperimentResult)
def run_experiment(req: ExperimentRequest):
    if req.evaluator_type != "deterministic":
        raise HTTPException(status_code=400, detail="Only 'deterministic' evaluator is supported in Phase 2.")
        
    config = ExperimentConfig(
        experiment_id=str(uuid.uuid4()),
        task_family="Transitive Inference",
        demonstration_count=req.demonstration_count,
        demonstration_complexity=req.demonstration_complexity,
        extrapolation_levels=req.extrapolation_levels,
        tasks_per_level=req.tasks_per_level,
        master_seed=req.master_seed,
        evaluator=req.evaluator_type
    )
    
    try:
        runner = ExperimentRunner(config)
        result = runner.run()
        return result
    except ValueError as e:
        # Scientific validation failure
        raise HTTPException(status_code=422, detail=f"Scientific Validation Failure: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected server failure")
""",
    "src/api/main.py": """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import health, configurations, experiments

app = FastAPI(
    title="Coverage Cliff API",
    version="1.0.0",
    description="FastAPI backend for Coverage Cliff Experiment Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(configurations.router, prefix="/api/v1", tags=["Configurations"])
app.include_router(experiments.router, prefix="/api/v1", tags=["Experiments"])
""",
    "api_smoke_test.py": """
import sys
from fastapi.testclient import TestClient
from src.api.main import app

def run_smoke_test():
    print("Running API Smoke Test...")
    client = TestClient(app)
    
    # 1. Health
    res = client.get("/api/v1/health")
    assert res.status_code == 200, "Health endpoint failed"
    print("Health OK")
    
    # 2. Configurations
    res = client.get("/api/v1/configurations")
    assert res.status_code == 200, "Configurations endpoint failed"
    print("Configurations OK")
    
    # 3. Valid Experiment
    payload = {
        "master_seed": 42,
        "demonstration_count": 3,
        "demonstration_complexity": 2,
        "extrapolation_levels": [0, 1, 2, 3],
        "tasks_per_level": 5,
        "evaluator_type": "deterministic"
    }
    res = client.post("/api/v1/experiments", json=payload)
    if res.status_code != 200:
        print(f"Experiment failed: {res.text}")
        sys.exit(1)
        
    data = res.json()
    assert "cliff_detected" in data
    print(f"Experiment OK - Cliff Detected: {data['cliff_detected']}")
    
    # 4. Invalid Request
    bad_payload = payload.copy()
    bad_payload["demonstration_count"] = -1
    res = client.post("/api/v1/experiments", json=bad_payload)
    assert res.status_code == 422, "Failed to reject invalid request"
    print("Invalid Request Rejection OK")
    
    print("API Smoke Test Passed!")

if __name__ == "__main__":
    run_smoke_test()
"""
}

for path, content in files.items():
    write_file(path, content)
