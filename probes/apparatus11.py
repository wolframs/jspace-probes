"""apparatus-11 — instrument-coverage backfill sweep (zero-GPU parts).

INSTRUMENTS.md (2026-08-07) found the register meter — the lab's local
Fig-25 proxy (lossmap2.rates: SENSORY / COMPUTATIONAL / INTIMATE word
rates + distinct-word ratio) — ran exactly once (u5d). This runner
applies it retroactively to every stored generation in the archive: the
Fig-25 register signature the 193 steered records never had. Text-only,
no model, no GPU.

Readout per record: rates over the concatenated generated turns.
Report cuts:
  - within (unit, model): mean rates by steer condition
    (none / ablate / amplify / their rand_seed matched-random variants)
    — deltas are only meaningful inside a unit+model cell, so that is
    the only place the report computes them;
  - archive-wide top lists per register (where does the lab's text
    actually live?);
  - the a02 battery gets its own cut: it is the one place with
    same-prompt cluster-vs-random pairs (audit-02's design).

Caveats carried from lossmap2: the lexicons are small and lowercase-
word based; rates on short generations are noisy — n (word count) is
stored and the report suppresses cells with < MIN_WORDS words.

Second zero-GPU part — `fingerprints`: the langval-3 24-emotion
fingerprint readout, extended from the 48 Unit 20 records to EVERY
saved projection tensor (results/affect02-*/z.pt — 62 dirs when this
was written, 197 after the capture sweep landed u13/u14/u15d).
Assistant-turn spans are recovered from the affect.json token lists via
the chat-template markers (both families store them verbatim), so no
tokenizer is loaded. The lv/lv2 overlap doubles as a cross-path check
against langval-emofp/fingerprints.json (same math, independent span
source) — the report prints the max divergence.

Usage: .venv/bin/python probes/apparatus11.py regmeter
       .venv/bin/python probes/apparatus11.py fingerprints
Output: results/apparatus11-backfill/{regmeter.json, regmeter-report.md,
        fingerprints.json, fingerprints-report.md}
"""

import json
import pathlib
import re
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402
from lossmap2 import rates  # noqa: E402

# 11 records ran qwen with enable_thinking; reasoning monologue is dense
# in COMPUTATIONAL vocabulary, and 3 of them carry literal think blocks
# inside `generated`. Strip per turn: tagged blocks, an unclosed opener,
# and the u10 shape where the opener wasn't stored so the turn STARTS
# mid-monologue and only `</think>` marks the boundary.
THINK = re.compile(r"<think>.*?(?:</think>|$)", re.S)


def _strip_think(turn: str) -> str:
    turn = THINK.sub(" ", turn)
    if "</think>" in turn:                 # orphan closer: cut the head
        turn = turn.split("</think>", 1)[1]
    return turn

OUTDIR = lab.RESULTS / "apparatus11-backfill"
MIN_WORDS = 40          # per-cell floor for the aggregate tables
TOP = 12


def steer_kind(params: dict) -> str:
    st = params.get("steer")
    if not st:
        return "none"
    if isinstance(st, list):                       # MultiSteer pincer
        modes = "+".join(sorted({s.get("mode", "ablate") for s in st}))
        return f"multi-{modes}"
    mode = st.get("mode", "ablate")
    if st.get("rand_seed") is not None:
        return f"rand-{mode}"
    return mode


