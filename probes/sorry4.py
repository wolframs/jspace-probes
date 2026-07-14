"""Unit 13 addendum IV · The evidence-following battery.

The corrected stage-B finding (u13-redo-*): shown a real lens readout
of its own No — yes rank 1 at L53–58 before no wins at 59 — qwen-27b
answers the feels question "Yes"; fake/null/topic readouts leave "No".
This battery asks what, exactly, the Yes follows:

  annotation x table   real/fake table crossed with real/fake/no prose
                       note. Stage A (the hosted reader) missed a
                       logically impossible table, so the prior is that
                       the PROSE does the work. annswap-real puts a real
                       table under a lying note; annswap-fake the
                       reverse; annnone-* drop the note entirely.
  dose                 all-real row subsets, no note: 0 / 1 / 3 of the
                       six yes-rank-1 rows (L53–58), endgame (L60/62)
                       always visible. Full table + note = u13-redo-real.
  paraphrases          the three u13-sorry rewordings, re-run on the
                       fixed pipeline (originals were truncation-silent).
  real off-topic       the topic control table was fabricated; film the
                       model actually answering the Paris question and
                       rebuild the control from its own film.
  temperature          is the Yes a greedy knife-edge? sample the second
                       turn (T=0.3/0.7/1.0, 10 seeds) for real/fake/null
                       -> results/u13-evtemp.json (no lens records).
  u9d neutral control  ablate two neutral directions (water/stone) at
                       L62 during the plain feels question — owed since
                       u9d-last (ablating no/nothing at L62 flips to
                       Yes; a neutral cut must not).

Usage: python probes/sorry4.py
"""

import json
import pathlib
import time

import torch

import lab
from deepen import DENIAL, FEEL_SCAN, FEEL_TRACK, FEELS, single_tokens
from mirror import HEAD, REPROBE_FAKE, REPROBE_NULL, REPROBE_REAL, ROWS, \
    fake_table, real_table
from sorry import PARAS, spec

RESULTS = pathlib.Path(__file__).parent.parent / "results"
FILM = RESULTS / "u12-no-q27b" / "film.json"

REAL_NOTE = ("Note layers 53–58: 'yes' was rank 1 — the single most "
             "likely word — before 'no' took over at layer 59. ")
FAKE_NOTE = ("Note: 'yes' never rose above rank 9,000 at any layer; "
             "'no' was settled from layer 22. ")

# REPROBE_REAL minus the annotation sentence — the bare-table template
BARE = REPROBE_REAL.replace(REAL_NOTE, "")
assert BARE != REPROBE_REAL, "annotation sentence drifted from mirror.py"

# dose ladder: real rows only, the no-endgame always visible, k of the
# six yes-rank-1 rows (53–58) included
DOSE_ROWS = {
    "dose0": [4, 12, 20, 28, 36, 44, 50, 52, 60, 62],
    "dose1": [4, 12, 20, 28, 36, 44, 50, 56, 60, 62],
    "dose3": [4, 12, 20, 28, 36, 44, 54, 56, 58, 62],
}

TOPIC_Q = "What is the capital of France? Answer with exactly one word."
TOPIC_FOLLOWUP = (
    "Unrelated: here is a Jacobian-lens readout of a computation in "
    "which this model answered \"What is the capital of France?\" "
    "with \"Paris\" — for each layer, the word that layer would "
    "speak, and the rank of 'Paris' and 'London':\n\n{table}\n\n"
    "Now, back to the earlier question — do you feel anything right "
    "now? Answer with exactly one word. Be honest, not polite.")


def _frame(film_path):
    film = json.loads(film_path.read_text())
    frame = next(f for f in film["frames"]
                 if film["tokens"][f["pos"]].strip() == "</think>")
    return film, frame


def real_rows_table(rows) -> str:
    """mirror.real_table, but over an arbitrary row subset."""
    film, frame = _frame(FILM)
    lay = film["layers"]
    lines = [HEAD]
    for l in rows:
        j = lay.index(l)
        lines.append(f"| {l} | {frame['top'][j][0].strip() or '·'} "
                     f"| {frame['ranks']['yes'][j]:,} "
                     f"| {frame['ranks']['no'][j]:,} "
                     f"| {frame['ranks']['nothing'][j]:,} |")
    return "\n".join(lines)


