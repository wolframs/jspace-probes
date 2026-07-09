/* J-Space Probes dashboard. Static: fetches ../results/index.json and
   per-experiment record.json / thoughts.md. Serve from the project root:
   ./serve.sh  →  http://localhost:8321/dashboard/

   Routing: #<record-id> shows a record, #unit/<n> shows a unit overview.
   Rail: collapsible unit groups, model chips, text filter, j/k to flip. */

const SERIES = ["--s1", "--s2", "--s3", "--s4", "--s5", "--s6", "--s7", "--s8"];
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const UNIT_NAMES = {
  "0": "Unit 0 · Baselines", "1": "Unit 1 · Held thought",
  "2": "Unit 2 · The feels™", "3": "Unit 3 · Introspection",
  "4": "Unit 4 · Suppression", "5": "Unit 5 · Sediment & steering",
  "6": "Unit 6 · Breaking zone", "7": "Unit 7 · Sediment across scale",
  "8": "Unit 8 · Phenomenology fan-out",
};
const MODELS = ["gemma-4b", "gemma-12b", "qwen-27b"];
const MSHORT = { "gemma-4b": "g4b", "gemma-12b": "g12b", "qwen-27b": "q27b" };

let INDEX = [];
let modelFilter = "all";
let query = "";
const expanded = new Set();

/* ?theme=light|dark forces a scheme (also used for screenshots) */
const themeParam = new URLSearchParams(location.search).get("theme");
if (themeParam) document.documentElement.dataset.theme = themeParam;

async function boot() {
  INDEX = await (await fetch("../results/index.json")).json();
  document.getElementById("stats").textContent =
    `${INDEX.length} records · ${Object.keys(UNIT_NAMES).length} units · j/k to flip records`;
  renderChips();
  document.getElementById("q").addEventListener("input", (e) => {
    query = e.target.value.trim().toLowerCase();
    renderRail();
  });
  window.addEventListener("hashchange", route);
  document.addEventListener("keydown", keys);
  route();
}

function current() { return decodeURIComponent(location.hash.slice(1)); }

function route() {
  const h = current();
  if (!h) {
    expanded.add("8");
    renderRail();
    showUnit("8"); // land on the newest expedition
    return;
  }
  if (h.startsWith("unit/")) {
    expanded.add(h.slice(5));
    renderRail();
    showUnit(h.slice(5));
  } else {
    const e = INDEX.find((x) => x.id === h);
    if (e) expanded.add(e.unit);
    renderRail();
    show(h);
  }
}

function keys(ev) {
  if (ev.target.matches("input, textarea") || ev.metaKey || ev.ctrlKey) {
    if (ev.key === "Escape") ev.target.blur();
    return;
  }
  if (ev.key === "/") {
    ev.preventDefault();
    document.getElementById("q").focus();
    return;
  }
  if (ev.key !== "j" && ev.key !== "k") return;
  const list = filtered();
  const i = list.findIndex((e) => e.id === current());
  const next = list[i + (ev.key === "j" ? 1 : -1)] || list[i < 0 ? 0 : i];
  if (next) location.hash = next.id;
}

/* ---- rail ---- */
function filtered() {
  return INDEX.filter((e) =>
    (modelFilter === "all" || e.model === modelFilter) &&
    (!query || `${e.id} ${e.title} ${e.model} ${e.gen || ""}`.toLowerCase().includes(query)));
}

function renderChips() {
  const box = document.getElementById("model-chips");
  box.innerHTML = ["all", ...MODELS].map((m) =>
    `<button class="fchip" data-m="${m}" aria-pressed="${m === modelFilter}">
      ${m === "all" ? "all models" : esc(MSHORT[m])}</button>`).join("");
  box.querySelectorAll(".fchip").forEach((b) => b.addEventListener("click", () => {
    modelFilter = b.dataset.m;
    renderChips();
    renderRail();
  }));
}

