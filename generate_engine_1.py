import os

files = {
    "src/engine/__init__.py": "",
    "src/engine/schemas.py": """
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
""",
    "src/engine/solver.py": """
import z3

class GroundTruthSolver:
    @staticmethod
    def solve_transitive_chain(variables: list[str], relations: list[tuple[str, str]], query: tuple[str, str]) -> bool:
        \"\"\"
        relations is a list of (A, B) meaning A > B.
        query is (X, Y) asking if X > Y is true.
        \"\"\"
        solver = z3.Solver()
        z3_vars = {v: z3.Int(v) for v in variables}
        
        for a, b in relations:
            solver.add(z3_vars[a] > z3_vars[b])
            
        # Check if relations are satisfiable
        if solver.check() != z3.sat:
            raise ValueError("Degenerate task: Relations are unsatisfiable.")
            
        # To prove X > Y, we show that (X <= Y) is unsatisfiable given the relations
        solver.push()
        solver.add(z3_vars[query[0]] <= z3_vars[query[1]])
        is_true = (solver.check() == z3.unsat)
        solver.pop()
        
        # Secondary algebraic check
        # Build adjacency list for >
        adj = {v: [] for v in variables}
        for a, b in relations:
            adj[a].append(b)
            
        # BFS/DFS to find path from query[0] to query[1]
        visited = set()
        queue = [query[0]]
        found_path = False
        while queue:
            curr = queue.pop(0)
            if curr == query[1]:
                found_path = True
                break
            if curr not in visited:
                visited.add(curr)
                queue.extend(adj[curr])
                
        if found_path != is_true:
            raise ValueError("Validation failure: Z3 and algebraic checker disagree!")
            
        return is_true
"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\\n")
