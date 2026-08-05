# Extended tour — feature candidates

Mining pass over `dashboard/app.js` (3755 lines), `dashboard/index.html`,
`dashboard/style.css`, and `dashboard/skins/CONTRACT.md`. Read-only; this is
the only file written. Plain-language rules per `PLAIN-LANGUAGE.md` §3.1
(uncertainty ladder) and §5 (accuracy) applied to every draft body below.

The short 4-step entrance tour (`TOUR_STEPS`, `app.js:3131`) stays as-is and
is not duplicated here. Candidates below are for the longer, on-demand
extended tour.

**Framework note (not a candidate, but load-bearing):** `dashboard/index.html`
already has a console section (`#con-tours`, index.html:112-120) with two
buttons: `#con-tour-entrance` ("restart entrance tour") and
`#con-tour-extended` ("start extended tour"). Neither is wired up in
`app.js` — grep for `con-tour` in `app.js` returns nothing. Both buttons are
inert today. Whoever builds the extended tour needs to wire
`#con-tour-extended` to start it (and probably wire `#con-tour-entrance` to
call the existing `tourStart()`, which currently has no button of its own
outside the findings-page "show the guided tour" link).

---

## 1. The core-sample glyph

**Draft body.** A small colored bar sits next to almost every record. Each
band is one layer of the model. A darker blue means our lens ranked the
model's real answer close to first place at that layer.

**Anchor.** Route `#findings` (default landing page). Selector:
`.find-card:first-child .fc-glyph` (a clickable `<a>` wrapping the glyph;
opens the record). The same glyph also renders inert (not clickable, just a
tooltip) as `.glyph-lg` in the record-detail head (route `#<any-record-id>`,
selector `.exp-head .glyph-lg`).

**Discoverability.** Findable. It's on every card and every rail row, but
nothing on the page states the color rule in one place except a tooltip on
the big header version and one sentence on the findings-page lead
(`.find-note`). A tour step that states the rule once, pointing at one
glyph, saves a reader from hunting for it.

**Priority.** High — it is the site's signature visualization (per
`CONTRACT.md` §4) and appears dozens of times per page; establishing its
meaning early pays off on every later view.

**Broken?** No. Note the asymmetry: everywhere else the glyph is a link to
the record; on the record's own detail page it is inert (title-only). Not a
bug, but worth knowing if the tour points at one on the detail page and
expects it to be clickable.

---

## 2. The film player

**Draft body.** For 285 of 499 records, we recorded the lens readout at
every layer and every word position, so you can play back how the answer
formed, one token at a time.

**Anchor.** Route `#u12-no-q27b` (has film data). Selector: `.film-card`
(a.k.a. `#filmroot-solo`). Controls inside it: `[data-f="play"]` (▶ play /
step ‹ ›), `[data-f="scroll"]` (click the strip to move the playhead),
word-worm chips under `[data-f="wormhost"]`, ridgeline chips under
`[data-f="ridge-words"]`.

**Discoverability.** Findable — it's a large card on any filmed record's
page, but its four sub-parts (strip, word worms, ridgelines, per-column
readout table) are dense enough that a first-time visitor may not realize
the ridgelines and worms are separate, independently toggleable charts, or
that clicking a token in the transcript also moves the playhead.

**Priority.** High — this is the deepest interactive instrument on the
site and the one most likely to be missed if a visitor doesn't scroll into
a record page.

**Broken?** No, but conditional: 214 of 499 records have no film (`rec.film`
unset), and `filmHTML()` shows a plain-text fallback for those. A tour step
must anchor on a record confirmed to have film — `u12-no-q27b` is one
(verified: `results/u12-no-q27b/record.json` has `"film": "film.json"`).

---

## 3. Pin a record, then compare any two

**Draft body.** Open a record, click "pin for compare," then open a second
record. A link appears that puts both side by side.

