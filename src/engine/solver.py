import z3

class GroundTruthSolver:
    @staticmethod
    def solve_transitive_chain(variables: list[str], relations: list[tuple[str, str]], query: tuple[str, str]) -> bool:
        solver = z3.Solver()
        z3_vars = {v: z3.Int(v) for v in variables}
        
        for a, b in relations:
            solver.add(z3_vars[a] > z3_vars[b])
            
        if solver.check() != z3.sat:
            raise ValueError("Degenerate task: Relations are unsatisfiable.")
            
        solver.push()
        solver.add(z3_vars[query[0]] <= z3_vars[query[1]])
        is_true = (solver.check() == z3.unsat)
        solver.pop()
        
        adj = {v: [] for v in variables}
        for a, b in relations:
            adj[a].append(b)
            
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
