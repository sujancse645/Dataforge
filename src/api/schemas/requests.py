from pydantic import BaseModel, Field
from typing import List

class ExperimentRequest(BaseModel):
    master_seed: int = Field(..., description="Master seed for deterministic generation")
    demonstration_count: int = Field(..., gt=0, le=10, description="Number of demonstrations")
    demonstration_complexity: int = Field(..., gt=0, le=5, description="Complexity of demonstrations")
    extrapolation_levels: List[int] = Field(..., description="List of extrapolation distances")
    tasks_per_level: int = Field(..., gt=0, le=50, description="Tasks to evaluate per level")
    evaluator_type: str = Field(..., description="Type of evaluator to use")
