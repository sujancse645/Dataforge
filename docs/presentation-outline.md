# Final Presentation Outline

## SLIDE 1 — HOOK
COVERAGE CLIFF
"How far can a model generalize beyond what its demonstrations actually cover?"

## SLIDE 2 — THE PROBLEM
Models are often evaluated on whether they get an answer right.
But that leaves a deeper question:
"How far beyond demonstrated examples does that success extend?"
Demonstrations → Coverage → Extrapolation → Accuracy → Boundary

## SLIDE 3 — OUR FALSIFIABLE CLAIM
"A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."
NOT A UNIVERSAL LAW. We test it under controlled conditions.

## SLIDE 4 — HOW THE EXPERIMENT WORKS
Demonstrations ↓
Cmax ↓
Test complexity ↓
Dext ↓
Prediction ↓
Independent Ground Truth ↓
Accuracy ↓
Cliff Detector

## SLIDE 5 — LIVE RESULT
(Show the actual accuracy curve highlighting the observed boundary)
"Under this configuration, we observe a sharp cliff at extrapolation distance 3."

## SLIDE 6 — CHALLENGE THE CLAIM
Show how changing seed, coverage, or extrapolation range creates a new experiment.
"A scientific claim should be testable, not merely demonstrated once."

## SLIDE 7 — BDH-CQ CONNECTION
Coverage Cliff: OUR LIVE EXPERIMENT
BDH-CQ: SOURCE-GROUNDED TECHNICAL CONTEXT
"We did not establish whether BDH-CQ has a Coverage Cliff under our conditions."

## SLIDE 8 — IMPACT / FUTURE WORK
Future work:
- real model evaluators
- multiple task families
- matched BDH-CQ experiments
"Instead of asking only whether a model generalizes, we can ask where that generalization stops."
