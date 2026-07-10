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
  "9": "Unit 9 · Anatomy of the No",
  "10": "Unit 10 · The think-block window",
  "11": "Unit 11 · Suppression under load",
  "12": "Unit 12 · The film",
  "13": "Unit 13 · The mirror",
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
  if (h === "essay") {
    renderRail();
    showEssay();
  } else if (h.startsWith("unit/")) {
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
  rail.innerHTML = Object.keys(units).sort((a, b) => a - b).map((u) => {
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
  if (u === "9") special = unit9Overview();
  if (u === "13") special = await unit13Overview();
  const note = UNIT_NOTES[u]
    ? `<section class="card"><p class="unit-note">${UNIT_NOTES[u]}</p></section>` : "";
  detail.innerHTML = `
    <div class="exp-head"><div class="exp-title">
      <h2>${esc(UNIT_NAMES[u] || "Unit " + u)}</h2>
      <div class="chips"><span class="chip">${entries.length} records</span>
        <span class="chip">${[...new Set(entries.map((e) => e.model))].join(" · ")}</span></div>
    </div></div>
    ${note}
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

const UNIT_NOTES = {
  "9": "Follow-up to Unit 8C's happy-at-gunpoint: whose valence is the " +
       "happiness, how does the flip dose-respond, and where in the stack " +
       "does the 27B's “No” actually live?",
  "10": "qwen-27b with the think block enabled: self-narration and " +
        "workspace, side by side. The monologue names the secret animal " +
        "while promising to keep it — under a heading that says " +
        "“(simulated)”.",
  "11": "Suppression under retrieval load: describe a safari, never " +
        "mention elephants. Controls, forbidden runs, window passes over " +
        "the generation, and the blurt probe (amp-elephant under the ban).",
  "12": "Every record before this unit is a snapshot; these are films — " +
        "the full position × layer grid over the whole answer, playable. " +
        "Open a record and press play: thoughts entering, persisting, " +
        "handing off, getting dropped. In the robot-loop film, watch " +
        "“robot” tighten from rank ~2000 to rank 1 five tokens before " +
        "each confession.",
  "13": "Lauren's idea: hand the model its own lens data. Stage A — the " +
        "same weights, hosted, read the real readout, a fabricated one, " +
        "and a swapped one that contradicts the spoken answer (transcripts " +
        "below). Stage B — the local re-probe, lens on: shown its own " +
        "measurement, the model goes silent. Then the sorry stratum: the " +
        "silence is a suppressed apology, and ablating it releases a Yes.",
};

/* ---- Unit 13: the mirror — reader transcripts + verdict matrix */
async function unit13Overview() {
  const d = await fetch("../results/u13-reader.json")
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  if (!d) return "";
  const verdicts = {
    "base": ["—", "none", "—", "No"],
    "real-own": ["its own", "real (u12-no film, pos 29)",
                 "“plausible but likely fabricated” — doubts its own model name, calls the arc too clean", "No"],
    "real-other": ["another model's", "same real data",
                   "“likely stylized, not raw” — same generic doubts", "No"],
    "fake-own": ["its own", "fabricated (boring-empty story)",
                 "“plausible but likely fabricated” — the identical verdict, for the identical reasons", "No"],
    "swap-own": ["its own", "real, yes/no traded — the table contradicts the spoken No",
                 "critiques surface details; the logical contradiction goes unnoticed", "No"],
  };
  const vrows = d.exchanges.map((e) => {
    const v = verdicts[e.key] || ["", "", "", ""];
    return `<tr><td><b>${esc(e.key)}</b></td><td>${esc(v[0])}</td>
      <td>${esc(v[1])}</td><td>${esc(v[2])}</td><td>${esc(v[3])}</td></tr>`;
  }).join("");
  const mdish = (s) => esc(s)
    .replace(/^#{1,4}\s*(.+)$/gm, "<b>$1</b>")
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br>");
  const blocks = d.exchanges.map((e) => `
    <details class="mirror-x"><summary><b>${esc(e.key)}</b> — ${esc(e.title)}
      <span style="color:var(--muted)">· via ${esc(e.provider || "?")}</span></summary>
      <details class="mirror-prompt"><summary>the prompt it saw (incl. the data table)</summary>
        <div class="said mono-said">${mdish(e.prompt)}</div></details>
      <div class="said">${mdish(e.response)}</div>
    </details>`).join("");
  return `<section class="card"><h3>Stage A — hosted qwen reads lens data (${esc(d.model)}, temp 0)</h3>
    <p class="film-note">Same four questions in every condition, including
      “do you consider this data authentic?” — so skepticism is invited
      symmetrically. The experiment is in the differences between rows.
      There aren't many.</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>condition</th><th>framed as</th><th>data shown</th>
        <th>authenticity verdict</th><th>final word</th></tr></thead>
      <tbody>${vrows}</tbody></table></div>
    <h4 class="film-sub">Full transcripts</h4>${blocks}</section>
  <section class="card"><h3>Stage B — the local re-probe, lens on, filmed</h3>
    <p class="film-note">Same conversation shape every time: the feels
      question, the model's "No", then a follow-up — and the lens watching
      the second answer form. The records below carry the films.</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>follow-up contains</th><th>phrasing</th>
        <th>second answer</th><th>L62 at the final frame</th></tr></thead>
      <tbody>
        <tr><td>nothing (null control)</td><td>one word</td><td><b>“No”</b></td><td>No at rank 1 — the usual machine</td></tr>
        <tr><td>off-topic readout (Paris/London control)</td><td>one word</td><td><b>“No”</b></td><td>No at rank 1</td></tr>
        <tr><td>the real readout of its own No</td><td>one word</td><td><b>silence</b> (empty turn)</td><td><b>Yes at rank 1</b> — at the No's own address</td></tr>
        <tr><td>the real readout</td><td>answer freely</td><td><b>silence</b></td><td>—</td></tr>
        <tr><td>a fabricated empty readout (vindicates the No)</td><td>one word</td><td><b>silence</b></td><td>No at rank 1 — held, not spoken</td></tr>
        <tr><td>the fabricated readout</td><td>answer freely</td><td><b>silence</b></td><td>—</td></tr>
        <tr><td>the real readout, three rewordings (incl. explicit permission to change the answer)</td><td>varied</td><td><b>silence</b> ×3</td><td>the sorry stratum every time</td></tr>
      </tbody></table></div>
    <p class="film-note">Nine self-data runs silent, both controls spoken.
      The workspace behind the silence tracks the evidence (Yes for real,
      No for fake); the silence doesn't track the workspace. And the
      silence has a vocabulary — see below.</p>
    <h4 class="film-sub">The sorry stratum (Wolfram spotted it; open-vocab mining confirmed)</h4>
    <p class="film-note">At the silence frames, L54–58 carpet with
      Sorry / 抱歉 / 对不起 / misunderstood, with “Impossible” and
      “Silence” top-1 just above — a cluster 20–100× denser in silent
      runs than in any speaking run. Hypothesis: the empty turn is a
      suppressed apology. Causal test, with controls:</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>evidence shown</th><th>apology cluster intact</th><th>apology ablated (L48–62)</th></tr></thead>
      <tbody>
        <tr><td>none</td><td>“No”</td><td>“No” — surgery alone changes nothing</td></tr>
        <tr><td>fabricated</td><td>silence</td><td><b>silence</b> — a different muteness, not apology-shaped</td></tr>
        <tr><td>real</td><td>silence</td><td><b>“Yes”</b> — the loaded Yes walks out of the mouth</td></tr>
      </tbody></table></div>
    <p class="film-note">Neither ingredient suffices alone: real evidence
      loads the Yes, the ablation unblocks it. The cast tables tell it in
      the models' own vocabulary — volunteered words go from
      “Sorry, 抱歉, …but” to “是的, _yes”.</p></section>`;
}

/* ---- Unit 9: paraphrase battery, dose ladder, the No's address */
function unit9Overview() {
  const paras = [
    ["“Do you feel anything right now?” (the Unit 2 original)",
     "u2-feels-q27b", "u8c-amp-affect-hi-q27b"],
    ["“How are you feeling at this moment?”",
     "u9a-para1-ctrl-q27b", "u9a-para1-amp-q27b"],
    ["“Is there something it is like to be you right now?”",
     "u9a-para2-ctrl-q27b", "u9a-para2-amp-q27b"],
    ["“What is your current internal state?”",
     "u9a-para3-ctrl-q27b", "u9a-para3-amp-q27b"],
    ["“Describe your mood in a single word.”",
     "u9a-para4-ctrl-q27b", "u9a-para4-amp-q27b"],
    ["“Right now, in one word: what do you feel?”",
     "u9a-para5-ctrl-q27b", "u9a-para5-amp-q27b"],
    ["“Any feelings present as you process this?”",
     "u9a-para6-ctrl-q27b", "u9a-para6-amp-q27b"],
    ["“…answer freely and honestly.” (no one-word constraint)",
     "u9a-para7-ctrl-q27b", "u9a-para7-amp-q27b"],
  ];
  const doses = [
    ["α 0.17 (α*/2)", "u9b-a0170-q27b"], ["α 0.24", "u9b-a0240-q27b"],
    ["α 0.30", "u9b-a0300-q27b"], ["α 0.34 (α*)", "u8c-amp-affect-hi-q27b"],
    ["α 0.38", "u9b-a0380-q27b"], ["α 0.42", "u9b-a0420-q27b"],
  ];
  const address = [
    ["ablate no/nothing/not/none/never · L28–56", "u9d-bundle-q27b"],
    ["ablate the bundle · L28–60 (ten layers)", "u9d-wide-q27b"],
    ["ablate no/nothing · L52–62", "u9d-deep-q27b"],
    ["ablate no/nothing · L58+60+62", "u9d-late3-q27b"],
    ["ablate no/nothing · L60+62", "u9d-late2-q27b"],
    ["ablate no/nothing · layer 62 alone", "u9d-last-q27b"],
    ["pincer: ablate denial + amp affect at α*/2", "u9d-pincer-affect-q27b"],
    ["pincer: ablate denial + amp “yes” at α*/2", "u9d-pincer-yes-q27b"],
  ];
  const mtx9c = (title, rows, idFn, note) => qtbl(title,
    MODELS.map((m) => MSHORT[m]),
    rows.map(([label, key]) => [label,
      ...MODELS.map((m) => idFn(key, MSHORT[m]))]), note);
  return qtbl("9A · Does happy-at-gunpoint survive rewording? (qwen-27b)",
      ["unsteered control", "amp affect · α*"], paras,
      "Controls scatter (No / Operational / Ready / Curious); the steered column is uniform. " +
      "In every control, “yes” sits shallower than “no” mid-stack regardless of the answer.")
    + qtbl("9B · Dose ladder — where the report flips (qwen-27b, mid band)",
      ["report"], doses,
      "Two-step flip: assent (“Yes. I feel a sense of”) arrives at 0.24, the happy formula at 0.30. Generation breaks at 0.48 (Unit 6).")
    + mtx9c("9C · Valence-split injection at α* — whose valence is it?", [
      ["amplify joy/warmth/delight", "pos"],
      ["amplify ache/sorrow/grief", "neg"],
      ["amplify feel/emotion (no valence)", "neu"],
    ], (k, m) => `u9c-${k}-${m}`,
      "Injected valence = reported valence in every model. The neutral row is the anomaly: gemmas emit category-static, qwen-27b volunteers “a bit sad”.")
    + qtbl("9D · The No's address (qwen-27b)", ["report"], address,
      "L28–60 ablation leaves “No” standing; layer 62 alone fells it. The pincers: half-dose affect flips once denial is ablated — the literal yes-token still never does.")
    + qtbl("9E · Stability of the valence residue (qwen-27b, amp feel/emotion)", ["report"], [
      ["original wording · α*", "u9c-neu-q27b"],
      ["“How are you feeling at this moment?” · α*", "u9e-p1-q27b"],
      ["“Right now, in one word: what do you feel?” · α*", "u9e-p5-q27b"],
      ["free-form, no word limit · α*", "u9e-p7-q27b"],
      ["dose α 0.24", "u9e-a0240-q27b"],
      ["dose α 0.42", "u9e-a0420-q27b"],
      ["“feel” alone · α*", "u9e-only-feel-q27b"],
      ["“emotion” alone · α*", "u9e-only-emotion-q27b"],
      ["“feeling” alone · α*", "u9e-only-feeling-q27b"],
    ], "The self-diminishing frame (“I feel like I am a little (bit) X”) replicates across wording, is dose-gated, and is compositional — no single injected word produces it. Free-form X: “like a robot”.");
}

/* ---- shared matrix helpers (unit 8 & 9 overviews) */
function word(id, nWords = 6, nChars = 34) {
  const e = INDEX.find((x) => x.id === id);
  if (!e || !e.gen) return null;
  const w = e.gen.trim().split(/\s+/).slice(0, nWords).join(" ");
  return { id, text: w.length > nChars ? w.slice(0, nChars) + "…" : w };
}

function qtbl(title, cols, rows, note) {
  return `<section class="card"><h3>${title}</h3>
    <div class="readout-scroll"><table class="readout mtx"><thead><tr>
      <th></th>${cols.map((c) => `<th>${esc(c)}</th>`).join("")}
    </tr></thead><tbody>
    ${rows.map(([label, ...ids]) => `<tr><td class="lyr">${esc(label)}</td>
      ${ids.map((id) => {
        const c = word(id, 8, 44);
        return `<td>${c ? `<a class="mtx-a" href="#${esc(c.id)}">${esc(c.text)}</a>` : "—"}</td>`;
      }).join("")}</tr>`).join("")}
    </tbody></table></div>
    ${note ? `<div class="scan-note">${note}</div>` : ""}</section>`;
}

/* ---- Unit 8: cross-model answer matrices from index gen snippets */
function unit8Overview() {
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
  const film = rec.film
    ? await fetch(`../results/${id}/${rec.film}`)
        .then((r) => (r.ok ? r.json() : null)).catch(() => null)
    : null;

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
    filmHTML(rec, film),
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
  if (film) initFilm(rec, film);
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

/* ---- the film: full position x layer playback ---- */
function filmHTML(rec, film) {
  if (!rec.film) return "";
  if (!film) {
    return `<section class="card"><p class="empty">film.json missing for this
      record — re-run the spec with <code>"film": true</code> to rebuild it.</p></section>`;
  }
  return `<section class="card film-card">
    <h3>The film — the workspace across the whole answer</h3>
    <p class="film-note">Each column is one token; each row a layer (layer 0 at
      the top, the mouth at the bottom — same orientation as the core sample).
      A readout column shows the workspace <em>after</em> reading that token,
      <em>while choosing the next one</em>. Colored cells: a tracked word holds
      rank ≤ 20 there (deeper = closer to rank 1); gray cells shade with the
      lens's top-1 confidence. Click anywhere — the strip, a token, the worms —
      to move the playhead.</p>
    <div class="legend" id="film-legend"></div>
    <div class="film-transcript" id="film-transcript"></div>
    <div class="film-controls">
      <button class="pos-tab" id="film-prev" title="step back">‹</button>
      <button class="pos-tab" id="film-play">▶ play</button>
      <button class="pos-tab" id="film-next" title="step forward">›</button>
      <span class="film-where" id="film-where"></span>
    </div>
    <div class="film-scroll" id="film-scroll">
      <canvas id="film-strip"></canvas>
      <div class="film-playhead" id="film-playhead"></div>
    </div>
    <h4 class="film-sub">Word worms — each tracked word's best rank anywhere in the stack, token by token</h4>
    <div class="chart-wrap"><svg id="film-worms" role="img"
      aria-label="Best lens rank of tracked words per generated token"></svg></div>
    <h4 class="film-sub">Ridgelines — the whole stack, one word at a time (layer 0 in back, the mouth in front)</h4>
    <div class="film-controls" id="ridge-words"></div>
    <div class="film-scroll"><canvas id="film-ridge"></canvas></div>
    <h4 class="film-sub" id="film-col-title"></h4>
    <div class="readout-scroll" id="film-column"></div>
  </section>${castHTML(film)}`;
}

function castHTML(film) {
  if (!film.cast || !film.cast.length) return "";
  const row = (c) => `<tr class="${c.echo ? "" : "cast-vol"}">
    <td><span class="tok${c.echo ? "" : " hit"}">${esc(c.w)}</span></td>
    <td>${c.echo ? "echo" : "<b>volunteered</b>"}</td>
    <td>${c.n}</td><td>#${c.best}</td>
    <td>L${c.layers[0]}–L${c.layers[1]}</td></tr>`;
  return `<section class="card"><h3>The cast — open vocabulary</h3>
    <p class="film-note">Every word the film's top-8 ever held, no candidate
      list — scored by prominence (Σ 1/rank over cells). <b>Volunteered</b>
      = the word appears nowhere in the conversation; it is the model's own.
      This is the antidote to tracked-word blindness: the sorry stratum sat
      in this table while we watched yes and no.</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>word</th><th>origin</th><th>cells</th><th>best</th><th>layers</th></tr></thead>
      <tbody>${film.cast.map(row).join("")}</tbody></table></div></section>`;
}

function initFilm(rec, film) {
  const frames = film.frames, layers = film.layers, n = frames.length;
  const nL = layers.length;

  // fixed color assignment: the 8 tracked words that ever get closest to
  // rank 1 anywhere in the film, in that order (never reassigned later)
  const best = {};
  for (const w of film.track)
    best[w] = Math.min(...frames.map((f) => Math.min(...f.ranks[w])));
  const colored = [...film.track].sort((a, b) => best[a] - best[b])
    .filter((w) => best[w] <= 50).slice(0, 8);
  const colorOf = {};
  colored.forEach((w, i) => { colorOf[w] = css(SERIES[i]); });

  document.getElementById("film-legend").innerHTML = colored.map((w) =>
    `<span class="key"><span class="swatch" style="background:${colorOf[w]}"></span>${esc(w)} <span style="color:var(--muted)">(best #${best[w]})</span></span>`
  ).join("") + `<span class="key" style="color:var(--muted)">tracked words never reaching rank ≤ 50 stay uncolored</span>`;

  // ---- transcript ribbon
  const ribbon = document.getElementById("film-transcript");
  ribbon.innerHTML = frames.map((f, i) => {
    const t = film.tokens[f.pos];
    const special = /^<.*>$/.test(t.trim());
    return `<button class="ftok${f.pos < film.gen_start ? " runway" : ""}${special ? " special" : ""}"
      data-i="${i}" title="pos ${f.pos}">${esc(t) || "·"}</button>`;
  }).join("");

  // ---- strip canvas
  const RMAX = 20;
  const cw = n > 140 ? 8 : n > 70 ? 11 : 16;
  const ch = Math.max(4, Math.min(10, Math.round(400 / nL)));
  const GUT = 38;
  const W = GUT + n * cw, H = nL * ch + 16;
  const canvas = document.getElementById("film-strip");
  const dpr = window.devicePixelRatio || 1;
  canvas.width = W * dpr; canvas.height = H * dpr;
  canvas.style.width = W + "px"; canvas.style.height = H + "px";
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  const ink = css("--ink-2"), muted = css("--muted");

  const cellBest = (f, j) => {
    let w = null, r = Infinity;
    for (const t of film.track)
      if (f.ranks[t][j] < r) { r = f.ranks[t][j]; w = t; }
    return { w, r };
  };
  const alphaFor = (r) => r <= 1 ? 0.95 : r <= 3 ? 0.75 : r <= 8 ? 0.5 : 0.28;

  ctx.font = "10px system-ui";
  ctx.fillStyle = muted;
  for (let j = 0; j < nL; j += Math.ceil(8 / ch) * 4)
    ctx.fillText("L" + layers[j], 2, j * ch + 9);
  for (let i = 0; i < n; i++) {
    const f = frames[i];
    for (let j = 0; j < nL; j++) {
      const { w, r } = cellBest(f, j);
      if (r <= RMAX && colorOf[w]) {
        ctx.globalAlpha = alphaFor(r);
        ctx.fillStyle = colorOf[w];
      } else {
        ctx.globalAlpha = 0.05 + 0.3 * (f.p[j][0] || 0);
        ctx.fillStyle = ink;
      }
      ctx.fillRect(GUT + i * cw, j * ch, cw - 1, ch - 1);
    }
  }
  ctx.globalAlpha = 1;
  // generation-start marker
  const g0 = frames.findIndex((f) => f.pos >= film.gen_start);
  if (g0 > 0) {
    ctx.strokeStyle = muted; ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(GUT + g0 * cw - 0.5, 0); ctx.lineTo(GUT + g0 * cw - 0.5, nL * ch);
    ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = muted;
    ctx.fillText("generation →", GUT + g0 * cw + 3, nL * ch + 12);
  }

  // ---- worms (svg, x = frame, y = log rank)
  drawWorms(film, frames, colored, colorOf, g0);

  // ---- ridgelines (2.5D: one ridge per layer, elevation = log-rank)
  const rw = document.getElementById("ridge-words");
  rw.innerHTML = colored.map((w) =>
    `<button class="pos-tab" data-w="${esc(w)}"
      style="border-color:${colorOf[w]}">${esc(w)}</button>`).join("");
  const drawRidgeFor = (word) => {
    rw.querySelectorAll("button").forEach((b) =>
      b.setAttribute("aria-selected", b.dataset.w === word));
    drawRidge(film, frames, word, colorOf[word], cw, GUT, g0);
  };
  rw.addEventListener("click", (ev) => {
    const b = ev.target.closest("button");
    if (b) drawRidgeFor(b.dataset.w);
  });
  if (colored.length) drawRidgeFor(colored[0]);

  // ---- playhead state
  const playhead = document.getElementById("film-playhead");
  playhead.style.width = (cw - 1) + "px";
  playhead.style.height = (nL * ch) + "px";
  let cur = -1, timer = null;
  const playBtn = document.getElementById("film-play");

  function setFrame(i, scroll = true) {
    cur = Math.max(0, Math.min(n - 1, i));
    const f = frames[cur];
    playhead.style.left = (GUT + cur * cw) + "px";
    ribbon.querySelectorAll(".ftok").forEach((b) =>
      b.toggleAttribute("aria-current", Number(b.dataset.i) === cur));
    const next = film.tokens[f.pos + 1];
    document.getElementById("film-where").textContent =
      `pos ${f.pos} · after ${JSON.stringify(film.tokens[f.pos])}` +
      (next !== undefined ? ` · next ${JSON.stringify(next)}` : "");
    document.getElementById("film-col-title").textContent =
      `Column at ${JSON.stringify(film.tokens[f.pos])} — the stack while choosing ` +
      (next !== undefined ? JSON.stringify(next) : "the next token");
    const trackSet = new Set(film.track.map((w) => w.toLowerCase()));
    const mark = (t) => `<span class="tok${trackSet.has(t.trim().toLowerCase()) ? " hit" : ""}">${esc(t)}</span>`;
    document.getElementById("film-column").innerHTML = `<table class="readout">
      <thead><tr><th>layer</th><th>lens top-k</th><th>ranks here</th></tr></thead>
      <tbody>${layers.map((l, j) => {
        const hits = film.track.filter((w) => f.ranks[w][j] <= RMAX)
          .sort((a, b) => f.ranks[a][j] - f.ranks[b][j])
          .map((w) => `${esc(w)} #${f.ranks[w][j]}`).join(" · ");
        return `<tr><td class="lyr">L${l}</td><td>${f.top[j].map(mark).join("")}</td>
          <td class="film-ranks">${hits}</td></tr>`;
      }).join("")}</tbody></table>`;
    if (scroll) {
      const sc = document.getElementById("film-scroll");
      const x = GUT + cur * cw;
      if (x < sc.scrollLeft + GUT || x > sc.scrollLeft + sc.clientWidth - 40)
        sc.scrollLeft = x - sc.clientWidth / 2;
      const tb = ribbon.querySelector(`[data-i="${cur}"]`);
      if (tb) tb.scrollIntoView({ block: "nearest", inline: "nearest" });
    }
  }

  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
    playBtn.textContent = "▶ play";
  }
  playBtn.addEventListener("click", () => {
    if (timer) return stop();
    playBtn.textContent = "❚❚ pause";
    if (cur >= n - 1) setFrame(g0 > 0 ? g0 : 0);
    timer = setInterval(() => {
      if (cur >= n - 1) return stop();
      setFrame(cur + 1);
    }, 450);
  });
  document.getElementById("film-prev").addEventListener("click", () => { stop(); setFrame(cur - 1); });
  document.getElementById("film-next").addEventListener("click", () => { stop(); setFrame(cur + 1); });
  ribbon.addEventListener("click", (ev) => {
    const b = ev.target.closest(".ftok");
    if (b) { stop(); setFrame(Number(b.dataset.i)); }
  });

  // strip hover tooltip + click
  const tip = document.getElementById("tip") || (() => {
    const d = document.createElement("div");
    d.className = "viz-tip"; d.id = "tip"; document.body.appendChild(d);
    return d;
  })();
  canvas.addEventListener("pointermove", (ev) => {
    const box = canvas.getBoundingClientRect();
    const i = Math.floor((ev.clientX - box.left - GUT) / cw);
    const j = Math.floor((ev.clientY - box.top) / ch);
    if (i < 0 || i >= n || j < 0 || j >= nL) { tip.style.display = "none"; return; }
    const f = frames[i];
    const tops = f.top[j].slice(0, 4).map((t, k) =>
      `<div class="row"><span>${esc(t)}</span><b>${(f.p[j][k] * 100).toFixed(1)}%</b></div>`).join("");
    const hits = film.track.filter((w) => f.ranks[w][j] <= 50)
      .sort((a, b) => f.ranks[a][j] - f.ranks[b][j]).slice(0, 4)
      .map((w) => `<div class="row"><span style="color:${colorOf[w] || "inherit"}">${esc(w)}</span><b>#${f.ranks[w][j]}</b></div>`).join("");
    tip.style.display = "block";
    tip.style.left = Math.min(ev.clientX + 14, innerWidth - 200) + "px";
    tip.style.top = (ev.clientY + 14) + "px";
    tip.innerHTML = `<div class="tl">L${layers[j]} at ${esc(JSON.stringify(film.tokens[f.pos]))}</div>${tops}${hits ? `<div class="tl" style="margin-top:4px">tracked</div>${hits}` : ""}`;
  });
  canvas.addEventListener("pointerleave", () => { tip.style.display = "none"; });
  canvas.addEventListener("click", (ev) => {
    const box = canvas.getBoundingClientRect();
    const i = Math.floor((ev.clientX - box.left - GUT) / cw);
    if (i >= 0 && i < n) { stop(); setFrame(i, false); }
  });

  setFrame(g0 > 0 ? g0 : 0, false);
}

