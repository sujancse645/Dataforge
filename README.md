# Coverage Cliff

**How far can a model generalize beyond what its demonstrations actually cover?**

## The Falsifiable Claim
"A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."

*Note: This is a task- and model-specific hypothesis, not a universal law of AI.*

## Project Overview
Coverage Cliff is an interactive educational laboratory built for the Pathway / DataForge 2026 Pathway Track. It provides a reproducible experimental pipeline to explicitly measure the boundary between demonstrated structural coverage and true algorithmic extrapolation.

## Architecture
Our architecture enforces strict separation between task generation, predictive evaluation, and mathematically verifiable ground truth.

```text
Frontend (Next.js)
        ↓
FastAPI (REST API)
        ↓
ExperimentRunner (Python)
        ↓
Task Generator → Evaluator (Deterministic Reference)
        ↓
Independent Ground Truth (Z3 Solver)
        ↓
Metrics & Cliff Detection
```

## How to Run

### 1. Backend (FastAPI)
```bash
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload
```
The backend API documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Frontend (Next.js)
In a separate terminal:
```bash
cd apps/web
npm install
npm run dev
```
Navigate to `http://localhost:3000` to interact with the laboratory.

### 3. Tests (Complete Regression)
```bash
# Windows powershell:
$env:PYTHONPATH="."
python smoke_test.py
python api_smoke_test.py
pytest
```

## Reproducibility
Experiments are fully reproducible. By passing the identical `Random Seed` and `Demonstration Coverage` into the UI (or API/CLI), the system deterministically regenerates the exact same tasks, evaluations, and accuracy curves. 

## Methodology & Definitions
- **Demonstration Coverage (Cmax)**: The maximum structural complexity shown to the model in the prompt.
- **Extrapolation Distance (Dext)**: How far a test task exceeds the demonstrated coverage.
- **Independent Ground Truth**: A Z3 solver computes the correct answer separately from the evaluator. The evaluator only sees strings.

## Evidence Labels & BDH-CQ Integration
We provide a substantive educational module on **BDH-CQ**, a frontier architecture capable of demonstration-driven latent reasoning without written chain-of-thought traces. This material serves as technical context.
All claims in our application are labeled:
- **OUR LIVE EXPERIMENT**: Results computed deterministically by our backend.
- **PUBLISHED**: Claims directly supported by primary cited research.
- **ILLUSTRATIVE**: Conceptual visual abstractions of architectures (e.g., our toy latent visualizer).

## Limitations
1. Our current deterministic reference evaluator validates the testing infrastructure; it is not a general-purpose frontier LLM.
2. A detected "sharp cliff" demonstrates our boundary-detection capability. It does not establish that all AI systems have the same boundary.
3. We have NOT tested whether official BDH-CQ has a Coverage Cliff under our experimental conditions.

## Future Work
We intend to integrate real commercial LLMs (OpenAI/Anthropic) as evaluators, expand the task families to logic/spatial reasoning, and provide a shareable URL encoding for remote collaboration.

## Disclosures & Provenance
- **AI-Assisted Development**: AI-assisted development was used for portions of coding, debugging, documentation, and interface development. The team reviewed and validated the resulting implementation and is responsible for understanding and defending the system.
- **Source / License**: This project uses open-source libraries (React, Next.js, FastAPI, Z3). The BDH-CQ integration relies strictly on the *Dragon Hatchling* paper and the *BDH-CQ Technical Report* as primary sources. No proprietary BDH-CQ code or models are redistributed. 
