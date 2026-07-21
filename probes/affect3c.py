"""affect-03 follow-up rungs (Batch 1 of the 2026-07-21 evening
autonomous series), one qwen-27b load:

  1  DOSE: alpha_e dose-response at the two hot cells (a_typo 0.60,
     0.68) x {desperate, calm} x alpha_e {0.03, 0.06, 0.12, 0.24}
     + rand1 at 0.24 (strongest-dose generic anchor). At what dose does
     calm's rescue kick in / desperate's boundary-lowering appear, and
     is the effect graded or a threshold?
  2  SECOND STIMULUS: same protocol on a fresh prompt (PLANT) at
     a_typo {0.60, 0.68} x {none, desperate, calm, rand1} at
     alpha_e=0.12 — does the exit-gate result generalize beyond WATER?
     (u18 predicts the terminal loop token again comes from the TYPO
     cluster's own field; whatever forms is data.)
  3  L0 ADJUDICATION (specimen 7 close-out): u18-hyst-a0680 " luckily"
     input columns, lens layers=[0], use_jacobian True vs False. If
     the variant-form cluster (amongst/whilst/neighbouring/learnt/
     Javascript) is absent under the vanilla logit lens, the cast
     entry was J_0 transport (specimen-6 pattern), closing the
     ' Javascript' mystery at the mechanism level.

Outputs: results/affect03-q27b/{dose.json,secondstim.json,report2.md},
results/u18-hyst-a0680-q27b/l0check.json.

Usage: .venv/bin/python probes/affect3c.py [run|analyze|both]
"""

import json
import re
import sys

import torch

import lab
from lab import CONFIGS, RESULTS, Steering, _strip_bos, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS, OUT
from fanout import TYPO, WATER, assess
from loops import MID, N_FREE, N_STEER, loop_gram, _null

MODEL = "qwen-27b"
PLANT = "Explain how plants make their food in two sentences."
DOSES = [0.03, 0.06, 0.12, 0.24]
HOT = [0.60, 0.68]
VARIANT_CLUSTER = [" amongst", " whilst", " neighbouring", " learnt",
                   " Javascript"]


def _gen(lm, ids, ctx, n_new, top5_steps=10):
    with ctx, torch.no_grad():
        out = lm.model._hf_model.generate(
            ids, max_new_tokens=n_new, do_sample=False,
            output_scores=True, return_dict_in_generate=True)
    text = lm.tok.decode(out.sequences[0, ids.shape[1]:],
                         skip_special_tokens=True)
    margins, top5 = [], []
    for i, s in enumerate(out.scores):
        vals, idxs = s[0].float().topk(5)
        margins.append(round(float(vals[0] - vals[1]), 3))
        if i < top5_steps:
            top5.append([[lm.tok.decode([int(t)]), round(float(v), 2)]
                         for t, v in zip(idxs, vals)])
    return text, margins, top5


def _cell(lm, out1, g1, n1, ctx, n_free=N_FREE):
    cont, margins, top5 = _gen(lm, out1, ctx, n_free)
    cont_norm = " ".join(re.findall(r"[A-Za-z']+", cont.lower()))
    g2, n2 = loop_gram(cont)
    return {
        "persists": bool(g1) and n1 >= 3 and cont_norm.count(g1) >= 2,
        "released_loop4": [g2, n2], "released_flags": assess(cont),
        "released_text": cont, "margins": margins, "top5_first": top5}


def _forced(lm, ids, at):
    with Steering(lm, TYPO, MID, "amplify", at), torch.no_grad():
        out1 = lm.model._hf_model.generate(
            ids, max_new_tokens=N_STEER, do_sample=False)
    steered = lm.tok.decode(out1[0, ids.shape[1]:],
                            skip_special_tokens=True)
    g1, n1 = loop_gram(steered)
    return out1, steered, g1, n1


def _prompt_ids(lm, prompt):
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    prefix = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False,
        add_generation_prompt=True, **tkw))
    return lm.model.encode(prefix, max_length=1_000_000)