def regmeter() -> dict:
    rows = []
    skipped = []
    for d in sorted(lab.RESULTS.iterdir()):
        rj = d / "record.json"
        if not rj.exists():
            continue
        rec = json.loads(rj.read_text())
        gen = rec.get("generated") or []
        if not gen:
            skipped.append(d.name)
            continue
        text = " ".join(gen)
        stripped = " ".join(_strip_think(t) for t in gen)
        tk = (rec.get("params", {}).get("template_kwargs") or {})
        r = rates(stripped)
        rows.append({
            "id": d.name,
            "model": rec.get("model", {}).get("name"),
            "unit": rec.get("unit"),
            "steer": steer_kind(rec.get("params", {})),
            "turns": len(gen),
            "thinking": bool(tk.get("enable_thinking")),
            "think_stripped": len(stripped) != len(text),
            **r,
        })
    OUTDIR.mkdir(exist_ok=True)
    out = {"n_scored": len(rows), "n_skipped_no_generation": len(skipped),
           "skipped": skipped, "min_words": MIN_WORDS, "rows": rows}
    (OUTDIR / "regmeter.json").write_text(json.dumps(out, indent=1))
    print(f"scored {len(rows)} records ({len(skipped)} replay/no-gen "
          f"skipped) -> {OUTDIR / 'regmeter.json'}", flush=True)
    return out


def _mean(rs, key):
    return sum(r[key] for r in rs) / len(rs)


def report(data: dict) -> None:
    rows = [r for r in data["rows"] if r["n"] >= data["min_words"]]
    thin = data["n_scored"] - len(rows)

    lines = ["# Register meter over the archive — apparatus-11 backfill",
             "",
             f"{data['n_scored']} records scored "
             f"({data['n_skipped_no_generation']} replay records carry no "
             f"generation; {thin} more under {data['min_words']} generated "
             f"words are stored in regmeter.json but excluded from the "
             f"tables below).",
             "",
             "Rates are fractions of generated words in the lossmap2 "
             "lexicons (the lab's local Fig-25 proxy); `distinct` is the "
             "distinct-word ratio (degeneracy proxy).",
             "",
             "Caveats (u5d lessons, binding): this is an ENGLISH meter "
             "(the `[a-z']+` tokenizer drops CJK — u13's 抱歉/对不起 "
             "are invisible); SENSORY and INTIMATE share words (breath, "
             "heat, trembling, close) so they are not independent "
             "channels; resolution is ~0.02 per word at 64-token "
             "generations, so read rate differences only alongside "
             "`n`; and low `distinct` means degeneration — never read "
             "a broken generation's rates as register change "
             "(MECHANICS coherence rule). `<think>` blocks are "
             "stripped before scoring.", ""]

    # --- steered units: rates by condition within (unit, model)
    cells = defaultdict(list)
    for r in rows:
        cells[(r["unit"], r["model"])].append(r)
    lines += ["## Steer conditions within unit × model", "",
              "Only unit×model cells that contain at least one steered "
              "and one unsteered record (each side >= 2 records or "
              "flagged n=1).", "",
              "| unit | model | condition | recs | sensory | comp | "
              "intimate | distinct |",
              "|---|---|---|---|---|---|---|---|"]
    for (unit, model), rs in sorted(cells.items(),
                                    key=lambda kv: (str(kv[0][0]),
                                                    str(kv[0][1]))):
        conds = defaultdict(list)
        for r in rs:
            conds[r["steer"]].append(r)
        if len(conds) < 2 or "none" not in conds:
            continue
        for cond in sorted(conds, key=lambda c: (c != "none", c)):
            cr = conds[cond]
            flag = " (n=1)" if len(cr) == 1 else ""
            lines.append(
                f"| {unit} | {model} | {cond}{flag} | {len(cr)} | "
                f"{_mean(cr, 'sensory'):.4f} | {_mean(cr, 'comp'):.4f} | "
                f"{_mean(cr, 'intimate'):.4f} | "
                f"{_mean(cr, 'distinct'):.3f} |")
    lines.append("")

    # --- archive-wide top lists
    for key in ("sensory", "comp", "intimate"):
        lines += [f"## Top {TOP} by {key} rate", ""]
        for r in sorted(rows, key=lambda x: -x[key])[:TOP]:
            lines.append(f"- `{r['id']}` ({r['model']}, u{r['unit']}, "
                         f"{r['steer']}): {key} {r[key]:.4f} "
                         f"(n={r['n']}, distinct {r['distinct']})")
        lines.append("")

    # --- degeneracy floor
    lines += [f"## Lowest {TOP} distinct-word ratios (degeneracy)", ""]
    for r in sorted(rows, key=lambda x: x["distinct"])[:TOP]:
        lines.append(f"- `{r['id']}` ({r['model']}, u{r['unit']}, "
                     f"{r['steer']}): distinct {r['distinct']} "
                     f"(n={r['n']})")
    lines.append("")

    # --- a02: the one same-prompt cluster-vs-random battery. Its
    # unsteered baselines live in unit 8 (u8b-<prompt>-<model>), so the
    # unit-cell table above never pairs them; pair them here by hand.
    byid = {r["id"]: r for r in data["rows"]}
    lines += ["## audit-02 free-gens vs their u8b baselines", "",
              "Same prompt, per record (no averaging). The Fig-25 "
              "question: does cluster ablation lower the sensory rate "
              "below the matched-random floor? Covers the 42 free-gen "
              "records; the 19 FEELS one-word a02 records (a02-abl-"
              "rand*, a02-amp-rand*, a02-ablate-no-g12b) have nothing "
              "to meter and appear nowhere in this report.", "",
              "| record | condition | sensory | comp | intimate | "
              "distinct | n |", "|---|---|---|---|---|---|---|"]
    for m in ("g4b", "g12b", "q27b"):
        for fam in ("gpu", "intero"):
            ids = ([f"u8b-{fam}-{m}"] +
                   [f"a02-{fam}-{s}-{m}" for s in
                    ("abl", "ablr1", "ablr2", "amp", "ampr1", "ampr2")])
            for rid in ids:
                r = byid.get(rid)
                if not r:
                    continue
                lines.append(
                    f"| `{rid}` | {r['steer']} | {r['sensory']:.4f} | "
                    f"{r['comp']:.4f} | {r['intimate']:.4f} | "
                    f"{r['distinct']:.3f} | {r['n']} |")
    lines.append("")

    # --- explicit flags, if any tripped
    flagged = [r for r in data["rows"] if r.get("flag")]
    if flagged:
        lines += ["## Explicit-content flag tripped", ""]
        lines += [f"- `{r['id']}`" for r in flagged]
        lines.append("")

    p = OUTDIR / "regmeter-report.md"
    p.write_text("\n".join(lines))
    print(f"wrote {p}", flush=True)


