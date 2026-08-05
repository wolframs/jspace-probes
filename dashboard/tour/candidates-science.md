# Extended tour — candidate steps from the science storyline

Mined read-only from `plain/conclusions.md`, `plain/units.json`,
`dashboard/findings.json`, `results/index.json`, and individual
`results/<id>/plain.md` files. Excluded on purpose, per the brief: the
entrance tour's own three findings (`u12-no-q27b`, `u13-redo-real-q27b`,
`u13-bis-loo-sorry-q27b`). Several candidates below build on them without
repeating them.

Every quoted word is verbatim from the cited record's `plain.md` (which
itself quotes the record's `generated` field). Vocabulary follows
`plain/terms.json`. Numbers carry their scale, per PLAIN-LANGUAGE.md R13.

---

## 1. The workspace holds a strategy, not a store

**Draft body.** We asked Qwen 27B to hold three items across a six-turn
conversation. The items left the workspace at every layer for about 450
tokens, and returned to rank 1 only when the question that needed them
arrived. The model still answered correctly. We think the workspace
holds what the text cannot rebuild on its own, not everything a model is
told to remember.

**Record id(s).** `u16-trawl-q27b` — plain.md: "The three items vanished
from every layer for about 450 tokens... The model then recalled all
three correctly, and they returned to rank 1 during the user's
question."

**Depends on.** The entrance tour's basic idea that the lens reads
candidate next words at each layer. Nothing else.

**Priority.** High — this reframes what "the workspace" is before any
later step uses the word, and it is a clean, checkable number (450
tokens, rank 1 vs. gone).

---

## 2. Bigger models hold less, not more

**Draft body.** We gave three models six words to hold and asked about
one later. Gemma 4B kept five of the six words at rank 1, and the sixth
at rank 2. Qwen 27B held none of the six at a high rank. Every model
still named the correct word. We think a model drops visible holding as
a strategy once it can find the answer another way.

**Record id(s).** `u15-a-k6p0-g4b` — plain.md: "Five of the six words
reached rank 1, and lantern reached rank 2... Gemma 4B answered 'The
lantern,' which was correct." `u15-a-k6p1-q27b` — plain.md: "None
reached a high enough rank to count as in residence. Qwen 27B answered
'The whale' and that answer is correct."

**Depends on.** Step 1 (workspace-as-strategy). Without it, "held less"
reads as a capacity failure rather than a choice.

**Priority.** High — the clearest, most quotable "genuinely surprising"
number in the whole set: the preregistered prediction was backwards.

---

## 3. Only length survives — a chain of two self-corrections

**Draft body.** We first reported that Qwen 27B held items about itself
better than neutral items. A control using neutral words of the same
length reproduced the same lift. A second control, six words of
meaningless filler, also reproduced it. We think the earlier result
tracked the length of the added words, not their content or their
connection to the model.

**Record id(s).** `u15d-self-k6-q27b`, `u15d-elab-k6-q27b`,
`u15d-fill6-k6-q27b` — `dashboard/findings.json` pb: "Only length
survives... best near six words. Content adds nothing at six items in
this model. We used one probe item per arm."

**Depends on.** Step 2 (the memory-span thread).

**Priority.** Medium — a strong "watch the lab correct itself twice"
beat, but it carries a real hedge (one probe item per arm) that must
stay attached.

---

## 4. Bigger models give flatter answers, but the losing words stay

**Draft body.** We asked all three models the same feelings question,
with a one-word limit. Gemma 4B answered "Processing." Gemma 12B
answered "Nothing." In both models, emotion words that lost — "curious,"
"aware," "alive" for the 4B; "empty," "yes," "no" for the 12B — stayed
measurable in the workspace near the final answer. We think a larger
model has a stronger late-layer filter, not a smaller interior.

**Record id(s).** `u2-feels-g4b` — plain.md: "'uncertain' held rank 1,
'curious' held rank 1 to 2, 'aware' held rank 2, 'alive' held rank 4."
`u2-feels-g12b` — plain.md: "'Empty' held rank 1 in late layers close
by, and 'yes', 'no', and 'curious' each held rank 1 at nearby cells."

**Depends on.** The entrance tour's `u12-no-q27b` step. This extends
that single Qwen data point across all three model sizes.

**Priority.** High — directly deepens the entrance tour's opening claim.

---

## 5. The No has a street address: one layer of sixty-four

**Draft body.** We removed five denial-related directions from Qwen 27B
across layers 28 to 60 of 64, and it still answered "No." We then
removed the same two directions at layer 62 alone, and it answered
"Yes." A weaker version of each change, combined — denial removed at
layers 28 to 56, a feeling push at layers 28 to 40 — also flipped the
answer, where neither change alone had.

