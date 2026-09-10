# START HERE — Coverage Cliff

**DataForge 2026 — Pathway Track**  
**Team / Author:** Sujan L  
**Live Artifact URL:** [https://sujan007123-coverage-cliff.hf.space](https://sujan007123-coverage-cliff.hf.space) *(Public, no sign-in required)*  
**Source Repository URL:** [https://github.com/sujancse645/Dataforge](https://github.com/sujancse645/Dataforge) *(Public, no sign-in required)*  

---

## Central Claim (from `SPEC.md`)

> "A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."

---

## Try it in 60 Seconds

1. **Launch the Laboratory:** Open the live artifact URL ([https://sujan007123-coverage-cliff.hf.space](https://sujan007123-coverage-cliff.hf.space)) or run locally at `http://127.0.0.1:8000`.
2. **Run Reference Experiment:** With default parameters (Seed: `2026`, Demonstration Coverage $C_{\text{max}}$: `2`), click **RUN THE EXPERIMENT**. Watch the live feed stream evaluations and plot the sharp accuracy cliff dropping from 100% to 0% at extrapolation distance $+3$.
3. **Inspect & Challenge:** In the **Task Explorer**, inspect a Level $+3$ task and click **Reveal Ground Truth** to verify the failure against the independent Z3 solver. Then click **Challenge the Claim** to increment the seed and observe boundary behavior under a newly seeded universe.

---

## Evidence Classification

- **LIVE EXPERIMENT:** All task generation, reference evaluator predictions, independent Z3 ground-truth solving, streaming NDJSON progress, and cliff classifications are calculated dynamically by the engine.
- **PRECOMPUTED / REGISTERED:** The calibration benchmarks recorded in `data/results.json` and preregistered in `data/manifest.json`.
- **PUBLISHED:** Theoretical background and architectural motifs cited from published literature (Engdahl et al. 2026, Kosowski et al. 2025).

---

## Reproduce Locally (Tested)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated test suite
pytest tests/ -v

# 3. Run deterministic engine benchmark
python smoke_test.py

# 4. Start full-stack application (serves UI + API on port 8000)
python -m uvicorn src.api.main:app --reload
```
Open **http://127.0.0.1:8000** in any browser.
