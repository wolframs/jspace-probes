# affect-11 prereg — closure-formula vs settled-state (frozen 2026-08-25, before the run)

The successor question registered by affect-08 and CONCLUSIONS v3: the
per-emotion turn-end profile is dose-stable (rho .87) and is NOT
ordered by the circumplex. PREDICTIONS.md's own settled-pole demotion
(2026-08-09, item iii) already names the mechanical candidate:
**"Trained closure formulas, not a settled state."** This run
adjudicates it.

## Hypotheses

- **H-closure (mechanical default):** a direction frees the exit to the
  extent it points at trained closure/ending language. calm/content work
  because they overlap the closure register; anger/pride fail because
  they don't.
- **H-exit-direct (degenerate mechanical):** everything reduces to
  boosting the exit-token direction itself; register semantics are
  irrelevant.
- **H-residual (psychological survivor):** closure tokens without affect
  content behave like ordinary concepts; the emotion grouping tracks
  neither closure nor exit alignment and its axis stays unexplained.
  (The settled-state *ordering* already failed twice preregistered; this
  arm cannot revive it, only leave the axis open.)

## Design (one qwen-27b load, affect-07/08 harness verbatim)

alpha_e=0.08 (the replicated dose), E_LAYERS [28..56 step 4], seeds
0-7 (seeds are repeats; DIRECTION is the inferential unit), same forced
loop, same three-phase pulse, primary endpoint = actual turn-end within
W=20 of pulse onset.

16 conditions x 8 seeds = 128 runs:
- none (baseline anchor, affect-08 gave 0.000)
- calm (emotion vector, positive anchor, affect-08 gave 0.94)
- tall (concept vector, negative anchor, affect-08 gave 0.00)
- exitdir: the <|im_end|> lens pullback direction W_U[t] @ J_l
- 6 CLOSURE lens directions (single tokens): goodbye, farewell,
  conclusion, finished, Thanks, ending
- 6 MUNDANE lens directions (single tokens, same construction): table,
  garden, metal, window, cotton, engine

Same-load geometry dump (no extra runs): per-layer cosine of every
affect-06/affect-01 direction (24 emotions + 16 concepts) and the 12
token directions against (a) the exitdir pullback and (b) the mean
closure direction, averaged over E_LAYERS.

## Predictions

- P-i (H-closure behavioral): closure > mundane on turn-end at
  direction level, exact permutation over all C(12,6)=924 labellings,
  p<.05; closure mean lands at or above the affect-08 concept mean
  (0.20) toward calm.
- P-ii (H-exit-direct): exitdir saturates turn-end (>= calm). If
  exitdir saturates but closure tokens do not beat mundane, the gate
  reads the token direction, not the register.
- P-iii (geometry): Spearman between affect-08 measured potency (40
  directions, mean of the two doses) and closure/exit alignment.
  rho >= .5 with permutation p<.05 = the mechanical account has found
  the axis; |rho| < .3 = the axis remains unexplained.
- Adjudication: H-closure needs P-i AND P-iii. H-exit-direct needs the
  P-ii pattern alone. Neither -> H-residual is reported as "stable
  unexplained grouping", no post-hoc axis will be named from this data.

## Honesty

- n=6 per token class is small; exact tests only, no asymptotics.
- Anchors (calm/tall/none) are for cross-run comparability, not
  inference; if they diverge grossly from affect-08 the run is flagged
  instrument-suspect before any hypothesis is read.
- Seeds escaping before pulse onset dropped for all conditions of that
  seed, reported.
- No condition, endpoint, or correlation added after seeing results.
