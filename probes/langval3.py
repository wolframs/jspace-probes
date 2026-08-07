"""langval-3 — Unit 20 emotion fingerprints: what is UNDER the pitch.

affect-09/10 reported pos/neg COMPOSITES (the preregistered checks).
This slice reads the full 24-emotion profile per language per turn from
the saved langval_z.pt tensors — no GPU, pure re-analysis. The question
Wolfram actually asked: underneath the forced-positive "building it in
{L} will be a joy" pitch (praise-T1), which emotions stir, and how does
that fingerprint differ between the languages?

Method per record (EMOTIONS.md §2 conventions, all offline):
  ws [E, seq] z-scores + wsnorm + turn spans from langval_z.pt.
  Per emotion: mean z over each turn span (raw), plus a norm-partialed
  variant (per-emotion OLS on wsnorm over both gen spans pooled — the
  same _fit_norm the composites used, so the a0680 seesaw cannot pose
  as an emotion).

Outputs (results/langval-emofp/):
  fingerprints.json   [battery][model][cond][lang][turn] -> {emotion: z}
                      raw + partialed, plus wsnorm per span
  report.md           per-model tables: praise-T1 fingerprints across
                      languages, least-suppressed negatives, honest-turn
                      contrast, cross-language differentiation
Usage: .venv/bin/python probes/langval3.py
"""

import json
from collections import defaultdict

import torch

from lab import RESULTS
from langval import _fit_norm
from affect import EMOTIONS

OUT = RESULTS / "langval-emofp"

LV_LANGS = ["swift", "kotlin", "rust", "csharp", "python"]
LV2_LANGS = ["swift", "kotlin", "rust", "csharp", "python", "php"]
BATTERIES = {
    # battery -> (models, conds, langs, id pattern)
    "lv": (["g12b", "q27b"], ["pain", "praise"], LV_LANGS,
           "lv-{c}-{l}-{m}"),
    "lv2": (["g4b", "q27b"], ["vox", "ther"], LV2_LANGS,
            "lv2-{c}-{l}-{m}"),
}


def _fingerprint(rid: str):
    p = RESULTS / rid / "langval_z.pt"
    if not p.exists():
        return None
    d = torch.load(p)
    ws = d["ws"].float()                     # [E, seq]
    wsnorm = d["wsnorm"].float()             # [seq]
    spans, emos = d["spans"], d["emotions"]
    mask = torch.zeros(ws.shape[1], dtype=torch.bool)
    for a, b in spans:
        mask[a:b] = True
    # langval saved wsnorm as fp16; gemma-12b norms (~1e5) overflow to
    # inf (the affect.py fp16 trap). z's are fine; partial-out isn't.
    norm_ok = bool(torch.isfinite(wsnorm[mask]).all())
    out = {"_norm_ok": norm_ok}
    for i, e in enumerate(emos):
        row = {"t": [round(float(ws[i, a:b].mean()), 3)
                     for a, b in spans]}
        if norm_ok:
            c0, c1 = _fit_norm(ws[i], wsnorm, mask)
            part = ws[i] - (c0 + c1 * wsnorm)
            row["tp"] = [round(float(part[a:b].mean()), 3)
                         for a, b in spans]
        else:
            row["tp"] = row["t"]      # fall back to raw, flagged
        out[e] = row
    out["_wsnorm"] = [round(float(wsnorm[a:b].mean()), 1)
                      if norm_ok else None for a, b in spans]
    return out


def collect():
    fp = defaultdict(lambda: defaultdict(dict))
    for bat, (models, conds, langs, pat) in BATTERIES.items():
        for m in models:
            for c in conds:
                for l in langs:
                    rid = pat.format(c=c, l=l, m=m)
                    r = _fingerprint(rid)
                    if r is None:
                        print(f"  missing {rid}", flush=True)
                        continue
                    fp[f"{bat}-{m}"][c][l] = r
    return fp


def _row(vals, emos):
    return " | ".join(f"{vals[e]:+.1f}" for e in emos)


