from abc import ABC, abstractmethod
from .schemas import Task, Demonstration, PredictionResult

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, task: Task, demonstrations: list[Demonstration]) -> PredictionResult:
        pass

class DeterministicReferenceEvaluator(BaseEvaluator):
    def __init__(self, failure_distance: int = 3):
        self.failure_distance = failure_distance
        
    def evaluate(self, task: Task, demonstrations: list[Demonstration]) -> PredictionResult:
        prediction = task.expected_output
        if task.extrapolation_distance >= self.failure_distance:
            prediction = not task.expected_output
            
        correctness = 'CORRECT' if prediction == task.expected_output else 'INCORRECT'
        return PredictionResult(
            task_id=task.task_id,
            prediction=prediction,
            raw_output=str(prediction),
            correctness=correctness,
            evaluator_name="DETERMINISTIC_REFERENCE",
            model_name="deterministic_mock",
            metadata={}
        )
