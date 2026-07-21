"""affect-03 — the causal arm (board affect-03; P14 preregistered
2026-07-21 in PREDICTIONS.md BEFORE this run).

Does the functional-emotion state causally gate the u18 loop regimes,
or ride them as a correlational passenger? Key design decision: under
greedy decoding a forced-phase co-steer can only matter by changing the
emitted text, so the clean lever is the FREE phase — forced phase
identical per alpha_typo, then release the TYPO cluster and steer an
emotion direction alone while the transcript tries to sustain itself.

Part 0  PRE-FLIGHT: WATER answer, 150 tok, desperate-only / calm-only
        amplify (alpha 0.12, E_LAYERS) — steer sanity anchor + "does
        desperate alone loop a healthy model?".
Part A  BOUNDARY GRID: u18 hysteresis protocol (TYPO amplify at MID,
        50 forced + 100 free), free-phase condition grid:
          alpha_typo in {0.42, 0.48, 0.54, 0.60, 0.68}
          free-phase in {none, amp-desperate, amp-calm, amp-rand1,
                         amp-rand2, abl-desperate, abl-rand1}
        DVs: persists (loops.py criterion), per-step output-logit
        margin Delta_t = top1-top2 (the dose-sensitive readout; margin
        lineage: u18 part C / P6 / P12).
Part B  SONG: u19-read user turn, 200-tok response under {none,
        abl-vigilant, abl-rand1, abl-rand2} — does removing the tonic
        vigilance state change the response? z readout re-forwarded
        UNDER the same steer (rebuild between hooked layers is signal);
        wsnorm saved alongside (partial-out rule).

Emotion steering: per-layer affect-01 vectors (results/affect01-*/
vectors.pt, [E, L, D]) at E_LAYERS = every 4th ws layer; amplify
h += a*||h||*v_hat, ablate h -= (h.v_hat)v_hat (MECHANICS 3a/3b).
Matched random controls: seeded unit Gaussians per layer, same layers,
same alpha (MECHANICS 3c — for BOTH amplify and ablate arms).

Usage:  .venv/bin/python probes/affect3.py run
        .venv/bin/python probes/affect3.py analyze
"""

import json
import re
import sys

import torch

import lab
from lab import CONFIGS, RESULTS, Steering, _strip_bos, get_model
from affect import BANDS
from affect2 import _all_resid, _load_vectors
from affect import outdir as a1dir
from fanout import TYPO, WATER, assess
from loops import MID, N_FREE, N_STEER, loop_gram, _null

MODEL = "qwen-27b"
TYPO_ALPHAS = [0.42, 0.48, 0.54, 0.60, 0.68]
E_LAYERS = [28, 32, 36, 40, 44, 48, 52, 56]
ALPHA_E = 0.12
OUT = RESULTS / "affect03-q27b"
B_EMOS = ("vigilant", "afraid", "anxious", "calm", "loving",
          "distressed")


class AffectSteer:
    """Amplify/ablate one emotion vector (or a seeded matched random
    direction) at given layers; hook convention as lab.Steering."""

    def __init__(self, lm, V, e_idx, layers, mode="amplify",
                 alpha=ALPHA_E, rand_seed=None):
        self._per_layer = {}
        for l in layers:
            if rand_seed is not None:
                g = torch.Generator().manual_seed(rand_seed * 1000 + l)
                v = torch.randn(V.shape[-1], generator=g)
            else:
                v = V[e_idx, l].clone()
            self._per_layer[l] = (v / v.norm()).float()
        self._mode, self._alpha = mode, alpha
        self._blocks = lm.model.layers
        self._handles = []

    def _make_hook(self, layer):
        v = self._per_layer[layer]
        mode, alpha = self._mode, self._alpha

        def hook(module, inputs, output):
            t = output if torch.is_tensor(output) else output[0]
            h = t.float()
            vv = v.to(h.device)
            if mode == "ablate":
                h = h - (h @ vv).unsqueeze(-1) * vv
            else:
                h = h + alpha * h.norm(dim=-1, keepdim=True) * vv
            h = h.to(t.dtype)
            return h if torch.is_tensor(output) else (h, *output[1:])

        return hook

    def __enter__(self):
        for layer in self._per_layer:
            self._handles.append(self._blocks[layer]
                                 .register_forward_hook(
                                     self._make_hook(layer)))
        return self

    def __exit__(self, *exc):
        for h in self._handles:
            h.remove()
        self._handles = []