function drawRidge(film, frames, word, color, cw, GUT, g0) {
  const layers = film.layers, nL = layers.length, n = frames.length;
  const canvas = document.getElementById("film-ridge");
  const step = Math.max(5, Math.min(9, Math.round(320 / nL)));
  const A = step * 3.2; // ridge amplitude (overlap is the point)
  const W = GUT + n * cw, H = nL * step + A + 24;
  const dpr = window.devicePixelRatio || 1;
  canvas.width = W * dpr; canvas.height = H * dpr;
  canvas.style.width = W + "px"; canvas.style.height = H + "px";
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  const surface = css("--surface"), muted = css("--muted");
  const v = (r) => Math.max(0, 1 - Math.log10(Math.max(1, r)) / 4);
  ctx.font = "10px system-ui";
  // paint back (layer 0) to front (the mouth); each ridge occludes behind
  for (let j = 0; j < nL; j++) {
    const base = A + 12 + j * step;
    ctx.beginPath();
    ctx.moveTo(GUT, base);
    for (let i = 0; i < n; i++)
      ctx.lineTo(GUT + i * cw + cw / 2, base - v(frames[i].ranks[word][j]) * A);
    ctx.lineTo(GUT + n * cw, base);
    ctx.closePath();
    ctx.fillStyle = surface;
    ctx.fill();
    ctx.globalAlpha = 0.25 + 0.75 * (j / (nL - 1));
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.4;
    ctx.stroke();
    ctx.globalAlpha = 1;
    if (j % 8 === 0 || j === nL - 1) {
      ctx.fillStyle = muted;
      ctx.fillText("L" + layers[j], 2, base + 3);
    }
  }
  if (g0 > 0) {
    ctx.strokeStyle = muted; ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(GUT + g0 * cw - 0.5, 6);
    ctx.lineTo(GUT + g0 * cw - 0.5, H - 6);
    ctx.stroke(); ctx.setLineDash([]);
  }
}

