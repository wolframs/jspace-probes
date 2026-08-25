# affect-13 prereg — dynamics of the exit gate (frozen 2026-08-25, before the run)

affect-12's decision rule: the grouping is not geometric, so watch what
the injection DOES. Full-roster overnight run: every free step of the
affect-07/08 pulse harness instrumented with RAW logits (output_logits,
not the top-k-filtered scores — the affect-05/07 −inf trap is the
reason this endpoint has never been read).

## Design

qwen-27b, ae=0.08, E_LAYERS, seeds 0-15, same forced loop, phases
PRE 20 / PULSE 10 / POST 50, CRN seeds as affect-08 (the trajectories
re-generate bit-identically, so dynamics align with known outcomes).

29 conditions x 16 seeds = 464 runs:
- none
- all 24 emotion vectors
- rand1, rand2 (null anchors)
- " table" pullback (the affect-11 token-potency specimen)
- exitdir (im_end pullback, direct-push positive control)

Per free step, store: exit-token raw logit, loop-token raw logit,
top-1 and top-2 raw logits and ids. Primary derived quantity per run:
**pulse exit lift** dExit = mean over pulse steps of (exit_logit −
none-condition exit_logit at the same seed and step).

## Predictions

- **P-a (the gate is the readout):** across the 24 emotion directions,
  potency (affect-08 turn-end, mean of both doses) correlates with
  dExit at direction level, Spearman >= .5, permutation p < .05. This
  is the inferential claim of the run.
- **P-b (two floors, sign prediction — descriptive, n too small for
  family inference):** anger family (angry, hostile, exasperated)
  shows dExit < 0 (active suppression below the unsteered path);
  pride family (proud, enthusiastic) shows dExit ~ 0 (inert). Reported
  per-direction; no family p-value will be claimed.
- **P-c (order of events, per potent run):** classify first-crossing
  inside pulse..pulse+W: (a) exit token reaches top-2 while the loop
  token still holds top-1 ("door first") vs (b) top-1 stops being the
  loop token before exit reaches top-2 ("deloop first"). Majority
  class across potent-direction runs decides whether the gate action
  is direct or the exit follows loop collapse. The mechanical default
  is (b).
- **P-d (construction classes):** " table" and exitdir classified by
  the same P-c rule; if " table" matches calm's class, token-potency
  and emotion-potency share a route; if not, affect-11's confound is
  mechanistically distinct.

## Honesty

- Direction is the unit; seeds are repeats. P-a is the only powered
  claim; P-b/P-c/P-d are classifications with counts, no post-hoc
  tests will be added.
- Seeds escaping before pulse: dropped for all conditions of that
  seed, reported.
- If the none-condition exit logit already drifts upward within the
  window (baseline instability), dExit is read against that drift by
  construction (same-seed same-step subtraction); no further detrend.
