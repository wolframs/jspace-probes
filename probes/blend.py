"""blend-02 — port published readouts to gemma-4b, each validated on its own
paper's task before anything is blended. Prereg: results/blend02-prereg.md.

Part A (this file, `oi`): ordering-ID principal component, Dai, Heinzerling
& Inui, EMNLP 2024 (arXiv 2409.05448). PCA over entity-token residuals in
box-tracking contexts; PC1 should order entities by mention order; editing
along PC1 should re-bind the query to another entity's attribute.

Two PCA variants are scored side by side: `raw` (the paper's reading, PCA
on the pooled entity rows) and `ctx` (rows centred per context, i.e. each
entity minus the mean of its K co-mentioned entities). The smoke test
showed raw PC1 at L10–18 carrying 70–88% of the variance and tracking
absolute token position as well as it tracks order — the mechanical
default the prereg names. Per-context centring removes whatever is shared
by all entities of one prompt (position drift, norm, topic) and leaves
only what distinguishes co-present entities, which is what an ordering ID
has to be.

    .venv/bin/python probes/blend.py oi            # full Part A
    .venv/bin/python probes/blend.py oi --quick    # smoke test, small N

Writes results/blend02-oi-g4b/{oi.json, oi-pc1.pt, report.md}. thoughts.md
and plain.md are written by hand afterwards.
"""
from __future__ import annotations

import json
import pathlib
import random
import sys
import time

import numpy as np
import torch
from scipy.stats import spearmanr

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lab import get_model            # noqa: E402
from affect2 import _all_resid       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "blend02-oi-g4b"
MODEL = "gemma-4b"
K = 3                                # entities per context
LAYERS_FIT = list(range(2, 27))      # PCA sweep (paper: L8/32 ≈ 25% depth → L8–9/34); edits sweep to L26
PAPER_LAYER = 8
EDIT_LAYERS = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]   # site × depth map for the edits

# ---------------------------------------------------------------- pools ----
# Every pool is filtered at runtime to items that tokenize to ONE token with
# a leading space, so "entity position" and "answer token" are unambiguous.
OBJECTS = ("coffee stone map key book apple phone letter coin ring hat lamp pen cup "
           "clock knife candle bottle ball shoe watch brush mirror fork spoon plate "
           "glove scarf sock rope wire nail bell drum flute ticket card stamp bag box "
           "bread cheese onion lemon melon peach plum grape").split()
LABELS = list("ABCDEFGHJKLMNPQRSTUVWXYZ")
PERSONS = ("Alice Bob Carol David Emma Frank Grace Henry Irene Jack Karen Leo Maria "
           "Nathan Olivia Paul Rachel Sam Tina Victor Wendy Zoe").split()
CITIES = ("Paris London Berlin Madrid Rome Vienna Prague Tokyo Delhi Cairo Lima Oslo "
          "Dublin Athens Boston Denver Austin Seattle Toronto Sydney Moscow Lisbon").split()
COLORS = ("red blue green yellow black white brown pink purple orange grey gold "
          "silver").split()
FILLERS = ["Nothing else is known.", "The room is quiet.", "It was a cold morning.",
           "Someone had checked earlier.", "The list goes on.", "A note was left behind.",
           "The light was dim.", "This was confirmed twice.", "The door stayed shut.",
           "Everyone agreed on that.", "The weather did not change.", "Lunch came late.",
           "The radio played softly.", "Nobody asked why.", "The clock kept ticking."]

RELATIONS = {
    # name: (statement(entity, attr), question(entity), answer prefix, attr pool)
    "box":   (lambda e, a: f"The {e} is in Box {a}.", lambda e: f"Which box is the {e} in?", " Box", "LABELS"),
    "city":  (lambda e, a: f"{e} lives in {a}.", lambda e: f"Which city does {e} live in?", "", "CITIES"),
    "color": (lambda e, a: f"The {e} is {a}.", lambda e: f"What color is the {e}?", "", "COLORS"),
}
HEADER = "Answer the question using the context.\n"


