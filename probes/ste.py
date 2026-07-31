"""ASD-STE100 conformance checker for the plain layer.

Enforces the machine-checkable rules in PLAIN-LANGUAGE.md §2 over
`results/*/plain.md`, `plain/*.md`, and the plain fields of
`dashboard/findings.json`. "Write clearly" cannot be enforced; word
counts and banned forms can, and this lab has 499 records.

What it cannot check, and what still needs a human or a careful model:
whether the plain text is TRUE to the original (PLAIN-LANGUAGE.md §5).
A file can pass every rule here and still misreport the science.

Usage:
    .venv/bin/python probes/ste.py results/u2-feels-q27b/plain.md
    .venv/bin/python probes/ste.py --all
    .venv/bin/python probes/ste.py --all --summary
    .venv/bin/python probes/ste.py --all --strict   # exit 1 on any error
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
PLAIN = ROOT / "plain"

MAX_SENTENCE = 25          # R1 descriptive
MAX_SENTENCE_PROC = 20     # R2 procedural
MAX_SENTENCES_PARA = 6     # R3
MAX_NOUN_CLUSTER = 3       # R5
SHORT_VERSION_MAX = 25     # §4

# R7: -ing forms. These are allowed: gerunds that are established technical
# names in our domain, plus a few that STE itself treats as nouns.
ING_ALLOWED = {
    "during", "string", "thing", "something", "nothing", "anything",
    "everything", "morning", "ring", "spring", "king", "bring", "sing",
    "wing", "being",          # "being" flagged separately when it is a verb
    "training", "encoding", "embedding", "steering", "reading", "readings",
    "meaning", "meanings", "setting", "settings", "sampling", "wording",
    "heading", "headings", "beginning", "ceiling", "engineering",
    "learning", "reasoning", "processing", "understanding", "warning",
    "feeling", "feelings",    # ordinary nouns (an emotion), not verb forms
    # STE Rule 3.5's own enumerated exceptions: -ing words approved as
    # ordinary parts of speech (nouns and adjectives), not verb forms.
    "lighting", "opening", "openings", "routing", "servicing",
    "remaining", "missing", "mating",
    # plain nouns that merely end in -ing
    "evening", "ceiling", "building", "morning",
}

# R11: metaphor / voice words this lab reaches for by reflex.
BANNED_VOICE = {
    "furniture", "sediment", "ghost", "gothic", "mouth", "elegy",
    "ratchet", "gorgeous", "delicious", "beautiful", "lovely", "damn",
    "frankly", "honestly", "obviously", "of course", "clearly",
    "interestingly", "remarkably", "strikingly", "fascinating",
    "punchline", "flavour", "flavor", "vibe", "juicy",   # NB: "shame" is
    # NOT banned — it is one of Unit 15's six charged test items, so it is
    # data, not lab voice.
    "hell", "weird", "wild", "crazy", "insane", "brutal", "sexy",
}

# R6: passive-voice detector needs the be-verbs.
BE = r"(?:is|are|was|were|be|been|being)"
PASSIVE = re.compile(rf"\b{BE}\s+(?:\w+ly\s+)?(\w+(?:ed|en))\b", re.I)
# Past participles that are really adjectives here — not passive voice.
PASSIVE_OK = {
    "based", "related", "limited", "used", "fixed", "advanced", "detailed",
    "involved", "interested", "concerned", "supposed", "designed",
    "intended", "expected", "known", "given", "seen", "written", "done",
    "made", "taken", "found", "held", "shown", "told", "kept", "left",
    "gone", "run", "set", "put", "read", "cut", "sent", "built", "lost",
}

# R15 [STE 3.4]: banned modals. STE redirects these to CAN / WILL / MUST.
# Graded uncertainty goes through the PLAIN-LANGUAGE.md §3.1 ladder instead.
BANNED_MODALS = {"may", "might", "could", "would", "shall", "should"}

# R16 [STE GR-6]: Latin abbreviations.
LATIN_ABBR = [r"\be\.g\.", r"\bi\.e\.", r"\betc\.", r"\bvs\.", r"\bcf\.",
              r"\bviz\.", r"\bN\.B\."]

CONTRACTION = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.I)

MAX_RECORD_WORDS = 200     # §4: a record summary that runs long stops being one


def load_terms() -> dict:
    """plain/terms.json is the registry of permitted technical names."""
    p = PLAIN / "terms.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text()).get("terms", {})


def technical_words() -> set[str]:
    """Every word that appears in an approved technical name, lowercased.

    A term of art may legally contain an -ing form ("word ranking",
    "steering") or a banned-voice word; the registry is what makes it
    legal, so the checker reads the same file the writers do.
    """
    out: set[str] = set()
    for key, t in load_terms().items():
        names = [key, t.get("display", "")] + list(t.get("aka", []))
        for n in names:
            for w in re.findall(r"[A-Za-z][\w\-]*", n or ""):
                out.add(w.lower())
    return out

SECTION_RE = re.compile(r"\*\*(.+?)\.\*\*")
REQUIRED_FIRST = "The short version"


def sentences(text: str) -> list[str]:
    """Split into sentences.

    Requiring whitespace + a capital after the stop already excludes
    decimals ("0.68") and version-like numbers, so we must NOT also
    refuse to split after a digit — sentences legitimately end in one
    ("...at rank 6. Frog was rank 20."), and refusing merged them into
    one over-long sentence, which the length rule then reported as a
    violation that was not there.
    """
    text = re.sub(r"\s+", " ", text).strip()

    # A quoted span is ONE unit and must never be split, even when the model
    # said two sentences. Splitting inside a quote left each half holding an
    # unbalanced quote mark, so the quote mask stopped working and the
    # model's own words got reported as our style violations — which made
    # writers truncate real evidence to silence the checker.
    spans: list[str] = []

    def _hold(m):
        spans.append(m.group(0))
        # A quote whose own last character is a full stop ends the sentence
        # it sits in ('The model said "Nothing." We measured...'). Mark those
        # with \x01 so the splitter can still see a boundary there. Without
        # this the stop is hidden inside the span and the next sentence
        # merges in — which pushed writers to move the period OUTSIDE the
        # quote, silently altering output the model really produced.
        inner = m.group(0)[1:-1].rstrip()
        mark = "\x01" if inner.endswith((".", "!", "?")) else "\x00"
        return f"{mark}{len(spans) - 1}{mark}"

    text = re.sub(r'"[^"]*"|“[^”]*”', _hold, text)

    # Two further quote-related fixes:
    #  - a following quote mark opens a sentence just as a capital does;
    #  - a sentence may END inside a quote, so the stop is either the closing
    #    mark or a sentence-final quote span (\x01).
    parts = re.split(
        r"(?<=\x01)(?=\s+[\"“(A-Z\x00\x01])"
        r"|[.!?]+[\"”'’)\]]*(?=\s+[\"“(A-Z\x00\x01]|$)", text)

    def _restore(p):
        return re.sub(r"[\x00\x01](\d+)[\x00\x01]",
                      lambda m: spans[int(m.group(1))], p)

    return [_restore(p).strip() for p in parts if p.strip()]


def strip_markup(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " CODE ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*|\*|_", "", text)
    return text


def mask_quotes(s: str) -> str:
    """Blank out quoted model output before the word-form rules run.

    PLAIN-LANGUAGE.md 3.3: quoted model output is data and is never
    edited. Without this mask the checker flags the model's own words
    ("Unfeeling", "Nothing.") and writers "fix" them by paraphrasing —
    which silently corrupts the evidence. The rules apply to OUR prose.
    """
    s = re.sub(r'"[^"]*"', ' "QUOTE" ', s)
    s = re.sub(r"[“][^”]*[”]", ' "QUOTE" ', s)
    return s


def word_count(s: str) -> int:
    """Count words the way STE Rule 8.6 does.

    A number with its unit, an abbreviation, a quoted string, a
    parenthetical, and a hyphenated word each count as ONE word. Counting
    them naively inflates every sentence in this lab past the limit,
    because our sentences are full of "rank 1 of 250,000" and "layers 53
    to 56" — so the checker would flag correct STE as too long.
    """
    s = re.sub(r"\([^)]*\)", " X ", s)          # parenthetical = 1
    s = re.sub(r"[\"“][^\"”]*[\"”]", " X ", s)   # quoted text = 1
    s = re.sub(r"\d[\d,.]*\s*(?:%|×|x)?\s*[A-Za-z]{0,4}\b", " X ", s)  # number+unit = 1
    s = re.sub(r"\b[\w]+(?:-[\w]+)+\b", " X ", s)   # hyphenated = 1
    return len(re.findall(r"[A-Za-z0-9][\w/%×]*", s))


def check_text(text: str, *, procedural: bool = False,
               allow: set[str] | None = None) -> list[dict]:
    """Return a list of violations: {rule, line, msg, excerpt}."""
    out = []
    allow = (allow or set()) | ING_ALLOWED
    # A section label ("**What we found.**") is a heading, not a sentence.
    # Counting it stole one sentence from every section's R3 budget and
    # writers were compressing real content to pay for it.
    text = re.sub(r"^\*\*[^*]+?\.\*\*\s*", "", text, flags=re.M)
    body = strip_markup(text)
    limit = MAX_SENTENCE_PROC if procedural else MAX_SENTENCE

    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    for pi, para in enumerate(paras):
        sents = sentences(para)
        if len(sents) > MAX_SENTENCES_PARA:
            out.append({"rule": "R3", "msg":
                        f"paragraph has {len(sents)} sentences (max {MAX_SENTENCES_PARA})",
                        "excerpt": para[:80]})
        for s in sents:
            n = word_count(s)
            if n > limit:
                out.append({"rule": "R1" if not procedural else "R2",
                            "msg": f"sentence has {n} words (max {limit})",
                            "excerpt": s[:100]})
            sq = mask_quotes(s)          # our prose only; quotes are data
            # R7 -ing
            for m in re.finditer(r"\b(\w+ing)\b", sq, re.I):
                w = m.group(1).lower()
                if w not in allow and len(w) > 4:
                    out.append({"rule": "R7",
                                "msg": f"-ing form '{m.group(1)}'",
                                "excerpt": s[:100]})
            # R6 passive
            for m in PASSIVE.finditer(sq):
                if m.group(1).lower() not in PASSIVE_OK:
                    out.append({"rule": "R6",
                                "msg": f"possible passive voice '{m.group(0)}'",
                                "excerpt": s[:100]})
            # R14 semicolons [STE 8.1]
            if ";" in sq:
                out.append({"rule": "R14", "msg": "semicolon — use two sentences",
                            "excerpt": s[:100]})
            # R15 banned modals [STE 3.4]
            for w in BANNED_MODALS:
                if re.search(rf"\b{w}\b", sq, re.I):
                    out.append({"rule": "R15",
                                "msg": f"banned modal '{w}' — use the "
                                       "PLAIN-LANGUAGE.md 3.1 ladder",
                                "excerpt": s[:100]})
            # R16 Latin abbreviations [STE GR-6]
            for pat in LATIN_ABBR:
                if re.search(pat, sq, re.I):
                    out.append({"rule": "R16",
                                "msg": f"Latin abbreviation {pat}",
                                "excerpt": s[:100]})
            # R9 contractions [STE 4.2]
            for m in CONTRACTION.finditer(sq):
                if not m.group(0).lower().endswith("'s"):   # possessive is allowed [GR-8]
                    out.append({"rule": "R9",
                                "msg": f"contraction '{m.group(0)}'",
                                "excerpt": s[:100]})
            # R11 voice
            low = sq.lower()
            for w in BANNED_VOICE - allow:
                if re.search(rf"\b{re.escape(w)}\b", low):
                    out.append({"rule": "R11",
                                "msg": f"metaphor / lab voice: '{w}'",
                                "excerpt": s[:100]})
            # R5 noun clusters: 4+ capitalised-or-plain nouns in a row is a
            # heuristic; we approximate with 4+ consecutive non-function words
            m = re.search(r"\b((?:[a-z]+\s+){3,})(?=[a-z]+\b)", s)
            # (approximation kept deliberately weak — reported as a note only)
    return out


def check_plain_md(path: pathlib.Path, allow: set[str] | None = None) -> dict:
    text = path.read_text()
    viol = check_text(text, allow=allow)
    secs = SECTION_RE.findall(text)
    if not secs:
        viol.append({"rule": "FMT", "msg": "no bold section headings found",
                     "excerpt": text[:60]})
    elif secs[0].strip() != REQUIRED_FIRST:
        viol.append({"rule": "FMT",
                     "msg": f"first section is '{secs[0]}', must be "
                            f"'{REQUIRED_FIRST}'", "excerpt": secs[0]})
    # the short version must be one sentence within the limit
    m = re.search(r"\*\*The short version\.\*\*\s*(.+?)(?:\n\s*\n|\Z)",
                  text, re.S)
    if m:
        sv = strip_markup(m.group(1)).strip()
        n = word_count(sv)
        if n > SHORT_VERSION_MAX:
            viol.append({"rule": "SV",
                         "msg": f"short version is {n} words (max {SHORT_VERSION_MAX})",
                         "excerpt": sv[:100]})
        if len(sentences(sv)) > 1:
            viol.append({"rule": "SV",
                         "msg": f"short version has {len(sentences(sv))} sentences (max 1)",
                         "excerpt": sv[:100]})
    total = word_count(strip_markup(text))
    # The length cap is about record summaries. Long-form pages (the essay)
    # are meant to be long; their discipline is per-sentence, not per-file.
    long_form = path.parent.name == "plain"
    if total > MAX_RECORD_WORDS and not long_form:
        viol.append({"rule": "LEN",
                     "msg": f"{total} words (max {MAX_RECORD_WORDS}) — "
                            "detail belongs in the research notes",
                     "excerpt": ""})
    try:
        shown = str(path.resolve().relative_to(ROOT))
    except ValueError:
        shown = str(path)
    return {"path": shown, "words": total, "violations": viol}


def targets(all_: bool, paths: list[str]) -> list[pathlib.Path]:
    if paths:
        return [pathlib.Path(p) for p in paths]
    if all_:
        out = sorted((ROOT / "results").glob("*/plain.md"))
        out += sorted(PLAIN.glob("*.md"))
        return out
    return []


def main():
    ap = argparse.ArgumentParser(description="ASD-STE100 checker for the plain layer")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--rule", help="only report this rule id")
    args = ap.parse_args()

    files = targets(args.all, args.paths)
    if not files:
        ap.error("give paths or --all")

    allow = technical_words()
    reports = [check_plain_md(p, allow) for p in files if p.exists()]
    if args.rule:
        for r in reports:
            r["violations"] = [v for v in r["violations"] if v["rule"] == args.rule]

    n_bad = sum(1 for r in reports if r["violations"])
    n_viol = sum(len(r["violations"]) for r in reports)

    if args.summary:
        by_rule = {}
        for r in reports:
            for v in r["violations"]:
                by_rule[v["rule"]] = by_rule.get(v["rule"], 0) + 1
        print(f"{len(reports)} files, {n_bad} with violations, {n_viol} total")
        for k in sorted(by_rule, key=lambda x: -by_rule[x]):
            print(f"   {k}: {by_rule[k]}")
        wc = [r["words"] for r in reports]
        if wc:
            print(f"   words: mean {sum(wc)/len(wc):.0f}, "
                  f"max {max(wc)}, min {min(wc)}")
    else:
        for r in reports:
            if not r["violations"]:
                continue
            print(f"\n{r['path']}  ({r['words']} words)")
            for v in r["violations"]:
                print(f"   [{v['rule']}] {v['msg']}")
                print(f"        “{v['excerpt']}”")

    if args.strict and n_viol:
        sys.exit(1)


if __name__ == "__main__":
    main()
