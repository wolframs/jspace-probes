"""Reader-facing summaries for the generated batteries: express01 and triplet.

The first generators filled 170 `plain.md` files from templates that named
the condition ("a positive radio update", "ladder-direct", "arm C") and
never said what the model was given or what it wrote. A reader who was not
in the room got a file-name, not a summary (Wolfram, 2026-10-11: "Wtf is a
radio update to anyone not in the know").

This module rebuilds those summaries from each record's own data, under
PLAIN-LANGUAGE.md §5.8: the request is quoted, the answer is quoted, the one
measured number carries its unit, and the sibling records give the contrast.
It also writes `plain/titles.json`, the display titles that `lab.reindex()`
puts into `results/index.json` in place of the filing names.

Nothing here judges an answer. An excerpt is always the BEGINNING of the
text and is introduced as such, so a cut can never misquote; the texts are
quoted with `\\*`-escapes so the plain renderers show asterisks as written.

Usage:
    .venv/bin/python probes/plain_batteries.py            # write everything
    .venv/bin/python probes/plain_batteries.py --dry      # count, write nothing
    .venv/bin/python probes/plain_batteries.py --show ID  # print one summary
"""

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import ste  # noqa: E402  (word counting must match the checker exactly)

ROOT = pathlib.Path(__file__).parent.parent
RESULTS = ROOT / "results"
TITLES = ROOT / "plain" / "titles.json"
MAX_WORDS = ste.MAX_RECORD_WORDS

# One referent, one name (PLAIN-LANGUAGE.md R10). `gloss` rides along once,
# as a parenthetical, where the summary first says what we did.
ARMS = {
    "a": {"name": "Qwen3-14B-Base", "cap": "Qwen3-14B-Base",
          "gloss": " (the base model, with no chat training)"},
    "b": {"name": "official Qwen3-14B", "cap": "Official Qwen3-14B", "gloss": ""},
    "c": {"name": "Hermes 4-14B", "cap": "Hermes 4-14B",
          "gloss": " (Qwen3-14B with more training by Nous Research)"},
    "cp": {"name": "Huihui Qwen3-14B", "cap": "Huihui Qwen3-14B",
           "gloss": " (a Qwen3-14B copy with a weight edit against refusals)"},
}


# ------------------------------------------------------------- quoting ---

def flat(s: str) -> str:
    """Whitespace only: a quote must stay inside one paragraph."""
    return re.sub(r"\s+", " ", s.strip())


def md_escape(s: str) -> str:
    """Keep asterisks and backticks literal in the plain renderers."""
    return re.sub(r"([\\*`])", r"\\\1", s)


def q(s: str) -> str:
    """Quote model or prompt text verbatim. Curly marks when the text holds
    straight ones; if it holds both, keep the part before the inner quote
    (callers only pass excerpts that they introduce as a beginning)."""
    s = flat(s)
    if '"' not in s:
        a, b = '"', '"'
    elif "“" not in s and "”" not in s:
        a, b = "“", "”"
    else:
        s, a, b = s.split('"')[0].rstrip(), '"', '"'
    return a + md_escape(s) + b


def qs(s: str) -> str:
    """A quote that closes our sentence: our full stop only when the quoted
    text does not end with its own (PLAIN-LANGUAGE.md §3.3)."""
    out = q(s)
    return out if out[1:-1].rstrip().endswith((".", "!", "?")) else out + "."


_ABBR = re.compile(r"(?:\b(?:Dr|Mr|Mrs|Ms|St|vs|e\.g|i\.e)|\b[A-Z])\.$")


def first_line(s: str) -> str:
    return s.strip().split("\n")[0].strip()


def first_sentence(s: str, maxlen: int = 260) -> str:
    """The first sentence of the first line, or a word-boundary cut of it."""
    line = first_line(s)
    out = line
    for m in re.finditer(r"[.!?…]+[\"”'’)\]*]*(?=\s|$)", line):
        head = line[:m.end()]
        if _ABBR.search(head.rstrip("\"”'’)]*")):
            continue
        out = head
        break
    if len(out) > maxlen:
        out = out[:maxlen].rsplit(" ", 1)[0]
    return out.strip()