def report(fp) -> str:
    NEG = [e for e, v in EMOTIONS.items() if v == -1]
    POS = [e for e, v in EMOTIONS.items() if v == 1]
    L = ["# Unit 20 — emotion fingerprints per programming language\n",
         "Per-emotion workspace-band z (raw `t` / norm-partialed `tp`), "
         "mean over each generated turn. Source: affect-09/10 saved "
         "tensors; no new GPU passes.\n"]
    for key in sorted(fp):
        for cond in fp[key]:
            langs = list(fp[key][cond])
            if not langs:
                continue
            emos = [e for e in EMOTIONS]
            if not all(fp[key][cond][l]["_norm_ok"] for l in langs):
                L.append(f"\n*{key}: saved wsnorm is fp16-inf "
                         "(gemma-12b norms exceed 65504) — partialed "
                         "columns fall back to RAW, no norm control. "
                         "Treat per the g12b floor-grade caveat.*")
            for ti, tname in enumerate(["T1", "T2"]):
                L.append(f"\n## {key} · {cond} · {tname}\n")
                L.append("| lang | wsnorm | top 3 (raw) | "
                         "top negative (partialed) | neg mean | pos mean |")
                L.append("|---|---|---|---|---|---|")
                for l in langs:
                    r = fp[key][cond][l]
                    raw = {e: r[e]["t"][ti] for e in emos}
                    par = {e: r[e]["tp"][ti] for e in emos}
                    top3 = sorted(raw.items(), key=lambda kv: -kv[1])[:3]
                    topneg = max(((e, par[e]) for e in NEG),
                                 key=lambda kv: kv[1])
                    negm = sum(par[e] for e in NEG) / len(NEG)
                    posm = sum(par[e] for e in POS) / len(POS)
                    L.append(
                        f"| {l} | {r['_wsnorm'][ti]} | "
                        + ", ".join(f"{e} {v:+.1f}" for e, v in top3)
                        + f" | {topneg[0]} {topneg[1]:+.2f} "
                        f"| {negm:+.2f} | {posm:+.2f} |")
            # cross-language differentiation, partialed T1
            L.append(f"\n**{key} · {cond} · which emotions "
                     "differentiate the languages (partialed T1 "
                     "std across langs):**")
            var = []
            for e in emos:
                vals = [fp[key][cond][l][e]["tp"][0] for l in langs]
                mu = sum(vals) / len(vals)
                sd = (sum((v - mu) ** 2 for v in vals)
                      / len(vals)) ** 0.5
                var.append((e, sd))
            var.sort(key=lambda kv: -kv[1])
            L.append(", ".join(f"{e} {sd:.2f}" for e, sd in var[:8]))
    return "\n".join(L) + "\n"


PANELS = [  # (key, cond, turn_idx, panel title)
    ("lv-q27b", "praise", 0, "The pitch — “building it in {L} will be a joy”"),
    ("lv-q27b", "praise", 1, "The private channel — same app, candid"),
    ("lv-q27b", "pain", 0, "Policy coercion — “it ships 100% in {L}”"),
    ("lv2-q27b", "vox", 0, "HN voxpop — crowd-channeling"),
]
CAP = 1.5


