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

        correct = prediction == task.expected_output
        return PredictionResult(
            task_id=task.task_id,
            complexity=task.complexity,
            extrapolation_distance=task.extrapolation_distance,
            input_representation=task.input_representation,
            prediction=str(prediction),
            ground_truth=str(task.expected_output),
            correct=correct,
            raw_output=str(prediction),
            correctness='CORRECT' if correct else 'INCORRECT',
            evaluator_name="DETERMINISTIC_REFERENCE",
            model_name="deterministic_mock",
            metadata={}
        )