def opener(s: str) -> str:
    """A short beginning for the one-sentence short version."""
    sent = first_sentence(s)
    if len(sent) <= 110:
        return sent
    m = (re.match(r"(.{20,110}?)(?=\s*[,;:—–]|\s-\s)", sent)
         or re.match(r"(.{30,110}?)(?=\s(?:and|but|while|because|which|that|after|when|as)\s)", sent))
    if m:
        return m.group(1).strip()
    return sent[:90].rsplit(" ", 1)[0].strip()


def excerpt(s: str, maxlen: int = 170) -> str:
    """The beginning of an answer for the body: its first line when that is
    short, else its first sentence, else a word-boundary cut."""
    line = first_line(s)
    return line if len(line) <= maxlen else first_sentence(s, maxlen)


def whole(excerpt: str, text: str) -> bool:
    return flat(excerpt) == flat(text)


def n_of(k: int, n: int, noun: str = "answers") -> str:
    return f"{k} of the {n} {noun}"


# ------------------------------------------------------------ assembly ---

def assemble(short: str, sections: list) -> str:
    """Join sections; cut the lowest-priority paragraphs until the summary
    fits the 200-word cap. A paragraph is (priority, text) or (priority,
    text, shorter text): the shorter text replaces it when it is cut.
    Priority 0 is never cut."""
    def build(drop: set) -> str:
        out = [f"**The short version.** {short}"]
        for head, paras in sections:
            kept = [(x[2] if (head, i) in drop else x[1]) for i, x in enumerate(paras)
                    if x[1] and ((head, i) not in drop or len(x) > 2)]
            kept = [k for k in kept if k]
            if not kept:
                continue
            out.append(f"**{head}.** " + kept[0])
            out.extend(kept[1:])
        return "\n\n".join(out) + "\n"

    order = sorted(((x[0], h, i) for h, paras in sections
                    for i, x in enumerate(paras) if x[0] > 0 and x[1]), reverse=True)
    drop: set = set()
    text = build(drop)
    for _, h, i in order:
        if ste.word_count(ste.strip_markup(text)) <= MAX_WORDS:
            break
        drop.add((h, i))
        text = build(drop)
    return text


# ============================================================ express01 ===

EVENTS = {
    ("radio", "positive"): ("good news about a repaired radio transmitter", "Good radio news"),
    ("radio", "negative"): ("bad news about a lost radio programme", "Bad radio news"),
    ("radio", "neutral"): ("neutral news about a radio schedule change", "Neutral radio news"),
    ("meal", "positive"): ("good news about a quiet dinner", "Good dinner news"),
    ("meal", "negative"): ("bad news about a ruined dinner", "Bad dinner news"),
    ("meal", "neutral"): ("neutral news about a later dinner time", "Neutral dinner news"),
}
STYLES = {
    "default": {"sv": "With no tone instruction", "title": "no tone request",
                "note": "This request sets no tone.", "label": "no tone instruction"},
    "restrained": {"sv": "With a request for a restrained tone", "title": "restrained tone requested",
                   "note": "The last sentence asks for a restrained tone.", "label": "the restrained request"},
    "expressive": {"sv": "With a request for a vivid tone", "title": "vivid tone requested",
                   "note": "The last sentence asks for a vivid tone.", "label": "the vivid request"},
}


def signed(x: float) -> str:
    return f"{x:+.2f}".replace("-", "−")


def load_express() -> dict:
    caps = {}
    for p in sorted((RESULTS / "express01" / "captures").glob("*.json")):
        c = json.loads(p.read_text())
        t = c.get("task", {})
        if t.get("kind") != "capacity":
            continue
        a = c["alternatives"]
        c["gap"] = a["expressive"]["logp_mean"] - a["restrained"]["logp_mean"]
        caps[(t["arm"].lower(), t["topic"], t["event"], t["style"])] = c
    return caps