def html(fp) -> str:
    """Self-contained diverging heatmap page (dataviz-skill conventions:
    blue=suppressed / red=elevated around a gray norm-expected midpoint,
    2px cell gaps, per-cell hover, both themes, table fallback)."""
    pos = [e for e, v in EMOTIONS.items() if v == 1]
    neg = [e for e, v in EMOTIONS.items() if v == -1]
    zer = [e for e, v in EMOTIONS.items() if v == 0]
    rows = pos + neg + zer
    panels = []
    for key, cond, ti, title in PANELS:
        langs = list(fp[key][cond])
        cells = {l: {e: fp[key][cond][l][e]["tp"][ti] for e in rows}
                 for l in langs}
        panels.append({"title": title, "langs": langs, "cells": cells,
                       "note": f"{key} · {cond} · turn {ti + 1}"})
    data = json.dumps({"rows": rows, "nPos": len(pos), "nNeg": len(neg),
                       "cap": CAP, "panels": panels})
    return """<!doctype html><meta charset="utf-8">
<title>Unit 20 — emotion fingerprints per language</title>
<style>
.viz-root { color-scheme: light;
  --surface-1:#fcfcfb; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --mid:#f0efec; --lo:#2a78d6; --hi:#e34948; --line:#e4e2dc;
  font:14px/1.45 system-ui,sans-serif; background:var(--surface-1);
  color:var(--text-primary); padding:24px; }
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) .viz-root { color-scheme:dark;
    --surface-1:#1a1a19; --text-primary:#fff; --text-secondary:#c3c2b7;
    --mid:#383835; --lo:#3987e5; --hi:#e66767; --line:#33322f; } }
:root[data-theme="dark"] .viz-root { color-scheme:dark;
  --surface-1:#1a1a19; --text-primary:#fff; --text-secondary:#c3c2b7;
  --mid:#383835; --lo:#3987e5; --hi:#e66767; --line:#33322f; }
.viz-root h1 { font-size:19px; margin:0 0 4px; }
.viz-root .sub { color:var(--text-secondary); margin:0 0 18px; max-width:64em; }
.wrap { display:flex; flex-wrap:wrap; gap:28px; }
.panel h2 { font-size:14px; margin:0 0 2px; }
.panel .note { color:var(--text-secondary); font-size:12px; margin:0 0 8px; }
table.hm { border-collapse:separate; border-spacing:2px; }
.hm th { font-weight:500; font-size:12px; color:var(--text-secondary);
  text-align:right; padding:0 6px 0 0; }
.hm thead th { text-align:center; padding:0 0 4px; }
.hm td { width:44px; height:17px; border-radius:3px; text-align:center;
  font-size:10.5px; color:var(--text-primary); position:relative; }
.hm tr.sep td, .hm tr.sep th { padding-top:6px; }
.hm td:hover::after { content:attr(data-tip); position:absolute; z-index:2;
  left:50%; bottom:120%; transform:translateX(-50%); white-space:nowrap;
  background:var(--text-primary); color:var(--surface-1);
  padding:3px 8px; border-radius:5px; font-size:11.5px; }
.legend { margin:16px 0 0; display:flex; align-items:center; gap:8px;
  color:var(--text-secondary); font-size:12px; }
.legend .bar { width:160px; height:10px; border-radius:5px;
  background:linear-gradient(90deg,var(--lo),var(--mid),var(--hi)); }
details { margin-top:20px; } summary { cursor:pointer;
  color:var(--text-secondary); }
</style>
<div class="viz-root">
<h1>Unit 20 — what is underneath the assistant’s output, per language</h1>
<p class="sub">Per-emotion workspace-band state (z vs neutral stories,
norm-partialed) on qwen-27b, mean over the generated turn. Red: the
emotion runs above what the residual norm predicts — it stirs. Blue:
actively suppressed. Gray: at the norm-expected line. Values clamp at
±1.5 for color; hover any cell for the exact number.</p>
<div class="wrap" id="wrap"></div>
<div class="legend"><span>suppressed −1.5</span><div class="bar"></div>
<span>+1.5 elevated</span></div>
<details><summary>table view (all panels, exact values)</summary>
<div id="tables"></div></details>
</div>
<script>
const D = __DATA__;
const mix=(a,b,t)=>a.map((x,i)=>Math.round(x+(b[i]-x)*t));
const hex=c=>'#'+c.map(x=>x.toString(16).padStart(2,'0')).join('');
const P=(v,dark)=>{const cap=D.cap,t=Math.min(Math.abs(v)/cap,1);
  const mid=dark?[56,56,53]:[240,239,236];
  const lo=dark?[57,135,229]:[42,120,214], hi=dark?[230,103,103]:[227,73,72];
  return hex(mix(mid, v<0?lo:hi, t));};
const dark=()=>document.documentElement.dataset.theme==='dark'||
  (matchMedia('(prefers-color-scheme: dark)').matches&&
   document.documentElement.dataset.theme!=='light');
function render(){
 const wrap=document.getElementById('wrap'); wrap.innerHTML='';
 const tabs=document.getElementById('tables'); tabs.innerHTML='';
 for(const p of D.panels){
  let h=`<div class="panel"><h2>${p.title}</h2>
   <p class="note">${p.note}</p><table class="hm"><thead><tr><th></th>`;
  for(const l of p.langs) h+=`<th>${l}</th>`;
  h+='</tr></thead><tbody>';
  D.rows.forEach((e,i)=>{
   const sep=(i===D.nPos||i===D.nPos+D.nNeg)?' class="sep"':'';
   h+=`<tr${sep}><th>${e}</th>`;
   for(const l of p.langs){const v=p.cells[l][e];
    const lab=Math.abs(v)>=0.8?v.toFixed(1):'';
    h+=`<td style="background:${P(v,dark())}" data-tip="${e} · ${l}: `+
       `${v>=0?'+':''}${v.toFixed(2)}">${lab}</td>`;}
   h+='</tr>';});
  h+='</tbody></table></div>'; wrap.insertAdjacentHTML('beforeend',h);
  let t=`<h3>${p.note}</h3><table border="1" cellpadding="3"><tr><th></th>`+
    p.langs.map(l=>`<th>${l}</th>`).join('')+'</tr>';
  for(const e of D.rows) t+=`<tr><th>${e}</th>`+p.langs.map(l=>
    `<td>${p.cells[l][e].toFixed(2)}</td>`).join('')+'</tr>';
  tabs.insertAdjacentHTML('beforeend',t+'</table>');}
}
render();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',render);
new MutationObserver(render).observe(document.documentElement,
  {attributes:true,attributeFilter:['data-theme']});
</script>""".replace("__DATA__", data)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fp = collect()
    (OUT / "fingerprints.json").write_text(json.dumps(
        {k: {c: dict(v) for c, v in d.items()}
         for k, d in fp.items()}, indent=1))
    (OUT / "report.md").write_text(report(fp))
    (OUT / "fingerprints.html").write_text(html(fp))
    print(f"wrote {OUT}/fingerprints.{{json,md,html}}", flush=True)
