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
