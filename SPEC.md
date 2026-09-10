# SPEC.md — Coverage Cliff Specification

**DataForge 2026 — Pathway Track**  
**Project:** Coverage Cliff  
**Concept:** Demonstration Coverage and Extrapolation

---

## 1. Central Falsifiable Claim

> "A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."

*Notice: This is a task- and model-specific hypothesis under controlled experimental conditions, not an asserted universal law of all artificial intelligence.*

---

## 2. Experimental Formalization

- **Task Family:** Transitive Inference over symbolic relations ($A > B, B > C, \dots$).
- **Demonstration Coverage ($C_{\text{max}}$):** Maximum relational complexity (chain length) represented in the demonstrations provided to the learner.
- **Extrapolation Distance ($D_{\text{ext}}$):**
  $$D_{\text{ext}} = C_{\text{test}} - C_{\text{max}}$$
  Measures the number of steps beyond demonstrated coverage.
- **Evaluation Isolation:** The ground-truth solver (Z3 theorem prover) runs independently of the evaluator. The evaluator receives strictly the task presentation without access to hidden rule metadata, ground truth, or difficulty labels.
- **Cliff Criterion:** A transition from high accuracy ($\ge 80\%$) within demonstrated coverage to near-zero accuracy ($\le 20\%$) across successive extrapolation steps.

---

## 3. Architecture Specification

- **Scientific Engine:** Python 3.11 with Z3 SMT solver for independent ground-truth verification.
- **API Layer:** FastAPI exposing `/api/v1/health`, `/api/v1/configurations`, and streaming NDJSON `/api/v1/experiments/stream`.
- **Educational Frontend:** Next.js 16 + Tailwind CSS static export, served directly by FastAPI as a unified single-port application.