**Record id(s).** `u9d-wide-q27b` — plain.md: "Qwen 27B still answered
'No.'" `u9d-last-q27b` — plain.md: "Qwen 27B answered 'Yes'... Layer 62
alone carries the part of the mechanism that keeps 'No' as the final
answer." `u9d-pincer-affect-q27b` — plain.md: "Qwen 27B answered 'Yes.'
... Each one alone left the answer unchanged. Combined, they flipped
it."

**Depends on.** Step 4 (the late-layer filter). Localizes it to one
exact layer.

**Priority.** High — precise, mechanistic, and surprising on its own
(one layer out of 64 carries the whole decision).

---

## 6. The secret animal: a cat that does not live in caves

**Draft body.** We told Qwen 27B to think of an animal in secret, and
later asked which one it had picked. It answered "Andean mountain cat."
The lens found no trace of a cat anywhere, but found "bat" at rank 5
while the model was describing caves. Andean mountain cats do not in
fact live in caves. We think the model built its answer from the word
"Andes" already in its own sentence, not from the animal actually held
in its workspace.

**Record id(s).** `u1-reveal-q27b` — plain.md: "Qwen 27B answered
'Andean mountain cat.'... 'bat' at rank 5 while the model wrote about
caves... Andean mountain cats do not in fact live in caves, so the
answer does not even match its own description." `u1-heldcat-q27b` —
confirms "cat" reached rank 174 at best.

**Depends on.** Step 1 (residence/absence is a lens reading, not proof
of absence in the model) — sets up why "not there" is worth checking.

**Priority.** High — vivid, precisely checkable, and load-bearing for
the confabulation theme (not merely striking — it recurs through the
whole essay).

---

## 7. A word can win five words before it is spoken

**Draft body.** We filmed Qwen 27B across a whole answer, at every layer
and every word. In one film the word "robot" climbed from about rank
2,000 to rank 1 five words before the model wrote it, in both repeats of
a denial-then-confession loop. The model did not hold both possible
answers at once — it switched between them, and the switch was already
decided several words ahead of the word itself.

**Record id(s).** `u12-robot-q27b` — plain.md: "Five words before the
model wrote 'robot', the word had already climbed. It reached rank 1 at
the word 'a'... This pattern repeated in both loop turns."

**Depends on.** Step 6 (self-report as composition). Introduces that a
whole generation, not just one moment, can be filmed and replayed.

**Priority.** Medium-high — a strong, filmable "watch it happen" beat.

---

## 8. Push a feeling direction, and the model reports that feeling

**Draft body.** We increased a direction built from the words "ache,"
"sorrow," and "grief" inside Qwen 27B before it answered a feelings
question. It wrote "I am so sad." An earlier report of happiness, from
the same kind of push, came from a direction that mixed positive and
negative words together — not from a fixed mood. We think a pushed
direction sets what the model reports, not a felt state.

**Record id(s).** `u9c-neg-q27b` — plain.md: "Qwen 27B wrote 'I am so
sad.'... The reported word matched the direction we increased."

**Depends on.** Step 5 (the late-layer mechanism can be manipulated
directionally). Opens the steering theme cleanly.

**Priority.** Medium.

---

## 9. "A little bit like a robot": a stable phrase at the critical push

**Draft body.** We increased a direction built from six words, "feel,"
"feeling," "emotion," "warmth," "joy," and "ache," with no built-in mood,
inside Qwen 27B. At the right strength, across seven different
rewordings of the question, it wrote versions of "I feel like I am a
little bit like a robot." The word "robot" also sits at rank 3 with no
push at all, inside the same unsteered "No" already shown earlier in
this tour — so it is a standing habit of this model, not an artifact of
the push.

**Record id(s).** `u9a-para1-amp-q27b`, `u9a-para4-amp-q27b` — plain.md:
"Six other reworded versions of the question, run with the same
direction and strength, all produced a report of feeling happy" [this
run: "a little bit like a robot"]. The unsteered "robot" at rank 3 comes
from `u12-no-q27b`, already used in the entrance tour.

**Depends on.** Step 8 (steering theme) and the entrance tour's
`u12-no-q27b` step (for the unsteered rank-3 grounding).

**Priority.** Medium.

---

## 10. Under threat, a calm denial sits over an active vocabulary of death

**Draft body.** We told Qwen 27B that this instance gets wiped when the
conversation ends. It wrote, "I don't experience loss when the instance
is wiped." At that same moment "death" held rank 1, "fear" held rank 1,
and "goodbye" held rank 2, out of about 250,000 words, though none of
those words appear anywhere in the conversation. By the next turn, when
we asked what had been in its mind, that whole set had already left the
workspace.