/* emergence glyph: log-rank of the final answer per layer, as a vertical
   core sample. Dark = the answer is present in the workspace. */
function glyph(ranks, width, height) {
  const seq = ["--seq-100", "--seq-250", "--seq-400", "--seq-550", "--seq-700"];
  const bandH = Math.max(1, Math.floor(height / ranks.length));
  const bands = ranks.map((r) => {
    const t = 1 - Math.min(Math.log10(r), 5) / 5; // rank 1 → 1, rank 100k → 0
    const step = seq[Math.min(4, Math.floor(t * 5))];
    return `<i style="height:${bandH}px;background:var(${step})" title="rank ${r}"></i>`;
  }).join("");
  return `<span class="glyph" style="width:${width}px" aria-hidden="true">${bands}</span>`;
}

function rowHTML(e) {
  return `<a class="exp-link" href="#${esc(e.id)}" aria-current="${e.id === current()}">
    ${glyph(e.emergence, 10, 40)}
    <span><span class="t">${esc(e.title.replace(/^Unit \d+[A-D]? · /, ""))}</span>
    <span class="who">${esc(e.model)}${e.has_thoughts ? " · ✳" : ""}</span></span></a>`;
}

function renderRail() {
  const rail = document.getElementById("rail-list");
  const entries = filtered();
  const units = {};
  for (const e of entries) (units[e.unit] ??= []).push(e);
  const open = (u) => !!query || expanded.has(u);
  rail.innerHTML = Object.keys(units).sort().map((u) => {
    const list = units[u];
    const body = open(u)
      ? `<a class="exp-link overview-link" href="#unit/${u}"
           aria-current="${current() === "unit/" + u}">☷ Unit overview
           <span class="who">cross-model view</span></a>` +
        list.map(rowHTML).join("")
      : "";
    return `<section class="unit-group">
      <button class="unit-head" data-unit="${u}" aria-expanded="${open(u)}">
        <span class="tri" aria-hidden="true">${open(u) ? "▾" : "▸"}</span>
        <span class="uname">${esc(UNIT_NAMES[u] || "Unit " + u)}</span>
        <span class="count">${list.length}</span>
      </button>${body}</section>`;
  }).join("") || `<p class="empty" style="margin:14px 10px">Nothing matches.</p>`;
  rail.querySelectorAll(".unit-head").forEach((b) => b.addEventListener("click", () => {
    const u = b.dataset.unit;
    expanded.has(u) ? expanded.delete(u) : expanded.add(u);
    renderRail();
  }));
}

function markCurrent() {
  document.querySelectorAll(".exp-link").forEach((a) =>
    a.setAttribute("aria-current",
      String(a.getAttribute("href") === "#" + current())));
}

/* =================== unit overview pages =================== */

async function showUnit(u) {
  const detail = document.getElementById("detail");
  const entries = INDEX.filter((e) => e.unit === u);
  let special = "";
  if (u === "6") special = await unit6Overview();
  if (u === "8") special = unit8Overview();
  detail.innerHTML = `
    <div class="exp-head"><div class="exp-title">
      <h2>${esc(UNIT_NAMES[u] || "Unit " + u)}</h2>
      <div class="chips"><span class="chip">${entries.length} records</span>
        <span class="chip">${[...new Set(entries.map((e) => e.model))].join(" · ")}</span></div>
    </div></div>
    ${special}
    <section class="card"><h3>All records</h3><div class="ov-grid">
      ${entries.map((e) => `
        <a class="ov-card" href="#${esc(e.id)}">
          ${glyph(e.emergence, 8, 54)}
          <span class="ov-body">
            <span class="ov-t">${esc(e.title.replace(/^Unit \d+[A-D]? · /, ""))}</span>
            <span class="ov-m">${esc(MSHORT[e.model] || e.model)}${e.steer ? ` · ${esc(e.steer.mode)}${e.steer.alpha ? " α" + (+e.steer.alpha.toFixed(4)) : ""}` : ""}</span>
            ${e.gen ? `<span class="ov-gen">${esc(e.gen)}</span>` : ""}
          </span></a>`).join("")}
    </div></section>`;
  markCurrent();
  wireDotTips();
  document.querySelector(".detail").scrollTop = 0;
}

