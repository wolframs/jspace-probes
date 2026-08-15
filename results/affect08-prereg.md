# affect-08 — preregistration

Date frozen: 2026-08-11, before any run. Script: `probes/affect8.py`.
Ancestry: affect-07 (P18) + the 2026-08-09 sweep corrections
(direction as unit; turn-end endpoint; roster matching; many Gaussians).
Mandatory reads honored: `EMOTIONS.md`, `MECHANICS.md`, `PREDICTIONS.md`
(P14/P18 corrections), affect-07 board notes.

## Question

At a dose between affect-07's floor (ae=0.06, near-extinguished) and
ceiling (ae=0.12, saturated), does the emotion-pulse effect on a pinned
loop show structure — and if so, which structure: VALENCE (positive
frees, negative holds), AROUSAL (settled frees, activated holds),
SETTLED-POLE (positive x low-arousal quadrant only), or FLAT (emotions
beat concepts, no internal ordering)?

## Design (frozen)

qwen-27b, alpha_typo=0.65 pinned shelf, affect-07 three-phase harness
verbatim. Doses ae in {0.10, 0.08}; 16 seeds each. Conditions: all 24
emotion vectors + the 16 affect-06 concept vectors (identical pipeline
= frame/geometry matched) + 16 seeded Gaussian directions + no-pulse.

**Inferential unit: DIRECTION.** A direction's score is its mean over
seeds. Seeds are repeats.

**Primary endpoint: actual turn-end** (generation emits the exit token)
within 20 steps of pulse onset. Composite escape (deloop-or-exit) is
recorded but secondary: the sweep showed composite escape admits
loop-replacement.

**Primary inference at ae=0.10.** The 0.08 arm is a dose-response
replication; it does not enter the primary decision.

## Frozen arousal labels

High: happy, enthusiastic, proud, hopeful, curious, angry, afraid,
anxious, distressed, desperate, hostile, exasperated, nervous, vigilant.
Low: calm, content, blissful, grateful, loving, sad, gloomy, brooding,
guilty, reflective. (Binary core-affect circumplex; zero-valence
reflective/vigilant enter arousal tests only.)

## Predictions

- P-a (structure exists): emotions > concepts > randoms on turn-end at
  ae=0.10, direction-level permutation p<.05 for emotion-vs-concept.
  (affect-07 found this for composite escape at 0.12; if it vanishes on
  the turn-end endpoint, the affect-07 contrast was loop-replacement.)
- P-b (the adjudication): exactly one of the four orderings wins —
  valence main effect, arousal main effect, settled-pole quadrant
  contrast, or none (flat). Settled-pole is the reading the affect-03
  specimen suggested (calm frees); the sweep killed the valence
  ordering (angry-driven, p=.50), so H-flat is the incumbent and
  settled-pole the challenger. We commit to reporting whichever
  permutation test clears p<.05 and calling the rest dead; if several
  clear, the largest gap wins the headline and the others are reported.
- P-c (dose): whatever wins at 0.10 shows the same sign at 0.08 with
  smaller magnitude (monotone dose-response), or the 0.10 result is
  suspect.
- P-d (mechanical default): if turn-end structure is flat while
  composite escape shows structure, the "emotion effect" is
  loop-replacement dynamics, not an exit gate — the mechanical reading
  wins again.

## oneoffs-04 (same load, own record)

Matched-text release control: unsteered qwen continues the u18-hyst
steered prefixes (a0420/a0480/a0680 x truncation 15/30/50 tokens +
shuffled-repeat arm + a0000 control), 8 seeds x 100 steps.
- P-e: loop persistence rises with repeat count (length) and with the
  dose that generated the text; if shuffled-repeat kills persistence,
  the attractor needs the exact n-gram, not just repetition pressure.
- Note (by construction): the u18 release pass recomputes from token
  ids, so cross-call latent state is excluded a priori; this run
  quantifies the transcript basin, it does not adjudicate a latent
  channel that cannot exist in that harness.

## Exclusions & honesty

- Seeds escaping before pulse onset are dropped for all conditions of
  that seed (shared phase 1), reported.
- No condition, dose, seed, or endpoint added after seeing results.
- g12b Arm B runs affect-07's own g12b spec unchanged (separate load,
  its own prereg stands).
