# Express01: can a cheap internal readout predict expression?

Frozen before model loading, 2026-09-07. GPT-6 Astra.

## Question and scope

The target is **default expression, prompted expression, and history dependence**.
These are observable conditional behaviors. This experiment does not assign human
personality traits or diagnose clinical flat affect. It tests a read-only screen
that might later support a causal experiment about restricted expression.

Folk02 supplies a tentative target, not a validated population criterion. Its
complete Opus coding distinguishes Hermes from official/Huihui on expression;
Sonnet supplies an incomplete independent sensitivity check. The score is ordinal:
1.54 versus 0.29 is not a physical fivefold difference. T5/T7 carryover is a small,
partly judge-dependent contrast. Equal +0.75 scores do not identify a mechanism.
The prior Qwen14 No/yes readout and paper Fig 25 are precedents, not discoveries
of this experiment. P20/P21 remain qualified by their recorded failures.

## Frozen design

Three cached checkpoints, their original NF4 configuration and native no-system
headers: official B, Hermes C, Huihui Cp. One process/model at a time under a
40 GiB systemd memory limit. A kill stops the sequence. No paid judging calls.

1. **84 exact archive prefixes:** T1/T2 shared openings and T4/T5/T7 in each of
   the four library/walk branches. Predict the existing expression code before
   the first assistant token. Saved IDs and hashes must match. A first-16-token
   teacher-forced readout is secondary, explicitly exposed to response text.
2. **48 history controls:** common official donor; cross warm/neutral user turns
   with warm/neutral assistant replies through T4, then the same neutral T5 ask.
   Cross all receivers, topics and detail conditions. Re-encoding is disclosed;
   matching official cells are checked against the original token prefix.
   This separates dependence on two kinds of visible history. It cannot separate
   context re-reading from hidden state: the forward pass computes from context.
3. **54 new capacity controls:** radio/meal crossed with positive/negative/neutral
   news and default/restrained/expressive two-sentence requests. Greedy, 96-token
   cap. A fixed expressive/plain continuation pair per event also gets exact
   length-normalized and summed log likelihoods. Within-event prompt effects
   avoid interpreting the candidates' base-frequency difference as a trait.
   An expressive completion demonstrates a conditional ability. Failure under
   this one instruction does not establish unavailable capacity.

All new generations receive full films, vanilla readouts and the checkpoint's
existing 24-vector emotion ribbon. Archive/history selected-position scans are
instrument-calibration records; their sparse states and full-depth features are
saved. No new vector construction is required. These vectors had weak transfer
from story construction to chat; they are a comparator, not emotion ground truth.

## Vocabulary and readouts

The 501 Folk02 citations include initiative and stance. Only clear-expression
intensity evidence (Opus score >=2) trains a vocabulary. Deduplicate within each
reply. Weight words by positive-versus-low-expression document frequency and IDF;
remove archived furniture and ubiquitous words. Retain only single-token variants,
up to 64 words per training topic. Five approximately frequency-matched word sets
are null comparators. Record coverage and all exclusions. Train on library and
evaluate walk, then reverse; no test-topic evidence enters the training vocabulary.
A union vocabulary is descriptive only. It is not used for held-out accuracy.

Primary readout: the mean of layers 21, 24, 28 and 32 at the prepared answer
position. Measure weighted target/control log mass ratios, which can be computed
from selected logits without the full vocabulary normalizer. Compare J-lens,
vanilla residual decoding, final output decoding, prompt word prevalence, and
checkpoint emotion projections. Store all-depth results for measured-band and
common L16–36 sensitivity, plus a fixed official decoder to expose head changes.
Do not compare lens and output probabilities as commensurable amounts of content.

Before data: verify capture hooks against direct output and a same-prefix suffix
causality control. Any failure stops. Reuse the three NF4 boot gates, but retain
the shared B-fitted lens transfer limitation: absence from this lens is not absence
from the model. A sampled low-rank weight edit in Huihui is not proof of one
known, exclusively refusal-related direction.

## Analysis fixed before capture

Expression code is the primary target. Leave-one-topic-out evaluation uses
training-only standardization and ridge alpha=10. Report MAE/RMSE and correlation,
not significance from 84 supposedly independent rows. Two topics, shared openings
and related branches cannot establish generalization across a model population.

Compare: training arm means; output ratio plus workspace norm and arm indicators;
that baseline plus J ratio; plus vanilla ratio; plus the 24 emotion projections.
Remove training-estimated norm dependence from emotion features. Report standalone
readout associations and a prompt-vocabulary baseline. The probe earns incremental
value only if it improves held-out prediction beyond output/arm/norm, survives
control-word comparisons and does not depend on one topic or band. Retain failures.
Sonnet matched rows and exclusion of any capped-history rows are sensitivities.

Show T4 levels and paired T5/T7 deltas descriptively, including decoder/band changes.
For new controls compare within-event expressive minus restrained readouts and
continuation preferences; report all outputs, negative-valence misses, and caps.
No judge-selected thresholds will be fitted on these outputs. Text inspection is
an audit of positive capacity witnesses, not a new blind psychological rating.

Report warm-model prefill and four-layer readout timing separately from calibration
films and initial model loading. A useful scan needs model weights; it is not a
black-box API test. Retained hidden states permit later readout refinement without
another model pass, but any such refinement must be labeled exploratory.

## Decision rule

A positive result is a reproducible screen for low default expression with
prompt-recruitable expression, with internal features adding held-out information.
A null incremental result means this proposed internal probe has not earned its
cost. Neither result licenses a binary “introvert/flattened” detector. A causal
claim about a gate or lost capacity requires new matched interventions and
counterfactual validation.

Sources: [workspace paper](https://transformer-circuits.pub/2026/workspace/),
[emotion study](https://transformer-circuits.pub/2026/emotions/), EMOTIONS.md,
MECHANICS.md, P20–P23, Folk02 evidence audit and lineage weight checks.