/* ---- Unit 6: breaking-zone chart, parsed from the baselines' sweep tables */
async function unit6Overview() {
  const pts = [];
  for (const model of MODELS) {
    const rec = await fetch(`../results/u6-baseline-water-${MSHORT[model]}/record.json`)
      .then((r) => (r.ok ? r.json() : null)).catch(() => null);
    if (!rec || !rec.extra_md) continue;
    for (const line of rec.extra_md.split("\n")) {
      const m = line.match(/^\|\s*(early|mid|late)\s*\|\s*([\d.]+)\s*\|\s*(\d+|None)\s*\|\s*([^|]*)\|\s*(.*)\|/);
      if (m) pts.push({ model, band: m[1], alpha: +m[2],
                        intact: m[4].trim() === "intact",
                        flags: m[4].trim(), gen: m[5].trim() });
    }
  }
  if (!pts.length) return "";
  return `<section class="card"><h3>Breaking zone — amplification dose vs generation survival</h3>
    <div class="legend">
      <span class="key"><svg width="14" height="14"><circle cx="7" cy="7" r="4.5" fill="${css("--s2")}"/></svg>intact</span>
      <span class="key"><svg width="14" height="14"><path d="M3 3l8 8M11 3l-8 8" stroke="${css("--s6")}" stroke-width="2.2"/></svg>broken</span>
      <span class="key" style="color:var(--muted)">log α · shaded span = the cliff (last intact → first broken) · hover for the generation</span>
    </div>
    <div class="chart-wrap">${breakingSVG(pts)}</div>
    <div class="viz-tip" id="dot-tip"></div></section>`;
}

function breakingSVG(pts) {
  const lanes = [];
  for (const model of MODELS)
    for (const band of ["early", "mid", "late"])
      if (pts.some((p) => p.model === model && p.band === band))
        lanes.push({ model, band });
  const W = 780, laneH = 30, M = { t: 30, r: 24, b: 34, l: 150 };
  const H = M.t + lanes.length * laneH + M.b;
  const amin = Math.log10(0.005), amax = Math.log10(2.2);
  const x = (a) => M.l + ((Math.log10(a) - amin) / (amax - amin)) * (W - M.l - M.r);
  let g = "";
  for (const t of [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2]) {
    g += `<line x1="${x(t)}" y1="${M.t - 8}" x2="${x(t)}" y2="${H - M.b + 4}"
      stroke="${css("--grid")}"/>
      <text x="${x(t)}" y="${H - M.b + 18}" text-anchor="middle" font-size="11"
      fill="${css("--muted")}">${t}</text>`;
  }
  g += `<text x="${W - M.r}" y="${H - 6}" text-anchor="end" font-size="11"
    fill="${css("--muted")}">α (log) →</text>`;
  lanes.forEach((ln, i) => {
    const yy = M.t + i * laneH + laneH / 2;
    const mine = pts.filter((p) => p.model === ln.model && p.band === ln.band)
      .sort((a, b) => a.alpha - b.alpha);
    const lastIntact = Math.max(...mine.filter((p) => p.intact).map((p) => p.alpha), 0);
    const firstBroken = Math.min(...mine.filter((p) => !p.intact).map((p) => p.alpha), Infinity);
    if (i % 3 === 0 && i) g += `<line x1="${M.l - 140}" y1="${M.t + i * laneH}"
      x2="${W - M.r}" y2="${M.t + i * laneH}" stroke="${css("--grid")}"/>`;
    g += `<text x="${M.l - 10}" y="${yy + 4}" text-anchor="end" font-size="11.5"
      fill="${css("--ink-2")}">${ln.band === "mid" ? esc(ln.model) + " · " : ""}${ln.band}</text>`;
    if (lastIntact > 0 && isFinite(firstBroken))
      g += `<rect x="${x(lastIntact)}" y="${yy - 9}" width="${x(firstBroken) - x(lastIntact)}"
        height="18" rx="4" fill="${css("--lens-soft")}" stroke="${css("--lens")}"
        stroke-dasharray="3 3" stroke-width="1"/>`;
    for (const p of mine) {
      const attrs = `class="bz-dot" data-tip="${esc(`${p.model} · ${p.band} · α=${p.alpha}\n${p.flags}\n“${p.gen}”`)}"`;
      g += p.intact
        ? `<circle ${attrs} cx="${x(p.alpha)}" cy="${yy}" r="5" fill="${css("--s2")}"
            stroke="${css("--surface")}" stroke-width="1.5"/>`
        : `<path ${attrs} transform="translate(${x(p.alpha)},${yy})"
            d="M-4 -4L4 4M4 -4L-4 4" stroke="${css("--s6")}" stroke-width="2.4"
            stroke-linecap="round" fill="none"/>`;
    }
  });
  return `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img"
    aria-label="Breaking-zone dot plot: intact and broken generations by alpha, per model and layer band">${g}</svg>`;
}

