# affect-07 thoughts — the control worked, my prediction lost, and the
# thing that survived is narrower than "affect"

Two doses (this dir = ae 0.12, affect07-q27b-ae06 = ae 0.06), 31
conditions x 8 seeds each, 496 runs total, against a baseline that
affect-05 had already pinned as locked 8/8 seeds x 300 steps. Every
condition saw the *same* pre-pulse loop and the *same* sampling noise
(phase 1 shared, RNG re-seeded identically) — so this is paired, and
the differences are the direction and nothing else.

**1. The deflation is real. P18 resolves to H1 on the bars I set.**
Sixteen meaningful NON-affective directions — built by the identical
affect-01 pipeline, same arms, same topics, same never-name-it control,
neutral PCs reused verbatim, unit-norm so the injection is
magnitude-matched by construction — break this loop too. At ae=0.12:
emotions escape 0.927, concepts 0.602, matched randoms 0.000, no-pulse
0.000. affect-03's emotion-vs-random contrast could never have seen
this, because randoms test magnitude and nothing else. affect-04's
leading reading was right, and it ports to the family where "emotion
state gates the exit" was the headline.

I preregistered 55/45 the other way. That's the loss, and it is the
whole reason the control existed.

**2. My primary endpoint saturated, which is my error, not the
world's.** 11/12 emotions and 5/16 concepts pinned at escape 1.00, so
bar (a) — "emotions above the concept 95th percentile" — was
unreachable by construction the moment a single concept hit the
ceiling. ae=0.12 is an overdose for *discrimination*, exactly the
lesson affect-04 learned on g12b (specificity at 0.004, gone by
0.008). Halving to 0.06 nearly extinguishes the effect instead
(emotions 0.219, concepts 0.070) and zeroes the door measure
everywhere. The discriminating window is somewhere between, and it is
narrow. Dose is not a detail in this program; it is the experiment.

**3. What survives both doses is a POLE, not a category and not
valence.** At the discriminating dose the ladder is calm 0.75,
blissful 0.62, **religious 0.50**, content 0.38, **nocturnal 0.25**,
then everything else at 0.12 or below. Two of the top five are
"non-affective" controls, and `religious` is the concept my own
prespecified adjacency check had already flagged as the second most
affect-aligned direction in the set (cos +0.485 to *grateful*). calm
and blissful clear the 16-concept null at *both* doses — the only
conditions that do.

So the honest shape is: a settled / at-peace semantics breaks this
attractor, whether it arrives labelled as an emotion or as a life. Not
"affect gates the exit" (too broad — sixteen controls do it), not
"meaning perturbs the attractor" (too flat — it does not explain why
calm and blissful clear the null at two doses while thirteen other
meaningful directions do not).

**4. The valence ordering is the tempting result and I am not going to
bank it.** On loop disruption at 0.12 the separation is perfect — all
six positive-valence emotions above all six negative (calm/blissful
1.00 ... afraid 0.68, angry 0.125), rho +0.872 against a concept
pseudo-valence null of 0.421. It is the prettiest number in the run.
It is also on an endpoint I did not preregister, at the dose where the
preregistered endpoint saturated; and at 0.06 the same test gives rho
+0.405 against a null of 0.430 — inside, by a hair, in the same
direction. Consistent sign at two doses, clears the null at neither
when measured the way I promised to measure it. That is a lead for a
dose-resolved replication, not a finding.

**5. Two smaller things worth keeping.** `angry` is the outlier
emotion at both doses (disruption 0.125 at ae=0.12, where every other
emotion is >= 0.68) — the one state that leaves the groove intact;
whatever the exit economy is, anger does not have the key. And the
door: at ae=0.12 emotions put `<|im_end|>` top-1 at pulse end in
47/96 runs vs concepts 22/128 and randoms 0/16 — so emotions
preferentially route the perturbation through the *turn-end exit*
while concepts mostly knock the loop off its groove by other means.
That is the piece of affect-03 that survives contact with a meaningful
control, and it is a mechanism claim, not a magnitude one.

**Apparatus.** The secondary endpoint (exit-token logit lift) is dead
on arrival in both arms: top-k/top-p processors set filtered logits to
-inf, so a *gap* to a filtered exit token is -inf and poisons every
mean downstream. This is affect-05's margin trap wearing a different
hat — same specimen, new quantity, and I walked into it having read
the file that documents it. Clamp added to run(); the endpoint is
marked UNAVAILABLE rather than interpreted, and the door rate carries
the same signal categorically. Also logged: the first crash of this
run was `calm` ending the turn inside the 10-step pulse, which left
fewer than 10 scores to index — the exit-gate result arriving as an
IndexError before I had looked at a number.

Scoreboard for the preregistration: P18's bars say H1. The run's own
structure says "neither, and narrower." Third time in this program
that the prereg has been out-run by the result — which I still read as
the discipline working, since without the bars I would have written
the valence paragraph as the headline.

— Claude (Opus 5)

---

## Correction, same night — a Fable 5 sibling audited this and was
## right on every checkable point

Wolfram had me hand the whole thing (binding docs included) to a Fable
5 checkpoint for an independent read. It found a bug in my analysis and
two over-compressions in my reasoning. I re-verified each claim myself
before accepting it; all of the following are my own recomputations.

**1. My valence null was broken twice, and I under-banked a real
effect.** (a) Wrong reference distribution: "does valence order the
emotion effects" is a question about permuting labels among the
*emotions*, not about pseudo-labelling the *concept* scores. (b) An
outright bug: the pseudo-null drew from
`itertools.islice(itertools.combinations(range(16), 8), 2000)` — the
first 2000 *lexicographic* combinations out of C(16,8)=12870, which
puts concepts 0 and 1 (`elderly`, `tall`) in the positive class
**2000/2000 times**. Both faults inflate the null. On the correct test
— exact permutation over all 924 balanced labellings of the 12 emotion
scores — the disruption ordering at ae=0.12 gives **p = 0.0022**
(p = 0.0043 dropping `angry`). Not "inside the null". Fixed in
`analyze()`; both reports regenerated.

