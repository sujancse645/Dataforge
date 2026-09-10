# DISCLOSURE.md — Project Disclosure & Provenance

**DataForge 2026 — Pathway Track**  
**Project:** Coverage Cliff  
**Team / Author:** Sujan L  

---

## 1. AI Assistance Statement

AI coding assistance was utilized during implementation based strictly on a human-authored architectural specification and experimental design. All central architectural decisions, experimental hypotheses, formal mathematical definitions ($C_{\text{max}}$, $D_{\text{ext}}$), and the core falsifiable claim are the team's own. The team fully understands, has independently audited, and can defend every component, algorithm, and line of code in this repository.

---

## 2. Reused Code & Data Provenance

- **Reused Code:** None. All task generators, SMT constraints, evaluator logic, API routes, and visualization components were developed specifically for this project.
- **Data Provenance:** No external scraped datasets were used. Tasks and symbolic relational chains are procedurally synthesized on-the-fly with seeded pseudorandomness and independently verified via the Z3 SMT constraint solver.

---

## 3. Dependency Licenses (from `requirements.txt`)

| Package | Version Range | License | Primary Purpose |
| :--- | :--- | :--- | :--- |
| `fastapi` | `>=0.100.0` | MIT License | REST & streaming API layer |
| `uvicorn` | `>=0.23.0` | BSD-3-Clause License | ASGI web server |
| `pydantic` | `>=2.0.0` | MIT License | Schema validation and data modeling |
| `z3-solver` | `>=4.12.0` | MIT License | Independent ground-truth solver |
| `pytest` | `>=7.0.0` | MIT License | Automated unit & integration testing |
| `httpx` | `>=0.24.0` | BSD-3-Clause License | HTTP test client |

---

## 4. Primary Sources & Citations

1. **Kosowski et al.** (2025). *The Dragon Hatchling*. arXiv:2509.26507.
   - *Supported concept*: Exploration of post-transformer recurrent latent updates.
2. **Engdahl et al.** (2026). *BDH-CQ: Demonstration-Driven In-Context Learning Without Chain of Thought*. arXiv:2608.09888.
   - *Supported concept*: Associative memory and latent hypothesis updating across sequential demonstration pairs.
3. **Hao et al.** (2024). *Training Large Language Models to Reason in a Continuous Latent Space (Coconut)*. arXiv:2412.06769.
   - *Supported concept*: Continuous latent-space reasoning versus token-based chain-of-thought.
4. **Geiping et al.** (2025). *Recurrent Depth in Language Models*. arXiv:2502.05171.
   - *Supported concept*: Scaling computational depth iteratively within bounded representation capacity.

---

## 5. Project License

This project is licensed under the terms of the MIT License. See [LICENSE](LICENSE) for full details.
