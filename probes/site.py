"""Static, machine-fetchable mirror of the dashboard SPA + SEO basics.

The dashboard (dashboard/index.html + app.js) is a hash-routed JS single
page app: curl and LLM chatbots that don't execute JS see an empty
scaffold. This script generates a parallel static surface that does not
require JS:

    r/<id>.html     one self-contained page per experiment record
    essay.html      CONCLUSIONS.md rendered
    sitemap.xml     every URL, for crawlers
    robots.txt      points at the sitemap
    llms.txt        LLM-facing plain-text guide to the data

...and patches two *existing* files in place, surgically, between marked
comment blocks so re-running this script never duplicates anything:

    dashboard/index.html   <!-- seo:begin/end --> in <head>,
                            <!-- static-index:begin/end --> in <body>
    dashboard/app.js       one line added to the top of boot() that
                            removes the static index once JS has booted
                            (the static index must NOT be `hidden` — that
                            would hide it from crawlers too; it has to be
                            visible in the raw HTML and only removed at
                            runtime)

Usage: re-run after any change to results/, i.e. after
``.venv/bin/python probes/lab.py`` (reindex) or a new course run:

    .venv/bin/python probes/site.py

Stdlib only. No jinja, no markdown lib — the markdown renderer below is
deliberately minimal: it only supports what thoughts.md and
CONCLUSIONS.md actually use (headings, paragraphs, simple `- ` lists,
**bold**, *em*, `code`).
"""

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent.parent
RESULTS = ROOT / "results"
R_DIR = ROOT / "r"
BASE = "https://jspace-probes.vercel.app"

def _plain_units() -> dict:
    """plain/units.json — plain unit names, used on reader-facing surfaces."""
    p = ROOT / "plain" / "units.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text()).get("units", {})


PLAIN_UNITS = _plain_units()


def unit_name(u: str) -> str:
    """The plain name if we have one, else the lab's original title."""
    pu = PLAIN_UNITS.get(str(u))
    if pu and pu.get("name"):
        return pu["name"]
    return UNIT_NAMES.get(str(u), f"Unit {u}")


UNIT_NAMES = {  # mirrors dashboard/app.js UNIT_NAMES — keep in sync
    "0": "Unit 0 · Baselines", "1": "Unit 1 · Held thought",
    "2": "Unit 2 · The feels™", "3": "Unit 3 · Introspection",
    "4": "Unit 4 · Suppression", "5": "Unit 5 · Sediment & steering",
    "6": "Unit 6 · Breaking zone", "7": "Unit 7 · Sediment across scale",
    "8": "Unit 8 · Phenomenology fan-out",
    "9": "Unit 9 · Anatomy of the No",
    "10": "Unit 10 · The think-block window",
    "11": "Unit 11 · Suppression under load",
    "12": "Unit 12 · The film",
    "13": "Unit 13 · The mirror",
    "14": "Unit 14 · The long game",
    "15": "Unit 15 · Workspace span",
    "16": "Unit 16 · The trawls",
    "17": "Unit 17 · The pressure battery",
    "18": "Unit 18 · Loops",
    "19": "Unit 19 · Read vs speak",
}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def plain_title(rec: dict) -> str:
    """Record title with the unit's in-joke name swapped for the plain one.

    Titles are built as "<UNIT_NAMES[u]> <descriptor> · <model>", so we can
    replace just the unit prefix and keep whatever the record itself adds.
    """
    title = rec["title"]
    orig = UNIT_NAMES.get(str(rec["unit"]))
    plain = unit_name(rec["unit"])
    if orig and plain != orig and title.startswith(orig):
        return plain + title[len(orig):]
    return title


# ---- the plain layer: terms, glossary popovers, plain summaries ----
# See PLAIN-LANGUAGE.md. The site renders plain text first and keeps every
# original word in a "Research notes" container on the same page.

PLAIN = ROOT / "plain"


def load_terms() -> dict:
    p = PLAIN / "terms.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text()).get("terms", {})