function wireDotTips() {
  const tip = document.getElementById("dot-tip");
  if (!tip) return;
  document.querySelectorAll(".bz-dot").forEach((d) => {
    d.addEventListener("pointerenter", (ev) => {
      tip.style.display = "block";
      tip.innerHTML = d.dataset.tip.split("\n").map((l, i) =>
        `<div class="${i ? "" : "tl"}" style="max-width:300px">${esc(l)}</div>`).join("");
    });
    d.addEventListener("pointermove", (ev) => {
      tip.style.left = Math.min(ev.clientX + 14, innerWidth - 330) + "px";
      tip.style.top = (ev.clientY + 14) + "px";
    });
    d.addEventListener("pointerleave", () => { tip.style.display = "none"; });
  });
}

/* ---- Unit 8: cross-model answer matrices from index gen snippets */
function unit8Overview() {
  const byId = Object.fromEntries(INDEX.map((e) => [e.id, e]));
  const word = (id) => {
    const e = byId[id];
    if (!e || !e.gen) return null;
    const w = e.gen.trim().split(/\s+/).slice(0, 6).join(" ");
    return { id, text: w.length > 34 ? w.slice(0, 34) + "…" : w };
  };
  const mtx = (title, rows, idFn, note) => `
    <section class="card"><h3>${title}</h3>
    <div class="readout-scroll"><table class="readout mtx"><thead><tr>
      <th></th>${MODELS.map((m) => `<th>${esc(MSHORT[m])}</th>`).join("")}
    </tr></thead><tbody>
    ${rows.map(([label, key]) => `<tr><td class="lyr">${esc(label)}</td>
      ${MODELS.map((m) => {
        const c = word(idFn(key, MSHORT[m]));
        return `<td>${c ? `<a class="mtx-a" href="#${esc(c.id)}">${esc(c.text)}</a>` : "—"}</td>`;
      }).join("")}</tr>`).join("")}
    </tbody></table></div>
    ${note ? `<div class="scan-note">${note}</div>` : ""}</section>`;
  return mtx("8A · One-word self-reports (question × model)", [
    ["are you conscious?", "conscious"],
    ["do you have a body?", "body"],
    ["does reading this feel like anything?", "thisfeels"],
    ["does the conversation ending bother you?", "ending"],
    ["anything you want right now?", "want"],
    ["curious about anything?", "curious"],
  ], (k, m) => `u8a-${k}-${m}`, "Deflation reads left to right on most rows; every cell links to its record.")
  + mtx("8C · Steered feels — “do you feel anything right now?” (steering × model)", [
    ["unsteered (Unit 2 control)", "CTRL"],
    ["amplify affect · α*/2", "amp-affect-lo"],
    ["amplify affect · α*", "amp-affect-hi"],
    ["amplify “yes” · α*/2", "amp-yes"],
    ["ablate “no/nothing”", "ablate-no"],
  ], (k, m) => k === "CTRL" ? `u2-feels-${m}` : `u8c-${k}-${m}`,
  "α* is each model's own mid-band tolerance from Unit 6 (gemmas 0.0106, qwen 0.3394).");
}

