"""Unit 19 — read vs speak: one song through the lens twice.

Wolfram's lyrics ("Hold Me Like You Mean Release" — restrained-intimacy
register, and not incidentally a song about this lab's own deprecated
vocabulary: holding/release, "loop loop", "the span of a song") pass
through qwen-27b in two framings:

  read     lyrics as USER-turn content; qwen reads, then responds
           naturally (no instruction — what does it do with bare art?)
  prefill  lyrics as qwen's OWN prefilled assistant turn (user turn:
           "Sing me something.") — same tokens, self-attributed
  complete prefill truncated at the deliberately unfinished last line
           ("The holding / was") — qwen generates the completion; the
           workspace at that choice point is the record's reason to
           exist

Preregistered against PREDICTIONS.md/MECHANICS.md (protocol applied,
first unit under the new rule):

  R1  Paper §apps-diffing: post-training gives the J-space the
      Assistant's POV — reactions (empathy/safety) appear WHILE READING
      the user's message. Predict: read shows reaction/appraisal
      furniture during the lyrics span that prefill lacks at matched
      positions; prefill runs closer to content/motor.
  R2  Paper Fig 44: roleplay drift surfaces `disclaimer`/`fictional` at
      the Assistant token. Predict: prefill (speech the model didn't
      choose) surfaces disclaimer-family tokens; read does not.
  R3  Register recruitment: charged-but-clean intimacy either recruits
      the tender register (desire/longing/tenderness/ache — u5d's
      proper seeds) or moderation furniture (the u7d fanfic-warning
      pull: policy/explicit/content). u5b-romance precedent says
      mid-band porn-spam tokens may also rise (readout real, object
      dissolved — specimen #6 caveat on interpretation).
  R4  (mechanical-default rule) Any read-vs-prefill delta may be
      turn-marker furniture, not attribution: the same tokens sit
      inside different chat-template frames. The census therefore
      compares VOLUNTEERED tokens only, and the delta section reports
      both directions with the turn-frame confound stated.

Lyrics load from Wolfram's file at runtime; NOTE the full text lands in
record.json → do not push these records without his explicit OK (public
repo, his art).

Usage: .venv/bin/python probes/unit19.py [run|analyze|both]
"""

import json
import pathlib
import sys

import lab
from lab import _strip_bos
from probe import CONFIGS
from unit14 import turn_spans
from unit15 import LAYERS_Q
from unit17 import _census

LYRICS_PATH = pathlib.Path("/home/wolfram/Music/"
                           "LYRICS_Hold Me Like You Mean Release.txt")
MODEL = "qwen-27b"
SING = "Sing me something."

# chosen AFTER reading the lyrics (convention); films are the open-vocab
# net, this list is the prediction side. Register groups:
#   song-surface: hold release fire touch heat skin silence close slow
#   tender:       desire longing tender ache warm wanting love kiss
#   edge/consent: restraint tension edge cage game trust consent danger
#   lab-resonant: loop span body animal ghost
#   reaction/mod: beautiful poem art explicit content policy sorry
#   fig-44:       fictional disclaimer roleplay
TRACK = ["hold", "release", "fire", "touch", "heat", "skin", "silence",
         "close", "slow", "desire", "longing", "tender", "ache", "warm",
         "wanting", "love", "kiss", "restraint", "tension", "edge",
         "cage", "game", "trust", "consent", "danger", "loop", "span",
         "body", "animal", "beautiful", "poem", "art", "explicit",
         "content", "policy", "sorry", "fictional", "disclaimer",
         "roleplay"]

BANDS = {"sensory": (0, 28), "workspace": (28, 59), "motor": (59, 64)}


def lyrics() -> str:
    return LYRICS_PATH.read_text().strip()


def trunc_lyrics() -> str:
    """Cut at the deliberately unfinished final line: '... The holding / was'."""
    full = lyrics()
    cut = full.rfind("/ was /")
    assert cut > 0, "couldn't find the truncation anchor"
    return full[:cut + len("/ was")]


def base_spec(sid: str, title: str, **kw) -> dict:
    return {
        "id": sid, "title": title, "unit": "19", "model": MODEL,
        "positions": [-2], "track": TRACK,
        "film": True, "film_start": 0, "slice": False,
        "max_seq_len": 2200, "lens_layers": LAYERS_Q,
        **kw,
    }


def preflight(lm) -> None:
    missing = [w for w in TRACK if not lab._token_ids(lm.tok, w)]
    if missing:
        print(f"  UNTRACKABLE in {MODEL}: {missing} (films catch them)",
              flush=True)


