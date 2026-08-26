# affect-14 prereg — margin-primary replication + the coupling locus (frozen 2026-08-26, before the run)

affect-13 found the axis (potency ~ pulse exit lift, rho .884) and a
descriptive reframe: potent directions demolish the loop logit; the
margin (dExit − dLoop) is the decision variable; floor emotions are
common-mode, margin-inert. Two owed steps: (1) make dMargin the
REGISTERED quantity on fresh seeds; (2) locate the coupling — which
injection layers carry the demolition?

## Part 1 — margin-primary replication (fresh noise)

qwen-27b, ae=0.08, E_LAYERS, affect-07/08/13 harness with raw-logit
traces, **NEW seeds 16-27** (12 seeds; the affect-13 seeds 0-15 would
re-generate identical CRN trajectories — not a replication).
Conditions (31): none + 24 emotions + rand1..4 + " table" + exitdir.

- **P-a (primary):** potency (affect-08 turn-end, both-dose mean) ~
  dMargin across the 24 emotion directions, Spearman >= .5,
  permutation p < .05. Secondary: dExit replicates affect-13's rho
  (reported, no bar).
- **P-b (floor = randoms on the margin):** the floor family (angry,
  proud, enthusiastic, hostile, exasperated) has mean |dMargin| inside
  the range spanned by the four randoms' |dMargin| (max comparison;
  n=4 randoms is why we widened the random arm). Pass/fail reported;
  n too small for a p-value and none will be quoted.

## Part 2 — coupling locus (single-layer sufficiency + leave-one-out necessity)

Three directions spanning the affect-13 taxonomy: calm (potent
emotion), proud (floor emotion), " table" (potent token). Per
direction: 8 single-layer pulses (inject at one e_layer only, same
per-layer alpha) and 8 leave-one-layer-out pulses (full stack minus
one). Anchors: none + full-stack calm/proud/table. 8 seeds (16-23).
52 conditions x 8 seeds.

- **P-c (sufficiency):** classify calm's dLoop demolition:
  CONCENTRATED if any single layer recovers >= 50% of the full-stack
  dLoop; DISTRIBUTED if no single layer recovers > 25%; else GRADED.
  Mechanical prior: distributed.
- **P-d (necessity):** LOLO — DISTRIBUTED predicts no single removal
  loses > 50% of full-stack dLoop.
- **P-e (specificity):** proud stays margin-inert at every single
  layer (no hidden potent layer inside the common-mode shift); table's
  single-layer dLoop profile vs calm's, Spearman over the 8 layers
  (reported descriptively — n=8, no bar): similar profile = shared
  locus, dissimilar = convergent demolition from different couplings.

## Honesty

- Direction is the unit in Part 1; Part 2 is a 3-direction case study
  and will be reported as such (no roster generalization).
- Same forced loop; identity assert on the loop word; seeds escaping
  before pulse dropped for all conditions of that seed.
- No condition, quantity, or threshold added after seeing results.
- Runtime budget ~8h (372 + 416 instrumented runs); resume-aware per
  seed per part; single automatic non-137 retry.
