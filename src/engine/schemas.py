from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class Rule(BaseModel):
    rule_id: str
    rule_family: str
    parameters: Dict[str, Any]
    complexity: int
    seed: int
    generator_version: str

class Task(BaseModel):
    task_id: str
    rule_id: str
    seed: int
    complexity: int
    extrapolation_distance: int
    input_representation: str
    expected_output: bool
    generator_version: str

class Demonstration(BaseModel):
    demo_id: str
    input_representation: str
    expected_output: bool
    complexity: int
    metadata: Dict[str, Any]

class PredictionResult(BaseModel):
    task_id: str
    prediction: Optional[bool]
    raw_output: str
    correctness: str  # 'CORRECT', 'INCORRECT', 'MALFORMED', 'ERROR'
    evaluator_name: str
    model_name: Optional[str]
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ExperimentConfig(BaseModel):
    experiment_id: str
    task_family: str
    demonstration_count: int
    demonstration_complexity: int
    extrapolation_levels: List[int]
    tasks_per_level: int
    master_seed: int
    evaluator: str

class ExperimentResult(BaseModel):
    experiment_id: str
    config: ExperimentConfig
    demonstration_coverage: int
    tasks_evaluated: int
    cliff_detected: bool
    cliff_type: str
    estimated_cliff_location: Optional[int]
    level_metrics: Dict[int, Dict[str, Any]]
    raw_results: List[PredictionResult]
