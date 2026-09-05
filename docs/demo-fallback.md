# Live Demo Fallback Plan

If the backend API service becomes unavailable during judging:

1. **Do NOT pretend the app is still running.**
2. Acknowledge the failure clearly: "The live experiment service is unavailable at the moment."
3. Open the API documentation or `docs/one-page-summary.md` to demonstrate the intended flow.
4. Open the recorded test logs (`pytest` output or `smoke_test.py` output) to prove the deterministic capabilities of the engine.
5. Explain that the results in the log are "PRECOMPUTED / RECORDED RESULTS" and are not a live run.
6. Pivot immediately to explaining the technical architecture, focusing on the rigorous separation between independent ground truth (Z3 solver) and the evaluator.
