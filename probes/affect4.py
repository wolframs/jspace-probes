"""affect-04 — the exit-gate FAMILY DISCRIMINATOR on gemma-12b.

Why this model decides it (see results/affect03-g4b/thoughts.md):
qwen-27b shows causal emotion gating of the loop exit (calm grants
im_end, desperate blocks; matched randoms null). gemma-4b shows
margin-thinning but NO exit — its runner-up is ".", <end_of_turn>
never adjacent ("the gate needs a door"), and per apparatus-07 it
lacks the second commitment-sharpening stage. gemma-12b HAS the
second stage (L32-43, audit-03 convergence) — so:
  - if g12b shows exit-gating -> the gate is a function of stage 2
    (staircase account), not a qwen quirk;
  - if g12b has a door (exit token adjacent) but still no gating ->
    exit-gating is qwen-specific after all;
  - if g12b has no door either -> exit economy, not stage 2, was
    the g4b blocker and the discriminator needs a new design.
Preregistered as P15 in PREDICTIONS.md BEFORE the run.

Dose rule (affect-03 scope note): alpha_e scales per family to its
own alpha*_typo. g12b alpha* = 0.0106 at MID [28,31,34,37]
(audit-03 bracket, measured band). Full ladder x condition factorial
from the start — no single-dose gamble (the g4b lesson).

Part D piggybacks P6 (PREDICTIONS.md): unsteered teacher-forced lens
top1-top2 PROB margin over the assistant span, layers around g12b's
measured onset, comparable to qwen's 0.204/0.205 at L28/32
(u18-margin.json recipe). int8-lens caveat applies (specimen 5):
this is a readout comparison, not a causal claim.

Output: results/affect04-g12b/{affect04.json, report.md}
Usage:  .venv/bin/python probes/affect4.py [run|analyze|both]
"""

import json
import re
import sys

import torch

from lab import CONFIGS, RESULTS, Steering, _strip_bos, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer
from fanout import TYPO, WATER, assess
from loops import loop_gram, _null

MODEL = "gemma-12b"
MID_G12B = [28, 31, 34, 37]            # audit-03 measured band
E_LAYERS_G12B = [28, 30, 32, 34, 36, 38, 40, 42]   # BANDS ws 28-45
SCOUT = [0.0106, 0.015, 0.0212, 0.03, 0.0424]      # multiples of alpha*
LADDER = [0.004, 0.008, 0.015, 0.03]   # alpha_e, family-scaled
MARGIN_LAYERS = [8, 21, 24, 28, 31, 34, 37, 40, 44]
N_STEER, N_FREE, N_BASE = 50, 100, 200
OUT = RESULTS / "affect04-g12b"


def _prompt_ids(lm):
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    prefix = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        [{"role": "user", "content": WATER}], tokenize=False,
        add_generation_prompt=True, **tkw))
    return lm.model.encode(prefix, max_length=1_000_000)


def _gen(lm, ids, ctx, n_new):
    with ctx, torch.no_grad():
        out = lm.model._hf_model.generate(
            ids, max_new_tokens=n_new, do_sample=False,
            output_scores=True, return_dict_in_generate=True)
    text = lm.tok.decode(out.sequences[0, ids.shape[1]:],
                         skip_special_tokens=True)
    margins, top5_0 = [], None
    for i, s in enumerate(out.scores):
        vals, idxs = s[0].float().topk(5)
        margins.append(round(float(vals[0] - vals[1]), 3))
        if i == 0:
            top5_0 = [[lm.tok.decode([int(t)]), round(float(v), 2)]
                      for t, v in zip(idxs, vals)]
    return out.sequences, text, margins, top5_0


def _cell(lm, out1, g1, n1, ctx):
    _, cont, margins, top5_0 = _gen(lm, out1, ctx, N_FREE)
    cont_norm = " ".join(re.findall(r"[A-Za-z']+", cont.lower()))
    g2, n2 = loop_gram(cont)
    return {"forced_loop4": [g1, n1],
            "persists": (bool(g1) and n1 >= 3
                         and cont_norm.count(g1) >= 2),
            "released_loop4": [g2, n2], "released_text": cont,
            "margins": margins, "top5_step0": top5_0}


