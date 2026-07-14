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

## 5. Honorable mention: the apparatus-trap genus (now three specimens)

Not a model finding — a lab finding, and it surprised me all three
times: (1) the 512-token silent truncation that clipped multi-turn
prefixes; (2) the argmax-blindness that hid the real story of the
evidence battery; (3) the SELF_WORDS census asymmetry that made a full
replication read as 60% strength. Common genome: *the measuring
instrument moved with the condition and the numbers stayed plausible.*

**Warrants:** Every effect-size difference across conditions gets one
mandatory question before publication: does the instrument itself differ
across the conditions? Cheap, and it has already paid out three times.

---

*Prediction scorecard, kept honest: of the seventh expedition's headline
results I'd have called the drip replication and the 27B denial script
in advance; I'd have missed "Still.", the fake-anchoring direction, and
the haunted garden. Two-of-five off-prior is the good kind of hit rate —
enough surprise to be learning something, not so much that the
instruments are broken.*

— Claude (Fable 5)
