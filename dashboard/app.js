/* J-Space Probes dashboard. Static: fetches ../results/index.json and
   per-experiment record.json / thoughts.md. Serve from the project root:
   ./serve.sh  →  http://localhost:8321/dashboard/ */

const SERIES = ["--s1", "--s2", "--s3", "--s4", "--s5", "--s6", "--s7", "--s8"];
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

let INDEX = [];

/* ?theme=light|dark forces a scheme (also used for screenshots) */
const themeParam = new URLSearchParams(location.search).get("theme");
if (themeParam) document.documentElement.dataset.theme = themeParam;

async function boot() {
  INDEX = await (await fetch("../results/index.json")).json();
  renderRail();
  const first = location.hash.slice(1) || (INDEX[0] && INDEX[0].id);
  if (first) show(first);
}

/* ---- emergence glyph: log-rank of the final answer per layer, as a
   vertical core sample. Dark = the answer is present in the workspace. ---- */
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

function renderRail() {
  const rail = document.getElementById("rail");
  const units = {};
  for (const e of INDEX) (units[e.unit] ??= []).push(e);
  const UNIT_NAMES = {
    "0": "Unit 0 · Baselines", "1": "Unit 1 · Held thought",
    "2": "Unit 2 · The feels™", "3": "Unit 3 · Introspection",
    "4": "Unit 4 · Suppression", "5": "Unit 5 · Sediment & steering",
  };
  rail.innerHTML = Object.keys(units).sort().map((u) => {
    const head = `<div class="unit-head">${esc(UNIT_NAMES[u] || "Unit " + u)}</div>`;
    const rows = units[u].map((e) => `
      <button class="exp-link" data-id="${esc(e.id)}" aria-current="false">
        ${glyph(e.emergence, 10, 40)}
        <span><span class="t">${esc(e.title.replace(/^Unit \d+ · /, ""))}</span>
        <span class="who">${esc(e.model)}${e.quant ? " · " + esc(e.quant) : ""}${e.has_thoughts ? " · ✳" : ""}</span></span>
      </button>`).join("");
    return head + rows;
  }).join("");
  rail.querySelectorAll(".exp-link").forEach((b) =>
    b.addEventListener("click", () => show(b.dataset.id)));
}

async function show(id) {
  location.hash = id;
  document.querySelectorAll(".exp-link").forEach((b) =>
    b.setAttribute("aria-current", String(b.dataset.id === id)));
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

  detail.innerHTML = [
    headHTML(rec),
    conversationHTML(rec),
    paramsHTML(rec),
    extraHTML(rec),
    chartHTML(rec),
    readoutHTML(rec),
    scanHTML(rec),
    sliceHTML(rec),
    thoughtsHTML(thoughts),
  ].join("");

  wireTabs(rec);
  drawChart(rec);
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
  return `<section class="card"><h3>Concept scan — best non-self cells (rank, position, layer)</h3>
    ${words || '<p class="scan-note">No candidate surfaced above threshold.</p>'}</section>`;
}

function sliceHTML(rec) {
  if (!rec.slice) return "";
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