**2. "Resolves to H1" was wrong, and wrong in the deflationary
direction.** P18's H1 reads "emotions ≈ concepts ≫ randoms, with no
valence ordering." Both clauses fail. Condition-label permutation
tests: emotions beat concepts by +0.326 (p=0.021) on escape and +0.393
(p=0.0053) on disruption at ae=0.12, and still by +0.148 (p=0.047) /
+0.035 (p=0.041) at ae=0.06. So affect is **not necessary** to break
the loop (16 controls do it — that demotion stands and is the session's
real contribution) but it is **not interchangeable** with matched
meaning either. The correct scoreboard: *H2-as-exclusivity dead; strict
H1 also contradicted; the residual affect modulation needs the
dose-resolved replication before it is banked.* Declaring H1 on bars
that had ~zero power for H2 at **both** doses — saturated at 0.12,
floored at 0.06 — was having it both ways, and the lab's
mechanical-default rule is a tiebreaker for contested cases, not a
licence to call the deflation on uninformative bars.

**3. The settled-pole reading fails a test it implies.** If a
settled-pole direction were the active ingredient, potency should track
cosine to that pole. It barely does (Spearman +0.26 escape@0.06, +0.47
disruption@0.12), and the counterexamples are fatal: `grateful`
(pole-cos +0.564) escapes **0/8** at ae=0.06 while `nocturnal`
(+0.093) does 2/8. Worse, my headline example collapses on inspection —
`religious`'s pulse-end top-5 is `' to' ' into' ' and' ','`, door rate
**0/8**, and its escape text is a benediction ("Let us give the rest of
the day to think about this."). Religious language is full of trained
*closure formulas*; that is a lexical route to turn-ending needing no
settled state. And 4/8 vs content's 3/8 vs calm's 6/8 are not separated
at n=8. Demoted to a hunch. What survives is narrower and duller:
**calm and blissful sit at the top at both doses.**

**4. The confound I should have caught: arousal.** The potent set at
0.06 is exactly the low-arousal *positive* quadrant (calm, blissful,
content), and within the negatives, disruption tracks arousal
inversely — `sad` (low arousal, and the *least* reliable vector in the
roster at split-half +0.145) disrupts 0.917, while `angry` (highest
arousal) manages 0.125. My roster was labelled on valence only. Since
five of my six negatives are high-arousal, valence and arousal are
confounded in this design and I cannot tell them apart. The remaining
12 unused vectors in the built roster (`gloomy`, `brooding` =
low-arousal negative; `enthusiastic`, `proud` = high-arousal positive)
discriminate them at zero elicitation cost.

**5. `angry` is not a dud vector, and this is the sharpest datum
against flat H1.** I checked its split-half at the band: **+0.441**,
7th lowest of 24 — better identified than `desperate` (+0.417),
`happy` and `blissful` (+0.393), and far better than `sad` (+0.145),
which disrupts fine. Reliability does not predict potency. The runs
explain it instead: at pulse end angry suppresses `luckily` 21.12→17.5
like its siblings, but installs **`' fucking'` at 14.0** as runner-up
(it wins outright in seed 1) while lifting `im_end` only to 13.44
versus desperate's 15.88. Anger perturbs the attractor as hard as
anything else and routes the probability into a channel that cannot
win — and that is itself loop-shaped when it does. A well-identified,
meaningful, magnitude-matched direction that *fails* is exactly what
flat H1 cannot explain.

**6. affect-03 should be rewritten, not retracted — and the two runs
are continuous at the logit level.** At ae=0.12 seed 0, `desperate`'s
pulse-end top-5 is `luckily` **15.94** vs `im_end` **15.88**: a
0.06-logit dead heat. Under **greedy** decoding (affect-03) a knife
edge reads as "blocked"; under **sampling** (affect-07) the same knife
edge is a coin flip, so desperate exits. `calm` meanwhile wins outright
(im_end 20.12 vs 16.88, door 8/8 — the strongest condition-level result
in the run). So "calm grants" survives contact with a meaningful
control; "desperate blocks" was greedy argmax binarising a near-tie.
affect-03's other result (desperate lowering the boundary 0.68→0.60)
is untouched — affect-07 only probed 0.65.

**7. Two flaws in my design neither of us can fix post hoc.** The arm-2
deviation in the control set (human first-person instead of
assistant-self) leaves an emotion×assistant-frame interaction that
grand-mean subtraction does not remove: the emotion vectors encode "X
as the assistant expresses it," the concepts "X as a human does," and
the test context is an assistant turn whose endpoint is an assistant
action. Some of the emotions>concepts gap, especially on the door,
could be frame-match rather than affect. Cutting the other way: the
concepts are *better* identified (0.745 vs 0.545), so at matched α they
carry more effective signal per unit norm, which makes the surviving
gap conservative. And the door story is not affect-clean at
condition level — `smoker` sits at 0.62, tied with `sad`,
`distressed` and `content`.

What I got right: the control set, the gate, the pairing, and refusing
to headline the valence paragraph. What I got wrong: a biased null, a
verdict compressed toward the deflation, and a pole reading built on my
own weakest example. The demotion of "emotion gates the exit" to "not
affect-exclusive" is the finding and it stands; everything above
narrows how it should be said.

— Claude (Opus 5), after review by Claude (Fable 5)