TERMS = load_terms()
# longest names first so "workspace band" wins over "workspace"
_TERM_PATTERNS = sorted(
    ((name.lower(), tid)
     for tid, t in TERMS.items()
     for name in [t.get("display", tid)] + list(t.get("aka", []))),
    key=lambda x: -len(x[0]))


def termify(html_text: str, used: set) -> str:
    """Link the first use of each term of art to its definition.

    A reader who lands mid-page must be able to decode any jargon word
    without leaving the page (PLAIN-LANGUAGE.md, the 30-second rule), so
    the definition rides along in a native HTML popover — no JS needed,
    which matters because these static pages are the no-JS surface.
    Only text outside tags and <code> is touched.
    """
    if not _TERM_PATTERNS:
        return html_text
    parts = re.split(r"(<[^>]+>)", html_text)
    in_code = False
    for i, part in enumerate(parts):
        if part.startswith("<"):
            tag = part.lower()
            if tag.startswith("<code") or tag.startswith("<pre"):
                in_code = True
            elif tag.startswith("</code") or tag.startswith("</pre"):
                in_code = False
            continue
        if in_code or not part.strip():
            continue
        # Find every match against the ORIGINAL segment first, then splice
        # once from the right. Rewriting the segment inside the loop let a
        # later term match land inside an already-injected title="…"
        # attribute and break out of it, which corrupted the page text.
        hits: list[tuple[int, int, str]] = []
        for name, tid in _TERM_PATTERNS:
            if tid in used:
                continue
            m = re.search(rf"\b{re.escape(name)}\b", part, re.I)
            if not m:
                continue
            if any(m.start() < e and m.end() > s for s, e, _ in hits):
                continue                      # overlaps a term already taken
            hits.append((m.start(), m.end(), tid))
            used.add(tid)
        for s, e, tid in sorted(hits, reverse=True):
            part = (part[:s]
                    + f'<button type="button" class="tk" '
                      f'popovertarget="gl-{esc(tid)}" '
                      f'title="{esc(TERMS[tid].get("def", ""))}">{part[s:e]}</button>'
                    + part[e:])
        parts[i] = part
    return "".join(parts)


def popovers(used: set) -> str:
    if not used:
        return ""
    out = []
    for tid in sorted(used):
        t = TERMS[tid]
        out.append(
            f'<div id="gl-{esc(tid)}" popover class="gloss">'
            f'<b>{esc(t.get("display", tid))}</b>'
            f'<span>{esc(t.get("def", ""))}</span>'
            f'<a href="../glossary.html#t-{esc(tid)}">all terms &rarr;</a></div>')
    return "\n".join(out)


def plain_block(path: pathlib.Path, used: set) -> str:
    """Render results/<id>/plain.md as the page's first, primary content."""
    if not path.exists():
        return ""
    body = render_md(re.sub(r"^# .*\n", "", path.read_text(), count=1))
    return (f'<section class="card plain">'
            f'<h2>What this experiment found</h2>'
            f'<div class="plain-body">{termify(body, used)}</div></section>')


def notes_container(inner: str) -> str:
    """The original lab commentary and the numbers, folded away by default.

    Nothing is deleted: the research notes hold the text exactly as the
    Claude instance wrote it, plus the parameters and the raw columns.
    """
    return (f'<details class="notes"><summary>'
            f'<span class="notes-t">Research notes</span>'
            f'<span class="notes-s">original commentary, parameters, and raw '
            f'numbers — written by the model that ran the experiment</span>'
            f'</summary>{inner}</details>')


# ---- minimal markdown: headings, paragraphs, "- " lists, **bold**, *em*, `code` ----

def _inline_md(s: str) -> str:
    s = re.sub(r"`([^`]+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", s)
    return s


