---
title: Coverage Cliff
emoji: 📉
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# Coverage Cliff — Demonstration Coverage and Extrapolation

**DataForge 2026 — Pathway Track**

Interactive scientific laboratory investigating demonstration coverage and out-of-distribution extrapolation in reasoning models.

## Falsifiable Claim

> "A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."

## Features

- **Deterministic Experiment Engine**: Generates relational transitive inference tasks with verified independent ground truth (via Z3 constraint solver).
- **Real-Time Streaming**: Dispatches live task generation, evaluation, and accuracy calculation events via streaming NDJSON.
- **Dynamic Accuracy Curve**: Plots accuracy across extrapolation distances ($D_{\text{ext}} = C_{\text{test}} - C_{\text{max}}$) to detect and classify sharp coverage cliffs.
- **Task Explorer**: Inspects task representations, evaluator predictions, and reveals independently verified ground truth.
- **BDH-CQ Context**: Educational module contextualizing latent reasoning mechanisms and in-context learning boundaries.

## Architecture

- **Backend**: FastAPI + Uvicorn + Z3 theorem prover
- **Frontend**: Next.js 16 + React 19 + Tailwind CSS (compiled static export)
- **Deployment**: Single container serving API (`/api/v1/*`) and UI (`/`) on port `7860`.