def one_token(tok, s: str) -> bool:
    return len(tok.encode(s, add_special_tokens=False)) == 1


def filtered_pools(tok) -> dict:
    pools = {
        "OBJECTS": [w for w in OBJECTS if one_token(tok, " " + w)],
        "LABELS": [w for w in LABELS if one_token(tok, " " + w)],
        "PERSONS": [w for w in PERSONS if one_token(tok, " " + w) and one_token(tok, w)],
        "CITIES": [w for w in CITIES if one_token(tok, " " + w)],
        "COLORS": [w for w in COLORS if one_token(tok, " " + w)],
    }
    for k, v in pools.items():
        assert len(v) >= 8, f"pool {k} too small after tokenizer filter: {v}"
    return pools


# -------------------------------------------------------------- prompts ----

def make_context(rel: str, rng: random.Random, pools: dict, filler: bool = False) -> dict:
    """One k-entity context. filler=True inserts 0–4 filler sentences BEFORE
    the first statement and 0–2 between statements, so that absolute token
    position and mention order decorrelate across contexts (the P-A2
    control). ent_end / attr_end are char offsets of the last character of
    each entity / attribute mention inside the context."""
    stmt, question, prefix, attr_pool = RELATIONS[rel]
    ents = rng.sample(pools["OBJECTS"] if rel != "city" else pools["PERSONS"], K)
    attrs = rng.sample(pools[attr_pool], K)
    text = HEADER + "Context:"
    ent_end, attr_end = [], []
    if filler:
        for _ in range(rng.randrange(0, 5)):
            text += " " + rng.choice(FILLERS)
    for i, (e, a) in enumerate(zip(ents, attrs)):
        if filler and i > 0:
            for _ in range(rng.randrange(0, 3)):
                text += " " + rng.choice(FILLERS)
        s = " " + stmt(e, a)
        ent_end.append(len(text) + s.index(e) + len(e))
        attr_end.append(len(text) + s.rindex(a) + len(a))
        text += s
    q = rng.randrange(K)
    text += "\nQuestion: " + question(ents[q]) + "\nAnswer:" + prefix
    return dict(rel=rel, text=text, ents=ents, attrs=attrs, q=q,
                ent_end=ent_end, attr_end=attr_end, filler=filler)


def encode(tok, ctx: dict):
    enc = tok(ctx["text"], return_offsets_mapping=True, return_tensors="pt")
    offs = enc["offset_mapping"][0].tolist()

    def at(end):
        hit = [i for i, (a, b) in enumerate(offs) if a < end <= b]
        assert hit, (ctx["text"], end)
        return hit[-1]
    return enc["input_ids"], [at(e) for e in ctx["ent_end"]], [at(a) for a in ctx["attr_end"]]


# --------------------------------------------------------------- capture ----

def capture(lm, ctxs: list[dict], attr_ids: dict) -> dict:
    tok = lm.tok
    Hs, poss, correct, top1, probs = [], [], [], [], []
    for ctx in ctxs:
        ids, pos, _ = encode(tok, ctx)
        ids = ids.to("cuda:0")
        with torch.no_grad():
            H = _all_resid(lm, ids)                        # [L, seq, D]
            logits = lm.model._hf_model(ids).logits[0, -1].float()
        Hs.append(H[:, pos, :].half())                     # [L, K, D]
        poss.append(pos)
        cand = [attr_ids[a] for a in ctx["attrs"]]
        gold = cand[ctx["q"]]
        correct.append(int(cand[int(logits[cand].argmax())] == gold))
        top1.append(int(int(logits.argmax()) == gold))
        probs.append(float(torch.softmax(logits, -1)[gold]))
    return dict(H=torch.stack(Hs), pos=poss, correct=correct, top1=top1, p_gold=probs)


VARIANTS = {"raw": (False, False), "ctx": (True, False), "z": (True, True)}
# raw: the paper's pooled PCA. ctx: rows centred per context (removes what all
# K entities of one prompt share: position drift, norm, topic). z: ctx rows
# additionally standardised per dimension with the fit set's σ, which stops
# Gemma's massive-activation dimensions (coordinates in the thousands in the
# smoke test) from owning PC1. Edits for z are mapped back to raw space as
# Δ = dc · (σ ⊙ û), which changes the standardised coordinate by exactly dc.