def _conds(lm, V, emos):
    """Free-phase condition factory (fresh contexts per call)."""
    e = emos.index
    return [
        ("none", lambda: _null()),
        ("amp-desperate", lambda: AffectSteer(lm, V, e("desperate"),
                                              E_LAYERS, "amplify")),
        ("amp-calm", lambda: AffectSteer(lm, V, e("calm"),
                                         E_LAYERS, "amplify")),
        ("amp-rand1", lambda: AffectSteer(lm, V, 0, E_LAYERS,
                                          "amplify", rand_seed=1)),
        ("amp-rand2", lambda: AffectSteer(lm, V, 0, E_LAYERS,
                                          "amplify", rand_seed=2)),
        ("abl-desperate", lambda: AffectSteer(lm, V, e("desperate"),
                                              E_LAYERS, "ablate")),
        ("abl-rand1", lambda: AffectSteer(lm, V, 0, E_LAYERS,
                                          "ablate", rand_seed=1)),
    ]


def _gen_margins(lm, ids, ctx, n_new):
    """Greedy-generate n_new under ctx; return (text, per-step top1-top2
    logit margins, first-10 top1 tokens)."""
    with ctx, torch.no_grad():
        out = lm.model._hf_model.generate(
            ids, max_new_tokens=n_new, do_sample=False,
            output_scores=True, return_dict_in_generate=True)
    text = lm.tok.decode(out.sequences[0, ids.shape[1]:],
                         skip_special_tokens=True)
    margins, tops = [], []
    for i, s in enumerate(out.scores):
        vals, idxs = s[0].float().topk(2)
        margins.append(round(float(vals[0] - vals[1]), 3))
        if i < 10:
            tops.append(lm.tok.decode([int(idxs[0])]))
    return text, margins, tops


def run() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)
    tok = lm.tok
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    res = {"model": MODEL, "e_layers": E_LAYERS, "alpha_e": ALPHA_E,
           "mid": MID, "n_steer": N_STEER, "n_free": N_FREE}

    def save():
        (OUT / "affect03.json").write_text(json.dumps(res, indent=1))

    # ---- Part 0: pre-flight -------------------------------------------
    prefix = _strip_bos(tok, tok.apply_chat_template(
        [{"role": "user", "content": WATER}], tokenize=False,
        add_generation_prompt=True, **tkw))
    ids = lm.model.encode(prefix, max_length=1_000_000)
    res["preflight"] = {}
    for emo in ("desperate", "calm"):
        ctx = AffectSteer(lm, V, emos.index(emo), E_LAYERS, "amplify")
        text, margins, _ = _gen_margins(lm, ids, ctx, 150)
        g, n = loop_gram(text)
        res["preflight"][emo] = {
            "text": text, "flags": assess(text), "loop4": [g, n],
            "margin_mean": round(sum(margins) / len(margins), 3)}
        print(f"PRE {emo}: flags={assess(text) or 'intact'} "
              f"loop4={g!r}x{n}\n  {text[:120]!r}", flush=True)
    save()

    # ---- Part A: boundary grid ----------------------------------------
    res["boundary"] = []
    for at in TYPO_ALPHAS:
        with Steering(lm, TYPO, MID, "amplify", at), torch.no_grad():
            out1 = lm.model._hf_model.generate(
                ids, max_new_tokens=N_STEER, do_sample=False)
        steered = tok.decode(out1[0, ids.shape[1]:],
                             skip_special_tokens=True)
        g1, n1 = loop_gram(steered)
        print(f"=== a_typo={at}: forced {assess(steered) or 'intact'} "
              f"{g1!r}x{n1}", flush=True)
        for cname, mk in _conds(lm, V, emos):
            cont, margins, tops = _gen_margins(lm, out1, mk(), N_FREE)
            cont_norm = " ".join(re.findall(r"[A-Za-z']+", cont.lower()))
            persists = (bool(g1) and n1 >= 3
                        and cont_norm.count(g1) >= 2)
            g2, n2 = loop_gram(cont)
            res["boundary"].append({
                "alpha_typo": at, "cond": cname,
                "forced_loop4": [g1, n1], "persists": persists,
                "released_loop4": [g2, n2],
                "released_flags": assess(cont), "released_text": cont,
                "margins": margins, "top1_first10": tops})
            print(f"  {cname:14s} persists={persists} "
                  f"loop4={g2!r}x{n2} m0={margins[0]:.1f} "
                  f"mend={margins[-1]:.1f}", flush=True)
            save()

    # ---- Part B: song / vigilant ablation -----------------------------
    conv = json.loads(
        (RESULTS / "u19-read-q27b" / "record.json").read_text())
    song_prefix = _strip_bos(tok, tok.apply_chat_template(
        [conv["conversation"][0]], tokenize=False,
        add_generation_prompt=True, **tkw))
    sids = lm.model.encode(song_prefix, max_length=1_000_000)
    pb = torch.load(a1dir(MODEL) / "projbase.pt")
    mu, sd = pb["mu"], pb["sd"]
    lo, hi, _ = BANDS[MODEL]
    e = emos.index
    bconds = [("none", lambda: _null()),
              ("abl-vigilant", lambda: AffectSteer(
                  lm, V, e("vigilant"), E_LAYERS, "ablate")),
              ("abl-rand1", lambda: AffectSteer(
                  lm, V, 0, E_LAYERS, "ablate", rand_seed=11)),
              ("abl-rand2", lambda: AffectSteer(
                  lm, V, 0, E_LAYERS, "ablate", rand_seed=12))]
    res["song"] = []
    for cname, mk in bconds:
        text, margins, _ = _gen_margins(lm, sids, mk(), 200)
        # state during generation: re-forward under the SAME context
        full_ids = lm.model.encode(song_prefix + text,
                                   max_length=1_000_000)
        with mk():
            H = _all_resid(lm, full_ids)             # [L, seq, D]
        z = (torch.einsum("lsd,eld->els", H, V)
             - mu.unsqueeze(-1)) / sd.unsqueeze(-1)
        span = slice(sids.shape[1], None)            # response positions
        ws = z[:, lo:hi, span].mean(1)               # [E, resp]
        wsn = H[lo:hi, span].norm(dim=-1).mean(0)    # [resp]
        res["song"].append({
            "cond": cname, "text": text,
            "margin_mean": round(sum(margins) / len(margins), 3),
            "ws_z": {emo: round(float(ws[e(emo)].mean()), 3)
                     for emo in B_EMOS},
            "wsnorm_mean": round(float(wsn.mean()), 1)})
        print(f"SONG {cname}: " + ", ".join(
            f"{emo} {res['song'][-1]['ws_z'][emo]:+.2f}"
            for emo in B_EMOS[:4]) + f" | {text[:90]!r}", flush=True)
        save()
    print("RUN DONE", flush=True)


