# Tour candidates — how this lab handles being wrong

Mining pass for the extended guided tour. Read-only; no site or data files
touched. Rules applied: PLAIN-LANGUAGE.md §5 (accuracy) and §3.1
(uncertainty ladder) to every draft body below. Evidence is a file path or
record id with the specific line or field that backs the claim.

---

## 1. The lab retracted a result, in public

**Draft body.** In 2026, this lab reported that Qwen 27B went silent when
shown its own answer. The lab later found a software bug: the prompt was
cut at 512 tokens. We were wrong. The corrected run shows Qwen 27B
answers "Yes".

**Evidence.** `results/u13-bis-solo-silence-q27b/plain.md` line 1: "Qwen
27B answered 'Yes' after we removed one apology word, in one of twenty
runs that found an instrument fault." Correction and mechanism:
`plain/conclusions.md` lines 99–113, "What we got wrong" — "We reported
that Qwen 27B answered nothing at all, six times out of six... We were
wrong. All of it came from a bug." Corrected re-run:
`results/u13-redo-abl-real-q27b/plain.md` line 7: "We retract the old
three-part result." `README.md` lines 259–279 carry the original claims
still marked `[RETRACTED 2026-07-12 — truncation artifact]` in place.

**Best anchor.** `#essay` page, "What we got wrong" section (this is the
one retraction `plain/conclusions.md`'s own short version names — line 3:
"we retract one result"). Secondary: the record pages themselves
(`#u13-bis-solo-silence-q27b`, `#u13-redo-abl-real-q27b`), where the
correction sits in the plain summary, not a separate errata page.

**Priority.** High — this is the single cleanest, most concrete
retraction in the dump: a named bug, a named record, an admitted error,
and a corrected number, all still on the live page.

---

## 2. A genus of bugs the lab named and counted

**Draft body.** Eight times, this lab found that its own tool, not the
model, made an effect. It gave this pattern a name: the apparatus trap.
Before it reports a new effect, it now asks whether the tool caused it.

