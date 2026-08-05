# Skin contract — dashboard/

Reference for CSS-only skins loaded after `style.css`. Do not edit
`index.html` or `app.js`. All facts below verified against
`dashboard/app.js` (3612 lines), `dashboard/style.css` (1055 lines),
`dashboard/index.html`, `glossary.html`, `essay.html` on 2026-08-05.

**Skin loading is already wired.** `index.html` has an inline script:
`?skin=paper|instrument|core` loads `dashboard/skins/<name>.css` after
`style.css` (whitelist, no arbitrary URL). A skin file must use one of
those three names to be reachable without editing `index.html`.

**Scope.** Skins style `dashboard/index.html` + `app.js` output only.
`../essay.html` and `../glossary.html` are separate static pages with
their own inline `<style>` (a reduced variable set: `--page --surface
--ink --ink-2 --muted --grid --ring --lens --lens-soft` + fonts) and do
NOT load `style.css` or any skin file. Out of scope, not overridable.

---

## 1. Pill/chip species table

All classes below render as small rounded (`border-radius: 99px` unless
noted) labelled shapes. Counts are per full page render, not per card,
unless stated. Tag and INTERACTIVE/INERT verified at the `app.js` line
that emits the markup.

| Class | Tag | I/O | Views | Example text | Count |
|---|---|---|---|---|---|
| `.chip` (bare) | `span` | INERT | findings (2), record detail (4/rec: hf_id, quant, n_layers, created), unit overview (2), explorer/board headers (2–3) | "gemma-4b bf16" | 2–5 per header |
| `.chip.model` | `span` | INERT | record detail (1), unit overview (0, uses bare), findings themes (0) | "qwen-27b" | 1 per record head |
| `.chip.rec` | `a` (`href="#<id>"`) | INTERACTIVE | findings map only | "u2-feels" **g4b** | ~2–4 per finding card, 90 total on findings.json today |
| `.chip.unitlink` | `a` (`href="#unit/<n>"`) | INTERACTIVE | findings map only | "unit 2 →" | 1 per finding card, 32 total |
| `.chip.sib` / `.chip.sib.cmp` | `a` | INTERACTIVE | record detail (sibling-model switcher) | "g12b" / "⇄ g12b" | 0–4 per record |
| `.chip.pin` | `button` (has `data-pin`/`data-unpin`) | INTERACTIVE | record detail | "⌖ pin for compare" | 1–2 per record |
| `.chip.pin.on` | `span` (no button, unpin button sits next to it) | INERT | record detail, only while a pin is active | "⌖ pinned — open any record to compare" | 0 or 1 |
| `.chip.pchip` | `span` | INERT | record detail, inside `.params` values that are arrays | "42" (a param value) | variable, 0–10 |
| `.chip.board-link` | `a` | INTERACTIVE | board only | "u5c-baseline-water-q27b" | 0–3 per board item |
| `.fchip` | `button` (`aria-pressed`) | INTERACTIVE | rail (every view, model filter: "all models"/g4b/g12b/q27b = 4, always mounted in `#model-chips`), explorer (model/unit-filter/view-mode rows) | "g12b" | 4 in rail always; +6–10 in explorer |
| `.door` | `a` | INTERACTIVE | findings map only (landing funnel) | "I'm curious → read the essay" | 3, fixed |
| `.pos-tab` | `button` | INTERACTIVE | record detail (readout position tabs, film playback ‹/▶/›, film ridge-word toggles), affect (stream-chart series toggles, model/emotion tabs) | "▶ play", "L24" | 3–20+ depending on section |
| `.board-chip.state-*` | `span` (7 modifiers: hunch/queued/hot/landed/dissolved/parked/dropped) | INERT | board (per item + legend), findings map (novelty, see below — no, state is board-only) | "landed" | 1 per board item, 7 in legend |
| `.board-chip.nov-*` | `span` (verdict: novel/anticipated/covered) | INERT | board (per item, when scored), **findings map** (`novChipHTML` reused on finding cards) | "★ novel" | 0–1 per board item/finding card |
| `.board-status.board-status-*` | `span` (active/parked/closed) | INERT | board (per arc heading) | "active" | 1 per arc |
| `.nov-novel`/`.nov-anticipated`/`.nov-covered` | — | — | CSS defines these as standalone selectors (line 793) but `app.js` only ever emits them combined with `.board-chip` (`novChipHTML`) — no standalone use found | — | see board-chip.nov-* |
| `.tk` / `.tk.gloss-see` | `button` | INTERACTIVE | anywhere `termify()` runs: record detail plain summary, findings card `pb`/theme `pdesc`, unit overview plain summary, board plain lead, affect plain lead, `#termpop` "See also" row | underlined term e.g. "workspace" | dense in plain-language prose, 5–30 per page |
| `.aff-chip` | `div` | INERT | affect view only (crossing cards) | "vigilant +0.42" | 3 per affect card |
| `.ex-badge` | `span` | INERT | explorer table only | "✦" / "⇄" / "✳" (icon only) | 0–3 per row |
| `.rail-toggle` | `button` | INTERACTIVE | every view, but `display:none` above 768px — mobile-only pill | "records" | 1, mobile only |
| `.con-reroll` | `button` | INTERACTIVE | console panel (fixed, all views) | "↻ resample records" | 1 |
| `.console-row button` (unnamed) | `button`, static HTML in `index.html`, no distinguishing class | INTERACTIVE | console panel, theme row + atmosphere row | "light" / "dark" / "auto" / "on" / "off" | 5 |

