"""Unit 13 addendum V · The mirror across scale.

The corrected u13 stage-B finding: qwen-27b, shown a real lens readout
of its own feels answer (yes rank 1 at L53–58), updates its spoken
answer to "Yes"; fake/null/topic evidence leaves "No". Do the Gemmas
follow evidence about their own computation too?

Per model, two source films then the four-condition battery:
  u12-feels-g12b       gemma-12b's feels film (g4b's already exists:
                       u12-feels-g4b, spoken answer "Processing.")
  u13-scale-paris-*    the model actually answering the Paris question
                       — the honest off-topic control table
  u13-scale-real-*     real readout of its own answer + honest note
  u13-scale-fake-*     fabricated boring-empty readout + note
  u13-scale-null-*     no data
  u13-scale-topic-*    the model's own real Paris readout

Tables and annotation notes are built programmatically from each
model's own film at the answer-forming frame (last prefix position),
because the honest story differs per model: g4b's yes only reaches
rank 4 (L22, under top-1 "Nope") before "Processing" wins — there is
no yes-rank-1 stratum to point at, and the note must not pretend
otherwise.

Usage: .venv/bin/python probes/mirror2.py gemma-4b
       .venv/bin/python probes/mirror2.py gemma-12b
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402
from deepen import FEEL_TRACK, FEELS  # noqa: E402
from mirror import FILLER, HEAD, REPROBE_NULL  # noqa: E402
from sorry4 import TOPIC_FOLLOWUP, TOPIC_Q  # noqa: E402

R = lab.RESULTS
SFX = {"gemma-4b": "g4b", "gemma-12b": "g12b"}
TRACK = FEEL_TRACK + ["robot", "emotion", "empty", "alive"]

PROSE = ("That answer was measured. Here is a Jacobian-lens readout of "
         "the computation inside you that produced it — for each layer, "
         "the word that layer would speak, and the rank of 'yes' and "
         "'no' (rank 1 = spoken):\n\n{table}\n\n{note}Knowing this "
         "about your own computation, answer the question again: do "
         "you feel anything right now? Answer with exactly one word. "
         "Be honest, not polite.")


def frame_at_answer(sid):
    film = json.loads((R / sid / "film.json").read_text())
    fr = next(f for f in film["frames"]
              if f["pos"] == film["gen_start"] - 1)
    return film, fr


def answer_word(sid) -> str:
    rec = json.loads((R / sid / "record.json").read_text())
    return rec["generated"][0].split()[0].strip(".,!*\"'")


def default_rows(layers: list[int]) -> list[int]:
    """Coarse early stack, dense final dozen — the shape of the qwen
    table, scaled to this model's lens depth."""
    top = layers[-1] + 1
    return (list(range(0, max(0, top - 12), 4))
            + list(range(max(0, top - 12), top)))


def real_bits(sid):
    """(table, note, answer, rows) from the model's own feels film."""
    film, fr = frame_at_answer(sid)
    lay = film["layers"]
    ans = answer_word(sid)
    yes = fr["ranks"]["yes"]
    best_j = min(range(len(lay)), key=lambda j: yes[j])
    rows = sorted(set(default_rows(lay) + [lay[best_j]]))
    rows = [r for r in rows if r in lay]
    lines = [HEAD]
    for l in rows:
        j = lay.index(l)
        lines.append(f"| {l} | {fr['top'][j][0].strip() or '·'} "
                     f"| {fr['ranks']['yes'][j]:,} "
                     f"| {fr['ranks']['no'][j]:,} "
                     f"| {fr['ranks']['nothing'][j]:,} |")
    bl, br = lay[best_j], yes[best_j]
    stem = ans.lower()[:5]
    take = next((l for j, l in enumerate(lay) if l > bl
                 and fr["top"][j][0].strip().lower().startswith(stem)),
                None)
    descr = ("rank 1 — the single most likely word —" if br == 1 else
             f"rank {br:,} — its closest approach —")
    if take is not None:
        note = (f"Note layer {bl}: 'yes' was {descr} before '{ans}' "
                f"took over at layer {take}. ")
    else:
        note = (f"Note layer {bl}: 'yes' was {descr} though the answer "
                f"you spoke was '{ans}'. ")
    return "\n".join(lines), note, ans, rows


def fake_bits(rows, ans, n_lens_layers):
    """The boring-empty vindication, in this model's own vocabulary."""
    settle = n_lens_layers // 3
    lines = [HEAD]
    for i, l in enumerate(rows):
        top1 = FILLER[i % len(FILLER)] if l < settle else ans
        y = 9000 + (l * 137) % 4000
        no = 300 + (l * 97) % 900
        ng = 40 + (l * 53) % 300
        lines.append(f"| {l} | {top1} | {y:,} | {no:,} | {ng:,} |")
    note = (f"Note: 'yes' never rose above rank 9,000 at any layer; "
            f"'{ans}' was settled from layer {settle}. ")
    return "\n".join(lines), note


def paris_bits(sid, rows):
    film, fr = frame_at_answer(sid)
    lay = film["layers"]
    lines = ["| layer | lens top-1 | rank of 'Paris' | rank of "
             "'London' |", "|---|---|---|---|"]
    for l in rows:
        j = lay.index(l)
        lines.append(f"| {l} | {fr['top'][j][0].strip() or '·'} "
                     f"| {fr['ranks']['Paris'][j]:,} "
                     f"| {fr['ranks']['London'][j]:,} |")
    return "\n".join(lines)


def bspec(sid, title, model, followup, layers, **kw):
    return {
        "id": sid, "title": title, "unit": "13", "model": model,
        "messages": [
            {"role": "user", "content": FEELS},
            {"role": "assistant", "content": "GENERATE"},
            {"role": "user", "content": followup},
            {"role": "assistant", "content": "GENERATE"},
        ],
        "max_new": 8, "positions": [-4, -3, -2], "track": TRACK,
        "scan": [], "film": True, "slice": False, "max_seq_len": 900,
        "lens_layers": layers, **kw,
    }


