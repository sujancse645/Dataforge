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