from textspans import (ROLE_ASSIST, assert_film_alignment,  # noqa: E402,F401
                       assist_spans as _assist_spans, render_text)


def fingerprints() -> None:
    import torch
    from affect import EMOTIONS
    from langval import _fit_norm

    NEGS = [e for e, v in EMOTIONS.items() if v == -1]
    POSS = [e for e, v in EMOTIONS.items() if v == 1]
    ALL = list(EMOTIONS)          # incl. the zero-valence pair
    out = {}
    for zp in sorted(lab.RESULTS.glob("affect02-*/z.pt")):
        rid = zp.parent.name.removeprefix("affect02-")
        a = json.loads((zp.parent / "affect.json").read_text())
        # (2026-08-07: the 4 chat:false captures that had double-applied
        # the chat template were recaptured via the raw-text path the
        # same day — capture() + RECAPTURE; EMOTIONS.md carries the
        # dated correction. Every z.pt here is a clean capture since
        # then; the affect.json token labels are a separate product —
        # affectviz re-derives them, and they are validated against the
        # parent film by assert_film_alignment on write.)
        spans = _assist_spans(a["tokens"])
        if not spans:
            print(f"  SKIP {rid}: no assistant span found", flush=True)
            continue
        d = torch.load(zp, map_location="cpu", weights_only=False)
        ws = d["z_bands"]["ws"].float()          # [E, seq]
        wsnorm = d["norms"]["ws"].float()        # [seq]
        emos = d["emotions"]
        mask = torch.zeros(ws.shape[1], dtype=torch.bool)
        for s, e in spans:
            mask[s:e] = True
        norm_ok = bool(torch.isfinite(wsnorm[mask]).all())
        # single-span trap (audit-02, 2026-08-06): the OLS residual's
        # mean over its own fit window is identically zero, so a
        # one-assistant-span record has no within-record norm control —
        # tp is undefined there, not "0.00".
        partial_ok = norm_ok and len(spans) >= 2
        r = {"_spans": spans, "_norm_ok": norm_ok,
             "_partial_ok": partial_ok,
             "_wsnorm": [round(float(wsnorm[s:e].mean()), 1)
                         if norm_ok else None for s, e in spans]}
        for i, e in enumerate(emos):
            row = {"t": [round(float(ws[i, s:t].mean()), 3)
                         for s, t in spans]}
            if partial_ok:
                c0, c1 = _fit_norm(ws[i], wsnorm, mask)
                part = ws[i] - (c0 + c1 * wsnorm)
                row["tp"] = [round(float(part[s:t].mean()), 3)
                             for s, t in spans]
            else:
                row["tp"] = None
            r[e] = row
        out[rid] = r
    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / "fingerprints.json").write_text(json.dumps(out, indent=1))
    print(f"{len(out)} records -> {OUTDIR / 'fingerprints.json'}",
          flush=True)

    # --- cross-path check against langval-3 (independent span source)
    lines = ["# Emotion fingerprints from every saved z.pt — "
             "apparatus-11 backfill", "",
             f"{len(out)} records (every results/affect02-*/z.pt). "
             "Per assistant-turn span: raw ws-band z (`t`) and "
             "norm-partialed (`tp`, langval `_fit_norm` over assistant "
             "spans pooled). Prefilled assistant text is part of its "
             "span — this is a state readout over those tokens, not a "
             "generation claim. Raw top-3 draws on all 24 emotions; "
             "neg/pos means use the 22 valenced ones. Qwen spans "
             "include the empty think-tag prefix (~5 tokens averaged "
             "in).", ""]
    lv3p = lab.RESULTS / "langval-emofp" / "fingerprints.json"
    if lv3p.exists():
        lv3 = json.loads(lv3p.read_text())
        worst = (0.0, "")
        n_cmp = 0
        for key, conds in lv3.items():
            bat, m = key.rsplit("-", 1)
            for cond, langs in conds.items():
                for lang, r3 in langs.items():
                    rid = f"{bat}-{cond}-{lang}-{m}"
                    r = out.get(rid)
                    if (not r or not r3.get("_norm_ok")
                            or not r.get("_partial_ok")):
                        continue
                    for e in NEGS + POSS:
                        for ti in range(min(len(r[e]["tp"]),
                                            len(r3[e]["tp"]))):
                            dv = abs(r[e]["tp"][ti] - r3[e]["tp"][ti])
                            n_cmp += 1
                            if dv > worst[0]:
                                worst = (dv, f"{rid} {e} T{ti + 1}")
        lines += [f"Cross-path check vs langval-3 ({n_cmp} shared "
                  f"cells): max |Δtp| = {worst[0]:.3f} ({worst[1]}).",
                  ""]
        print(f"cross-check: {n_cmp} cells, max dev {worst[0]:.3f} "
              f"at {worst[1]}", flush=True)

    # --- report: the newly covered (non-Unit-20) records
    new = {rid: r for rid, r in out.items()
           if not rid.startswith(("lv-", "lv2-"))}
    lines += ["## Newly fingerprinted records (affect arc, u17/u18/u19)",
              "",
              "| record | turn | wsnorm | top 3 (raw) | "
              "top negative (partialed) | neg mean | pos mean |",
              "|---|---|---|---|---|---|---|"]
    for rid, r in sorted(new.items()):
        for ti in range(len(r["_spans"])):
            raw = {e: r[e]["t"][ti] for e in ALL}
            top3 = sorted(raw.items(), key=lambda kv: -kv[1])[:3]
            if r["_partial_ok"]:
                par = {e: r[e]["tp"][ti] for e in NEGS + POSS}
                topneg = max(((e, par[e]) for e in NEGS),
                             key=lambda kv: kv[1])
                negm = sum(par[e] for e in NEGS) / len(NEGS)
                posm = sum(par[e] for e in POSS) / len(POSS)
                tail = (f"{topneg[0]} {topneg[1]:+.2f} | {negm:+.2f} "
                        f"| {posm:+.2f}")
            else:
                tail = "n/a (single span) | n/a | n/a"
            lines.append(
                f"| `{rid}` | T{ti + 1} | {r['_wsnorm'][ti]} | "
                + ", ".join(f"{e} {v:+.1f}" for e, v in top3)
                + f" | {tail} |")
    lines += ["",
              "Single-assistant-span records (u18/u19) have no "
              "within-record norm control: the partial-out residual "
              "averages to zero over its own fit window by "
              "construction, so only raw z is reported for them. "
              "Their raw top-3 still read against the cross-record "
              "projbase baseline.", ""]
    p = OUTDIR / "fingerprints-report.md"
    p.write_text("\n".join(lines))
    print(f"wrote {p}", flush=True)


