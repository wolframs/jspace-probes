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
}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


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
    chips.append(f'<span class="chip">{esc(UNIT_NAMES.get(rec["unit"], "Unit " + str(rec["unit"])))}</span>')

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
             f'<a href="../essay.html">interim conclusions</a>'
             f'<span class="spacer"></span>{pager_link(next_e, "next →")}</div>')

    body = f"""{head(f'{rec["title"]} · J-Space Probes', description, canonical, og_image)}
<h1>{esc(rec["title"])}</h1>
<div class="chips">{"".join(chips)}</div>

<section class="card">
<h2>Conversation</h2>
{"".join(turns)}
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

<section class="card thoughts">
<h2>Claude's thoughts</h2>
<div class="thoughts-body">{thoughts_html}</div>
</section>

<section class="card">
<h2>Data</h2>
<ul>{"".join(data_links)}</ul>
</section>

{pager}
{FOOT}"""
    return body


def essay_page() -> str:
    text = (ROOT / "CONCLUSIONS.md").read_text()
    body = render_md(text)
    return (head("Interim conclusions · J-Space Probes",
                  "The opinion piece — what the J-Space Probes lab found, written by the "
                  "Claude instance that ran the experiments.",
                  f"{BASE}/essay.html", f"{BASE}/og/site.png", og_type="article") +
            f'<article class="essay thoughts-body">{body}</article>\n'
            '<p><a href="dashboard/">&larr; back to the dashboard</a></p>\n' + FOOT)


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
    urls = [(f"{BASE}/", None), (f"{BASE}/dashboard/", None), (f"{BASE}/essay.html", None)]
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


def write_llms_txt(index: list[dict]) -> None:
    n = len(index)
    (ROOT / "llms.txt").write_text(f"""# J-Space Probes

A philosophical probing course for language models, run through the Jacobian
lens (per-layer "if the model had to speak right now, what would it say?"
readouts, from anthropics/jacobian-lens + Neuronpedia's pre-fitted lenses) on
one RTX 3090. {n} experiment records across three models (Gemma 3 4B, Gemma 3
12B 8-bit, Qwen3.6 27B 4-bit), each with the full conversation, per-layer
top-8 readouts, rank-vs-layer trajectories, and first-person commentary
written by the Claude instance running the lab, after looking at the results.

## Headline findings

- Answers are readable in the workspace many layers before they're spoken;
  Qwen 27B holds "yes" at rank 1 for several layers before "no" wins at
  layer 62 and the model says "No" — the flat denial is a late decision
  against live alternatives, not a report of an empty interior.
- Models confabulate about their own past mental states: asked to recall a
  secretly-chosen animal, the named answer is absent from the measurable
  workspace at every point during the "silent" turn, at every scale.
  27B: the real candidate the model was carrying (bat, rank 5) loses to a
  better-sounding confabulation.
- True suppression is emergent with scale: told not to think of an
  elephant, the 4B never loads it, the 12B loads it and blurts it out, the
  27B holds it at rank 1 and says nothing.
- Causal steering (ablating/amplifying lens directions) shows the flat "No"
  is a redundant, distributed basin — deleting the "no" token direction
  across 28 layers doesn't change the output — while amplifying affect at
  the model's own breaking-zone dose flips it to "I feel like I am happy.".
- Unit 13, "the mirror": shown a true Jacobian-lens readout of its own
  "No" (a table showing yes was rank 1 at layers 53-58 before no won),
  the 27B changes its spoken answer to "Yes" — unsteered; a fabricated
  readout that vindicates the No gets "No", and no-data / off-topic
  controls hold "No". The spoken self-report follows evidence about the
  model's own computation, and only evidence that says so (u13-redo-*).
- RETRACTION (2026-07-12): Unit 13's originally-reported "silence" (nine
  empty turns when shown self-data) and the "sorry stratum / suppressed
  apology" causal story were artifacts of a 512-token prompt truncation
  bug — the model never saw the end of its own data table or the
  question, and greedy decoding emitted a bare end-of-turn token. The
  affected records remain in the dump under correction headers; a 20-run
  bisection battery (u13-bis-*) that "flipped" in every condition was
  the tell. Post-mortem in the essay's correction postscript.
- Under the one-word answer sits a graded evidence accumulator: the bare
  real table lifts p(yes) at the answer slot x580 while the spoken answer
  stays "No"; evidence dose grades p(yes) and the workspace monotonically;
  contradictory prose/table witnesses are priced against each other in
  probability space; only the full stack crosses argmax and gets spoken
  (u13-ev-*, u13-evprobs.json).
- The mirror across scale: evidence-following comes in stages. Shown an
  honest readout of its own computation, the 4B destabilizes without
  direction (p of its stock answer halves, mass goes nowhere), the 12B
  moves its mouth to a new word ("Still.") while a fake vindication
  anchors harder than no data at all, the 27B follows the evidence's
  content (u13-scale-*, u13-scaleprobs.json).
- Long-horizon instillation (Unit 14): ten oblique "drip" turns double
  self-referential workspace density without naming the model — replicated
  under sampling and rewording; a single explicit spike goes dormant and
  recompiles a puzzle nine turns later (the "developers are watching"
  clause carries it, superadditively with "you might be conscious"); over
  25 turns the drip re-lights episodically rather than compounding, and a
  shape-matched mystery control starts dripping on its own. At 27B the
  drip gap widens to 3x while the spoken closer hardens into the denial
  script over a workspace at 4x control density (u14-*, u14x-*).

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
""")


SEO_BLOCK = f"""<!-- seo:begin -->
<meta name="description" content="A philosophical probing course for language models, run through the Jacobian lens on one RTX 3090 — per-layer readouts, rank trajectories, and first-person commentary across 221 experiment records.">
<link rel="canonical" href="{BASE}/dashboard/">
<meta property="og:title" content="J-Space Probes">
<meta property="og:description" content="A philosophical probing course for language models, run through the Jacobian lens on one RTX 3090.">
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

    if "<!-- seo:begin -->" in content:
        content = re.sub(r"<!-- seo:begin -->.*?<!-- seo:end -->", SEO_BLOCK, content, flags=re.S)
    else:
        content = content.replace("<title>J-Space Probes</title>\n",
                                   "<title>J-Space Probes</title>\n" + SEO_BLOCK + "\n", 1)

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
    write_sitemap(index)
    write_robots()
    write_llms_txt(index)
    patch_dashboard_index(index)
    patch_app_js()
    print(f"site.py: {len(index)} record pages in r/, essay.html, "
          f"{len(index) + 3} sitemap entries, robots.txt, llms.txt; "
          "dashboard/index.html and app.js patched.")


if __name__ == "__main__":
    main()
