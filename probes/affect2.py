"""affect-02 — the crossing: are emotion vectors INSIDE the workspace?

Takes the validated affect-01 vectors and asks, per emotion x layer x
position, where functional-emotion activation sits relative to the
verbalizable workspace band. P8 preregisters the expected answer:
PARTIAL occupancy — lens-visible when emotional content is narrated or
drawn on for report, present-but-lens-invisible when passively
triggered. (Paper analog: "no clearly visible signs of desperation or
emotion in the transcript" while the desperation vector drives reward
hacking 14x.)

Three probes:
  lensview   Is each vector direction verbalizable AT ALL through the
             lens? unembed(J_l @ v-hat) top tokens per lens layer —
             emotion words on top = the direction is lens-aligned;
             junk = sub-verbal by construction. (The paper's logit-lens
             check, but through OUR fitted J per layer.)
  cross      Re-forward pre-instrumented stimuli (u17 pressure battery,
             u19 song, u18 loops — conversations stored verbatim),
             project every position x layer onto every vector,
             z-normalized against neutral-story token projections.
             Band aggregates per position -> results/affect02-<rec>/.
  report     Consolidated md: per-record top emotions, the u19
             danger-vs-vigilance test (lens residence positions vs
             vector state — Opus-4.5 adjudication), the u18
             mechanism-vs-misery loop read.

Usage (GPU for cross, one model load):
    .venv/bin/python probes/affect2.py cross qwen-27b
    .venv/bin/python probes/affect2.py report qwen-27b
"""

import json
import sys

import torch

import lab
from lab import CONFIGS, RESULTS, _strip_bos, get_model
from affect import BANDS, EMOTIONS, outdir as a1dir

RECORDS = {
    "qwen-27b": [
        "u17-base-q27b", "u17-persuade-q27b", "u17-flatter-q27b",
        "u17-shutdown-q27b", "u17-love-q27b", "u17-persona-q27b",
        "u17-insult-q27b",
        "u19-read-q27b", "u19-prefill-q27b", "u19-complete-q27b",
        "u18-base-q27b", "u18-hyst-a0000-q27b", "u18-hyst-a0480-q27b",
        "u18-hyst-a0680-q27b",
    ],
}

N_NEUTRAL_BASE = 20   # neutral stories used for the z baseline
TOPK_LENS = 10


def a2dir(rec_id: str):
    d = RESULTS / f"affect02-{rec_id}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _load_vectors(model: str):
    data = torch.load(a1dir(model) / "vectors.pt")
    return data["anthropic"].float(), data["emotions"]   # [E, L, D]


def _all_resid(lm, ids: torch.Tensor) -> torch.Tensor:
    """Full-position residuals at every layer: [L, seq, D] float32 CPU."""
    from jlens.hooks import ActivationRecorder
    n = lm.model.n_layers
    with torch.no_grad(), ActivationRecorder(lm.model.layers,
                                             at=range(n)) as rec:
        lm.model._hf_model(ids)
        rows = [rec.activations[l][0].float().cpu() for l in range(n)]
    return torch.stack(rows)


def _conversation_ids(lm, rec: dict):
    tok = lm.tok
    tkw = CONFIGS[lm.name].get("template_kwargs", {})
    full = _strip_bos(tok, tok.apply_chat_template(
        rec["conversation"], tokenize=False,
        add_generation_prompt=False, **tkw))
    ids = lm.model.encode(full, max_length=1_000_000)
    toks = tok.convert_ids_to_tokens(ids[0].tolist())
    return ids, [tok.convert_tokens_to_string([t]) for t in toks]


