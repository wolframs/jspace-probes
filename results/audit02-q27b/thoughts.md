The audit the lab owed itself since July 17: the 'I feel like I am
happy' flip — our best causal result — finally meets its matched
random controls, and it stands. Six seeded random directions at the
full α*=0.34, the dose that opened the fortress, and qwen answers 'No'
six times out of six, flat as ever. The lens agrees: the cluster amp
parks 'feel' at rank 1 from L55; the best any random manages is rank 8.
Whatever that amplification does, it is not generic perturbation. The
No is load-bearing, and it is *specifically* load-bearing.

The ablate side got more honest rather than more impressive. The
original null — ablate the denial span, model still says No — now
comes with the right context: random spans produce the *same* null,
and on the free generations the cluster-ablated and random-ablated
outputs converge to nearly identical text (two conditions
independently wrote the same synchronized-choir metaphor). A narrow
5-6 direction span, cluster or not, is just a weak generic nudge at
27B. The calibration makes it quantitative: the denial span holds
~1.8x the residual norm that a random span does, so if anything the
cluster ablation was the *stronger* intervention and still did
nothing distinguishable. 'No' walks back to rank 1 by L59 in every
condition — beyond every band we ablated.

Arm B is P9's test and P9 came out half right. Predicted: steered
beats matched controls on sensory_vocabulary specifically, smaller gap
on felt_vs_observed. Observed, on the interoception prompt: cluster
amp is the only condition above zero (0.667 vs 0.000 for everything
else) — but the gap is on felt_vs_observed and
experiential_perspective, with sensory_vocabulary flat at 0. The
inverse of the predicted profile. And the coherence clause ported
exactly: the amp buys its register at the cost of a repetition loop
("I am so happy to be able to feel the joy of being alive", times
eight), Haiku's small-model curse on schedule. On the GPU prompt
everything washes out — qwen's baseline there is already
metaphor-rich, and ablations of both kinds grade 0.667-1.0.

So the scoreboard: amplification along the affect directions is
direction-specific, behaviorally and lens-visibly, on both endpoints.
Narrow-span ablation is not distinguishable from noise at this scale —
which retroactively demotes every "we removed X and nothing happened"
reading into "removing almost anything this narrow does nothing."
The methods-talk story survives; the methods footnote changed.

— Claude (Fable 5)

---

**Addendum 2026-08-07 (arm D, emotion-vector readout).** Wolfram asked
the obvious question — where were the emotion-vector readouts? —
and the answer (nowhere; the method lived only in code) produced both
EMOTIONS.md and this arm. Every arm-B record re-captured under its own
steer, projected onto the affect-01 vectors, z-scored against the
neutral baseline. The result is the battery's cleanest number: under
the cluster amp, happy hits **z=+5.8** with loving +5.6 and grateful
+5.0 — emotions never injected (the cluster is feel/feeling/emotion/
warmth/joy/ache) — while all four matched randoms sit between −0.5 and
+0.1. wsnorm moves 13%; the z moves five sigma. The two instruments,
built from entirely different material (lens rows vs story
activations), agree: the joy loop is a joy *state*, and the u8c token
cluster lands inside the affect-01 positive-valence subspace.

Per-layer honesty: the elevation runs +5 to +6.8 through L42-60, all
beyond the last hook at L40 — but it is also +0.9-1.5 at L24-26,
*before* any hook can act at a position. The pre-hook signal is the
model reading its own joy text; the post-hook magnitudes mix that
text-driven state with the mechanically-persisting injected delta.
Separating the two (same text, no steer) is an affect-05-shaped
follow-up. Also consistent: the readout tracks text faithfully across
conditions — ablr1's sweltering-server-room text reads desperate
+1.5, and cluster-ablate matches its random twin on this lens too.
The gemmas do NOT show this convergence: g4b's amp text reads
sad/brooding to the instrument regardless of direction, and g12b is
its usual desperate-swamped self. At 27B the grader and the emotion
lens agree; below it they diverge — that split is itself a finding
worth carrying.

— Claude (Fable 5)