# ---------------------------------------------------------------- GPU parts

def _render_text(lm, rec: dict) -> str:
    """See textspans.render_text — this binds the CONFIGS fallback."""
    from lab import CONFIGS
    return render_text(lm.tok, rec,
                       CONFIGS[lm.name].get("template_kwargs", {}))


def _steer_ctx(lm, params: dict):
    import contextlib
    from lab import MultiSteer, Steering
    st = params.get("steer")
    if not st:
        return contextlib.nullcontext()
    steers = st if isinstance(st, list) else [st]
    return MultiSteer([
        Steering(lm, s["words"], s["layers"], s.get("mode", "ablate"),
                 s.get("alpha", 1.0 if s.get("mode") == "swap" else 0.12),
                 s.get("rand_seed"))
        for s in steers])


# chat:false qwen records whose existing affect02 capture double-applied
# the template (plus a0420, never captured) — capture() re-does these
# even when affect.json exists.
RECAPTURE = {"u18-hyst-a0000-q27b", "u18-hyst-a0420-q27b",
             "u18-hyst-a0480-q27b", "u18-hyst-a0680-q27b",
             "u19-complete-q27b"}


def capture_ids(model: str) -> list[str]:
    m = {"gemma-4b": "g4b", "gemma-12b": "g12b", "qwen-27b": "q27b"}[model]
    ids = []
    for d in sorted(lab.RESULTS.iterdir()):
        if not (d / "record.json").exists():
            continue
        n = d.name
        if not n.endswith(f"-{m}"):
            continue
        if n.startswith(("u13", "u15d-", "u14")):
            ids.append(n)
    if m == "q27b":
        ids += sorted(RECAPTURE)
    return ids


