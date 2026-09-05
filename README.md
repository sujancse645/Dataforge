# Dataforge
Coverage Cliff Project.

## Architecture
```text
Future Frontend (Next.js)
      ↓
FastAPI API (src/api)
      ↓
ExperimentRunner (src/engine/runner.py)
      ↓
Generator (Task / Rule generation)
      ↓
Independent Solver (Z3 / Algebraic)
      ↓
Evaluator (Deterministic Reference)
      ↓
Metrics & Cliff Detection
      ↓
ExperimentResult
```

## Running the Backend
Ensure you have `fastapi` and `uvicorn` installed.
To start the FastAPI backend server:
```bash
python -m uvicorn src.api.main:app --reload
```

## API Documentation
When the server is running, interactive API documentation is available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Running Tests
Run the entire test suite (Engine + API tests):
```bash
$env:PYTHONPATH="."
pytest
```
Or run the API smoke test directly:
```bash
python api_smoke_test.py
```

## Scientific Integrity
- **Ground Truth Independence**: Ground truth is computed by Z3 independently of the model prediction.
- **Data Leakage**: The API strictly validates requests. Evaluators receive only representations meant for a model. Hidden rule parameters and seeds are isolated.
- **Synthetic Evaluator**: The current deterministic evaluator is used purely for infrastructure testing and synthetic cliff detection. It is not real model evidence.
