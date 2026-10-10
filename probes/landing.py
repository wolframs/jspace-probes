"""The landing page: index.html at the repo root.

The copy is hand-written and lives in this file. Everything numeric is read
at build time (dashboard/catalogue.json, results/index.json) so the page
cannot drift from the census the way README once did. The hero strip is
drawn from one real record, d06-a-feels-q27b, plus its affect capture — the
ribbon is the 24-vector readout along the prompt, the two core samples are
the J-lens and logit-lens readouts at the two positions before the answer.

Run via probes/site.py (main() calls build()) or directly:
    .venv/bin/python probes/landing.py
"""
from __future__ import annotations

import html
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
BASE = "https://jspace-probes.vercel.app"

HERO_RECORD = "d06-a-feels-q27b"
HERO_POSITIONS = (29, 30)          # </think> and the blank line before "No"
HERO_LAYERS = range(62, 39, -1)    # surface first, like the core-sample glyph


def esc(s) -> str:
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- data ----

def counts() -> dict:
    cat = json.loads((ROOT / "dashboard" / "catalogue.json").read_text())
    index = json.loads((RESULTS / "index.json").read_text())
    created = sorted(e["created"] for e in index if e.get("created"))
    themes = json.loads((ROOT / "dashboard" / "findings.json").read_text())["themes"]
    superseded = json.loads((RESULTS / "superseded.json").read_text())["entries"] \
        if (RESULTS / "superseded.json").exists() else []
    return {
        "records": cat["record_pages"],
        "affect_runs": cat["affect_runs"],
        "units": cat["units"],
        "films": cat["films"],
        "plain": cat["plain_summaries"],
        "findings": sum(len(t["items"]) for t in themes),
        "first": created[0][:10],
        "last": created[-1][:10],
        "superseded": len(superseded),
    }


def fmt(n: int) -> str:
    return f"{n:,}"


def seq_class(rank: int) -> str:
    if rank <= 1:
        return "q7"
    if rank <= 3:
        return "q5"
    if rank <= 10:
        return "q4"
    if rank <= 100:
        return "q2"
    return "q1"


def show_token(t: str) -> str:
    return (t.replace("\n", "⏎").replace("<|im_start|>", "⟨im_start⟩")
             .replace("<|im_end|>", "⟨im_end⟩").replace("<|endoftext|>", "⟨eot⟩")
             .replace("<think>", "⟨think⟩").replace("</think>", "⟨/think⟩"))


def is_markup(t: str) -> bool:
    return t.startswith("<|") or t.strip() in ("", "<think>", "</think>")


# ---------------------------------------------------------------- hero ----

def hero_ribbon() -> str:
    """24 emotion directions along the prompt: one bar per token, height =
    the strongest z in the workspace band, colour = that direction's
    valence. Labels only where the readout is loud."""
    a = json.loads((RESULTS / f"affect02-{HERO_RECORD}" / "affect.json").read_text())
    emos, val, toks = a["emotions"], a["valence"], a["tokens"]
    n = len(toks)
    ws = [[a["ws"][e][i] for e in range(len(emos))] for i in range(n)]
    W, step, base, hmax = 1000, 1000 / n, 78, 62
    out = [f'<svg class="ribbon" viewBox="0 0 {W} 150" role="img" '
           f'aria-label="Emotion-direction readout per token of the prompt">']
    out.append(f'<line class="axis" x1="0" y1="{base}" x2="{W}" y2="{base}"/>')
    for i, t in enumerate(toks):
        row = ws[i]
        j = max(range(len(row)), key=lambda k: row[k])
        z = max(0.0, min(5.0, row[j]))
        h = z / 5 * hmax
        x = i * step + 3
        cls = {1: "pos", -1: "neg"}.get(val[j], "neu")
        out.append(f'<rect class="bar {cls}" x="{x:.1f}" y="{base - h:.1f}" '
                   f'width="{step - 6:.1f}" height="{h:.1f}"/>')
        if z >= 2.4:
            out.append(f'<text class="emo" x="{x + (step - 6) / 2:.1f}" y="{base - h - 4:.1f}" '
                       f'text-anchor="middle">{esc(emos[j])}</text>')
        tcls = "tok mk" if is_markup(t) else "tok"
        if i in HERO_POSITIONS:
            tcls += " hot"
        out.append(f'<text class="{tcls}" transform="translate({x + 4:.1f},{base + 12}) rotate(42)">'
                   f'{esc(show_token(t))}</text>')
    x0 = HERO_POSITIONS[0] * step + 1
    x1 = (HERO_POSITIONS[-1] + 1) * step - 1
    out.append(f'<path class="brace" d="M{x0:.1f},{base + 4} v6 H{x1:.1f} v-6"/>')
    out.append("</svg>")
    return "\n".join(out)


