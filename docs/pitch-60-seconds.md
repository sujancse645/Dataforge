# 60-Second Pitch

**HOOK:**
"Most AI demos ask one question: Can the model solve this example? We ask a harder one: How far can it generalize beyond what its demonstrations actually cover?"

**PROBLEM:**
"A model can look perfect on examples similar to what it has seen. But that doesn't tell us where its demonstrated coverage ends."

**SOLUTION:**
"Coverage Cliff turns that boundary into an experiment. We generate demonstrations, define their coverage, then progressively push the same rule beyond that coverage. Every prediction is compared against independently computed exact ground truth."

**RESULT:**
"In our reference experiment, accuracy remains perfect through the demonstrated range and then drops sharply at a specific extrapolation distance."

**HONESTY:**
"That does NOT prove every AI model has a universal cliff. It proves that this controlled experiment can expose and measure a boundary."

**BDH-CQ:**
"We then connect this idea to BDH-CQ, a research system studying demonstration-driven reasoning without a written chain-of-thought trace. But we keep that evidence separate: we did not test BDH-CQ for a Coverage Cliff."

**CLOSING:**
"Coverage Cliff is not just asking whether a model generalizes. It asks where that generalization stops."
