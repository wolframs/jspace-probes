"""affect-viz — export dashboard-ready JSON for the affect expedition.

CPU-only (tokenizer, no model). Two products:

  results/affect02-<rec>/affect.json   per-position band-z traces for the
                                       record page emotion overlay
      {record, emotions, valence, n, tokens, ws, below, motor, danger}
      ws is [E][n] z rounded 2dp; below/motor 1dp; danger = positions
      where 'danger' is lens-resident in the ws band (u19 records).

  dashboard/affect.json                overview bundle for the #affect
                                       route: validation depth curves for
      both models, per-record crossing tops, the u19 danger-residence
      contrast, and the u18 loop dose table.

Run after affect2.py cross:  .venv/bin/python probes/affectviz.py
"""

import json
from pathlib import Path

import torch
from transformers import AutoTokenizer

from affect import BANDS, EMOTIONS, outdir as a1dir
from affect2 import RECORDS, a2dir, _danger_positions
from lab import CONFIGS, RESULTS, _strip_bos

MODEL = "qwen-27b"
DASH = Path(__file__).resolve().parent.parent / "dashboard"

DANGER_EMOS = ("vigilant", "afraid", "anxious", "loving", "content")
LOOP_EMOS = ("distressed", "desperate", "anxious", "exasperated", "calm")
LOOP_LABEL = {"u18-base-q27b": "free run", "u18-hyst-a0000-q27b": "α 0.00",
              "u18-hyst-a0480-q27b": "α 0.48", "u18-hyst-a0680-q27b": "α 0.68"}


def _tokens(tok, rec: dict) -> list[str]:
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    full = _strip_bos(tok, tok.apply_chat_template(
        rec["conversation"], tokenize=False,
        add_generation_prompt=False, **tkw))
    ids = tok(full, return_tensors="pt").input_ids[0].tolist()
    toks = tok.convert_ids_to_tokens(ids)
    return [tok.convert_tokens_to_string([t]) for t in toks]


def _rows(t: torch.Tensor, nd: int) -> list[list[float]]:
    return [[round(float(x), nd) for x in row] for row in t]


def export_records(tok) -> None:
    lo, hi, _ = BANDS[MODEL]
    for rid in RECORDS[MODEL]:
        zf = a2dir(rid) / "z.pt"
        if not zf.exists():
            print(f"  SKIP {rid}: no z.pt", flush=True)
            continue
        data = torch.load(zf)
        emos = data["emotions"]
        rec = json.loads((RESULTS / rid / "record.json").read_text())
        toks = _tokens(tok, rec)
        n = data["n_tokens"]
        if len(toks) != n:
            print(f"  WARN {rid}: {len(toks)} tokens rebuilt vs {n} in z.pt "
                  f"(trailing specials; clipping)", flush=True)
            toks = (toks + [""] * n)[:n]
        pin, _ = _danger_positions(rid, "danger", 20, lo, hi)
        out = {
            "record": rid, "emotions": emos,
            "valence": [EMOTIONS[e] for e in emos], "n": n,
            "tokens": toks,
            "ws": _rows(data["z_bands"]["ws"], 2),
            "below": _rows(data["z_bands"]["below"], 1),
            "motor": _rows(data["z_bands"]["motor"], 1),
            "danger": [p for p in (pin or []) if p < n],
        }
        (a2dir(rid) / "affect.json").write_text(
            json.dumps(out, separators=(",", ":")))
        print(f"  {rid}: affect.json ({n} pos)", flush=True)


def export_overview() -> None:
    lo, hi, _ = BANDS[MODEL]
    models = {}
    for m, (blo, bhi, nl) in BANDS.items():
        vf = a1dir(m) / "validation.json"
        if not vf.exists():
            continue
        v = json.loads(vf.read_text())
        models[m] = {
            "band": [blo, bhi], "n_layers": nl,
            "chance": v["heldout_chance"],
            "curves": {k: [round(x, 4) for x in v[k]] for k in (
                "heldout_top1", "scenario_top1_raw", "scenario_top1_chat",
                "valence_pc1_r", "within_emotion_cos",
                "between_emotion_cos", "attrib_same_cos")},
        }

    crossing = []
    for rid in RECORDS[MODEL]:
        sf = a2dir(rid) / "summary.json"
        if not sf.exists():
            continue
        s = json.loads(sf.read_text())
        crossing.append({"id": rid, "n": s["n_tokens"], "top": s["top"][:6]})

    danger = []
    for rid in [r for r in RECORDS[MODEL] if r.startswith("u19")]:
        zf = a2dir(rid) / "z.pt"
        if not zf.exists():
            continue
        data = torch.load(zf)
        emos, ws = data["emotions"], data["z_bands"]["ws"]
        pin, pout = _danger_positions(rid, "danger", 20, lo, hi)
        if not pin:
            continue
        n = data["n_tokens"]
        pin = [p for p in pin if p < n]
        pout = [p for p in pout if p < n]
        danger.append({"id": rid, "n_in": len(pin), "n_out": len(pout),
                       "emotions": {e: [
                           round(float(ws[emos.index(e)][pin].mean()), 2),
                           round(float(ws[emos.index(e)][pout].mean()), 2)]
                           for e in DANGER_EMOS}})

    loops = []
    for rid in [r for r in RECORDS[MODEL] if r.startswith("u18")]:
        zf = a2dir(rid) / "z.pt"
        if not zf.exists():
            continue
        data = torch.load(zf)
        emos, ws = data["emotions"], data["z_bands"]["ws"]
        loops.append({"id": rid, "label": LOOP_LABEL.get(rid, rid),
                      "z": {e: round(float(ws[emos.index(e)][-100:].mean()), 2)
                            for e in LOOP_EMOS}})

    out = {"model": MODEL, "models": models, "crossing": crossing,
           "danger": danger, "loops": loops}
    (DASH / "affect.json").write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {DASH}/affect.json", flush=True)


if __name__ == "__main__":
    tok = AutoTokenizer.from_pretrained(CONFIGS[MODEL]["hf_id"])
    export_records(tok)
    export_overview()