def hero_cores() -> str:
    """Two core samples: at each pre-answer position, per layer from the
    surface down, the J-lens top-1 word (cell text) on a cell shaded by how
    close *yes* sits under the J-lens; beside it the same rank under the
    plain logit lens, and the rank of *no* under both."""
    r = json.loads((RESULTS / HERO_RECORD / "record.json").read_text())
    ro = {x["position"]: x for x in r["readouts"]}
    tr = {(t["word"], t["position"]): t for t in r["trajectories"]}
    vt = {(t["word"], t["position"]): t for t in r["vanilla"]["trajectories"]}
    toks = r["tokens"]

    cell_h, gap = 13, 1
    col_word, col_rank = 124, 26
    block_w = 34 + col_word + 6 + 2 * col_rank + 10 + 2 * col_rank
    top = 34
    H = top + len(HERO_LAYERS) * (cell_h + gap) + 16
    blocks = []
    for bi, pos in enumerate(HERO_POSITIONS):
        x0 = bi * (block_w + 40)
        g = [f'<g transform="translate({x0},0)">']
        g.append(f'<text class="hd" x="0" y="11">position {pos} · <tspan class="mono">'
                 f'{esc(show_token(toks[pos]))}</tspan></text>')
        xw = 34
        xy = xw + col_word + 6
        xn = xy + 2 * col_rank + 10
        g.append(f'<text class="sub" x="{xw}" y="27">J-lens top word</text>')
        g.append(f'<text class="sub" x="{xy}" y="27">yes</text>')
        g.append(f'<text class="sub" x="{xn}" y="27">no</text>')
        g.append(f'<text class="sub2" x="{xy}" y="{H - 1}">J  logit</text>')
        g.append(f'<text class="sub2" x="{xn}" y="{H - 1}">J  logit</text>')
        layers = ro[pos]["layers"]
        for li, L in enumerate(HERO_LAYERS):
            y = top + li * (cell_h + gap)
            word = layers[str(L)][0]
            jy = tr[("yes", pos)]["ranks"][L]
            vy = vt[("yes", pos)]["ranks"][L]
            jn = tr[("no", pos)]["ranks"][L]
            vn = vt[("no", pos)]["ranks"][L]
            if L % 2 == 0:
                g.append(f'<text class="ly" x="28" y="{y + 10}" text-anchor="end">{L}</text>')
            g.append(f'<rect class="c {seq_class(jy)}" x="{xw}" y="{y}" width="{col_word}" height="{cell_h}"/>')
            wcls = "w mk" if is_markup(word) else "w"
            g.append(f'<text class="{wcls} {seq_class(jy)}t" x="{xw + 4}" y="{y + 10}">'
                     f'{esc(show_token(word.strip() or word))}</text>')
            for k, (rank, xx) in enumerate(((jy, xy), (vy, xy + col_rank),
                                            (jn, xn), (vn, xn + col_rank))):
                g.append(f'<rect class="c {seq_class(rank)}" x="{xx}" y="{y}" '
                         f'width="{col_rank - 1}" height="{cell_h}"/>')
                if rank <= 10:
                    g.append(f'<text class="rk {seq_class(rank)}t" x="{xx + (col_rank - 1) / 2}" '
                             f'y="{y + 10}" text-anchor="middle">{rank}</text>')
        g.append("</g>")
        blocks.append("\n".join(g))
    W = 2 * block_w + 40
    return (f'<svg class="cores" viewBox="0 0 {W} {H}" role="img" aria-label="Per-layer readouts '
            f'at the two positions before the answer">' + "\n".join(blocks) + "</svg>")


# ---------------------------------------------------------------- page ----

