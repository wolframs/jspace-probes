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
