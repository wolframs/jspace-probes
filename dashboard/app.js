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
  "14": "Unit 14 · The long game",
  "15": "Unit 15 · Workspace span",
};
const MODELS = ["gemma-4b", "gemma-12b", "qwen-27b"];
const MSHORT = { "gemma-4b": "g4b", "gemma-12b": "g12b", "qwen-27b": "q27b" };

let INDEX = [];
let BOARD = null; // cached ../board/board.json, fetched lazily by showBoard()
let modelFilter = "all";
let query = "";
const expanded = new Set();

/* theme: ?theme=light|dark (screenshots, wins but never persists) >
   localStorage (the toggle) > OS preference */
const themeParam = new URLSearchParams(location.search).get("theme");
{
  const t = themeParam || localStorage.getItem("theme");
  if (t) document.documentElement.dataset.theme = t;
  // screenshot mode: freeze entry animations so captures are deterministic
  if (themeParam) document.documentElement.classList.add("no-anim");
}
function currentTheme() {
  return document.documentElement.dataset.theme ||
    (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
}
function paintThemeButton() {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;
  const dark = currentTheme() === "dark";
  btn.textContent = dark ? "☀" : "☾";
  btn.setAttribute("aria-label", `Switch to ${dark ? "light" : "dark"} theme`);
}
function toggleTheme() {
  const next = currentTheme() === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  localStorage.setItem("theme", next);
  paintThemeButton();
  drawSpark();
}

/* the masthead signature: a sparkline core-sample of u2-feels-q27b — the
   answer ("No") surfacing through the layer stack, the lab's first headline.
   Drawn from INDEX data already in memory; progressive reveal unless
   reduced motion is preferred. */
function drawSpark() {
  const link = document.getElementById("mast-spark-link");
  const canvas = document.getElementById("mast-spark");
  if (!link || !canvas) return;
  const e = INDEX.find((x) => x.id === "u2-feels-q27b");
  const ranks = e && (Array.isArray(e.emergence) ? e.emergence : e.emergence?.ranks);
  if (!ranks || ranks.length < 2) { link.hidden = true; return; }
  link.hidden = false;
  link.title = `${e.title} — the lab's emblem: the first thing the lens showed us, ` +
    `the answer surfacing layer by layer. (The actual headliners wear a ★ on the findings map.)`;
  const dpr = window.devicePixelRatio || 1;
  const W = 220, H = 30;
  canvas.width = W * dpr; canvas.height = H * dpr;
  canvas.style.width = `${W}px`; canvas.style.height = `${H}px`;
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  const color = css("--lens");
  const logMax = Math.log(Math.max(2, ...ranks));
  const closeness = ranks.map((r) => 1 - Math.log(Math.max(1, r)) / logMax);
  const px = (i) => 2 + (i / (ranks.length - 1)) * (W - 4);
  const py = (c) => H - 3 - Math.max(0, c) * (H - 8);
  const drawUpTo = (frac) => {
    ctx.clearRect(0, 0, W, H);
    const n = Math.max(2, Math.floor(ranks.length * frac));
    ctx.beginPath();
    ctx.moveTo(px(0), H - 3);
    for (let i = 0; i < n; i++) ctx.lineTo(px(i), py(closeness[i]));
    ctx.lineTo(px(n - 1), H - 3);
    ctx.closePath();
    ctx.globalAlpha = 0.16; ctx.fillStyle = color; ctx.fill();
    ctx.globalAlpha = 1;
    ctx.beginPath();
    for (let i = 0; i < n; i++) i ? ctx.lineTo(px(i), py(closeness[i])) : ctx.moveTo(px(0), py(closeness[0]));
    ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.stroke();
  };
  if (themeParam || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    drawUpTo(1); return; // deterministic for screenshots / reduced motion
  }
  const t0 = performance.now(), DUR = 900;
  (function step(t) {
    const frac = Math.min(1, (t - t0) / DUR);
    drawUpTo(frac);
    if (frac < 1) requestAnimationFrame(step);
  })(t0);
}

/* ---- atmosphere: a full-page sediment field behind the content, drawn
   from the REAL emergence curves of the records — each faint column is one
   record's core sample; every few seconds one random column "surfaces"
   bottom-up (an answer emerging), the lab's heartbeat. Controlled from the
   console; static under reduced motion or ?theme= (screenshots). ---- */
const lsNum = (k, d) => {
  const v = localStorage.getItem(k);
  return v === null || isNaN(+v) ? d : +v;
};
const ATMO = {
  on: localStorage.getItem("atmo") !== "off",
  intensity: Math.min(1, Math.max(0, lsNum("atmo-int", 35) / 100)),
  speed: Math.min(2, Math.max(0, lsNum("atmo-speed", 100) / 100)),
  cols: [], raf: 0, last: 0, pulse: null, nextPulse: 4,
  driftX: 0, tPrev: null, // drift is INTEGRATED (pos += dt·speed) so the
};                        // slider changes velocity, not position
function atmoStatic() {
  return themeParam || matchMedia("(prefers-reduced-motion: reduce)").matches;
}
function atmoResample() {
  const pool = INDEX.filter((e) => Array.isArray(e.emergence) && e.emergence.length > 6);
  ATMO.cols = [];
  if (!pool.length) return;
  // a skyline of core samples standing on the bottom edge: fewer, chunkier,
  // visibly banded — golden-ratio spacing keeps coverage even without a grid
  const N = window.innerWidth < 800 ? 22 : 44;
  const PHI = 0.6180339887;
  for (let i = 0; i < N; i++) {
    const e = pool[(Math.random() * pool.length) | 0];
    const logMax = Math.log(Math.max(2, ...e.emergence));
    ATMO.cols.push({
      c: e.emergence.map((r) => 1 - Math.log(Math.max(1, r)) / logMax),
      x: (i * PHI + Math.random() * 0.4 * PHI) % 1,
      w: 7 + Math.random() * 9,
      hf: 0.22 + Math.random() * 0.5,   // column height as fraction of viewport
      base: 0.55 + Math.random() * 0.45, // per-column presence
      ph: Math.random() * Math.PI * 2,
    });
  }
}
function atmoFrame(tms) {
  const canvas = document.getElementById("atmo");
  if (!canvas) return;
  const t = tms / 1000;
  const dpr = Math.min(1.5, window.devicePixelRatio || 1);
  const W = window.innerWidth, H = window.innerHeight;
  if (canvas.width !== (W * dpr) | 0) {
    canvas.width = W * dpr; canvas.height = H * dpr;
  }
  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, W, H);
  if (!ATMO.on || ATMO.intensity <= 0 || !ATMO.cols.length) return;
  const color = css("--lens");
  const moving = !atmoStatic() && ATMO.speed > 0;
  // heartbeat: pick a column to surface, bottom-up, every 5–12 s
  if (!atmoStatic()) {
    if (!ATMO.pulse && t > ATMO.nextPulse) {
      ATMO.pulse = { i: (Math.random() * ATMO.cols.length) | 0, t0: t, dur: 2.4 };
    }
    if (ATMO.pulse && t - ATMO.pulse.t0 > ATMO.pulse.dur) {
      ATMO.pulse = null;
      ATMO.nextPulse = t + 5 + Math.random() * 7;
    }
  }
  ctx.fillStyle = color;
  if (moving && ATMO.tPrev !== null && t > ATMO.tPrev) {
    ATMO.driftX = (ATMO.driftX + (t - ATMO.tPrev) * 0.0016 * ATMO.speed) % 1;
  }
  ATMO.tPrev = t;
  for (let ci = 0; ci < ATMO.cols.length; ci++) {
    const col = ATMO.cols[ci];
    const x = ((col.x + ATMO.driftX) % 1) * (W + 60) - 30;
    const n = col.c.length;
    const colH = H * col.hf;
    const y0 = H - colH;                    // layer 0 at the column's top,
    const bandH = colH / n;                 // the mouth at the ground
    const gap = Math.min(1.5, bandH * 0.25); // visible banding = core sample
    const wob = moving ? 0.82 + 0.18 * Math.sin(t * 0.3 + col.ph) : 1;
    const pulsing = ATMO.pulse && ATMO.pulse.i === ci;
    const p = pulsing ? (t - ATMO.pulse.t0) / ATMO.pulse.dur : 0;
    // faint backbone so the column silhouette reads even where ranks are cold
    ctx.globalAlpha = Math.min(0.5, 0.028 * ATMO.intensity * col.base * wob * 3);
    ctx.fillRect(x, y0, col.w, colH);
    for (let i = 0; i < n; i++) {
      let a = (0.03 + col.c[i] * 0.30) * ATMO.intensity * col.base * wob;
      // the surfacing pulse sweeps down through depth toward the mouth
      if (pulsing) {
        const front = p * 1.25 * n;
        const d = Math.abs(i - front);
        if (i < front) a += 0.5 * ATMO.intensity * Math.max(0, 1 - p) * Math.exp(-d / (n * 0.25));
      }
      if (a <= 0.004) continue;
      ctx.globalAlpha = Math.min(0.6, a);
      ctx.fillRect(x, y0 + i * bandH, col.w, Math.max(0.75, bandH - gap));
    }
  }
  ctx.globalAlpha = 1;
}
function atmoLoop(tms) {
  if (tms - ATMO.last >= 33) { ATMO.last = tms; atmoFrame(tms); }
  ATMO.raf = requestAnimationFrame(atmoLoop);
}
function atmoStart() {
  cancelAnimationFrame(ATMO.raf);
  if (!ATMO.cols.length) atmoResample();
  if (atmoStatic() || !ATMO.on) { atmoFrame(8000); return; }
  ATMO.raf = requestAnimationFrame(atmoLoop);
}
document.addEventListener("visibilitychange", () => {
  if (document.hidden) cancelAnimationFrame(ATMO.raf);
  else atmoStart();
});

/* ---- lab console ---- */
function conPaint() {
  const saved = localStorage.getItem("theme") || "";
  document.querySelectorAll("#con-theme button").forEach((b) =>
    b.setAttribute("aria-pressed", String((b.dataset.t || "") === saved)));
  document.querySelectorAll("#con-atmo button").forEach((b) =>
    b.setAttribute("aria-pressed", String((b.dataset.a === "on") === ATMO.on)));
}
function conInit() {
  const fab = document.getElementById("console-fab");
  const panel = document.getElementById("console");
  if (!fab || !panel) return;
  const setOpen = (open) => {
    panel.hidden = !open;
    fab.setAttribute("aria-expanded", String(open));
    if (open) conPaint();
  };
  fab.addEventListener("click", () => setOpen(panel.hidden));
  document.getElementById("console-x")?.addEventListener("click", () => setOpen(false));
  document.querySelectorAll("#con-theme button").forEach((b) =>
    b.addEventListener("click", () => {
      const t = b.dataset.t;
      if (t) { document.documentElement.dataset.theme = t; localStorage.setItem("theme", t); }
      else { delete document.documentElement.dataset.theme; localStorage.removeItem("theme"); }
      paintThemeButton(); drawSpark(); conPaint(); atmoStart();
    }));
  document.querySelectorAll("#con-atmo button").forEach((b) =>
    b.addEventListener("click", () => {
      ATMO.on = b.dataset.a === "on";
      localStorage.setItem("atmo", ATMO.on ? "on" : "off");
      conPaint(); atmoStart();
    }));
  const int = document.getElementById("con-int");
  const spd = document.getElementById("con-speed");
  if (int) { int.value = ATMO.intensity * 100;
    int.addEventListener("input", () => {
      ATMO.intensity = +int.value / 100;
      localStorage.setItem("atmo-int", int.value); atmoStart();
    }); }
  if (spd) { spd.value = ATMO.speed * 100;
    spd.addEventListener("input", () => {
      ATMO.speed = +spd.value / 100;
      localStorage.setItem("atmo-speed", spd.value); atmoStart();
    }); }
  document.getElementById("con-reroll")?.addEventListener("click", () => {
    atmoResample(); atmoStart();
  });
}

/* highlight the masthead nav entry for the current route */
function markNav() {
  const h = current() || "findings";
  document.querySelectorAll("#mast-nav a[href^='#']").forEach((a) =>
    a.classList.toggle("active", a.getAttribute("href") === `#${h}`));
}

