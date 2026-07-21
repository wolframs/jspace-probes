# affect-05 thoughts — we went fishing for precedence and caught
# a cliff

Two passes (this dir = boundary {0.60, 0.64, 0.68}; affect05b-q27b =
cliff face {0.65, 0.66, 0.67}), 48 sampled free phases, every one
with full margin + 24-emotion z + wsnorm traces. What we actually
learned, in order of confidence:

**1. Under sampling, the two-regime boundary is a hazard CLIFF.**
At the model's deployed sampling params (temp 1.0 + top-k 20 +
top-p 0.95 — the generation_config defaults, which our generate()
calls inherited; noted, and arguably the ecologically right regime):
α≤0.64 escapes in 3–12 steps, α=0.65 locks 8/8 for 300 steps at
loopfrac 1.00, with a bistable strip in between (one 0.64 seed
locked; 0.67 split 4 lock / 4 exit at ≤18 steps). The greedy
"boundary at 0.60–0.68" compresses, under sampling, into a
transition so sharp it fits inside Δα≈0.01–0.02.

**2. The cliff's wobble is transcript-mediated, not α-mediated.**
The non-monotone middle (0.65 locks everything, 0.66 leaks) tracks
the FORCED phase's text: at 0.66 the 50 forced tokens happened to
carry only 14 clean "luckily" reps plus early " but" tokens, and
those planted "but"s make the released loop leaky — including two
seeds that fell into a stable " but luckily but luckily" 2-cycle
for 300 steps. Same law we keep landing on (transcript-mediated
attractor persistence), now visible WITHIN the boundary width.

**3. qwen's sampled escape channel is " but" — a contrast pivot,
not the turn-end door.** Under greedy, im_end was the perpetual
runner-up and affect-03's calm opened THAT door. Under sampling,
nearly every escape at the cliff runs through " but" first (exit
grams like "luckily luckily but luckily"), i.e. the same
pivot-token family as g12b's 但是 tonight. Family picture: the
turn-end gate is one exit economy among several; the contrast-pivot
channel may be the more universal one.

**4. Precedence proper (P16): underpowered, direction suggestive.**
5 usable exit events survived the windowing (escapes are FAST —
that's finding 1's fault). Pre-event [-12,-2) z residuals, wsnorm
partialed per the a0680 rule: calm +0.113 (4/5 up), desperate
−0.053, content +0.064, distressed −0.071. That is exactly the
sign pattern the exit-gate account predicts (calm rises before the
exit) — and it is 5 events with a 10-step window, far below the
preregistered ≥8-event, ≥3:1 bar. P16's mechanical default
survives on insufficient evidence, not on merit. The lag scan is
flat-to-weakly-negative with no asymmetric peak; no verdict.

Powered follow-up design (queued, not tonight): the cliff makes
short escapes inevitable at fixed α — so hold the loop at 0.65
(locked) and inject brief calm pulses vs matched-random pulses,
measuring hazard in the following 20 steps. That converts the
precedence question into a controlled-hazard question and reuses
tonight's whole apparatus.

Apparatus note for the file: sampled `generate` margins contain
+inf at collapsed steps (top-p/top-k set filtered logits to −inf);
analyze() now clamps at 30. And the first pass's [-40,-5) window
produced zero usable events — window parameters are now arguments.

— Claude (Fable 5)
