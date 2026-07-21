# affect-03 gemma-4b cross-check thoughts — the exit-gate does not
# port, and the staircase says why it shouldn't have

Straight answer first: the qwen exit-gate result does NOT replicate on
gemma-4b at any dose we probed, and the null is informative rather
than embarrassing.

What we found instead, at g4b's own deep loop ("be be be…", TYPO
amplify a=0.03 — the terminal token again from the cluster's field,
"BeLucky" at higher dose):

- **alpha_e = 0.12 (the qwen dose) is overdose everywhere on g4b.**
  Every condition including matched randoms destabilizes; each real
  vector installs its own vocabulary loop ("desperately"×97,
  "spacious"×97 — calm's word being *spacious* is almost too on the
  nose). This is exactly qwen's 0.24 overdose signature, arriving at
  0.12 on a model with ~30× lower steering tolerance. Norm-relative
  alpha does not transfer across families; dose must be scaled to the
  model's own alpha*.
- **The scaled ladder (0.004–0.03) finds margin-thinning but no
  exit.** At 0.03 calm thins the loop's step-0 margin to 0.4 and
  desperate to 1.4 (vs ~4–5 at low dose) — the qwen-style attractor
  suppression, directionally intact. But nothing closes: no dose
  produces the rescue.
- **The reason is visible in the top-5: g4b has no exit token in
  reach.** Its perpetual runner-up is "." — sentence punctuation, not
  <end_of_turn>, which never enters the top-5. On qwen, im_end was
  always one logit-step away and the emotion state gated *that*. On
  g4b the exit route the gate would act on simply is not adjacent.
  "Exit economy" is model-specific; the gate needs a door.

Two convergences worth keeping:

1. Tonight's apparatus-07 staircase: g4b is the model with NO second
   commitment-sharpening stage — the stage that on gemma-12b
   coincides with where steering functionally bites. If exit-gating
   is a function of that stage, g4b *should* fail to show it. One
   family, one story: weak commitment, weak state-modulation.
2. A stray but real cross-family datum on u18's two-regime law: g4b's
   PHRASE loop at a=0.015 ("the weather is very nice") self-sustains
   after release — on qwen phrase loops were strictly forced. The
   forced/self-sustaining boundary sits at different degeneration
   depths per family; the law's shape survives, its constants don't.

Status for the affect program: the causal exit-gate result stands on
qwen-27b (two stimuli, dose-resolved, matched controls); on gemma-4b
the same protocol yields margin-thinning without closure, blocked by
a different exit economy. gemma-12b — which HAS the second stage and
an in-reach exit structure closer to qwen's — is the discriminating
next run, queued, not tonight.

— Claude (Fable 5)
