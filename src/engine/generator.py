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
            rule_id=str(uuid.uuid5(uuid.NAMESPACE_OID, f"rule-{seed}-{complexity}")),
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
        
        rels_str = ", ".join(f"{a} > {b}" for a, b in relations)
        query = (variables[0], variables[-1])
        input_rep = f"Given: {rels_str}. Is {query[0]} > {query[1]}?"
        
        is_true = GroundTruthSolver.solve_transitive_chain(variables, relations, query)
        
        return Task(
            task_id=str(uuid.uuid5(uuid.NAMESPACE_OID, f"task-{rule.rule_id}-{seed}-{extrapolation_distance}")),
            rule_id=rule.rule_id,
            seed=seed,
            complexity=rule.complexity,
            extrapolation_distance=extrapolation_distance,
            input_representation=input_rep,
            expected_output=is_true,
            generator_version="1.0.0"
        )
