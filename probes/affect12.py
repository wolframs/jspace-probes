"""affect-12 — is the emotion grouping geometric? CPU-only analysis.

Prereg: results/affect12-prereg.md (frozen before computing). Tests
whether the dose-stable turn-end grouping of the 24 emotion directions
(anger/pride floor, calm ceiling; five semantic/mechanical candidates
dead) is linearly visible in vector geometry at the injection band —
Mantel cluster test, leave-one-out potency axis, concept-roster
transfer, and a split-half-reliability confound check.

Usage: .venv/bin/python probes/affect12.py
"""

import json
import random

import torch

from lab import RESULTS
from affect3 import E_LAYERS

OUT = RESULTS / "affect12-geom-q27b"
A01 = RESULTS / "affect01-qwen-27b"
A06 = RESULTS / "affect06-qwen-27b"


def _unit(x):
    return x / x.norm(dim=-1, keepdim=True)


def _potency():
    out = {}
    for path in ("affect08-q27b-ae08", "affect08-q27b-ae1"):
        d = json.loads((RESULTS / path / "affect08.json").read_text())
        for c in {r["cond"] for r in d["runs"]}:
            rs = [r for r in d["runs"] if r["cond"] == c]
            out.setdefault(c, []).append(
                sum(r["turnend_in_window"] for r in rs) / len(rs))
    return {k: sum(v) / len(v) for k, v in out.items()}


def _band_cos(A, B):
    """mean over E_LAYERS of cos(A[l], B[l])."""
    return float(torch.stack(
        [(_unit(A[l]) * _unit(B[l])).sum() for l in E_LAYERS]).mean())


