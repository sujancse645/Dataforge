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
