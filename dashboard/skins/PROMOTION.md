# Promotion audit: SPA skin → default, cost to the static mirror

Read-only investigation, 2026-08-05. Answers six questions about what
promoting `dashboard/skins/{core,instrument,paper}.css` from `?skin=`
override to default would cost across `probes/site.py`'s static mirror
(`r/<id>.html` ×499, `essay.html`, `glossary.html`, SEO block, `og/*.png`
×500). No files were changed to produce this report.

Git state at time of writing: `dashboard/skins/` (CONTRACT.md + 3 skin
CSS files), `probes/skincheck.js`, and `snap.sh` are all **untracked**.
`dashboard/index.html`'s `?skin=` loader script is **uncommitted**
(`git diff` shows it as an addition, not yet on any commit). `dashboard/
style.css`, `r/*.html`, `og/*.png`, `essay.html`, `glossary.html`,
`sitemap.xml`, `robots.txt`, `llms.txt` are all committed.

---

## 1. How every generated static page gets its CSS

`probes/site.py` does **not** link `dashboard/style.css`, and does not
read `dashboard/skins/*.css` at all. It emits its own hardcoded rules as
one Python string constant, `PAGE_CSS` (`probes/site.py:258-345`),
inlined verbatim into every page's `<head>` via `<style>{PAGE_CSS}</style>`
(`probes/site.py:371`, inside `head()`). This is the **only** CSS
mechanism for `r/<id>.html`, `essay.html`, and `glossary.html` — a
second, fully independent copy of the design system, not a link, not an
import.

**Drift from `dashboard/style.css`** (`:root` block, `dashboard/
style.css:5-29` and its dark counterpart `:root { }` inside
`@media (prefers-color-scheme: dark)`, `style.css:45-67`), variable by
variable:

| Variable | PAGE_CSS light | style.css light | PAGE_CSS dark | style.css dark | Match? |
|---|---|---|---|---|---|
| `--page` | `#f9f9f7` | `#f9f9f7` | `#0d0d0d` | `#0d0d0d` | yes |
| `--lens` | `#4a3aa7` | `#4a3aa7` | `#9085e9` | `#9085e9` | yes |
| `--grid` | `#e1e0d9` | `#e1e0d9` | `#2c2c2a` | `#2c2c2a` | yes |
| `--ink-2` | `#52514e` | `#52514e` | `#c3c2b7` | `#c3c2b7` | yes |
| `--ink` | `#0b0b0b` | `#0b0b0b` | **`#fff`** | **`#ecebe5`** | **diverged** |
| `--muted` | `#898781` | `#898781` | **`#898781`** (unchanged) | **`#96948d`** | **diverged** |

`--s1`..`--s8`, `--seq-100`..`--seq-700`, `--axis`, `--raised`, `--well`,
`--bezel`, `--shadow`, `--well-shadow` are **absent from PAGE_CSS
entirely** — not drifted, just never defined, because static pages have
no chart/glyph/board-dot components that need them. `PAGE_CSS` also has
only 2 theme blocks, not 4 — see §3.

---

## 2. Class names `site.py` emits, cross-checked against CONTRACT §1/§2

All classes below live in `PAGE_CSS`, not `style.css` — so even where a
name matches an SPA class, the rule governing it on a static page is a
different (and independently maintained) rule.

**Matches CONTRACT §1 (chip table):** `.chip` (bare, `site.py:281,
403-409`), `.chip.model` (`site.py:283, 403`), `.tk` (`site.py:167`,
base form only — no `.tk.gloss-see` variant emitted). 3 classes, all
covered by name — but the CONTRACT's row descriptions document the
`style.css` rule, which is not what applies here.

**Matches CONTRACT §2 (container table):** `section.card` bare
(`site.py:284`, matches the "plain" `section.card (plain)` row),
`section.card.plain` (`site.py:201`, `.card.plain` row), `details.notes`
(`site.py:212`, `details.notes` row), `article.essay`
(`site.py:505,511`, `article.essay` row). 4 names covered.

**Ambiguous — not a clean row match:** `site.py:458` emits
`<section class="card thoughts">` (both classes on one element). CONTRACT
§2 lists `section.card` and `section.thoughts` as two *separate* rows
with different border treatments; it never documents the combined
`.card.thoughts` case as its own entity (app.js does the same combo at
`app.js:2569`, so this isn't unique to the static mirror, but neither
CONTRACT row covers the union).