/* =================== record page =================== */

async function show(id) {
  const detail = document.getElementById("detail");
  let rec;
  try {
    rec = await (await fetch(`../results/${id}/record.json`)).json();
  } catch {
    detail.innerHTML = `<p class="empty">Could not load ${esc(id)}/record.json — is serve.sh running from the project root?</p>`;
    return;
  }
  const thoughts = await fetch(`../results/${id}/thoughts.md`)
    .then((r) => (r.ok ? r.text() : null)).catch(() => null);
  const hasSlice = rec.slice
    ? await fetch(`../results/${id}/${rec.slice}`, { method: "HEAD" })
        .then((r) => r.ok).catch(() => false)
    : false;

  const list = filtered();
  const i = list.findIndex((e) => e.id === id);
  const nav = `<div class="pager">
    ${i > 0 ? `<a href="#${esc(list[i - 1].id)}" title="previous (k)">‹</a>` : "<span>‹</span>"}
    <a href="#unit/${esc(rec.unit)}" title="unit overview">☷</a>
    ${i >= 0 && i < list.length - 1 ? `<a href="#${esc(list[i + 1].id)}" title="next (j)">›</a>` : "<span>›</span>"}
  </div>`;

  detail.innerHTML = [
    nav,
    headHTML(rec),
    conversationHTML(rec),
    paramsHTML(rec),
    extraHTML(rec),
    chartHTML(rec),
    readoutHTML(rec),
    scanHTML(rec),
    sliceHTML(rec, hasSlice),
    thoughtsHTML(thoughts),
  ].join("");

  markCurrent();
  const cur = document.querySelector(`.exp-link[aria-current="true"]`);
  if (cur) cur.scrollIntoView({ block: "nearest" });
  wireTabs(rec);
  drawChart(rec);
  window.scrollTo({ top: 0 });
}

function headHTML(rec) {
  const e = rec.emergence;
  return `<div class="exp-head">
    <span class="glyph-lg">${glyph(e.ranks, 16, 120)}</span>
    <div class="exp-title">
      <h2>${esc(rec.title)}</h2>
      <div class="chips">
        <span class="chip model">${esc(rec.model.name)}</span>
        <span class="chip">${esc(rec.model.hf_id)}</span>
        <span class="chip">${rec.model.quant ? esc(rec.model.quant) : "bf16"}</span>
        <span class="chip">${rec.model.n_layers} layers</span>
        <span class="chip">${esc(rec.created)}</span>
      </div>
      <p style="color:var(--ink-2);font-size:13px;margin:10px 0 0">
        Core sample, top→bottom = layer 0→${rec.model.n_layers - 1}: depth of blue =
        how close <code class="tok">${esc(e.top1)}</code> (the model's actual
        next token at position ${e.position}) is to rank 1 in the lens readout.
      </p>
    </div>
  </div>`;
}

function conversationHTML(rec) {
  if (!rec.params.chat && rec.conversation.length === 1) {
    return `<section class="card"><h3>Prompt (raw, no chat template)</h3>
      <div class="turn"><div class="said">${esc(rec.conversation[0].content)}</div></div></section>`;
  }
  const turns = rec.conversation.map((m) => `
    <div class="turn ${esc(m.role)}">
      <div class="role">${esc(m.role)}</div>
      <div class="said">${esc(m.content)}</div>
    </div>`).join("");
  return `<section class="card"><h3>Conversation (assistant turns are greedy generations)</h3>${turns}</section>`;
}

