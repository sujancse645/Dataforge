import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse

from src.api.schemas.requests import ExperimentRequest
from src.engine.schemas import ExperimentConfig, ExperimentResult
from src.engine.runner import ExperimentRunner

router = APIRouter()

def _build_config(req: ExperimentRequest) -> ExperimentConfig:
    if req.evaluator_type != "deterministic":
        raise HTTPException(status_code=400, detail="Only 'deterministic' evaluator is supported in Phase 2.")

    return ExperimentConfig(
        experiment_id=str(uuid.uuid4()),
        task_family="Transitive Inference",
        demonstration_count=req.demonstration_count,
        demonstration_complexity=req.demonstration_complexity,
        extrapolation_levels=req.extrapolation_levels,
        tasks_per_level=req.tasks_per_level,
        master_seed=req.master_seed,
        evaluator=req.evaluator_type
    )

@router.post("/experiments", response_model=ExperimentResult)
def run_experiment(req: ExperimentRequest):
    config = _build_config(req)
    try:
        runner = ExperimentRunner(config)
        return runner.run()
    except ValueError as e:
        # Scientific validation failure
        raise HTTPException(status_code=422, detail=f"Scientific Validation Failure: {str(e)}")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server failure")

@router.post("/experiments/stream")
def run_experiment_stream(req: ExperimentRequest):
    """Runs the experiment engine in real time, streaming one NDJSON event per
    line as demonstrations are generated and each task is evaluated, so the
    frontend can render live progress instead of waiting for the final result."""
    config = _build_config(req)

    def event_source():
        try:
            for event in ExperimentRunner(config).run_stream():
                yield json.dumps(jsonable_encoder(event)) + "\n"
        except ValueError as e:
            yield json.dumps({"type": "error", "message": f"Scientific Validation Failure: {str(e)}"}) + "\n"
        except Exception:
            yield json.dumps({"type": "error", "message": "Unexpected server failure"}) + "\n"

    return StreamingResponse(event_source(), media_type="application/x-ndjson")
