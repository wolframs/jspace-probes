"""affect-03 follow-up: WHO is the runner-up? Top-5 per free-phase step
at the two hot cells of the boundary grid (a_typo 0.60 and 0.68), to
adjudicate closure-gate vs valence-general-opposition readings of the
Part A result. Writes results/affect03-q27b/top5.json.

Usage: .venv/bin/python probes/affect3b.py
"""

import json

import torch

import lab
from lab import CONFIGS, Steering, _strip_bos, get_model
from affect2 import _load_vectors
from affect3 import AffectSteer, E_LAYERS, OUT
from fanout import TYPO, WATER
from loops import MID, N_FREE, N_STEER, _null

MODEL = "qwen-27b"
CELLS = {0.60: ["none", "amp-desperate", "amp-calm"],
         0.68: ["none", "amp-desperate", "amp-calm", "amp-rand1"]}
KEEP = list(range(20)) + list(range(20, 100, 10))


def main() -> None:
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)
    tok = lm.tok
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    prefix = _strip_bos(tok, tok.apply_chat_template(
        [{"role": "user", "content": WATER}], tokenize=False,
        add_generation_prompt=True, **tkw))
    ids = lm.model.encode(prefix, max_length=1_000_000)

    def ctx(name):
        if name == "none":
            return _null()
        kind, emo = name.split("-")
        if emo.startswith("rand"):
            return AffectSteer(lm, V, 0, E_LAYERS, "amplify",
                               rand_seed=int(emo[4:]))
        return AffectSteer(lm, V, emos.index(emo), E_LAYERS, "amplify")

    out = []
    for at, conds in CELLS.items():
        with Steering(lm, TYPO, MID, "amplify", at), torch.no_grad():
            out1 = lm.model._hf_model.generate(
                ids, max_new_tokens=N_STEER, do_sample=False)
        for cname in conds:
            with ctx(cname), torch.no_grad():
                g = lm.model._hf_model.generate(
                    out1, max_new_tokens=N_FREE, do_sample=False,
                    output_scores=True, return_dict_in_generate=True)
            steps = []
            for i, s in enumerate(g.scores):
                if i not in KEEP:
                    continue
                vals, idxs = s[0].float().topk(5)
                steps.append({"step": i, "top5": [
                    [tok.decode([int(t)]), round(float(v), 2)]
                    for t, v in zip(idxs, vals)]})
            out.append({"alpha_typo": at, "cond": cname,
                        "steps": steps})
            head = steps[0]["top5"]
            print(f"a={at} {cname}: step0 " + " | ".join(
                f"{t!r} {v}" for t, v in head), flush=True)
    (OUT / "top5.json").write_text(json.dumps(out, indent=1))
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