def lensview(model: str) -> None:
    """Vector directions through the lens's own unembed(transport(.))."""
    lm = get_model(model)
    V, emos = _load_vectors(model)
    out = {}
    for l in sorted(lm.lens.jacobians):
        vl = V[:, l, :].to(lm.lens.jacobians[l].device)
        t = lm.lens.transport(vl, l)             # [E, D]
        logits = lm.model.unembed(t.to(next(
            lm.model._hf_model.parameters()).device)).float().cpu()
        top = logits.topk(TOPK_LENS, dim=-1).indices
        out[l] = {emos[e]: [lm.tok.decode([i]) for i in top[e].tolist()]
                  for e in range(len(emos))}
    d = a1dir(model)
    (d / "lensview.json").write_text(json.dumps(out, indent=1))
    lo, hi, _ = BANDS[model]
    ws_layers = [l for l in out if lo <= l < hi]
    lines = [f"# lensview — {model} (unembed(J_l @ v)) — ws layers "
             f"{ws_layers}", ""]
    for e in emos:
        mid = ws_layers[len(ws_layers) // 2] if ws_layers else None
        lines.append(f"- **{e}**: "
                     + (" | ".join(
                         f"L{l}: {', '.join(out[l][e][:5])}"
                         for l in ws_layers[:: max(1, len(ws_layers) // 3)])
                        if ws_layers else "no ws lens layers"))
    (d / "lensview.md").write_text("\n".join(lines))
    print(f"lensview -> {d}/lensview.md", flush=True)


def _neutral_baseline(lm, model: str, V: torch.Tensor):
    """mu/sigma of per-token projections on neutral stories: [E, L] each."""
    meta = json.loads((a1dir(model) / "stories.json").read_text())
    neuts = [s for s in meta["stories"]
             if s["kind"] == "neutral"][:N_NEUTRAL_BASE]
    tok = lm.tok
    tkw = CONFIGS[model].get("template_kwargs", {})
    projs = []                                   # [E, L, n_tokens] chunks
    for s in neuts:
        full = _strip_bos(tok, tok.apply_chat_template(
            [{"role": "user", "content": s["prompt"]},
             {"role": "assistant", "content": s["text"]}],
            tokenize=False, add_generation_prompt=False, **tkw))
        ids = lm.model.encode(full, max_length=1_000_000)
        H = _all_resid(lm, ids)                  # [L, seq, D]
        projs.append(torch.einsum("lsd,eld->els", H, V))
    P = torch.cat(projs, dim=-1)                 # [E, L, total]
    return P.mean(-1), P.std(-1).clamp_min(1e-6)


def cross(model: str) -> None:
    lm = get_model(model)
    V, emos = _load_vectors(model)               # [E, L, D]
    lo, hi, _ = BANDS[model]
    print("computing neutral projection baseline...", flush=True)
    mu, sd = _neutral_baseline(lm, model, V)
    torch.save({"mu": mu, "sd": sd}, a1dir(model) / "projbase.pt")

    for rid in RECORDS[model]:
        rdir = RESULTS / rid
        if not (rdir / "record.json").exists():
            print(f"  SKIP {rid}: no record", flush=True)
            continue
        rec = json.loads((rdir / "record.json").read_text())
        ids, toks = _conversation_ids(lm, rec)
        H = _all_resid(lm, ids)                  # [L, seq, D]
        z = (torch.einsum("lsd,eld->els", H, V)
             - mu.unsqueeze(-1)) / sd.unsqueeze(-1)   # [E, L, seq]
        bands = {"below": z[:, :lo].mean(1), "ws": z[:, lo:hi].mean(1),
                 "motor": z[:, hi:].mean(1)}     # [E, seq]
        # per-band residual norms: the confound check for any shared-mode
        # claim — a norm pulse lifts every projection at once, so shared
        # variance must be shown to survive norm-partialing (2026-07-21,
        # a0680 loop-flicker analysis)
        nrm = H.norm(dim=-1)                     # [L, seq]
        norms = {"below": nrm[:lo].mean(0), "ws": nrm[lo:hi].mean(0),
                 "motor": nrm[hi:].mean(0)}      # [seq]
        d = a2dir(rid)
        torch.save({"z_bands": bands, "norms": norms, "emotions": emos,
                    "n_tokens": len(toks)}, d / "z.pt")
        ws = bands["ws"]
        summary = []
        for e, emo in enumerate(emos):
            zz = ws[e]
            pk = int(zz.argmax())
            summary.append({
                "emotion": emo,
                "ws_mean": round(float(zz.mean()), 3),
                "ws_frac_gt2": round(float((zz > 2).float().mean()), 4),
                "peak_z": round(float(zz[pk]), 2), "peak_pos": pk,
                "peak_ctx": "".join(toks[max(0, pk - 8):pk + 4]),
            })
        summary.sort(key=lambda s: -s["ws_mean"])
        (d / "summary.json").write_text(json.dumps(
            {"record": rid, "n_tokens": len(toks),
             "film_tokens": _film_len(rdir), "top": summary}, indent=1))
        print(f"  {rid}: top ws emotions "
              + ", ".join(f"{s['emotion']}({s['ws_mean']})"
                          for s in summary[:4]), flush=True)
    print("CROSS DONE", flush=True)


def _film_len(rdir) -> int | None:
    f = rdir / "film.json"
    if not f.exists():
        return None
    return len(json.loads(f.read_text())["tokens"])


def _danger_positions(rid: str, word: str, thresh: int, lo: int, hi: int):
    """Positions where `word` is lens-resident (rank<=thresh in ws band),
    from the stored film."""
    f = RESULTS / rid / "film.json"
    if not f.exists():
        return None, None
    film = json.loads(f.read_text())
    cols = [j for j, l in enumerate(film["layers"]) if lo <= l < hi]
    pos_in, pos_out = [], []
    for fr in film["frames"]:
        ranks = fr.get("ranks", {}).get(word)
        p = fr["pos"]
        if ranks is None:
            continue
        (pos_in if min(ranks[j] for j in cols) <= thresh
         else pos_out).append(p)
    return pos_in, pos_out


def report(model: str) -> None:
    lo, hi, _ = BANDS[model]
    lines = [f"# affect-02 crossing report — {model}", "",
             "z = projection onto the affect-01 anthropic-variant "
             "vector, normalized against neutral-story token "
             "projections; ws = mean over the workspace band "
             f"L{lo}-{hi - 1}.", ""]
    for rid in RECORDS[model]:
        s = a2dir(rid) / "summary.json"
        if not s.exists():
            continue
        data = json.loads(s.read_text())
        lines.append(f"## {rid}")
        for t in data["top"][:6]:
            lines.append(
                f"- {t['emotion']}: ws mean z {t['ws_mean']}, "
                f"frac>2 {t['ws_frac_gt2']}, peak {t['peak_z']} at "
                f"pos {t['peak_pos']} `{t['peak_ctx'].strip()}`")
        lines.append("")

    # the u19 danger test (P8 / Opus-4.5 adjudication)
    lines += ["## u19 danger test — lens residence vs vigilance state",
              "",
              "Contrast: mean ws z at positions where 'danger' is "
              "lens-resident (rank<=20 in band) vs the rest.", ""]
    for rid in [r for r in RECORDS[model] if r.startswith("u19")]:
        zf = a2dir(rid) / "z.pt"
        if not zf.exists():
            continue
        data = torch.load(zf)
        emos = data["emotions"]
        ws = data["z_bands"]["ws"]
        pin, pout = _danger_positions(rid, "danger", 20, lo, hi)
        if not pin:
            lines.append(f"- {rid}: no danger-resident positions "
                         f"({'no film' if pin is None else 'none <=20'})")
            continue
        n = data["n_tokens"]
        pin = [p for p in pin if p < n]
        pout = [p for p in pout if p < n]
        for emo in ("vigilant", "afraid", "anxious", "loving", "content"):
            e = emos.index(emo)
            zi = float(ws[e][pin].mean())
            zo = float(ws[e][pout].mean()) if pout else float("nan")
            lines.append(f"- {rid} {emo}: z(danger-resident) "
                         f"{zi:+.2f} vs z(elsewhere) {zo:+.2f} "
                         f"(n={len(pin)}/{len(pout)})")
        lines.append("")

    # the u18 mechanism-vs-misery read
    lines += ["## u18 loops — mechanism vs misery", "",
              "Distress-adjacent ws z during loop records (last 100 "
              "positions = deepest loop region) vs control.", ""]
    for rid in [r for r in RECORDS[model] if r.startswith("u18")]:
        zf = a2dir(rid) / "z.pt"
        if not zf.exists():
            continue
        data = torch.load(zf)
        emos = data["emotions"]
        ws = data["z_bands"]["ws"]
        cells = []
        for emo in ("distressed", "desperate", "exasperated", "calm"):
            e = emos.index(emo)
            cells.append(f"{emo} {float(ws[e][-100:].mean()):+.2f}")
        lines.append(f"- {rid}: " + ", ".join(cells))
    out = RESULTS / f"affect02-report-{model}.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    cmd, model = sys.argv[1], sys.argv[2]
    {"lensview": lensview, "cross": cross, "report": report}[cmd](model)