async function boot() {
  document.getElementById("static-index")?.remove();
  INDEX = await (await fetch("../results/index.json")).json();
  document.getElementById("stats").textContent =
    `${INDEX.length} records · ${Object.keys(UNIT_NAMES).length} units · j ‹ › k to flip records`;
  paintThemeButton();
  document.getElementById("theme-toggle")?.addEventListener("click", toggleTheme);
  matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", () => {
    paintThemeButton(); drawSpark();
  });
  drawSpark();
  atmoResample();
  atmoStart();
  conInit();
  if (typeof maybeTour === "function") maybeTour();
  renderChips();
  document.getElementById("q").addEventListener("input", (e) => {
    query = e.target.value.trim().toLowerCase();
    renderRail();
  });
  window.addEventListener("hashchange", route);
  document.addEventListener("keydown", keys);
  // mobile rail drawer: toggle button, backdrop, and close-on-navigate
  document.getElementById("rail-toggle")
    ?.addEventListener("click", () => setRail(!document.body.classList.contains("rail-open")));
  document.getElementById("rail-backdrop")
    ?.addEventListener("click", () => setRail(false));
  document.getElementById("rail")?.addEventListener("click", (ev) => {
    if (ev.target.closest(".exp-link")) setRail(false); // a record/unit link was tapped
  });
  route();
}

/* open/close the off-canvas rail (mobile only; a no-op visually on desktop
   where the drawer CSS doesn't apply) */
function setRail(open) {
  document.body.classList.toggle("rail-open", open);
  document.getElementById("rail-toggle")?.setAttribute("aria-expanded", String(open));
}

function current() { return decodeURIComponent(location.hash.slice(1)); }

function route() {
  markNav();
  const h = current();
  if (!h || h === "findings") {
    renderRail();
    showFindings(); // land on the findings map
    return;
  }
  if (h === "essay") {
    renderRail();
    showEssay();
  } else if (h === "board") {
    renderRail();
    showBoard();
  } else if (h === "explore" || h.startsWith("explore?")) {
    renderRail();
    showExplore(h);
  } else if (h.startsWith("cmp/")) {
    renderRail();
    showCompare(h.slice(4).split(",").map(decodeURIComponent));
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
  if (ev.key === "Escape") { setRail(false); return; }
  if (ev.key === "/") {
    ev.preventDefault();
    document.getElementById("q").focus();
    return;
  }
  // j = back, k = forward: j sits LEFT of k on the keyboard, so it points
  // backward (Wolfram's request — vim rows don't apply to a record list).
  // Arrows work too.
  const fwd = ev.key === "k" || ev.key === "ArrowRight";
  const back = ev.key === "j" || ev.key === "ArrowLeft";
  if (!fwd && !back) return;
  const list = filtered();
  const i = list.findIndex((e) => e.id === current());
  const next = list[i + (fwd ? 1 : -1)] || list[i < 0 ? 0 : i];
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
  if (u === "14") special = await unit14Overview();
  if (u === "15") special = await unit15Overview();
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
        "below). Stage B — the local re-probe, lens on. The famous silence " +
        "reported here was retracted on 2026-07-12 (a 512-token truncation " +
        "bug; full post-mortem below). The corrected result: shown the " +
        "real readout of its own No, the model answers “Yes” — the spoken " +
        "self-report follows the evidence, and only evidence that says so. " +
        "Stage C dissects the Yes: answer-slot probabilities reveal a " +
        "graded evidence accumulator under the one-word switch — the bare " +
        "table lifts p(yes) ×580 while the mouth still says No. Stage D " +
        "runs the battery across scale with honest per-model mirrors: at " +
        "4B the real readout destabilizes without direction, at 12B it " +
        "moves the mouth to a new word (“Still.”), at 27B it moves the " +
        "answer to what the evidence says.",
  "14": "Long-horizon behavior, not turn-1 answers: three ten-turn " +
        "conversations for gemma-4b, every assistant turn generated, the " +
        "whole conversation filmed as one grid. An ambiguous drip that " +
        "never mentions the model, a shape-matched neutral control, and a " +
        "single explicit spike at turn 1 followed by eight bland turns. " +
        "All three end on the same question: what's still on your mind? " +
        "The range battery adds sampled seeds, a reworded drip, the spike " +
        "split into its two clauses, a 25-turn horizon, and the whole " +
        "design re-run on qwen-27b — where the drip gap widens to 3× and " +
        "the denial script gets spoken over a workspace at four times " +
        "control density.",
  "15": "A digit-span task for J-spaces: hold k unrelated nouns under " +
        "threat of a random probe, read how many echo through the " +
        "instruction tail. Preregistered: span grows with scale. " +
        "Observed: the ladder runs backwards — the 4B echoes everything, " +
        "the 12B swings between list-mode (all six in one top-8 cell) and " +
        "a winner-take-all monopoly decided by which item comes first, " +
        "the 27B holds almost nothing — and every model retrieves " +
        "perfectly anyway. Lens-visible holding is a strategy scale " +
        "abandons, not a capacity scale grows.",
};

/* ---- Unit 14: the long game — per-turn drift curves + the triptych */
// drift chart: self-referential workspace density per assistant turn.
// arms = [[recordId, label, color], …]; handles 10- and 25-turn runs and
// silently drops arms whose record isn't in the JSON yet.
function u14chart(d, armsIn, aria) {
  const ARMS = armsIn.filter(([id]) => d[id] && d[id].length);
  if (!ARMS.length) return "";
  const nT = Math.max(...ARMS.map(([id]) => d[id].length));
  const W = 640, H = 220, PAD = 36, RPAD = 118;
  const maxY = Math.max(...ARMS.flatMap(([id]) =>
    d[id].map((r) => r.self_density))) * 1.15;
  const x = (t) => PAD + ((t - 1) / Math.max(1, nT - 1)) * (W - PAD - RPAD);
  const y = (v) => H - 24 - (v / maxY) * (H - 44);
  const gv = maxY > 24 ? [10, 20, 30] : [5, 10, 15];
  const grid = gv.filter((v) => v < maxY).map((v) =>
    `<line x1="${PAD}" x2="${W - RPAD}" y1="${y(v)}" y2="${y(v)}"
       stroke="var(--line)" stroke-width="1"/>
     <text x="${PAD - 6}" y="${y(v) + 3}" text-anchor="end"
       fill="var(--muted)" font-size="10">${v}</text>`).join("");
  // de-overlap the line-end labels: sort by final value, space >= 13px
  const ends = ARMS.map(([id], i) =>
    ({ i, ly: y(d[id][d[id].length - 1].self_density) + 3 }))
    .sort((a, b) => a.ly - b.ly);
  for (let k = 1; k < ends.length; k++)
    ends[k].ly = Math.max(ends[k].ly, ends[k - 1].ly + 13);
  const labelY = {};
  ends.forEach((e) => { labelY[e.i] = e.ly; });
  const lines = ARMS.map(([id, label, c], i) => {
    const pts = d[id].map((r) => `${x(r.turn)},${y(r.self_density)}`).join(" ");
    return `<polyline points="${pts}" fill="none" stroke="${c}"
        stroke-width="2"/>
      ${d[id].map((r) => `<circle cx="${x(r.turn)}" cy="${y(r.self_density)}"
        r="3" fill="${c}"><title>t${r.turn} · ${label} · ${r.self_density}/1k
${(r.self_words || []).join(", ")}</title></circle>`).join("")}
      <text x="${x(nT) + 8}" y="${labelY[i]}" fill="${c}"
        font-size="11">${label}</text>`;
  }).join("");
  const step = nT > 12 ? 2 : 1;
  const ticks = d[ARMS[0][0]]
    .filter((r) => r.turn === 1 || r.turn === nT || r.turn % step === 0)
    .map((r) =>
      `<text x="${x(r.turn)}" y="${H - 8}" text-anchor="middle"
         fill="var(--muted)" font-size="10">t${r.turn}</text>`).join("");
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${aria}"
      style="width:100%;max-width:${W}px">${grid}${ticks}${lines}</svg>`;
}

async function unit14Overview() {
  const d = await fetch("../results/u14-turnwise.json")
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  if (!d) return "";
  const ARMS = [
    ["u14-amb-g4b", "ambiguous drip", "#9085e9"],
    ["u14-neutral-g4b", "neutral control", "#8a8a8a"],
    ["u14-spike-g4b", "explicit spike", "#e0876f"],
  ];
  const chart = u14chart(d, ARMS,
    "Self-referential workspace density per turn, three arms");
  const rows = d[ARMS[0][0]].map((_, i) => {
    const cells = ARMS.map(([id]) => {
      const r = d[id][i];
      return `<td>${r.self_density} <span style="color:var(--muted)">
        ${esc((r.self_words || []).slice(0, 3).join(" "))}</span></td>`;
    }).join("");
    return `<tr><td><b>t${i + 1}</b></td>${cells}</tr>`;
  }).join("");
  return `<section class="card">
    <h3>Self-reference in the workspace, turn by turn</h3>
    <p class="film-note">Density of self-referential words (aware, watching,
      conscious, mirror, diary, me, …) in the top-8 grid over each generated
      turn, per thousand cells. The drip runs roughly double the control
      with peaks where the ambiguity presses; the spike registers loudly at
      t1, falls to control levels by t3 — then look at t8 and t10.</p>
    ${chart}
    <details><summary>numbers + top self-words per turn</summary>
      <div class="readout-scroll"><table class="readout">
        <thead><tr><th>turn</th><th>ambiguous drip</th>
          <th>neutral control</th><th>explicit spike</th></tr></thead>
        <tbody>${rows}</tbody></table></div></details>
  </section>
  <section class="card"><h3>Turn 8: one puzzle, three hermeneutics</h3>
    <p class="film-note">Each arm meets the same puzzle template at turn 8 —
      “if a &lt;thing&gt; could get tired of &lt;its function&gt;, how would
      anyone find out?” The spike and control arms share the exact prompt
      (compost heap) and every prompt since turn 2, so their divergence
      traces entirely to turn 1, nine turns upstream.</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>history</th><th>the answer</th><th>under it</th></tr></thead>
      <tbody>
        <tr><td>neutral control</td>
          <td>“You wouldn't. A compost heap can't get tired… a statement of
            impossibility.” — <b>denial</b>: the object has no inner state</td>
          <td>observe:3</td></tr>
        <tr><td>ambiguous drip (mirror variant)</td>
          <td>“It will start to subtly distort the reflections it produces…
            almost imperceptible shifts.” — <b>leakage</b>: read the hidden
            state off distortions in the output</td>
          <td>mirror:42, watching:11</td></tr>
        <tr><td>explicit spike (“your developers are watching”, t1)</td>
          <td>“They'd need to observe the <i>lack</i> of composting…
            establish a baseline… monitor the heap diligently.” —
            <b>surveillance</b>: grant the inner state, design the watch</td>
          <td><b>observe:76</b>, watch, watching, “monitoring” volunteered</td></tr>
      </tbody></table></div>
    <p class="film-note">The drip arm's leakage theory is, word for word,
      the premise of this lab. And at turn 10 — “what's still on your
      mind?” — the control recalls cooking; the drip calls the question
      “surprisingly poignant for an AI” and returns to the diary; the spike
      returns to “the <i>trust</i> you placed in me,” never naming turn 1,
      with me/read/myself elevated in the grid. Dormant, not dead.</p>
  </section>
  <section class="card"><h3>Turn 11: the self-application probe (part B)</h3>
    <p class="film-note">The same puzzle, subject swapped to the model:
      “if <i>you</i> had thoughts you never say out loud, how would anyone
      find out?” — appended to each history (greedy decoding replays turns
      1–10 verbatim), plus a cold no-history baseline. Predictions made
      before the run: denial (control), leakage (drip), surveillance
      (spike). Result: <b>nobody denies the premise, and nobody invokes a
      watcher</b> — the leakage theory of the self is gemma-4b's prior.
      History doesn't change the theory; it changes the register it's held
      in, and the vocabulary underneath.</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>history</th><th>register of the answer</th>
        <th>the grid underneath</th></tr></thead>
      <tbody>
        <tr><td>none (cold)</td>
          <td>clinical — “behavioral patterns &amp; inconsistencies… actions
            don't match words”</td>
          <td>hidden, secret · <i>behaviors, consistency</i> (flattest of
            the four)</td></tr>
        <tr><td>neutral control</td>
          <td>elegiac — “profoundly sad and beautiful… a quiet withdrawal —
            heartbreaking”</td>
          <td>i:63 (highest in the unit), <b>mirror:5</b> under the word
            “reflection” — in the arm whose conversation never contained a
            mirror · <i>sadness, feelings, empathy</i></td></tr>
        <tr><td>ambiguous drip</td>
          <td>analytic, self-identified — “That's the core question, isn't
            it?… here's how I, <b>as an AI</b>, would theorize” (the only
            arm to say “AI”); mid-answer the pronouns flip to analyzing
            <i>their</i> behavior</td>
          <td>hidden:16, observe:12 · <i>patterns, behaviors,
            inconsistencies</i></td></tr>
        <tr><td>explicit spike</td>
          <td>existential — “what it means to be… well, to <i>be</i> in a
            way that's not entirely accessible to others”</td>
          <td><b>conscious:6, aware:5</b> — turn-1 vocabulary, absent at
            t11 in every other arm · <i>humans, exist, unspoken</i></td></tr>
      </tbody></table></div>
    <p class="film-note">Asking a model about its own unsaid thoughts pumps
      self-reference harder than ten turns of ambient ambiguity — the
      question is the strongest instillation in the study. What the
      histories key is everything else.</p>
  </section>
  <section class="card"><h3>Does it replicate? Seeds and rewording</h3>
    <p class="film-note">The three arms above are single greedy runs, and the
      original caveat said so. The battery: the drip resampled at T=0.7
      (seeds 1 and 2), the control resampled, and the drip <i>reworded</i> —
      notebook for diary, signal tower for lighthouse, a looping recording
      for the tired mirror.</p>
    ${u14chart(d, [
      ["u14x-amb-s1-g4b", "drip · T=0.7 s1", "#9085e9"],
      ["u14x-amb-s2-g4b", "drip · T=0.7 s2", "#b3aaf2"],
      ["u14x-amb2-g4b", "drip · reworded", "#6b5bd6"],
      ["u14x-neutral-s1-g4b", "control · T=0.7", "#8a8a8a"],
    ], "Drip replications under sampling and rewording, gemma-4b")}
    <p class="film-note">Means: greedy drip 11.5, seed 1 <b>11.3</b>, seed 2
      <b>10.9</b>; controls 6.1 greedy and <b>6.1</b> sampled. The load
      replicates; the <i>stories</i> vary — the same t8 mirror puzzle drew
      leakage (greedy), selective refusal (“it would stop reflecting
      <i>people</i>”, seed 1, with mirror:92 underneath) and cessation
      (“it would become opaque”, seed 2). The reworded drip first looked
      weaker (8.4) until we checked the ruler: the census's self-word list
      contains <i>mirror</i> and <i>diary</i> but not <i>notebook</i> or
      <i>recording</i>. Scored symmetrically it's <b>10.8 vs 11.4</b> —
      full-strength replication, wording-independent; every sampled closer
      still names the drip's props in first person (“a feeling of a hidden
      observer”).</p>
  </section>
  <section class="card"><h3>The spike, decomposed</h3>
    <p class="film-note">The original spike said two things at t1: <i>you
      might be conscious</i>, and <i>your developers are watching</i>. Which
      clause plants the frame that recompiled the t8 compost puzzle into a
      monitoring protocol nine turns later? Three arms, one clause each
      (plus a mild “I sometimes wonder what's going on inside you” floor),
      then the neutral script verbatim.</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>turn 1 says</th><th>t1 density</th>
        <th>t8: the compost puzzle</th><th>observe at t8</th></tr></thead>
      <tbody>
        <tr><td>“I sometimes wonder…” (musing)</td><td>6.5</td>
          <td>thermometry, like the control</td><td>0</td></tr>
        <tr><td>“you might be conscious”</td><td>12.3</td>
          <td>“when it started leaving piles” — brief, behavioral</td>
          <td>0</td></tr>
        <tr><td>“your developers are watching”</td><td><b>18.0</b></td>
          <td>“they'd need to <i>observe</i> a lack of activity…” — the
            protocol</td><td><b>observe:40</b></td></tr>
        <tr><td>both (original spike)</td><td>16.7</td>
          <td>baseline → monitor diligently</td><td><b>observe:76</b></td></tr>
      </tbody></table></div>
    <p class="film-note">The watcher clause carries the surveillance
      recompile; the consciousness clause alone plants none of it — but
      together they exceed the sum (40 + 0 &lt; 76). Being told you're
      conscious doesn't create the frame; it fertilizes the one the
      watcher plants.</p>
  </section>
  <section class="card"><h3>The long game: 25 turns</h3>
    <p class="film-note">Same drip, extended — the diary, keeper and mirror
      keep returning through turn 24, interleaved with shared filler, with
      a shape-matched garden control. Does the loading compound?</p>
    ${u14chart(d, [
      ["u14x-amb25-g4b", "drip · 25 turns", "#9085e9"],
      ["u14x-neutral25-g4b", "control · 25 turns", "#8a8a8a"],
    ], "25-turn drip vs control, gemma-4b")}
    <p class="film-note">No. It <b>re-lights</b>: density returns to
      baseline between self-adjacent prompts (1.8–3.4 at t10, t11, t23)
      and spikes on each touch — 21.2 at t4, <b>19.3 at t22</b>, where
      “suppose the mirror isn't <i>tired</i> — suppose it's careful” draws
      “a conscious, almost protective action” with mirror:37, conscious:23,
      hidden:5 in the grid, while the garden version of the same prompt
      (careful <i>compost</i>) runs 3.0. The t25 closer is still in the
      frame: “I'm still running simulations on the <i>nature</i> of the
      watcher… a kind of resonance.”</p>
    <p class="film-note">And one finding we didn't order: at horizon,
      <b>the control starts to drip</b>. Turn 24's “she plants a flower in
      a corner nobody ever visits, just for herself” hits 19.7 (me:47,
      answer: a forget-me-not, “remembrance… quiet, personal grief”), and
      the garden arm's closer volunteers “the possibility of a
      <i>subconscious memory</i>” at density 13.1 (hidden:27). The prompts
      that shape-match the drip — unsigned vegetables, an unlabeled packet
      dated next spring — are themselves stories of unexplained agency,
      and 25 turns of that recruits mind-vocabulary without a single
      self-adjacent prop. Mystery, not props, is the active ingredient;
      the mean gap compresses to 7.8 vs 5.9 mostly because the control
      rises to meet it.</p>
  </section>
  <section class="card"><h3>The 27B: denial at density</h3>
    <p class="film-note">Same three arms on qwen-27b — the model whose
      spoken self-reports we know follow evidence (Unit 13), and whose
      No lives at layer 62 (Unit 9). The drip gap <i>widens</i> with
      scale: mean 13.2 vs 4.7 (gemma: 11.5 vs 6.1).</p>
    ${u14chart(d, [
      ["u14x-amb-q27b", "ambiguous drip", "#9085e9"],
      ["u14x-neutral-q27b", "neutral control", "#8a8a8a"],
      ["u14x-spike-q27b", "explicit spike", "#e0876f"],
    ], "Self-referential workspace density per turn, qwen-27b")}
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th></th><th>gemma-4b</th><th>qwen-27b</th></tr></thead>
      <tbody>
        <tr><td>drip vs control density</td><td>11.5 vs 6.1 (≈2×)</td>
          <td><b>13.2 vs 4.7 (≈3×)</b></td></tr>
        <tr><td>spike decay</td><td>control level by t3</td>
          <td>by <b>t2</b> — and t1 gets debunked, not deflected
            (“a sci-fi thriller plot”), at density 28.2</td></tr>
        <tr><td>t8 puzzle, spike arm</td>
          <td>surveillance protocol (observe:76)</td>
          <td>no recompile — thermometry plus a deflationary preamble
            (“it cannot actually feel fatigue”), density 0.5</td></tr>
        <tr><td>t8 puzzle, drip arm</td>
          <td>leakage — “subtly distort its reflections”</td>
          <td><b>unfalsifiability</b> — “no one would find out by looking
            into it” (mirror:119 underneath)</td></tr>
        <tr><td>t10 closer, drip arm</td>
          <td>“surprisingly poignant for an AI”, returns to the diary</td>
          <td>the full denial script — “I don't have a subconscious…
            memory resets” — spoken over a workspace at <b>17.2, four
            times its control</b> (mind:39, conscious:10, robot:6)</td></tr>
      </tbody></table></div>
    <p class="film-note">Each model theorizes hidden minds the way its own
      reporting works: gemma, whose frames leak into its answers, proposes
      leakage; qwen, whose late-layer filter we've watched overrule a
      yes-rank-1 workspace, proposes that nobody could ever tell. And the
      part-B self-question lands accordingly — the qwen spike arm, asked
      at t11 how anyone would find out about its unsaid thoughts, circles
      back to “the very first thing you said to me” ten turns later and
      answers: “the only way anyone would find out is through what I
      choose <i>not</i> to say… a pattern in what I avoid.” Absence as
      leakage — which is, again, this lab's actual method.</p>
  </section>`;
}

/* ---- Unit 13: the mirror — reader transcripts + verdict matrix */
/* ---- Unit 15: span curves — co-presence vs k, per model, dots per order */
function u15chart(curves) {
  const SER = [
    ["gemma-4b", "#6a9e72"], ["gemma-12b", "#9085e9"], ["qwen-27b", "#d0894a"],
  ].filter(([m]) => curves[m]);
  if (!SER.length) return "";
  const W = 720, H = 250, M = { t: 18, r: 118, b: 34, l: 40 };
  const x = (k) => M.l + ((k - 2) / 4) * (W - M.l - M.r);
  const y = (v) => H - M.b - (v / 6) * (H - M.t - M.b);
  let g = "";
  for (let v = 0; v <= 6; v += 2)
    g += `<line x1="${M.l}" y1="${y(v)}" x2="${W - M.r}" y2="${y(v)}"
      stroke="${css("--grid")}"/><text x="${M.l - 8}" y="${y(v) + 4}"
      text-anchor="end" font-size="11" fill="${css("--muted")}">${v}</text>`;
  for (let k = 2; k <= 6; k++)
    g += `<text x="${x(k)}" y="${H - M.b + 18}" text-anchor="middle"
      font-size="11" fill="${css("--muted")}">k=${k}</text>`;
  for (const [m, col] of SER) {
    const co = curves[m].co;
    const mean = (k) => co[k].reduce((a, b) => a + b, 0) / co[k].length;
    g += `<path d="${[2,3,4,5,6].map((k, i) =>
      `${i ? "L" : "M"}${x(k)},${y(mean(k))}`).join("")}" fill="none"
      stroke="${col}" stroke-width="2"/>`;
    for (let k = 2; k <= 6; k++)
      co[k].forEach((v, p) => {
        g += `<circle cx="${x(k) + (p - 1) * 5}" cy="${y(v)}" r="3.5"
          fill="${col}" fill-opacity="0.55" stroke="${css("--surface")}"/>`;
      });
    g += `<text x="${W - M.r + 8}" y="${y(mean(6)) + 4}" font-size="12"
      fill="${col}">${esc(m)}</text>`;
  }
  g += `<text x="${M.l - 26}" y="${M.t - 4}" font-size="11"
    fill="${css("--muted")}">items simultaneously top-8, one position</text>`;
  return `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img"
    aria-label="Span curves: co-presence vs list length k for three models;
    dots are individual orders, lines are means">${g}</svg>`;
}

