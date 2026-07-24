# affect-06 — concept control set, qwen-27b

192 stories, 16 concepts x 3 arms x 4 seeds; neutral PCs affect01 (verbatim).
Workspace band for gating: L28-59.

## P17 gate — concept set vs emotion set (band means)

| metric | concepts | emotions | gate |
|---|---|---|---|
| split-half within-set cosine | 0.745 | 0.545 | PASS |
| held-out top-1 | 0.979 | 0.736 | PASS |
| pairwise separation (lower better) | -0.066 | -0.042 | PASS |
| attribution: same-target cross-arm | 0.640 | 0.559 | PASS |

chance: concepts 0.062, emotions 0.042 (different roster sizes — compare each to its own chance)
between-set leakage: concept-emotion cosine mean +0.000, max +0.531

**GATE: PASS** (4/4 criteria)

- within-concept cos: L0:0.34 L4:0.44 L8:0.53 L12:0.57 L16:0.56 L20:0.72 L24:0.74 L28:0.73 L32:0.72 L36:0.79 L40:0.77 L44:0.76 L48:0.73 L52:0.74 L56:0.73 L60:0.71
- held-out top-1: L0:0.58 L4:0.71 L8:0.83 L12:0.90 L16:0.90 L20:0.98 L24:0.98 L28:0.98 L32:0.98 L36:0.98 L40:0.98 L44:0.98 L48:0.98 L52:0.98 L56:0.98 L60:0.96
- max cos to any emotion: L0:0.56 L4:0.52 L8:0.48 L12:0.52 L16:0.52 L20:0.48 L24:0.46 L28:0.50 L32:0.51 L36:0.49 L40:0.49 L44:0.54 L48:0.55 L52:0.56 L56:0.56 L60:0.54
