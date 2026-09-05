# BDH-CQ LEARNING OBJECTIVE

After using this module, the learner can explain how BDH-CQ's recurrent latent state updates allow demonstration-driven reasoning without a written chain-of-thought trace, and clearly distinguish this internal mechanism from the deterministic demonstration-coverage experiment measured in Coverage Cliff.

## Why BDH-CQ is Relevant
Because our experiment studies demonstration coverage and extrapolation, and BDH-CQ provides a concrete research system involving learning from demonstrations and reasoning *without* a written chain-of-thought trace. However, that connection does not make our deterministic experiment a BDH-CQ evaluation.

## What BDH-CQ Is (and Is Not)
- **BDH** = A brain-inspired post-transformer architecture family.
- **BDH-CQ** = A later system in that family designed to learn from demonstrations and reason over a latent state without producing explicit textual chain-of-thought tokens.
- **What it is NOT**: BDH-CQ is not a guarantee of unlimited generalization.

## Core Mechanism & Architecture
BDH-CQ processes input demonstrations and query representations through a recurrent, latent state update mechanism.
Instead of: `input -> text step 1 -> text step 2 -> answer`
BDH-CQ uses: `input -> hidden state -> state update -> state update -> answer`

## Conceptual Equation
A simplified conceptual update rule representing recurrent latent reasoning:
`h_(t+1) = f(h_t, x)`
Where `x` is the input representation, `h_t` is the latent state at computation step `t`, and `f` is the internal reasoning transformation.

## Published Evidence & Limitations
- **Established by Source**: BDH-CQ can learn algorithmic tasks from demonstrations without CoT.
- **Demonstrated Here**: We demonstrate an abstract toy visualization of latent updates.
- **What We Did Not Do**: We did not run an official BDH-CQ checkpoint. We did not reproduce the authors' complete training pipeline. Our Coverage Cliff evaluator is a reference Z3 verifier, not BDH-CQ.

## Primary Sources
See `sources.md`.