**Evidence.** `board/board.json`, item `apparatus-01` ("Trap-specimen
catalog"), notes dated 2026-07-14 through 2026-07-21 name specimens 5
through 8 explicitly ("EIGHTH specimen — cross-model embedding
scaling..."). `SURPRISES.md` line 89: "the apparatus-trap genus (now five
specimens)" lists the first five by name. `MENTIS_ISSUES.md` line 57
extends the same habit to a third-party tool the lab trialled.

**Best anchor.** No page currently renders this list (checked
`dashboard/app.js` and `index.html` nav — Findings map, Explorer, Essay,
Research board, Affect; no "Method" page). The tour step would have to
either quote it inline or link `#board` and name `apparatus-01` in the
list, since the board item itself has no dedicated anchor on the
rendered page (`probes/board.py` renders `BOARD.md` as plain text, not
per-item links).

**Priority.** High — this is the lab's most distinctive intellectual
habit per the brief, but it currently has no home on the site. This step
is a candidate reason to add a small "apparatus traps" list to the site
itself (out of scope for this candidates file).

---

## 3. Best specimen: a truncation bug that looked like a finding

**Draft body.** A tokenizer setting cut long prompts to 512 tokens. Every
run that used a long prompt went silent. Every run that used a short
prompt spoke. The lab mistook a software limit for a discovery about the
model.

**Evidence.** `plain/conclusions.md` lines 101–105: "the tokenizer
default... cut every second-turn prompt to 512 tokens... The confound was
exact." `results/u13-bis-loo-silence-q27b/thoughts.md` and sibling
`u13-bis-*` records hold the 20-run bisection that caught it.

**Best anchor.** Same as candidate 1 (`#essay`, "What we got wrong") —
this is the same event, told as method rather than as result. Could be a
distinct tour step if the tour separates "what happened" from "how we
caught it".

**Priority.** Medium — strong story, but overlaps candidate 1. Keep one,
not both, unless the tour wants a dedicated "how a bug gets caught" beat
before the "what we got wrong" beat.

---

## 4. Best specimen: junk words that were the ruler, not the reading

**Draft body.** For fifteen experiment units, this lab saw explicit
vocabulary appear in Qwen 27B's early layers, on every topic. Apparatus-9
found the cause: a fixed part of the model's own early state, always
present, that the lab's tool reads out. It does not change with the
question asked.

**Evidence.** `results/apparatus09-thoughts.md` lines 11–20: "H-standing
wins, cleanly, on both models... it is the transported image of a fixed,
input-independent component of the early residual stream." Lines 22–28:
"reading out μ alone at qwen L4 — no prompt anywhere in sight — returns
Blowjob, Geile, Shemale..." `plain/conclusions.md` lines 23–29 gives the
reader-facing version.

**Best anchor.** `#essay`, the "We reported a pattern that was not about
the input" section (`plain/conclusions.md` line 23). No dedicated record
page carries a `plain.md` for apparatus-09 (it is a decomposition run
under `results/apparatus09-{gemma-4b,qwen-27b}/report.json` with a single
shared `thoughts.md`, not a standard course record) — the tour would
point at the essay section, not a record card.

**Priority.** High — vivid, resolved, and a live example of
PLAIN-LANGUAGE.md §5.7's own warning (see "claims we should NOT make"
below): the correct statement is that the junk is *real* content the
lens reveals, not something the lens invented.

---

## 5. Every record ends with what it does not prove

**Draft body.** Every one of this lab's 499 result pages ends with the
same heading: "What this does not show." The lab writes it even when the
finding is strong.

**Evidence.** `PLAIN-LANGUAGE.md` line 149: "**What this does not
show.** One or two sentences. The limit of the claim." Lines 145–148:
"The last heading is the lab's honesty slot... always when the claim is
about absence." Verified count: all 499 `results/*/plain.md` files
contain the heading (`grep -c` returned 499 matches across 499 files).
Example: `results/u13-redo-abl-real-q27b/plain.md` line 9: "This run
does not show that the apology words have no other role. The lens shows
only words the model can say next."

**Best anchor.** Any record page, the bottom of the plain-language
summary above the "Research notes" fold. A general-audience example
works better than a technical one — e.g. the u13 retraction record
already used in candidate 1, or a plainer emotion-lens record.

**Priority.** High — this is the structural version of the honesty
practice: not a story about one mistake, but a heading that runs through
the whole site.

---

## 6. Every summary was checked against its source

**Draft body.** All 499 plain-language summaries went through an
accuracy check against their original records. Twenty checkers found 116
possible errors. A second, independent check confirmed 108 of them, and
the lab applied fixes for the confirmed findings.

**Evidence.** `plain/audit/audit-3-summary.md` lines 10–16: "20 Sonnet
auditors, 25 records each... 116 raw findings... 108 survived (26 high,
64 medium, 18 low), 8 refuted." Line 21: "9 Opus appliers... All edited
files pass `ste.py`."

**Best anchor.** No rendered page for this yet (same gap as candidate 2 —
checked `dashboard/app.js`, no reference to `audit-3-summary`). Tour step
would either summarize inline or link the raw markdown file directly.

**Priority.** High — the audit is the concrete backing for candidate 5's
"honesty slot" and candidate 9's "originals are preserved" claims; it
answers "how do you know the plain text is accurate," which a careful
visitor will ask.

---

## 7. The audit admits it did not catch everything

**Draft body.** An independent check by a different AI model found three
more errors in six records the first audit had already passed. None of
those three had turned up in the first audit's 116 findings.

**Evidence.** `plain/audit/audit-3-summary.md` lines 24–27: "GPT-5.6-Sol
(codex exec, read-only) audited 6 records independently: 3 clean, 3 with
real findings — and none of its 3 hits appeared anywhere in the Claude
sweep's 116 findings." "Honest residual" section, lines 47–52: "Sol's
3-in-6 hit rate on records the full sweep passed means recall is
imperfect in every pass, ours included... 'audited' never means
'error-free'."

**Best anchor.** Same gap as candidate 6 — pairs with it as the second
half of one tour step ("we checked everything, and we know the check is
not perfect") rather than a separate step.

**Priority.** High — this is the single best sentence in the whole
mining pass for "do not overclaim the honesty": the audit's own writers
say recall is imperfect. Use it verbatim or close to it.

---

## 8. The working notes are never rewritten

**Draft body.** Every record keeps two texts: the plain summary for
readers, and the lab's original notes underneath, unedited. The notes
stay exactly as first written, even where later work proved them wrong.

**Evidence.** `CLAUDE.md` (project instructions), "Conventions" section:
"`thoughts.md`... is never edited — it moves into the 'Research notes'
container on every page." `PLAIN-LANGUAGE.md` line 16: "Nothing is
deleted. The original text stays exactly as written and moves into a
Research notes container on the same page." `plain/audit/audit-3-summary.md`
line 22: appliers were "instructed to re-verify against sources before
editing and to leave originals (`thoughts.md`, the `t`/`b`/`name`/`desc`
fields) untouched."

**Best anchor.** Any record page, the "Research notes" container below
the plain summary (`dashboard/app.js` line 2900, `<span
class="notes-t">Research notes</span>`). Best paired with a record that
was later corrected, so the visitor sees the old wrong reasoning sitting
next to the current corrected summary — e.g. `#u13-bis-solo-silence-q27b`.

**Priority.** Medium-high — a strong practice, but it needs a retracted
or corrected record as its example to land; on a clean record it just
looks like "we show our work," which is less distinctive.

---

## 9. A research board that will not let a claim stand alone

**Draft body.** This lab keeps a public list of open questions. An item
can only be marked "landed" if the notes name the result and the record
that supports it. When a claim turns out wrong, the lab adds a dated
correction below the old note. It does not delete the old note.

**Evidence.** `CLAUDE.md`, "Research board" section: "Honesty rules: no
`landed` without a link to evidence... never rewrite old notes — append
a dated correction." Example of an appended correction:
`board/board.json`, item `span-02`, note dated 2026-07-18: "CORRECTION:
the decisive control... demoted this item's interpretation... the
premium tracks ELABORATION, not self-relevance." A second, larger
example: item `affect-07`, note dated 2026-07-24, a five-part correction
that starts "the 'H1' verdict is WITHDRAWN as over-compressed toward the
deflation, and rested partly on a broken null" and ends by naming the
exact bug (a lopsided random sample).

**Best anchor.** `#board` page. `BOARD.md` line 18 (span-02) and line 159
(affect-07) render these corrections inline, dated, under the original
note — nothing is hidden behind a second click.

**Priority.** High — affect-07 is the strongest single example in the
whole mining pass: the lab found a bug in its own statistical test,
named it precisely, and kept the wrong verdict visible next to the fix.

---

## 10. The board's evidence rule is convention, not code

**Draft body.** The lab says every landed item must link its evidence.
The tool that manages the board does not check this. What actually
enforces it is that landed notes name a result file by hand, every time.

**Evidence.** `probes/board.py` line 138 prints an item's `links` field
if present, but nothing in the script rejects a `state: landed` write
with an empty `links` array (checked the full `mv` code path). Of 23
`landed` board items, 20 carry no `links` entry at all (checked
programmatically) — only `span-01`, `span-02`, and `apparatus-01` have
one. Yet the notes still do the work by hand: 20 of the 23 landed notes
name a `results/...` path or report file inline (e.g. `apparatus-09`'s
landed note ends with the exact `report.json` reasoning). Two items fall
back on something thinner — `span-01`'s only evidence is a page link
(`#unit/15`, not a specific record), and `span-08` has neither a `links`
entry nor a path in its own note; its result lives in a later sibling
item's note (`span-09`).

**Best anchor.** No page surfaces this distinction (it requires reading
`board.json` and `board.py` together); this is background for whoever
writes the tour script, not a step on its own, unless the tour wants a
beat on "what's actually enforced vs. what's a habit."

**Priority.** Low as a standalone step — better folded into candidate 9
as one honest caveat ("the rule is followed by hand, not by the tool")
rather than given its own slide.

---

## 11. A preregistered prediction that came out wrong

**Draft body.** The lab wrote down a prediction before running the
experiment: a measured layer would fall in a specific range. The result
landed outside that range. The lab marked the prediction "FALSIFIED" on
the page where it was written down, not just in the result.

**Evidence.** `PREDICTIONS.md` lines 79–93 (P4): predicted range "L28–36";
resolution block, line 89: "Resolved 2026-07-21 evening — FALSIFIED
(second same-day loss)... width plateau (0.25) onset at L25, the
fraction-ported boundary." The ledger keeps the original prediction text
above the resolution, not replacing it.

**Best anchor.** No rendered page for `PREDICTIONS.md` itself (nav has no
"Predictions" entry). Could pair with `#essay`'s discussion of ignition
timing, or stay a background citation for the "preregistration" beat if
the tour covers it at all.

**Priority.** Medium — a clean preregistration-failure example, but it
requires explaining preregistration first, which costs tour budget the
other candidates don't. Use only if the tour has a step on method
discipline broader than error-correction.

---

## claims we should NOT make

- **"The lab always catches its own mistakes."** False as stated: the
  audit's own text says an independent checker found errors the lab's
  sweep missed (candidate 7). Say "checked," not "caught everything."
- **"The measuring tool invented the pornographic vocabulary."** This is
  the exact losing hypothesis PLAIN-LANGUAGE.md §5.7 flags by name
  (apparatus-09): the winning result is that the content is *real*, a
  fixed part of the model's own early state, which the lens then reads
  out in a distorted way. Getting this backwards is not a simplification,
  it is the wrong finding.
- **"Every open item on the board has evidence linked."** Not literally
  true — see candidate 10: the `links` field is empty on 20 of 23 landed
  items, and the enforcement is a writing habit, not a check the software
  performs. Fine to say "the convention is to name the record," not fine
  to say "the system requires it."
- **"This lab retracts things often."** It retracted one result
  (`plain/conclusions.md` line 3 says so itself: "we retract one
  result"). The eight apparatus-trap specimens are mostly caught
  *before* publication, which is a different and arguably better
  practice than retraction — don't conflate the two counts.
- **"The plain-language layer is proven accurate."** The checker
  (`probes/ste.py`) only enforces form — sentence length, banned words,
  quote fidelity — not truth. `PLAIN-LANGUAGE.md`'s own text says the
  checker "cannot tell whether the plain text matches the original."
  Accuracy is a human/audit practice, not a guarantee.
- **"Mnestis's issues prove the lab distrusts AI tools generally."**
  `MENTIS_ISSUES.md` is about one specific tool's specific bugs, found
  through direct use, not a general position — don't generalize it into
  a broader claim the source doesn't make.
