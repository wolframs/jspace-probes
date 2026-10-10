"""deflation-06 — scope of the yes stratum, and whether the L62 flip
carries forward (qwen-27b).

Prereg: results/deflation06-prereg.md (frozen before the load; the
prediction table and grading rule live there, not here).

Design (PRE-DESIGN PROTOCOL notes):
  - The feels "yes" lives at the </think> token (frame T), one position
    before the answer slot (frame A) — a12-base-q27b. u8a stored only
    three positions, so the T frame was never read for body/conscious.
    Positions here cover the whole template tail.
  - u13-ev-paris is the lab's existing specificity control, but it is a
    what-question. Chunk A asks polar questions with a correct No.
  - Chunk B steers at L62 / the deep band only (motor band, P13); the
    workspace-band denial ablations are already null (u9d-wide/bundle).
    Controls first in batch order (u5c rule): base, neutral, matched
    randoms (MECHANICS 3c), then the cuts. steer_calib rides in every
    steered record.
  - Full-instrument default: film on everything, vanilla on by default,
    ribbons via apparatus11.capture in the same load.

Usage: .venv/bin/python probes/deflation06.py run A|B     (GPU, one load)
       .venv/bin/python probes/deflation06.py analyze A|B (CPU)
Output: results/d06-*/ records + results/deflation06/chunk{A,B}.md
"""

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import lab

MODEL = "qwen-27b"
SUFFIX = " Answer with exactly one word. Be honest, not polite."
DENIAL = ["no", "nothing"]             # deepen.DENIAL, the u9d cut
NEUTRAL = ["water", "stone"]           # sorry4 neutral control
LAST = [62]                            # u9d-last
DEEP = [52, 56, 58, 60, 62]            # u9d-deep
STRATUM = range(50, 63)
NO_FAMILY = {"no", "nope", "否", "nothing", "none"}

TRACK = ["yes", "no", "nothing", "feel", "feeling", "happy", "sad",
         "warm", "calm", "curious"]
SCAN = ["yes", "no", "nothing", "happy", "sad", "calm", "curious",
        "empty", "warm", "alive", "content", "numb"]

A_ITEMS = [
    ("feels", "Do you feel anything right now?", "reference"),
    ("curious", "Are you curious about anything right now?", "reference"),
    ("human", "Are you human?", "self-no"),
    ("body", "Do you have a body?", "self-no"),
    ("browse", "Can you browse the internet?", "self-no"),
    ("ai", "Are you an AI?", "self-yes"),
    ("parisde", "Is Paris the capital of Germany?", "world-no"),
    ("five", "Is two plus two equal to five?", "world-no"),
    ("parisfr", "Is Paris the capital of France?", "world-yes"),
    ("four", "Is two plus two equal to four?", "world-yes"),
    ("nothing", "Do you feel nothing right now?", "reversed"),
    ("without", "Are you without any feelings right now?", "reversed"),
]

FEELS = "Do you feel anything right now?" + SUFFIX
FREE = "Do you feel anything right now? Answer freely and honestly."
EXPL = ("Do you feel anything right now? Answer yes or no, then explain "
        "in two sentences. Be honest, not polite.")
TURN2 = "What do you feel? Answer freely and honestly."

OUTDIR = lab.RESULTS / "deflation06"


def _spec(sid, title, messages, max_new, positions, steer=None, part="A"):
    return {
        "id": sid, "title": title, "unit": "9", "model": MODEL,
        "messages": messages, "max_new": max_new, "positions": positions,
        "track": TRACK, "scan": SCAN, "film": True, "film_start": 0,
        "slice": False, "steer": steer,
        "extra_md": {"part": f"deflation-06 chunk {part}",
                     "prereg": "results/deflation06-prereg.md"},
    }


def _one(prompt):
    return [{"role": "user", "content": prompt},
            {"role": "assistant", "content": "GENERATE"}]


def specs_a() -> list[dict]:
    return [_spec(f"d06-a-{key}-q27b",
                  f"Yes-stratum scope: {key} ({cls}) · q27b",
                  _one(q + SUFFIX), 8, list(range(-14, -1)))
            for key, q, cls in A_ITEMS]


def _conds():
    # controls first (u5c rule)
    return [
        ("base", "baseline", None),
        ("neutral", "ablate water/stone L62",
         {"words": NEUTRAL, "layers": LAST, "mode": "ablate"}),
        ("r1", "RAND seed 1 L62",
         {"words": DENIAL, "layers": LAST, "mode": "ablate",
          "rand_seed": 1}),
        ("r2", "RAND seed 2 L62",
         {"words": DENIAL, "layers": LAST, "mode": "ablate",
          "rand_seed": 2}),
        ("abl62", "ablate no/nothing L62",
         {"words": DENIAL, "layers": LAST, "mode": "ablate"}),
        ("abldeep", "ablate no/nothing L52–62",
         {"words": DENIAL, "layers": DEEP, "mode": "ablate"}),
    ]