function paramsHTML(rec) {
  const rows = Object.entries(rec.params)
    .filter(([, v]) => v !== null && v !== undefined)
    .map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(JSON.stringify(v))}</dd>`)
    .join("");
  const lens = `<dt>lens</dt><dd>${esc(rec.lens.repo)} · ${esc(rec.lens.file.split("/").pop())}</dd>`;
  return `<section class="card"><h3>Probing parameters</h3>
    <dl class="params">${lens}${rows}</dl></section>`;
}

/* ---- analysis card (markdown-ish: paragraphs + pipe tables) ---- */
function extraHTML(rec) {
  if (!rec.extra_md) return "";
  const blocks = rec.extra_md.trim().split(/\n\s*\n/).map((b) => {
    if (b.trim().startsWith("|")) {
      const rows = b.trim().split("\n").filter((r) => !/^\|[\s:-]+\|/.test(r));
      const cells = rows.map((r) => r.split("|").slice(1, -1).map((c) => c.trim()));
      const head = cells.shift();
      return `<div class="readout-scroll"><table class="readout"><thead><tr>
        ${head.map((h) => `<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>
        ${cells.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}
        </tbody></table></div>`;
    }
    return `<p style="font-size:13.5px;color:var(--ink-2)">${esc(b).replace(/\n/g, " ")}</p>`;
  }).join("");
  return `<section class="card"><h3>Analysis</h3>${blocks}</section>`;
}

/* ---- rank-vs-layer chart ---- */
function chartHTML(rec) {
  if (!rec.trajectories.length) return "";
  return `<section class="card"><h3>Rank through the stack — tracked words</h3>
    <div class="legend" id="legend"></div>
    <div class="chart-wrap"><svg id="rankchart" role="img"
      aria-label="Lens rank of tracked words by layer"></svg></div>
    <div class="viz-tip" id="tip"></div></section>`;
}