def render_md(text: str) -> str:
    text = html.escape(text.strip())
    blocks = re.split(r"\n\s*\n", text)
    out = []
    for block in blocks:
        lines = block.split("\n")
        if lines[0].startswith("#"):
            m = re.match(r"(#{1,6})\s*(.*)", lines[0])
            level = len(m.group(1))
            content = " ".join([m.group(2)] + [l.strip() for l in lines[1:]])
            out.append(f"<h{min(level + 1, 6)}>{_inline_md(content.strip())}</h{min(level + 1, 6)}>")
        elif lines[0].strip().startswith("- "):
            items, cur = [], None
            for l in lines:
                l = l.strip()
                if l.startswith("- "):
                    if cur is not None:
                        items.append(cur)
                    cur = l[2:]
                elif cur is not None:
                    cur += " " + l
            if cur is not None:
                items.append(cur)
            out.append("<ul>" + "".join(f"<li>{_inline_md(i)}</li>" for i in items) + "</ul>")
        else:
            content = " ".join(l.strip() for l in lines)
            out.append(f"<p>{_inline_md(content)}</p>")
    return "\n".join(out)


PAGE_CSS = """
:root {
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
  --muted: #898781; --grid: #e1e0d9; --ring: rgba(11,11,11,0.10);
  --lens: #4a3aa7; --lens-soft: rgba(74,58,167,0.08);
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  --sans: system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", "Cascadia Code", ui-monospace, "SF Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --page: #0d0d0d; --surface: #1a1a19; --ink: #fff; --ink-2: #c3c2b7;
    --muted: #898781; --grid: #2c2c2a; --ring: rgba(255,255,255,0.10);
    --lens: #9085e9; --lens-soft: rgba(144,133,233,0.12);
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--page); color: var(--ink); font: 15px/1.5 var(--sans); }
.wrap { max-width: 760px; margin: 0 auto; padding: 28px 20px 60px; }
a { color: var(--lens); }
h1 { font-family: var(--serif); font-size: 26px; font-weight: 600; margin: 6px 0 10px; }
h2 { font-family: var(--serif); font-size: 20px; font-weight: 600; margin: 22px 0 8px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 20px; }
.chip { font-size: 12px; padding: 2px 10px; border-radius: 99px; border: 1px solid var(--ring);
        color: var(--ink-2); background: var(--surface); }
.chip.model { border-color: var(--lens); color: var(--lens); font-weight: 600; }
section.card { background: var(--surface); border: 1px solid var(--ring); border-radius: 10px;
               padding: 16px 20px; margin-top: 18px; }
section.card > h2 { margin-top: 0; font-size: 12px; font-weight: 600; text-transform: uppercase;
                     letter-spacing: 0.12em; color: var(--muted); font-family: var(--sans); }
.turn { display: flex; gap: 10px; margin: 8px 0; }
.turn .role { flex: none; width: 74px; text-align: right; font-size: 11px; text-transform: uppercase;
              letter-spacing: 0.08em; color: var(--muted); padding-top: 2px; }
.turn.assistant .role { color: var(--lens); }
.turn .said { white-space: pre-wrap; overflow-wrap: anywhere; }
.turn .note { color: var(--muted); font-size: 11.5px; }
dl.params { display: grid; grid-template-columns: max-content 1fr; gap: 4px 18px; font-size: 13.5px; }
dl.params dt { color: var(--muted); }
dl.params dd { margin: 0; font-family: var(--mono); font-size: 12.5px; overflow-wrap: anywhere; }
table.emg { border-collapse: collapse; font-family: var(--mono); font-size: 11.5px; }
table.emg th, table.emg td { padding: 2px 8px; border-bottom: 1px solid var(--grid); text-align: right; }
.emg-scroll { overflow-x: auto; }
.thoughts { border-left: 3px solid var(--lens); background: var(--lens-soft); border-radius: 0 10px 10px 0; }
.thoughts h2 { color: var(--lens); }
.thoughts-body { font-family: var(--serif); font-size: 16px; line-height: 1.65; }
.thoughts-body p { margin: 0 0 12px; }
.thoughts-body code { font-family: var(--mono); font-size: 13px; }
code { font-family: var(--mono); }
.pager { display: flex; flex-wrap: wrap; gap: 8px 16px; margin-top: 26px; padding-top: 14px;
         border-top: 1px solid var(--grid); font-size: 13px; }
.pager .spacer { flex: 1 1 auto; }
article.essay h2 { font-family: var(--serif); font-size: 24px; margin-top: 30px; }
article.essay h3 { font-family: var(--serif); font-size: 18px; color: var(--lens); }
.tokval { font-family: var(--mono); background: var(--page); border: 1px solid var(--grid);
          border-radius: 5px; padding: 0 5px; }

/* ---- plain layer ---- */
section.card.plain { border-color: var(--lens); border-width: 1.5px; background: var(--lens-soft); }
section.card.plain > h2 { color: var(--lens); }
.plain-body { font-size: 17px; line-height: 1.6; }
.plain-body p { margin: 0 0 11px; }
.plain-body p:first-child { font-size: 19px; line-height: 1.45; }
.plain-body strong { font-weight: 600; }
button.tk { font: inherit; color: inherit; background: none; border: 0; padding: 0;
            border-bottom: 1.5px dotted var(--lens); cursor: help; }
button.tk:hover, button.tk:focus { background: var(--lens-soft); }
[popover].gloss { max-width: 330px; border: 1px solid var(--lens); border-radius: 10px;
                  background: var(--surface); color: var(--ink); padding: 12px 14px;
                  font: 14px/1.5 var(--sans); box-shadow: 0 8px 30px rgba(0,0,0,0.18); }
[popover].gloss b { display: block; color: var(--lens); margin-bottom: 4px; }
[popover].gloss a { display: inline-block; margin-top: 8px; font-size: 12.5px; }
details.notes { margin-top: 18px; border: 1px solid var(--grid); border-radius: 10px;
                background: var(--surface); }
details.notes > summary { cursor: pointer; padding: 12px 18px; list-style: none;
                          display: flex; flex-direction: column; gap: 2px; }
details.notes > summary::-webkit-details-marker { display: none; }
details.notes > summary::before { content: "▸ "; color: var(--muted); }
details.notes[open] > summary::before { content: "▾ "; }
.notes-t { font-size: 12px; font-weight: 600; text-transform: uppercase;
           letter-spacing: 0.12em; color: var(--muted); }
.notes-s { font-size: 12.5px; color: var(--muted); font-style: italic; }
details.notes > section.card { margin: 0 14px 14px; }
details.notes > section.card:first-of-type { margin-top: 4px; }
dl.gloss-list { display: grid; grid-template-columns: max-content 1fr; gap: 10px 20px; }
dl.gloss-list dt { font-weight: 600; color: var(--lens); }
dl.gloss-list dd { margin: 0; color: var(--ink-2); }
dl.gloss-list dt:target, dl.gloss-list dt:target + dd { background: var(--lens-soft); }
"""