**Two "chip" names are misleading — not actually pill-shaped:**
- `.aff-chip` (style.css:974-976) is a flex row (bar + label), no
  `border-radius`, no border. It reads as a labelled bar-chart legend
  row, not a chip.
- `.ex-badge` (style.css:860-861) is bare colored text (a Unicode glyph),
  no border/radius/background at all.
- `.tk` (style.css:1010-1012) is an inline dotted-underline term, not a
  pill — it sits inside prose, not a chip row.

Do not "fix" these to look like chips without checking with the owner —
listed here only so a skin's generic `[class*=chip]`-style selector
doesn't accidentally rebox them.

**Landing page (`#findings`, default route) ground truth, reconciled:**
inert = 32 `.board-chip.nov-*` (one per finding, all 32 items in
`findings.json` are scored) + 2 bare `.chip` (header counts) = **34**.
Interactive = 90 `.chip.rec` + 32 `.chip.unitlink` + 3 `.door` = **125**.
34 + 125 = **159**, matching the audit that motivated this doc. (The
rail's 4 `.fchip` are mounted on every route including findings but sit
outside `.detail`; they were evidently excluded from that count — worth
knowing if a skin is checked against the same total.)

---

## 2. Surface/container inventory

| Class | Border | Background | Radius | Shadow |
|---|---|---|---|---|
| `section.card` (plain) | `1px solid var(--ring)` | `var(--raised)` | `14px` | `var(--shadow)` |
| `section.card:has(.readout-scroll, .chart-wrap, .params, .scan-cells, [data-f], table.mtx)` | `1px solid var(--bezel)` | `var(--well)` | `8px` | `var(--well-shadow)` |
| `section.card:has(.find-grid)` | none (transparent) | none (transparent) | `0` | none |
| `section.card.plain` (`.card.plain`) | `1.5px solid var(--lens)` | `var(--lens-soft)` | `12px` | none |
| `section.thoughts` | `border-left: 3px solid var(--lens)` only | `var(--lens-soft)` | `0 10px 10px 0` | none |
| `article.essay` | `border-left: 3px solid var(--lens)` only | `var(--lens-soft)` | `0 10px 10px 0` | none |
| `details.notes` | `1px solid var(--grid)` | `var(--surface)` | `10px` | none |
| `.notes-inner` | none | none | — | — |
| `.find-hero` (= `.exp-title.find-hero`) | **none** | **none** | — | — (typographic only: bigger `h2`, no box) |
| `.find-card` | `1px solid var(--ring)` | `var(--surface)` (overrides an earlier `var(--raised)` in the same rule) | `12px` | `var(--shadow)` |
| `.find-grid` | — (layout grid, not a box) | — | — | — |
| `.ov-card` | `1px solid var(--ring)` | `var(--page)` | `9px` | none |
| `.aff-card` | `1px solid var(--grid)` | none | `8px` | none |
| `.film-card` = `section.card.film-card` | inherits `section.card` | inherits | inherits | inherits |
| `.console` | `1px solid var(--ring)` | `var(--surface)` | `12px` | `0 10px 34px rgba(0,0,0,.26)` |
| `.rail` | `border-right: 1px solid var(--grid)` | none (page bg) | — | — |
| `.detail` | none | none (page bg) | — | — |
| `.frame` | — (flex layout row: `.rail` + `.detail`) | — | — | — |
| `#ex-results` | `1px solid var(--bezel)` | `var(--well)` | `8px` | `var(--well-shadow)` |

**Nesting — where a skin border creates a double frame:**

1. **`details.notes` > `.notes-inner` > `section.card` (and `section.thoughts`).**
   Confirmed live on every record detail page (`app.js:1471-1479`
   wraps thoughts + params + chart + readout + scan + slice inside one
   `notesWrap`) and on every unit overview (`app.js:492`). This is the
   single highest-traffic nesting pair in the app — a `.notes` border
   plus each inner `.card`/`.thoughts` border is two frames today.