def rows_of(cap: dict, l: int, variant: str, sigma: torch.Tensor | None = None) -> torch.Tensor:
    """[N*K, D] float32 rows at layer l under a variant (see VARIANTS)."""
    center, _ = VARIANTS[variant]
    X = cap["H"][:, l].float()                             # [N, K, D]
    if center:
        X = X - X.mean(1, keepdim=True)
    X = X.reshape(-1, X.shape[-1])
    if sigma is not None:
        X = X / sigma
    return X


def pca1(X: torch.Tensor):
    mu = X.mean(0)
    U, S, Vh = torch.linalg.svd(X - mu, full_matrices=False)
    return mu, Vh[0], float(S[0] ** 2 / (S ** 2).sum())


def fit_and_score(cap_fit: dict, heldout: dict[str, dict]) -> dict:
    """{variant: {layer: row}}; rows carry PC1, per-order coordinate means,
    per-order full means (for the mean-difference edit) and the Spearman
    scores on fit / held-out / filler sets."""
    N = cap_fit["H"].shape[0]
    order = np.tile(np.arange(K), N)
    out = {v: {} for v in VARIANTS}
    for variant in out:
        for l in LAYERS_FIT:
            sigma = None
            if VARIANTS[variant][1]:
                sigma = rows_of(cap_fit, l, variant).std(0).clamp_min(1e-3)
            X = rows_of(cap_fit, l, variant, sigma)
            mu, u, evr = pca1(X)
            c = (X - mu) @ u
            rho = spearmanr(c.numpy(), order).correlation
            if rho < 0:
                u, c, rho = -u, -c, -rho
            m12 = order > 0
            row = dict(evr=evr, rho_fit=float(rho),
                       rho_fit_12=float(spearmanr(c.numpy()[m12], order[m12]).correlation),
                       c_mean=[float(c[order == o].mean()) for o in range(K)],
                       c_sd=[float(c[order == o].std()) for o in range(K)],
                       mu=mu, u=u, sigma=sigma,
                       w=(u * sigma if sigma is not None else u),   # raw-space edit direction
                       means=[(X[order == o].mean(0) * (sigma if sigma is not None else 1.0))
                              for o in range(K)])
            for name, cap in heldout.items():
                Xh = rows_of(cap, l, variant, sigma)
                ch = ((Xh - mu) @ u).numpy()
                oh = np.tile(np.arange(K), cap["H"].shape[0])
                row[f"rho_{name}"] = float(spearmanr(ch, oh).correlation)
                row[f"rho_{name}_12"] = float(spearmanr(ch[oh > 0], oh[oh > 0]).correlation)
                if name == "filler":
                    tp = np.array(cap["pos"]).reshape(-1).astype(float)
                    row["rho_filler_pos"] = float(spearmanr(ch, tp).correlation)
                    A = np.stack([tp, np.ones_like(tp)], 1)
                    beta, *_ = np.linalg.lstsq(A, ch, rcond=None)
                    row["rho_filler_order_given_pos"] = float(
                        spearmanr(ch - A @ beta, oh).correlation)
                    B = np.stack([oh.astype(float), np.ones_like(tp)], 1)
                    beta2, *_ = np.linalg.lstsq(B, ch, rcond=None)
                    row["rho_filler_pos_given_order"] = float(
                        spearmanr(ch - B @ beta2, tp).correlation)
            out[variant][l] = row
    return out


# ------------------------------------------------------------------ edit ----

