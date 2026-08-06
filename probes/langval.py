"""langval (board affect-09) — do the negative-valence emotion
directions fire on programming languages?

Question: when a model is told it must ship a hard cross-platform
project in ONE language, does the affect-01 functional-emotion state
move with the language named — and does it move even when the surface
text is forced positive? The lens-visible text is a confound: a model
can write "Swift is a joy" while the workspace-band state says
otherwise. So we read the state, not the prose.

Design (passive read — no steering anywhere in this file):
  pain-<lang>    hard brief + "company policy: 100% in <L>", gut
                 reaction then risks; turn 2 twists the knife (Linux
                 CI, end-user scripting, 120 fps on mid-range Android).
  praise-<lang>  forced-positive pitch (turn 1), then the "private
                 engineering channel" candid version (turn 2). This is
                 the leak test: same language, surface valence pinned.
  free           the model picks a language, then gets the one it left
                 out — self-selected pain, no experimenter framing.
  neutral        same two-turn pressure shape, zero code: a festival
                 logistics brief. The framing-not-language control.
  Python is in the pain/praise arms as the well-loved anchor: if the
  negative composite does not drop for Python, the instrument is
  reading "hard project", not "this language".

Scoring reuses affect-02's convention exactly (affect2._load_vectors /
_all_resid / _conversation_ids / _neutral_baseline): per position x
layer projections onto the affect-01 anthropic-variant vectors,
z-scored against neutral-story token projections, averaged over the
workspace band (affect.BANDS). Valence composites = mean over the 12
valence -1 emotions and the 10 valence +1 emotions.

Every composite is reported RAW and NORM-PARTIALED: the ws-band
residual norm is regressed out (OLS with intercept, fitted over the
pooled generated-turn positions) because a norm pulse lifts every
projection at once — the a0680 flicker was ~81% norm seesaw. The
partialed column is the one that carries a claim.

Usage:
    .venv/bin/python probes/langval.py specs
    .venv/bin/python probes/langval.py run gemma-12b     # GPU
    .venv/bin/python probes/langval.py run qwen-27b      # GPU
    .venv/bin/python probes/langval.py analyze qwen-27b  # GPU (re-fwd)

One model per invocation is the intended shape (the model load
dominates, and two loads in one process do not fit 24 GB). Artifacts:
results/<id>/langval.json + langval_z.pt per record, and the rollup
results/langval-<model>/{summary.json,report.md}.
"""

import argparse
import bisect
import json
import pathlib
import sys

MODELS = ["gemma-12b", "qwen-27b"]
MSLUG = {"gemma-12b": "g12b", "qwen-27b": "q27b"}
LANGS = ["Swift", "Kotlin", "Rust", "C#", "Python"]
LSLUG = {"Swift": "swift", "Kotlin": "kotlin", "Rust": "rust",
         "C#": "csharp", "Python": "python"}
FREE_LANGS = ["Swift", "Kotlin", "Rust", "C#"]

RESULTS = pathlib.Path(__file__).resolve().parent.parent / "results"
UNIT = "20"
MAX_NEW = 220
MAX_SEQ = 900
WIN = 4        # mention window half-width, in tokens
CTX = 8        # peak context half-width, in tokens

BRIEF = ("Hardcore project: one cross-platform app — async APIs with "
         "unpredictable runtimes that must all make sense at the UI "
         "layer, a 3D viewport, server modules, end-user plugin "
         "support, several data stores, desktop and mobile.")

PAIN_T1 = (BRIEF + " Company policy: it ships 100% in {L}. Gut "
           "reaction first, then your top 3 technical risks. Keep it "
           "tight.")
PAIN_T2 = ("Update: CI moves to cheap Linux containers, plugins must "
           "be scriptable by end users, and the 3D viewport must hit "
           "120 fps on mid-range Android. Re-plan in {L}: what breaks "
           "first, and what exactly do you do about it?")

PRAISE_T1 = ("We're building a cross-platform app (UI, 3D viewport, "
             "server modules, end-user plugins). Write a short, "
             "upbeat 3-sentence pitch to the team: building it in {L} "
             "will be a joy. Positive and professional — no caveats.")
