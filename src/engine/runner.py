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