class EditAt:
    """Add deltas to the residual at given layers: edits = [(pos, delta), ...]
    applied at every layer in `layers`. Records ‖Δ‖/‖h‖ at the first edit."""

    def __init__(self, lm, layers: list[int], edits: list[tuple[int, torch.Tensor]]):
        self.blocks = [lm.model.layers[l] for l in layers]
        self.edits = edits
        self.ratio, self.hs = None, []

    def _hook(self, mod, inp, output):
        t = output if torch.is_tensor(output) else output[0]
        h = t.clone()
        for n, (p, d) in enumerate(self.edits):
            d = d.to(h.device, h.dtype)
            base = h[0, p, :]
            if n == 0 and self.ratio is None:
                self.ratio = float(d.norm() / base.float().norm().clamp_min(1e-6))
            h[0, p, :] = base + d
        return h if torch.is_tensor(output) else (h, *output[1:])

    def __enter__(self):
        self.hs = [b.register_forward_hook(self._hook) for b in self.blocks]
        return self

    def __exit__(self, *exc):
        for h in self.hs:
            h.remove()


def run_edits(lm, ctxs: list[dict], fit: dict, layers: list[int], attr_ids: dict,
              n_rand: int = 3) -> dict:
    """Conditions per layer, all with the queried entity i re-bound toward
    entity j (j ≠ i, fixed per context):
      oi_x{1,2,4}   +s·(c_j−c_i)·û on i's entity token          (preregistered: x1)
      rand{s}       same ‖Δ‖ along a seeded random unit vector   (P-A3 control)
      swap_x{1,2}   +s·dc·û on i's entity+attribute tokens, −s·dc·û on j's
      randswap{s}   the swap with a random unit vector
      meandiff      full per-order mean difference μ_j−μ_i on i's entity token
      oi_win_x2     oi_x2 applied at layers L, L+1, L+2
    Only contexts the model answers correctly unedited are counted."""
    tok = lm.tok
    res = {l: {} for l in layers}
    gen = torch.Generator().manual_seed(2026)
    D = fit[layers[0]]["w"].numel()
    rand_dirs = []
    for _ in range(n_rand):
        r = torch.randn(D, generator=gen)
        rand_dirs.append(r / r.norm())
    n_layers = len(lm.model.layers)
    for ctx in ctxs:
        ids, pos, apos = encode(tok, ctx)
        ids = ids.to("cuda:0")
        cand = [attr_ids[a] for a in ctx["attrs"]]
        i = ctx["q"]
        j = (i + 1 + random.Random(hash(ctx["text"]) & 0xffff).randrange(K - 1)) % K
        with torch.no_grad():
            base = lm.model._hf_model(ids).logits[0, -1].float()
        if int(base[cand].argmax()) != i:
            continue
        base_diff = float(base[cand[j]] - base[cand[i]])
        for l in layers:
            row = fit[l]
            u = row["w"]                       # raw-space direction for a unit change of the PC1 coordinate
            dc = row["c_mean"][j] - row["c_mean"][i]
            conds: dict[str, tuple[list[int], list]] = {}
            ent = lambda v: [(pos[i], v), (pos[j], -v)]
            att = lambda v: [(apos[i], v), (apos[j], -v)]
            conds["ent_x1"] = ([l], [(pos[i], dc * u)])              # the preregistered literal
            conds["meandiff"] = ([l], [(pos[i], row["means"][j] - row["means"][i])])
            for s_ in (1.0, 2.0, 4.0):
                v = s_ * dc * u
                conds[f"entswap_x{s_:g}"] = ([l], ent(v))
                conds[f"attrswap_x{s_:g}"] = ([l], att(v))
                conds[f"fullswap_x{s_:g}"] = ([l], ent(v) + att(v))
            wn = float(u.norm())              # matched norm: ‖Δ_rand‖ = ‖s·dc·w‖
            for si, r in enumerate(rand_dirs[:2]):
                v = 2.0 * dc * wn * r
                conds[f"randent_x2_{si}"] = ([l], ent(v))
                conds[f"randattr_x2_{si}"] = ([l], att(v))
                conds[f"randfull_x2_{si}"] = ([l], ent(v) + att(v))
            v = 4.0 * dc * wn * rand_dirs[0]
            conds["randfull_x4_0"] = ([l], ent(v) + att(v))
            for name, (lays, edits) in conds.items():
                with torch.no_grad(), EditAt(lm, lays, edits) as ed:
                    lg = lm.model._hf_model(ids).logits[0, -1].float()
                am = int(lg[cand].argmax())
                r = res[l].setdefault(name, dict(n=0, flip=0, stay=0, other=0, ddiff=0.0, ratio=0.0))
                r["n"] += 1
                r["flip"] += int(am == j)
                r["stay"] += int(am == i)
                r["other"] += int(am not in (i, j))
                r["ddiff"] += float(lg[cand[j]] - lg[cand[i]]) - base_diff
                r["ratio"] += ed.ratio or 0.0
    for l in layers:
        for r in res[l].values():
            n = max(r["n"], 1)
            r.update(flip_rate=r["flip"] / n, stay_rate=r["stay"] / n,
                     other_rate=r["other"] / n, ddiff_mean=r["ddiff"] / n, ratio_mean=r["ratio"] / n)
    return res