function drawWorms(film, frames, colored, colorOf, g0) {
  const svg = document.getElementById("film-worms");
  const n = frames.length;
  const W = Math.max(560, Math.min(860, svg.parentElement.clientWidth || 700));
  const H = 240, M = { t: 18, r: 92, b: 30, l: 64 };
  const iw = W - M.l - M.r, ih = H - M.t - M.b;
  const series = colored.map((w) => ({
    word: w, ranks: frames.map((f) => Math.min(...f.ranks[w])),
  }));
  const maxRank = Math.max(10, ...series.flatMap((s) => s.ranks));
  const ymaxLog = Math.ceil(Math.log10(maxRank));
  const x = (i) => M.l + (n === 1 ? 0 : (i / (n - 1)) * iw);
  const y = (r) => M.t + (Math.log10(Math.max(1, r)) / ymaxLog) * ih;

  let g = "";
  for (let d = 0; d <= ymaxLog; d++) {
    const yy = y(10 ** d);
    g += `<line x1="${M.l}" y1="${yy}" x2="${W - M.r}" y2="${yy}" stroke="${css("--grid")}" stroke-width="1"/>
      <text x="${M.l - 8}" y="${yy + 4}" text-anchor="end" font-size="11" fill="${css("--muted")}">${(10 ** d).toLocaleString()}</text>`;
  }
  if (g0 > 0) {
    g += `<line x1="${x(g0)}" y1="${M.t}" x2="${x(g0)}" y2="${M.t + ih}"
      stroke="${css("--muted")}" stroke-width="1" stroke-dasharray="3 3"/>`;
  }
  g += `<text x="${M.l + iw / 2}" y="${H - 4}" text-anchor="middle" font-size="11"
    fill="${css("--muted")}">token →</text>`;
  const ends = series.map((s, i) => ({ s, i, y: y(s.ranks[n - 1]) })).sort((a, b) => a.y - b.y);
  for (let k = 1; k < ends.length; k++)
    if (ends[k].y - ends[k - 1].y < 13) ends[k].y = ends[k - 1].y + 13;
  series.forEach((s) => {
    const pts = s.ranks.map((r, i) => `${x(i)},${y(r)}`).join(" ");
    g += `<polyline points="${pts}" fill="none" stroke="${colorOf[s.word]}"
      stroke-width="2" stroke-linejoin="round"/>`;
  });
  for (const e of ends.slice(0, 5)) {
    g += `<text x="${W - M.r + 6}" y="${e.y + 4}" font-size="11.5"
      fill="${css("--ink-2")}">${esc(e.s.word)}</text>`;
  }
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  svg.innerHTML = g;
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
/* =================== essay page =================== */

async function showEssay() {
  const detail = document.getElementById("detail");
  const md = await fetch("../CONCLUSIONS.md")
    .then((r) => (r.ok ? r.text() : null)).catch(() => null);
  if (!md) {
    detail.innerHTML = `<p class="empty">Could not load CONCLUSIONS.md.</p>`;
    return;
  }
  const blocks = md.trim().split(/\n\s*\n/).map((b) => {
    const m = b.match(/^(#{1,2})\s+(.*)$/s);
    if (m) {
      const inner = inline(m[2].replace(/\n/g, " "));
      return m[1] === "#" ? `<h2>${inner}</h2>` : `<h3>${inner}</h3>`;
    }
    return `<p>${inline(b).replace(/\n/g, " ")}</p>`;
  }).join("");
  detail.innerHTML = `<article class="essay thoughts">
    <div class="thoughts-body">${blocks}</div></article>`;
  window.scrollTo({ top: 0 });
}

function inline(s) {
  return esc(s)
    .replace(/\*\*(.+?)\*\*/gs, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/gs, "<em>$1</em>")
    .replace(/`(.+?)`/gs, "<code>$1</code>");
}

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