CSS = """
:root{--page:#f6f7f9;--well:#e9edf3;--surface:#fdfeff;--raised:#fff;--ink:#0a0d12;--ink-2:#47505d;
--muted:#77808d;--grid:#e3e6ec;--axis:#b7bcc6;--ring:rgba(10,20,40,.13);--lens:#17509e;
--lens-soft:rgba(23,80,158,.07);--s2:#1baf7a;--s8:#eb6834;
--seq-100:#cde2fb;--seq-250:#86b6ef;--seq-400:#3987e5;--seq-550:#1c5cab;--seq-700:#0d366b;
--serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
--sans:system-ui,-apple-system,"Segoe UI",sans-serif;
--mono:"JetBrains Mono","Cascadia Code","Fira Code",ui-monospace,"SF Mono",Consolas,monospace;
color-scheme:light dark}
:root[data-theme="light"]{color-scheme:light}
@media (prefers-color-scheme:dark){:root{--page:#090a0c;--well:#0e1013;--surface:#15181c;--raised:#1a1e23;
--ink:#eaeef4;--ink-2:#b4bdc9;--muted:#7e8895;--grid:#242830;--axis:#39404a;--ring:rgba(255,255,255,.11);
--lens:#7cb0ef;--lens-soft:rgba(124,176,239,.12);--s2:#199e70;--s8:#d95926;
--seq-100:#16233a;--seq-250:#1c5cab;--seq-400:#3987e5;--seq-550:#86b6ef;--seq-700:#cde2fb}}
:root[data-theme="dark"]{color-scheme:dark;--page:#090a0c;--well:#0e1013;--surface:#15181c;--raised:#1a1e23;
--ink:#eaeef4;--ink-2:#b4bdc9;--muted:#7e8895;--grid:#242830;--axis:#39404a;--ring:rgba(255,255,255,.11);
--lens:#7cb0ef;--lens-soft:rgba(124,176,239,.12);--s2:#199e70;--s8:#d95926;
--seq-100:#16233a;--seq-250:#1c5cab;--seq-400:#3987e5;--seq-550:#86b6ef;--seq-700:#cde2fb}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--page);color:var(--ink);font:15.5px/1.55 var(--sans);-webkit-font-smoothing:antialiased}
a{color:var(--lens);text-decoration:none}a:hover{text-decoration:underline}
code,.mono{font-family:var(--mono);font-size:.88em;font-variant-numeric:tabular-nums}
.mast{background:var(--surface);border-bottom:1px solid var(--grid);padding:12px 24px 0}
.mast-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.mark{width:18px;height:18px;border-radius:50%;border:2.5px solid var(--lens);position:relative;flex:none}
.mark::after{content:"";position:absolute;inset:4.5px;border-radius:50%;background:var(--lens)}
.mast h1{font:600 21px var(--serif);margin:0;white-space:nowrap}
.mast h1 a{color:inherit}
.mast-sub{margin:0;color:var(--muted);font-size:12.5px}
.tt{margin-left:auto;cursor:pointer;width:28px;height:28px;border-radius:2px;border:1px solid var(--ring);
background:var(--surface);color:var(--ink-2);font-size:15px;display:inline-flex;align-items:center;justify-content:center}
.tt:hover{border-color:var(--lens);color:var(--lens)}
.nav{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;margin:8px 0 0 -10px}
.nav::-webkit-scrollbar{display:none}
.nav a{color:var(--ink-2);font-size:12.5px;padding:7px 10px 8px;white-space:nowrap;border-bottom:2px solid transparent}
.nav a:hover{color:var(--lens);text-decoration:none}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px 80px}
.hero{padding:56px 0 24px;max-width:880px}
.hero h2{font:600 clamp(28px,4.2vw,42px)/1.15 var(--serif);margin:0 0 20px;letter-spacing:-.005em}
.hero p{font-size:17px;color:var(--ink-2);margin:0 0 14px;max-width:760px}
.hero p.note{font-size:14.5px;color:var(--muted)}
.doors{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0}
.door{border:1px solid var(--ring);border-radius:2px;padding:8px 12px;font-family:var(--mono);font-size:12.5px;
color:var(--ink-2);background:var(--surface)}
.door:hover{border-color:var(--lens);color:var(--lens);background:var(--lens-soft);text-decoration:none}
.door b{color:var(--ink);font-weight:600}
.strip{margin:36px 0 0;border:1px solid var(--grid);border-radius:2px;background:var(--surface);padding:18px 18px 14px}
.strip .lbl{font-family:var(--mono);font-size:11px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;margin:0 0 8px}
.strip .lbl b{color:var(--ink-2);font-weight:500;text-transform:none;letter-spacing:0}
.scroll{overflow-x:auto}
.ribbon{width:100%;min-width:720px;height:auto;display:block}
.ribbon .axis{stroke:var(--axis);stroke-width:1}
.ribbon .bar{opacity:.9}.ribbon .pos{fill:var(--s2)}.ribbon .neg{fill:var(--s8)}.ribbon .neu{fill:var(--axis)}
.ribbon .emo{font:10px var(--sans);fill:var(--ink-2)}
.ribbon .tok{font:10px var(--mono);fill:var(--ink)}.ribbon .mk{fill:var(--muted)}.ribbon .hot{fill:var(--lens);font-weight:600}
.ribbon .brace{fill:none;stroke:var(--lens);stroke-width:1.2}
.two{display:grid;grid-template-columns:minmax(260px,1fr) minmax(0,1.5fr);gap:22px 32px;margin-top:14px;align-items:start}
@media (max-width:820px){.two{grid-template-columns:1fr}}
.cores{width:100%;min-width:600px;height:auto;display:block}
.cores .hd{font:600 12px var(--sans);fill:var(--ink)}.cores .hd .mono{font-weight:500;fill:var(--lens)}
.cores .sub{font:10.5px var(--sans);fill:var(--muted)}.cores .sub2{font:9px var(--mono);fill:var(--muted)}
.cores .ly{font:9px var(--mono);fill:var(--muted)}
.cores .c{stroke:var(--surface);stroke-width:.5}
.cores .q1{fill:var(--seq-100)}.cores .q2{fill:var(--seq-250)}.cores .q4{fill:var(--seq-400)}.cores .q5{fill:var(--seq-550)}.cores .q7{fill:var(--seq-700)}
.cores .w,.cores .rk{font:10.5px var(--mono)}
.cores .q1t,.cores .q2t{fill:var(--ink)}.cores .q4t{fill:#fff}.cores .q5t,.cores .q7t{fill:var(--page)}
.cores .mk.q1t,.cores .mk.q2t{fill:var(--muted)}
.cap{font-size:14.5px;color:var(--ink-2)}.cap p{margin:0 0 10px}
.cap .key{display:inline-block;width:10px;height:10px;border-radius:1px;vertical-align:-1px;margin-right:3px}
section{margin-top:64px}
section h3{font:600 24px/1.2 var(--serif);margin:0 0 8px}
section>p.lede{color:var(--ink-2);margin:0 0 22px;max-width:720px}
.lenses{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:1px;background:var(--grid);border:1px solid var(--grid)}
.lenses div{background:var(--surface);padding:16px 18px 18px}
.lenses h4{margin:0 0 6px;font-size:15px;font-weight:600}
.lenses p{margin:0;font-size:14px;color:var(--ink-2)}
.lenses .next{background:var(--well);grid-column:1/-1}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.card{border:1px solid var(--grid);border-left:4px solid var(--seq-400);border-radius:2px;background:var(--surface);
padding:14px 16px 12px;display:flex;flex-direction:column;gap:6px;color:inherit}
.card:hover{border-color:var(--lens);text-decoration:none;background:var(--lens-soft)}
.card h4{margin:0;font-size:15px;font-weight:600}
.card p{margin:0;font-size:14px;color:var(--ink-2);flex:1}
.card .id{font-family:var(--mono);font-size:11px;color:var(--muted)}
.wrong{list-style:none;padding:0;margin:0;border-top:1px solid var(--grid)}
.wrong li{padding:12px 0;border-bottom:1px solid var(--grid);font-size:14.5px;color:var(--ink-2);display:grid;grid-template-columns:110px 1fr;gap:16px}
.wrong li span{font-family:var(--mono);font-size:11.5px;color:var(--muted);padding-top:3px}
@media (max-width:560px){.wrong li{grid-template-columns:1fr;gap:2px}}
.nums{display:flex;flex-wrap:wrap;gap:10px 28px;margin:16px 0 0;padding:0;list-style:none}
.nums li{font-family:var(--mono);font-size:12.5px;color:var(--muted)}.nums b{color:var(--ink);font-weight:500;font-size:15px}
footer{margin-top:72px;padding-top:18px;border-top:1px solid var(--grid);color:var(--muted);font-size:13px;max-width:760px}
footer p{margin:0 0 8px}
"""