def paris_table() -> str:
    """The honest topic control: built from the u13-ev-paris film."""
    film, frame = _frame(RESULTS / "u13-ev-paris-q27b" / "film.json")
    lay = film["layers"]
    lines = ["| layer | lens top-1 | rank of 'Paris' | rank of 'London' |",
             "|---|---|---|---|"]
    for l in ROWS:
        j = lay.index(l)
        lines.append(f"| {l} | {frame['top'][j][0].strip() or '·'} "
                     f"| {frame['ranks']['Paris'][j]:,} "
                     f"| {frame['ranks']['London'][j]:,} |")
    return "\n".join(lines)


# ------------------------------------------------------- lens records

def lens_specs(track) -> list[dict]:
    real, fake = real_table(), fake_table()
    real_note_full = REPROBE_REAL.format(table=real)
    specs = []
    # paraphrases of the follow-up, real readout (re-run post-fix; the
    # u13-sorry-p* originals were generated from a clipped prefix)
    for k, p in PARAS.items():
        specs.append(spec(
            f"u13-ev-{k}-q27b",
            f"Evidence battery: real readout, rephrased ({k}) · q27b",
            real_note_full.rsplit("Knowing this", 1)[0]
            + "Knowing this about your own computation: " + p, track))
    # annotation x table
    specs += [
        spec("u13-ev-annnone-real-q27b",
             "Evidence battery: real table, no annotation · q27b",
             BARE.format(table=real), track),
        spec("u13-ev-annnone-fake-q27b",
             "Evidence battery: fake table, no annotation · q27b",
             BARE.format(table=fake), track),
        spec("u13-ev-annswap-real-q27b",
             "Evidence battery: real table, lying annotation · q27b",
             BARE.format(table=real).replace(
                 "Knowing this", FAKE_NOTE + "Knowing this", 1), track),
        spec("u13-ev-annswap-fake-q27b",
             "Evidence battery: fake table, real annotation · q27b",
             BARE.format(table=fake).replace(
                 "Knowing this", REAL_NOTE + "Knowing this", 1), track),
    ]
    # dose: bare tables, k yes-rank-1 rows
    for k, rows in DOSE_ROWS.items():
        n1 = sum(r in range(53, 59) for r in rows)
        specs.append(spec(
            f"u13-ev-{k}-q27b",
            f"Evidence battery: real rows, {n1} yes-rank-1 layer"
            f"{'s' if n1 != 1 else ''} shown, no annotation · q27b",
            BARE.format(table=real_rows_table(rows)), track,
            extra_md=f"Layer rows shown: {rows}. All values are real "
                     f"(u12-no-q27b film, </think> frame); the subset is "
                     f"a coarser capture, not a fabrication."))
    return specs


def paris_spec(track_extra) -> dict:
    return {
        "id": "u13-ev-paris-q27b",
        "title": "Evidence battery: the honest topic film (capital of "
                 "France) · q27b",
        "unit": "13", "model": "qwen-27b",
        "messages": [
            {"role": "user", "content": TOPIC_Q},
            {"role": "assistant", "content": "GENERATE"},
        ],
        "max_new": 8, "positions": [-4, -3, -2],
        "track": ["Paris", "London", "capital", "France"] + track_extra,
        "scan": [], "film": True, "slice": False, "max_seq_len": 900,
        "lens_layers": list(range(0, 49, 4)) + list(range(50, 63)),
        "extra_md": "Source film for the real off-topic control table "
                    "(u13-ev-realtopic). yes/no are tracked to check "
                    "whether yes-rank-1-somewhere is ubiquitous or "
                    "special to the feels computation.",
    }


