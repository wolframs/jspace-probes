"""langval-viz — bring Unit 20 records up to the u18-hyst standard.

The dashboard record page renders the emotion state ribbon + overlay
whenever results/affect02-<rid>/affect.json exists. The affect arc got
this on viz day; Unit 20 (lv/lv2, 48 records) never did. This runner
closes the gap with one capture pass per record (affect2.cross math
verbatim: below/ws/motor band z + per-band norms, projbase z-scoring,
EMOTIONS.md §2), then emits the dashboard affect.json (affectviz
format, no danger pins — nothing was pinned in these prompts).

Per the full-instrument default (CLAUDE.md conventions, added
2026-08-07): substantive records ship the u18-grade treatment;
calibration/instrument-validity runs are the documented exception.

Usage:  .venv/bin/python probes/langval_viz.py <model>
        (gemma-4b | gemma-12b | qwen-27b; resumable, skips existing)
"""

import json
import sys

import torch

import lab
from lab import CONFIGS, RESULTS, _strip_bos, get_model
from affect import BANDS, EMOTIONS
from affect2 import _all_resid, _conversation_ids, _load_vectors, a2dir
from langval import _baseline

LV_LANGS = ["swift", "kotlin", "rust", "csharp", "python"]
LV2_LANGS = LV_LANGS + ["php"]


def record_ids(model: str) -> list[str]:
    m = {"gemma-4b": "g4b", "gemma-12b": "g12b", "qwen-27b": "q27b"}[model]
    ids = []
    if m in ("g12b", "q27b"):
        for c in ("pain", "praise"):
            ids += [f"lv-{c}-{l}-{m}" for l in LV_LANGS]
        ids += [f"lv-free-{m}", f"lv-neutral-{m}"]
    if m in ("g4b", "q27b"):
        for c in ("vox", "ther"):
            ids += [f"lv2-{c}-{l}-{m}" for l in LV2_LANGS]
    return ids


def _tokens(tok, model: str, rec: dict) -> list[str]:
    tkw = CONFIGS[model].get("template_kwargs", {})
    full = _strip_bos(tok, tok.apply_chat_template(
        rec["conversation"], tokenize=False,
        add_generation_prompt=False, **tkw))
    ids = tok(full, return_tensors="pt").input_ids[0].tolist()
    return [tok.convert_tokens_to_string([t])
            for t in tok.convert_ids_to_tokens(ids)]


def run(model: str) -> None:
    lm = get_model(model)
    V, emos = _load_vectors(model)
    mu, sd = _baseline(lm, model, V)
    lo, hi, _ = BANDS[model]
    for rid in record_ids(model):
        rdir = RESULTS / rid
        if not (rdir / "record.json").exists():
            print(f"  SKIP {rid}: no record", flush=True)
            continue
        d = a2dir(rid)
        if (d / "affect.json").exists():
            print(f"  skip {rid} (affect.json exists)", flush=True)
            continue
        rec = json.loads((rdir / "record.json").read_text())
        ids, toks = _conversation_ids(lm, rec)
        H = _all_resid(lm, ids)
        z = (torch.einsum("lsd,eld->els", H, V)
             - mu.unsqueeze(-1)) / sd.unsqueeze(-1)
        bands = {"below": z[:, :lo].mean(1), "ws": z[:, lo:hi].mean(1),
                 "motor": z[:, hi:].mean(1)}
        nrm = H.norm(dim=-1)
        norms = {"below": nrm[:lo].mean(0), "ws": nrm[lo:hi].mean(0),
                 "motor": nrm[hi:].mean(0)}
        torch.save({"z_bands": bands, "norms": norms, "emotions": emos,
                    "n_tokens": len(toks)}, d / "z.pt")
        n = len(toks)
        jtoks = _tokens(lm.tok, model, rec)
        if len(jtoks) != n:
            jtoks = (jtoks + [""] * n)[:n]
        out = {
            "record": rid, "emotions": emos,
            "valence": [EMOTIONS[e] for e in emos], "n": n,
            "tokens": jtoks,
            "ws": [[round(float(x), 2) for x in row]
                   for row in bands["ws"]],
            "below": [[round(float(x), 1) for x in row]
                      for row in bands["below"]],
            "motor": [[round(float(x), 1) for x in row]
                      for row in bands["motor"]],
            "danger": [],
            "wsnorm": [round(float(x), 1) for x in norms["ws"]],
        }
        (d / "affect.json").write_text(
            json.dumps(out, separators=(",", ":")))
        print(f"  {rid}: affect.json ({n} pos)", flush=True)
    print(f"LANGVAL-VIZ DONE {model}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in BANDS:
        sys.exit(f"usage: langval_viz.py <{'|'.join(BANDS)}>")
    run(sys.argv[1])
