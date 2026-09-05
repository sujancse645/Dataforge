import os

docs = {
    "docs/claim.md": "# FINAL LOCKED CLAIM\n\n\"A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage.\"\n",
    "docs/methodology.md": "# METHODOLOGY\n\n## Coverage Definition\nMaximum demonstrated complexity $C_{max}$.\n\n## Extrapolation Definition\nExtrapolation distance is defined as $D_{ext} = C_{test} - C_{max}$.\n\n## Evaluation Policy\nExact-match accuracy against Z3-verified ground truth.\n",
    "docs/task-design.md": "# TASK DESIGN\n\n## Task Family\nSymbolic Logic / Transitive Inference.\n\n## Rule Representation\nA chain of boolean relations (e.g., A > B, B > C).\n\n## Complexity Variable\nReasoning Chain Length ($L$).\n",
    "docs/bdh-cq.md": "# BDH-CQ INTEGRATION\n\nContextualize the discovered cliff within Big-Bench Hard (BBH) capabilities. Connect model extrapolation failures to known length-generalization issues in frontier models.\n",
    "docs/scientific-audit.md": "# SCIENTIFIC AUDIT RULES\n\n- No constant outputs\n- No single-example memorization\n- No output format leakage\n- Enforce strict separation of hidden rules from model prompt.\n",
    "docs/product-spec.md": "# PRODUCT SPEC\nCoverage Cliff is an interactive educational laboratory testing extrapolation limits of models.",
    "docs/architecture.md": "# ARCHITECTURE\n- Frontend: Next.js\n- Backend: FastAPI\n- Engine: Python, Z3\n",
    "docs/evidence.md": "# EVIDENCE\n(Placeholder) - Evidence gathered during Phase 1.\n",
    "docs/research-sources.md": "# RESEARCH SOURCES\n- Z3 Prover Documentation\n- Length Generalization papers (e.g., \"Faithful Reasoning Using Large Language Models\").\n",
    "docs/implementation-roadmap.md": "# IMPLEMENTATION ROADMAP\n- Phase 1: Experiment Engine\n- Phase 2: FastAPI Backend\n- Phase 3: Frontend UI\n- Phase 4: Integration\n",
    "README.md": "# Dataforge\nCoverage Cliff Project.\n"
}

os.makedirs("docs", exist_ok=True)
for path, content in docs.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