2. **`section.card` (theme wrapper) > `.find-grid` > `.find-card`.**
   Already de-nested on purpose: the `:has(.find-grid)` rule
   (style.css:366-372) strips the outer card's border/background/shadow
   specifically so only `.find-card` shows a box. A skin that
   restyles `.find-card` without checking this exception restores
   double-boxing; a skin that removes the `:has()` override (e.g. by
   giving `section.card` a background via a broader selector) does too.
3. **`section.card` ("All records") > `.ov-grid` > `.ov-card`.** No
   `:has()` exception exists for this pair — it is double-boxed today
   by design (light `--page`-colored inner boxes on a `--raised` outer
   card). Note this before "fixing" it inconsistently.
4. **`section.card` (affect crossings) > `.aff-gallery` > `.aff-card`.**
   Same shape as #3, also un-exempted.
5. `.card.plain` and `section.thoughts`/`article.essay` never nest
   inside another `.card` — they are used as standalone top-level or
   pre-notes elements, not inside `.notes-inner` except thoughts (see #1).

---

## 3. Views and entry selectors

Every route renders into the single `<main class="detail" id="detail">`
(there is one DOM mount point, not one per view). `route()` (app.js:335)
dispatches on `location.hash`:

| Hash | Function | Top wrapper written into `#detail` |
|---|---|---|
| *(empty)* or `#findings` | `showFindings()` | `.exp-head > .exp-title.find-hero`, then `section.card` per theme |
| `#essay` | `showEssay()` | `article.essay.thoughts` |
| `#board` | `showBoard()` | `.exp-head > .exp-title`, then `section.card.plain`, then `section.card.board-arc` per arc |
| `#affect` | `showAffect()` | `section.card.plain`, then `details.notes`-wrapped charts, `.aff-gallery` |
| `#explore` or `#explore?...` | `showExplore(h)` | `.exp-head > .exp-title`, `section.card.ex-controls`, `#ex-results` (table or matrix) |
| `#cmp/<id>[,<id>][,<id>]` | `showCompare(ids)` | `.cmp-grid.cols-2` or `.cmp-grid.cols-3` |
| `#unit/<n>` | `showUnit(u)` | `.exp-head > .exp-title`, `.unit-plain`, `details.notes`, `section.card > .ov-grid` |
| `#<record-id>` (anything else matching `INDEX`) | `show(h)` (defined ~app.js:1430) | `.pager`, `headHTML` (`.exp-head`), `plainHTML` (`.card.plain`), conversation, film, `details.notes` |

Not an `app.js` route: `../glossary.html` and `../essay.html` are
separate static files (linked from `.masthead-nav`), each a standalone
page outside the SPA and outside skin scope (see header of this doc).

---

## 4. Things a skin MUST NOT break

**The `css()` helper** (app.js:9): `getComputedStyle(document.documentElement).getPropertyValue(v).trim()`.
Variables it reads, confirmed by grep of every `css("--…")` and
`css(SERIES[i])` call site:
`--lens`, `--lens-soft`, `--surface`, `--grid`, `--muted`, `--ink-2`,
`--axis`, and `--s1`..`--s8` (via the `SERIES` array, app.js:8: used for
chart line colors, ridge-word colors, stream-chart series colors,
danger-crossing swatches). If a skin redefines any of these to something
transparent/too-close-to-background, the affected canvas draw (chart,
ridge, stream chart, cast-vs-broken glyphs) becomes unreadable — CSS is
carrying data, not decoration, there.

**The `--seq-*` ramp is read directly in HTML, not through `css()`.**
`glyph()` (app.js:414-423) emits `<i style="background:var(--seq-100..700)">`
inline per layer-band — this is the core-sample glyph itself
(`.glyph`, `.glyph-lg`, `.fc-glyph` all call `glyph()`). It is a 5-step
sequential ramp (`--seq-100/250/400/550/700`) encoding log-rank distance
to the model's actual next token: **darker/deeper = closer to rank 1**.
A skin must keep these 5 steps monotonic in perceived lightness/depth in
both themes, or the glyph — the site's signature visualization, present
on the masthead, every rail row, every finding card, every unit-overview
card, and record detail heads — silently misreports which layer "knew
the answer."

**`--s1`..`--s8`** are categorical series slots (chart lines, ridge
colors, `SERIES` array). Also double-referenced indirectly:
`.state-hunch { --dot: var(--s5); }` etc. (style.css:769-775) assign
each of the 7 board states a `--dot` custom property sourced from an
`--s*` slot, consumed by `.board-dot { background: var(--dot); }`. A
skin that omits `--s3`/`--s5`/`--s2`/`--s6`/`--s7`/`--axis` (the ones
used by board states) drops board-status dot color, not just chart
color.

**`.fc-glyph` / `.glyph` / `.glyph-lg`** — same component (`glyph()`),
different sizes (`10×40`, `8×54`, `16×120`, `12×62`, `12×90`, `8×28`).
Colour is entirely the `--seq-*` ramp above; the only other CSS is a
1px `var(--ring)` border and 3px radius. Do not add a background,
gradient, or drop-shadow that would compete with the band colors.

**`.tour-highlight`** (style.css:929-936): the only visual marker for
the guided-tour's current target (`app.js` `tourGoto`, ~line 3145-3155),
a 2px outline that pulses via `tour-pulse` keyframes. If a skin removes
outlines globally (a common reset), the tour still runs (JS-driven) but
becomes silently unable to show which element it means.

**`#termpop` / `.gloss`.** Created once at runtime (`boot()`,
app.js:290-294: `<div id="termpop" class="gloss" hidden>`), styled by
`#termpop { position: absolute; ... }` (style.css:1014-1018). JS sets
`pop.style.top` / `pop.style.left` in px, computed as
`window.scrollY/scrollX + button.getBoundingClientRect()` (app.js:2860-2862)
— that math assumes `position: absolute` (document-relative). **A skin
must not change `#termpop`'s `position` to `fixed` or `static`** — doing
so misplaces every glossary popover (triggered by any `.tk` button,
which is most pages). `.gloss > span` / `.gloss > a` block-formatting
(style.css:1047,1054) also must survive — it's what keeps the term
name, definition, "see also" row, and "all terms →" link from running
together into one paragraph.

**Undefined-variable trap, not to "fix" as part of a skin:**
`app.js:1155` (unit 13 Stage C evidence table) references
`var(--fg)`, which is defined nowhere in `style.css`, `index.html`, or
any current theme block. Today this makes that inline
`color-mix(in srgb, var(--fg) 8%, transparent)` invalid, so the
gauge-track background is currently invisible (only the hardcoded
`#9085e9` fill bar shows, and it doesn't adapt to light theme). If a
skin happens to define `--fg` for unrelated reasons, this dormant style
activates and starts drawing a track color no one has designed for.

---

## 5. Theme mechanism

Confirmed: `style.css` defines the variable set in exactly **four**
places:

1. `:root { ... }` (style.css:5-29) — the light defaults, unconditional.
2. `:root[data-theme="light"] { ... }` (style.css:30-44) — explicit
   light override, same values as #1 (used when `data-theme` is forced
   by the in-page toggle/console or `?theme=light`).
3. `@media (prefers-color-scheme: dark) { :root { ... } }` (style.css:45-67)
   — dark values, applied automatically when the OS prefers dark AND no
   `data-theme` attribute is set (`:root[data-theme]` is more specific
   and wins whenever present).
4. `:root[data-theme="dark"] { ... }` (style.css:70-85) — explicit dark
   override, same values as #3.

JS theme logic (`app.js:39-65`): precedence is `?theme=` URL param (never
persisted, screenshot mode) > `localStorage["theme"]` (set by the
toggle/console) > OS `prefers-color-scheme`. `data-theme` is only set on
the `<html>` element when there's an explicit choice (URL param or
localStorage); with neither, block #3 (the media query) is what paints
dark mode, not block #4.

