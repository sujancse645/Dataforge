# Coverage Cliff

## Problem
Models can appear to generalize from demonstrations, but it is difficult to see exactly where demonstrated coverage stops being reliable. Does a model truly understand the underlying rule, or does it merely interpolate within the bounds of the provided examples?

## Claim
"A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."

*This is a task- and model-specific hypothesis, not a universal law of AI.*

## What We Built
A reproducible interactive experiment that:
1. Generates rule-based demonstrations.
2. Defines explicit structural coverage.
3. Increases extrapolation distances sequentially.
4. Predicts results using a deterministic reference evaluator.
5. Independently computes ground truth via a Z3 solver.
6. Measures accuracy at each extrapolation step.
7. Detects boundary patterns (such as a Sharp Cliff or Stable performance).

## Key Technical Contribution
Controlled demonstration coverage and extrapolation measurement with independent mathematically verified ground truth. The separation of the evaluator from the ground truth solver guarantees zero data leakage.

## Result
Under our reference configuration (Transitive Inference, Seed 2026, Coverage 2), the deterministic evaluator remains 100% correct within its coverage and near-boundary levels, but drops sharply to 0% at an extrapolation distance of 3. This establishes that the experimental infrastructure successfully detects boundaries without assuming every failure is a cliff.

## BDH-CQ Connection
BDH-CQ asks a related but different research question: how can an architecture use demonstrations and perform reasoning without producing a written chain-of-thought trace? Our BDH-CQ educational module contextualizes our deterministic experiment against frontier brain-inspired latent reasoning architectures.

## Evidence
- **OUR LIVE EXPERIMENT**: The interactive Coverage Cliff extrapolation metrics.
- **PUBLISHED**: Theoretical context and architectural mechanisms for BDH-CQ derived from primary sources.
- **ILLUSTRATIVE**: Conceptual visual abstraction of latent state updates.

## Limitations
1. Current task family is limited to Transitive Inference.
2. The deterministic reference evaluator is not a general-purpose frontier LLM.
3. A synthetic failure demonstrates our infrastructure's boundary-detection capability; it does NOT establish that all AI systems share the same boundary.
4. We have not tested whether BDH-CQ exhibits a Coverage Cliff under identical conditions.

## Reproducibility
Experiments are fully reproducible from the displayed seed and coverage configuration. Execution is strictly deterministic across CLI and API.

## Future Work
- Integration of additional task families (e.g., spatial reasoning, formal logic).
- Direct API integration with commercial LLM evaluators.
- Porting the benchmark to evaluate official BDH-CQ checkpoints.