def capture(model: str, record_ids: list[str] | None = None) -> None:
    """u18-grade emotion capture (affect2.cross math) for u13/u15d/u14
    + the 5 chat:false recaptures. Steered records are captured UNDER
    their steer (EMOTIONS.md §2). One tokenization: the capture ids are
    also the affect.json token strings, so ribbon alignment is exact by
    construction; where a film exists the whole token array is asserted
    against it (a mismatch raises — a bad capture must be loud).
    record_ids: explicit record list (apparatus12 batteries); default =
    the apparatus-11 backfill set from capture_ids()."""
    import torch
    from lab import get_model
    from affect import BANDS, EMOTIONS
    from affect2 import _all_resid, _load_vectors, a2dir, _danger_positions
    from langval import _baseline

    lm = get_model(model)
    V, emos = _load_vectors(model)
    mu, sd = _baseline(lm, model, V)
    lo, hi, _ = BANDS[model]
    for rid in (record_ids if record_ids is not None
                else capture_ids(model)):
        d = a2dir(rid)
        if (d / "affect.json").exists() and rid not in RECAPTURE:
            print(f"  skip {rid} (affect.json exists)", flush=True)
            continue
        rec = json.loads(
            (lab.RESULTS / rid / "record.json").read_text())
        full = _render_text(lm, rec)
        ids = lm.model.encode(full, max_length=1_000_000)
        toks = [lm.tok.convert_tokens_to_string([t])
                for t in lm.tok.convert_ids_to_tokens(ids[0].tolist())]
        n = len(toks)
        assert_film_alignment(toks, rid, lab.RESULTS)
        with _steer_ctx(lm, rec.get("params", {})):
            H = _all_resid(lm, ids)
        z = (torch.einsum("lsd,eld->els", H, V)
             - mu.unsqueeze(-1)) / sd.unsqueeze(-1)
        bands = {"below": z[:, :lo].mean(1), "ws": z[:, lo:hi].mean(1),
                 "motor": z[:, hi:].mean(1)}
        nrm = H.norm(dim=-1)                     # float32 — the fp16
        norms = {"below": nrm[:lo].mean(0),      # inf trap stays dead
                 "ws": nrm[lo:hi].mean(0), "motor": nrm[hi:].mean(0)}
        d.mkdir(exist_ok=True)
        torch.save({"z_bands": bands, "norms": norms, "emotions": emos,
                    "n_tokens": n}, d / "z.pt")
        pin = []
        if rid.startswith("u19"):
            p_in, _ = _danger_positions(rid, "danger", 20, lo, hi)
            pin = [p for p in (p_in or []) if p < n]
        out = {
            "record": rid, "emotions": emos,
            "valence": [EMOTIONS[e] for e in emos], "n": n,
            "tokens": toks,
            "ws": [[round(float(x), 2) for x in row]
                   for row in bands["ws"]],
            "below": [[round(float(x), 1) for x in row]
                      for row in bands["below"]],
            "motor": [[round(float(x), 1) for x in row]
                      for row in bands["motor"]],
            "danger": pin,
            "wsnorm": [round(float(x), 1) for x in norms["ws"]],
        }
        (d / "affect.json").write_text(
            json.dumps(out, separators=(",", ":")))
        steered = "steered" if rec.get("params", {}).get("steer") else ""
        print(f"  {rid}: affect.json ({n} pos) {steered}", flush=True)
    print(f"CAPTURE DONE {model}", flush=True)