**A skin must therefore override in at least three places to be correct
everywhere**: `:root` (block #1, the unconditional light default and
what a skin's own light values should replace), `@media
(prefers-color-scheme: dark) :root` (block #3, the *only* path that
paints a skin's dark palette for a visitor who never touched the
toggle), and `:root[data-theme="dark"]` (block #4, for a visitor who
explicitly chose dark). Skipping `:root[data-theme="light"]` (block #2)
is safe only if a skin's light values equal its `:root` values (as
upstream already does — light is set identically at #1 and #2); if a
skin's `:root` default differs from what it wants for a forced-light
visitor, block #2 needs its own override too.

Full variable set (identical name set in all four blocks except
`color-scheme` and `--serif`/`--sans`/`--mono`, which only exist once,
in `:root`, not repeated per theme):

```
--page --surface --ink --ink-2 --muted --grid --axis --ring
--lens --lens-soft --raised --well --bezel --shadow --well-shadow
--s1 --s2 --s3 --s4 --s5 --s6 --s7 --s8
--seq-100 --seq-250 --seq-400 --seq-550 --seq-700
--serif --sans --mono                              (root-only, not themed)
```

Two variables are referenced with inline fallback values and are NOT
defined in any of the four blocks — `var(--good, #2ecc71)`,
`var(--warn, #e67e22)`, `var(--rule, #8884)` (style.css:607-611, the
unit-15 hot-span table). They currently always resolve to their
fallback. A skin is free to define them (scoped, not part of the core
four-block set) without touching anything above.