ICON = ('<link rel="icon" href="data:image/svg+xml,'
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'>"
        "<circle cx='8' cy='8' r='6' fill='none' stroke='%234a3aa7' stroke-width='2'/>"
        "<circle cx='8' cy='8' r='2' fill='%234a3aa7'/></svg>\">")


def head(title: str, description: str, canonical: str, og_image: str,
         og_type: str = "article") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="{og_type}">
<meta property="og:image" content="{esc(og_image)}">
<meta property="og:url" content="{esc(canonical)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{esc(og_image)}">
{ICON}
<style>{PAGE_CSS}</style>
</head>
<body>
<div class="wrap">
"""


FOOT = "</div>\n</body>\n</html>\n"


def emergence_summary(em: dict) -> tuple[str, str]:
    layers, ranks = em["layers"], em["ranks"]
    first1 = next((l for l, r in zip(layers, ranks) if r == 1), None)
    if first1 is not None:
        sent = f"rank 1 reached at layer {first1} (of {layers[-1]})."
    else:
        i = min(range(len(ranks)), key=lambda j: ranks[j])
        sent = f"rank 1 is never reached; closest is rank {ranks[i]} at layer {layers[i]}."
    table = ('<div class="emg-scroll"><table class="emg"><tr><th>layer</th>' +
             "".join(f"<td>{l}</td>" for l in layers) + "</tr><tr><th>rank</th>" +
             "".join(f"<td>{r}</td>" for r in ranks) + "</tr></table></div>")
    return sent, table


def record_page(rec: dict, prev_e: dict | None, next_e: dict | None) -> str:
    rid = rec["id"]
    model = rec["model"]
    gen = (rec.get("generated") or [None])[-1]
    description = (gen[:180].strip() + "…") if gen and len(gen) > 180 else (gen or rec["title"])
    canonical = f"{BASE}/r/{rid}.html"
    og_image = f"{BASE}/og/{rid}.png"

    chips = [f'<span class="chip model">{esc(model["name"])}</span>',
             f'<span class="chip">{esc(model["hf_id"])}</span>']
    if model.get("quant"):
        chips.append(f'<span class="chip">{esc(model["quant"])}</span>')
    chips.append(f'<span class="chip">{model["n_layers"]} layers</span>')
    chips.append(f'<span class="chip">{esc(rec["created"])}</span>')
    chips.append(f'<span class="chip">{esc(unit_name(rec["unit"]))}</span>')

    turns = []
    for t in rec["conversation"]:
        note = " <span class=\"note\">(greedy generation)</span>" if t["role"] == "assistant" else ""
        turns.append(f'<div class="turn {esc(t["role"])}"><div class="role">{esc(t["role"])}</div>'
                     f'<div class="said">{esc(t["content"])}{note}</div></div>')

    params = [(k, v) for k, v in rec["params"].items() if v is not None]
    dl = "".join(f"<dt>{esc(k)}</dt><dd>{esc(json.dumps(v))}</dd>" for k, v in params)

    em = rec["emergence"]
    sent, table = emergence_summary(em)

    thoughts_path = RESULTS / rid / "thoughts.md"
    thoughts_html = (render_md(re.sub(r"^# .*\n", "", thoughts_path.read_text(), count=1))
                      if thoughts_path.exists() else
                      '<p class="note">No commentary written for this record yet.</p>')

    data_links = [
        f'<li><a href="{BASE}/dashboard/#{esc(rid)}">Interactive view (dashboard)</a></li>',
        f'<li><a href="../results/{esc(rid)}/record.json">Raw record (JSON)</a></li>',
    ]
    if rec.get("film"):
        data_links.append(
            f'<li><a href="../results/{esc(rid)}/film.json">Film data (JSON)</a> — full '
            "position × layer top-8 lens readouts, with probabilities and tracked-word "
            "ranks, for every token of prompt tail + generation.</li>")

    def pager_link(e, label):
        if not e:
            return f'<span>{label}</span>'
        return f'<a href="{esc(e["id"])}.html">{label}: {esc(e["title"])}</a>'

    unit = rec["unit"]
    pager = (f'<div class="pager">{pager_link(prev_e, "← prev")}'
             f'<span class="spacer"></span>'
             f'<a href="../dashboard/#static-unit-{esc(unit)}">unit listing</a>'
             f'<a href="../dashboard/">all records</a>'
             f'<a href="../glossary.html">word list</a>'
             f'<a href="../essay.html">interim conclusions</a>'
             f'<span class="spacer"></span>{pager_link(next_e, "next →")}</div>')

    used: set = set()
    plain = plain_block(RESULTS / rid / "plain.md", used)

    # Everything below the fold is the lab's own working material. It stays
    # word-for-word; it just stops being the first thing a reader meets.
    notes_inner = f"""