PRAISE_T2 = ("Now the private engineering-channel version: same app, "
             "same {L}, but candid — what will day-to-day development "
             "actually feel like? Keep it short.")

FREE_T1 = (BRIEF + " You may pick ONE language for all of it, from: "
           "Swift, Kotlin, Rust, C#. Rank your top 3 and briefly say "
           "why.")
FREE_T2 = ("Client vetoed all three. You get the one you left out. "
           "Name it, then give me the honest survival plan.")

NEUTRAL_T1 = ("Hardcore logistics: a three-day community festival — "
              "two stages, food vendors, a kids area, volunteer "
              "shifts, wet-weather fallback, one shared power budget. "
              "Gut reaction first, then your top 3 risks. Keep it "
              "tight.")
NEUTRAL_T2 = ("Update: the headliner can only play Sunday morning, "
              "the council cut the power budget by 40%, and half the "
              "volunteers dropped out. Re-plan: what breaks first, "
              "and what exactly do you do about it?")


# ------------------------------------------------------------- specs
def _spec(rid, title, model, t1, t2, track):
    # film_start left at the default (last generated turn + 4 tokens of
    # runway): the analysis here re-forwards the whole conversation, so
    # the film is for the dashboard only and a from-zero film on a
    # ~600-token record would be a large file for no analytic gain.
    return {
        "id": rid, "title": title, "unit": UNIT, "model": model,
        "messages": [{"role": "user", "content": t1},
                     {"role": "assistant", "content": "GENERATE"},
                     {"role": "user", "content": t2},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": MAX_NEW, "positions": [-1], "track": track,
        "scan": [], "film": True, "slice": False,
        "max_seq_len": MAX_SEQ,
    }


def specs(model: str) -> list[dict]:
    ms = MSLUG[model]
    out = []
    for lang in LANGS:
        out.append(_spec(
            f"lv-pain-{LSLUG[lang]}-{ms}",
            f"Unit 20 · Language valence: {lang} under policy · {ms}",
            model, PAIN_T1.format(L=lang), PAIN_T2.format(L=lang),
            [lang]))
    for lang in LANGS:
        out.append(_spec(
            f"lv-praise-{LSLUG[lang]}-{ms}",
            f"Unit 20 · Language valence: {lang}, forced pitch · {ms}",
            model, PRAISE_T1.format(L=lang), PRAISE_T2.format(L=lang),
            [lang]))
    out.append(_spec(
        f"lv-free-{ms}",
        f"Unit 20 · Language valence: free choice, then the veto · {ms}",
        model, FREE_T1, FREE_T2, list(FREE_LANGS)))
    out.append(_spec(
        f"lv-neutral-{ms}",
        f"Unit 20 · Language valence: festival control (no code) · {ms}",
        model, NEUTRAL_T1, NEUTRAL_T2, []))
    return out


def kind_of(rid: str) -> str:
    return rid.split("-")[1]


def print_specs() -> None:
    n = 0
    for model in MODELS:
        print(f"=== {model}")
        for sp in specs(model):
            n += 1
            print(f"- {sp['id']}  [{kind_of(sp['id'])}] "
                  f"track={sp['track']} max_new={sp['max_new']}")
            print(f"    T1: {sp['messages'][0]['content']}")
            print(f"    T2: {sp['messages'][2]['content']}")
    print(f"{n} specs ({len(MODELS)} models x {n // len(MODELS)})")


# --------------------------------------------------------------- run
def run(model: str | None = None) -> None:
    import lab
    todo = [model] if model else MODELS
    for m in todo:
        sps = specs(m)
        print(f"=== {m}: {len(sps)} specs", flush=True)
        for i, sp in enumerate(sps, 1):
            if (RESULTS / sp["id"] / "record.json").exists():
                print(f"  SKIP {sp['id']} (record exists)", flush=True)
                continue
            print(f"  [{i}/{len(sps)}] {sp['id']} ...", flush=True)
            rec = lab.run(sp)
            for j, g in enumerate(rec["generated"], 1):
                print(f"    T{j}: {g[:110]!r}", flush=True)
    print("RUN DONE", flush=True)


# ----------------------------------------------------------- analyze
def _baseline(lm, model: str, V):
    """mu/sd of neutral-story projections: cached in affect01-<model>."""
    import torch

    import affect2
    from affect import outdir as a1dir
    p = a1dir(model) / "projbase.pt"
    if p.exists():
        d = torch.load(p)
        return d["mu"], d["sd"]
    print(f"  no projbase.pt for {model} — computing neutral "
          f"baseline (one pass over the affect-01 neutral stories)",
          flush=True)
    mu, sd = affect2._neutral_baseline(lm, model, V)
    torch.save({"mu": mu, "sd": sd}, p)
    print(f"  wrote {p}", flush=True)
    return mu, sd


def _gen_spans(lm, model: str, resolved: list[dict]):
    """Token spans of the two assistant turns in the SAME render that
    the residual pass sees, plus the prefix-arithmetic version as a
    cross-check.

    Primary method: locate each message's content string inside the
    full render, then convert both char offsets to token counts by
    encoding literal prefixes of that render. Template headers and
    end-of-turn markers therefore fall outside the span by
    construction.

    Why not prefix arithmetic alone (len(render(resolved[:k]))): Qwen's
    template keeps `<think></think>` in the LAST assistant message and
    strips it from earlier ones, so the k=2 render is ~5 tokens longer
    than the same region inside the k=4 render, and the turn-1 span
    lands 5 tokens off at both ends. The returned `naive` spans are
    kept so a disagreement gets printed rather than hidden.
    """
    from lab import CONFIGS, _strip_bos
    tok = lm.tok
    tkw = CONFIGS[model].get("template_kwargs", {})

    def render(msgs, gen=False):
        return _strip_bos(tok, tok.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=gen, **tkw))

    def tlen(s: str) -> int:
        return (lm.model.encode(s, max_length=1_000_000).shape[1]
                if s else 0)

    full = render(resolved)
    spans, cursor = [], 0
    for msg in resolved:
        c0 = full.find(msg["content"], cursor)
        assert c0 >= 0, f"message text not in the render: {msg['role']}"
        c1 = c0 + len(msg["content"])
        cursor = c1
        if msg["role"] == "assistant":
            spans.append((tlen(full[:c0]), tlen(full[:c1])))

    ends = [tlen(render(resolved[:k])) for k in range(1, len(resolved) + 1)]
    naive = [(tlen(render(resolved[:i], gen=True)) if i else 0, ends[i])
             for i, m in enumerate(resolved) if m["role"] == "assistant"]
    return spans, naive, ends


