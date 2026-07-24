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