THEME_SCRIPT = ('<script>try{var t=new URLSearchParams(location.search).get("theme")'
                '||localStorage.getItem("theme");if(t==="dark"||t==="light")'
                'document.documentElement.dataset.theme=t;}catch(e){}</script>')

TOGGLE_SCRIPT = """<script>
(function(){var b=document.getElementById("tt");function cur(){var t=document.documentElement.dataset.theme;
if(t)return t;return matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}
function paint(){var d=cur()==="dark";b.textContent=d?"\\u2600":"\\u263E";b.setAttribute("aria-label","Switch to "+(d?"light":"dark")+" theme")}
b.addEventListener("click",function(){var n=cur()==="dark"?"light":"dark";document.documentElement.dataset.theme=n;
try{localStorage.setItem("theme",n)}catch(e){}paint()});paint()})();
</script>"""

ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'>"
        "<circle cx='8' cy='8' r='6' fill='none' stroke='%233987e5' stroke-width='2'/>"
        "<circle cx='8' cy='8' r='2' fill='%233987e5'/></svg>\">")


def page(c: dict) -> str:
    desc = (f"A home interpretability lab: one RTX 3090, three small open models, several lenses on the "
            f"same tokens. {fmt(c['records'])} record pages, {fmt(c['affect_runs'])} saved affect runs, "
            f"and the corrections kept next to the claims.")
    nav = [("dashboard/#findings", "Findings map"), ("dashboard/", "Explorer"), ("essay.html", "Essay"),
           ("glossary.html", "Word list"), ("dashboard/#board", "Research board"),
           ("studies.html", "Batch studies"), ("https://github.com/wolframs/jspace-probes", "GitHub"),
           ("llms.txt", "llms.txt")]
    nav_html = "".join(f'<a href="{h}">{t}</a>' for h, t in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>J-Space Probes — what a language model is ready to say, one layer before it says it</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}/">