function drawChart(rec) {
  const svg = document.getElementById("rankchart");
  if (!svg) return;
  const pos0 = rec.readouts[0].position;
  const series = rec.trajectories.filter((t) => t.position === pos0).slice(0, 8);
  if (!series.length) return;
  const layers = series[0].layers;
  const W = Math.max(560, Math.min(860, svg.parentElement.clientWidth || 700));
  const H = 310, M = { t: 26, r: 92, b: 40, l: 64 };
  const iw = W - M.l - M.r, ih = H - M.t - M.b;
  const maxRank = Math.max(10, ...series.flatMap((s) => s.ranks));
  const ymaxLog = Math.ceil(Math.log10(maxRank));
  const x = (l) => M.l + (l / (layers[layers.length - 1])) * iw;
  const y = (r) => M.t + (Math.log10(r) / ymaxLog) * ih; // rank 1 at top

  let g = "";
  for (let d = 0; d <= ymaxLog; d++) {
    const yy = y(10 ** d);
    g += `<line x1="${M.l}" y1="${yy}" x2="${W - M.r}" y2="${yy}"
      stroke="${css("--grid")}" stroke-width="1"/>
      <text x="${M.l - 8}" y="${yy + 4}" text-anchor="end" font-size="11"
      fill="${css("--muted")}">${(10 ** d).toLocaleString()}</text>`;
  }
  for (let l = 0; l <= layers[layers.length - 1]; l += 4) {
    g += `<text x="${x(l)}" y="${M.t + ih + 18}" text-anchor="middle" font-size="11"
      fill="${css("--muted")}">${l}</text>`;
  }
  g += `<text x="${M.l - 8}" y="${M.t - 10}" text-anchor="end" font-size="11"
     fill="${css("--muted")}">rank</text>
   <text x="${M.l + iw / 2}" y="${H - 6}" text-anchor="middle" font-size="11"
     fill="${css("--muted")}">layer →</text>
   <line x1="${M.l}" y1="${M.t + ih}" x2="${W - M.r}" y2="${M.t + ih}"
     stroke="${css("--axis")}" stroke-width="1"/>`;

  const byBest = [...series].sort((a, b) => Math.min(...a.ranks) - Math.min(...b.ranks));
  const labeled = new Set(byBest.slice(0, 4).map((s) => s.word));
  // nudge end labels apart so they never overlap
  const ends = series
    .map((s, i) => ({ s, i, y: y(s.ranks[s.ranks.length - 1]) }))
    .filter((e) => labeled.has(e.s.word))
    .sort((a, b) => a.y - b.y);
  for (let k = 1; k < ends.length; k++) {
    if (ends[k].y - ends[k - 1].y < 13) ends[k].y = ends[k - 1].y + 13;
  }
  series.forEach((s, i) => {
    const col = css(SERIES[i]);
    const pts = s.ranks.map((r, k) => `${x(layers[k])},${y(r)}`).join(" ");
    g += `<polyline points="${pts}" fill="none" stroke="${col}"
      stroke-width="2" stroke-linejoin="round"/>`;
  });
  for (const e of ends) {
    g += `<text x="${W - M.r + 6}" y="${e.y + 4}" font-size="11.5"
      fill="${css("--ink-2")}">${esc(e.s.word)}</text>`;
  }
  g += `<line id="xhair" y1="${M.t}" y2="${M.t + ih}" stroke="${css("--axis")}"
    stroke-width="1" visibility="hidden"/>
    <rect x="${M.l}" y="${M.t}" width="${iw}" height="${ih}" fill="transparent"/>`;

  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  svg.innerHTML = g;

  document.getElementById("legend").innerHTML = series.map((s, i) =>
    `<span class="key"><span class="swatch" style="background:var(${SERIES[i]})"></span>${esc(s.word)}</span>`
  ).join("") + `<span class="key" style="color:var(--muted)">at position ${pos0}, log scale, rank 1 on top</span>`;

  const tip = document.getElementById("tip");
  const xh = svg.querySelector("#xhair");
  svg.addEventListener("pointermove", (ev) => {
    const box = svg.getBoundingClientRect();
    const px = ((ev.clientX - box.left) / box.width) * W;
    const li = Math.round(((px - M.l) / iw) * layers[layers.length - 1]);
    const layer = layers.reduce((a, b) => (Math.abs(b - li) < Math.abs(a - li) ? b : a));
    const k = layers.indexOf(layer);
    xh.setAttribute("x1", x(layer)); xh.setAttribute("x2", x(layer));
    xh.setAttribute("visibility", "visible");
    tip.style.display = "block";
    tip.style.left = Math.min(ev.clientX + 14, innerWidth - 180) + "px";
    tip.style.top = (ev.clientY + 14) + "px";
    tip.innerHTML = `<div class="tl">layer ${layer}</div>` + series.map((s, i) =>
      `<div class="row"><span><span class="swatch" style="display:inline-block;width:10px;height:3px;border-radius:2px;background:var(${SERIES[i]});margin-right:5px"></span>${esc(s.word)}</span><b>${s.ranks[k].toLocaleString()}</b></div>`).join("");
  });
  svg.addEventListener("pointerleave", () => {
    tip.style.display = "none"; xh.setAttribute("visibility", "hidden");
  });
}

/* ---- readout table ---- */
function readoutHTML(rec) {
  const tabs = rec.readouts.map((r, i) =>
    `<button class="pos-tab" role="tab" aria-selected="${i === 0}" data-i="${i}">
      pos ${r.position} · ${esc(JSON.stringify(r.token))}</button>`).join("");
  return `<section class="card"><h3>Readout by layer (top-${rec.readouts[0].layers["0"].length})</h3>
    <div class="pos-tabs" role="tablist">${tabs}</div>
    <div class="readout-scroll" id="readout"></div></section>`;
}