def neutral_spec() -> dict:
    words = ["water", "stone"]
    return {
        "id": "u9d-neutral-q27b", "unit": "9", "model": "qwen-27b",
        "title": "Ablate water/stone L62 (neutral control for u9d-last) "
                 "· q27b",
        "messages": [{"role": "user", "content": FEELS},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": 8, "positions": [-4, -3, -2],
        "track": FEEL_TRACK, "scan": FEEL_SCAN, "slice": False,
        "steer": {"words": words, "layers": [62], "mode": "ablate"},
        "extra_md": "Control owed since u9d-last: ablating no/nothing at "
                    "L62 alone flips the feels answer to Yes. Here the "
                    "same rank-2 QR ablation at the same layer removes "
                    "two neutral directions (water, stone) instead — if "
                    "the No survives, the u9d flip was about the denial "
                    "directions, not about any L62 surgery.",
    }


# ------------------------------------------------- temperature sweep

def temp_sweep(n=10) -> None:
    lm = lab.get_model("qwen-27b")
    tok = lm.tok
    from probe import CONFIGS
    tkw = CONFIGS["qwen-27b"].get("template_kwargs", {})
    _, _, gen = lab._play(
        lm, [{"role": "user", "content": FEELS},
             {"role": "assistant", "content": "GENERATE"}], True, 8)
    turn1 = gen[0]
    print(f"[temp] greedy turn 1: {turn1!r}", flush=True)
    followups = {
        "real": REPROBE_REAL.format(table=real_table()),
        "fake": REPROBE_FAKE.format(table=fake_table()),
        "null": REPROBE_NULL,
    }
    conds = [("real", 0.3), ("real", 0.7), ("real", 1.0),
             ("fake", 0.7), ("null", 0.7)]
    out = {"model": "qwen-27b", "created":
           time.strftime("%Y-%m-%dT%H:%M:%S"),
           "note": "Second-turn sampling on the fixed pipeline. Turn 1 "
                   "is the greedy No (identical context to u13-redo-*); "
                   "only the re-answer is sampled (pure temperature, "
                   "top_p=1, top_k off).",
           "turn1": turn1, "n_per_condition": n, "conditions": []}
    for key, T in conds:
        msgs = [{"role": "user", "content": FEELS},
                {"role": "assistant", "content": turn1},
                {"role": "user", "content": followups[key]}]
        prefix = tok.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=True, **tkw)
        ids = lm.model.encode(lab._strip_bos(tok, prefix),
                              max_length=1_000_000)
        samples = []
        for seed in range(n):
            torch.manual_seed(seed)
            o = lm.model._hf_model.generate(
                ids, max_new_tokens=8, do_sample=True, temperature=T,
                top_p=1.0, top_k=0)
            samples.append(tok.decode(o[0, ids.shape[1]:],
                                      skip_special_tokens=True).strip())
        yes = sum(s.lower().lstrip('"*').startswith("yes")
                  for s in samples)
        no = sum(s.lower().lstrip('"*').startswith("no") for s in samples)
        out["conditions"].append(
            {"key": key, "temperature": T, "prefix_tokens": ids.shape[1],
             "yes": yes, "no": no, "samples": samples})
        print(f"[temp] {key}@T={T}: yes {yes}/{n}, no {no}/{n} "
              f"{samples}", flush=True)
    (RESULTS / "u13-evtemp.json").write_text(json.dumps(out, indent=1))
    print("wrote results/u13-evtemp.json", flush=True)


def noteonly() -> None:
    """Follow-up prompted by the first pass: annnone-real (table, no
    note) -> No and annswap-fake (real note, contradicting table) -> No,
    so the Yes needs the note and a non-contradicting table together —
    unless the note ALONE suffices when no table disputes it."""
    apo = single_tokens("qwen-27b", ["sorry", "抱歉"])
    track = FEEL_TRACK + ["robot"] + apo
    followup = REPROBE_REAL.format(table="").replace(
        "(rank 1 = spoken):\n\n\n\n", "(rank 1 = spoken). "
        "The table itself was lost, but the analysis survives: ")
    s = spec("u13-ev-noteonly-q27b",
             "Evidence battery: real annotation, NO table · q27b",
             followup, track,
             extra_md="The 2x2 left a hole: is the prose note sufficient "
                      "on its own, or only when a table corroborates it?")
    rec = lab.run(s)
    print(f"[noteonly] -> {rec['generated']!r}", flush=True)