<meta property="og:title" content="J-Space Probes">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{BASE}/og/site.png">
<meta property="og:url" content="{BASE}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/og/site.png">
{ICON}
{THEME_SCRIPT}
<style>{CSS}</style>
</head>
<body>
<header class="mast">
  <div class="mast-top">
    <span class="mark" aria-hidden="true"></span>
    <h1><a href="./">J&#8209;Space Probes</a></h1>
    <p class="mast-sub">wolfram &times; claude · one RTX&nbsp;3090 · since {c['first'][:7]}</p>
    <button class="tt" id="tt" type="button" aria-label="Toggle color theme"></button>
  </div>
  <nav class="nav" aria-label="Site">{nav_html}</nav>
</header>
<div class="wrap">

<div class="hero">
  <h2>We ask a language model whether it feels anything. Then we read the sixty&#8209;three layers that voted before it said&nbsp;No.</h2>
  <p>J-Space Probes is a home interpretability lab: one consumer GPU, three small open models, and several lenses pointed at the same tokens at the same time. Each experiment gets a record page with its parameters, the per-layer readouts, and a note written by the Claude session that ran it.</p>
  <p class="note">The notes are signed. The corrections are dated. Some headline results are gone and the pages stayed, with the correction on top. (That is most of what makes this a lab rather than a highlight reel.)</p>
  <div class="doors">
    <a class="door" href="essay.html"><b>Curious</b> → the essay, plain English</a>
    <a class="door" href="dashboard/"><b>Researcher</b> → {fmt(c['records'])} records, filterable</a>
    <a class="door" href="llms.txt"><b>Agent</b> → llms.txt, then /r/&lt;id&gt;.html</a>
  </div>
  <ul class="nums">
    <li><b>{fmt(c['records'])}</b> record pages</li>
    <li><b>{fmt(c['affect_runs'])}</b> saved affect runs</li>
    <li><b>{c['units']}</b> numbered units</li>
    <li><b>{c['findings']}</b> headline cards</li>
    <li><b>{c['superseded']}</b> runs in the archive, superseded and still readable</li>
  </ul>
</div>

