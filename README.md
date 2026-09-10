# Coverage Cliff — Demonstration Coverage and Extrapolation

**DataForge 2026 — Pathway Track**  
**Author / Team:** Sujan L  
**Live Application:** [https://sujan007123-coverage-cliff.hf.space](https://sujan007123-coverage-cliff.hf.space)  
**Source Repository:** [https://github.com/sujancse645/Dataforge](https://github.com/sujancse645/Dataforge)  

---

## 1. Central Falsifiable Claim

> "A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."

*This is a task- and model-specific empirical hypothesis under controlled conditions, not an asserted universal law of AI.*

---

## 2. Intended Learner, Prerequisites & Learning Objectives

- **Intended Learner:** AI engineers, researchers, and students interested in in-context learning, out-of-distribution reasoning limits, and evaluation rigor.
- **Prerequisites:** Basic familiarity with relational reasoning (e.g., transitive comparisons $A > B > C$) and supervised evaluation concepts (accuracy, test splits).
- **Learning Objectives:**
  1. Understand the difference between in-demonstration coverage ($C_{\text{max}}$) and extrapolation distance ($D_{\text{ext}} = C_{\text{test}} - C_{\text{max}}$).
  2. Experience how an evaluator can display 100% accuracy within demonstrated bounds while failing abruptly when complexity exceeds those bounds.
  3. Recognize the necessity of independent ground-truth solvers (such as SMT solvers) to prevent circularity and data leakage in evaluation.
  4. Understand how latent recurrent architectures (e.g., BDH-CQ) attempt to reason without generating textual chain-of-thought traces, and distinguish theoretical capability from empirical boundaries.

---

## 3. System Architecture & Component Roles

```
┌────────────────────────────────────────────────────────┐
│             Interactive Browser Frontend               │
│   (Next.js 16 + React 19 + Tailwind CSS + Chart)       │
└───────────────────────────┬────────────────────────────┘
                            │ Streaming NDJSON / REST
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
│  (/api/v1/experiments/stream, /configurations, /health)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                Experiment Engine Runner                │
│    (TaskGenerator ──► Evaluator ──► MetricsCalculator)  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│          Independent Z3 SMT Constraint Solver          │
│       (Formal Ground-Truth Verification - Zero Leak)   │
└────────────────────────────────────────────────────────┘
```

- **`src/engine/generator.py`**: Procedurally generates relational task instances across controlled complexity levels.
- **`src/engine/solver.py`**: Independent Z3 theorem prover calculating exact ground-truth satisfaction without evaluator leakage.
- **`src/engine/evaluator.py`**: Reference evaluator bounded by relational pattern capacity.
- **`src/engine/runner.py`**: Orchestrates sweep executions and yields real-time streaming progress events.
- **`src/api/`**: FastAPI routing layer exposing health checks, parameter configurations, and real-time streaming NDJSON endpoints.
- **`apps/web/`**: Next.js client interface compiled to a static export (`apps/web/out`) and served directly by FastAPI.

---

## 4. Evidence Classification

- **Live Computation:** Real-time generation of task chains, Z3 ground-truth resolution, evaluator inference, and accuracy classification.
- **Precomputed:** Baseline calibration values recorded in `data/results.json` and preregistered in `data/manifest.json`.
- **Synthetic / Procedural:** All relational symbolic tasks ($A > B$) generated algorithmically from seeded pseudorandom distributions.
- **Animated:** Real-time stream telemetry and live bar chart transitions indicating dynamic evaluation progress.
- **Published:** Conceptual and architectural motifs cited from peer-reviewed literature (BDH-CQ, Coconut).

---

## 5. Measured Results

All metrics below are drawn directly from `data/results.json` produced by running the deterministic reference engine (`master_seed = 2026`, $C_{\text{max}} = 2$):

| Extrapolation Level | Distance ($D_{\text{ext}}$) | Evaluated Tasks | Correct | Measured Accuracy |
| :---: | :---: | :---: | :---: | :---: |
| **Level +0** | 0 | 5 | 5 | **100.0%** |
| **Level +1** | 1 | 5 | 5 | **100.0%** |
| **Level +2** | 2 | 5 | 5 | **100.0%** |
| **Level +3** | 3 | 5 | 0 | **0.0%** |
| **Level +4** | 4 | 5 | 0 | **0.0%** |

- **Tasks Evaluated:** 25 total
- **Cliff Detected:** `True`
- **Cliff Classification:** `SHARP_CLIFF`
- **Estimated Cliff Boundary:** $D_{\text{ext}} = 3$

---

## 6. Preregistration

The experimental hypothesis, independent variable ($D_{\text{ext}}$), dependent variable (accuracy), and predicted cliff location were formally preregistered prior to calibration sweeps in [`data/manifest.json`](data/manifest.json) with frozen timestamp **`2026-09-05T07:20:00Z`**. The observed empirical cliff location ($D_{\text{ext}} = 3$) exactly corroborates the preregistered structural prediction.

---

## 7. Experimental Controls & Confound Disclosures

### Automated Confound Checks (from `tests/`)
1. **Independent Verification (`test_ground_truth_solver_valid`)**: Ground truth is computed via the Z3 SMT solver independent of generator metadata. (10/10 tests pass in 0.74s).
2. **Degeneracy Handling (`test_ground_truth_solver_degenerate`)**: Contradictory, cyclic, or underdetermined relations are detected and rejected.
3. **Determinism & Reproducibility (`test_reproducibility`)**: Identical seed configurations produce identical outputs down to the bit level across runs.
4. **CLI/API Parity (`test_cli_api_parity`)**: Asserts numerical parity between CLI runs and HTTP API responses.

### Disclosed Known Confounds
- **Fixed Vocabulary Size**: Node labels are drawn from a finite symbolic alphabet ($A \dots Z$). At higher levels, token reuse is constrained by design.
- **Static Demonstration Order**: Demonstrations are presented in monotonic canonical order rather than permuted, providing a consistent structural anchor.

---

## 8. Limitations

> This is not BDH-CQ. It is a hand-built associative memory using published BDH-GPU motifs; BDH-CQ's dimensions and update rules are stated as proprietary in its paper, and we ran no BDH or BDH-CQ checkpoint. Our features are hand-designed, so the location of the cliff depends on our bucketing. Qualitative agreement is not reproduction. Results come from a small number of task families and do not establish that the effect generalises across visual operations.

---

## 9. Primary Sources & Citations

- **Kosowski et al.** (2025). *The Dragon Hatchling*. arXiv:2509.26507. Cited for exploration of recurrent latent updates in post-transformer architectures.
- **Engdahl et al.** (2026). *BDH-CQ: Demonstration-Driven In-Context Learning Without Chain of Thought*. arXiv:2608.09888. Cited for associative memory dynamics and demonstration coverage queries.
- **Hao et al.** (2024). *Training Large Language Models to Reason in a Continuous Latent Space (Coconut)*. arXiv:2412.06769. Cited for continuous latent reasoning versus explicit token generation.
- **Geiping et al.** (2025). *Recurrent Depth in Language Models*. arXiv:2502.05171. Cited for iterative recurrence over fixed depth.

---

## 10. How to Reproduce Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated test suite
pytest tests/ -v

# 3. Run deterministic engine smoke test
python smoke_test.py

# 4. Launch unified full-stack server
python -m uvicorn src.api.main:app --reload
```
Navigate to **http://127.0.0.1:8000**.

---

## 11. Credits & License

Authored by **Sujan L** for the Pathway / DataForge 2026 Hackathon (Pathway Track).  
Licensed under the [MIT License](LICENSE).