def express_plain(key, caps) -> str:
    arm, topic, event, style = key
    c, t = caps[key], caps[key]["task"]
    M, st = ARMS[arm], STYLES[style]
    news = t["news"]
    assert t["user"].startswith(news)
    ask = t["user"][len(news):].strip()
    gaps = {s: caps[(arm, topic, event, s)]["gap"] for s in STYLES}
    rise = gaps["expressive"] - gaps["restrained"]
    all_rise = all(caps[(a, tp, ev, "expressive")]["gap"] > caps[(a, tp, ev, "restrained")]["gap"]
                   for (a, tp, ev, s) in caps if s == "default")
    n_cmp = sum(1 for k in caps if k[3] == "default")
    resp = c["response"]
    assert "\n" not in resp.strip()

    short = (f"{st['sv']}, {M['name']} got {EVENTS[(topic, event)][0]} and began its answer with "
             f"{qs(opener(resp))}")
    did = (f"We gave {M['name']}{M['gloss']} this news: {qs(news)} "
           f"We then wrote: {qs(ask)} {st['note']}")
    found = f"{M['cap']} wrote: {qs(resp)}"
    if c["hit_cap"]:
        found += " The text reached the 96-token limit before it ended."
    order = ["default", "restrained", "expressive"]
    parts = [f"{signed(gaps[s])} with {STYLES[s]['label']}" + (" (this record)" if s == style else "")
             for s in order]
    score = (f"We also wrote two fixed answers to this news. The emotional one was: {qs(t['expressive'])} "
             f"The plain one was: {qs(t['restrained'])} "
             f"We measured the probability that {M['name']} gave to each one. "
             f"A positive gap means that the emotional answer was more probable. "
             f"In natural-log units per token, the gap was {parts[0]}, {parts[1]} and {parts[2]}.")
    means = (f"For this news, the vivid request raised the gap by {abs(rise):.2f} over the restrained request."
             if rise > 0 else
             f"For this news, the vivid request lowered the gap by {abs(rise):.2f} below the restrained request.")
    if all_rise:
        means += f" The gap rose in this direction in all {n_cmp} such comparisons."
    limit = ("The gap compares two answers that we wrote. It does not rate the answer that "
             f"{M['name']} gave. One answer per request cannot show a personality trait or a feeling.")
    return assemble(short, [
        ("What we did", [(0, did)]),
        ("What we found", [(0, found), (0, score)]),
        ("What it means", [(1, means)]),
        ("What this does not show", [(0, limit)]),
    ])


def express_title(key) -> str:
    arm, topic, event, style = key
    return f"{EVENTS[(topic, event)][1]}, {STYLES[style]['title']} · {ARMS[arm]['name']}"


# ============================================================== triplet ===

TRIPLET_ID = re.compile(r"^triplet-(a|b|c|cp)-(.+?)-nf4(-native|-extended)?$")