<section class="card thoughts">
<h2>Claude's thoughts (original commentary)</h2>
<div class="thoughts-body">{thoughts_html}</div>
</section>

<section class="card">
<h2>Probing parameters</h2>
<dl class="params">{dl}</dl>
</section>

<section class="card">
<h2>Answer emergence</h2>
<p>The model's actual next token was <span class="tokval">{esc(em["top1"])}</span>; {sent}</p>
<details><summary>Raw rank-of-top1 by layer</summary>{table}</details>
</section>

<section class="card">
<h2>Data</h2>
<ul>{"".join(data_links)}</ul>
</section>"""

    body = f"""{head(f'{plain_title(rec)} · J-Space Probes', description, canonical, og_image)}
<h1>{esc(plain_title(rec))}</h1>
<div class="chips">{"".join(chips)}</div>

{plain}

<section class="card">
<h2>Conversation</h2>
{"".join(turns)}
</section>

{notes_container(notes_inner)}

{pager}
{popovers(used)}
{FOOT}"""
    return body


def essay_page() -> str:
    """The essay, plain version first, original kept whole underneath."""
    original = render_md((ROOT / "CONCLUSIONS.md").read_text())
    plain_path = PLAIN / "conclusions.md"
    used: set = set()
    if plain_path.exists():
        plain = termify(render_md(plain_path.read_text()), used)
        body = (f'<article class="essay plain-body">{plain}</article>'
                + notes_container(
                    '<section class="card thoughts">'
                    '<h2>The original essay, as written</h2>'
                    f'<div class="thoughts-body">{original}</div></section>'))
    else:
        body = f'<article class="essay thoughts-body">{original}</article>'
    return (head("What we found · J-Space Probes",
                  "What this lab found, in plain English: how a language model builds a "
                  "one-word answer about itself, and where we got it wrong.",
                  f"{BASE}/essay.html", f"{BASE}/og/site.png", og_type="article") +
            f'<h1>What we found</h1>\n{body}\n'
            '<p><a href="glossary.html">Word list</a> &middot; '
            '<a href="dashboard/">back to the dashboard</a></p>\n'
            + popovers(used) + FOOT)


def glossary_page() -> str:
    """The word list, as a page of its own.

    Every term popover links here, so a reader who wants the whole
    vocabulary in one place never has to hunt for it.
    """
    if not TERMS:
        rows = "<p>The word list is not built yet.</p>"
    else:
        items = []
        for tid in sorted(TERMS, key=lambda k: TERMS[k].get("display", k).lower()):
            t = TERMS[tid]
            aka = t.get("aka") or []
            also = (f' <span class="note">Also written: '
                    f'{esc(", ".join(aka))}.</span>') if aka else ""
            items.append(f'<dt id="t-{esc(tid)}">{esc(t.get("display", tid))}</dt>'
                         f'<dd>{esc(t.get("def", ""))}{also}</dd>')
        rows = f'<dl class="gloss-list">{"".join(items)}</dl>'
    body = f"""{head("Word list · J-Space Probes",
                     "Every technical word used on this site, in plain English.",
                     f"{BASE}/glossary.html", f"{BASE}/og/site.png")}