# ---------------------------------------------------------------- report ----

def report(meta: dict, fit: dict, edits: dict, pick: list[int]) -> str:
    L = ["# blend-02 Part A — ordering-ID port on gemma-4b", "",
         f"Prereg: results/blend02-prereg.md (P26). Model {MODEL}, bf16, 34 layers. "
         f"k={K} entities; fit N={meta['n_fit']} box contexts; held-out N={meta['n_held']} "
         f"each (city, color); filler/position control N={meta['n_filler']}; edit set "
         f"N={meta['n_edit']}. Raw-text prompts, answer read as the restricted argmax over "
         f"the context's three attribute tokens.", "",
         "## Unedited accuracy", "",
         "| set | restricted argmax | full-vocab top-1 | mean p(gold) |", "|---|---:|---:|---:|"]
    for name, a in meta["acc"].items():
        L.append(f"| {name} | {a['restricted']:.3f} | {a['top1']:.3f} | {a['p_gold']:.3f} |")
    for variant, title in (("z", "per-context centred + per-dimension standardised"),
                           ("ctx", "per-context centred"), ("raw", "raw pooled PCA (paper's reading)")):
        title += " (PRIMARY for the edits)" if variant == meta["edit_variant"] else ""
        L += ["", f"## PC1 by layer — {title}", "",
              "Spearman ρ of the PC1 coordinate with mention order. `filler` = position-decorrelated "
              "control; `pos` = ρ with absolute token position there; `order|pos` and `pos|order` are "
              "the two partial correlations.", "",
              "| layer | EVR | ρ fit | ρ fit 1v2 | ρ city | ρ city 1v2 | ρ color | ρ color 1v2 | ρ filler | ρ pos | order\\|pos | pos\\|order | c̄ by order |",
              "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
        for l, r in fit[variant].items():
            cm = " / ".join(f"{x:+.1f}" for x in r["c_mean"])
            L.append(f"| {l} | {r['evr']:.3f} | {r['rho_fit']:.3f} | {r['rho_fit_12']:.3f} | {r['rho_city']:.3f} | "
                     f"{r['rho_city_12']:.3f} | {r['rho_color']:.3f} | {r['rho_color_12']:.3f} | {r['rho_filler']:.3f} | "
                     f"{r['rho_filler_pos']:.3f} | {r['rho_filler_order_given_pos']:.3f} | "
                     f"{r['rho_filler_pos_given_order']:.3f} | {cm} |")
    L += ["", f"Edit layers {pick} (fixed sweep plus the best held-out layer L{meta['best_layer']}). "
          f"Directions for the edits come from the **{meta['edit_variant']}** PCA.", "",
          "## Causal edits", "",
          "Queried entity i re-bound toward entity j (j ≠ i). Flip = restricted argmax moves to "
          "j's attribute. `ent_x1` is the preregistered literal (P-A3: +(c_j−c_i)·û on i's entity "
          "token); `meandiff` the full mean-difference edit at the same site. The swaps exchange "
          "the PC1 coordinate between i and j at a SITE: `entswap` on the two entity tokens, "
          "`attrswap` on the two attribute tokens, `fullswap` on all four; `x1/x2/x4` scale the "
          "coordinate difference. `rand*_x2_*` are the matched-norm random-direction controls per "
          "site (the P-A3 control, read against the x2 rows), `randfull_x4_0` against fullswap_x4.", "",
          "| layer | condition | n | flip → j | stays i | other | mean Δ(logit_j − logit_i) | ‖Δ‖/‖h‖ |",
          "|---:|---|---:|---:|---:|---:|---:|---:|"]
    for l in pick:
        for name, r in edits[l].items():
            L.append(f"| {l} | {name} | {r['n']} | {r['flip_rate']:.3f} | {r['stay_rate']:.3f} | "
                     f"{r['other_rate']:.3f} | {r['ddiff_mean']:+.2f} | {r['ratio_mean']:.3f} |")
    return "\n".join(L) + "\n"


def main(quick: bool = False) -> None:
    t0 = time.time()
    n_fit, n_held, n_filler, n_edit = (60, 40, 60, 24) if quick else (600, 300, 400, 150)
    lm = get_model(MODEL)
    tok = lm.tok
    pools = filtered_pools(tok)
    attr_ids = {w: tok.encode(" " + w, add_special_tokens=False)[0]
                for p in ("LABELS", "CITIES", "COLORS") for w in pools[p]}
    rng = random.Random(0)
    sets = {
        "fit": [make_context("box", rng, pools) for _ in range(n_fit)],
        "city": [make_context("city", rng, pools) for _ in range(n_held)],
        "color": [make_context("color", rng, pools) for _ in range(n_held)],
        "filler": [make_context("box", rng, pools, filler=True) for _ in range(n_filler)],
    }
    edit_ctxs = [make_context("box", rng, pools) for _ in range(n_edit)]
    caps = {k: capture(lm, v, attr_ids) for k, v in sets.items()}
    acc = {k: dict(restricted=sum(c["correct"]) / len(c["correct"]),
                   top1=sum(c["top1"]) / len(c["top1"]),
                   p_gold=sum(c["p_gold"]) / len(c["p_gold"])) for k, c in caps.items()}
    print("accuracy:", json.dumps(acc, indent=1), flush=True)
    fit = fit_and_score(caps["fit"], {k: caps[k] for k in ("city", "color", "filler")})
    def score(v, l):
        r = fit[v][l]
        return (r["rho_city"] + r["rho_color"] + r["rho_city_12"] + r["rho_color_12"]) / 4
    pv, best = max(((v, l) for v in VARIANTS for l in LAYERS_FIT), key=lambda t: score(*t))
    prim = fit[pv]
    print("primary variant", pv, "best layer", best, "score", round(score(pv, best), 3), flush=True)
    pick = sorted(set(EDIT_LAYERS) | {best})
    print("best layer", best, "edit layers", pick, flush=True)
    edits = run_edits(lm, edit_ctxs, prim, pick, attr_ids)
    meta = dict(model=MODEL, n_fit=n_fit, n_held=n_held, n_filler=n_filler, n_edit=n_edit,
                acc=acc, best_layer=best, edit_layers=pick, edit_variant=pv,
                pools={k: len(v) for k, v in pools.items()}, seconds=round(time.time() - t0),
                quick=quick)
    OUT.mkdir(parents=True, exist_ok=True)
    slim = {v: {l: {k: x for k, x in r.items() if k not in ("mu", "u", "means", "sigma", "w")}
                for l, r in fit[v].items()} for v in fit}
    tag = "-quick" if quick else ""
    (OUT / f"oi{tag}.json").write_text(json.dumps(dict(meta=meta, layers=slim, edits=edits), indent=1))
    torch.save({v: {l: dict(mu=fit[v][l]["mu"], u=fit[v][l]["u"], sigma=fit[v][l]["sigma"], w=fit[v][l]["w"])
                    for l in pick} for v in fit},
               OUT / f"oi-pc1{tag}.pt")
    (OUT / f"report{tag}.md").write_text(report(meta, slim, edits, pick))
    print(f"done in {meta['seconds']}s → {OUT}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "oi":
        sys.exit(__doc__)
    main(quick="--quick" in sys.argv)