def _spearman(x, y):
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for i, j in enumerate(s):
            r[j] = i
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx)
           * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(2718)
    N = 20000

    va = torch.load(A01 / "vectors.pt", map_location="cpu")
    V, emos = va["anthropic"].float(), list(va["emotions"])
    cv = torch.load(A06 / "cvectors.pt", map_location="cpu")
    C, slugs = cv["anthropic"].float(), list(cv["slugs"])
    pot = _potency()
    p_e = [pot[e] for e in emos]
    p_c = [pot[s] for s in slugs]
    E = len(emos)

    # unit-normalize once per layer, restricted to band
    Vb = torch.stack([torch.stack([_unit(V[i, l]) for l in E_LAYERS])
                      for i in range(E)])          # [24, 8, d]
    Cb = torch.stack([torch.stack([_unit(C[j, l]) for l in E_LAYERS])
                      for j in range(len(slugs))])  # [16, 8, d]

    lines = ["# affect-12 — is the emotion grouping geometric? "
             "(qwen-27b, CPU)", "",
             f"band {E_LAYERS}; potency = affect-08 turn-end, "
             "mean of ae=0.08/0.10", ""]

    # ---------------- P-a Mantel ---------------------------------------
    cosm = torch.einsum("ild,jld->ij", Vb, Vb) / len(E_LAYERS)
    pairs = [(i, j) for i in range(E) for j in range(i + 1, E)]
    x = [float(cosm[i, j]) for i, j in pairs]

    def mantel_stat(p):
        y = [-abs(p[i] - p[j]) for i, j in pairs]
        return _spearman(x, y)
    obs_a = mantel_stat(p_e)
    ge = 0
    for _ in range(N):
        sh = p_e[:]
        rng.shuffle(sh)
        if abs(mantel_stat(sh)) >= abs(obs_a) - 1e-12:
            ge += 1
    lines += ["## P-a Mantel: pairwise cosine vs potency similarity",
              f"- rho {obs_a:+.3f}, permutation p={ge / N:.4f}"
              f"{' (sig .05)' if ge / N < .05 else ''}", ""]

    # ---------------- P-b LOO potency axis -----------------------------
    def loo_predict(p):
        mp = sum(p) / len(p)
        wts = torch.tensor([q - mp for q in p])
        S = torch.einsum("i,ild->ld", wts, Vb)
        preds = []
        for i in range(E):
            w = _unit(S - wts[i] * Vb[i])
            preds.append(float((Vb[i] * w).sum(-1).mean()))
        return preds
    preds = loo_predict(p_e)
    obs_b = _spearman(preds, p_e)
    ge = 0
    for _ in range(N // 10):          # LOO refit is heavier: 2k perms
        sh = p_e[:]
        rng.shuffle(sh)
        if abs(_spearman(loo_predict(sh), sh)) >= abs(obs_b) - 1e-12:
            ge += 1
    lines += ["## P-b leave-one-out potency axis (24 emotions)",
              f"- LOO Spearman {obs_b:+.3f}, permutation "
              f"p={ge / (N // 10):.4f}"
              f"{' (sig .05)' if ge / (N // 10) < .05 else ''}",
              "- per-emotion (predicted vs actual):"]
    order = sorted(range(E), key=lambda i: -p_e[i])
    for i in order:
        lines.append(f"    {emos[i]:<13} pred {preds[i]:+.3f}  "
                     f"actual {p_e[i]:.3f}")
    lines.append("")

    # ---------------- P-c transfer to concepts -------------------------
    mp = sum(p_e) / E
    w_full = _unit(sum((p_e[j] - mp) * Vb[j] for j in range(E)))
    proj_c = [float((Cb[k] * w_full).sum(-1).mean())
              for k in range(len(slugs))]
    obs_c = _spearman(proj_c, p_c)
    ge = 0
    for _ in range(N):
        sh = p_c[:]
        rng.shuffle(sh)
        if abs(_spearman(proj_c, sh)) >= abs(obs_c) - 1e-12:
            ge += 1
    lines += ["## P-c transfer: emotion-fit axis -> 16 concept potencies",
              f"- Spearman {obs_c:+.3f}, permutation p={ge / N:.4f}"
              f"{' (sig .05)' if ge / N < .05 else ''}", ""]

    # ---------------- P-d reliability confound -------------------------
    meta = json.loads((A01 / "stories.json").read_text())
    idx = meta["stories"]
    means = torch.load(A01 / "means.pt", map_location="cpu").float()
    U = torch.stack([means[[i for i, s in enumerate(idx)
                            if s["emotion"] == e]].mean(0)
                     for e in emos])
    grand = U.mean(0)
    rel = []
    for e in emos:
        rows = [i for i, s in enumerate(idx) if s["emotion"] == e]
        cs = []
        for seed in range(7, 27):
            g = torch.Generator().manual_seed(seed)
            perm = torch.randperm(len(rows), generator=g).tolist()
            h1 = means[[rows[i] for i in perm[:len(rows) // 2]]].mean(0)
            h2 = means[[rows[i] for i in perm[len(rows) // 2:]]].mean(0)
            c = (_unit(h1 - grand) * _unit(h2 - grand)).sum(-1)
            cs.append(float(c[E_LAYERS].mean()))
        rel.append(sum(cs) / len(cs))
    obs_d = _spearman(rel, p_e)
    lines += ["## P-d split-half reliability vs potency",
              f"- Spearman {obs_d:+.3f} "
              f"({'CONFOUND TRIGGERED (>=.5)' if abs(obs_d) >= .5 else 'below .5 bar'})",
              "- per-emotion reliability at band:"]
    for i in order:
        lines.append(f"    {emos[i]:<13} rel {rel[i]:+.3f}  "
                     f"potency {p_e[i]:.3f}")
    lines.append("")

    json.dump({"emotions": emos, "potency_e": p_e, "slugs": slugs,
               "potency_c": p_c, "loo_pred": preds, "reliability": rel,
               "proj_concepts": proj_c,
               "pairwise_cos": [[float(cosm[i, j]) for j in range(E)]
                                for i in range(E)]},
              open(OUT / "geom.json", "w"), indent=1)
    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
    print("DONE", flush=True)
