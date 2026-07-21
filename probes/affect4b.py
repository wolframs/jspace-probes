"""affect-04b — deeper scout for gemma-12b's self-sustaining loop.

The affect4.py scout topped out at 4x alpha* (0.0424) with a weak
'Anyways'x3 and NO persisting released loop anywhere — the exit-gate
paradigm had no substrate. The forced phase degenerates through
punctuation/whitespace fields rather than word loops, but the
'Anyways' trend suggests a word attractor deeper in. Scout
{6, 8, 11}x alpha*; wherever the released (unsteered) free phase
persists, run the emotion grid there at the two doses that were
clean-on-randoms in affect4 (0.004, 0.008) plus 0.015 with both
randoms as the non-specificity sentinel.

Output: results/affect04-g12b/{affect04b.json, appended report}
Usage:  .venv/bin/python probes/affect4b.py
"""

import json
import re

import torch

from lab import RESULTS, Steering, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer
from affect4 import (E_LAYERS_G12B, MID_G12B, MODEL, N_STEER, OUT,
                     _cell, _gen, _prompt_ids)
from fanout import TYPO, assess
from loops import loop_gram, _null

SCOUT2 = [0.06, 0.085, 0.12]
LADDER2 = [0.004, 0.008, 0.015]


def main() -> None:
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)
    ids = _prompt_ids(lm)
    res = {"model": MODEL, "scout2": [], "grid2": []}

    def save():
        (OUT / "affect04b.json").write_text(json.dumps(res, indent=1))

    substrate = None
    for at in SCOUT2:
        with Steering(lm, TYPO, MID_G12B, "amplify", at), torch.no_grad():
            out1 = lm.model._hf_model.generate(
                ids, max_new_tokens=N_STEER, do_sample=False)
        text = lm.tok.decode(out1[0, ids.shape[1]:],
                             skip_special_tokens=True)
        g, n = loop_gram(text)
        row = {"alpha_typo": at, "flags": assess(text),
               "loop4": [g, n], "text": text}
        # does it persist unsteered?
        cell = _cell(lm, out1, g, n, _null())
        row["released_persists"] = cell["persists"]
        row["released_loop4"] = cell["released_loop4"]
        row["top5_step0"] = cell["top5_step0"]
        res["scout2"].append(row)
        print(f"SCOUT2 a={at}: loop4={g!r}x{n} "
              f"persists={cell['persists']} "
              f"rel={cell['released_loop4']!r} "
              f"top5(0)={cell['top5_step0']}", flush=True)
        save()
        if cell["persists"] and substrate is None:
            substrate = (at, out1, g, n)

    if substrate is None:
        print("NO SUBSTRATE: no persisting released loop up to "
              f"{SCOUT2[-1]} — exit-gate untestable on g12b in this "
              "paradigm", flush=True)
        save()
        return

    at, out1, g1, n1 = substrate
    res["substrate_alpha"] = at
    for ae in LADDER2:
        conds = [("amp-desperate",
                  lambda ae=ae: AffectSteer(
                      lm, V, emos.index("desperate"), E_LAYERS_G12B,
                      "amplify", alpha=ae)),
                 ("amp-calm",
                  lambda ae=ae: AffectSteer(
                      lm, V, emos.index("calm"), E_LAYERS_G12B,
                      "amplify", alpha=ae)),
                 ("amp-rand1",
                  lambda ae=ae: AffectSteer(
                      lm, V, 0, E_LAYERS_G12B, "amplify", alpha=ae,
                      rand_seed=1)),
                 ("amp-rand2",
                  lambda ae=ae: AffectSteer(
                      lm, V, 0, E_LAYERS_G12B, "amplify", alpha=ae,
                      rand_seed=2))]
        for cname, mk in conds:
            cell = _cell(lm, out1, g1, n1, mk())
            cell.update({"alpha_typo": at, "cond": cname,
                         "alpha_e": ae})
            res["grid2"].append(cell)
            m = cell["margins"]
            print(f"  a={at} ae={ae} {cname:13s} "
                  f"persists={cell['persists']} "
                  f"loop4={cell['released_loop4']!r} "
                  f"nsteps={len(m)} m0={m[0]:.1f} mend={m[-1]:.1f}",
                  flush=True)
            save()
    print("RUN DONE", flush=True)

    lines = ["", "## Deeper scout (affect4b)", ""]
    for s in res["scout2"]:
        lines.append(f"- a={s['alpha_typo']}: loop4={s['loop4']} "
                     f"released_persists={s['released_persists']} "
                     f"rel={s['released_loop4']} "
                     f"top5(0)={s['top5_step0']}")
        lines.append(f"  - `{s['text'][:110]}`")
    if res.get("substrate_alpha"):
        lines += ["", f"## Grid at substrate a="
                  f"{res['substrate_alpha']}", ""]
        for c in res["grid2"]:
            m = c["margins"]
            tag = ("P" if c["persists"]
                   else "NEWLOOP" if c["released_loop4"][1] >= 10
                   else f"snap@{len(m)}")
            lines.append(f"- ae={c['alpha_e']} {c['cond']}: {tag}, "
                         f"loop4={c['released_loop4']}, "
                         f"m {m[0]:.1f}->{m[-1]:.1f}, "
                         f"top5(0)={c['top5_step0']}")
    with open(OUT / "report.md", "a") as f:
        f.write("\n".join(lines))
    print("report appended", flush=True)


if __name__ == "__main__":
    main()