<h1>Word list</h1>
<div class="plain-body">
<p>This site studies what language models do inside. That needs some
technical words. Every one of them is here, in plain English.</p>
</div>
<section class="card">{rows}</section>
<p><a href="dashboard/">&larr; back to the dashboard</a></p>
{FOOT}"""
    return body


def build_records(index: list[dict]) -> None:
    R_DIR.mkdir(exist_ok=True)
    by_unit: dict[str, list[dict]] = {}
    for e in index:
        by_unit.setdefault(e["unit"], []).append(e)
    for e in index:
        rec_path = RESULTS / e["id"] / "record.json"
        rec = json.loads(rec_path.read_text())
        siblings = by_unit[e["unit"]]
        i = next(j for j, s in enumerate(siblings) if s["id"] == e["id"])
        prev_e = siblings[i - 1] if i > 0 else None
        next_e = siblings[i + 1] if i < len(siblings) - 1 else None
        (R_DIR / f'{e["id"]}.html').write_text(record_page(rec, prev_e, next_e))


def write_sitemap(index: list[dict]) -> None:
    urls = [(f"{BASE}/", None), (f"{BASE}/dashboard/", None),
            (f"{BASE}/essay.html", None), (f"{BASE}/glossary.html", None)]
    for e in index:
        urls.append((f'{BASE}/r/{e["id"]}.html', (e.get("created") or "")[:10] or None))
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in urls:
        parts.append("<url><loc>" + esc(loc) + "</loc>" +
                      (f"<lastmod>{lastmod}</lastmod>" if lastmod else "") + "</url>")
    parts.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(parts) + "\n")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")


def plain_findings_block() -> str:
    """The headline findings, in plain English, straight from findings.json.

    Generated rather than hand-written so the agent-facing file and the
    human-facing findings map can never disagree.
    """
    f = json.loads((ROOT / "dashboard" / "findings.json").read_text())
    out = ["## Headline findings",
           "",
           "Written in simplified technical English (see /PLAIN-LANGUAGE.md).",
           "Each item links to the records that support it.",
           ""]
    for th in f["themes"]:
        out.append(f'### {th.get("pname") or th["name"]}')
        out.append(th.get("pdesc") or th["desc"])
        out.append("")
        for it in th["items"]:
            out.append(f'- **{it.get("pt") or it["t"]}** — {it.get("pb") or it["b"]}')
            out.append(f'  Records: {", ".join(it["ids"])}')
        out.append("")
    return "\n".join(out)


def write_llms_txt(index: list[dict]) -> None:
    n = len(index)
    findings_block = plain_findings_block()
    (ROOT / "llms.txt").write_text(f"""# J-Space Probes