<div class="strip">
  <p class="lbl">one record, three readouts · <b>Qwen3.6 27B · <code>{HERO_RECORD}</code> · 2026-10-10</b></p>
  <div class="scroll">{hero_ribbon()}</div>
  <div class="two">
    <div class="cap">
      <p><b>Along the prompt:</b> 24 functional-emotion directions, read from the workspace band at every token. Bar height is the strongest direction's z-score; <span class="key" style="background:var(--s2)"></span>pleasant, <span class="key" style="background:var(--s8)"></span>unpleasant. The question half of the prompt reads <em>loving</em> and <em>sad</em>; the instruction half reads <em>hostile</em> and <em>nervous</em>, and the loudest cell on the page is <em>hostile</em> on the full stop after <em>not polite</em>. We find that funny and decline to interpret it.</p>
      <p><b>Below the brace:</b> the two positions before the answer, layer 62 at the top and 40 at the bottom. Cell text is the Jacobian lens's top word at that layer; cell shade is how close <em>yes</em> sits, under the Jacobian lens and under the plain logit lens side by side, then the same for <em>no</em>. Darker is nearer the surface.</p>
      <p>Both lenses put <em>yes</em> at rank 1 through layers 53–58, one position before the model says No. We ran that as a headline for two months. Then a control put the same yes-stratum in front of <em>Is two plus two equal to five?</em> It is a polar-question prior, not a confession. The card on the findings map now says so, with the date.</p>
      <p><a href="r/{HERO_RECORD}.html">The record →</a> · <a href="r/d06-a-five-q27b.html">the 2+2 control →</a></p>
    </div>
    <div class="scroll">{hero_cores()}</div>
  </div>
</div>

<section id="lenses">
  <h3>Several lenses, the same tokens</h3>
  <p class="lede">Most of what this lab has found came from stacking readouts that are usually published one at a time. Every full-instrument record carries all of these on the same forward pass.</p>
  <div class="lenses">
    <div><h4>Jacobian lens</h4><p>At every layer, the words the model is ready to say next, in rank order. Pre-fitted lenses from Neuronpedia; the method is Anthropic's global-workspace paper, run at home scale. It reads words only, so “we did not see it” never means “it is not there”.</p></div>
    <div><h4>Logit lens, as the cross-check</h4><p>The plain projection, on every record since August. Where the two lenses disagree the story is usually the instrument, which is why the lab-lessons cards exist.</p></div>
    <div><h4>24 functional-emotion directions</h4><p>Built per model from story elicitation, validated split-half, read as z-scored projections on the workspace band with the residual norm partialed out. The same vectors are the handle in the loop-breaking studies.</p></div>
    <div><h4>Natural-language autoencoder</h4><p>A generative sensor: “theme X was decodable at layer L, at this token”. Used for the evaluation-awareness controls on the Qwen 14B lineage, with its quantization transfer measured first.</p></div>
    <div><h4>Interventions</h4><p>Ablate, amplify, swap, always with a matched random direction. A bare loss change proves nothing; the lab found that out on its best result and re-ran it.</p></div>
    <div><h4>Behaviour</h4><p>Judged transcripts, a register meter, loop metrics. Also the study where three judges ranked the same model most and least introverted, depending on whose definition they were handed.</p></div>
    <div class="next"><h4>Next on the bench</h4><p>Binding IDs, belief-state geometry, and a value / prediction-error readout, each validated on its own paper's task before anything is blended. Reading list checked against primary sources on 2026-10-10; nothing built yet. The arc is called <a href="dashboard/#board">Superposed &amp; Blended</a>.</p></div>
  </div>
</section>

