# Experimental Calibration & Tuning Log

## Experiment Calibration Summary

- **Task Family**: Symbolic Logic / Transitive Inference over relational chains ($A > B > C \dots$).
- **Solver Mechanism**: Z3 Theorem Prover independent solver with formal constraint satisfaction checks.
- **Reference Sweep Parameters**:
  - `master_seed`: 2026
  - `demonstration_complexity`: 2 ($C_{\text{max}} = 2$)
  - `extrapolation_levels`: [0, 1, 2, 3, 4]
  - `tasks_per_level`: 5 (25 total tasks)
- **Measured Threshold**:
  - Level +0 ($D_{\text{ext}} = 0$): 5/5 correct (100%)
  - Level +1 ($D_{\text{ext}} = 1$): 5/5 correct (100%)
  - Level +2 ($D_{\text{ext}} = 2$): 5/5 correct (100%)
  - Level +3 ($D_{\text{ext}} = 3$): 0/5 correct (0.0%)
  - Level +4 ($D_{\text{ext}} = 4$): 0/5 correct (0.0%)
- **Conclusion**: Sharp boundary observed at $D_{\text{ext}} = 3$. Evaluator capacity is strictly bounded by demonstrated relational chain depth.