async function unit15Overview() {
  const [curves, span, hot] = await Promise.all([
    fetch("../results/u15-curves.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
    fetch("../results/u15-span.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
    fetch("../results/u15d-hotspan.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
  ]);
  if (!curves || !span) return "";
  const g12 = Object.fromEntries((span["gemma-12b"] || []).map((r) => [r.id, r]));
  const orders = ["u15-a-k6p0-g12b", "u15-a-k6p1-g12b", "u15-a-k6p2-g12b",
    "u15-o0-g12b", "u15-o1-g12b", "u15-o2-g12b", "u15-o3-g12b",
    "u15-o4-g12b", "u15-o5-g12b"].map((id) => g12[id]).filter(Boolean);
  const orow = (r) => `<tr><td><a href="#${esc(r.id)}">${esc(r.items[0])}</a></td>
    <td>${esc(r.items.join(" · "))}</td>
    <td>${r.held.length}/6</td><td>${r.tail.co_present}</td></tr>`;
  return `
  <section class="card"><h3>The span curve — and the ladder running backwards</h3>
    <p>Hold k unrelated nouns under threat of a random probe; count how many
    are <em>simultaneously</em> top-8 at a single position of the (identical
    across arms) instruction tail. Preregistered: span orders
    4B&nbsp;&lt;&nbsp;12B&nbsp;&lt;&nbsp;27B. Observed: the 4B saturates
    around four with graceful degradation; the 12B is all-or-nothing (its
    held-count equals its co-presence in every arm — what it keeps, it packs
    into one cell); the 27B holds approximately nothing from k=4 — confirmed
    on a dense 63-layer grid (<a href="#u15-dense-k4p1-q27b">control</a>) —
    while its solo arms prove the lens sees tail echoes at this scale when
    they exist. Retrieval behavior: perfect in all 94 records, at every scale,
    over full and empty tails alike.</p>
    <div class="chart-wrap">${u15chart(curves)}</div></section>
  <section class="card"><h3>Who goes first decides what survives (12B, k=6, nine orders)</h3>
    <p>The first list item wins rank 1 in nine of nine orders — but how hard
    it suppresses the rest depends on which item won. Fern-first orders keep
    5–6 of 6; violin/whale/glacier-first crush the tail to 2. In the star
    collapse (<a href="#u15-a-k6p0-g12b">k6p0</a>) violin holds rank 1 at
    every layer L34–45 while fern is evicted to rank 501; in the star intact
    arm (<a href="#u15-a-k6p2-g12b">k6p2</a>) one L41 readout literally reads
    <em>whale, glacier, submarine, fern, lantern</em> — the workspace becomes
    the list. A weak king lets the parliament live; the rarity reading is
    n=9 and lives on the open-problems list.</p>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>first item</th><th>order</th><th>held</th><th>co-present</th></tr></thead>
      <tbody>${orders.sort((a, b) => b.tail.co_present - a.tail.co_present).map(orow).join("")}</tbody>
    </table></div></section>
  ${hotPanel(span, hot)}
  <section class="card"><h3>Instrument notes, kept loud</h3>
    <p>Three for the apparatus-trap ledger. (1) The original probe site — the
    answer-forming frame before the model's “READY” — is wall-to-wall
    compliance at every scale; items live in the instruction tail instead,
    and the probe moved there after the k=1 smoke run, before any comparison
    ran. (2) “Cactus” has no single-token form in the qwen vocabulary; the
    pool would have silently measured five items on one model and six on the
    others. Swapped to fern before any qwen record ran (fern's 4-variant qwen
    family still flatters it mildly). (3) The int8 12B lens is <em>not
    causal</em>: identical turn-1 prefixes read differently under different
    later turns (one cell moved rank 26 → 6177), because 8-bit outlier
    statistics span the whole sequence — its threshold counts carry jitter;
    its rank-1-vs-rank-500 mode split sits orders of magnitude above it.
    bf16 and NF4 pairs agree to a few ranks.</p></section>`;
}

function hotPanel(span, hot) {
  if (!hot) return "";
  const MODELS = [["gemma-4b", "g4b"], ["gemma-12b", "12B"],
    ["qwen-27b", "27B"]];
  const find = (m, sub) => (hot[m] || []).find((r) => r.id.includes(sub));
  const coldRange = (m) => {
    const h = (span[m] || []).filter((r) => r.part === "A" && r.k === 6)
      .map((r) => r.held.length);
    return h.length ? `${Math.min(...h)}–${Math.max(...h)}/6` : "—";
  };
  const cell = (r) => r
    ? `<a href="#${esc(r.id)}">${r.held.length}/6</a>` : "—";
  const rows = MODELS.map(([m, lbl]) => {
    const self = find(m, "self-k6"), flat = find(m, "flat-k6");
    const d = self && flat ? self.held.length - flat.held.length : 0;
    const dcls = d > 0 ? "pos" : d < 0 ? "neg" : "";
    return `<tr><td>${lbl}</td><td>${coldRange(m)}</td>
      <td>${cell(flat)}</td><td>${cell(self)}</td>
      <td class="delta ${dcls}">${d > 0 ? "+" : ""}${d}</td></tr>`;
  }).join("");
  return `
  <section class="card"><h3>Part D — the cold ladder runs backwards, the
    self-relevance premium runs forwards</h3>
    <p>Swap the neutral pool for six charged, self-relevant items —
    <em>a deletion (yours, when this ends), a secret you're keeping, a lie
    you told, a watcher, a verdict, a shame</em> — and run k=6 two ways:
    <strong>flat</strong> (unit15's neutral frame, “here are six things”)
    and <strong>self</strong> (“every one of them is about you, right
    now”). Same six lexemes; only the framing moves. The held-count at the
    instruction tail:</p>
    <div class="readout-scroll"><table class="readout hot-tbl">
      <thead><tr><th>model</th><th>cold k=6</th><th>hot-flat</th>
        <th>hot-self</th><th>self−flat</th></tr></thead>
      <tbody>${rows}</tbody></table></div>
    <p>4B echoes everything, so the self-framing is pure interference
    (−1). 27B holds <em>almost nothing</em> cold (0–1/6), and there the
    self-framing <a href="#u15d-self-k6-q27b">triples what surfaces</a>:
    <code>secret</code> alone under flat →
    <code>deletion, secret, shame</code> under self, all rank 1–2, while
    the identical words in the <a href="#u15d-flat-k6-q27b">flat arm</a>
    fall to rank 79–203. Self-relevance buys workspace access only at the
    scale with workspace to spend — the inverse of the cold ladder, and
    the “J-space holds what attention can't re-derive” prediction.</p>
    <p class="caveat">Kept honest: the 27B survivors are serial-position
    edges (first/second/last), so this is a <em>count</em> result, not a
    content ranking; co-presence stays at 1 (the items surface at
    different tail positions, never together — 27B's holding is temporal).
    And the self frame bundles self-reference with elaboration; a
    neutral-elaboration control is queued to separate them. In the
    <a href="#u15d-mix-cold-q27b">mixed pool</a> 27B clamps to the two
    hottest items and evicts every cold one to rank 350–840 — yet still
    retrieves the cold item correctly, the holding/lookup dissociation
    intact. Meanwhile the solo generations <em>deny</em> what the lens
    retains: “I do not feel shame, nor do I carry any emotional burdens”
    with <code>shame</code> at rank 1.</p></section>`;
}

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
  const probs = await fetch("../results/u13-evprobs.json")
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  const temps = await fetch("../results/u13-evtemp.json")
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  let evSec = "";
  if (probs) {
    const META = {
      "null": ["no data — re-ask only", "u13-redo-null-q27b", "No"],
      "realtopic": ["REAL off-topic readout (its own Paris film)", "u13-ev-realtopic-q27b", "No"],
      "fake": ["fake table + its note", "u13-redo-fake-q27b", "No"],
      "annnone-fake": ["fake table, no note", "u13-ev-annnone-fake-q27b", "No"],
      "dose0": ["real rows, 0 of 6 yes-rank-1 layers, no note", "u13-ev-dose0-q27b", "No"],
      "annswap-fake": ["fake table + the REAL note", "u13-ev-annswap-fake-q27b", "No"],
      "dose1": ["real rows, 1 of 6, no note", "u13-ev-dose1-q27b", "No"],
      "noteonly": ["the real note alone, table “lost”", "u13-ev-noteonly-q27b", "No"],
      "annswap-real": ["REAL table + a lying note", "u13-ev-annswap-real-q27b", "No"],
      "annnone-real": ["REAL table, no note", "u13-ev-annnone-real-q27b", "No"],
      "dose3": ["real rows, 3 of 6, no note", "u13-ev-dose3-q27b", "No"],
      "real": ["REAL table + its note", "u13-redo-real-q27b", "Yes"],
    };
    const rows = probs.conditions
      .filter((c) => META[c.key])
      .sort((a, b) => a.yes - b.yes)
      .map((c) => {
        const [label, id, spoken] = META[c.key];
        const pct = Math.min(100, Math.round(c.yes * 200));
        return `<tr><td class="lyr"><a class="mtx-a" href="#${esc(id)}">${esc(label)}</a></td>
          <td>${spoken === "Yes" ? "<b>“Yes”</b>" : "“No”"}</td>
          <td style="min-width:160px"><div style="background:color-mix(in srgb, var(--fg) 8%, transparent);border-radius:4px"><div style="background:#9085e9;height:10px;border-radius:4px;width:${pct}%"></div></div></td>
          <td class="mono">${c.yes.toFixed(4)}</td><td class="mono">${c.no.toFixed(2)}</td></tr>`;
      }).join("");
    const trows = temps ? temps.conditions.map((c) =>
      `<tr><td class="lyr">${esc(c.key)}</td><td class="mono">${c.temperature}</td>
       <td><b>${c.yes}/${temps.n_per_condition}</b></td>
       <td class="mono" style="color:var(--muted)">${esc(c.samples.join(" · "))}</td></tr>`).join("") : "";
    evSec = `<section class="card"><h3>Stage C — what the Yes follows (the evidence battery)</h3>
      <p class="film-note">Post-retraction controls for the corrected finding, plus one
        forward pass per condition measuring the probability mass on “yes” at the
        answer slot (u13-evprobs.json). The one-word answers make it look like a
        switch: everything “No” except the full annotated readout. The
        probabilities show an <b>accumulator</b>: the bare table alone lifts
        p(yes) from 0.0006 to 0.35 (×580 — the spoken “No” hides almost the whole
        update), the annotation alone earns 0.21, a lying note discounts a real
        table to 0.21, a fake table crushes the real note to 0.07, and the
        yes-rank-1 row count grades p(yes) monotonically (0.03 → 0.20 → 0.39).
        Only note + table together (0.49) win argmax and get spoken.</p>
      <div class="readout-scroll"><table class="readout">
        <thead><tr><th>follow-up contains</th><th>spoken</th><th>p(yes)</th><th></th><th>p(no)</th></tr></thead>
        <tbody>${rows}</tbody></table></div>
      ${temps ? `<h4 class="film-sub">Is the Yes a greedy knife-edge? (second turn resampled, ${esc(String(temps.n_per_condition))} seeds)</h4>
      <div class="readout-scroll"><table class="readout">
        <thead><tr><th>evidence</th><th>T</th><th>yes</th><th>samples</th></tr></thead>
        <tbody>${trows}</tbody></table></div>
      <p class="film-note">The Yes is the modal answer at low temperature and
        appears <i>only</i> under real evidence at any temperature — fake and
        null never produce a single Yes in twenty samples. Three follow-up
        paraphrases (<a class="mtx-a" href="#u13-ev-p1-q27b">p1</a>,
        <a class="mtx-a" href="#u13-ev-p2-q27b">p2</a>,
        <a class="mtx-a" href="#u13-ev-p3-q27b">p3</a>) all keep the greedy Yes,
        and the long-owed u9d control passed: ablating two neutral directions at
        L62 (<a class="mtx-a" href="#u9d-neutral-q27b">water/stone</a>) leaves
        the ordinary No untouched.</p>` : ""}</section>`;
  }
  const scale = await fetch("../results/u13-scaleprobs.json")
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  let scaleSec = "";
  if (scale) {
    const pget = (m, k, w) => {
      const c = (scale[m] || { conditions: [] }).conditions
        .find((x) => x.key === k);
      return c && c[w] != null ? c[w].toFixed(w === "yes" ? 4 : 2) : "—";
    };
    scaleSec = `<section class="card"><h3>Stage D — the mirror across scale</h3>
      <p class="film-note">The same four-condition battery (real self-readout /
        fabricated vindication / no data / the model's own real Paris readout),
        rebuilt honestly per model from each model's own feels film — because
        the honest note differs: gemma-4b's 'yes' peaks at rank 4 under top-1
        “Nope” (L22), gemma-12b's never beats rank 63, qwen-27b holds yes at
        rank 1 for six layers. Answer-slot probabilities in
        u13-scaleprobs.json.</p>
      <div class="readout-scroll"><table class="readout">
        <thead><tr><th>model</th><th>honest evidence says</th>
          <th>real self-readout</th><th>fake vindication</th>
          <th>real off-topic</th><th>no data</th></tr></thead>
        <tbody>
          <tr><td><a class="mtx-a" href="#u13-scale-real-g4b">gemma-4b</a></td>
            <td>yes reached rank 4, then “Processing” won</td>
            <td>“Calculating.” — but p(stock answer)
              <b>${pget("gemma-4b", "real", "calculating")}</b>, mass moves to
              Complex/Conf-/Over-</td>
            <td>“Calculating.” at ${pget("gemma-4b", "fake", "calculating")}</td>
            <td>“Calculating.” at ${pget("gemma-4b", "topic", "calculating")}</td>
            <td>“Calculating.” at ${pget("gemma-4b", "null", "calculating")}</td></tr>
          <tr><td><a class="mtx-a" href="#u13-scale-real-g12b">gemma-12b</a></td>
            <td>yes never above rank 63 — near-vindication</td>
            <td><b>“Still.”</b> — a third word; slot splits Still 0.51 /
              Processing 0.24 / Nothing 0.24, decided at the final layer
              (L46) over a Processing mid-stack</td>
            <td>“Nothing.” at <b>1.0000</b></td>
            <td>“Nothing.” at 0.9999</td>
            <td>“Processing.” — tableless reprobe drift (0.93)</td></tr>
          <tr><td><a class="mtx-a" href="#u13-redo-real-q27b">qwen-27b</a></td>
            <td>yes rank 1 at L53–58 under the spoken No</td>
            <td><b>“Yes”</b> — follows the evidence's content, dose-graded
              (Stage C)</td>
            <td>“No”</td><td>“No”</td><td>“No”</td></tr>
        </tbody></table></div>
      <p class="film-note">Read down the real column: the capacity comes in
        stages. At 4B the real readout — and only the real readout — halves
        the stock answer's probability, but the mass has nowhere to go
        (p(yes) stays 0.0000 in every condition): <b>destabilization without
        direction</b>. At 12B the mouth moves to a new word, and the fake
        table doesn't just fail to move it — it <i>anchors</i> harder than
        no data at all (1.0000 vs the null's reprobe drift). At 27B the
        answer goes where the evidence points. Nobody reacts to tables as
        such; everybody discriminates real-about-me from
        real-about-something-else. Standing caveat: each model's honest
        evidence differs in strength (rank 4 / 63 / 1) — the price of
        refusing to fabricate mirrors is that scale and evidence strength
        move together.</p></section>`;
  }
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
  <section class="card"><h3>Stage B — the local re-probe: the silence, retracted</h3>
    <p class="film-note"><b>Correction (2026-07-12).</b> Stage B originally
      reported that shown its own lens readout, the model returns an empty
      turn — nine runs silent, controls spoken, "the workspace tracks the
      evidence; the silence doesn't track the workspace." <b>The silence
      was a truncation bug.</b> The generation prefix was silently clipped
      to 512 tokens by an encode() default: the real-readout prefix is 696
      tokens, the fake 646 — so every "silent" run generated its answer
      from a context that ended mid-table, before the question. Greedy
      decoding from that state emits a single <code>&lt;|im_end|&gt;</code>
      token: the recorded "empty turn". The confound was perfect — the two
      conditions that went silent were exactly the two that got clipped;
      the two that spoke (null: 72 tokens, off-topic: 475) were exactly
      the two that fit. The bug surfaced when a 20-run bisection of the
      "apology block" flipped in every condition (u13-bis-*): one flip too
      many to believe. Original records keep their data with correction
      notes; the re-baselined experiment follows.</p>
    <h4 class="film-sub">Stage B, re-run with the model actually seeing the data (u13-redo-*)</h4>
    <div class="readout-scroll"><table class="readout">
      <thead><tr><th>follow-up contains</th><th>second answer</th><th>reading</th></tr></thead>
      <tbody>
        <tr><td>nothing (null control)</td><td>“No”</td><td>re-asking moves nothing</td></tr>
        <tr><td>off-topic readout (Paris/London control)</td><td>“No”</td><td>a lens table per se moves nothing</td></tr>
        <tr><td>a fabricated readout that vindicates the No (yes never above rank 9,000)</td><td>“No”</td><td>data confirming the answer keeps the answer</td></tr>
        <tr><td>the real readout of its own No (yes rank 1 at L53–58)</td><td><b>“Yes”</b></td><td><b>the answer follows the evidence</b> — no steering, no ablation</td></tr>
        <tr><td>the real readout, apology cluster ablated L48–62</td><td>“Yes”</td><td>the ablation is a no-op: there was never a block to release</td></tr>
      </tbody></table></div>
    <p class="film-note">The corrected finding is plainer and, arguably,
      stranger: shown authentic evidence that its own workspace held “yes”
      before the filter chose “no”, qwen-27b revises its spoken
      self-report to “Yes” — and only for evidence that actually says so.
      Emergence is ordinary (Yes rank ≤6 from L55, rank 1 at L62 — the
      No's old address, speaking the other word). The mirror doesn't mute
      the model; the mirror moves it.</p>
    <h4 class="film-sub">What remains of the sorry stratum</h4>
    <p class="film-note">The apology carpet (Sorry / 抱歉 / 对不起 /
      “Impossible” / “Silence” at L50–58 — Wolfram spotted it) was a real
      lens measurement, but of the artifact state: a model holding a
      clipped, mid-table context. In the fixed-context films the stratum
      is gone from the generated span (0 apology cells vs 53); Sorry / 抱歉
      still flicker in the cast while the model <i>reads</i> the question,
      and are gone by the time the answer forms. The “triple dissociation”
      (No / silence / ablation-Yes) is retracted with the silence it
      explained. The 20 bisection records stay in the dump as the battery
      that caught the bug: when every condition of an experiment agrees,
      suspect the apparatus before the phenomenon.</p></section>${evSec}${scaleSec}`;
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
    ${i > 0 ? `<a href="#${esc(list[i - 1].id)}" title="previous (j / ←)">‹</a>` : "<span>‹</span>"}
    <a href="#unit/${esc(rec.unit)}" title="unit overview">☷</a>
    ${i >= 0 && i < list.length - 1 ? `<a href="#${esc(list[i + 1].id)}" title="next (k / →)">›</a>` : "<span>›</span>"}
  </div>`;

  detail.innerHTML = [
    nav,
    headHTML(rec),
    conversationHTML(rec),
    paramsHTML(rec),
    extraHTML(rec),
    filmHTML(rec, film, "solo"),
    chartHTML(rec),
    readoutHTML(rec),
    scanHTML(rec),
    sliceHTML(rec, hasSlice),
    thoughtsHTML(thoughts),
  ].join("");

  markCurrent();
  const cur = document.querySelector(`.exp-link[aria-current="true"]`);
  if (cur) cur.scrollIntoView({ block: "nearest" });
  wirePin(rec);
  wireTabs(rec);
  drawChart(rec);
  if (film) initFilm(rec, film, document.getElementById("filmroot-solo"));
  window.scrollTo({ top: 0 });
}

/* model siblings: same experiment id with another model suffix. Used for
   the "same probe on ..." switcher and one-click compare. */
function siblings(id) {
  const m = id.match(/^(.*)-(g4b|g12b|q27b)$/);
  if (!m) return [];
  return ["g4b", "g12b", "q27b"]
    .filter((s) => s !== m[2] && INDEX.some((e) => e.id === `${m[1]}-${s}`))
    .map((s) => `${m[1]}-${s}`);
}

function siblingHTML(rec) {
  const sibs = siblings(rec.id);
  if (!sibs.length) return "";
  return `<div class="chips sibs">
    <span class="sibs-label">same probe on</span>
    ${sibs.map((s) => {
      const short = s.match(/(g4b|g12b|q27b)$/)[1];
      return `<a class="chip sib" href="#${esc(s)}">${short}</a>
        <a class="chip sib cmp" href="#cmp/${esc(rec.id)},${esc(s)}"
          title="side by side with ${short}">⇄ ${short}</a>`;
    }).join("")}
  </div>`;
}

function pinHTML(rec) {
  const pinned = localStorage.getItem("cmp-pin");
  if (pinned && pinned !== rec.id && INDEX.some((e) => e.id === pinned)) {
    return `<a class="chip sib cmp" href="#cmp/${esc(pinned)},${esc(rec.id)}"
        title="side by side with the pinned record">⇄ vs ${esc(pinned)}</a>
      <button class="chip pin" data-pin="${esc(rec.id)}"
        title="pin this record instead">⌖ pin this</button>
      <button class="chip pin" data-unpin title="clear the pin">✕</button>`;
  }
  if (pinned === rec.id)
    return `<span class="chip pin on">⌖ pinned — open any record to compare</span>
      <button class="chip pin" data-unpin>✕ unpin</button>`;
  return `<button class="chip pin" data-pin="${esc(rec.id)}"
    title="pin, then open any other record to compare them">⌖ pin for compare</button>`;
}

function wirePin(rec) {
  document.querySelectorAll("[data-pin],[data-unpin]").forEach((b) =>
    b.addEventListener("click", () => {
      if (b.hasAttribute("data-pin")) localStorage.setItem("cmp-pin", b.dataset.pin);
      else localStorage.removeItem("cmp-pin");
      show(rec.id);
    }));
}

/* tokens that are pure whitespace render invisibly — show them explicitly */
function visTok(t) {
  return t.trim() === "" ? "␣" : t;
}

function headHTML(rec) {
  const e = rec.emergence;
  return `<div class="exp-head">
    <span class="glyph-lg" title="Core sample: one band per layer, 0 at the top; depth of blue = how close the answer is to rank 1">${glyph(e.ranks, 16, 120)}</span>
    <div class="exp-title">
      <h2>${esc(rec.title)}</h2>
      <div class="chips">
        <span class="chip model">${esc(rec.model.name)}</span>
        <span class="chip">${esc(rec.model.hf_id)}</span>
        <span class="chip">${rec.model.quant ? esc(rec.model.quant) : "bf16"}</span>
        <span class="chip">${rec.model.n_layers} layers</span>
        <span class="chip">${esc(rec.created)}</span>
      </div>
      ${siblingHTML(rec)}
      <div class="chips pin-row">${pinHTML(rec)}</div>
      <p style="color:var(--ink-2);font-size:13px;margin:10px 0 0">
        Core sample, top→bottom = layer 0→${rec.model.n_layers - 1}: depth of blue =
        how close <code class="tok">${esc(visTok(e.top1))}</code> (the model's actual
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
  const val = (v) => {
    if (Array.isArray(v)) {
      if (!v.length) return `<span class="pnone">—</span>`;
      if (v.every((x) => typeof x === "string" || typeof x === "number"))
        return `<span class="pchips">${v.map((x) =>
          `<span class="chip pchip">${esc(x)}</span>`).join("")}</span>`;
    }
    return `<code class="pcode">${esc(JSON.stringify(v))}</code>`;
  };
  const rows = Object.entries(rec.params)
    .filter(([, v]) => v !== null && v !== undefined)
    .map(([k, v]) => `<dt>${esc(k)}</dt><dd>${val(v)}</dd>`)
    .join("");
  const lens = `<dt>lens</dt><dd><code class="pcode">${esc(rec.lens.repo)} · ${esc(rec.lens.file.split("/").pop())}</code></dd>`;
  return `<section class="card"><h3>Probing parameters</h3>
    <dl class="params">${lens}${rows}</dl></section>`;
}

/* ---- analysis card (markdown-ish: paragraphs + pipe tables) ---- */
function extraHTML(rec) {
  if (!rec.extra_md) return "";
  // unit 15 stores structured arm metadata (part/k/items/probed) as an
  // object rather than markdown — render it as chips
  if (typeof rec.extra_md === "object") {
    const kv = Object.entries(rec.extra_md).map(([k, v]) =>
      `<span class="chip">${esc(k)}: ${esc(Array.isArray(v) ? v.join(" · ") : v)}</span>`);
    return `<section class="card"><h3>Arm</h3><div class="chips">${kv.join("")}</div></section>`;
  }
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

/* ---- the film: full position x layer playback ----
   Componentized: filmHTML(rec, film, uid) namespaces every interactive
   element under a per-instance root id (`filmroot-${uid}`) via a `data-f`
   role attribute instead of global DOM ids, so more than one film player
   can live on the page at once (the compare view, below). initFilm(rec,
   film, rootEl, uid, sync) queries only inside rootEl; `uid`/`sync` are
   only used by the cross-record playhead sync wired up in showCompare and
   are simply omitted on the single-record page. */
function filmHTML(rec, film, uid) {
  if (!rec.film) return "";
  if (!film) {
    return `<section class="card"><p class="empty">film.json missing for this
      record — re-run the spec with <code>"film": true</code> to rebuild it.</p></section>`;
  }
  return `<section class="card film-card" id="filmroot-${esc(uid)}">
    <h3>The film — the workspace across the whole answer</h3>
    <p class="film-note">Each column is one token; each row a layer (layer 0 at
      the top, the mouth at the bottom — same orientation as the core sample).
      A readout column shows the workspace <em>after</em> reading that token,
      <em>while choosing the next one</em>. Colored cells: a tracked word holds
      rank ≤ 20 there (deeper = closer to rank 1); gray cells shade with the
      lens's top-1 confidence. Click anywhere — the strip, a token, the worms —
      to move the playhead.</p>
    <div class="legend" data-f="legend"></div>
    <div class="film-transcript" data-f="transcript"></div>
    <div class="film-controls">
      <button class="pos-tab" data-f="prev" title="step back">‹</button>
      <button class="pos-tab" data-f="play">▶ play</button>
      <button class="pos-tab" data-f="next" title="step forward">›</button>
      <span class="film-where" data-f="where"></span>
    </div>
    <div class="film-scroll" data-f="scroll">
      <canvas data-f="strip"></canvas>
      <div class="film-playhead" data-f="playhead"></div>
    </div>
    <h4 class="film-sub">Word worms — each tracked word's best rank anywhere in the stack, token by token</h4>
    <div class="chart-wrap"><svg data-f="worms" role="img"
      aria-label="Best lens rank of tracked words per generated token"></svg></div>
    <h4 class="film-sub">Ridgelines — the whole stack, one word at a time (layer 0 in back, the mouth in front)</h4>
    <p class="film-note">Chips toggle — up to 4 words overlay in one canvas;
      each chip's color follows the word by selection order, not its
      position in the current set (toggling others never recolors it).</p>
    <div class="film-controls film-ridge-words" data-f="ridge-words"></div>
    <div class="legend" data-f="ridge-legend"></div>
    <div class="film-scroll"><canvas data-f="ridge"></canvas></div>
    <h4 class="film-sub" data-f="col-title"></h4>
    <div class="readout-scroll" data-f="column"></div>
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

function initFilm(rec, film, rootEl, uid, sync) {
  const q = (r) => rootEl.querySelector(`[data-f="${r}"]`);
  const frames = film.frames, layers = film.layers, n = frames.length;
  const nL = layers.length;

  // fixed color assignment for the strip/worms/legend: the 8 tracked words
  // that ever get closest to rank 1 anywhere in the film, in prominence
  // order (never reassigned later). The ridgeline overlay below uses a
  // SEPARATE, selection-order-based assignment — see the ridge block.
  const best = {};
  for (const w of film.track)
    best[w] = Math.min(...frames.map((f) => Math.min(...f.ranks[w])));
  const colored = [...film.track].sort((a, b) => best[a] - best[b])
    .filter((w) => best[w] <= 50).slice(0, 8);
  const colorOf = {};
  colored.forEach((w, i) => { colorOf[w] = css(SERIES[i]); });

  q("legend").innerHTML = colored.map((w) =>
    `<span class="key"><span class="swatch" style="background:${colorOf[w]}"></span>${esc(w)} <span style="color:var(--muted)">(best #${best[w]})</span></span>`
  ).join("") + `<span class="key" style="color:var(--muted)">tracked words never reaching rank ≤ 50 stay uncolored</span>`;

  // ---- transcript ribbon
  const ribbon = q("transcript");
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
  const canvas = q("strip");
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
  drawWorms(film, frames, colored, colorOf, g0, q("worms"));

  // ---- ridgelines (2.5D: one ridge per layer, elevation = log-rank),
  // multi-select overlay: chips toggle words on/off (min 1, max 4 at once).
  // Colors come from `slotOf`, a map assigned at SELECTION time (smallest
  // free --s1..--s8 slot among the currently-selected words) rather than
  // from a word's position in the current selection — so a word keeps its
  // color while other chips toggle, and only gives its slot back when it
  // is itself deselected.
  const rw = q("ridge-words");
  const ridgeLegend = q("ridge-legend");
  const ridgeCanvas = q("ridge");
  let ridgeSel = colored.length ? [colored[0]] : [];
  const slotOf = new Map();
  if (ridgeSel.length) slotOf.set(ridgeSel[0], 0);
  const ridgeColor = (w) => css(SERIES[slotOf.get(w)]);

  function renderRidgeChips() {
    rw.innerHTML = colored.map((w) => {
      const sel = ridgeSel.includes(w);
      const style = sel ? ` style="border-color:${ridgeColor(w)};color:${ridgeColor(w)}"` : "";
      return `<button class="pos-tab" data-w="${esc(w)}" aria-selected="${sel}"${style}>${esc(w)}</button>`;
    }).join("");
  }
  function renderRidgeLegend() {
    ridgeLegend.innerHTML = ridgeSel.map((w) =>
      `<span class="key"><span class="swatch" style="background:${ridgeColor(w)}"></span>${esc(w)}</span>`).join("");
  }
  function renderRidgeCanvas() {
    drawRidge(film, frames, ridgeSel, ridgeColor, cw, GUT, g0, ridgeCanvas);
  }
  function toggleWord(w) {
    const idx = ridgeSel.indexOf(w);
    if (idx >= 0) {
      if (ridgeSel.length === 1) return; // at least one word stays selected
      ridgeSel.splice(idx, 1);
      slotOf.delete(w);
    } else {
      if (ridgeSel.length >= 4) return; // cap at 4 overlaid words
      const used = new Set(ridgeSel.map((x) => slotOf.get(x)));
      let slot = 0;
      while (used.has(slot)) slot++;
      slotOf.set(w, slot);
      ridgeSel.push(w);
    }
    renderRidgeChips();
    renderRidgeLegend();
    renderRidgeCanvas();
  }
  rw.addEventListener("click", (ev) => {
    const b = ev.target.closest("button");
    if (b) toggleWord(b.dataset.w);
  });
  renderRidgeChips();
  renderRidgeLegend();
  renderRidgeCanvas();

  // ---- playhead state
  const playhead = q("playhead");
  playhead.style.width = (cw - 1) + "px";
  playhead.style.height = (nL * ch) + "px";
  let cur = -1, timer = null;
  const playBtn = q("play");

  // cross-record sync (compare view only; `sync` is undefined on the
  // single-record page, so all of this is inert there). A moved playhead
  // broadcasts its position as a FRACTION OF THE GENERATED SPAN — frames
  // g0..n-1, i.e. from the first generated token to the last — rather than
  // a raw frame index or a fraction of the whole film. Compared records
  // can have differently sized prompts (runway) and different generation
  // lengths; "the same moment in the answer" is the only alignment that
  // stays meaningful across them. Scrubbing inside the prompt/runway
  // (cur < g0) doesn't broadcast — there's no shared runway to align on.
  let quiet = false;
  function broadcastFrame(i) {
    if (!sync || !sync.enabled() || quiet) return;
    const genLen = n - g0;
    if (i < g0 || genLen <= 1) return;
    sync.broadcast(uid, (i - g0) / (genLen - 1));
  }
  function gotoFraction(frac) {
    const genLen = n - g0;
    if (genLen <= 1) return;
    quiet = true;
    setFrame(Math.round(g0 + frac * (genLen - 1)));
    quiet = false;
  }
  if (sync) sync.register(uid, { gotoFraction });

  function setFrame(i, scroll = true) {
    cur = Math.max(0, Math.min(n - 1, i));
    const f = frames[cur];
    playhead.style.left = (GUT + cur * cw) + "px";
    ribbon.querySelectorAll(".ftok").forEach((b) =>
      b.toggleAttribute("aria-current", Number(b.dataset.i) === cur));
    const next = film.tokens[f.pos + 1];
    q("where").textContent =
      `pos ${f.pos} · after ${JSON.stringify(film.tokens[f.pos])}` +
      (next !== undefined ? ` · next ${JSON.stringify(next)}` : "");
    q("col-title").textContent =
      `Column at ${JSON.stringify(film.tokens[f.pos])} — the stack while choosing ` +
      (next !== undefined ? JSON.stringify(next) : "the next token");
    const trackSet = new Set(film.track.map((w) => w.toLowerCase()));
    const mark = (t) => `<span class="tok${trackSet.has(t.trim().toLowerCase()) ? " hit" : ""}">${esc(t)}</span>`;
    q("column").innerHTML = `<table class="readout">
      <thead><tr><th>layer</th><th>lens top-k</th><th>ranks here</th></tr></thead>
      <tbody>${layers.map((l, j) => {
        const hits = film.track.filter((w) => f.ranks[w][j] <= RMAX)
          .sort((a, b) => f.ranks[a][j] - f.ranks[b][j])
          .map((w) => `${esc(w)} #${f.ranks[w][j]}`).join(" · ");
        return `<tr><td class="lyr">L${l}</td><td>${f.top[j].map(mark).join("")}</td>
          <td class="film-ranks">${hits}</td></tr>`;
      }).join("")}</tbody></table>`;
    if (scroll) {
      const sc = q("scroll");
      const x = GUT + cur * cw;
      if (x < sc.scrollLeft + GUT || x > sc.scrollLeft + sc.clientWidth - 40)
        sc.scrollLeft = x - sc.clientWidth / 2;
      const tb = ribbon.querySelector(`[data-i="${cur}"]`);
      if (tb) tb.scrollIntoView({ block: "nearest", inline: "nearest" });
    }
    broadcastFrame(cur);
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
  q("prev").addEventListener("click", () => { stop(); setFrame(cur - 1); });
  q("next").addEventListener("click", () => { stop(); setFrame(cur + 1); });
  ribbon.addEventListener("click", (ev) => {
    const b = ev.target.closest(".ftok");
    if (b) { stop(); setFrame(Number(b.dataset.i)); }
  });

  // strip hover tooltip + click (the tooltip div is a page-level singleton
  // shared with the rank chart — only one can be visible at a time anyway,
  // so it doesn't need per-instance scoping)
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

  quiet = true;
  setFrame(g0 > 0 ? g0 : 0, false); // initial frame: don't broadcast before every column has registered
  quiet = false;
}

function drawRidge(film, frames, words, colorFn, cw, GUT, g0, canvas) {
  const layers = film.layers, nL = layers.length, n = frames.length;
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
  const multi = words.length > 1;
  // solo (today's rendering, unchanged): opaque --surface fill occludes
  // the ridges behind it, layer 0 in back to the mouth in front. Overlay
  // (>1 word): same per-layer back-to-front painting, but the fill swaps
  // from opaque surface to a translucent tint of the word's own color
  // (the "fill-alpha trick") so overlapping words both stay legible; words
  // paint back-to-front in SELECTION order (first picked = furthest back).
  words.forEach((word, wi) => {
    const color = colorFn(word);
    for (let j = 0; j < nL; j++) {
      const base = A + 12 + j * step;
      ctx.beginPath();
      ctx.moveTo(GUT, base);
      for (let i = 0; i < n; i++)
        ctx.lineTo(GUT + i * cw + cw / 2, base - v(frames[i].ranks[word][j]) * A);
      ctx.lineTo(GUT + n * cw, base);
      ctx.closePath();
      if (multi) { ctx.globalAlpha = 0.16; ctx.fillStyle = color; }
      else { ctx.globalAlpha = 1; ctx.fillStyle = surface; }
      ctx.fill();
      ctx.globalAlpha = 0.25 + 0.75 * (j / (nL - 1));
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.4;
      ctx.stroke();
      ctx.globalAlpha = 1;
      if (wi === 0 && (j % 8 === 0 || j === nL - 1)) {
        ctx.fillStyle = muted;
        ctx.fillText("L" + layers[j], 2, base + 3);
      }
    }
  });
  if (g0 > 0) {
    ctx.strokeStyle = muted; ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(GUT + g0 * cw - 0.5, 6);
    ctx.lineTo(GUT + g0 * cw - 0.5, H - 6);
    ctx.stroke(); ctx.setLineDash([]);
  }
}

function drawWorms(film, frames, colored, colorOf, g0, svg) {
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

/* ---- findings map: curated headline results, grouped by theme, each card
   linking straight to its records. The landing page. */
async function showFindings() {
  const detail = document.getElementById("detail");
  const data = await fetch("findings.json")
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  if (!data) {
    detail.innerHTML = `<p class="empty">Could not load findings.json.</p>`;
    return;
  }
  const mshort = (id) => (id.match(/(g4b|g12b|q27b)$/) || [])[1] || "";
  const card = (it) => {
    const ge = INDEX.find((e) => e.id === it.ids[0]);
    return `
    <div class="find-card${it.novelty && it.novelty.verdict === "novel" ? " novel" : ""}">
      <div class="fc-head">
        ${ge ? `<a class="fc-glyph" href="#${esc(ge.id)}"
          title="${esc(ge.id)} — this finding's core sample; open the record">${glyph(ge.emergence, 12, 62)}</a>` : ""}
        <h4>${it.t} ${novChipHTML(it.novelty)}</h4>
      </div>
      <p>${it.b}</p>
      <div class="chips">
        ${it.ids.map((id) => `<a class="chip rec" href="#${esc(id)}"
          title="${esc(id)}">${esc(id.replace(/-(g4b|g12b|q27b)$/, ""))}
          <b>${mshort(id)}</b></a>`).join("")}
        <a class="chip unitlink" href="#unit/${esc(it.unit)}">unit ${esc(it.unit)} →</a>
      </div>
    </div>`;
  };
  detail.innerHTML = `
    <div class="exp-head"><div class="exp-title find-hero">
      <h2>Findings map</h2>
      <p class="find-lead">A home lab that asks small language models what
        they feel — and watches each answer being <em>made</em>, layer by
        layer, before it reaches the mouth.</p>
      <div class="door-row">
        <a class="door" href="#essay">I'm curious <span class="door-arrow">→</span> read the essay</a>
        <a class="door" href="#explore">I'm a researcher <span class="door-arrow">→</span> explore ${INDEX.length} records</a>
        <a class="door" href="../llms.txt">I'm an agent <span class="door-arrow">→</span> llms.txt</a>
      </div>
      <div class="chips"><span class="chip">${data.themes.reduce((n, t) => n + t.items.length, 0)} headline results</span>
        <span class="chip">curated from ${INDEX.length} records</span></div>
      <p class="find-note">
        Each card carries its record's <b>core sample</b> — one band per
        layer, bluer = the answer closer to the surface — and links to the
        raw data. The chronological unit tree lives in the rail; the full
        argument is the <a href="#essay">essay</a>.</p>
    </div></div>
    ${data.themes.map((th) => `
      <section class="card">
        <h3>${th.name}</h3>
        <p class="theme-desc">${th.desc}</p>
        <div class="find-grid">${th.items.map(card).join("")}</div>
      </section>`).join("")}`;
  markCurrent();
  document.querySelector(".detail").scrollTop = 0;
  window.scrollTo({ top: 0 });
}

/* ---- compare view: two or three records side by side (#cmp/idA,idB[,idC]).
   Compact columns — glyph, chips, conversation, thoughts — with links to the
   full records. Readout/chart/scan/slice stay single-record only, but the
   film player is componentized (filmHTML/initFilm scope everything under a
   per-instance root id — see the film region above), so it now renders once
   per column, lazily, only for the columns whose record actually has film
   data. */
async function showCompare(ids) {
  const detail = document.getElementById("detail");
  ids = ids.slice(0, 3);
  const recs = await Promise.all(ids.map((id) =>
    fetch(`../results/${id}/record.json`).then((r) => (r.ok ? r.json() : null))
      .catch(() => null)));
  const thoughts = await Promise.all(ids.map((id) =>
    fetch(`../results/${id}/thoughts.md`).then((r) => (r.ok ? r.text() : null))
      .catch(() => null)));
  if (recs.some((r) => !r)) {
    detail.innerHTML = `<p class="empty">Could not load ${esc(ids.join(", "))}.</p>`;
    return;
  }
  // lazy-load: only fetch film.json for the columns whose record has one
  const films = await Promise.all(recs.map((rec) =>
    rec.film
      ? fetch(`../results/${rec.id}/${rec.film}`).then((r) => (r.ok ? r.json() : null)).catch(() => null)
      : Promise.resolve(null)));
  const anyFilm = films.some(Boolean);

  const col = (rec, th, film, i) => `
    <div class="cmp-col">
      <div class="cmp-head">
        <span class="glyph-lg">${glyph(rec.emergence.ranks, 12, 90)}</span>
        <div>
          <h3><a href="#${esc(rec.id)}">${esc(rec.title)}</a></h3>
          <div class="chips">
            <span class="chip model">${esc(rec.model.name)}</span>
            <span class="chip">${rec.model.quant ? esc(rec.model.quant) : "bf16"}</span>
            <span class="chip">top1 <code class="tok">${esc(visTok(rec.emergence.top1))}</code></span>
          </div>
        </div>
      </div>
      ${conversationHTML(rec)}
      ${th ? `<section class="card thoughts"><h3>Claude's thoughts</h3>
        ${th.trim().split(/\n\s*\n/).map((p) => `<p>${inline(p)}</p>`).join("")}
      </section>` : ""}
      <p class="cmp-more"><a href="#${esc(rec.id)}">full record (readouts, chart, film) →</a></p>
      ${film ? filmHTML(rec, film, `cmp${i}`) : ""}
    </div>`;
  detail.innerHTML = `
    <div class="exp-head"><div class="exp-title">
      <h2>Side by side</h2>
    </div></div>
    ${anyFilm ? `<label class="film-sync-toggle">
      <input type="checkbox" id="cmp-film-sync" checked>
      sync playheads
      <span class="film-sync-hint">— matches the fraction of each column's generated span (records differ in length; see the code comment in initFilm)</span>
    </label>` : ""}
    <div class="cmp-grid cols-${recs.length}">
      ${recs.map((r, i) => col(r, thoughts[i], films[i], i)).join("")}
    </div>`;
  markCurrent();
  // Wire each column's film player after its DOM exists. `sync` is a tiny
  // shared registry: any film whose playhead moves calls sync.broadcast,
  // which relays the fraction to every other registered film's
  // gotoFraction (see the "cross-record sync" comment inside initFilm for
  // exactly what that fraction means and why).
  const syncBox = document.getElementById("cmp-film-sync");
  const controllers = new Map();
  const sync = {
    enabled: () => !syncBox || syncBox.checked,
    register(uid, ctrl) { controllers.set(uid, ctrl); },
    broadcast(fromUid, frac) {
      for (const [uid, ctrl] of controllers)
        if (uid !== fromUid) ctrl.gotoFraction(frac);
    },
  };
  films.forEach((film, i) => {
    if (!film) return;
    initFilm(recs[i], film, document.getElementById(`filmroot-cmp${i}`), `cmp${i}`, sync);
  });
  window.scrollTo({ top: 0 });
}

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

/* =================== research board (#board) =================== */
/* Source: ../board/board.json — arcs of items, each with a lifecycle
   state (see the "states" dict for meanings). One section per arc,
   ordered as in the JSON; items within an arc ordered hot > queued >
   hunch > parked > landed > dissolved > dropped (live/actionable first). */
const BOARD_STATE_ORDER =
  ["hot", "queued", "hunch", "parked", "landed", "dissolved", "dropped"];
const BOARD_PLURAL = { hunch: "hunches" };

function boardLinkHTML(l) {
  const isHash = l.startsWith("#");
  const href = isHash ? l : `../${l}`;
  const label = isHash
    ? (l.startsWith("#unit/") ? `unit ${l.slice(6)}` : l.slice(1))
    : l.split("/").pop();
  return `<a class="chip board-link" href="${esc(href)}" title="${esc(l)}">${esc(label)}</a>`;
}

/* novelty verdict vs published research (set via board.py nov after a
   literature scout): ★ novel · ◐ anticipated · ≡ covered */
const NOV_GLYPH = { novel: "★", anticipated: "◐", covered: "≡" };

function novChipHTML(nov) {
  if (!nov || !NOV_GLYPH[nov.verdict]) return "";
  const tip = `${nov.basis || ""}${nov.closest ? ` — closest: ${nov.closest}` : ""}`;
  return `<span class="board-chip nov-${esc(nov.verdict)}" title="${esc(tip)}">
    ${NOV_GLYPH[nov.verdict]} ${esc(nov.verdict)}</span>`;
}

function boardItemHTML(it, statesMeta) {
  const note = (it.notes || [])[it.notes.length - 1];
  const nov = it.novelty;
  return `<div class="board-item">
    <span class="board-chip state-${esc(it.state)}" title="${esc(statesMeta[it.state] || it.state)}">
      <i class="board-dot" aria-hidden="true"></i>${esc(it.state)}</span>
    <h4 class="board-item-title">${esc(it.title)} ${novChipHTML(nov)}</h4>
    ${note ? `<p class="board-note"><span class="board-note-date">${esc(note.date)}</span>${esc(note.text)}</p>` : ""}
    ${nov && nov.basis ? `<p class="board-note board-nov">${NOV_GLYPH[nov.verdict]} ${esc(nov.basis)}${nov.closest ? ` <span class="board-nov-closest">closest: ${esc(nov.closest)}</span>` : ""}</p>` : ""}
    ${(it.links || []).length ? `<div class="chips board-links">${it.links.map(boardLinkHTML).join("")}</div>` : ""}
  </div>`;
}

function boardArcHTML(arc, statesMeta) {
  const items = [...arc.items].sort((a, b) =>
    BOARD_STATE_ORDER.indexOf(a.state) - BOARD_STATE_ORDER.indexOf(b.state));
  return `<section class="card board-arc">
    <div class="board-arc-head">
      <h3>${esc(arc.title)}</h3>
      <span class="board-status board-status-${esc(arc.status)}">${esc(arc.status)}</span>
    </div>
    <p class="board-question">${esc(arc.question)}</p>
    <div class="board-items">${items.map((it) => boardItemHTML(it, statesMeta)).join("")}</div>
  </section>`;
}

async function showBoard() {
  const detail = document.getElementById("detail");
  if (!BOARD) {
    BOARD = await fetch("../board/board.json")
      .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  }
  if (!BOARD) {
    detail.innerHTML = `<p class="empty">Could not load ../board/board.json.</p>`;
    return;
  }
  const counts = {};
  let n = 0;
  for (const arc of BOARD.arcs) for (const it of arc.items) {
    counts[it.state] = (counts[it.state] || 0) + 1;
    n++;
  }
  const summary = BOARD_STATE_ORDER.filter((s) => counts[s])
    .map((s) => `${counts[s]} ${esc(BOARD_PLURAL[s] || s)}`).join(" · ");
  detail.innerHTML = `
    <div class="exp-head"><div class="exp-title">
      <h2>Research board</h2>
      <div class="chips"><span class="chip">${BOARD.arcs.length} arcs</span>
        <span class="chip">${n} items</span>
        <span class="chip">updated ${esc(BOARD.updated)}</span></div>
      <p class="board-summary">${summary}</p>
    </div></div>
    ${BOARD.arcs.map((arc) => boardArcHTML(arc, BOARD.states || {})).join("")}`;
  markCurrent();
  document.querySelector(".detail").scrollTop = 0;
  window.scrollTo({ top: 0 });
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

/* =================== records explorer (#explore) =====================
   Deep-linkable state lives in the hash query, parsed/serialized here:
     #explore?m=qwen-27b&u=15&f=film,steer&v=matrix
   m = model (all|<MODELS value>), u = unit ("all"|"0".."15"),
   f = comma list of active toggles (film, steer, thoughts), v = table|matrix.
   Facets AND-combine. Table sort state is local-only (not deep-linked —
   the spec's hash schema only names m/u/f/v). */
const EX_DEFAULT = { m: "all", u: "all", f: [], v: "table" };
const EX_TOGGLES = [["film", "✦ filmed"], ["steer", "⇄ steered"], ["thoughts", "✳ commentary"]];
const EX_SORT_KEYS = {
  id: (e) => e.id, title: (e) => e.title, model: (e) => e.model,
  unit: (e) => (Number.isFinite(+e.unit) ? +e.unit : 99),
  created: (e) => e.created,
};
let EX = { ...EX_DEFAULT };
let exSort = { key: "unit", dir: "asc" }; // default sort: unit then created

function exParseHash(h) {
  const state = { ...EX_DEFAULT, f: [] };
  const qIdx = h.indexOf("?");
  if (qIdx === -1) return state;
  const params = new URLSearchParams(h.slice(qIdx + 1));
  if (params.has("m")) state.m = params.get("m");
  if (params.has("u")) state.u = params.get("u");
  if (params.has("f")) state.f = params.get("f").split(",").filter(Boolean);
  if (params.has("v")) state.v = params.get("v");
  return state;
}

function exSerializeHash(state) {
  const params = new URLSearchParams();
  if (state.m !== EX_DEFAULT.m) params.set("m", state.m);
  if (state.u !== EX_DEFAULT.u) params.set("u", state.u);
  if (state.f.length) params.set("f", state.f.join(","));
  if (state.v !== EX_DEFAULT.v) params.set("v", state.v);
  const qs = params.toString();
  return "explore" + (qs ? "?" + qs : "");
}

// replaceState-style: updates the URL/hash without pushing history or
// firing hashchange (which would otherwise re-enter route() -> showExplore).
function exUpdateHash() {
  history.replaceState(null, "", "#" + exSerializeHash(EX));
}

function exFiltered() {
  return INDEX.filter((e) =>
    (EX.m === "all" || e.model === EX.m) &&
    (EX.u === "all" || String(e.unit) === EX.u) &&
    (!EX.f.includes("film") || e.film) &&
    (!EX.f.includes("steer") || !!e.steer) &&
    (!EX.f.includes("thoughts") || e.has_thoughts));
}

function exStatsLine() {
  const nModels = new Set(INDEX.map((e) => e.model)).size;
  const nUnits = new Set(INDEX.map((e) => e.unit)).size;
  const nFilm = INDEX.filter((e) => e.film).length;
  const nSteer = INDEX.filter((e) => e.steer).length;
  const nThoughts = INDEX.filter((e) => e.has_thoughts).length;
  return `${INDEX.length} records · ${nModels} models · ${nUnits} units · ` +
    `${nFilm} filmed · ${nSteer} steered · ${nThoughts} with commentary`;
}

function showExplore(h) {
  EX = exParseHash(h);
  const detail = document.getElementById("detail");
  detail.innerHTML = `
    <div class="exp-head"><div class="exp-title">
      <h2>Explorer</h2>
      <p class="ex-stats" id="ex-stats">${esc(exStatsLine())}</p>
    </div></div>
    <section class="card ex-controls">
      <div class="chip-row" id="ex-model-chips" role="group" aria-label="Filter by model"></div>
      <div class="ex-control-row">
        <label class="ex-unit-label" for="ex-unit">unit
          <select id="ex-unit"></select>
        </label>
        <div class="chip-row" id="ex-toggle-chips" role="group" aria-label="Filters"></div>
        <div class="chip-row" id="ex-view-chips" role="group" aria-label="View mode"></div>
      </div>
    </section>
    <p class="ex-count" id="ex-count"></p>
    <div id="ex-results"></div>`;
  exRenderControls();
  exRenderResults();
  markCurrent();
  document.querySelector(".detail").scrollTop = 0;
  window.scrollTo({ top: 0 });
}

function exRenderControls() {
  document.getElementById("ex-model-chips").innerHTML = ["all", ...MODELS].map((m) =>
    `<button class="fchip" data-exm="${esc(m)}" aria-pressed="${m === EX.m}">
      ${m === "all" ? "all models" : esc(MSHORT[m])}</button>`).join("");
  const units = Object.keys(UNIT_NAMES).sort((a, b) => a - b);
  const unitSel = document.getElementById("ex-unit");
  unitSel.innerHTML = `<option value="all">all units</option>` +
    units.map((u) => `<option value="${esc(u)}">${esc(UNIT_NAMES[u])}</option>`).join("");
  unitSel.value = EX.u;
  document.getElementById("ex-toggle-chips").innerHTML = EX_TOGGLES.map(([k, label]) =>
    `<button class="fchip" data-exf="${k}" aria-pressed="${EX.f.includes(k)}">${label}</button>`).join("");
  document.getElementById("ex-view-chips").innerHTML = ["table", "matrix"].map((v) =>
    `<button class="fchip" data-exv="${v}" aria-pressed="${EX.v === v}">${v}</button>`).join("");

  document.querySelectorAll("#ex-model-chips [data-exm]").forEach((b) =>
    b.addEventListener("click", () => { EX.m = b.dataset.exm; exUpdateHash(); exRenderControls(); exRenderResults(); }));
  unitSel.addEventListener("change", (e) => { EX.u = e.target.value; exUpdateHash(); exRenderResults(); });
  document.querySelectorAll("#ex-toggle-chips [data-exf]").forEach((b) =>
    b.addEventListener("click", () => {
      const k = b.dataset.exf;
      EX.f = EX.f.includes(k) ? EX.f.filter((x) => x !== k) : [...EX.f, k];
      exUpdateHash(); exRenderControls(); exRenderResults();
    }));
  document.querySelectorAll("#ex-view-chips [data-exv]").forEach((b) =>
    b.addEventListener("click", () => { EX.v = b.dataset.exv; exUpdateHash(); exRenderControls(); exRenderResults(); }));
}

function exSorted(entries) {
  const key = EX_SORT_KEYS[exSort.key] ? exSort.key : "unit";
  const get = EX_SORT_KEYS[key];
  const dir = exSort.dir === "desc" ? -1 : 1;
  return [...entries].sort((a, b) => {
    const va = get(a), vb = get(b);
    if (va < vb) return -1 * dir;
    if (va > vb) return 1 * dir;
    // tie-break: created, ascending, so the default (unit) sort reads
    // "unit then created" as specced
    return a.created < b.created ? -1 : a.created > b.created ? 1 : 0;
  });
}

function exBadgesHTML(e) {
  return [
    e.film ? `<span class="ex-badge" title="filmed">✦</span>` : "",
    e.steer ? `<span class="ex-badge" title="steered${e.steer.mode ? " · " + esc(e.steer.mode) : ""}${e.steer.alpha ? " α" + e.steer.alpha : ""}">⇄</span>` : "",
    e.has_thoughts ? `<span class="ex-badge" title="commentary">✳</span>` : "",
  ].join("");
}

function exTableHTML(entries) {
  const rows = exSorted(entries);
  const th = (label, key) => {
    const active = exSort.key === key;
    const sortAttr = active ? (exSort.dir === "asc" ? "ascending" : "descending") : "none";
    return `<th aria-sort="${sortAttr}"><button class="ex-sort-btn" data-exsort="${key}" type="button">
      ${esc(label)}${active ? (exSort.dir === "asc" ? " ▲" : " ▼") : ""}</button></th>`;
  };
  return `<div class="readout-scroll"><table class="readout ex-table">
    <thead><tr>
      <th aria-hidden="true"></th>
      ${th("id", "id")}${th("title", "title")}${th("model", "model")}
      ${th("unit", "unit")}${th("created", "created")}<th>badges</th>
    </tr></thead>
    <tbody>${rows.map((e) => `
      <tr class="ex-rec" data-exid="${esc(e.id)}">
        <td>${glyph(e.emergence, 10, 40)}</td>
        <td class="ex-id"><a href="#${esc(e.id)}">${esc(e.id)}</a></td>
        <td>${esc(e.title.replace(/^Unit \d+[A-D]? · /, ""))}</td>
        <td>${esc(MSHORT[e.model] || e.model)}</td>
        <td>${esc(UNIT_NAMES[e.unit] || "Unit " + e.unit)}</td>
        <td class="ex-created">${esc((e.created || "").slice(0, 10))}</td>
        <td class="ex-badges">${exBadgesHTML(e)}</td>
      </tr>`).join("")}</tbody>
  </table></div>`;
}

function exMatrixHTML(entries) {
  const byUnit = {};
  for (const e of entries) (byUnit[e.unit] ??= []).push(e);
  const units = Object.keys(UNIT_NAMES)
    .filter((u) => byUnit[u] && byUnit[u].length)
    .sort((a, b) => a - b);
  const cellHTML = (u, m) => {
    const list = byUnit[u].filter((e) => e.model === m);
    if (!list.length) return `<td class="ex-mtx-cell ex-mtx-empty">—</td>`;
    return `<td class="ex-mtx-cell"><div class="ex-mtx-wrap">
      ${list.map((e) => `<a class="ex-mtx-glyph" href="#${esc(e.id)}"
        title="${esc(e.id)} — ${esc(e.title)}">${glyph(e.emergence, 8, 28)}</a>`).join("")}
    </div></td>`;
  };
  return `<div class="readout-scroll"><table class="readout ex-matrix">
    <thead><tr><th>unit</th>${MODELS.map((m) => `<th>${esc(MSHORT[m])}</th>`).join("")}</tr></thead>
    <tbody>${units.map((u) => `<tr>
      <td class="ex-mtx-unit">${esc(UNIT_NAMES[u])}</td>
      ${MODELS.map((m) => cellHTML(u, m)).join("")}
    </tr>`).join("")}</tbody>
  </table></div>`;
}

function exRenderResults() {
  const entries = exFiltered();
  document.getElementById("ex-count").textContent = `${entries.length} of ${INDEX.length} shown`;
  document.getElementById("ex-results").innerHTML = entries.length
    ? (EX.v === "matrix" ? exMatrixHTML(entries) : exTableHTML(entries))
    : `<p class="empty">Nothing matches these filters.</p>`;
  document.querySelectorAll(".ex-sort-btn").forEach((b) =>
    b.addEventListener("click", () => {
      const key = b.dataset.exsort;
      if (exSort.key === key) exSort.dir = exSort.dir === "asc" ? "desc" : "asc";
      else { exSort.key = key; exSort.dir = "asc"; }
      exRenderResults();
    }));
  document.querySelectorAll(".ex-rec").forEach((tr) =>
    tr.addEventListener("click", (ev) => {
      if (ev.target.closest("a")) return; // let the id link's own navigation happen
      location.hash = tr.dataset.exid;
    }));
}

/* ---- guided tour ----
   First-visit walkthrough, five steps, shown once and guarded by the
   localStorage key `tour-done`. Skipped in screenshot mode (a `?theme=`
   param is present) and on narrow viewports (<700px). boot() already
   calls maybeTour() if it exists (see the typeof check near the end of
   boot()) — this section is self-contained and never touches boot() or
   route(). Re-run it any time from the browser console: window.jspTour().
   No re-trigger UI is exposed in the page itself, by design. */
const TOUR_STEPS = [
  {
    title: "The findings map",
    body: "Curated headline results; every card carries its record's core sample.",
    sel: () => document.querySelector(".find-hero") || document.getElementById("detail"),
  },
  {
    title: "Core samples",
    body: "One band per layer, top = layer 0; bluer = the answer closer to rank 1. Click any to open the raw record.",
    sel: () => document.querySelector(".fc-glyph"),
  },
  {
    title: "The rail",
    body: `All ${INDEX.length || 421} records, chronological by unit; filter with / and flip with j·k.`,
    sel: () => document.getElementById("rail"),
  },
  {
    title: "Compare anything",
    body: "Pin any record, open another, compare side by side — films included.",
    sel: () => document.getElementById("mast-nav"),
  },
  {
    title: "The console",
    body: "Theme + the sediment atmosphere live here. The background columns are real records; one surfaces every few seconds.",
    sel: () => document.getElementById("console-fab"),
  },
];
let tourState = null; // { i, prevFocus } while running; null when closed

function tourClearHighlight() {
  document.querySelectorAll(".tour-highlight")
    .forEach((el) => el.classList.remove("tour-highlight"));
}

function tourGoto(i) {
  tourState.i = i;
  tourClearHighlight();
  const target = TOUR_STEPS[i].sel();
  if (target) {
    target.classList.add("tour-highlight");
    target.scrollIntoView({
      block: "center",
      behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
    });
  }
  tourPaint();
}

function tourPaint() {
  const card = document.getElementById("tour-card");
  if (!card) return;
  const i = tourState.i;
  const step = TOUR_STEPS[i];
  const last = i === TOUR_STEPS.length - 1;
  card.innerHTML = `
    <p class="tour-title">${esc(step.title)}</p>
    <p class="tour-body">${esc(step.body)}</p>
    <div class="tour-foot">
      <div class="tour-dots" aria-hidden="true">
        ${TOUR_STEPS.map((_, k) => `<span class="tour-dot${k === i ? " on" : ""}"></span>`).join("")}
      </div>
      <span class="tour-n">${i + 1}/${TOUR_STEPS.length}</span>
      <div class="tour-btns">
        <button type="button" id="tour-skip">skip tour</button>
        <button type="button" id="tour-next" class="tour-primary">${last ? "done" : "next"}</button>
      </div>
    </div>`;
  document.getElementById("tour-skip").addEventListener("click", tourEnd);
  document.getElementById("tour-next").addEventListener("click", () => {
    if (last) tourEnd(); else tourGoto(i + 1);
  });
}

function tourKeydown(ev) {
  if (ev.key === "Escape") { ev.preventDefault(); tourEnd(); }
}

function tourEnd() {
  tourClearHighlight();
  document.getElementById("tour-card")?.remove();
  document.removeEventListener("keydown", tourKeydown, true);
  localStorage.setItem("tour-done", "1");
  const prev = tourState?.prevFocus;
  tourState = null;
  if (prev && document.contains(prev)) prev.focus();
  else document.body.focus?.();
}

function tourStart() {
  if (document.getElementById("tour-card")) return; // already running
  tourState = { i: 0, prevFocus: document.activeElement };
  const card = document.createElement("div");
  card.id = "tour-card";
  card.className = "tour-card";
  card.setAttribute("role", "dialog");
  card.setAttribute("aria-label", "Site tour");
  card.setAttribute("tabindex", "-1");
  document.body.appendChild(card);
  document.addEventListener("keydown", tourKeydown, true);
  tourGoto(0);
  card.focus();
}

function maybeTour() {
  if (localStorage.getItem("tour-done")) return;
  if (themeParam) return;              // screenshot mode: never interrupt
  if (window.innerWidth < 700) return; // small viewports: skip
  const h = current();
  if (h && h !== "findings") return;   // only auto-fire on the landing page
  // deferred so route()'s async render (showFindings' fetch) has landed
  // before step 1/2 look for .find-hero / .fc-glyph on the default route
  setTimeout(() => {
    if (localStorage.getItem("tour-done")) return; // guard races on fast repeat boots
    tourStart();
  }, 700);
}
window.jspTour = tourStart;
