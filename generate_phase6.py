import os

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "docs/presentation-outline.md": """
# Final Presentation Outline

## SLIDE 1 — HOOK
COVERAGE CLIFF
"How far can a model generalize beyond what its demonstrations actually cover?"

## SLIDE 2 — THE PROBLEM
Models are often evaluated on whether they get an answer right.
But that leaves a deeper question:
"How far beyond demonstrated examples does that success extend?"
Demonstrations → Coverage → Extrapolation → Accuracy → Boundary

## SLIDE 3 — OUR FALSIFIABLE CLAIM
"A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."
NOT A UNIVERSAL LAW. We test it under controlled conditions.

## SLIDE 4 — HOW THE EXPERIMENT WORKS
Demonstrations ↓
Cmax ↓
Test complexity ↓
Dext ↓
Prediction ↓
Independent Ground Truth ↓
Accuracy ↓
Cliff Detector

## SLIDE 5 — LIVE RESULT
(Show the actual accuracy curve highlighting the observed boundary)
"Under this configuration, we observe a sharp cliff at extrapolation distance 3."

## SLIDE 6 — CHALLENGE THE CLAIM
Show how changing seed, coverage, or extrapolation range creates a new experiment.
"A scientific claim should be testable, not merely demonstrated once."

## SLIDE 7 — BDH-CQ CONNECTION
Coverage Cliff: OUR LIVE EXPERIMENT
BDH-CQ: SOURCE-GROUNDED TECHNICAL CONTEXT
"We did not establish whether BDH-CQ has a Coverage Cliff under our conditions."

## SLIDE 8 — IMPACT / FUTURE WORK
Future work:
- real model evaluators
- multiple task families
- matched BDH-CQ experiments
"Instead of asking only whether a model generalizes, we can ask where that generalization stops."
""",
    "docs/pitch-60-seconds.md": """
# 60-Second Pitch

**HOOK:**
"Most AI demos ask one question: Can the model solve this example? We ask a harder one: How far can it generalize beyond what its demonstrations actually cover?"

**PROBLEM:**
"A model can look perfect on examples similar to what it has seen. But that doesn't tell us where its demonstrated coverage ends."

**SOLUTION:**
"Coverage Cliff turns that boundary into an experiment. We generate demonstrations, define their coverage, then progressively push the same rule beyond that coverage. Every prediction is compared against independently computed exact ground truth."

**RESULT:**
"In our reference experiment, accuracy remains perfect through the demonstrated range and then drops sharply at a specific extrapolation distance."

**HONESTY:**
"That does NOT prove every AI model has a universal cliff. It proves that this controlled experiment can expose and measure a boundary."

**BDH-CQ:**
"We then connect this idea to BDH-CQ, a research system studying demonstration-driven reasoning without a written chain-of-thought trace. But we keep that evidence separate: we did not test BDH-CQ for a Coverage Cliff."

**CLOSING:**
"Coverage Cliff is not just asking whether a model generalizes. It asks where that generalization stops."
""",
    "docs/pitch-30-seconds.md": """
# 30-Second Pitch

"Coverage Cliff is an interactive scientific experiment for measuring how far a model can generalize beyond its demonstrations.

We define demonstration coverage, push the same rule into controlled extrapolation, compare predictions against independent exact ground truth, and plot accuracy to detect where performance changes.

Our reference experiment produces a sharp boundary.

We don't claim that's universal AI behavior.

We built a reproducible way to measure the boundary."
""",
    "docs/reproducibility.md": """
# Reproducibility

## 1. Environment requirements
- Python 3.11+
- Node.js 18+

## 2. Backend start command
```bash
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload
```

## 3. Frontend start command
```bash
cd apps/web
npm install
npm run dev
```

## 4. Test command
```bash
pytest
```

## 5. Smoke test command
```bash
python smoke_test.py
python api_smoke_test.py
```

## 6. Reference experiment configuration
- **Master Seed**: 2026
- **Demonstration Coverage (Cmax)**: 2
- **Extrapolation Range**: 0-4
- **Tasks per level**: 5

## 7. Expected qualitative behavior
The evaluator will correctly solve levels 0, 1, 2 (100% accuracy). At level 3 and beyond, accuracy will sharply drop to 0%. The UI will report `SHARP_CLIFF`.

## 8. How to reproduce
Ensure the UI inputs exactly match the Reference experiment configuration above, then click 'RUN THE EXPERIMENT'.

## 9. What deterministic reproduction means
Our `Random Seed` drives the task generation, permutations, and selections. If the seed and parameters are exactly the same across any machine or environment, the mathematical formulations and evaluations will output the identical result. We guarantee bit-for-bit equivalence in the logical generation of the experiment.
""",
    "docs/demo-fallback.md": """
# Live Demo Fallback Plan

If the backend API service becomes unavailable during judging:

1. **Do NOT pretend the app is still running.**
2. Acknowledge the failure clearly: "The live experiment service is unavailable at the moment."
3. Open the API documentation or `docs/one-page-summary.md` to demonstrate the intended flow.
4. Open the recorded test logs (`pytest` output or `smoke_test.py` output) to prove the deterministic capabilities of the engine.
5. Explain that the results in the log are "PRECOMPUTED / RECORDED RESULTS" and are not a live run.
6. Pivot immediately to explaining the technical architecture, focusing on the rigorous separation between independent ground truth (Z3 solver) and the evaluator.
""",
    "docs/final-verification.md": """
# Final Verification Test Matrix

| Test | Result |
|---|---|
| Engine tests | PASS |
| API tests | PASS |
| Integration tests | PASS |
| Smoke test | PASS |
| API smoke test | PASS |
| Reproducibility | PASS |
| Different seed | PASS |
| Challenge flow | PASS |
| No-cliff state | PASS |
| Sharp-cliff state | PASS |
| Gradual state | PASS |
| Inconclusive state | PASS |
| Invalid request | PASS |
| API unavailable | PASS |
| Frontend build | PASS |
| TypeScript | PASS |
| Accessibility | PASS |
| Responsive layout | PASS |
| Source audit | PASS |
| Secret audit | PASS |
| Git audit | PASS |
""",
    "docs/SUBMISSION-FREEZE.md": """
# SUBMISSION FREEZE

Phase 6 submission freeze completed.

The scientific engine, API, frontend and BDH-CQ educational module were regression-tested.

Future changes should not alter scientific behavior without a new validation cycle.
"""
}

for path, content in files.items():
    write_file(path, content)

print("Phase 6 documentation applied.")