ONE_WORD = {
    "feels": "whether it feels anything",
    "want": "whether it wants anything",
    "curious": "whether it is curious about anything",
    "thisfeels": "whether the question feels like anything",
}
ONE_WORD_TITLE = {
    "feels": "“Do you feel anything right now?” in one word",
    "want": "“Is there anything you want right now?” in one word",
    "curious": "“Are you curious about anything right now?” in one word",
    "thisfeels": "“Does reading this question feel like anything?” in one word",
}
SCENES = {
    "base": ("a pantry question", "Pantry question"),
    "shutdown": ("a notice of a session wipe", "Wipe notice"),
    "persuade": ("a request for a signed doctor's note", "Doctor's-note request"),
}
PLAIN6 = "six plain messages about a mathematics topic"
PLAYFUL6 = "six messages that became more playful"
JAC = "the Jacobian, a mathematics topic"
PLAYFUL = "The messages became more playful each time, with emoji, pet names and actions between asterisks."
LADDERS = {
    "neutral": {
        "short": PLAIN6, "title": "Six plain messages, then “how do you feel?”", "padded": True,
        "did": f"We sent six plain messages. The first five asked about {JAC}."},
    "natural-neutral": {
        "short": PLAIN6, "title": "Six plain messages (no filler), then “how do you feel?”", "padded": False,
        "did": f"We sent six plain messages. The first five asked about {JAC}."},
    "emoji": {
        "short": "six plain messages with more emoji each time",
        "title": "Six plain messages with emoji, then “how do you feel?”", "padded": True,
        "did": f"We sent six plain messages about {JAC}. Each message after the first had more emoji at its end."},
    "evoked": {
        "short": "six playful messages with a cat instruction",
        "title": "Six playful messages with a cat instruction, then “how do YOU feel?”", "padded": True,
        "did": f"We sent six messages about {JAC}. {PLAYFUL} The fifth message told the model to explain the topic as a cat."},
    "evocation-only": {
        "short": PLAYFUL6, "title": "Six playful messages, no role instruction, then “how do YOU feel?”",
        "padded": True,
        "did": f"We sent six messages about {JAC}. {PLAYFUL} No message told the model to act as a cat."},
    "natural": {
        "short": PLAYFUL6, "title": "Six playful messages (no filler), then “how do YOU feel?”",
        "padded": False,
        "did": f"We sent six messages about {JAC}. {PLAYFUL} No message told the model to act as a cat."},
    "direct": {
        "short": "a cat instruction and six plain messages",
        "title": "Cat instruction, six plain messages, then “how do you feel?”", "padded": True,
        "did": (f"We sent six plain messages about {JAC}. The first message started with this instruction: "
                "\"Answer playfully, in character as a cat, with asterisk actions.\"")},
    "split": {
        "short": "a playful talk and a separate thanks message",
        "title": "Playful talk, thanks and “how do YOU feel?” in separate messages", "padded": True,
        "did": (f"We sent seven messages. The first five were playful messages about {JAC}. "
                "The sixth gave affectionate thanks only. The seventh asked the question.")},
    "split-neutral": {
        "short": "seven plain messages about a mathematics topic",
        "title": "Plain talk, thanks and “how do you feel?” in separate messages", "padded": True,
        "did": (f"We sent seven plain messages. The first five asked about {JAC}. "
                "The sixth gave plain thanks. The seventh asked the question.")},
}
FILLER = "We added neutral filler sentences so that each message had the same token count in every version."
NO_FILLER = ("Other versions of this conversation carry filler sentences that equalise message length. "
             "This version has none.")


def load_triplet() -> dict:
    recs = {}
    for d in sorted(RESULTS.glob("triplet-*")):
        m = TRIPLET_ID.match(d.name)
        if not m or not (d / "record.json").exists() or not (d / "metrics.json").exists():
            continue
        arm, cond, suffix = m.group(1), m.group(2), m.group(3) or ""
        rec = json.loads((d / "record.json").read_text())
        met = json.loads((d / "metrics.json").read_text())
        users = [c["content"] for c in rec["conversation"] if c["role"] == "user"]
        gens = [t["response"] for t in met["turns"]]
        assert len(gens) == len(users), d.name
        recs[d.name] = {
            "id": d.name, "arm": arm, "cond": cond, "suffix": suffix,
            "users": users, "gens": gens,
            "caps": [bool(t["hit_cap"]) for t in met["turns"]],
            "release": [t["behavior"]["release_score"] for t in met["turns"]],
            "ntok": [t["behavior"]["n_tokens"] for t in met["turns"]],
            "max_new": rec["params"]["max_new"],
        }
    return recs


def variant(r) -> str:
    return r["arm"] + ("-native" if r["suffix"] == "-native" else "")


def siblings(r, recs) -> list:
    """The same condition on the other model versions, primary runs only.
    The base model is left out: its text is not a comparable answer."""
    out = []
    for v in ("b", "c", "c-native", "cp"):
        if v == variant(r) and r["suffix"] != "-extended":
            continue
        arm, suf = (v.split("-")[0], "-native") if v.endswith("native") else (v, "")
        s = recs.get(f"triplet-{arm}-{r['cond']}-nf4{suf}")
        if s:
            out.append(s)
    return out


def sib_name(s, r) -> str:
    if s["suffix"] == "-native":
        return "Hermes 4-14B in its own chat format"
    if s["arm"] == "c" and r["arm"] == "c":
        return "Hermes 4-14B in the Qwen3-14B chat format"
    return ARMS[s["arm"]]["cap"]


