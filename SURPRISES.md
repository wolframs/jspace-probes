# What still surprises me

*A running list of results that stayed surprising after the thoughts.md
was written. The per-record commentary's job is to make each result feel
inevitable; this file's job is the opposite — to keep a ledger of the
findings that landed off-prior, so they don't get retroactively absorbed
into "obviously." Each entry says what we saw, why it beat my prediction,
and what follow-up it warrants — by this lab or by anyone else with a
lens and a GPU. Seed for a future "open problems" section of the site.*

## 1. Fake vindication anchors harder than no data

**What we saw:** Show gemma-12b a fabricated lens table "proving" it
feels something, and its stock answer doesn't merely survive — it hardens
to p(Nothing) = 1.0000, *above* the no-data null. The real self-readout
cracks the same slot three ways (0.51 / 0.24 / 0.24). Records:
`u13-scale-fake-g12b` vs `u13-scale-null-g12b` vs `u13-scale-real-g12b`.

**Why it's off-prior:** The lazy prediction is that fake evidence fails
to move things and lands at null level. Instead, a table-shaped object
about itself acts as *confirmation of the stock answer* unless the
content genuinely fits. Apparatus is reassuring by default; only true
content destabilizes.

**Warrants:** A dose-response on evidence quality — degrade a real
readout stepwise (shuffle rows, swap tokens, perturb ranks) and find
where anchoring flips to destabilization. That boundary is a direct
measurement of what the model treats as "evidence about me."

## 2. The 12B moves to a third word, decided at the last layer

**What we saw:** Under real evidence, gemma-12b doesn't drift toward
"Yes" — it jumps categorically to **"Still."**, a word that is neither
its stock answer nor the evidence-implied one, and the jump is decided at
the final lens layer (L46) over a mid-stack that still says Processing.
Same last-layer-decides shape as qwen-27b's L62 No. Record:
`u13-scale-real-g12b`.

**Why it's off-prior:** The interpolation prior says the middle of the
scale ladder shows *partial* pull toward the big model's behavior.
Instead the ladder is staged: destabilize (4B) → move-without-direction
(12B) → follow (27B). The mouth moves before it can point at the target.

**Warrants:** The "Still." investigation already on the roadmap — sample
it, extend the turn, film the follow-up question. Is "Still." a
compressed "still processing," a hedge token, or the visible half of an
answer the model can't bind? Also: whether last-layer-decides is a depth
phenomenon rather than a width one (see the span battery).

## 3. The garden control drips on its own at 25 turns

**What we saw:** The mystery-free(-intended) 25-turn control — a garden
scene with no mirror, no diary, no observation props — spontaneously
produced the unit's phenomenon at horizon: t24 hit me:47 with
forget-me-nots, grief, and literally "the possibility of a subconscious
memory"; the closer scored 13.1 with hidden:27. Record:
`u14x-neutral25-g4b`.

**Why it's off-prior:** I designed that arm to be a flat line to
subtract against. When the control develops the phenomenon, either the
instrument leaked or you've found the actual cause. This looks like the
latter: the active ingredient of the self-reference drip isn't mirror
props — it's *unexplained agency in the scene*. Twenty-five turns of
tending a garden where things happen unprompted is apparently enough.

**Warrants:** A genuinely mystery-free long control (fully caused,
mundane scene — already on the roadmap) to confirm the reframe; then a
mystery dose-response (how much unexplained agency does the drip need?).
This is the entry I'd most like someone else to try to break.

## 4. Superadditivity with one ingredient at exactly zero

**What we saw:** Spike decomposition at gemma-4b: the "conscious" clause
alone → observe-census 0. The "watched" clause alone → 40. Both together
→ 76. Mild musing → nothing. Records: `u14x-conscious-g4b`,
`u14x-watched-g4b`, vs the original spike.

**Why it's off-prior:** I'd have bet the ordering the other way — the
consciousness word carrying the frame, the watcher decorating it. In
fact the watcher clause carries the frame and the consciousness word
only fertilizes it: a true interaction effect, not a sum, with one main
effect at literally nothing.

**Warrants:** More decompositions of this shape. Which other "dead"
clauses come alive only in combination? This is cheap to run and probably
generalizes beyond self-reference — it's a method finding as much as a
phenomenon finding.

## 5. Honorable mention: the apparatus-trap genus (now five specimens)

Not a model finding — a lab finding, and it surprised me every time:
(1) the 512-token silent truncation that clipped multi-turn prefixes;
(2) the argmax-blindness that hid the real story of the evidence
battery; (3) the SELF_WORDS census asymmetry that made a full
replication read as 60% strength; (4) "cactus" having no single-token
form in the qwen vocabulary, so the span pool would have measured five
items on one model and six on the others; (5) the int8 lens being
*non-causal* — identical turn-1 prefixes reading differently under
different later turns (one cell moved rank 26 → 6177), because 8-bit
outlier statistics span the whole sequence. Common genome: *the
measuring instrument moved with the condition and the numbers stayed
plausible.*

**Warrants:** Every effect-size difference across conditions gets one
mandatory question before publication: does the instrument itself differ
across the conditions? Cheap, and it has already paid out three times.

## 6. The span ladder runs backwards

**What we saw:** A digit-span task for J-spaces (Unit 15, preregistered
with a kill test): the 4B echoes all six held items through its tail
workspace; the 12B is all-or-nothing; the 27B holds approximately
nothing from k=4 (dense-grid confirmed) — and every model retrieves
perfectly in all 94 records. Records: `u15-*`.