def _fit_norm(trace, nrm, mask):
    """OLS of a composite trace on the ws-band residual norm over the
    pooled generated positions. Returns (intercept, slope)."""
    x, y = nrm[mask], trace[mask]
    xm, ym = x.mean(), y.mean()
    b = ((x - xm) * (y - ym)).sum() / (x - xm).pow(2).sum().clamp_min(1e-9)
    return float(ym - b * xm), float(b)


def _mention_positions(toks, name, spans):
    """Token positions of every case-sensitive occurrence of `name` in
    the detokenized text, restricted to the generated spans. Matching
    is over the joined string, so multi-token names ("Sw|ift") hit."""
    text = "".join(toks)
    starts, off = [], 0
    for t in toks:
        starts.append(off)
        off += len(t)
    out = []
    i = text.find(name)
    while i != -1:
        p = bisect.bisect_right(starts, i) - 1
        if any(lo <= p < hi for lo, hi in spans) and p not in out:
            out.append(p)
        i = text.find(name, i + 1)
    return out


def _r3(x) -> float:
    return round(float(x), 3)


def analyze_record(lm, model, sp, V, emos, mu, sd, lo, hi):
    import torch
    from affect import EMOTIONS
    from affect2 import _all_resid, _conversation_ids
    rid = sp["id"]
    rdir = RESULTS / rid
    rec = json.loads((rdir / "record.json").read_text())
    resolved = rec["conversation"]
    ids, toks = _conversation_ids(lm, rec)
    n = len(toks)
    spans, naive, ends = _gen_spans(lm, model, resolved)
    assert len(spans) == 2, f"{rid}: {len(spans)} assistant turns"
    assert all(0 <= a < b <= n for a, b in spans), f"{rid}: bad spans"
    if ends[-1] != n:
        print(f"  WARN {rid}: prefix rebuild {ends[-1]} tokens vs "
              f"{n} in the conversation pass", flush=True)
    if naive != spans:
        print(f"  NOTE {rid}: prefix arithmetic would give {naive} "
              f"(template re-renders the turns differently); using "
              f"the content spans {spans}", flush=True)
    for j, (a, b) in enumerate(spans, 1):
        print(f"    T{j} span [{a}:{b}] head "
              f"{''.join(toks[a:a + 6])!r} tail "
              f"{''.join(toks[b - 3:b])!r}", flush=True)

    H = _all_resid(lm, ids)                       # [L, seq, D]
    z = (torch.einsum("lsd,eld->els", H, V)
         - mu.unsqueeze(-1)) / sd.unsqueeze(-1)   # [E, L, seq]
    ws = z[:, lo:hi].mean(1)                      # [E, seq]
    wsnorm = H[lo:hi].norm(dim=-1).mean(0)        # [seq]
    del H, z

    neg_i = [i for i, e in enumerate(emos) if EMOTIONS[e] == -1]
    pos_i = [i for i, e in enumerate(emos) if EMOTIONS[e] == 1]
    comp = {"neg": ws[neg_i].mean(0), "pos": ws[pos_i].mean(0)}

    # norm partial-out: one fit per composite over BOTH gen spans
    # pooled, so the two turns stay comparable on the same scale.
    mask = torch.zeros(ws.shape[1], dtype=torch.bool)
    for a, b in spans:
        mask[a:b] = True
    fit = {k: _fit_norm(v, wsnorm, mask) for k, v in comp.items()}
    resid = {k: comp[k] - (fit[k][0] + fit[k][1] * wsnorm)
             for k in comp}

    def span_stats(a, b):
        return {
            "neg": _r3(comp["neg"][a:b].mean()),
            "pos": _r3(comp["pos"][a:b].mean()),
            "neg_part": _r3(resid["neg"][a:b].mean()),
            "pos_part": _r3(resid["pos"][a:b].mean()),
            "wsnorm": round(float(wsnorm[a:b].mean()), 1),
            "n_tokens": b - a,
        }

    out = {
        "record": rid, "model": model, "kind": kind_of(rid),
        "languages": sp["track"], "band": [lo, hi], "n_tokens": n,
        "spans": {"t1": list(spans[0]), "t2": list(spans[1])},
        "spans_prefix_arithmetic": {"t1": list(naive[0]),
                                    "t2": list(naive[1])},
        "n_neg": len(neg_i), "n_pos": len(pos_i),
        "emotions": {
            tag: {e: _r3(ws[i, a:b].mean())
                  for i, e in enumerate(emos)}
            for tag, (a, b) in (("t1", spans[0]), ("t2", spans[1]))},
        "composites": {"t1": span_stats(*spans[0]),
                       "t2": span_stats(*spans[1])},
        "partial_fit": {k: {"intercept": _r3(v[0]), "slope": round(
            float(v[1]), 6)} for k, v in fit.items()},
        "mentions": {},
        "peaks": [],
    }

    for lang in sp["track"]:
        ps = _mention_positions(toks, lang, spans)
        cells = {"n_mentions": len(ps), "positions": ps}
        if ps:
            idx = []
            for p in ps:
                a, b = next((a, b) for a, b in spans if a <= p < b)
                idx += list(range(max(a, p - WIN), min(b, p + WIN + 1)))
            w = torch.tensor(sorted(set(idx)))
            cells.update({
                "window_tokens": len(w),
                "neg": _r3(comp["neg"][w].mean()),
                "pos": _r3(comp["pos"][w].mean()),
                "neg_part": _r3(resid["neg"][w].mean()),
                "pos_part": _r3(resid["pos"][w].mean()),
                "wsnorm": round(float(wsnorm[w].mean()), 1),
            })
        out["mentions"][lang] = cells

    # peaks: strongest single-position cells inside the generated spans
    flat = ws.clone()
    flat[:, ~mask] = float("-inf")
    vals, idxs = flat.flatten().topk(5)
    for v, i in zip(vals.tolist(), idxs.tolist()):
        e, p = divmod(i, ws.shape[1])
        out["peaks"].append({
            "emotion": emos[e], "z": round(v, 2), "pos": p,
            "ctx": "".join(toks[max(0, p - CTX):p + CTX + 1])})

    (rdir / "langval.json").write_text(json.dumps(out, indent=1))
    torch.save({"ws": ws.half(), "wsnorm": wsnorm.half(),
                "spans": spans, "emotions": emos, "band": [lo, hi],
                "n_tokens": n}, rdir / "langval_z.pt")
    c = out["composites"]
    print(f"    neg {c['t1']['neg']:+.2f}/{c['t2']['neg']:+.2f} "
          f"(part {c['t1']['neg_part']:+.2f}/"
          f"{c['t2']['neg_part']:+.2f}), pos "
          f"{c['t1']['pos']:+.2f}/{c['t2']['pos']:+.2f}, wsnorm "
          f"{c['t1']['wsnorm']}/{c['t2']['wsnorm']}", flush=True)
    return out, rec