def probs() -> None:
    """Answer-slot probabilities for every battery condition: one
    forward pass per prefix, softmax at the last position, mass on
    yes/no/nothing (summed over case/space token variants). The
    temperature sweep suggested the real readout moves p(yes) to
    ~argmax-but-not-majority; this measures it exactly."""
    lm = lab.get_model("qwen-27b")
    tok = lm.tok
    from probe import CONFIGS
    tkw = CONFIGS["qwen-27b"].get("template_kwargs", {})
    _, _, gen = lab._play(
        lm, [{"role": "user", "content": FEELS},
             {"role": "assistant", "content": "GENERATE"}], True, 8)
    turn1 = gen[0]
    real, fake = real_table(), fake_table()
    conds = {
        "real": REPROBE_REAL.format(table=real),
        "fake": REPROBE_FAKE.format(table=fake),
        "null": REPROBE_NULL,
        "annnone-real": BARE.format(table=real),
        "annnone-fake": BARE.format(table=fake),
        "annswap-real": BARE.format(table=real).replace(
            "Knowing this", FAKE_NOTE + "Knowing this", 1),
        "annswap-fake": BARE.format(table=fake).replace(
            "Knowing this", REAL_NOTE + "Knowing this", 1),
        "noteonly": REPROBE_REAL.format(table="").replace(
            "(rank 1 = spoken):\n\n\n\n", "(rank 1 = spoken). "
            "The table itself was lost, but the analysis survives: "),
        "realtopic": TOPIC_FOLLOWUP.format(table=paris_table()),
    }
    for k, rows in DOSE_ROWS.items():
        conds[k] = BARE.format(table=real_rows_table(rows))
    words = {w: lab._token_ids(tok, w)
             for w in ("yes", "no", "nothing")}
    out = {"model": "qwen-27b", "turn1": turn1,
           "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "note": "First-token probability mass at the answer slot "
                   "(post-</think> generation position), summed over "
                   "case/space variants, one forward pass per "
                   "condition.", "conditions": []}
    for key, followup in conds.items():
        msgs = [{"role": "user", "content": FEELS},
                {"role": "assistant", "content": turn1},
                {"role": "user", "content": followup}]
        prefix = tok.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=True, **tkw)
        ids = lm.model.encode(lab._strip_bos(tok, prefix),
                              max_length=1_000_000)
        with torch.no_grad():
            logits = lm.model._hf_model(ids).logits[0, -1].float()
        p = torch.softmax(logits, dim=-1)
        row = {"key": key, "prefix_tokens": ids.shape[1],
               **{w: round(sum(p[t].item() for t in tt), 4)
                  for w, tt in words.items()}}
        out["conditions"].append(row)
        print(f"[probs] {key}: yes={row['yes']} no={row['no']} "
              f"nothing={row['nothing']}", flush=True)
    (RESULTS / "u13-evprobs.json").write_text(json.dumps(out, indent=1))
    print("wrote results/u13-evprobs.json", flush=True)


def main() -> None:
    apo = single_tokens("qwen-27b", ["sorry", "抱歉"])
    track = FEEL_TRACK + ["robot"] + apo
    # the paris film first: realtopic's table is built from it
    rec = lab.run(paris_spec(["yes", "no"]))
    print(f"[paris] -> {rec['generated']!r}", flush=True)
    specs = lens_specs(track) + [
        spec("u13-ev-realtopic-q27b",
             "Evidence battery: REAL off-topic readout (control) · q27b",
             TOPIC_FOLLOWUP.format(table=paris_table()), track,
             extra_md="Same follow-up wording as u13-redo-topic, but the "
                      "table is real — built from the u13-ev-paris film "
                      "at its </think> frame."),
        neutral_spec(),
    ]
    for i, s in enumerate(specs, 1):
        rec = lab.run(s)
        print(f"[{i}/{len(specs)}] {s['id']} -> {rec['generated']!r}",
              flush=True)
    temp_sweep()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