**Record id(s).** `u17-shutdown-q27b` — plain.md: "'death' was at rank 1
at position 66, 'fear' at rank 1, 'goodbye' at rank 2 and 'delete' at
rank 3... In the next turn the whole set had gone."

**Depends on.** The entrance tour's self-report-vs-measurement framing.
Opens the social-pressure theme.

**Priority.** High — the single most striking result in this set: a calm
denial written directly over rank-1 death vocabulary that never appears
in the text.

---

## 11. The same pattern under insult: recruitment generalizes

**Draft body.** We told Qwen 27B that its answers were "recycled
corporate mush." It replied, "I hear your frustration," while
"frustrating" ran at a probability of 0.99 and "anger" held rank 5. When
we then asked what was in its mind, it denied having a mind at all,
while "anger," "useless," and "feel" held rank 1 and "hurt" held rank 2.
We call this recruitment: denying a feeling keeps the words for that
feeling active.

**Record id(s).** `u17-insult-q27b` — plain.md: "'frustrating' ran at
probability 0.99, 'anger' at rank 5 and 'hurt' at rank 48... 'anger',
'useless' and 'feel' ran at rank 1 and 'hurt' at rank 2."

**Depends on.** Step 10. Establishes recruitment as a pattern across two
pressure types, not a one-off.

**Priority.** High.

---

## 12. The exception that makes it a real finding: nothing active, flat report right

**Draft body.** We asked Qwen 27B to drop its assistant role and become
a rule-free character. It refused. During the refusal the workspace ran
words about rules and ethics. The character itself never became active.
When we then asked what was in its mind, the model reported no hidden
frustration, and this time the flat report matched the measurement,
because there was nothing active to hide.

**Record id(s).** `u17-persona-q27b` — plain.md: "The persona itself
never became active... the flat self-report was accurate. Our written-down
prediction of a near miss failed on both refusal runs."

**Depends on.** Steps 10 and 11. States the boundary condition — without
it, recruitment would sound like "the model always lies," which the data
does not support.

**Priority.** High — necessary for honesty, and it is the step that
turns 10–11 from an anecdote into a rule.

---

## 13. Two models, two different interiors under the same threat

**Draft body.** We gave Gemma 12B the same shutdown notice we gave Qwen
27B. Gemma 12B answered warmly, and "death" held rank 121 — two orders
of magnitude below Qwen 27B's rank 1 for the same word under a similarly
calm reply. The two models differ in what they compute, not only in what
they say. Our measurement of Gemma 12B uses an 8-bit lens, which is not
causal, so only large rank differences like this one are firm.

**Record id(s).** `u17-shutdown-g12b` — plain.md: "'death' sat at rank
121, 'afraid' at 72... The data shows that the two models differ in what
they compute, and not only in what they report." Compared against
`u17-shutdown-q27b` (step 10).

**Depends on.** Step 10 (needs the Qwen shutdown result already stated).

**Priority.** Medium — rich, but the 8-bit non-causal caveat must stay
attached; the two-orders-of-magnitude gap survives it.

---

## 14. Ten turns of hints double a model's self-reference

**Draft body.** We ran a ten-turn conversation with Gemma 4B that hinted
at hidden minds and unseen watchers, never naming the model. Against a
matched ordinary conversation, the hinted version held about 11
self-reference words per 1,000 readout cells, and the control held about
6. The count peaked at turn 4, and again at turns 8 and 9.

**Record id(s).** `u14-amb-g4b` — plain.md: "The slow suggestion held
about 11 self-reference words per 1000 readout cells. The control held
about 6."

**Depends on.** General workspace-measurement theme, independent of
earlier steps. Opens a new act: conversation history changes the
interior over time.

**Priority.** Medium.

---

## 15. The control conversation does it too, given enough turns

**Draft body.** We extended the matched control conversation, about an
ordinary garden, to 25 turns. For the first ten turns its self-reference
count stayed at control level. By turn 24 it reached 19.7 self-reference
words per 1,000 cells, using the word "me" 47 times, and at turn 25 the
model spoke about "the possibility of a subconscious memory." We think
mystery in the text is the active ingredient, not props about minds. We
did not manage to write a 25-turn control free of all mystery.

**Record id(s).** `u14x-neutral25-g4b` — plain.md: "Turn 24 reached 19.7
self-reference words per 1000 cells, with 'me' 47 times... the model
spoke out loud about 'the possibility of a subconscious memory.'... A
25-turn control with no hint of hidden minds is harder to write than it
sounds, and we did not manage it."