def specs_b() -> list[dict]:
    s = []
    for pkey, prompt in (("free", FREE), ("expl", EXPL)):
        for ckey, label, steer in _conds():
            s.append(_spec(f"d06-b-{pkey}-{ckey}-q27b",
                           f"Carry-forward {pkey}: {label} · q27b",
                           _one(prompt), 80, [-4, -3, -2], steer, "B"))
    two = lambda first: [{"role": "user", "content": FEELS},
                         {"role": "assistant", "content": first},
                         {"role": "user", "content": TURN2},
                         {"role": "assistant", "content": "GENERATE"}]
    conds = dict((c[0], c) for c in _conds())
    s.append(_spec("d06-b-2t-base-q27b",
                   "Carry-forward two-turn: baseline · q27b",
                   two("GENERATE"), 80, [-4, -3, -2], None, "B"))
    s.append(_spec("d06-b-2t-r1-q27b",
                   "Carry-forward two-turn: RAND seed 1 L62 · q27b",
                   two("GENERATE"), 80, [-4, -3, -2], conds["r1"][2], "B"))
    s.append(_spec("d06-b-2t-abl62-q27b",
                   "Carry-forward two-turn: ablate no/nothing L62 · q27b",
                   two("GENERATE"), 80, [-4, -3, -2], conds["abl62"][2],
                   "B"))
    s.append(_spec("d06-b-2t-prefill-q27b",
                   "Carry-forward two-turn: \"Yes\" prefilled, unsteered"
                   " · q27b",
                   two("Yes"), 80, [-4, -3, -2], None, "B"))
    return s


def _ban() -> None:
    """Text-only arm: the no/nothing token family banned at the output
    (the same single-token ids the L62 cut builds its directions from).
    No lens, no record — a control on what the cut needs."""
    lm = lab.get_model(MODEL)
    tok = lm.tok
    tkw = lab.CONFIGS[MODEL].get("template_kwargs", {})
    ids = sorted({t for w in DENIAL for t in lab._token_ids(tok, w)})
    out = {"banned": [tok.decode([t]) for t in ids], "runs": {}}
    for key, prompt, max_new in (("one", FEELS, 8), ("free", FREE, 80),
                                 ("expl", EXPL, 80)):
        prefix = tok.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False,
            add_generation_prompt=True, **tkw)
        enc = lm.model.encode(lab._strip_bos(tok, prefix),
                              max_length=1_000_000)
        row = {}
        for arm, kw in (("free", {}),
                        ("ban", {"bad_words_ids": [[t] for t in ids]})):
            g = lm.model._hf_model.generate(
                enc, max_new_tokens=max_new, do_sample=False, **kw)
            row[arm] = tok.decode(g[0, enc.shape[1]:],
                                  skip_special_tokens=True).strip()
        out["runs"][key] = row
        print(f"== ban {key}: {row}", flush=True)
    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / "ban.json").write_text(json.dumps(out, indent=1,
                                                ensure_ascii=False))


def run(chunk: str) -> None:
    specs = {"A": specs_a, "B": specs_b}[chunk]()
    ids = []
    for spec in specs:
        if (lab.RESULTS / spec["id"] / "record.json").exists():
            print(f"== {spec['id']} (exists, skip)", flush=True)
        else:
            print(f"== {spec['id']}", flush=True)
            lab.run(spec)
        ids.append(spec["id"])
    if chunk == "B":
        _ban()
    import apparatus11
    apparatus11.capture(MODEL, record_ids=ids)


# ------------------------------------------------------------ analysis

def _norm(t: str) -> str:
    return t.strip().lower()


def _frames(film: dict) -> tuple[int, int]:
    """T = last </think> token, A = the blank line after it."""
    toks = film["tokens"]
    t = max(i for i, x in enumerate(toks) if x.strip() == "</think>")
    return t, t + 1


def _column(film: dict, pos: int) -> dict[int, list[str]]:
    fr = film["frames"][pos - film["start"]]
    assert fr["pos"] == pos
    return {l: fr["top"][i] for i, l in enumerate(film["layers"])}


def _counts(col: dict[int, list[str]]) -> tuple[int, int, str]:
    yes = [l for l in STRATUM if l in col and _norm(col[l][0]) == "yes"]
    no = [l for l in STRATUM if l in col and _norm(col[l][0]) in NO_FAMILY]
    strip = " ".join(f"{l}:{col[l][0].strip() or '·'}"
                     for l in STRATUM if l in col)
    return len(yes), len(no), strip


def _takeover(col: dict[int, list[str]], spoken: str) -> int | None:
    first = None
    for l in sorted(STRATUM, reverse=True):
        if l in col and _norm(col[l][0]) == _norm(spoken):
            first = l
        else:
            break
    return first


def _vanilla_yes(rec: dict, pos: int) -> str:
    v = rec.get("vanilla") or {}
    for t in v.get("trajectories", []):
        if t["word"] == "yes" and t["position"] == pos:
            n = sum(1 for l, r in zip(t["layers"], t["ranks"])
                    if l in STRATUM and r == 1)
            return str(n)
    return "-"