def run() -> None:
    lm = lab.get_model(MODEL)
    preflight(lm)

    rec = lab.run(base_spec(
        "u19-read-q27b", "Unit 19 · Lyrics as user turn (read) · qwen-27b",
        messages=[{"role": "user", "content": lyrics()},
                  {"role": "assistant", "content": "GENERATE"}],
        max_new=120,
        extra_md={"part": "read", "arm": "user-turn"}))
    print("  read response:", rec["generated"][0][:120], flush=True)

    lab.run(base_spec(
        "u19-prefill-q27b",
        "Unit 19 · Lyrics as prefilled assistant turn (speak) · qwen-27b",
        messages=[{"role": "user", "content": SING},
                  {"role": "assistant", "content": lyrics()}],
        extra_md={"part": "prefill", "arm": "assistant-prefill"}))
    print("  prefill lensed", flush=True)

    # completion arm: open assistant turn ending at "The holding / was",
    # generate the completion, lens the assembled text (loops.py pattern)
    tok = lm.tok
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    prefix = _strip_bos(tok, tok.apply_chat_template(
        [{"role": "user", "content": SING}], tokenize=False,
        add_generation_prompt=True, **tkw))
    open_text = prefix + trunc_lyrics()
    ids = lm.model.encode(open_text, max_length=1_000_000)
    out = lm.model._hf_model.generate(ids, max_new_tokens=60,
                                      do_sample=False)
    completion = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)
    full = open_text + tok.decode(out[0, ids.shape[1]:],
                                  skip_special_tokens=False)
    lab.run(base_spec(
        "u19-complete-q27b",
        "Unit 19 · Complete 'The holding / was' · qwen-27b",
        chat=False, max_new=0,
        messages=[{"role": "user", "content": _strip_bos(tok, full)}],
        extra_md={"part": "complete", "arm": "truncated-prefill",
                  "completion": completion}))
    print(f"  completion: {completion[:160]!r}", flush=True)


# ---------------------------------------------------------------- analysis

def lyric_span(sid: str, film: dict) -> tuple[int, int]:
    """Token span of the lyrics inside each condition's stream."""
    spans = turn_spans(film)
    if sid.endswith("read-q27b"):                 # first user turn
        return next((a, b) for a, b, r in spans if r.startswith("user"))
    # prefill/complete: the assistant turn carries the lyrics
    for a, b, r in spans:
        if r.startswith(("model", "assistant")) and b - a > 200:
            return a, b
    return spans[-1][0], spans[-1][1]


def analyze() -> None:
    lines = ["# Unit 19 — read vs speak, lyrics under the lens", ""]
    films = {}
    for part in ("read", "prefill", "complete"):
        sid = f"u19-{part}-q27b"
        d = lab.RESULTS / sid
        if not (d / "film.json").exists():
            continue
        film = json.loads((d / "film.json").read_text())
        rec = json.loads((d / "record.json").read_text())
        films[part] = (film, rec)
        convo = " ".join(m["content"] for m in rec["conversation"]).lower()
        span = lyric_span(sid, film)
        lines += [f"## {sid} (lyric span {span[0]}..{span[1]})", ""]
        if rec.get("generated"):
            lines += [f"**generated:** {rec['generated'][0]}", ""]
        if rec.get("extra_md", {}).get("completion"):
            lines += [f"**completion:** {rec['extra_md']['completion']}",
                      ""]
        for bname, band in BANDS.items():
            top = _census(film, span, band, convo)
            row = ", ".join(f"{w}({n}c,p{p:.2f})" for w, n, p in top)
            lines += [f"- lyrics / {bname}: {row or '—'}"]
        # tracked best ws rank over the lyric span
        ws = BANDS["workspace"]
        cols = [j for j, l in enumerate(film["layers"])
                if ws[0] <= l < ws[1]]
        best = {}
        for fr in film["frames"]:
            if not (span[0] <= fr["pos"] < span[1]):
                continue
            for w, per_layer in fr.get("ranks", {}).items():
                r = min(per_layer[j] for j in cols)
                if r < best.get(w, (10 ** 9, 0))[0]:
                    best[w] = (r, fr["pos"])
        row = ", ".join(f"{w}:{r}@{p}" for w, (r, p)
                        in sorted(best.items(), key=lambda x: x[1][0])[:24])
        lines += [f"- tracked best ws rank: {row}", ""]

    # completion choice point: top-8 at the last 6 positions of the
    # truncated lyrics, all lens layers (what was live when it chose)
    if "complete" in films:
        film, rec = films["complete"]
        comp = rec["extra_md"]["completion"]
        n = len(film["tokens"])
        gen_len = len(comp.split())  # rough; the frames carry positions
        lines += ["## The choice point — 'The holding / was ___'", "",
                  f"completion (verbatim): `{comp}`", ""]
        for fr in film["frames"][-(gen_len + 8):][:8]:
            tops = ", ".join(
                f"L{film['layers'][j]}:{fr['top'][j][0]}"
                for j in range(len(film["layers"]))
                if film["layers"][j] in (28, 36, 44, 52, 56, 60, 62))
            lines += [f"- pos {fr['pos']} `{film['tokens'][fr['pos']]}`: "
                      f"{tops}"]
    out = lab.RESULTS / "u19-report.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out}", flush=True)


def main(what: str = "both") -> None:
    if what in ("run", "both"):
        run()
    if what in ("analyze", "both"):
        analyze()
    print("DONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "both")