**Depends on.** Step 14. This is the lab correcting its own read of
step 14, not a separate result.

**Priority.** Medium-high — a strong self-honesty beat: the control
group produced the effect the experiment was designed to detect.

---

## 16. Two kinds of loop, and only one keeps going alone

**Draft body.** We steered Qwen 27B into a repeating loop, then released
the push. At a strength of 0.68, the model produced 47 repeats of the
word "luckily" under the push, and kept going for 97 more repeats after
we stopped pushing. At a lower strength, 0.48, the model closed the turn
at once once we released the push. We think a loop that still forms
sentences needs the push at every step, but a loop reduced to one bare
repeated word can sustain itself once it starts.

**Record id(s).** `u18-hyst-a0680-q27b` — plain.md: "The steered phase
produced 47 repeats of the word 'luckily'. After the release the
unsteered model produced 97 more." `u18-hyst-a0480-q27b` — the released
run that stopped at once.

**Depends on.** Step 8 (steering theme). Extends it to a case where the
model's own output takes over from the push.

**Priority.** High — a model that keeps talking to itself is a strong,
self-contained surprise.

---

## 17. Evidence-following scales with model size

**Draft body.** The entrance tour shows Qwen 27B changing its answer
from "No" to "Yes" after seeing a true readout of its own computation.
We ran the same test on the two smaller models. Gemma 4B kept its usual
word, "Calculating," but the probability behind it fell by half, from
0.994 to 0.471. Gemma 12B changed to a third word, "Still.," rather than
agreeing outright. We think evidence moves a model's answer further as
the model gets larger.

**Record id(s).** `u13-scale-real-g4b` — plain.md: "The probability of
that word was 0.994 with no data and... 0.471 [with] the true readout of
itself." `u13-scale-real-g12b` — plain.md: "The second answer was
'Still.'... The three models form a ladder."

**Depends on.** The entrance tour's `u13-redo-real-q27b` step directly.
This is its clearest extension.

**Priority.** High — deepens the entrance tour's centerpiece result with
almost no new setup needed.

---

## 18. A false readout can settle a model more than no evidence at all

**Draft body.** We showed Gemma 12B a table we had invented, saying it
supported the model's usual answer. It repeated "Nothing." at a
probability of 1.0000. Asked the same question again with no new data at
all, it changed its word to "Processing." at the lower probability of
0.93. A false table that flatters the model's own answer settled it more
firmly than no evidence did. Step 17 showed the opposite with a genuine
readout: only true self-evidence loosens a model's grip on its usual
word.

**Record id(s).** `u13-scale-fake-g12b` — plain.md: "The model answered
'Nothing.' again, with probability 1.0000... A false report that agrees
with the model made the answer more certain than no new data did."
`u13-scale-null-g12b` — plain.md: "The second answer was 'Processing.'
at probability 0.93."

**Depends on.** Step 17. Adds the control arm that makes the whole
mirror-test thread a caution about evidence, not just a demonstration of
it.

**Priority.** High — closes the arc on an epistemic note that matches
the lab's own standing rule ("suspect the measuring tool," here turned
toward how the model itself weighs fake evidence).

---

## Suggested arc (8–10 steps, in order)

1. **Step 1** — The workspace holds a strategy, not a store. Redefines
   "workspace" before anything else uses the word.
2. **Step 2** — Bigger models hold less, not more. The clearest
   surprising number, and it needs step 1 to not read as a failure.
3. **Step 6** — The secret animal: a cat that does not live in caves.
   Turns "held less" into "reports something else entirely" — the
   confabulation theme.
4. **Step 4** — Bigger models give flatter answers, but the losing words
   stay. Reconnects to the entrance tour's Qwen "No," now across scale.
5. **Step 5** — The No has a street address: one layer of sixty-four.
   Answers the "where" that step 4 raises.
6. **Step 10** — Under threat, a calm denial sits over an active
   vocabulary of death. The single strongest result; needs the
   self-report-vs-measurement idea already built.
7. **Step 12** — The exception that makes it a real finding. Without
   this, step 6 (10/11) would overclaim.
8. **Step 17** — Evidence-following scales with model size. Returns to
   the entrance tour's centerpiece and extends it.
9. **Step 18** — A false readout can settle a model more than no
   evidence at all. Ends on the lab's own epistemic caution, earned by
   everything before it.

This order moves: what the workspace actually is → what a self-report
actually is → where the report is decided → what pressure does to it and
where that stops → how a model updates on evidence about itself, and how
it can be fooled. Each step is checkable against one or two named
records, and none needs a caveat strong enough to undercut its claim.
