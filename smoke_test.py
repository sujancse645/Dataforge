from src.engine.schemas import ExperimentConfig
from src.engine.runner import ExperimentRunner
import json

if __name__ == "__main__":
    print("Running Experiment Engine Smoke Test...")
    config = ExperimentConfig(
        experiment_id="smoke_01",
        task_family="Transitive Inference",
        demonstration_count=3,
        demonstration_complexity=2,
        extrapolation_levels=[0, 1, 2, 3, 4],
        tasks_per_level=5,
        master_seed=2026,
        evaluator="deterministic"
    )
    runner = ExperimentRunner(config)
    result = runner.run()
    
    print("\\n=== SMOKE TEST SUMMARY ===")
    print(f"Task Family: {config.task_family}")
    print(f"Master Seed: {config.master_seed}")
    print(f"Demonstration Coverage: {result.demonstration_coverage}")
    print(f"Tasks Evaluated: {result.tasks_evaluated}")
    
    print("\\nAccuracy by Extrapolation Level:")
    for lvl, metrics in result.level_metrics.items():
        print(f"  Level {lvl}: {metrics['accuracy']*100:.1f}%")
        
    print(f"\\nCliff Detected: {result.cliff_detected}")
    if result.cliff_detected:
        print(f"Cliff Type: {result.cliff_type}")
        print(f"Estimated Location (distance): {result.estimated_cliff_location}")
    print("==========================")