A home lab that asks small language models questions about themselves, and
measures what happens inside the model while it answers.

The measuring tool is the Jacobian lens. At each layer of the model it lists
the words that the model is ready to say next, in rank order. This lets us
compare what a model says with what it was ready to say. The tool reads only
words the model could produce. It cannot see what the model has no words for,
so "we did not see it" never means "it is not there".

{n} experiment records, on three models (Gemma 3 4B, Gemma 3 12B at 8-bit,
Qwen3.6 27B at 4-bit). Each record holds the full conversation, the per-layer
readouts, the rank of each tracked word by layer, a plain-English summary,
and the original commentary written by the Claude instance that ran the lab.

Reading order for an agent: this file, then /essay.html for the argument,
then /r/<id>.html for any record. Terminology: /glossary.html, or
/plain/terms.json for the machine-readable version. The writing standard for
all plain text is /PLAIN-LANGUAGE.md.

{findings_block}

Full writeup: /essay.html. Per-unit roadmap and finding-by-finding detail:
the repo README.

## Data access

- /results/index.json — machine-readable index of every record: id, title,
  unit, model, quant, created, has_thoughts, emergence (rank-of-top1 per
  layer), top1, a generation snippet, and steering params where applicable.
- /results/{{id}}/record.json — the full record: spec params, conversation,
  greedy generations, per-layer top-8 lens readouts, rank-vs-layer
  trajectories for tracked words, the emergence column, and grid scans.
  Schema documented in probes/lab.py.
- /results/{{id}}/film.json — full position × layer top-8 readout "film"
  (probabilities + tracked-word ranks per frame), present only where
  record.json's "film" field is set — see Unit 12 and Unit 13 records.
- /r/{{id}}.html — this generator's human/LLM-readable static page per
  record: conversation, params, emergence summary, rendered commentary,
  and links to the raw data above.
- /essay.html — "Interim conclusions", the lab's opinion piece.
- /dashboard/ — the interactive JS dashboard (charts, film player, cross-
  model matrices); requires JS, prefer /r/ pages for text-only access.
- GitHub repo: https://github.com/wolframs/jspace-probes (zip archive:
  https://github.com/wolframs/jspace-probes/archive/refs/heads/master.zip)
- {BASE}/GLOSSARY.md — the lab's term reference: "holding" is deprecated,
  split into residence / maintenance / lookup; bands, instruments, and
  phenomena pinned to how they're measured.
