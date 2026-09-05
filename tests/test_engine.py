import pytest
from src.engine.schemas import ExperimentConfig
from src.engine.runner import ExperimentRunner
from src.engine.solver import GroundTruthSolver

def test_ground_truth_solver_valid():
    # A > B, B > C => A > C
    relations = [("A", "B"), ("B", "C")]
    variables = ["A", "B", "C"]
    assert GroundTruthSolver.solve_transitive_chain(variables, relations, ("A", "C")) == True
    assert GroundTruthSolver.solve_transitive_chain(variables, relations, ("C", "A")) == False

def test_ground_truth_solver_degenerate():
    # A > B, B > A (unsat)
    relations = [("A", "B"), ("B", "A")]
    variables = ["A", "B"]
    with pytest.raises(ValueError, match="Degenerate task"):
        GroundTruthSolver.solve_transitive_chain(variables, relations, ("A", "B"))

def test_runner_deterministic_cliff():
    config = ExperimentConfig(
        experiment_id="test_01",
        task_family="Transitive Inference",
        demonstration_count=3,
        demonstration_complexity=2,
        extrapolation_levels=[0, 1, 2, 3, 4],
        tasks_per_level=10,
        master_seed=42,
        evaluator="deterministic"
    )
    runner = ExperimentRunner(config)
    result = runner.run()
    
    assert result.cliff_detected == True
    assert result.cliff_type == "SHARP_CLIFF"
    assert result.estimated_cliff_location == 3
    
    assert result.level_metrics[0]["accuracy"] == 1.0
    assert result.level_metrics[3]["accuracy"] == 0.0

def test_reproducibility():
    config = ExperimentConfig(
        experiment_id="test_02",
        task_family="Transitive Inference",
        demonstration_count=1,
        demonstration_complexity=2,
        extrapolation_levels=[0, 1],
        tasks_per_level=2,
        master_seed=99,
        evaluator="deterministic"
    )
    runner1 = ExperimentRunner(config)
    res1 = runner1.run()
    
    runner2 = ExperimentRunner(config)
    res2 = runner2.run()
    
    assert res1.raw_results[0].task_id == res2.raw_results[0].task_id
    assert res1.raw_results[0].prediction == res2.raw_results[0].prediction
