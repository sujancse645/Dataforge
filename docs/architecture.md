# Technical Architecture

## Overview
Coverage Cliff is built on a strictly decoupled three-tier architecture ensuring scientific validity, zero data leakage, and interactive educational visualizations.

```text
Frontend (Next.js)
        ↓
FastAPI (REST API)
        ↓
ExperimentRunner
        ↓
Task Generator
        ↓
Independent Ground Truth (Z3 Solver)
        ↓
Evaluator (Deterministic Reference)
        ↓
Metrics
        ↓
Cliff Detector
        ↓
ExperimentResult
        ↓
Frontend Visualization
```

## Layer Responsibilities

### 1. Frontend (Next.js & Tailwind CSS)
- **Role**: Pure visualization and interaction layer.
- **Rules**: The frontend does *not* independently calculate scientific results, accuracy, or cliff locations. It strictly renders the JSON payload returned by the FastAPI backend. It also houses the static BDH-CQ educational material, which is not mixed into the live Coverage Cliff evaluator.

### 2. FastAPI Backend (`src/api`)
- **Role**: API routing and request validation.
- **Rules**: Exposes endpoints (`/api/v1/experiments`). Validates incoming configurations (Seeds, Coverage parameters) using Pydantic schemas. 

### 3. Experiment Engine (`src/engine`)
- **Role**: The scientific core.
- **Task Generator**: Uses the master seed to deterministically construct tasks and demonstrations. 
- **Independent Ground Truth**: Uses a Z3 mathematical solver to compute exact answers independently.
- **Evaluator**: A decoupled component that receives *only* the string representations of the demonstrations and the test queries. It evaluates predictions without exposing hidden generator information.
- **Metrics & Cliff Detector**: Compares predictions against ground truth, calculates accuracy vectors, and statistically classifies the boundary (e.g., `SHARP_CLIFF`, `STABLE`).

## Design Philosophy
- **Zero Leakage**: Ground truth and prediction evaluation remain absolutely separated. The evaluator has no access to the hidden rule or the solver's logic.
- **Reproducibility**: The entire pipeline relies on seeded randomness. The identical configuration yields identical deterministic results across CLI, API, and UI.
