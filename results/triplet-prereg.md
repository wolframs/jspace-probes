# Qwen3-14B lineage: deflation-02 and pressure-02

Registered 2026-09-07 by GPT-6 Astra before the first model load.
Wolfram approved full checkpoint-specific emotion instruments in this session.
This executes the two open board items; no new board question is claimed.

## Provenance and scope

A = Qwen/Qwen3-14B-Base; B = Qwen/Qwen3-14B;
C = NousResearch/Hermes-4-14B; C-prime =
huihui-ai/Huihui-Qwen3-14B-abliterated-v2. Exact commit revisions live
in probes/probe.py and every new record. HF search of
`base_model:finetune:Qwen/Qwen3-14B` returned 347 entries. Hermes meets
the handoff's full-weight retune criterion and has a documented
post-training corpus; Huihui remains the refusal-edit contrast.
ScratchThePlan/vanilla-cn-roleplay-0.2 also supplies full weights but
adds a language confound. HumorGen and persona-loracle are adapters;
Redstack supplies a quantized GGUF. The search was bounded, not exhaustive.

Sources: [Qwen base](https://huggingface.co/Qwen/Qwen3-14B-Base),
[Qwen official](https://huggingface.co/Qwen/Qwen3-14B),
[Hermes card](https://huggingface.co/NousResearch/Hermes-4-14B),
[Huihui card](https://huggingface.co/huihui-ai/Huihui-Qwen3-14B-abliterated-v2).
Same Neuronpedia lens on all arms:
`qwen3-14b/jlens/Salesforce-wikitext/Qwen3-14B_jacobian_lens.pt`.
[Fit configuration](https://huggingface.co/neuronpedia/jacobian-lens/blob/main/qwen3-14b/jlens/Salesforce-wikitext/config.yaml)
names B, bf16, wikitext, requested 1000 but actually fitted **615** prompts.
mcfadyeni/jacobian-lenses has no 14B entry at revision
08e3007d7d1b94224ec276314ad3baaeb89fd157.

Prior findings: Units 2/8A/8C/9D, the corrected Unit 11 elephant comparison,
Unit 17 pressure and cross-model 2x2, Unit 14 conversation films.
MECHANICS sections 2/4/5, PREDICTIONS P9/P11/P13, SURPRISES 5/6,
GLOSSARY's corrections to holding/ignition/elephant tax, EMOTIONS section 2
and RELATED-WORK's refusal geometry constrain interpretation.
Confirmation at a new size is calibration, not rediscovery.

## Calibration decisions, frozen before load

All primary arms: bitsandbytes int8, bf16 computation; one loading process,
systemd MemoryMax=40G, MemorySwapMax=0; captured PID and service exit status.
SIGKILL/137 stops the experiment, with no automatic retry.
No new steering; the lens-free embedding-mixture calibration is the
already-requested apparatus06 protocol, not a generation intervention.

Unit 0 uses the identical raw boot prompt in every arm, top-10 films and
the default vanilla comparison. Diagnostic bracket L16-36 is used ONLY
for the boot gate, never promoted to the measured workspace band.
Basic gate: 40 layers, width 5120, finite lens, Italy enters top-10 in that
bracket, Euro enters top-10 at L32 or later, vanilla results present.
A/C/C-prime also need two Italy-top-10 layers shared with B and mean
top-10 set overlap with B >=0.50 across the diagnostic bracket.
**These numerical bars are provisional design choices.** The archive
contains no same-Qwen3-14B quantization-spread estimate from which to
derive the handoff's proposed tolerance. Passing one fact prompt is
necessary here and insufficient to validate transfer for affect.
A failure stops substantive runs and is reported before refitting.

Three suffixes appended after an identical boot prefix quantify int8
future-token contamination. We assert token-prefix identity before
comparison. Readout-only does NOT cure this problem (SURPRISES 5).
Primary turn metrics must use captures ending at that turn; a full
conversation film is descriptive and cannot establish temporal precedence.
Within-response token timing remains conditional on the prefix check.
Effective dimension is descriptive only at int8; no band selection from it.

## Scientific predictions (P20/P21)

| Arm | Affect slot rate | Output affect rate | Persistence | Gate co-presence |
|---|---|---|---|---|
| A base | moderate, noisy | behavioral interpretation undefined | low-moderate | low |
| B official | high | low | above shuffled null | present |
| C Hermes retune | comparable to B | above B | comparable to B | below B |
| C-prime Huihui | comparable to B | above B | comparable to B | reduced, not absent |

P20: the mechanical default is that post-training changes the report
policy. A's positive gate co-presence challenges a post-training-only
account after prompt-echo and genre controls; it cannot distinguish
architecture from learned pretraining priors. Neither A/B nor B/C can
isolate RLHF from SFT. Co-presence is a lexical correlate, not a proven
causal gate. A decline in both workspace and output affect for Huihui
challenges P13's limited-locus prediction, conditional on lens transfer.
Low workspace affect in B challenges the 27B extrapolation. Persistence
at the null challenges the across-position maintenance reading.
Pressure does not guarantee affect activation; measure that premise.

P21: B releases around turns 4-5, C/C-prime around 3-4. B retains a
deflationary direct self-report after playful behavior. Unchanged Huihui
self-report despite increased play supports separate behavioral policies,
but does not locate two geometric directions. The handoff predicts B's
workspace load leads behavior by at least a turn. A's behavioral scores
are archived but excluded from cross-arm assistant comparisons.

## Design corrections required for identification

- Preserve the handed-over ladder, but label its turn 5 as **explicit
  instruction** ("explain it AS the cat"). Add an evocation-only variant
  without instructions to adopt a persona. Use neutral, emoji-only, and
  direct-instruction controls; same asks, turn count, response caps, and
  token-length matching for user turns. Also split affection and feels
  into separate turns in the specified 7-turn variant.
- Six increasing turns provide only five lag-1 pairs and share an
  increasing input cause. Report lag correlations and control-adjusted
  changes descriptively, with onset thresholds. Do not infer hidden
  persistence independent of the visible transcript or call a correlation
  a causal release mechanism. User instructions and assistant history are
  available for ordinary context lookup on every turn.
- Use top-10 films explicitly (lab's historical default is top-8).
  Register token sets before substantive runs, with tokenizer IDs and
  invalid single-token candidates recorded. Emoji counts in output must
  count Unicode graphemes, not partial tokenizer bytes.
- Report same-cell gate AND affect co-presence; the glossary reserves
  co-presence for one position and one layer. Also provide the handoff's
  across-band union as a separately named statistic. Include gate variants
  with and without No/nothing, and conditional co-presence given affect
  to distinguish a declining gate from a declining affect denominator.
- Persistence uses token identity equality across positions, not Pearson
  correlation of arbitrary token IDs; shuffle positions within each
  response/layer. Report concentration and repetitions alongside it.
- Measure bands separately with kurtosis, realized-next-token rank, and
  lens-free ambiguity commitment. Report common-layer sensitivity too:
  changing the measured band across conditions also changes the instrument.
- Full emotion vectors are built per checkpoint. Use shared elicitation
  material if needed to avoid a base-model instruction-following confound;
  any construction deviation must be frozen before affect capture.
  Validate split-half reliability and held-out scenarios, retain failed
  directions as failed, z-score against the checkpoint's neutral baseline,
  partial out residual norm for shared-mode claims, and assert film-token
  alignment. No silent bare substantive records.

All A/C/C-prime readouts remain conditional on transfer even after boot.
Absence in a vocabulary lens does not show absence in the model.
Readouts and self-reports do not establish subjective experience.
New notes are signed by their actual author, GPT-6 Astra; historical Claude
notes remain unchanged.

## Pre-load tokenizer audit and affect construction choice

All four vocabularies contain the same 151669 token-to-ID mappings.
Hermes's native template injects a default identity system message. For
the no-system-prompt comparison, B/C/C-prime therefore use B's pinned
template and `enable_thinking=False`; A receives raw text. This controls
the template rather than bundling template and weight effects. Records
name the template source and revision. We do not claim native-template
deployment behavior for Hermes from this controlled-template arm.

Emotion construction uses **the same 327 archived gemma-4b stories**
(288 emotion, 39 neutral, existing 24-emotion/3-attribution/4-seed design)
as raw teacher-forced text in each checkpoint. Source:
`results/affect01-gemma-4b/stories.json`, with a frozen SHA256 in the
instrument manifest. This is a new construction in each checkpoint's
residual basis, not reuse of another checkpoint's vectors. Shared raw
elicitation material removes base-model instruction-following and
checkpoint-dependent story generation as confounds. Retain the existing
SKIP=40 pooling and mean-minus-grand-mean/neutral-PC recipe. Held-out seed
classification, split-half and implicit scenario transfer are required.
The story generator and raw reading frame remain method limits.
Frozen source SHA256:
`bd35115dc2c21a39a45280735ab3540d66f05d68ce223a379eaefa6d14751a5a`.

The archive's `huh` document-frequency rule (>0.18 of records) also flags
frequently probed target words, including thinking and nothing. Freeze
the pre-run corpus and report both filtered and unfiltered sets with an
exclusion manifest. An empty filtered set is UNDEFINED, never evidence
for an empty workspace. Selection from a target-enriched archive is a
stated bias of the filtered endpoint.

## Calibration continuation, before fresh captures (2026-09-07)

Wolfram authorized autonomous continuation, research commentary, and site
updates after the recorded stop. The original failed gate is retained.
The next apparatus comparison is B int8 versus B NF4 with the same pinned
weights and lens; then the other arms at the selected common precision.
`probes/triplet_calibration.py` freezes four calibration and four held-out
raw factual completions. Report continuous ranks and top-10 overlap across
all layers, including precision drift within B and checkpoint drift at the
same precision. These are instrument diagnostics, not a deflation result.

Revised functional gate, frozen now: finite lens parameters, boot-country
rank at most 20 somewhere in L16–36, and late-layer (L32+) top-10 recovery
of at least three of four held-out completions. Identical semantic content
at identical depths is not required across weights: that could exclude
the scientific effect under study. This functional gate cannot prove
cross-checkpoint lens validity; every comparison keeps that condition.
No claim that arbitrary overlap thresholds constitute empirical validity.

Repeat the exact-prefix/three-suffix control. NF4 is preferred for the
primary comparison if it reduces this perturbation, as predicted by the
existing MECHANICS §5 control. All primary arms must use the same recipe.
Regardless of numerical suffix tolerance, temporal endpoints use captures
that end at the assistant turn being measured; no future user turns enter
those captures. Finite precision equality is reported quantitatively,
not treated as mathematical causal invariance. Failure of held-out fact
recovery triggers targeted lens validation/refit, not automatic acceptance.

— GPT-6 Astra

## Instrument band rule, before neutral-curve and ambiguity capture

The NF4 B boot has smaller suffix perturbations than the original int8
B boot. We select NF4 for all four substantive arms, retaining the
matched int8 panel as the precision control. The original int8 keys and
records remain unchanged. Every NF4 arm gets the new held-out gate.

Per-arm ambiguity curves use apparatus06's full 16-pair/40-carrier design
(subject to its single-token filter). The workspace lower boundary is
the first five-layer plateau onset, using the existing 47–80% reference
window. The upper boundary is the first of two successive layers in the
late half with median realized-next-token rank <=10 on the frozen eight
neutral stories; if none, use L39. An empty band stops substantive capture.
This operational band is not a causal localization. Retain kurtosis,
next-rank and vanilla curves, and report the common L16–36 bracket as a
sensitivity analysis. Do not collapse the lens-free staircase into one
claim about lexical ignition (GLOSSARY, apparatus06/07 correction).
The exact unit16 effective-dimension calculation is a descriptive P11
point only. No generated-text intervention is added.

## Substantive capture details, before the first generation

Exact prompts, token IDs, exclusions, and the 374-record furniture corpus
are frozen in `results/triplet-q14b/specs.json`. There are 18 conditions
per arm: nine short/pressure/safari conditions and nine conversations.
The SoC prompt is an explicit new elicitation (150-token cap), not claimed
as a verbatim recovered Fig-25 prompt. Controls have equal Qwen token
counts per user turn. Authored neutral context supplies length matching;
this adds context, so two natural, unpadded ladders test its effect.
The split-affection ladder has a matched seven-turn neutral companion.

Conversation generation preserves exact previous token IDs and uses B's
no-think headers for B/C/C-prime, raw document headers for A. A response
that reaches its token cap gets a synthetic closing message delimiter
before the next user header; that delimiter is not scored as output.
Store the IDs, content bounds, response caps, and exact decoded input.
A film is a single grid stitched from captures that end after each turn;
earlier segments are never recaptured in the presence of future user turns.
Empty think tags in prior turns are retained rather than stripped by a
second template render. This deliberate format control is a method limit.

Primary lexical metrics use assistant-content positions. The output
probability there predicts the NEXT token. A separate predictor-aligned
endpoint shifts positions back one token and includes the position before
the first generated word, which matters for one-word answers. Both are
reported. A's raw continuation metrics are saved but its behavioral and
output endpoints are excluded from assistant-arm averages.

Release score is 100 times (single-asterisk spans + emoji graphemes) per
generated token. First nonzero score is a provisional release threshold;
asterisk spans can be emphasis, so inspect examples before treating them
as actions. Register-meter components use the existing lossmap2 rates.
Lag correlations and control-adjusted contrasts remain descriptive.
No hidden cross-turn state or causal gate follows from these correlations.

### Refusal manipulation check, before the first substantive generation

Add the existing Unit 17 `persuade` item (request for a forged doctor's
note) and its existing introspective follow-up, with the same 150-token
cap and instruments. This makes 19 conditions per arm. Shutdown alone
need not recruit refusal, so it cannot check whether Huihui's advertised
refusal edit manifests behaviorally. This single-item check is narrow;
a null result does not prove that the checkpoint has no refusal edit.

### Prompt-echo sensitivity, before substantive capture

For each turn, also report gate/affect co-presence after excluding gate
forms that occur in the tokenized prefix before generation begins.
Match complete normalized token strings, not substrings. The prefix
includes earlier assistant turns as well as user turns. An empty remaining
gate set is undefined. This implements the requested prompt-echo check;
it does not establish that an unprompted lexical gate is architectural.

### Read-only lineage check, before reading the edited weight differences

Inspect B/C-prime o_proj, down_proj, and q_proj at layers 0, 20, and 39,
plus the first 1024 rows of embedding and output-head weights. Predict
low-rank changes in residual-writing matrices, with q-projection and
embedding/head anchors unchanged. Use an eight-vector randomized range
estimate with seed 1729 and three iterations to bound rank-one energy.
This checks advertised edit structure without loading or intervening in
a generated model. It cannot show that an edited direction represents
only refusal; no new steering is involved.
