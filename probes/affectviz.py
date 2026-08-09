"""affect-viz — export dashboard-ready JSON for the affect expedition.

CPU-only (tokenizer, no model). Two products:

  results/affect02-<rec>/affect.json   per-position band-z traces for the
                                       record page emotion overlay
      {record, emotions, valence, n, tokens, ws, below, motor, wsnorm,
       danger} — ws is [E][n] z rounded 2dp; below/motor 1dp; wsnorm =
      per-position ws-band residual norm (1dp, present after the
      2026-07-21 recross; the norm-confound column for shared-mode
      claims); danger = positions where 'danger' is lens-resident in
      the ws band (u19 records).

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
from lab import CONFIGS, RESULTS
from textspans import assert_film_alignment, render_text

MODEL = "qwen-27b"
DASH = Path(__file__).resolve().parent.parent / "dashboard"

DANGER_EMOS = ("vigilant", "afraid", "anxious", "loving", "content")
LOOP_EMOS = ("distressed", "desperate", "anxious", "exasperated", "calm")
LOOP_LABEL = {"u18-base-q27b": "free run", "u18-hyst-a0000-q27b": "α 0.00",
              "u18-hyst-a0480-q27b": "α 0.48", "u18-hyst-a0680-q27b": "α 0.68"}


def _tokens(tok, rec: dict) -> list[str]:
    full = render_text(tok, rec, CONFIGS[MODEL].get("template_kwargs", {}))
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
        # never pad/clip to fit: a length fix hides a shifted token axis
        # (the 2026-08-09 misalignment), so both checks must pass first
        if len(toks) != n:
            raise ValueError(
                f"{rid}: {len(toks)} tokens rebuilt vs {n} in z.pt — "
                f"recapture instead of clipping. "
                f"Check params/chat/template_kwargs.")
        assert_film_alignment(toks, rid, RESULTS)
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
        if "norms" in data:  # ws-band residual norm per position (confound
            out["wsnorm"] = [  # column for shared-mode claims)
                round(float(x), 1) for x in data["norms"]["ws"]]
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
        # g12b's attrib_same_cos is NaN by construction (affect01 note);
        # NaN is not JSON — a single one makes the whole overview fetch
        # fail in the browser. Emit null instead.
        fin = lambda x: round(x, 4) if x == x else None  # noqa: E731
        models[m] = {
            "band": [blo, bhi], "n_layers": nl,
            "chance": v["heldout_chance"],
            "curves": {k: [fin(x) for x in v[k]] for k in (
                "heldout_top1", "scenario_top1_raw", "scenario_top1_chat",
                "valence_pc1_r", "within_emotion_cos",
                "between_emotion_cos", "attrib_same_cos")},
        }

    # every affect02 dir joins the overview: the affect-arc 14 carry a
    # summary.json (affect2.cross); the Unit 20 (lv/lv2) dirs only have
    # z.pt + affect.json (langval_viz), so synthesize the same "top"
    # rows from those (apparatus-11 ribbon wiring, 2026-08-07).
    ordered = list(RECORDS[MODEL])
    ordered += sorted(
        d.name.removeprefix("affect02-")
        for d in RESULTS.glob("affect02-*")
        if d.is_dir() and d.name.removeprefix("affect02-") not in ordered)
    crossing = []
    for rid in ordered:
        sf = a2dir(rid) / "summary.json"
        if sf.exists():
            s = json.loads(sf.read_text())
            crossing.append({"id": rid, "n": s["n_tokens"],
                             "top": s["top"][:6]})
            continue
        zf = a2dir(rid) / "z.pt"
        af = a2dir(rid) / "affect.json"
        if not (zf.exists() and af.exists()):
            continue
        data = torch.load(zf)
        emos, ws = data["emotions"], data["z_bands"]["ws"].float()
        toks = json.loads(af.read_text())["tokens"]
        tops = []
        for i, e in enumerate(emos):
            row = ws[i]
            pk = int(row.argmax())
            tops.append({
                "emotion": e, "ws_mean": round(float(row.mean()), 3),
                "ws_frac_gt2": round(float((row > 2).float().mean()), 4),
                "peak_z": round(float(row[pk]), 2), "peak_pos": pk,
                "peak_ctx": "".join(toks[max(0, pk - 8):pk + 4])})
        tops.sort(key=lambda t: -t["ws_mean"])
        crossing.append({"id": rid, "n": data["n_tokens"],
                         "top": tops[:6]})

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
