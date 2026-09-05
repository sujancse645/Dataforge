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