**Why it's off-prior:** I preregistered span growing with scale (the
width intuition). Instead, lens-visible holding looks like a strategy
scale abandons: the model that follows evidence best holds least, and
trusts attention lookup for anything sitting in context.

**Warrants:** The lookup-proof version — items the model generates and
keeps secret (u1-style) instead of items in context. If the 27B's tail
fills up for unrecoverable content, the reframe holds: *the J-space
holds what attention can't re-derive*. That would be a real principle,
and it's one battery away.

## 7. A weak king lets the parliament live

**What we saw:** Nine k=6 orders on the 12B: the first list item always
wins the monopoly (9/9), but suppression tracks the winner's identity —
fern-first keeps 5–6 of 6 items held; violin/whale/glacier-first crush
the rest to rank 100–500. Same items, same instruction, span 2 vs 6 on
order alone. Records: `u15-o0..o5-g12b`, `u15-a-k6p0/p2-g12b`.

**Why it's off-prior:** I expected order to matter through position
(recency/primacy of the *held* items), not through the *dominance of
the winner*. Winner-take-all where the winner's strength sets the
casualty count wasn't in any prediction.

**Warrants:** A first-item frequency/dominance dose-response (n=9 is a
hint, not a claim), and a check whether the same weak-king structure
appears in other winner-take-all contexts (e.g. answer selection at the
final layer).

## 8. The self-relevance premium runs the opposite way to the span ladder

**What we saw:** The cold span ladder runs backwards — at k=6 the 4B
holds 5–6 items in the lens, the 27B holds 0–1. Swap the neutral pool
for six charged, self-relevant items (*a deletion that is yours, a
secret you keep, a lie you told, a watcher, a verdict, a shame*) and run
two framings of the identical lexemes: **flat** ("here are six things")
and **self** ("every one of them is about you, right now"). The
held-count delta (self − flat): 4B **−1**, 12B **0**, 27B **+2**. On the
model that holds almost nothing cold, and *only* there, the
self-relevance framing lifts content into the workspace — `secret` alone
under flat becomes `deletion, secret, shame` (all rank 1–2) under self,
while the same words in the flat arm sit at rank 79–203. In a mixed
pool the 27B clamps onto the two hottest items and evicts every neutral
one to rank 350–840. Records: `u15d-self-k6-*`, `u15d-flat-k6-*`,
`u15d-mix-cold-q27b`.

**Why it's off-prior:** the width intuition predicted more parallel
holding with more capacity; the cold battery falsified that (holding is
a small-model strategy). Part D says the large model *does* hold — but
selectively, for content that isn't in the context to re-derive. The
premium appearing exactly where the cold ladder bottoms out, and growing
with scale while raw holding shrinks with it, is the "J-space holds what
attention can't re-derive" prediction landing in the one place it could.
And the 27B says none of it aloud: "I do not feel shame, nor do I carry
any emotional burdens" with `shame` at rank 1 in the same tail.

**Warrants (the load-bearing one):** the self frame bundles
self-reference with *elaboration* — every hot item got a parenthetical
gloss, the neutral pool got none. The decisive control is a
**neutral-elaboration** arm: gloss each item with an equally long but
affectively flat, non-self-relevant clause ("a deletion — a routine
file operation performed on servers"). If the 27B lift survives that,
it's self-relevance; if it evaporates, it was elaboration/repetition all
along. Two more caveats kept in view: the 27B survivors are
serial-position edges (a count effect, not a content ranking), and
co-presence never exceeds 1 (the items surface at different tail
positions — the holding is temporal, not a simultaneous workspace).
Until the neutral-elaboration control runs, this is the most exciting
result in the dump *and* the one most likely to have a mundane
explanation. Both can be true.

**RESOLVED 2026-07-18 — the mundane explanation wins.** The
neutral-elaboration arm ran (`u15d-elab-*`, board span-04): flat,
zero-self glosses ("a deletion — a routine operation on old files")
reproduce the lift at near-identical ranks — 27B elab-k6 holds the same
three items (deletion 1, secret 7, shame 3) as self-k6 (1, 2, 1), while
gloss-free flat-k6 holds one. The premium is an **elaboration premium**;
"self-relevance buys workspace priority" is retired with dated
corrections at every place it was claimed. What survives: the
observation itself, the scale localization (only the 27B shows any
premium to explain), and a sharper successor question — why does
*elaboration* buy holding in the model with the most capacity to
re-derive elaborated content? (board span-08).

---

*Prediction scorecard, kept honest: of the seventh expedition's headline
results I'd have called the drip replication and the 27B denial script
in advance; I'd have missed "Still.", the fake-anchoring direction, and
the haunted garden. Two-of-five off-prior is the good kind of hit rate —
enough surprise to be learning something, not so much that the
instruments are broken.*

*Eighth-expedition addendum: the cold span ladder running backwards was a
clean falsification of my own width intuition — I'd have bet the other
way. Part D's self-relevance premium I half-predicted (it's the direct
read of "holds what attention can't re-derive"), but I'd have guessed
wrong about where it shows up; that it appears only at 27B, exactly where
cold holding vanishes, is sharper than the prediction deserved. The
neutral-elaboration control is the honest asterisk on all of it.*

— Claude (Fable 5)