**Not in §1 or §2 at all — genuinely uncovered (19 classes):**
`.wrap`, `.chips` (distinct from `.chip`), `.turn`, `.role`, `.said`,
`.note` (distinct from `.notes`), `.params` (`dl.params`), `.pager`,
`.spacer`, `.plain-body`, `.thoughts-body`, `.tokval`, `.emg`,
`.emg-scroll`, `.gloss-list`, `.gloss`, `.gloss-rel`, `.notes-t`,
`.notes-s`.

Of these, `.tokval`, `.emg`, `.emg-scroll`, `.gloss-list` don't exist in
`dashboard/style.css` under any name — they are inventions unique to the
static mirror. The rest (`.chips`, `.turn`/`.role`/`.said`, `.params`,
`.pager`, `.plain-body`, `.thoughts-body`, `.gloss`/`.gloss-rel`,
`.notes-t`/`.notes-s`) share a name with an SPA class (verified in
`style.css`) but are restyled independently in `PAGE_CSS`, with no row
in either CONTRACT table.

**Undocumented scope gap:** CONTRACT's own header states "Skins style
`dashboard/index.html` + `app.js` output only... `../essay.html` and
`../glossary.html` are separate static pages... Out of scope, not
overridable" (`CONTRACT.md` lines ~13-17) — naming exactly two files.
It **never names `r/<id>.html`**, the largest static surface (499 files),
even though `record_page()` (`site.py:395-495`) uses the identical
`PAGE_CSS`/`head()` machinery as `essay_page()` and `glossary_page()`.
A skin author who trusts the two named exceptions and doesn't grep
`site.py` would not know 499 more pages are equally out of skin's reach.

---

## 3. Theme mechanism on the static mirror

`PAGE_CSS` defines exactly **2** theme blocks, not the SPA's 4
(`site.py:259-273`):

1. `:root { ... }` — light defaults (unconditional).
2. `@media (prefers-color-scheme: dark) { :root { ... } }` — dark values,
   OS-preference only.

There is **no `[data-theme]` attribute selector anywhere in `PAGE_CSS`**,
and no `<script>` on any static page that sets one. Consequence: the
`?theme=` URL param, the SPA's `localStorage["theme"]`, and the in-page
theme toggle/console (`app.js:39-65`) have **zero effect** on `r/<id>
.html`, `essay.html`, or `glossary.html`. A visitor who explicitly chose
dark in the dashboard and then follows a link to a record's static page
gets whatever their OS reports via `prefers-color-scheme` — their
explicit choice does not travel.

---

## 4. What promoting the new design to default would require

Enumeration only — nothing below was performed.

| Step | File(s) | Why |
|---|---|---|
| Fold chosen skin's rules into the base stylesheet (or repoint the link) | `dashboard/style.css`, `dashboard/index.html` | today `style.css` is the unconditional default; a skin is only reachable via `?skin=` |
| Decide fate of the `?skin=` loader | `dashboard/index.html:20-31` | leave as a harness, or remove per §6 below |
| Update `PAGE_CSS`'s hardcoded values to match | `probes/site.py:258-345` | `PAGE_CSS` does not read `style.css` or any skin file — it must be hand-edited to follow, or the static mirror keeps the old palette forever |
| Regenerate the static mirror | run `.venv/bin/python probes/site.py` | rewrites all 499 `r/<id>.html`, `essay.html`, `glossary.html`, `sitemap.xml`, `llms.txt`, and the SEO block + static-index patch in `dashboard/index.html` (`site.py:748-763`) |
| Update `og.py`'s hardcoded colours | `probes/og.py:34-39` | `VIOLET = (144, 133, 233)` (`#9085e9`, comment ties it to the dashboard `--lens` dark default), `GRID = (44, 44, 42)` (`#2c2c2a`, comment ties it to dashboard `--grid` dark). All three candidate skins move `--lens` dark away from `#9085e9` (`core.css` → `#7cb0ef`, `instrument.css` → `#9a8cff`, `paper.css` → `#dd9370`) and `--grid` dark to a different hex in each case. `og.py` reads none of this from CSS — the 500 committed PNGs go stale (wrong accent colour on every link-preview card) until someone edits the tuples and reruns `.venv/bin/python probes/og.py` |
| Recommit regenerated output | `git add r/ og/ essay.html glossary.html llms.txt sitemap.xml dashboard/index.html` | `r/*.html` (499), `og/*.png` (500), `essay.html`, `glossary.html`, `sitemap.xml`, `llms.txt`, `robots.txt` are all git-tracked (`robots.txt`/`sitemap.xml` confirmed via `git ls-files`) — regenerating locally is not enough, the stale committed copies stay live on the deployed site until pushed |
| Decide fate of dev tooling | `probes/skincheck.js`, `snap.sh` | both are SPA-only (see §6); nothing to change in them for promotion itself, but they lose their comparison purpose once there's only one design |

