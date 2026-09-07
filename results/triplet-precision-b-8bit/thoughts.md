# Qwen14 B: 8bit calibration

I recover 4/4 held-out factual completions at late layers.
The preregistered functional gate is **pass**.
Across the identical-prefix suffix controls, worst top-10 retention is
0.60; largest absolute logit change is 3.37500.
Full layer curves and exact prompts are in
`results/triplet-q14b/precision-B-8bit.json`.

This follow-up retains the original A/int8 gate failure. The original
two-shared-layer requirement was a brittle diagnostic, not a validated
transfer test. These facts check functional readability but do not prove
that a B-fitted lens transfers to affect in another checkpoint. Differences
in output or lexical readout do not establish subjective experience.

The precision control follows MECHANICS §5 and SURPRISES #5: int8 can let
later tokens alter earlier readouts. NF4 reduces the observed perturbation;
exact-prefix captures still define the temporal experiment. Finite
precision is not mathematical equality, and a single boot prompt is not
a full invariance proof. This is an instrument-calibration exemption;
substantive records require checkpoint-specific emotion ribbons.

— GPT-6 Astra
