# Extended guided tour — candidates: the method

Mining pass for the "how do I read this site" leg of the extended tour.
13 candidates. Plain-language drafts follow PLAIN-LANGUAGE.md (§3.1
uncertainty ladder, §5 accuracy rules, vocabulary from `plain/terms.json`).
Every number below is copied from a source file or a record, not invented.

---

## 1. What the lens is

**Draft body.** The lens is our measuring tool. At one layer inside a
model, it shows which words the model is most ready to say next, ranked
from likely to unlikely. We built it from a published method, applied to
three models on one home graphics card.

**Source.** `README.md:3-7` ("run through the Jacobian lens... on one
RTX 3090"); `MECHANICS.md` §1 (`lens_l(h) = softmax(W_U · norm(J_l h))`,
"the rows of `W_U J_ℓ` as the Jacobian lens (J-lens) vectors"); `plain/terms.json`
term `lens` ("Our measuring tool. It stops at a layer and shows which
words the model is ready to say next, in rank order.").

**Best anchor.** The masthead sparkline (`#mast-spark-link`, a live core
sample of `u2-feels-q27b`) on any route, or the term popover on the word
"lens" the first time it appears on a record page.

**Priority.** High — every other step assumes the reader knows this.

---

## 2. Reading rank

**Draft body.** Rank is a word's place in the lens list. Rank 1 is the
word the model is most ready to say, out of about 250,000 words.

**Source.** `plain/terms.json` term `rank` ("The position of a word in
the lens list. Rank 1 is the word the model is most ready to say, out of
about 250,000."); `dashboard/app.js:2408-2415` (`renderReadout`, the
per-layer top-k table a record page shows).

**Best anchor.** The "Readout by layer" table on any record page
(`#<record-id>`, section built by `readoutHTML`/`renderReadout`), or the
"rank" term popover.

**Priority.** Medium — quick and load-bearing, but short enough to fold
into step 1 or 3 if the tour needs to shrink.

---

## 3. How to read a core sample

**Draft body.** Every record shows a core sample: one colored band for
each layer, first layer at the top, last layer at the bottom. A deeper
blue means the model's actual next word ranked closer to rank 1 at that
layer.

**Source.** Verbatim from the record head's own caption,
`dashboard/app.js:1571-1575`: "Core sample, top→bottom = layer 0→N-1:
depth of blue = how close `<token>` (the model's actual next token at
position P) is to rank 1 in the lens readout." Glyph construction:
`dashboard/app.js:412-423` (`function glyph`, log-rank color mapping,
5 shade steps).

**Best anchor.** The large core sample glyph (`.glyph-lg`) at the top of
any record page (route `#<record-id>`), left of the title.

**Priority.** High — this strip appears on nearly every page (masthead,
rail rows, findings cards, record heads); reading it once unlocks all of
them.

---

## 4. The same strip is a clickable thumbnail

**Draft body.** The small core samples in lists are links. Click one to
open the full record behind it.

**Source.** `dashboard/app.js:425-429` (`rowHTML`, glyph wrapped in
`<a class="exp-link" href="#<id>">` in the rail); `dashboard/app.js:2483`
(findings-map cards, glyph title reads "this finding's core sample; open
the record"); comment at `dashboard/app.js:3162-3164` notes the glyph
inside a findings card is a ~10px sliver, too small to outline on its
own, so the tour should highlight the whole card or row instead of the
glyph pixel-strip.

**Best anchor.** A row in the left rail (`#rail-list`, any route) or a
card on the findings map (`#findings`).

**Priority.** Medium — a UI-mechanics note, useful but not conceptual.

---

## 5. The workspace band

**Draft body.** The workspace band is the middle part of a model, about
38 to 92 percent of its depth. The published paper reports that changes
made inside this band can change the model's answer. Changes made before
it usually cannot.

**Source.** `MECHANICS.md` §2, quoting the paper: "the workspace is the
region 'beginning about a third of the way through (~L38) and ending
shortly before the output (~L92)'"; `GLOSSARY.md` "Workspace band" entry;
`plain/terms.json` term `workspace-band` ("about 38 to 92 percent of the
way through... Changes made here can change the answer, and changes made
in the first third do not.").

**Best anchor.** The term popover for "workspace band", first use on a
steering-related record (e.g. `#u5c-ablate-nsfw-early-q27b` or any Unit
6 record), or the glossary entry at `../glossary.html#t-workspace-band`.

**Priority.** High — the load-bearing structural fact behind every
steering and ablation result on the site.

---

## 6. Early layers look inert, but only to one kind of push

**Draft body.** We once removed five word-directions from Qwen 27B's
early layers, and its top prediction barely moved. Those layers sit
before the workspace band. A later test pushed the same layers harder
instead of removing directions, and it broke the model's text at once.

**Source.** `results/u5c-ablate-nsfw-early-q27b/plain.md` ("we removed
five adult-content directions from Qwen 27B's early layers, and its top
prediction for a currency question barely moved... These layers are
inert to read, but they are not passive. A push at the same layers
destroys the model's text at once."); `results/u5c-amp-typo-early-q27b/plain.md`
("We pushed a slang-word direction hard into Qwen 27B's early layers...
and the answer broke apart"); `MECHANICS.md` opening correction note
("Unit 5C ablated the NSFW cluster at L2-8... found nothing — because
causal interventions only bite in the WORKSPACE band").

**Best anchor.** The plain block (`section.card.plain`) of
`#u5c-ablate-nsfw-early-q27b`, paired with its sibling
`#u5c-amp-typo-early-q27b`.

**Priority.** High — this is the lab's own founding mistake, corrected
in public; it teaches "distinguish measured from assumed" by example.

---

## 7. Start depth (ignition): measured, not assumed

**Draft body.** Start depth is the point where the workspace begins to
work. The published paper gives one number as a fraction of depth. We
measured our own three models directly, and each one starts later than
that fraction.

**Source.** `plain/terms.json` term `ignition` ("The signs the lens can
read start later, at 44 to 74 percent of depth in three models.");
`results/u16-trawl-q27b/plain.md` ("We measured the start depth at
layers 28 to 36, or 44 to 56 percent of depth."); `results/u16-trawl-g4b/plain.md`
("The start depth was layers 16 to 22, which is 48 to 67 percent of
depth, later than the ported layer 13. All three models start their
workspace later than the value we ported from the paper."); `MECHANICS.md`
§2 measured note dated 2026-07-17.

**Best anchor.** The plain block of `#u16-trawl-q27b` or
`#u16-trawl-g4b`; term popover for "start depth" (`data-term="ignition"`).

**Priority.** High — directly answers the question a careful reader will
ask ("is 38% a fact about this model, or a number from the paper?").

---

## 8. What a record contains

**Draft body.** Each record holds the exact conversation we gave a
model, what it generated, and a measurement at every layer and word
position we tracked. It also holds a plain-language summary and our
original working notes, unedited.

**Source.** `README.md` "What's in the dump" list (`record.json`,
`thoughts.md`, `plain.md`); record.json top-level keys observed in
`results/u0-boot-q27b/record.json` (`id, title, unit, created, model,
lens, params, conversation, generated, tokens, readouts, trajectories,
emergence, scan, slice`); render order in `dashboard/app.js:1464-1480`
(head → plain summary → conversation → film/affect → Research notes
fold).

**Best anchor.** A full record page top-to-bottom, e.g. `#u0-boot-q27b`
(a short, single-turn record good for a first look).

**Priority.** High — this is the page structure every later step
assumes the reader can navigate.

---

## 9. The plain summary and the "Research notes" fold

**Draft body.** Every record leads with a short plain-language summary.
The lab's own working notes, the raw parameters, and the full per-layer
table sit below, folded under "Research notes." Nothing is deleted or
rewritten; the plain summary is added on top.

**Source.** `PLAIN-LANGUAGE.md` "Nothing is deleted" (§ intro) and the
30-second rule; `dashboard/app.js:2882-2896` (`plainHTML`, `notesWrap` —
"original commentary, parameters, per-layer readouts and scans — written
by the model that ran the experiment").

**Best anchor.** The `<details class="notes">` element on any record
page, labeled "Research notes."

**Priority.** Medium — explains a UI convention the reader will meet
immediately but can infer without a dedicated step.

---

## 10. A quoted word is never rewritten

**Draft body.** When a summary quotes a word the model actually
produced, the quote keeps the model's exact spelling and punctuation.
Everywhere else, the summary is written in plain language.

**Source.** `PLAIN-LANGUAGE.md` §3.3 ("Model output is data. It keeps
its original spelling, spacing, and punctuation, inside quotation
marks... Sentence punctuation belongs outside the closing quote.");
rendered example at `dashboard/app.js:1573` — `<code class="tok">` around
the model's actual next token in every record head caption.

**Best anchor.** The monospace token inside the record head caption
(the `<code class="tok">` element), any record page.

**Priority.** Medium — a small but distinctive discipline point; good
as a closing aside rather than a headline step.

---

## 11. The uncertainty ladder

**Draft body.** This site's plain-language pages use seven fixed
phrases for confidence, from "We measured X" down to "We do not know."
Each phrase means one exact thing, everywhere it appears.

**Source.** `PLAIN-LANGUAGE.md` §3.1, the closed table: "We measured X" /
"The data shows X" / "We think X" / "X is possible. We did not test it."
/ "We do not know." / "This method cannot show X." / "We were wrong. The
correct result is X."

**Best anchor.** The "What this does not show" line inside any plain
block — a fixed heading present on nearly every `plain.md`, and usually
where a ladder phrase appears. No dedicated on-site glossary page for
this table exists yet; the tour card itself is likely the only place a
reader will see the full ladder spelled out.

**Priority.** High — explicitly named as unusual and worth a step; once
known, it lets a reader calibrate every hedge on the site without
re-asking "how sure are they?" each time.

---

## 12. Small models, home hardware — read the scale honestly

**Draft body.** We run three models on one home graphics card, not the
much larger models in the published paper. Our results usually match a
control described in the paper's appendix, not its main findings.

**Source.** `README.md:3-6` ("on one RTX 3090"); `PREDICTIONS.md`
"Standing design rules" #3 ("Appendices first... our regime (small
models, passive items, single readouts) usually matches an appendix
control instead"); `MECHANICS.md` §4 Haiku-scale caveat ("Qwen-27B is
small — we may hit coherence-break before register-flattening");
`plain/terms.json` term `quantization` ("We store the model with less
precision so that it fits on one graphics card. This can change
measurements.").

**Best anchor.** The model chips row in any record head (`.chip.model`,
`.chip` for `hf_id` and quantization, e.g. "pre-4bit", "8-bit", "bf16").

**Priority.** High — the single biggest source of a reader over-trusting
a small-model number as if it were the paper's headline result.

---

## 13. Where this lab's measurements disagree with the paper

**Draft body.** The published paper predicts that one measure, called
effective dimensionality, rises near the end of a model. In our own
measurements, on two different models, it falls instead after an
earlier peak. We do not know yet if this comes from the models or from
how we built our lens.

**Source.** `PREDICTIONS.md` P11 ("The paper predicts effective
dimensionality *rises* into the motor band... Our qwen NF4 curve falls
L58→L62... the bf16 gemma-4b curve... also falls after its ~85% peak...
Until then, do not cite the paper's motor-band effdim rise as if it held
for our stack."); `MECHANICS.md` §2 ("Tension kept honest: the paper's
effective dimensionality *rises* into the motor band, ours falls
L58→L62 — unresolved"); `README.md` "Theory day" section, same claim.

**Best anchor.** Not yet rendered anywhere on the site as reader-facing
text — no `plain.md` currently states this finding. The nearest existing
anchors are the plain blocks of `#u16-trawl-q27b` / `#u16-trawl-g4b`
(they measure the same curves but their plain text stops short of
naming the paper disagreement) or a new line in `#essay`. Flag this gap
explicitly if the step is built before a plain-language writeup exists
for it.

**Priority.** High — directly answers the brief's Q7, and it is the
single clearest, most honestly-hedged case of "measured here, paper says
otherwise" on file.

---

## The one concept that unlocks the rest

If a visitor learns only one thing, make it **step 3 — the core sample.**
The same blue-depth-by-layer strip is the masthead, every rail row,
every findings card, and every record head; a reader who can decode one
can decode all of them without re-explanation. The second-most-leveraged
idea is step 12 (small models, appendix not headline) — it is the
correction most likely to stop a reader from mis-citing this site.
