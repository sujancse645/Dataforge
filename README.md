# Dataforge
Coverage Cliff Project.

## Architecture
```text
Phase 3 Frontend (Next.js)
      ↓
Phase 2 API (FastAPI)
      ↓
Phase 1 Engine (Python)
      ↓
Generator (Task / Rule generation)
      ↓
Independent Solver (Z3 / Algebraic)
      ↓
Evaluator (Deterministic Reference)
      ↓
Metrics & Cliff Detection
```

## Running the Backend
Ensure you have `fastapi` and `uvicorn` installed.
To start the FastAPI backend server:
```bash
python -m uvicorn src.api.main:app --reload
```
API Documentation: `http://127.0.0.1:8000/docs`

## Running the Frontend
The interactive frontend is located in `apps/web`.
```bash
cd apps/web
npm install
npm run dev
```
Navigate to `http://localhost:3000`. 
*(Note: If the backend runs on a different port, set `NEXT_PUBLIC_API_BASE_URL` in an `.env` file).*

## Running Tests
Run the entire backend test suite (Engine + API tests):
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