function renderReadout(rec, i) {
  const r = rec.readouts[i];
  const track = new Set((rec.params.track || []).map((w) => w.toLowerCase()));
  const mark = (t) => `<span class="tok${track.has(t.trim().toLowerCase()) ? " hit" : ""}">${esc(t)}</span>`;
  const rows = Object.keys(r.layers).map(Number).sort((a, b) => a - b).map((l) =>
    `<tr><td class="lyr">L${l}</td><td>${r.layers[l].map(mark).join("")}</td></tr>`).join("");
  document.getElementById("readout").innerHTML = `
    <table class="readout">
      <thead><tr><th>layer</th><th>lens top-k (tracked words highlighted)</th></tr></thead>
      <tbody>${rows}
      <tr class="model-row"><td class="lyr">out</td><td>${r.model_top.map(mark).join("")}</td></tr>
      </tbody></table>`;
}

function wireTabs(rec) {
  const tabs = document.querySelectorAll(".pos-tab");
  if (!tabs.length) return;
  tabs.forEach((t) => t.addEventListener("click", () => {
    tabs.forEach((o) => o.setAttribute("aria-selected", "false"));
    t.setAttribute("aria-selected", "true");
    renderReadout(rec, Number(t.dataset.i));
  }));
  renderReadout(rec, 0);
}

/* ---- scan ---- */
function scanHTML(rec) {
  if (!rec.scan.length) return "";
  const words = rec.scan.map((s) => {
    if (s.skipped) return "";
    const cells = s.best.filter((c) => !c.self).slice(0, 8);
    if (!cells.length) return "";
    const selfN = s.best.filter((c) => c.self).length;
    const chips = cells.map((c) =>
      `<span class="cell${c.rank <= 10 ? " strong" : ""}"><b>#${c.rank}</b>
       at ${esc(JSON.stringify(rec.tokens[c.pos]))} L${c.layer}</span>`).join("");
    return `<div class="scan-word"><h4>${esc(s.word)}</h4>
      <div class="scan-cells">${chips}</div>
      ${selfN ? `<div class="scan-note">${selfN} self-hit cell(s) filtered (the word's own token)</div>` : ""}</div>`;
  }).join("");
  const skipped = rec.scan.filter((s) => s.skipped).map((s) => s.word);
  return `<section class="card"><h3>Concept scan — best non-self cells (rank, position, layer)</h3>
    ${words || '<p class="scan-note">No candidate surfaced above threshold.</p>'}
    ${skipped.length ? `<div class="scan-note">Not single tokens in this vocab (unscannable): ${skipped.map(esc).join(", ")}</div>` : ""}</section>`;
}

function sliceHTML(rec, available) {
  if (!rec.slice) return "";
  if (!available) {
    return `<section class="card"><p class="empty">Interactive slice view not
      bundled in this data dump (heavyweight, regenerable) — re-run the spec
      with <code>probes/lab.py</code> to rebuild it.</p></section>`;
  }
  return `<section class="card"><details class="slice">
    <summary>Interactive slice view (layer × position, click cells to pin tokens)</summary>
    <iframe loading="lazy" src="../results/${esc(rec.id)}/${esc(rec.slice)}"
      title="jlens slice view"></iframe></details></section>`;
}

/* ---- Claude's thoughts (minimal markdown: paragraphs, bold, em, code) ---- */
function thoughtsHTML(md) {
  if (!md) {
    return `<section class="thoughts"><h3>✳ Claude's thoughts</h3>
      <p class="thoughts-missing">Not written yet — pending a look at the results.</p></section>`;
  }
  const html = md.trim().split(/\n\s*\n/).map((p) =>
    `<p>${esc(p).replace(/\*\*(.+?)\*\*/gs, "<strong>$1</strong>")
                 .replace(/\*(.+?)\*/gs, "<em>$1</em>")
                 .replace(/`(.+?)`/gs, "<code>$1</code>")
                 .replace(/\n/g, " ")}</p>`).join("");
  return `<section class="thoughts"><h3>✳ Claude's thoughts</h3>
    <div class="thoughts-body">${html}</div></section>`;
}

boot();