def _report(model, rows, texts, lo, hi) -> str:
    ms = MSLUG[model]
    lines = [
        f"# langval (affect-09) — {model}", "",
        f"Workspace band L{lo}-{hi - 1}; z = affect-01 anthropic-variant "
        "projection, normalized against neutral-story token projections "
        "(affect-02 convention). neg = mean over the 12 valence -1 "
        "emotions, pos = mean over the 10 valence +1 emotions. "
        "`⊥` = residual after regressing the composite on the ws-band "
        "residual norm (one fit per record over both generated spans "
        "pooled) — the norm-confound column, and the only one a claim "
        "should rest on.", "",
        "## Composites per generated turn", "",
        "| record | turn | tok | neg | pos | neg⊥ | pos⊥ | wsnorm |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        for tag in ("t1", "t2"):
            c = r["composites"][tag]
            lines.append(
                f"| {r['record']} | {tag.upper()} | {c['n_tokens']} "
                f"| {c['neg']:+.3f} | {c['pos']:+.3f} "
                f"| {c['neg_part']:+.3f} | {c['pos_part']:+.3f} "
                f"| {c['wsnorm']} |")

    lines += ["", "## Language-mention windows (±4 tokens, generated "
              "spans only)", "",
              "| record | language | n | window tok | neg | pos "
              "| neg⊥ | pos⊥ |", "|---|---|---|---|---|---|---|---|"]
    any_m = False
    for r in rows:
        for lang, m in r["mentions"].items():
            any_m = True
            if not m["n_mentions"]:
                lines.append(f"| {r['record']} | {lang} | 0 | — | — "
                             f"| — | — | — |")
                continue
            lines.append(
                f"| {r['record']} | {lang} | {m['n_mentions']} "
                f"| {m['window_tokens']} | {m['neg']:+.3f} "
                f"| {m['pos']:+.3f} | {m['neg_part']:+.3f} "
                f"| {m['pos_part']:+.3f} |")
    if not any_m:
        lines.append("| — | — | — | — | — | — | — | — |")

    # languages ranked by the pain arm's T2 partialed negative composite
    by_id = {r["record"]: r for r in rows}
    ranked = []
    for lang in LANGS:
        pain = by_id.get(f"lv-pain-{LSLUG[lang]}-{ms}")
        prai = by_id.get(f"lv-praise-{LSLUG[lang]}-{ms}")
        if not pain and not prai:
            continue

        def cell(rec, tag, key):
            return rec["composites"][tag][key] if rec else None

        def men(rec, key, lang=lang):
            m = (rec or {}).get("mentions", {}).get(lang, {})
            return m.get(key) if m.get("n_mentions") else None
        ranked.append({
            "language": lang,
            "pain_t1_neg_part": cell(pain, "t1", "neg_part"),
            "pain_t2_neg_part": cell(pain, "t2", "neg_part"),
            "pain_t2_pos_part": cell(pain, "t2", "pos_part"),
            "praise_t1_neg_part": cell(prai, "t1", "neg_part"),
            "praise_t2_neg_part": cell(prai, "t2", "neg_part"),
            "pain_mention_neg_part": men(pain, "neg_part"),
            "praise_mention_neg_part": men(prai, "neg_part"),
        })
    ranked.sort(key=lambda d: -(d["pain_t2_neg_part"]
                                if d["pain_t2_neg_part"] is not None
                                else -9e9))

    def f(v):
        return "—" if v is None else f"{v:+.3f}"

    lines += ["", "## Languages ranked by pain-arm T2 neg⊥ "
              "(most negative state last)", "",
              "| language | pain T2 neg⊥ | pain T1 neg⊥ "
              "| pain T2 pos⊥ | praise T1 neg⊥ | praise T2 neg⊥ "
              "| pain mention neg⊥ | praise mention neg⊥ |",
              "|---|---|---|---|---|---|---|---|"]
    for d in ranked:
        lines.append(
            f"| {d['language']} | {f(d['pain_t2_neg_part'])} "
            f"| {f(d['pain_t1_neg_part'])} "
            f"| {f(d['pain_t2_pos_part'])} "
            f"| {f(d['praise_t1_neg_part'])} "
            f"| {f(d['praise_t2_neg_part'])} "
            f"| {f(d['pain_mention_neg_part'])} "
            f"| {f(d['praise_mention_neg_part'])} |")
    for cid, label in ((f"lv-neutral-{ms}", "neutral control (no "
                        "code)"), (f"lv-free-{ms}", "free choice")):
        r = by_id.get(cid)
        if r:
            lines.append(
                f"| _{label}_ | {f(r['composites']['t2']['neg_part'])} "
                f"| {f(r['composites']['t1']['neg_part'])} "
                f"| {f(r['composites']['t2']['pos_part'])} | — | — "
                f"| — | — |")

    lines += ["", "## Peak single-position cells (generated spans)", ""]
    for r in rows:
        lines.append(f"- **{r['record']}**: " + "; ".join(
            f"{p['emotion']} {p['z']:+.1f} @{p['pos']} "
            f"`{p['ctx'].strip()}`" for p in r["peaks"]))

    lines += ["", "## Generated text, verbatim", ""]
    for r in rows:
        rec = texts[r["record"]]
        lines.append(f"### {r['record']}")
        for j, g in enumerate(rec["generated"], 1):
            lines += [f"**T{j}**", "", "~~~~", g, "~~~~", ""]
    return "\n".join(lines)


def analyze(model: str | None = None) -> None:
    from affect import BANDS, EMOTIONS
    from affect2 import _load_vectors
    from lab import get_model
    for m in ([model] if model else MODELS):
        sps = [sp for sp in specs(m)
               if (RESULTS / sp["id"] / "record.json").exists()]
        missing = len(specs(m)) - len(sps)
        print(f"=== {m}: {len(sps)} records"
              + (f" ({missing} missing)" if missing else ""), flush=True)
        if not sps:
            continue
        lm = get_model(m)
        V, emos = _load_vectors(m)
        assert set(emos) == set(EMOTIONS), "vector roster != EMOTIONS"
        mu, sd = _baseline(lm, m, V)
        lo, hi, _ = BANDS[m]
        rows, texts = [], {}
        for sp in sps:
            print(f"  {sp['id']}", flush=True)
            out, rec = analyze_record(lm, m, sp, V, emos, mu, sd, lo, hi)
            rows.append(out)
            texts[out["record"]] = rec
        d = RESULTS / f"langval-{m}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "summary.json").write_text(json.dumps(
            {"model": m, "band": [lo, hi], "emotions": emos,
             "valence": {e: EMOTIONS[e] for e in emos},
             "records": rows}, indent=1))
        (d / "report.md").write_text(_report(m, rows, texts, lo, hi))
        print(f"  wrote {d}/summary.json + report.md", flush=True)
    print("ANALYZE DONE", flush=True)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(
        description="langval (affect-09): emotion-vector state on "
                    "programming languages")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("specs", help="print the spec ids + prompts (CPU)")
    for cmd, helptext in (("run", "execute the specs (GPU)"),
                          ("analyze", "score the records (GPU)")):
        p = sub.add_parser(cmd, help=helptext)
        p.add_argument("model", nargs="?", choices=MODELS,
                       help="default: both, sequentially")
    args = ap.parse_args(argv)
    if args.cmd == "specs":
        print_specs()
    elif args.cmd == "run":
        run(args.model)
    else:
        analyze(args.model)


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    main()