**Anchor.** Route `#<any-record-id>`, selector `[data-pin]` (the "⌖ pin for
compare" button, in the chips row under the conversation). After pinning,
the compare link appears on every other record page as
`.chip.sib.cmp[href^="#cmp/"]`.

**Discoverability.** Hidden. There is no on-page hint that pinning is a
two-step, cross-page action — a visitor has to notice the pin button, click
it, then separately notice a new chip appeared on the *next* record they
open. Nothing on the pinned record itself says "now go open another one."

**Priority.** High — compare is one of the few analytical tools on the
site, and this is the only way to compare two records that are not the same
probe on different models (see #4 and #15 below for the other paths in).

**Broken?** No — confirmed working end to end (`pinHTML`/`wirePin`,
`app.js:1526-1549`; state lives in `localStorage["cmp-pin"]`).

---

## 4. Three-way compare (URL-only)

**Draft body. ** The compare page can hold three records side by side, not
just two, but nothing in the interface offers a third slot — you have to
add it yourself in the address bar.

**Anchor.** Route `#cmp/<id1>,<id2>,<id3>` (comma-separated, third id has
no UI generator). Selector: `.cmp-grid.cols-3`.

**Discoverability.** Hidden — completely. Every in-page path to `#cmp/...`
(pin chip, sibling ⇄ chip) generates exactly two ids. `showCompare()`
(`app.js:2538-2540`) accepts up to three (`ids.slice(0, 3)`) but nothing
in the UI ever writes a third one into the hash.

**Priority.** Medium — genuinely useful (e.g., comparing all three models'
siblings on one probe at once) but a niche move; worth one tour step
precisely because it is otherwise undiscoverable by any amount of clicking.

**Broken?** No — works if you type the URL. Just unreachable from the UI.

---

## 5. Flip through records with j / k (or arrow keys)

**Draft body.** With a record open, press `j` or `k` to jump to the
previous or next record in the current list, without going back to the
list.

**Anchor.** Route `#<any-record-id>`. No DOM selector needed (a document
keydown handler, `app.js:370-391`); the visible affordance is the pager,
selector `.pager a[title^="previous"]` / `.pager a[title^="next"]` (titles
literally say "previous (j / ←)" / "next (k / →)").

**Discoverability.** Findable, barely — the shortcut is spelled out in two
places: the pager arrow tooltips (hover-only, easy to miss) and the
masthead stats line ("j ‹ › k to flip records," visible small text under
the nav on every page). No on-page label calls it a "keyboard shortcut" in
so many words.

**Priority.** Medium — a fast way to browse 499 records sequentially, and
worth calling out explicitly since the current hint is a hover tooltip and
a small stats line most visitors skim past.

**Broken?** No. Note `j` moves backward and `k` moves forward — the
reverse of typical vim orientation, a deliberate choice per the code
comment ("j sits LEFT of k on the keyboard, so it points backward").

---

## 6. Press / to jump into the filter box

**Draft body.** Press the `/` key anywhere on the site to jump straight
into the record search box, without reaching for the mouse.

**Anchor.** Any route. Selector: `#q` (the filter input in the rail,
`aria-label="Filter experiments"`, placeholder already shows "( / )").

**Discoverability.** Hidden-ish/findable — the placeholder text
`Filter records… ( / )` is the only hint, and it is inside the rail, which
on mobile is a hidden drawer by default.

**Priority.** Low-medium — a small but real efficiency win for a returning
visitor; not essential for a first-time reader.

**Broken?** No (`app.js:376-380`). One conflict worth knowing: pressing
`/` while the guided-tour overlay is open does nothing special (the tour's
own keydown handler only claims Escape/Arrow keys), so `/` still opens the
filter box mid-tour, which could be confusing if a tour step is anchored
inside the rail.

---

## 7. Glossary popovers on hard words

**Draft body.** Any underlined word in the plain-language text can be
clicked. A small box opens with its definition, without leaving the page.

**Anchor.** Route `#findings` (or any page with plain text). Selector:
`.tk` (the first underlined term button in, e.g., `.fc-plain`). Popover
itself: `#termpop`.

**Discoverability.** Obvious visually (dotted underline, per
`CONTRACT.md` §1) once a reader notices the styling, but the interaction
(click, not hover) is not signposted anywhere, and the "See also" chips
inside the popover that chain to related terms are a genuinely hidden
sub-feature.

**Priority.** High — this is the mechanism that makes the whole
plain-language layer work (the 30-second rule from `PLAIN-LANGUAGE.md`
depends on it), and it appears on nearly every page.

**Broken?** No. One nuance: only the *first* use of each term per text
block gets linked (`termify()`, `app.js:2812-2848`, tracks a `used` set) —
later repeats of the same word in the same block are plain text. Not a
bug, just worth knowing if a tour step promises "every hard word is
clickable."

---

## 8. The site publishes itself for AI agents too

**Draft body.** This site has a second, plainer copy of itself, built for
computer programs to read: a summary file, one page per record, and a
full data download.

**Anchor.** Route `#findings`. Selector: `.door[href="../llms.txt"]`
(the "I'm an agent → llms.txt" button in the landing-page door row).
Related surfaces reachable from there: `/llms.txt`, `/r/<id>.html` (one
static page per record, confirmed present — e.g. `/r/u2-feels-q27b.html`
— with its own OG image), `/sitemap.xml`, `/essay.html` (a static twin of
the `#essay` route), and the "data (.zip)" masthead link
(`a[href*="archive/refs/heads/master.zip"]`, index.html:58-60).

**Discoverability.** Findable — the door button is prominent on the
landing page, but almost no visitor is themselves an agent, so most humans
will never click it and never learn the site has this second layer. That
is exactly why it belongs in a tour aimed at humans: it's a deliberate,
unusual design decision worth explaining even to a reader who will never
use it directly.

**Priority.** High — genuinely unusual (per the task brief) and otherwise
invisible to the site's actual (human) visitors.

**Broken?** No — verified `llms.txt`, `r/u2-feels-q27b.html`, `sitemap.xml`,
`essay.html` all exist at the repo root with real content.

---

## 9. The research board and its honesty rules

**Draft body.** This page lists open research questions and their status:
being worked on now, next in line, an untested idea, on hold, finished, or
dropped. Every status word is explained on the page itself.

**Anchor.** Route `#board`. Selector: `.board-legend` (the seven status
chips with plain-word definitions, right under the page's own short
version).

**Discoverability.** Obvious — "Research board" is a top-level nav link,
and the legend is the first thing under the page's plain-language lead.

**Priority.** Medium — worth a step mainly to explain the novelty
verdicts (★ novel / ◐ anticipated / ≡ covered, `NOV_GLYPH`, `app.js:2685`),
which are easy to see but whose meaning ("did published research already
find this?") is not explained inline — only in a hover tooltip
(`.board-chip.nov-*[title]`).

**Broken?** No.

---

## 10. Explorer: filter, sort, and a cross-model matrix

**Draft body.** This page lists every record as a table or as a grid, with
filters for model, unit, and whether a record has film, steering, or notes.
The current filter settings live in the page's own address, so you can
share or bookmark one exact view.

**Anchor.** Route `#explore`. Selector for the matrix mode specifically:
`#ex-view-chips [data-exv="matrix"]` — clicking it shows
`table.ex-matrix`, one glyph per record, grouped by unit (rows) × model
(columns).

**Discoverability.** Obvious that the page exists (nav link "Explorer");
findable that its state is a shareable URL (`#explore?m=qwen-27b&u=15&…`,
`app.js:2900-2937`) — nothing on the page says "this link is now
bookmarkable," and the matrix view in particular is one click away from
the default table but easy to never try.

**Priority.** Medium — a genuinely useful research tool, and the matrix
view is the fastest way to see "which units has which model been run on."

**Broken?** No.

---

## 11. "The original wording" — plain text vs. the lab's own voice

**Draft body.** Every finding on the map is written twice: once in plain
language, and once exactly as the lab first wrote it. A small link under
each card opens the original.

**Anchor.** Route `#findings`. Selector: `.fc-orig` (a `<details>` element,
closed by default, labeled "the original wording").

**Discoverability.** Hidden — it's a closed disclosure triangle at the
bottom of a card that's already dense with text; nothing calls attention
to it besides the summary label itself.

**Priority.** Medium — it's a nice concrete illustration of the whole
plain-language project (see `PLAIN-LANGUAGE.md`: "nothing is deleted, the
original moves into a container"), and a tour step can make that
principle tangible in one click.

**Broken?** No.

---

## 12. The emotion-state overlay

**Draft body.** For 16 conversations, we also measured which of 24
emotions was active inside the model at each word, and lined that reading
up against the film, so you can see what the model said next to what
state it was in.

**Anchor.** Route `#u18-hyst-a0000-q27b` (confirmed to have both film and
affect data). Selector: `#affectroot` (embedded inside the film card as
"The state underneath — emotion overlay").

**Discoverability.** Hidden — it only renders on 16 of 499 records (those
crossed with `affect2.py`), with no index or flag on the rail/findings
list distinguishing which ones have it; a visitor finds it only by landing
on the right record.

**Priority.** Medium — a distinctive cross-instrument view (lens reading
vs. emotion-vector reading), but low reach given how few records carry it;
better paired with a pointer to the `#affect` page (item 12b below) which
is the actual home for this instrument and is nav-reachable.

**Broken?** No.

**12b. The #affect page itself** is nav-reachable ("Affect" link, obvious)
and is the right target if the tour wants one step instead of two: it
hosts the depth-validation charts, the "lensview" per-layer vocabulary
explorer, the crossing gallery (all 16), the danger/vigilance test with
receipts, and the loop-distress chart — all in one place, selector
`.aff-figs` or `.aff-gallery` for a first anchor.

---

## 13. The lab console (theme, sediment field, tour restart)

**Draft body.** A gear button in the corner opens a small panel: switch
between light and dark, turn the drifting background pattern on or off,
and (once wired up) replay either guided tour.

**Anchor.** Any route. Selector: `#console-fab` (the "⚙" button, fixed
position). Panel: `#console`.

**Discoverability.** Hidden — a small fixed-position gear icon with no
label text, easy to mistake for decoration.

**Priority.** Medium — worth surfacing because it's the only way back into
tour replay from most pages (findings-page has its own "show the guided
tour" link, but no other page does), and it explains the atmospheric
background, which a visitor might otherwise dismiss as pure decoration
rather than a real chart drawn from the same records.

**Broken?** The tour-related buttons in this panel are not wired (see the
framework note at the top of this file) — `#con-tour-entrance` and
`#con-tour-extended` currently do nothing on click.

---

## 14. The masthead sparkline

**Draft body.** In the site's header, a small line chart quietly redraws
itself. It is the answer to the lab's very first question, rising through
the model's layers — the discovery that started the whole project.

**Anchor.** Any route. Selector: `#mast-spark-link` (wraps `#mast-spark`
canvas, links to `#u2-feels-q27b`).

**Discoverability.** Hidden — it looks like a logo flourish, not a chart
of real data; its tooltip explains the connection ("the lab's emblem...")
but only on hover, and it's easy to visually merge into the title.

**Priority.** Low-medium — a nice "aha" moment (this decoration is real
data) but not essential to using the site; good as a closing or opening
flourish step precisely because it rewards a visitor who now understands
what a core-sample glyph is (callback to step 1).

**Broken?** No.

---

## 15. Same probe on another model (sibling switcher)

**Draft body.** Many questions were asked to all three models. On a
record's page, a row of buttons jumps straight to the same question asked
of a different model, or opens both side by side.

**Anchor.** Route `#u2-feels-q27b` (has all three model siblings).
Selector: `.chips.sibs .chip.sib.cmp` (the "⇄ g4b" / "⇄ g12b" buttons).

**Discoverability.** Findable — it's a visible chip row under the head of
any record that has siblings, but the distinction between the plain sibling
chip (`.chip.sib`, jumps to that record) and the compare chip
(`.chip.sib.cmp`, opens both side by side) is subtle (one extra glyph, "⇄"
vs. plain text).

**Priority.** Medium — the fastest way into a same-probe-across-models
comparison, which is one of the site's central axes (three models, one
question, three answers).

**Broken?** No.

---

## 16. Filter the record list by model

**Draft body.** Four buttons above the record list narrow it to one model
at a time, or show all three together.

**Anchor.** Any route (rail is present everywhere, may need
`#rail-toggle` on mobile to open the drawer first). Selector:
`#model-chips .fchip[data-m="qwen-27b"]`.

**Discoverability.** Obvious on desktop (sits at the top of the always-
visible rail); hidden on narrow viewports, where the rail is a collapsed
drawer behind `.rail-toggle` and easy to miss on a phone.

**Priority.** Low — basic and mostly self-explanatory, but worth one
step on a mobile-oriented tour run given the drawer is genuinely easy to
never open.

**Broken?** No.

---

## Features that are effectively invisible today, ranked

1. **Pin-then-compare** (item 3) — a two-step, cross-page action with zero
   in-page instruction; the single biggest "nobody would ever find this"
   gap, and it unlocks the site's only cross-record analysis view.
2. **Three-way compare via URL** (item 4) — a working feature with no UI
   path in at all; a visitor would need to read the source to learn it
   exists.
3. **The extended-tour console button** (item 13) — not a content gap but
   an implementation gap: the button visitors would use to start *this
   very tour* is currently wired to nothing.
4. **The `/` filter shortcut and `j`/`k` record-flipping** (items 5, 6) —
   real, working, and named only in a placeholder string and a small
   stats-line hint that most visitors will never read closely.
5. **The emotion-state overlay** (item 12) — a real second instrument
   layered onto the film, present on only 16 records with no listing of
   which ones, discoverable only by chance.
6. **The masthead sparkline's meaning** (item 14) — visually indistinguishable
   from decoration; its status as real, clickable data is easy to miss
   entirely.
