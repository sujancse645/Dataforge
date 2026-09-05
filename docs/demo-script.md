# Coverage Cliff - Live Demo Script

**Target Time:** 2–3 minutes

---

### 0:00–0:20 | HOOK
"Most model demos ask: 'Can the model solve this?' We ask a different question: 'How far beyond its demonstrations can it keep solving?' Welcome to Coverage Cliff."

### 0:20–0:40 | CLAIM
"Our claim is simple but falsifiable: A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."

### 0:40–1:00 | DEMONSTRATIONS
"Here is how we test it. We generate demonstrations for a hidden rule—in this case, Transitive Inference. We define 'Demonstration Coverage' as the maximum complexity represented in these examples. The model sees the examples, but not the hidden rule."

### 1:00–1:20 | EXPERIMENT
"Now, we push the task complexity past what was demonstrated. This is the 'Extrapolation Distance'. We run the backend experiment. The predictions are evaluated, while a Z3 solver independently computes the exact ground truth to guarantee zero leakage."

### 1:20–1:40 | RESULT
"Let's look at the accuracy curve. Under these conditions, the evaluator drops from correct to incorrect at this exact extrapolation level. The system detects a 'SHARP CLIFF'."

### 1:40–2:00 | CHALLENGE
"But this is a laboratory, not a static report. We can challenge the claim. Let's change the random seed or the demonstration coverage and run again. Watch how the boundary behaves. Sometimes it moves, proving that a claim must survive controlled variation."

### 2:00–2:30 | BDH-CQ
"Now we connect this to the frontier. What about models designed to reason from demonstrations without writing a chain of thought? This is BDH-CQ. It's a related research question about latent reasoning. We explore the published architecture here, but note our limitation: we have NOT tested official BDH-CQ for this Coverage Cliff. They are different experiments."

### 2:30–3:00 | CLOSING
"We don't claim a universal law of AI. We built a rigorous, reproducible way to measure the boundary. Instead of asking vaguely whether a model generalizes, we can now ask *exactly where* that generalization stops. Thank you."
