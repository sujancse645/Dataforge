# Dataforge
Coverage Cliff Project.

## Architecture
```text
Phase 3/4 Frontend (Next.js) -> Includes Coverage Cliff UI & BDH-CQ Educational Module
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

## Scientific Integrity
- **Ground Truth Independence**: Ground truth is computed by Z3 independently of the model prediction.
- **Data Leakage**: The API strictly validates requests. Evaluators receive only representations meant for a model. Hidden rule parameters and seeds are isolated.
- **Synthetic Evaluator**: The current deterministic evaluator is used purely for infrastructure testing and synthetic cliff detection. It is not real model evidence.

## BDH-CQ Educational Module
The frontend includes a substantive educational module on BDH-CQ, serving as a frontier architecture contrast to the deterministic evaluator. 

### Disclosures & Provenance
- **AI-Assisted Development**: The development of this repository (including the engine, backend, and interactive UI) was assisted by AI agents following a strict scientific prompt sequence.
- **Reused / Open-Source Code**: No proprietary BDH-CQ official inference code is redistributed. The application uses standard MIT-licensed React, Next.js, and Tailwind CSS templates.
- **Toy Implementation**: The BDH-CQ module features an interactive visualizer for latent state updates. This is explicitly an **educational toy abstraction** and does not run an official BDH-CQ checkpoint.
- **Primary Sources**: Claims within the BDH-CQ module are derived from the *Dragon Hatchling* paper and the *BDH-CQ Technical Report*. See `docs/sources.md` for a full mapping.
