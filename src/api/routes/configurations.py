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