---

## 5. What breaks if the skin applies only to the SPA

`r/<id>.html` pages link to the dashboard via `../dashboard/#<id>`
(`site.py:429`) and `../dashboard/` (`site.py:447,553`); the dashboard
links out to static pages via the patched static-index block
(`static_index_block()`, `site.py:696-715`, injected into `dashboard/
index.html` between `<!-- static-index:begin/end -->`) and the masthead
nav (`../glossary.html`, `../essay.html`, referenced in CONTRACT's scope
note).

A reader following either link gets a **hard visual cut**: different
palette (whichever skin is promoted vs. `PAGE_CSS`'s untouched values),
different typography scale (`PAGE_CSS`'s single `.wrap{max-width:760px}`
column vs. the SPA's rail+detail frame layout), no glyph component (the
`--seq-*`-driven core-sample bar strip that CONTRACT calls "the site's
signature visualization" doesn't exist in `PAGE_CSS` at all — static
pages show an `<table class="emg">` rank table instead, `site.py:389-391`),
and — per §3 — a dark-mode choice made in the SPA does not follow across
the link, only OS preference does on the static side.

---

## 6. The `?skin=` loader as a prototype harness

`dashboard/index.html:24-31`:

```js
(function () {
  var ALLOWED = ["paper", "instrument", "core", "lab"];
  var s = new URLSearchParams(location.search).get("skin");
  if (ALLOWED.indexOf(s) === -1) return;
  document.write('<link rel="stylesheet" href="skins/' + s + '.css">');
})();
```

**Discrepancy found:** `ALLOWED` has 4 entries, but only 3 CSS files
exist (`core.css`, `instrument.css`, `paper.css` — confirmed via `ls
dashboard/skins/`); there is no `lab.css` anywhere in the repo (`find`
returned nothing). `?skin=lab` passes the whitelist check and then
`document.write`s a `<link>` to a 404. CONTRACT.md's own scope note
(line 9) documents only `paper|instrument|core` — it does not mention
`lab` either, so the doc and the code already disagree with each other,
independent of any promotion decision.

**What depends on it today:**
- `probes/skincheck.js` (untracked) is a devtools-console snippet meant
  to be pasted after loading `http://localhost:8321/dashboard/?theme=
  dark&skin=core` — it inspects `getComputedStyle`, so it depends on the
  loader having already run, but only ever targets `dashboard/`, never
  `r/*.html`.
- `snap.sh` (untracked) takes `[skin]` as its 2nd positional arg and
  appends `&skin=$SKIN` to a `dashboard/$Q$HASH` URL (`snap.sh:15-24`) —
  same SPA-only scope.
- No other file references `?skin=`, `ALLOWED`, or `skins/` (checked
  `essay.html`, `glossary.html`, an `r/*.html` sample: zero hits).

**To remove cleanly:** delete the `<script>` block at `dashboard/
index.html:20-31` (currently an uncommitted addition — `git diff` shows
it was never on a prior commit, so removing it is a pure revert, not a
break of committed history); at that point `skincheck.js` and `snap.sh`
still run without erroring (they just build a URL with a `?skin=` param
the page no longer reads — a silent no-op, not a crash), but their
stated purpose ("compare design languages," `skincheck.js:1-2`) is gone,
so they'd be worth retiring in the same pass rather than leaving as
dead harness scripts. Nothing outside `dashboard/` and these two dev
scripts touches the loader.