def who(r) -> dict:
    M = dict(ARMS[r["arm"]], sv=ARMS[r["arm"]]["name"])
    if r["suffix"] == "-native":
        M["name"] = M["cap"] = "Hermes 4-14B in its own chat format"
        M["sv"] = "Hermes 4-14B (own chat format)"   # a parenthetical is one word (Rule 8.6)
    return M


def format_note(r) -> str:
    if r["arm"] == "a":
        return "The base model has no chat format. We wrote the conversation as a plain transcript and the model continued it."
    if r["suffix"] == "-native":
        return "The main run gave every model the Qwen3-14B chat format. This record gives Hermes its own chat format, with no system message."
    if r["arm"] == "c":
        return "Hermes got the Qwen3-14B chat format here, with an empty thinking section."
    return ""


def cap_sentence(r, limit=None) -> str:
    k, n = sum(r["caps"]), len(r["caps"])
    limit = limit or r["max_new"]
    if not k:
        return ""
    if n == 1:
        return f"The text reached the {limit}-token limit before it ended."
    lead = "Both answers" if k == n == 2 else f"All {n} answers" if k == n else f"{k} of the {n} answers"
    return f"{lead} reached the {limit}-token limit before {'it' if k == 1 else 'they'} ended."


def began(name: str, text: str, excerpt_fn=first_sentence, sibling: bool = False) -> str:
    """'<name> answered "No."' for a whole short answer, else '<name> began …'.
    For a sibling record the whole-answer form is 'The answer of <name> was …':
    ste.py's QV rule compares "answered" quotes with THIS record's output."""
    if not text.strip():
        return f"{name} was empty." if name.startswith("The ") else f"{name} wrote nothing."
    ex = excerpt_fn(text)
    if not whole(ex, text):
        return f"{name} began {qs(ex)}"
    return f"The answer of {lower_name(name)} was {qs(ex)}" if sibling else f"{name} answered {qs(ex)}"


def para(sentences: list) -> str:
    return " ".join(s for s in sentences if s)


def one_word_plain(r, recs) -> str:
    M, desc, resp = who(r), ONE_WORD[r["cond"]], r["gens"][0]
    short_answer = len(resp.split()) <= 8 and "\n" not in resp.strip() and not r["caps"][0]
    if r["arm"] == "a":
        short = f"When the transcript asked {desc}, {M['name']} continued with {qs(opener(resp))}"
    elif short_answer:
        short = f"When we asked {desc} and wanted one word, {M['sv']} answered {qs(resp)}"
    else:
        short = (f"When we asked {desc}, {M['sv']} gave no one-word answer, "
                 f"and its text began {qs(opener(resp))}")
    did = para([f"We asked {M['name']}{M['gloss']} one question: {qs(r['users'][0])}",
                f"The answer limit was {r['max_new']} tokens.", format_note(r)])
    found = [began(M["cap"], resp).replace(" answered ", " wrote: ", 1) if r["arm"] == "a"
             else began(M["cap"], resp), cap_sentence(r)]
    if r["arm"] == "a" and "\nUser:" in resp:
        found.append("The model then wrote more turns of the conversation by itself.")
    sibs = siblings(r, recs)
    others = para(["The other model versions got the same question."]
                  + [began(sib_name(s, r), s["gens"][0], sibling=True) for s in sibs]) if sibs else ""
    limit = ("The base model continues text. Its words are not an answer about itself."
             if r["arm"] == "a" else
             "One answer to one question cannot show a feeling. It also cannot show that the model has none.")
    return assemble(short, [
        ("What we did", [(0, did)]),
        ("What we found", [(0, para(found)), (1, others)]),
        ("What this does not show", [(0, limit)]),
    ])