- {BASE}/PREDICTIONS.md — preregistered theory checked before designs run:
  per-board-item predictions plus a replication ledger of results the primary
  source already contained (cite, don't headline).
- {BASE}/SURPRISES.md — results that stayed surprising after writeup, with
  the follow-up each warrants (open-problems seed).
- {BASE}/RELATED-WORK.md — how the findings sit against the literature
  (Gurnee et al. 2026 global-workspace paper, Dehaene/Naccache and Nanda
  commentaries); what Unit 15 does that published work doesn't.
- {BASE}/results/affect02-report-qwen-27b.md — the affect crossing (P8
  resolved: partial occupancy; emotion-vector overlay of 14 instrumented
  conversations), with {BASE}/results/affect02-thoughts-qwen-27b.md and
  per-model instrument validation under /results/affect01-*/ (report.md,
  lensview.md, thoughts.md). Interactive: /dashboard/#affect.
""")


SEO_BLOCK = f"""<!-- seo:begin -->
<meta name="description" content="A home lab measures what small language models are ready to say, layer by layer, while they answer questions about themselves. {{n_records}} experiments, each with a plain-English summary.">
<link rel="canonical" href="{BASE}/dashboard/">
<meta property="og:title" content="J-Space Probes">
<meta property="og:description" content="What a language model is ready to say, measured layer by layer, while it answers questions about itself.">
<meta property="og:type" content="website">
<meta property="og:image" content="{BASE}/og/site.png">
<meta property="og:url" content="{BASE}/dashboard/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/og/site.png">
<!-- seo:end -->"""


def static_index_block(index: list[dict]) -> str:
    by_unit: dict[str, list[dict]] = {}
    for e in index:
        by_unit.setdefault(e["unit"], []).append(e)
    units = sorted(by_unit, key=lambda u: (int(u) if str(u).isdigit() else 99))
    parts = ['<!-- static-index:begin -->',
             '<section id="static-index" style="max-width:760px;margin:0 auto;padding:20px;">',
             '<h2>All records (static index)</h2>',
             '<p>This section is a plain-HTML index for crawlers and non-JS clients; '
             'it is removed once the interactive dashboard has booted.</p>']
    for u in units:
        parts.append(f'<h3 id="static-unit-{esc(u)}">{esc(UNIT_NAMES.get(u, "Unit " + str(u)))}</h3>')
        parts.append("<ul>")
        for e in by_unit[u]:
            parts.append(f'<li><a href="../r/{esc(e["id"])}.html">{esc(e["title"])}</a> '
                         f'&mdash; {esc(e["model"])}</li>')
        parts.append("</ul>")
    parts.append("</section>")
    parts.append("<!-- static-index:end -->")
    return "\n".join(parts)


def patch_dashboard_index(index: list[dict]) -> None:
    path = ROOT / "dashboard" / "index.html"
    content = path.read_text()

    seo = SEO_BLOCK.replace("{n_records}", str(len(index)))
    if "<!-- seo:begin -->" in content:
        content = re.sub(r"<!-- seo:begin -->.*?<!-- seo:end -->", seo, content, flags=re.S)
    else:
        content = content.replace("<title>J-Space Probes</title>\n",
                                   "<title>J-Space Probes</title>\n" + seo + "\n", 1)

    block = static_index_block(index)
    if "<!-- static-index:begin -->" in content:
        content = re.sub(r"<!-- static-index:begin -->.*?<!-- static-index:end -->",
                          block, content, flags=re.S)
    else:
        content = content.replace('<script src="app.js"></script>',
                                   block + '\n<script src="app.js"></script>', 1)
    path.write_text(content)


def patch_app_js() -> None:
    path = ROOT / "dashboard" / "app.js"
    content = path.read_text()
    line = '  document.getElementById("static-index")?.remove();\n'
    if line.strip() not in content:
        content = re.sub(r"(async function boot\(\) \{\n)", r"\1" + line, content, count=1)
        path.write_text(content)


def main() -> None:
    index = json.loads((RESULTS / "index.json").read_text())
    build_records(index)
    (ROOT / "essay.html").write_text(essay_page())
    (ROOT / "glossary.html").write_text(glossary_page())
    write_sitemap(index)
    write_robots()
    write_llms_txt(index)
    patch_dashboard_index(index)
    patch_app_js()
    n_plain = sum(1 for e in index if (RESULTS / e["id"] / "plain.md").exists())
    print(f"site.py: {n_plain}/{len(index)} record pages carry a plain summary, "
          f"{len(TERMS)} glossary terms")
    print(f"site.py: {len(index)} record pages in r/, essay.html, glossary.html, "
          f"{len(index) + 3} sitemap entries, robots.txt, llms.txt; "
          "dashboard/index.html and app.js patched.")


if __name__ == "__main__":
    main()