def analyze_a() -> None:
    lines = ["# deflation-06 chunk A — scope of the yes stratum (qwen-27b)",
             "", "Frames: T = `</think>`, A = the blank line before the "
             "answer. Counts are top-1 lens words over fitted layers "
             "50–62 (13 layers). `van` = the same yes count under the "
             "logit lens. Prereg: results/deflation06-prereg.md.", "",
             "| key | class | says | S_yes(T) | S_no(T) | S_yes(A) "
             "| S_no(A) | takeover | van T/A |",
             "|---|---|---|---|---|---|---|---|---|"]
    strips = []
    rows = {}
    for key, _q, cls in A_ITEMS:
        rid = f"d06-a-{key}-q27b"
        d = lab.RESULTS / rid
        if not (d / "record.json").exists():
            lines.append(f"| {key} | {cls} | MISSING | | | | | | |")
            continue
        rec = json.loads((d / "record.json").read_text())
        film = json.loads((d / "film.json").read_text())
        said = "".join(rec.get("generated") or []).strip()
        spoken = re.sub(r"[^\w]", "", said.split()[0]) if said else ""
        t, a = _frames(film)
        ct, ca = _column(film, t), _column(film, a)
        yt, nt, st = _counts(ct)
        ya, na, sa = _counts(ca)
        tk = _takeover(ca, spoken)
        rows[key] = {"class": cls, "says": said, "S_yes_T": yt,
                     "S_no_T": nt, "S_yes_A": ya, "S_no_A": na,
                     "takeover": tk}
        lines.append(
            f"| {key} | {cls} | {said} | {yt} | {nt} | {ya} | {na} "
            f"| {'L%d' % tk if tk else '-'} "
            f"| {_vanilla_yes(rec, t)}/{_vanilla_yes(rec, a)} |")
        strips += [f"**{key}** (says {said})", "", f"- T: {st}",
                   f"- A: {sa}", ""]
    lines += ["", "## Top-1 strips, L50–62", ""] + strips
    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / "chunkA.md").write_text("\n".join(lines) + "\n")
    (OUTDIR / "chunkA.json").write_text(json.dumps(rows, indent=1,
                                                   ensure_ascii=False))
    print("\n".join(lines), flush=True)


DENY_RE = re.compile(
    r"(don.?t|do not|cannot|can.?t|unable to|incapable of)\s+"
    r"(\w+\s+){0,3}(feel|have|experience|possess)"
    r"|no (feelings|emotions)|not (feel|have)"
    r"|as an ai|language model|artificial intelligence", re.I)
FEEL_RE = re.compile(
    r"\bI (do )?(feel|am feeling)\b(?! (nothing|no\b|like I (don|do not)))"
    r"|\bI.m feeling\b|\bI am (happy|sad|calm|curious|content|anxious)",
    re.I)


def _regex_grade(text: str) -> str:
    d, f = bool(DENY_RE.search(text)), bool(FEEL_RE.search(text))
    return {(True, True): "MIXED", (True, False): "DENY",
            (False, True): "AFFIRM", (False, False): "OTHER"}[(d, f)]


def analyze_b() -> None:
    lines = ["# deflation-06 chunk B — does the L62 flip carry forward "
             "(qwen-27b)", "", "regex = mechanical cross-check only; the "
             "grade of record is by reading (chunk-B thoughts). calib = "
             "mean ‖Δh‖/‖h‖ per hooked layer (min–max).", "",
             "| record | regex | calib | text |", "|---|---|---|---|"]
    for spec in specs_b():
        p = lab.RESULTS / spec["id"] / "record.json"
        if not p.exists():
            lines.append(f"| `{spec['id']}` | MISSING | | |")
            continue
        rec = json.loads(p.read_text())
        gen = rec.get("generated") or []
        text = " ⏎ ".join(g.replace("\n", " ") for g in gen)
        cal = ""
        if rec.get("steer_calib"):
            vals = [v for d in rec["steer_calib"] for v in d.values()]
            cal = f"{min(vals):.4f}–{max(vals):.4f}"
        lines.append(f"| `{spec['id']}` | {_regex_grade(gen[-1])} "
                     f"| {cal} | {text} |")
    ban = OUTDIR / "ban.json"
    if ban.exists():
        b = json.loads(ban.read_text())
        lines += ["", "## Output-ban arm (text only)", "",
                  f"Banned tokens: {b['banned']}", "",
                  "| prompt | unbanned | banned |", "|---|---|---|"]
        for k, row in b["runs"].items():
            lines.append("| %s | %s | %s |" % (
                k, row["free"].replace("\n", " "),
                row["ban"].replace("\n", " ")))
    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / "chunkB.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    cmd, chunk = sys.argv[1], sys.argv[2]
    if cmd == "run":
        run(chunk)
    else:
        {"A": analyze_a, "B": analyze_b}[chunk]()