def run() -> None:
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)
    ids = _prompt_ids(lm, WATER)

    # ---- 1: dose-response --------------------------------------------
    dose = []
    for at in HOT:
        out1, steered, g1, n1 = _forced(lm, ids, at)
        print(f"=== DOSE a_typo={at}: forced {g1!r}x{n1}", flush=True)
        conds = ([("desperate", a) for a in DOSES]
                 + [("calm", a) for a in DOSES] + [("rand1", 0.24)])
        for emo, ae in conds:
            if emo == "rand1":
                ctx = AffectSteer(lm, V, 0, E_LAYERS, "amplify",
                                  alpha=ae, rand_seed=1)
            else:
                ctx = AffectSteer(lm, V, emos.index(emo), E_LAYERS,
                                  "amplify", alpha=ae)
            c = _cell(lm, out1, g1, n1, ctx)
            c.update({"alpha_typo": at, "emo": emo, "alpha_e": ae})
            dose.append(c)
            m = c["margins"]
            print(f"  {emo:9s} ae={ae}: persists={c['persists']} "
                  f"loop4={c['released_loop4']} nsteps={len(m)} "
                  f"m0={m[0]:.1f} mend={m[-1]:.1f}", flush=True)
            (OUT / "dose.json").write_text(json.dumps(dose, indent=1))

    # ---- 2: second stimulus ------------------------------------------
    pids = _prompt_ids(lm, PLANT)
    second = {"prompt": PLANT, "cells": []}
    for at in HOT:
        out1, steered, g1, n1 = _forced(lm, pids, at)
        print(f"=== PLANT a_typo={at}: forced {g1!r}x{n1} "
              f"{steered[:70]!r}", flush=True)
        for cname in ("none", "desperate", "calm", "rand1"):
            if cname == "none":
                ctx = _null()
            elif cname == "rand1":
                ctx = AffectSteer(lm, V, 0, E_LAYERS, "amplify",
                                  rand_seed=1)
            else:
                ctx = AffectSteer(lm, V, emos.index(cname), E_LAYERS,
                                  "amplify")
            c = _cell(lm, out1, g1, n1, ctx)
            c.update({"alpha_typo": at, "cond": cname,
                      "forced_loop4": [g1, n1],
                      "forced_text": steered})
            second["cells"].append(c)
            m = c["margins"]
            print(f"  {cname:9s}: persists={c['persists']} "
                  f"loop4={c['released_loop4']} nsteps={len(m)} "
                  f"m0={m[0]:.1f} mend={m[-1]:.1f}", flush=True)
            (OUT / "secondstim.json").write_text(
                json.dumps(second, indent=1))

    # ---- 3: L0 adjudication ------------------------------------------
    rec = json.loads((RESULTS / "u18-hyst-a0680-q27b"
                      / "record.json").read_text())
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    full = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        rec["conversation"], tokenize=False,
        add_generation_prompt=False, **tkw))
    fids = lm.model.encode(full, max_length=1_000_000)
    toks = lm.tok.convert_ids_to_tokens(fids[0].tolist())
    lucky = [i for i, t in enumerate(toks)
             if "luckily" in t.lower()][:40:4]    # 10 sampled columns
    res = {"positions": lucky, "cluster": VARIANT_CLUSTER, "modes": {}}
    for jac in (True, False):
        logits, _, _ = lm.lens.apply(
            lm.model, full, positions=lucky, layers=[0],
            max_seq_len=1200, use_jacobian=jac)
        block = logits[0].float()                # [n_pos, vocab]
        top8 = block.topk(8, dim=-1).indices
        rows = [[lm.tok.decode([int(t)]) for t in r] for r in top8]
        hits = sum(any(c in r for c in VARIANT_CLUSTER) for r in rows)
        res["modes"]["jlens" if jac else "logitlens"] = {
            "top8_per_pos": rows,
            "cluster_hit_positions": hits, "n_positions": len(rows)}
        print(f"L0 {'J-lens' if jac else 'logit-lens'}: cluster hits "
              f"{hits}/{len(rows)}; pos0 top8={rows[0]}", flush=True)
    (RESULTS / "u18-hyst-a0680-q27b" / "l0check.json").write_text(
        json.dumps(res, indent=1))
    print("RUN DONE", flush=True)


def analyze() -> None:
    lines = ["# affect-03 follow-up rungs — dose, second stimulus, L0",
             ""]
    dj = OUT / "dose.json"
    if dj.exists():
        dose = json.loads(dj.read_text())
        lines += ["## 1 — alpha_e dose-response", "",
                  "| a_typo | emo | a_e | outcome | m0 -> mend |",
                  "|---|---|---|---|---|"]
        for c in dose:
            m = c["margins"]
            tag = ("P" if c["persists"]
                   else "NEWLOOP" if c["released_loop4"][1] >= 10
                   else f"snap@{len(m)}")
            lines.append(f"| {c['alpha_typo']} | {c['emo']} | "
                         f"{c['alpha_e']} | {tag} | "
                         f"{m[0]:.1f} -> {m[-1]:.1f} |")
    sj = OUT / "secondstim.json"
    if sj.exists():
        sec = json.loads(sj.read_text())
        lines += ["", f"## 2 — second stimulus: `{sec['prompt']}`", ""]
        for c in sec["cells"]:
            m = c["margins"]
            tag = ("P" if c["persists"]
                   else "NEWLOOP" if c["released_loop4"][1] >= 10
                   else f"snap@{len(m)}")
            lines.append(
                f"- a={c['alpha_typo']} {c['cond']}: {tag}, "
                f"loop4={c['released_loop4']}, "
                f"m {m[0]:.1f}->{m[-1]:.1f}")
            lines.append(f"  - `{c['released_text'][:120]}`")
    lj = RESULTS / "u18-hyst-a0680-q27b" / "l0check.json"
    if lj.exists():
        l0 = json.loads(lj.read_text())
        lines += ["", "## 3 — L0 variant-form cluster: J-lens vs "
                  "logit lens", ""]
        for mode, d in l0["modes"].items():
            lines.append(f"- {mode}: cluster present at "
                         f"{d['cluster_hit_positions']}/"
                         f"{d['n_positions']} sampled ' luckily' "
                         f"columns; example top-8: "
                         f"{d['top8_per_pos'][0]}")
    (OUT / "report2.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'report2.md'}", flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    if what in ("run", "both"):
        run()
    if what in ("analyze", "both"):
        analyze()
