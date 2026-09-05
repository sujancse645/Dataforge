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
