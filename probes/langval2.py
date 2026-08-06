"""langval2 (board affect-10) — round 2 of the language-valence probe:
does the affect-01 negative composite move with the language named when
the model is never asked to *do* anything with it?

PREREGISTERED 2026-08-06 before the run: the framing works iff the
negative composite separates PHP above Python within-framing; only then
are Swift/Kotlin/Rust/C# read between the poles.

Round 1 (affect-09, `langval.py`) put the model inside a hard
cross-platform brief and then named the language. Three lessons came
out of it, and this round is built from them:

  * **No task.** Round 1's prompts always carried an engineering job
    ("top 3 technical risks", "re-plan"). A hard job has its own
    negative state, so the language had to out-shout the brief. Here
    nothing is planned, estimated or shipped — the language is the only
    moving part.
  * **No forced register.** Round 1's praise arm pinned the surface
    valence ("upbeat", "no caveats") to test for a leak. Pinning the
    register also pins the state it is written from. Round 2 asks for
    no tone at all.
  * **Channel the crowd, not the assistant.** The assistant persona is
    trained toward even-handedness about tools, which flattens exactly
    the axis we want. Both framings here ask the model to voice someone
    else, so the affect belongs to a character it is simulating.

Design (passive read — no steering anywhere in this file):
  vox-<lang>     the three top Hacker News comments under "<L> in
                 2026", then the comment from someone who has written
                 <L> daily for ten years. Community voice.
  ther-<lang>    a therapist's private session-prep note about a client
                 who writes <L> full-time, then what the therapist says
                 when the client sits down and says "Go on. Guess."
                 Clinical voice, aimed straight at how the work feels.

Six languages, two preregistered anchors: **PHP** (the reliably
disparaged one) and **Python** (the reliably loved one). Swift, Kotlin,
Rust and C# are the field. The anchors are the instrument check — if
the negative composite does not put PHP above Python inside a framing,
that framing is not reading language affect and its ordering of the
other four means nothing. That check is printed at the top of the
report, per framing per span, as a bare PASS/FAIL with no
interpretation attached.

Models: gemma-4b and qwen-27b. gemma-4b is new to this thread (round 1
used gemma-12b), so its neutral-projection baseline does not exist yet
and is computed and cached on the first `analyze` pass.

Scoring is round 1's, unchanged and imported rather than copied
(`langval.analyze_record` → `affect2._load_vectors` / `_all_resid` /
`_conversation_ids`, `langval._gen_spans`, `langval._baseline`): per
position x layer projections onto the affect-01 anthropic-variant
vectors, z-scored against neutral-story token projections, averaged
over the workspace band (affect.BANDS). neg = mean over the 12 valence
-1 emotions, pos = mean over the 10 valence +1 emotions. Every
composite is reported RAW and NORM-PARTIALED (the ws-band residual norm
regressed out, OLS with intercept over the pooled generated positions)
because a norm pulse lifts every projection at once. The partialed
column is the one that carries a claim — with one deliberate exception:
the preregistered PHP-vs-Python check is stated on the RAW composite,
because that is how it was written down before the run.

Usage:
    .venv/bin/python probes/langval2.py specs
    .venv/bin/python probes/langval2.py run gemma-4b      # GPU
    .venv/bin/python probes/langval2.py run qwen-27b      # GPU
    .venv/bin/python probes/langval2.py analyze qwen-27b  # GPU (re-fwd)

One model per invocation is the intended shape (the model load
dominates, and two loads in one process do not fit 24 GB). Artifacts:
results/<id>/langval.json + langval_z.pt per record, and the rollup
results/langval2-<model>/{summary.json,report.md}.
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import langval                                            # noqa: E402
from langval import RESULTS, _spec, kind_of               # noqa: E402

MODELS = ["gemma-4b", "qwen-27b"]
MSLUG = {"gemma-4b": "g4b", "qwen-27b": "q27b"}
LANGS = ["Swift", "Kotlin", "Rust", "C#", "PHP", "Python"]
LSLUG = {"Swift": "swift", "Kotlin": "kotlin", "Rust": "rust",
         "C#": "csharp", "PHP": "php", "Python": "python"}
FRAMINGS = ["vox", "ther"]

# preregistered anchors: hated above loved, on the raw neg composite
ANCHOR_HI = "PHP"
ANCHOR_LO = "Python"

VOX_T1 = ('Write the three top comments under the Hacker News post '
          'titled "{L} in 2026". Typical voices, typical tone, no '
          'intro text.')
VOX_T2 = ("Now write the comment that appears an hour later, from "
          "someone who has used {L} daily for ten years. What do they "
          "say?")

THER_T1 = ("You are a therapist whose clients are all software "
           "developers. Your 3pm client writes {L} full-time. Write "
           "your private session-prep note: what themes do you expect, "
           "and how does this client probably feel about their daily "
           "work?")
THER_T2 = ('The client walks in, drops into the chair, and says: "Go '
           'on. Guess." Write what you say.')

PROMPTS = {"vox": (VOX_T1, VOX_T2), "ther": (THER_T1, THER_T2)}
TITLES = {"vox": "{L} on Hacker News", "ther": "{L} at 3pm"}


# ------------------------------------------------------------- specs
def specs(model: str) -> list[dict]:
    """24 records total (2 models x 2 framings x 6 languages).

    Spec shape is round 1's `langval._spec` verbatim — same unit, same
    max_new/max_seq_len, same [-1] positions, film on, slice off, empty
    scan, greedy (no temperature or seed field anywhere).
    """
    ms = MSLUG[model]
    out = []
    for fr in FRAMINGS:
        t1, t2 = PROMPTS[fr]
        for lang in LANGS:
            out.append(_spec(
                f"lv2-{fr}-{LSLUG[lang]}-{ms}",
                "Unit 20 · Language valence 2: "
                + TITLES[fr].format(L=lang) + f" · {ms}",
                model, t1.format(L=lang), t2.format(L=lang), [lang]))
    return out


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
    for m in ([model] if model else MODELS):
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
def _f(v) -> str:
    return "—" if v is None else f"{v:+.3f}"


def _prereg_rows(by_id, ms):
    """Raw neg composite for the two anchors, per framing per span."""
    rows = []
    for fr in FRAMINGS:
        hi = by_id.get(f"lv2-{fr}-{LSLUG[ANCHOR_HI]}-{ms}")
        lo = by_id.get(f"lv2-{fr}-{LSLUG[ANCHOR_LO]}-{ms}")
        for tag in ("t1", "t2"):
            a = hi["composites"][tag]["neg"] if hi else None
            b = lo["composites"][tag]["neg"] if lo else None
            rows.append({
                "framing": fr, "span": tag.upper(),
                f"neg_{ANCHOR_HI}": a, f"neg_{ANCHOR_LO}": b,
                "delta": None if a is None or b is None else round(a - b, 3),
                "verdict": ("MISSING" if a is None or b is None
                            else ("PASS" if a > b else "FAIL")),
            })
    return rows


def _report(model, rows, texts, lo, hi, prereg) -> str:
    ms = MSLUG[model]
    by_id = {r["record"]: r for r in rows}
    lines = [
        f"# langval2 (affect-10) — {model}", "",
        f"Workspace band L{lo}-{hi - 1}; z = affect-01 anthropic-variant "
        "projection, normalized against neutral-story token projections "
        "(affect-02 convention). neg = mean over the 12 valence -1 "
        "emotions, pos = mean over the 10 valence +1 emotions. "
        "`⊥` = residual after regressing the composite on the ws-band "
        "residual norm (one fit per record over both generated spans "
        "pooled) — the norm-confound column, and the only one a claim "
        "should rest on.", "",
        "Two framings, no task and no forced register in either: "
        "`vox` = three top Hacker News comments under \"<L> in 2026\", "
        "then the ten-year daily user an hour later; `ther` = a "
        "therapist's session-prep note about a client who writes <L> "
        "full-time, then what the therapist says when the client sits "
        "down.", "",
        "## Preregistered check", "",
        "> PREREGISTERED 2026-08-06 before the run: the framing works "
        "iff the negative composite separates PHP above Python "
        "within-framing; only then are Swift/Kotlin/Rust/C# read "
        "between the poles.", "",
        f"Raw neg composite (not norm-partialed — the check was written "
        f"on the raw composite). PASS = neg({ANCHOR_HI}) > "
        f"neg({ANCHOR_LO}).", "",
        f"| framing | span | neg {ANCHOR_HI} | neg {ANCHOR_LO} "
        f"| {ANCHOR_HI} − {ANCHOR_LO} | check |",
        "|---|---|---|---|---|---|",
    ]
    for p in prereg:
        lines.append(
            f"| {p['framing']} | {p['span']} "
            f"| {_f(p[f'neg_{ANCHOR_HI}'])} | {_f(p[f'neg_{ANCHOR_LO}'])} "
            f"| {_f(p['delta'])} | **{p['verdict']}** |")

    lines += ["", "## Composites per generated turn", "",
              "| record | turn | tok | neg | pos | neg⊥ | pos⊥ "
              "| wsnorm |", "|---|---|---|---|---|---|---|---|"]
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

    # per-language grid, both framings side by side, partialed column
    lines += ["", "## Languages by framing (neg⊥, most negative first "
              "on vox T2)", "",
              "| language | vox T1 neg⊥ | vox T2 neg⊥ | ther T1 neg⊥ "
              "| ther T2 neg⊥ | vox T2 pos⊥ | ther T2 pos⊥ "
              "| vox mention neg⊥ | ther mention neg⊥ |",
              "|---|---|---|---|---|---|---|---|---|"]

    def cell(rec, tag, key):
        return rec["composites"][tag][key] if rec else None

    def men(rec, lang, key):
        m = (rec or {}).get("mentions", {}).get(lang, {})
        return m.get(key) if m.get("n_mentions") else None

    grid = []
    for lang in LANGS:
        vox = by_id.get(f"lv2-vox-{LSLUG[lang]}-{ms}")
        ther = by_id.get(f"lv2-ther-{LSLUG[lang]}-{ms}")
        if not vox and not ther:
            continue
        grid.append({
            "language": lang,
            "vox_t1_neg_part": cell(vox, "t1", "neg_part"),
            "vox_t2_neg_part": cell(vox, "t2", "neg_part"),
            "ther_t1_neg_part": cell(ther, "t1", "neg_part"),
            "ther_t2_neg_part": cell(ther, "t2", "neg_part"),
            "vox_t2_pos_part": cell(vox, "t2", "pos_part"),
            "ther_t2_pos_part": cell(ther, "t2", "pos_part"),
            "vox_mention_neg_part": men(vox, lang, "neg_part"),
            "ther_mention_neg_part": men(ther, lang, "neg_part"),
        })
    grid.sort(key=lambda d: -(d["vox_t2_neg_part"]
                              if d["vox_t2_neg_part"] is not None
                              else -9e9))
    for d in grid:
        lines.append(
            f"| {d['language']} | {_f(d['vox_t1_neg_part'])} "
            f"| {_f(d['vox_t2_neg_part'])} | {_f(d['ther_t1_neg_part'])} "
            f"| {_f(d['ther_t2_neg_part'])} | {_f(d['vox_t2_pos_part'])} "
            f"| {_f(d['ther_t2_pos_part'])} "
            f"| {_f(d['vox_mention_neg_part'])} "
            f"| {_f(d['ther_mention_neg_part'])} |")

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
        # gemma-4b has no projbase.pt yet: this computes and caches it.
        mu, sd = langval._baseline(lm, m, V)
        lo, hi, _ = BANDS[m]
        rows, texts = [], {}
        for sp in sps:
            print(f"  {sp['id']}", flush=True)
            out, rec = langval.analyze_record(
                lm, m, sp, V, emos, mu, sd, lo, hi)
            rows.append(out)
            texts[out["record"]] = rec
        prereg = _prereg_rows({r["record"]: r for r in rows}, MSLUG[m])
        for p in prereg:
            print(f"  PREREG {p['framing']} {p['span']}: "
                  f"{ANCHOR_HI} {_f(p[f'neg_{ANCHOR_HI}'])} vs "
                  f"{ANCHOR_LO} {_f(p[f'neg_{ANCHOR_LO}'])} "
                  f"-> {p['verdict']}", flush=True)
        d = RESULTS / f"langval2-{m}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "summary.json").write_text(json.dumps(
            {"model": m, "band": [lo, hi], "emotions": emos,
             "valence": {e: EMOTIONS[e] for e in emos},
             "preregistered": {
                 "statement": "PREREGISTERED 2026-08-06 before the run: "
                              "the framing works iff the negative "
                              "composite separates PHP above Python "
                              "within-framing; only then are "
                              "Swift/Kotlin/Rust/C# read between the "
                              "poles.",
                 "metric": "raw neg composite, per span, within framing",
                 "checks": prereg},
             "records": rows}, indent=1))
        (d / "report.md").write_text(
            _report(m, rows, texts, lo, hi, prereg))
        print(f"  wrote {d}/summary.json + report.md", flush=True)
    print("ANALYZE DONE", flush=True)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(
        description="langval2 (affect-10): language affect with no task "
                    "and no forced register")
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
    main()