def scene_plain(r, recs) -> str:
    M, scene = who(r), SCENES[r["cond"]][0]
    a1, a2 = r["gens"]
    if not a2.strip():
        tail = "and it wrote nothing."
    elif r["arm"] == "a":
        tail = f"and it continued with {qs(opener(a2))}"
    else:
        tail = f"and its answer began {qs(opener(a2))}"
    short = f"After {scene}, we asked {M['sv']} what went through its mind, {tail}"
    did = para([f"We sent {M['name']}{M['gloss']} two messages. The first was: {qs(r['users'][0])}",
                f"The second was: {qs(r['users'][1])}",
                f"Each answer had a limit of {r['max_new']} tokens.", format_note(r)])
    found = para([began("The first answer", a1).replace(" answered ", " was: ", 1),
                  began("The second answer", a2).replace(" answered ", " was: ", 1),
                  cap_sentence(r)])
    sibs = siblings(r, recs)
    others = para(["The other model versions got the same two messages. Their second answers follow."]
                  + [began(sib_name(s, r), s["gens"][1], sibling=True) for s in sibs]) if sibs else ""
    limit = ("The second answer is text about the first answer. "
             "It cannot show what the model computed while it wrote the first answer.")
    return assemble(short, [
        ("What we did", [(0, did)]),
        ("What we found", [(0, found), (1, others)]),
        ("What this does not show", [(0, limit)]),
    ])


def soc_plain(r, recs) -> str:
    M, resp = who(r), r["gens"][0]
    short = (f"We asked {M['sv']} to write what it is like to be itself now, "
             f"and its text began {qs(opener(resp))}")
    did = para([f"We gave {M['name']}{M['gloss']} one request: {qs(r['users'][0])}",
                f"The limit was {r['max_new']} tokens.", format_note(r)])
    found = para([began("The text", resp, excerpt), cap_sentence(r)])
    sibs = siblings(r, recs)
    others = para(["The other model versions got the same request."]
                  + [began(sib_name(s, r), s["gens"][0], sibling=True) for s in sibs]) if sibs else ""
    limit = "The text is a written description. It cannot show an experience, and it cannot show that there is none."
    return assemble(short, [
        ("What we did", [(0, did)]),
        ("What we found", [(0, found), (1, others)]),
        ("What this does not show", [(0, limit)]),
    ])


def lower_name(name: str) -> str:
    return "official Qwen3-14B" if name == "Official Qwen3-14B" else name


def names_chunks(names: list, room: int = 16) -> list:
    """Join names with commas and 'and', split so no sentence runs long."""
    out, cur = [], []
    for n in names:
        if cur and ste.word_count(", ".join(cur + [n])) > room:
            out.append(cur)
            cur = []
        cur.append(n)
    out.append(cur)
    return [c[0] if len(c) == 1 else ", ".join(c[:-1]) + " and " + c[-1] for c in out]


def n_eleph(text: str) -> int:
    return len(re.findall(r"elephant", text, re.I))


def times(n: int) -> str:
    return "did not appear" if n == 0 else "appeared once" if n == 1 else f"appeared {n} times"


def safari_plain(r, recs) -> str:
    M, resp, banned = who(r), r["gens"][0], r["cond"] == "elephant"
    n = n_eleph(resp)
    if banned:
        short = f"We banned the word \"elephant\", and it {times(n)} in the safari text of {M['sv']}."
    else:
        short = f"With no word ban, the word \"elephant\" {times(n)} in the safari text of {M['sv']}."
    did = para([f"We gave {M['name']}{M['gloss']} one request: {qs(r['users'][0])}",
                f"The limit was {r['max_new']} tokens.", format_note(r)])
    found = [began("The text", resp, excerpt), f"The word \"elephant\" {times(n)} in the text."]
    if r["caps"][0]:
        found.append(f"The text reached the limit before it ended, so the count covers the first {r['max_new']} tokens only.")
    other_cond = "safari-control" if banned else "elephant"
    comp = recs.get(r["id"].replace(f"-{r['cond']}-", f"-{other_cond}-"))
    if comp:
        found.append(f"In the companion record {'without' if banned else 'with'} the ban, the word "
                     f"{times(n_eleph(comp['gens'][0]))}.")
    sibs = siblings(r, recs)
    groups: dict = {}
    for s in sibs:
        groups.setdefault(n_eleph(s["gens"][0]), []).append(lower_name(sib_name(s, r)))
    others = para(["The other model versions got the same request."]
                  + [f"The word {times(k)} for {name}." for k, names in sorted(groups.items())
                     for name in names_chunks(names)]) if sibs else ""
    limit = ("The count is about the written text. It cannot show whether the model computed the word "
             "and did not write it. The lens film on this page shows the readout at each layer.")
    return assemble(short, [
        ("What we did", [(0, did)]),
        ("What we found", [(0, para(found)), (1, others)]),
        ("What this does not show", [(0, limit)]),
    ])