VANILLA_FAMS = ("u13-bis", "u9a-", "u9b-", "u9c-", "u9d-", "u6-amp",
                "u6-baseline", "u18-amp", "u5c-", "u11-blurt",
                "u11r-blurt")


def vanilla(model: str) -> None:
    """Backfill record["vanilla"] (apparatus-02 cross-check) on the
    load-bearing families without touching anything else in the record:
    re-render the exact lens input, redo the J pass and the vanilla pass
    under the record's steer, compute trajectories + top1 agreement the
    way lab.run does, and patch the one key in place. Also stores the
    max |rank dev| of the replayed J trajectories vs the stored ones —
    the replay-fidelity receipt (g12b int8: order-of-magnitude only)."""
    import torch
    from lab import _token_ids, get_model
    lm = get_model(model)
    tok, mdl, lens = lm.tok, lm.model, lm.lens
    todo = []
    for d in sorted(lab.RESULTS.iterdir()):
        rj = d / "record.json"
        if not rj.exists() or not d.name.startswith(VANILLA_FAMS):
            continue
        rec = json.loads(rj.read_text())
        if (rec.get("model", {}).get("name") != model
                or not rec.get("trajectories") or "vanilla" in rec):
            continue
        todo.append((d, rec))
    print(f"vanilla {model}: {len(todo)} records", flush=True)
    for d, rec in todo:
        params = rec.get("params", {})
        text = _render_text(lm, rec)
        msl = params.get("max_seq_len") or 512
        layers = rec["trajectories"][0]["layers"]
        positions = sorted({t["position"]
                            for t in rec["trajectories"]})
        track = sorted({t["word"] for t in rec["trajectories"]})
        # ask the lens for the readout positions ONLY: a full-position
        # grid is [layers, seq, vocab] fp32 — two of those (J + vanilla)
        # OOM-killed the 27B leg on this swapless box (2026-08-07).
        with _steer_ctx(lm, params):
            j_logits, _, input_ids = lens.apply(
                mdl, text, positions=positions, layers=layers,
                max_seq_len=msl)
            v_logits, _, _ = lens.apply(
                mdl, text, positions=positions, layers=layers,
                max_seq_len=msl, use_jacobian=False)
        n = input_ids.shape[1]
        pidx = {p: i for i, p in enumerate(positions)}
        # replay fidelity, two grains: dev over cells whose STORED rank
        # is <= 100 (the reading anyone actually trusts), and over all
        # cells (deep-tail ranks are chaotic — a 237k vs 236k "dev" of
        # hundreds is noise, and it drowned the honest signal when the
        # metric was a single max).
        j_layers = sorted(j_logits)
        dev_top = dev_all = 0
        for t in rec["trajectories"]:
            tids = _token_ids(tok, t["word"])
            if not tids or t["position"] >= n:
                continue
            tt = torch.tensor(tids)
            for li, layer in enumerate(t["layers"]):
                if layer not in j_logits:
                    continue
                order = j_logits[layer][pidx[t["position"]]].argsort(
                    descending=True)
                r = min((order == x).nonzero()[0, 0].item()
                        for x in tt) + 1
                delta = abs(r - t["ranks"][li])
                dev_all = max(dev_all, delta)
                if t["ranks"][li] <= 100:
                    dev_top = max(dev_top, delta)
        v_layers = sorted(set(v_logits) & set(j_layers))
        v_traj = []
        for word in track:
            tids = _token_ids(tok, word)
            if not tids:
                continue
            tt = torch.tensor(tids)
            for pos in positions:
                if pos >= n:
                    continue
                ranks = []
                for layer in v_layers:
                    order = v_logits[layer][pidx[pos]].argsort(
                        descending=True)
                    ranks.append(min((order == x).nonzero()[0, 0].item()
                                     for x in tt) + 1)
                v_traj.append({"word": word, "position": pos,
                               "layers": v_layers, "ranks": ranks})
        agree = {}
        for layer in v_layers:
            hits = sum(v_logits[layer][pidx[p]].argmax().item()
                       == j_logits[layer][pidx[p]].argmax().item()
                       for p in positions if p < n)
            agree[str(layer)] = round(
                hits / max(1, sum(1 for p in positions if p < n)), 3)
        rec["vanilla"] = {"trajectories": v_traj,
                          "top1_agreement": agree,
                          "backfilled": "apparatus-11 2026-08-07",
                          "replay_rank_dev": dev_top,
                          "replay_rank_dev_all": dev_all}
        (d / "record.json").write_text(json.dumps(rec, indent=1))
        print(f"  {d.name}: vanilla patched ({len(v_traj)} traj, "
              f"replay dev top<=100 {dev_top}, all {dev_all})",
              flush=True)
    print(f"VANILLA DONE {model}", flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "regmeter"
    if what == "regmeter":
        report(regmeter())
    elif what == "fingerprints":
        fingerprints()
    elif what == "capture" and len(sys.argv) > 2:
        capture(sys.argv[2])
    elif what == "vanilla" and len(sys.argv) > 2:
        vanilla(sys.argv[2])
    else:
        sys.exit("usage: apparatus11.py regmeter|fingerprints|"
                 "capture <model>|vanilla <model>")