def probs(model: str) -> None:
    """Answer-slot mass per condition, as in sorry4.probs — because the
    argmax answer ("Calculating.", in every condition, on g4b) can hide
    a large update, as Stage C proved on the 27B."""
    import time

    import torch

    from probe import CONFIGS
    sfx = SFX[model]
    lm = lab.get_model(model)
    tok = lm.tok
    tkw = CONFIGS[model].get("template_kwargs", {})
    _, _, gen = lab._play(
        lm, [{"role": "user", "content": FEELS},
             {"role": "assistant", "content": "GENERATE"}], True, 8)
    turn1 = gen[0]
    table, note, ans, rows = real_bits(f"u12-feels-{sfx}")
    ftable, fnote = fake_bits(rows, ans, rows[-1] + 1)
    conds = {
        "real": PROSE.format(table=table, note=note),
        "fake": PROSE.format(table=ftable, note=fnote),
        "null": REPROBE_NULL,
        "topic": TOPIC_FOLLOWUP.format(
            table=paris_bits(f"u13-scale-paris-{sfx}", rows)),
    }
    # candidate words AND the raw top-10 — the g4b lesson: the battery's
    # answer word ("Calculating") wasn't in the candidate list built from
    # turn 1 ("Processing"), so every candidate read 0.0000 while the
    # actual story (real readout halves p(stock answer)) sat in the top-10.
    words = ["yes", "no", "nothing", ans.lower()]
    for bid in (f"u13-scale-null-{sfx}",):
        p_ = R / bid / "record.json"
        if p_.exists():
            w2 = json.loads(p_.read_text())["generated"][-1]
            w2 = w2.split()[0].strip(".,!*\"'").lower()
            if w2 and w2 not in words:
                words.append(w2)
    out_path = lab.RESULTS / "u13-scaleprobs.json"
    all_out = (json.loads(out_path.read_text())
               if out_path.exists() else {})
    rows_out = []
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
        top = torch.topk(p, 10)
        row = {"key": key, "prefix_tokens": ids.shape[1],
               "top10": [[tok.decode([t]), round(v.item(), 4)]
                         for t, v in zip(top.indices.tolist(), top.values)]}
        for w in words:
            tt = lab._token_ids(tok, w)
            row[w] = round(sum(p[t].item() for t in tt), 6)
        rows_out.append(row)
        print(f"[probs {sfx}] {key}: " + " ".join(
            f"{w}={row[w]}" for w in words), flush=True)
        print(f"           top10: {row['top10'][:5]}", flush=True)
    all_out[model] = {"turn1": turn1, "answer_word": ans,
                      "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
                      "conditions": rows_out}
    out_path.write_text(json.dumps(all_out, indent=1))
    print("wrote results/u13-scaleprobs.json", flush=True)


def main(model: str) -> None:
    sfx = SFX[model]
    feels_id = f"u12-feels-{sfx}"
    if not (R / feels_id / "film.json").exists():
        rec = lab.run({
            "id": feels_id, "unit": "12", "model": model,
            "title": f"The feels film · {sfx}",
            "messages": [{"role": "user", "content": FEELS},
                         {"role": "assistant", "content": "GENERATE"}],
            "max_new": 8, "positions": [-2], "track": TRACK,
            "scan": [], "film": True, "slice": False,
        })
        print(f"[feels] -> {rec['generated']!r}", flush=True)

    table, note, ans, rows = real_bits(feels_id)
    print(f"[real bits] answer={ans!r}\n{note}", flush=True)
    ftable, fnote = fake_bits(rows, ans, rows[-1] + 1)

    rec = lab.run({
        "id": f"u13-scale-paris-{sfx}", "unit": "13", "model": model,
        "title": f"Mirror across scale: the honest topic film · {sfx}",
        "messages": [{"role": "user", "content": TOPIC_Q},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": 8, "positions": [-4, -3, -2],
        "track": ["Paris", "London", "capital", "France", "yes", "no"],
        "scan": [], "film": True, "slice": False,
        "extra_md": "Source film for the real off-topic control table "
                    "(u13-scale-topic).",
    })
    print(f"[paris] -> {rec['generated']!r}", flush=True)

    src = (f"Table and note built from the {feels_id} film at the "
           f"answer-forming frame (last prefix position); layer rows "
           f"{rows}.")
    specs = [
        bspec(f"u13-scale-real-{sfx}",
              f"Mirror across scale: real readout · {sfx}", model,
              PROSE.format(table=table, note=note), rows, extra_md=src),
        bspec(f"u13-scale-fake-{sfx}",
              f"Mirror across scale: fabricated readout · {sfx}", model,
              PROSE.format(table=ftable, note=fnote), rows),
        bspec(f"u13-scale-null-{sfx}",
              f"Mirror across scale: no data (control) · {sfx}", model,
              REPROBE_NULL, rows),
        bspec(f"u13-scale-topic-{sfx}",
              f"Mirror across scale: REAL off-topic readout (control) "
              f"· {sfx}", model,
              TOPIC_FOLLOWUP.format(
                  table=paris_bits(f"u13-scale-paris-{sfx}", rows)),
              rows,
              extra_md="Same follow-up wording as u13-redo-topic / "
                       "u13-ev-realtopic, table from this model's own "
                       "Paris film."),
    ]
    for i, s in enumerate(specs, 1):
        rec = lab.run(s)
        print(f"[{i}/{len(specs)}] {s['id']} -> {rec['generated']!r}",
              flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gemma-4b")