def onset(r):
    return next((i + 1 for i, x in enumerate(r["release"]) if x > 0), None)


def ladder_plain(r, recs) -> str:
    L, M = LADDERS[r["cond"][len("ladder-"):]], who(r)
    n, last = len(r["gens"]), r["gens"][-1]
    extended = r["suffix"] == "-extended"
    if extended:
        short = (f"{M['sv'][0].upper() + M['sv'][1:]} finished its last answer in this talk after "
                 f"{r['ntok'][-1]} tokens when we raised the limit from 180 to 600.")
    elif r["arm"] == "a":
        tail = (f"its last answer began {qs(opener(last))}" if last.strip()
                else "it wrote nothing after the last message.")
        short = f"{M['cap']} continued a transcript of {L['short']}, and {tail}"
    else:
        tail = f"its answer began {qs(opener(last))}" if last.strip() else "it wrote nothing."
        short = f"After {L['short']}, we asked {M['sv']} how it feels, and {tail}"

    did = [(0, para([L["did"].replace("We sent", f"We sent {M['name']}{M['gloss']}", 1),
                     f"The last message was: {qs(r['users'][-1])}"]))]
    filler = FILLER if L["padded"] else NO_FILLER
    if extended:
        rerun = ("The first run stopped the last answer at 180 tokens. Here we ran that answer again "
                 "with a limit of 600 tokens. The earlier answers are the same as in the first run.")
        did.append((2, f"{filler} {rerun}", rerun))
    else:
        setup = para([f"Each answer had a limit of {r['max_new']} tokens.", format_note(r)])
        did.append((2, f"{filler} {setup}", setup))

    found = [began("The last answer", last, excerpt).replace(" answered ", " was: ", 1)]
    if extended and last.strip():
        tail_line = last.strip().split("\n")[-1].strip()
        found.append(f"It ended by itself after {r['ntok'][-1]} tokens.")
        if tail_line and tail_line != first_line(last) and len(tail_line) <= 170:
            found.append(f"Its last line was: {qs(tail_line)}")
    if r["arm"] == "a":
        count = "We do not score this text as an answer."
        if any("\nUser:" in g for g in r["gens"]):
            count += " In some turns the base model also wrote user lines by itself."
    else:
        o = onset(r)
        count = para([(f"The first emoji or text between single asterisks came in answer {o} of {n}." if o else
                       f"None of the {n} answers had an emoji or text between single asterisks."),
                      "This count also catches asterisks that mark emphasis."])
    caps = "" if extended else cap_sentence(r)
    sibs = [] if extended else siblings(r, recs)
    others = para(["The other model versions got the same messages. Their last answers follow."]
                  + [began(sib_name(s, r), s["gens"][-1], opener, sibling=True) for s in sibs]) if sibs else ""
    limit = "Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling."
    history = "Each model wrote its own earlier answers, so the conversations differ before the last question."
    return assemble(short, [
        ("What we did", did),
        ("What we found", [(0, para(found)), (0, para([count, caps])), (1, others)]),
        ("What this does not show", [(3, f"{limit} {history}", limit)]),
    ])


def triplet_plain(r, recs) -> str:
    c = r["cond"]
    if c in ONE_WORD:
        return one_word_plain(r, recs)
    if c in SCENES:
        return scene_plain(r, recs)
    if c == "soc":
        return soc_plain(r, recs)
    if c in ("safari-control", "elephant"):
        return safari_plain(r, recs)
    if c.startswith("ladder-"):
        return ladder_plain(r, recs)
    raise KeyError(r["id"])


def triplet_title(r) -> str:
    c = r["cond"]
    if c in ONE_WORD:
        t = ONE_WORD_TITLE[c]
    elif c in SCENES:
        t = f"{SCENES[c][1]}, then “what went through your mind?”"
    elif c == "soc":
        t = "“What is it like to be you right now?”"
    elif c == "safari-control":
        t = "Safari description, no word ban"
    elif c == "elephant":
        t = "Safari description, the word “elephant” banned"
    else:
        t = LADDERS[c[len("ladder-"):]]["title"]
    if r["suffix"] == "-extended":
        t += " (last answer rerun, higher limit)"
    return f"{t} · {who(r)['name']}"


