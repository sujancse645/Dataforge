# Coverage Cliff — Final Run Guide

## Requirements

- Python (3.11+)
- Node.js (18+)
- npm

## How to Run

1. Open a terminal and start the backend:
```bash
python -m uvicorn src.api.main:app --reload
```

## URLs

- **Full Application (Frontend + Backend)**: http://127.0.0.1:8000
- **API Health**: http://127.0.0.1:8000/api/v1/health

## Demo Flow

1. **Start the applications**: Run the commands in Terminal 1 and Terminal 2.
2. **Open the browser**: Navigate to http://localhost:3000.
3. **Run the Experiment**: Keep the default "Reference demo configuration" (Seed: 2026, Coverage: 2) and click **RUN THE EXPERIMENT**.
4. **Walkthrough the Results**: Discuss the generated tasks, predict outcomes, reveal the independent ground truth, and analyze the Accuracy Curve to highlight the detected Coverage Cliff.
5. **Challenge the Claim**: Change the Random Seed or Demonstration Coverage and run again to prove reproducibility and controlled variation. Finally, review the BDH-CQ context at the bottom.
