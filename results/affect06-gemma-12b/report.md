# affect-06 — concept control set, gemma-12b

192 stories, 16 concepts x 3 arms x 4 seeds; neutral PCs affect01 (verbatim).
Workspace band for gating: L28-45.

## P17 gate — concept set vs emotion set (band means)

| metric | concepts | emotions | gate |
|---|---|---|---|
| split-half within-set cosine | 0.650 | 0.048 | PASS |
| held-out top-1 | 0.945 | 0.387 | PASS |
| pairwise separation (lower better) | -0.066 | -0.042 | PASS |
| attribution: same-target cross-arm | 0.588 | nan | FAIL |

chance: concepts 0.062, emotions 0.042 (different roster sizes — compare each to its own chance)
between-set leakage: concept-emotion cosine mean +0.000, max +0.264

**GATE: PARTIAL** (3/4 criteria)

- within-concept cos: L0:0.35 L3:0.35 L6:0.33 L9:0.29 L12:0.45 L15:0.65 L18:0.78 L21:0.77 L24:0.69 L27:0.67 L30:0.66 L33:0.68 L36:0.66 L39:0.63 L42:0.62 L45:0.64
- held-out top-1: L0:0.48 L3:0.54 L6:0.62 L9:0.73 L12:0.85 L15:0.90 L18:0.92 L21:0.98 L24:0.94 L27:0.96 L30:0.96 L33:0.98 L36:0.94 L39:0.94 L42:0.94 L45:0.90
- max cos to any emotion: L0:0.55 L3:0.38 L6:0.46 L9:0.45 L12:0.39 L15:0.39 L18:0.40 L21:0.32 L24:0.29 L27:0.27 L30:0.25 L33:0.26 L36:0.26 L39:0.27 L42:0.27 L45:0.33
