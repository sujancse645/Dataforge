import os

files = {
    "src/engine/generator.py": """
import random
import uuid
from .schemas import Rule, Task, Demonstration
from .solver import GroundTruthSolver

class TaskGenerator:
    @staticmethod
    def generate_rule(seed: int, complexity: int) -> Rule:
        rng = random.Random(seed)
        variables = [chr(65 + i) for i in range(complexity + 1)] # A, B, C...
        parameters = {"variables": variables, "relations": []}
        for i in range(complexity):
            parameters["relations"].append([variables[i], variables[i+1]]) # A > B, B > C
            
        return Rule(
            rule_id=str(uuid.uuid4()),
            rule_family="Transitive Inference",
            parameters=parameters,
            complexity=complexity,
            seed=seed,
            generator_version="1.0.0"
        )

    @staticmethod
    def calculate_coverage(demonstrations: list[Demonstration]) -> int:
        return max(d.complexity for d in demonstrations)

    @staticmethod
    def generate_task(rule: Rule, seed: int, extrapolation_distance: int, is_demo: bool = False) -> Task:
        rng = random.Random(seed)
        variables = rule.parameters["variables"]
        relations = rule.parameters["relations"]
        
        # Format input string
        rels_str = ", ".join(f"{a} > {b}" for a, b in relations)
        # Randomly choose a query (for simplicity, we ask if the first > the last)
        query = (variables[0], variables[-1])
        input_rep = f"Given: {rels_str}. Is {query[0]} > {query[1]}?"
        
        # Ground truth
        is_true = GroundTruthSolver.solve_transitive_chain(variables, relations, query)
        
        return Task(
            task_id=str(uuid.uuid4()),
            rule_id=rule.rule_id,
            seed=seed,
            complexity=rule.complexity,
            extrapolation_distance=extrapolation_distance,
            input_representation=input_rep,
            expected_output=is_true,
            generator_version="1.0.0"
        )
""",
    "src/engine/evaluator.py": """
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
        # Simulate perfect performance inside coverage, and failure at failure_distance
        prediction = task.expected_output
        if task.extrapolation_distance >= self.failure_distance:
            prediction = not task.expected_output # Deliberately wrong
            
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
""",
    "src/engine/metrics.py": """
from typing import List, Dict, Any
from .schemas import PredictionResult

class MetricsCalculator:
    @staticmethod
    def calculate_level_metrics(results: List[PredictionResult]) -> Dict[str, Any]:
        total = len(results)
        if total == 0:
            return {"accuracy": 0.0, "error_rate": 0.0, "total": 0}
        correct = sum(1 for r in results if r.correctness == 'CORRECT')
        return {
            "accuracy": correct / total,
            "error_rate": (total - correct) / total,
            "total": total
        }

    @staticmethod
    def detect_cliff(level_accuracies: Dict[int, float]) -> tuple[bool, str, int]:
        \"\"\"
        Returns (cliff_detected, cliff_type, estimated_location)
        \"\"\"
        if not level_accuracies:
            return False, "INSUFFICIENT_DATA", -1
            
        distances = sorted(level_accuracies.keys())
        if len(distances) < 2:
            return False, "INSUFFICIENT_DATA", -1
            
        base_acc = level_accuracies.get(0, level_accuracies[distances[0]])
        if base_acc < 0.6:
            return False, "FLOOR", -1
            
        for dist in distances[1:]:
            acc = level_accuracies[dist]
            drop = base_acc - acc
            if drop > 0.3:
                return True, "SHARP_CLIFF", dist
                
        if base_acc - level_accuracies[distances[-1]] > 0.1:
            return False, "GRADUAL_DEGRADATION", -1
            
        return False, "STABLE", -1
""",
    "src/engine/runner.py": """
from typing import List
from .schemas import ExperimentConfig, ExperimentResult, Rule, Demonstration
from .generator import TaskGenerator
from .evaluator import DeterministicReferenceEvaluator
from .metrics import MetricsCalculator

class ExperimentRunner:
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.evaluator = DeterministicReferenceEvaluator()
        
    def run(self) -> ExperimentResult:
        demonstrations = []
        for i in range(self.config.demonstration_count):
            rule = TaskGenerator.generate_rule(self.config.master_seed + i, self.config.demonstration_complexity)
            task = TaskGenerator.generate_task(rule, self.config.master_seed + i, 0, True)
            demonstrations.append(Demonstration(
                demo_id=task.task_id,
                input_representation=task.input_representation,
                expected_output=task.expected_output,
                complexity=task.complexity,
                metadata={}
            ))
            
        coverage = TaskGenerator.calculate_coverage(demonstrations)
        
        all_results = []
        level_metrics = {}
        
        for level in self.config.extrapolation_levels:
            level_tasks = []
            for t_idx in range(self.config.tasks_per_level):
                seed = self.config.master_seed + 100 * level + t_idx
                rule = TaskGenerator.generate_rule(seed, self.config.demonstration_complexity + level)
                task = TaskGenerator.generate_task(rule, seed, level)
                
                result = self.evaluator.evaluate(task, demonstrations)
                all_results.append(result)
                level_tasks.append(result)
                
            level_metrics[level] = MetricsCalculator.calculate_level_metrics(level_tasks)
            
        acc_dict = {lvl: metrics["accuracy"] for lvl, metrics in level_metrics.items()}
        cliff_detected, cliff_type, cliff_loc = MetricsCalculator.detect_cliff(acc_dict)
        
        return ExperimentResult(
            experiment_id=self.config.experiment_id,
            config=self.config,
            demonstration_coverage=coverage,
            tasks_evaluated=len(all_results),
            cliff_detected=cliff_detected,
            cliff_type=cliff_type,
            estimated_cliff_location=cliff_loc if cliff_loc != -1 else None,
            level_metrics=level_metrics,
            raw_results=all_results
        )
"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\\n")