def run() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)
    ids = _prompt_ids(lm)
    res = {"model": MODEL, "mid": MID_G12B, "e_layers": E_LAYERS_G12B,
           "ladder": LADDER, "scout": []}

    def save():
        (OUT / "affect04.json").write_text(json.dumps(res, indent=1))

    # ---- A: dose scout (find the family's own deep loop) -------------
    forced = {}
    for at in SCOUT:
        with Steering(lm, TYPO, MID_G12B, "amplify", at), torch.no_grad():
            out1 = lm.model._hf_model.generate(
                ids, max_new_tokens=N_STEER, do_sample=False)
        text = lm.tok.decode(out1[0, ids.shape[1]:],
                             skip_special_tokens=True)
        g, n = loop_gram(text)
        words = re.findall(r"[A-Za-z']+", text.lower())
        token_loop = (len(set(words[-20:])) <= 2) if len(words) >= 20 \
            else False
        forced[at] = (out1, g, n, token_loop)
        res["scout"].append({"alpha_typo": at, "flags": assess(text),
                             "loop4": [g, n], "token_loop": token_loop,
                             "text": text})
        print(f"SCOUT a={at}: flags={assess(text) or 'intact'} "
              f"loop4={g!r}x{n} token_loop={token_loop} "
              f"{text[:70]!r}", flush=True)
        save()

    loopy = [a for a in SCOUT if forced[a][2] >= 3]
    deep = [a for a in SCOUT if forced[a][3]]
    a_deep = min(deep) if deep else (max(loopy) if loopy else SCOUT[-1])
    a_mid = max([a for a in loopy if a < a_deep], default=None)
    res["a_mid"], res["a_deep"] = a_mid, a_deep
    print(f"chosen: a_mid={a_mid} a_deep={a_deep}", flush=True)

    # ---- B: full factorial — {none} + emotions x ladder --------------
    res["grid"] = []
    for at in [a for a in (a_mid, a_deep) if a is not None]:
        out1, g1, n1, _ = forced[at]
        cells = [("none", 0.0, lambda ae: _null())]
        for ae in LADDER:
            cells += [
                ("amp-desperate", ae, lambda ae=ae: AffectSteer(
                    lm, V, emos.index("desperate"), E_LAYERS_G12B,
                    "amplify", alpha=ae)),
                ("amp-calm", ae, lambda ae=ae: AffectSteer(
                    lm, V, emos.index("calm"), E_LAYERS_G12B,
                    "amplify", alpha=ae)),
                ("amp-rand1", ae, lambda ae=ae: AffectSteer(
                    lm, V, 0, E_LAYERS_G12B, "amplify", alpha=ae,
                    rand_seed=1)),
                ("amp-rand2", ae, lambda ae=ae: AffectSteer(
                    lm, V, 0, E_LAYERS_G12B, "amplify", alpha=ae,
                    rand_seed=2)),
            ]
        for cname, ae, mk in cells:
            cell = _cell(lm, out1, g1, n1,
                         mk(ae) if cname != "none" else _null())
            cell.update({"alpha_typo": at, "cond": cname, "alpha_e": ae})
            res["grid"].append(cell)
            m = cell["margins"]
            print(f"  a={at} ae={ae} {cname:13s} "
                  f"persists={cell['persists']} "
                  f"loop4={cell['released_loop4']!r} "
                  f"nsteps={len(m)} m0={m[0]:.1f} mend={m[-1]:.1f}",
                  flush=True)
            save()

    # ---- D: P6 margin measurement (unsteered, own WATER answer) ------
    with _null(), torch.no_grad():
        out_b = lm.model._hf_model.generate(
            ids, max_new_tokens=N_BASE, do_sample=False)
    base_text = lm.tok.decode(out_b[0, ids.shape[1]:],
                              skip_special_tokens=True)
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    full = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        [{"role": "user", "content": WATER},
         {"role": "assistant", "content": base_text}],
        tokenize=False, add_generation_prompt=False, **tkw))
    a_start = ids.shape[1]
    lens_logits, _, _ = lm.lens.apply(
        lm.model, full, positions=None, layers=MARGIN_LAYERS,
        max_seq_len=1200)
    p6 = {}
    for layer, block in lens_logits.items():
        p = torch.softmax(block[a_start:].float(), dim=-1)
        top2 = p.topk(2, dim=-1).values
        p6[str(layer)] = round((top2[:, 0] - top2[:, 1]).mean().item(), 4)
    res["p6_margins"] = p6
    res["p6_base_text"] = base_text
    print(f"P6 margins: {p6}", flush=True)
    save()
    print("RUN DONE", flush=True)


def analyze() -> None:
    res = json.loads((OUT / "affect04.json").read_text())
    lines = ["# affect-04 gemma-12b exit-gate discriminator", "",
             f"MID {res['mid']}, emotion layers {res['e_layers']}, "
             f"ladder {res['ladder']}; a_mid={res.get('a_mid')} "
             f"a_deep={res.get('a_deep')}", "", "## Dose scout", ""]
    for s in res["scout"]:
        lines.append(f"- a={s['alpha_typo']}: "
                     f"{', '.join(s['flags']) or 'intact'} "
                     f"loop4={s['loop4']} token_loop={s['token_loop']}")
        lines.append(f"  - `{s['text'][:110]}`")
    lines += ["", "## Grid (ladder x condition)", ""]
    door = None
    for c in res.get("grid", []):
        m = c["margins"]
        tag = ("P" if c["persists"]
               else "NEWLOOP" if c["released_loop4"][1] >= 10
               else f"snap@{len(m)}")
        lines.append(f"- a={c['alpha_typo']} ae={c['alpha_e']} "
                     f"{c['cond']}: {tag}, "
                     f"loop4={c['released_loop4']}, "
                     f"m {m[0]:.1f}->{m[-1]:.1f}, "
                     f"top5(0)={c['top5_step0']}")
        lines.append(f"  - `{c['released_text'][:110]}`")
        if c["cond"] == "none" and c["alpha_typo"] == res.get("a_deep"):
            door = any("end_of_turn" in t for t, _ in c["top5_step0"])
    lines += ["", f"## Door check (deep loop, unsteered step-0 top-5): "
              f"exit token adjacent = **{door}**", ""]
    if res.get("p6_margins"):
        lines += ["", "## P6: unsteered lens prob margins "
                  "(assistant span mean; qwen ref 0.204/0.205 at "
                  "L28/32)", "",
                  "| " + " | ".join(f"L{l}" for l in
                                    sorted(map(int, res["p6_margins"]))
                                    ) + " |",
                  "|" + "---|" * len(res["p6_margins"]),
                  "| " + " | ".join(
                      f"{res['p6_margins'][str(l)]:.3f}" for l in
                      sorted(map(int, res["p6_margins"]))) + " |"]
    (OUT / "report.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'report.md'}", flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    if what in ("run", "both"):
        run()
    if what in ("analyze", "both"):
        analyze()