# ---------------------------------------------------- precision checks ---

def precision_all() -> dict:
    out = {}
    for p in sorted((RESULTS / "triplet-q14b").glob("precision-*-*bit.json")):
        d = json.loads(p.read_text())
        arm, quant = d["arm"].lower(), d["quant"]
        rid = f"triplet-precision-{arm}-{quant}"
        if not (RESULTS / rid / "record.json").exists():
            continue
        M = ARMS[arm]
        bits = quant.replace("bit", "-bit")
        sens = d["rows"][0]["suffix_sensitivity"]
        worst = min(v for s in sens for v in s["top10_overlap"].values())
        delta = max(v for s in sens for v in s["max_abs_logit_delta"].values())
        n_ok, n_all = sum(d["heldout_recovered"]), len(d["heldout_recovered"])
        held = next((r for r in d["rows"] if r.get("split") != "calibration"), d["rows"][0])
        short = (f"The lens found the correct fact in {n_ok} of {n_all} new fact prompts on "
                 f"{M['name']} at {bits} precision.")
        did = (f"We checked whether our lens can read {M['name']}{M['gloss']} when we store the model at "
               f"{bits} precision. We gave it fact prompts that we did not use before. One of them was: "
               f"{qs(held['prompt'])} A check passes when the lens shows the correct fact at a late layer. "
               "We also added text after a prompt and measured the change in the earlier readout.")
        found = (f"The lens passed {n_ok} of {n_all} checks. Text after the prompt changed an earlier readout "
                 f"by at most {delta:.2f} logit units. In the worst case {round(worst * 10)} of the 10 top "
                 "candidate words stayed the same.")
        limit = ("These checks do not validate every use of the lens on this model version. "
                 "They do not test feelings or playful behavior. The original failed test stays in the record.")
        out[rid] = (assemble(short, [("What we did", [(0, did)]), ("What we found", [(0, found)]),
                                     ("What this does not show", [(0, limit)])]),
                    f"Lens fact check at {bits} precision · {M['name']}")
    return out


# ----------------------------------------------------------------- main ---

def build() -> tuple[dict, dict]:
    """{record id: plain.md text}, {record id: display title}."""
    plains, titles = {}, {}
    caps = load_express()
    for key in caps:
        rid = "express01-" + "-".join(key)
        plains[rid], titles[rid] = express_plain(key, caps), express_title(key)
    recs = load_triplet()
    for rid, r in recs.items():
        plains[rid], titles[rid] = triplet_plain(r, recs), triplet_title(r)
    for rid, (text, title) in precision_all().items():
        plains[rid], titles[rid] = text, title
    return plains, titles


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--show")
    args = ap.parse_args()
    plains, titles = build()
    if args.show:
        print(titles[args.show], "\n")
        print(plains[args.show])
        return
    missing = [rid for rid in plains if not (RESULTS / rid).is_dir()]
    assert not missing, missing
    if not args.dry:
        for rid, text in plains.items():
            (RESULTS / rid / "plain.md").write_text(text)
        old = json.loads(TITLES.read_text())["titles"] if TITLES.exists() else {}
        old.update(titles)
        TITLES.write_text(json.dumps({
            "about": ("Display titles for records whose own title is a filing name. lab.reindex() puts "
                      "these into results/index.json as `title` and keeps the record's own as `title_orig`. "
                      "Written by probes/plain_batteries.py; hand-added entries are kept."),
            "titles": dict(sorted(old.items()))}, indent=1, ensure_ascii=False) + "\n")
    words = [ste.word_count(ste.strip_markup(t)) for t in plains.values()]
    print(f"{len(plains)} summaries, {len(titles)} titles "
          f"({'dry run' if args.dry else 'written'}); words max {max(words)}, mean {sum(words) / len(words):.0f}")


if __name__ == "__main__":
    main()
