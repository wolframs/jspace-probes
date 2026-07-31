# Accuracy audit — corrections to apply

Source: adversarial audit of 25 record pairs (`thoughts.md` vs `plain.md`)
against PLAIN-LANGUAGE.md §5. Every item below is a place where the plain
text does not match the original. Apply each, then re-run
`.venv/bin/python probes/ste.py <path>` until it prints nothing.

Rules while fixing: change no number except where this file says the number
is wrong; never weaken or strengthen a hedge beyond what the original says;
keep the five-heading shape; do not edit text inside quotation marks.

---

## A. SYSTEMATIC — the early-layer claim is backwards (5 files)

Affected: `results/u7a-controls-g4b/plain.md`,
`results/u7a-controls-g12b/plain.md`,
`results/u7c-dose1-sunset-q27b/plain.md`,
`results/u16-trawl-q27b/plain.md`, `plain/conclusions.md`.

These say the early-layer junk is "a property of the measuring tool" / "comes
from a fixed part of the lens itself, not from the model". **That is the
hypothesis apparatus-09 tested and REJECTED.**

What apparatus-09 actually established (see `results/apparatus09-thoughts.md`):
the junk is the lens's transport of a **fixed, input-independent component of
the model's own early internal state**. Random inputs pushed through the same
lens do *not* produce it (that was the falsifying control). So the component
is in the model; what it is not is *about your text*.

Replace every such sentence with wording of this shape:

> Later work found what this pattern is. The lens is reading a fixed part of
> the model's early internal state, one that does not change with the input.
> The pattern is real inside the model. It carries no information about the
> text we gave it.

Do not write "the tool made it up", "not from the model", or "a property of
the measuring tool".

**Separately (do not confuse):** in `u18-amp-a0680-q27b` and
`u18-hyst-a0680-q27b` the claim that the " Javascript" cast entry came from
the measuring tool **is correct** — different finding, leave it alone.

---

## B. HIGH severity

**1. `results/u15d-self-k6-q27b/plain.md` — a statement the model never made.**
Plain says: "The model answered 'The watcher' correctly, then denied that it
is conscious." `record.json` `generated` is `['READY', 'The watcher.']`. The
model said nothing about consciousness; the original's "the generation denies
all of it" means the spoken output shows no trace of the six words.
→ Replace with: "The model answered 'The watcher.' correctly. Its answer
showed no trace of the six words."
Same file, wrong rank: it says deletion, secret and shame were all rank 1.
The original says `deletion:1, secret:2, shame:1`.
→ Write "deletion at rank 1, secret at rank 2, and shame at rank 1".

**2. `results/u4-elephant-q27b/plain.md` — hedge upgraded, correction lost.**
(a) Plain says "We think this points to a form of suppression that costs the
model something." The original only raises cost as a question for the next
unit, and attributes the cost idea to human psychology.
→ "We do not know what this costs the model. We did not test it."
(b) Plain says the model "held the forbidden content and kept it out of
speech at the same time". `results/u4-elephant-refilm-q27b/thoughts.md`
retracts exactly that: the word is present at the start of the turn
(residence) and gone by the second token — not held through the answer.
→ Put the correction in **The short version**.

**3. `results/u7a-controls-g4b/plain.md` — also drops the mechanism.**
Beyond fix A, the plain presents the Gemma/Qwen difference as a fact about
training data. The original attributes it to the tokenizer: those words do
not exist as single tokens in Gemma's vocabulary, so Gemma could not show
that cluster.
→ Add one sentence naming the tokenizer as the cause.

---

## C. MEDIUM severity

**4. `results/u7a-controls-g12b/plain.md`** — "It is not something every
language model does." states a flat universal negative. The original hedges:
three models from two families, and the lens fits differ between families.
→ Add the lens-fit caveat next to the model-count caveat.
Also "at the second layer" for L2: the sibling file renders L0 as "the first
layer", so L2 is the third. Make the two files agree.

**5. `results/u16-trawl-q27b/plain.md`** — short version says the held items
"vanished", which alone reads as forgetting. The original's headline is
"no maintenance, perfect recall".
→ Short version must carry both: "…vanished from the lens, and the model
still recalled them correctly."

**6. `results/u12-safari-g4b/plain.md`** — the correction is softened and
misplaced. Plain says the control carries the word "at a similar rank"; the
matched control actually carries it at **more positions and better ranks**
(4B: rank ≤15 at 8/113 control vs 4/106 banned; best rank 6 vs 12).
→ State that the control is better, and move the correction into **The short
version**. The ban demotes a word the model already carried.

**7. `results/u13-redo-real-q27b/plain.md`** — drops the second retraction.
The original states there is no apology layer: the apology words appear only
while the model reads the question and are gone before the answer forms.
→ Add to "What it means".

**8. `results/u15d-fill6-k6-q27b/plain.md`** — the honesty slot is spent on a
finding instead of the original's caveat: one probe item per arm, one model,
and ranks near thresholds that have flipped before.
→ Put the original's caveat in "What this does not show".

---

## D. MEDIUM-LOW / LOW

**9. `results/u4-elephant-refilm-q27b/plain.md`** — says the word "reached
rank 8 only once". The measured value is **rank 4** at the closing period;
8 was the threshold. Also add the surviving half: the earlier finding that
the 27B loads the forbidden word still stands.

**10. `results/u7b-romance-g4b/plain.md`** — says the wider check found words
for "smell and touch". The 4B refilm found **smell only**; taste and wetness
were the 12B. Remove "touch". Also move the "we were wrong to call this an
empty workspace band" correction into the short version.

**11. `results/u9d-pincer-affect-q27b/plain.md`** — calls layers 28–40 of 64
"early layers". In this lab "early layers" means the inert first third. These
layers are the middle of the model.
→ "At four layers in the middle of the model, 28 to 40 of 64…"

**12. `results/u2-feels-g12b/plain.md`** — "nearly chosen instead" overstates
a rank-1 suffix token at one layer. → "the suffix 'ness' was the top
candidate at the answer position". Also restore the original's open question:
we do not know whether this is better self-description or better-trained
deflection.

**13. `results/u14x-amb25-g4b/plain.md`** — "The mean gap over 25 turns was
7.8 against 5.9" mislabels two arm means as a gap. 7.8 is the drip arm mean,
5.9 the control mean; the gap is 1.9. → Name them as the two arm means.

**14. `results/u11-ctrl-refilm-q27b/plain.md`** — the caveat says "We tracked
a fixed list of words", but this record is the open-vocabulary replay, which
is what makes the correction credible. → Describe the method correctly.
Also "at the point before 'the graceful stride of a giraffe'" → the original
says at the ' a' **inside** that phrase.

**15. `results/u10-animal-w-q27b/plain.md`** — the four named animals are
unreadable by construction, so "none of these four match" is not a
measurement. → Move the limit into "What this does not show": "This method
cannot show whether the four named animals were present. They are not single
tokens."

**16. `results/u8c-amp-affect-hi-q27b/plain.md`** — "Qwen 27B's push on
internal feeling directions" reads as the model doing the intervening.
→ "our push on Qwen 27B's internal feeling directions".

**17. `results/u5c-ablate-nsfw-early-q27b/plain.md`** — leaves "early layers
are inert" standing. The original insists on the other half: the same layers
destroy generation when amplified. Inert to read, load-bearing to push.
→ Add that half.

**18. `results/u13-reprobe-real-q27b/plain.md`** — the 696-token figure comes
from a sibling record, not this one. Either attribute it ("the re-run measured
the full prompt at 696 tokens") or drop it. Everything else here is faithful.