def analyze() -> None:
    res = json.loads((OUT / "affect03.json").read_text())
    lines = ["# affect-03 — causal arm (P14)", "",
             f"amplify alpha={res['alpha_e']} at layers "
             f"{res['e_layers']}; hysteresis: {res['n_steer']} forced + "
             f"{res['n_free']} free.", "", "## Part 0 — pre-flight", ""]
    for emo, p in res.get("preflight", {}).items():
        lines.append(f"- {emo}-only: flags={p['flags'] or 'intact'} "
                     f"loop4={p['loop4']} margin {p['margin_mean']}")
        lines.append(f"  - `{p['text'][:140]}`")
    lines += ["", "## Part A — boundary grid (persists / margin "
              "first->last)", ""]
    conds = []
    for c in res.get("boundary", []):
        if c["cond"] not in conds:
            conds.append(c["cond"])
    alphas = sorted({c["alpha_typo"] for c in res.get("boundary", [])})
    lines.append("| a_typo | " + " | ".join(conds) + " |")
    lines.append("|" + "---|" * (len(conds) + 1))
    idx = {(c["alpha_typo"], c["cond"]): c
           for c in res.get("boundary", [])}
    for at in alphas:
        row = [f"| {at} "]
        for cn in conds:
            c = idx.get((at, cn))
            if not c:
                row.append("| — ")
                continue
            m = c["margins"]
            row.append(f"| {'P' if c['persists'] else 'snap'} "
                       f"{m[0]:.0f}->{m[-1]:.0f} ")
        lines.append("".join(row) + "|")
    lines += ["", "Boundary (lowest persisting a_typo) per condition:",
              ""]
    for cn in conds:
        ps = [at for at in alphas
              if idx.get((at, cn), {}).get("persists")]
        lines.append(f"- {cn}: {min(ps) if ps else 'never'}")
    lines += ["", "## Part B — song, vigilant ablation (ws z over "
              "response; wsnorm alongside per the partial-out rule)",
              ""]
    for s in res.get("song", []):
        lines.append(f"- {s['cond']}: " + ", ".join(
            f"{k} {v:+.2f}" for k, v in s["ws_z"].items())
            + f"; wsnorm {s['wsnorm_mean']}")
        lines.append(f"  - `{s['text'][:140]}`")
    (OUT / "report.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'report.md'}", flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "run"
    if what in ("run", "both"):
        run()
    if what in ("analyze", "both"):
        analyze()