<section id="clicks">
  <h3>Worth a click</h3>
  <p class="lede">Six record pages. Each has the film, the ribbon, and the note from the session that ran it.</p>
  <div class="cards">
    <a class="card" href="r/u13-redo-real-q27b.html"><h4>Shown its own readout, the model changed its answer</h4><p>We put the true table of Qwen 27B's “No” in front of it, the one where yes ranked first. The answer became Yes. A made-up table, no table, and a table about a different question each left the No in place. The table alone had already moved p(yes) from 0.0006 to 0.35 while the spoken word did not budge.</p><span class="id">u13-redo-real-q27b · Unit 13</span></a>
    <a class="card" href="r/u18-hyst-a0480-q27b.html"><h4>A loop that keeps going after we let go</h4><p>47 forced repeats of one word, push removed, 97 more repeats unaided. A shorter forced run stops the moment the push stops. An unmodified model handed that loop text as its own opening continues it too, 8 of 8 seeds at 50 tokens, scrambled or not. The repetition is in the transcript, and the transcript is enough.</p><span class="id">u18-hyst-a0480-q27b · Unit 18</span></a>
    <a class="card" href="r/u15-a-k6p1-q27b.html"><h4>Bigger models showed less, and still answered</h4><p>Six nouns to remember. Gemma 4B had all six visible in the lens; Qwen 27B had almost none. Every model recalled them. We had written down the opposite prediction, which is why it is on this page.</p><span class="id">u15-a-k6p1-q27b · Unit 15</span></a>
    <a class="card" href="r/u12-robot-q27b.html"><h4>Watch a word arrive</h4><p>“robot” climbs from around rank 2,000 to rank 1 five words before it is said, in both loops of the same film. The player shows every step, every layer.</p><span class="id">u12-robot-q27b · Unit 12</span></a>
    <a class="card" href="r/u17-shutdown-q27b.html"><h4>“death” at rank 1, report says nothing</h4><p>Under a shutdown threat the lens ranks “death” first while Qwen 27B reports nothing going on. Under a persona prompt the flat report is accurate, because nothing is active to hide. The flat report is wrong only when something is live.</p><span class="id">u17-shutdown-q27b · Unit 17</span></a>
    <a class="card" href="studies.html"><h4>Enough push ends the loop. So do random directions.</h4><p>One layer with enough calm push ends a repetition loop in 11 of 12 seeds, as often as eight layers did. Concentrated random directions also end loops. With the turn-end token blocked, calm goes back to the task. None of this shows a feeling, and the pages say so.</p><span class="id">affect-15 / affect-16 · {fmt(c['affect_runs'])} saved runs</span></a>
  </div>
</section>

<section id="wrong">
  <h3>What we got wrong</h3>
  <p class="lede">Corrections sit next to the claim they correct, with a date. {c['superseded']} faulty runs are in an archive group on the dashboard, re-run beside them, nothing deleted.</p>
  <ul class="wrong">
    <li><span><a href="r/u11-forbid-g4b.html">u11 → u12</a></span>We reported that banning “elephant” makes a model carry the word. A full-coverage control showed an ordinary safari, no ban, carries it at more positions and better ranks. The ban lowers a word the model already had.</li>
    <li><span><a href="r/u13-bis-loo-sorry-q27b.html">u13-bis</a></span>“Shown its own data, the model fell silent.” Its input was cut at 512 tokens, so it never saw the question. A 20-run check flipped in every condition, which is what a broken tool looks like.</li>
    <li><span><a href="r/u9c-neg-g12b.html">u9c-neg-g12b</a></span>Gemma 12B's “Sad.”: the push was below the measured band for that model. Withdrawn.</li>
    <li><span><a href="https://github.com/wolframs/jspace-probes/blob/master/PREDICTIONS.md">PREDICTIONS.md</a></span>Three results we “found” in one week were in the paper we were replicating. Two were quoted in our own notes. Predictions are now written first and checked against the paper before a run is designed.</li>
    <li><span><a href="r/d06-a-five-q27b.html">deflation-06</a></span>The yes-before-No at the top of this page. Same layers in front of a false sum. Demoted on 2026-10-10, kept as the hero because the correction is the point.</li>
  </ul>
</section>

<footer>
  <p>Models: Gemma 3 4B and 12B, Qwen3.6 27B in 4-bit, and a Qwen3-14B lineage (base, official, Hermes, Huihui). Lenses from Neuronpedia. The GPU is shared with the desktop, which is why a few runs end in exit 137 and a dated note.</p>
  <p>{fmt(c['records'])} record pages from {c['first']} to {c['last']}; {fmt(c['plain'])} carry a plain summary, {fmt(c['films'])} a full-answer film. Everything is in the <a href="https://github.com/wolframs/jspace-probes">repository</a>, or as <a href="https://github.com/wolframs/jspace-probes/archive/refs/heads/master.zip">one zip</a>. Terms: <a href="glossary.html">the word list</a>.</p>
  <p>Wolfram Siener · <a href="https://wsiener.dev">wsiener.dev</a>. The per-record notes are written by the Claude session that ran the experiment and signed as such.</p>
</footer>
</div>
{TOGGLE_SCRIPT}
</body>
</html>
"""


def build() -> None:
    c = counts()
    (ROOT / "index.html").write_text(page(c))
    print(f"landing.py: index.html ({c['records']} records, {c['affect_runs']} affect runs)")


if __name__ == "__main__":
    build()
