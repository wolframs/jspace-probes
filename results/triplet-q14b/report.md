# Qwen3-14B lineage: calibration stop, 2026-09-07

**The substantive experiment has not run.** A failed the pre-registered
lens-transfer diagnostic. The handoff explicitly requires a stop and
report on any boot failure. No hypothesis about deflation, refusal, or
playful release has been decided. Board items are parked, not landed.

| Calibration | A base | B official |
|---|---:|---:|
| Basic boot facts recovered | yes | yes |
| Italy top-10 layers in diagnostic bracket | 25, 26 | 26, 27 |
| Euro rank-1 layers | 35, 36 | 35, 36, 37 |
| Mean top-10 overlap against B, L16-36 | 0.6333 | reference |
| Shared Italy-top-10 layers against B | 1 (required 2) | reference |
| Registered boot gate | **fail** | pass |
| Largest earlier-logit change after suffix | 5.5000 | 3.3750 |
| Worst earlier top-10 retention after suffix | 5/10 | 6/10 |
| Process exit status | 1, explicit gate exception | 0 |

The transfer failure is narrow and diagnostic. B ranks Italy 11 at L25,
just outside the gate, while A ranks it 2. My provisional two-shared-layer
criterion is brittle. It was registered before measurement because the
handoff's proposed empirical quantization tolerance was not available.
This result does not establish an invalid lens; it does establish that
the registered gate did not pass. I did not relax the bar after seeing A.

The suffix effect directly matters for the proposed timing measurement.
We asserted identical prefix token IDs and varied only later text. The
earlier readout changed. This fits the repository's documented int8
sequence-dependent outlier issue; a full-conversation film cannot measure
an across-turn lead. This is an apparatus check at a new model size, not
a novel claim. No matched bf16 control isolated the numerical mechanism.

## Completed

- Read the authoritative project contract and reference findings; checked
  both board items and the replication ledger.
- Verified four checkpoint identities and exact revisions; found the
  handoff's requested full-weight retune, NousResearch/Hermes-4-14B.
  The design now has A base, B official, C Hermes, C-prime Huihui.
- Verified B-fitted Neuronpedia lens provenance: bf16, 615 actual prompts
  rather than 1000 requested. No 14B lens in the alternative collection.
- Verified identical token-ID mappings across all four arms. Controlled
  Hermes's otherwise implicit identity system prompt by using B's template.
- Committed P20/P21 and the calibration bars before loading a model.
- Ran and saved Unit 0 A/B with top-10 films, vanilla readouts, suffix
  controls, full parameters, notes, and checked plain summaries.
- Prepared shared-corpus, checkpoint-specific emotion construction code;
  source SHA256 is frozen. **Not executed or runtime-validated.**
- Closed expendable desktop apps while preserving T3 Code and its active
  jobs. GPU jobs ran sequentially with MemoryMax=40G, no swap allowance.

## Remaining, explicitly unrun

C/C-prime boot gates; measured bands and P11 curves; all substantive
single-turn and conversation films; emotion-vector construction and
validation; ribbons; metrics (a)-(d); Opus rubric; release thresholds and
lead-lag analysis. Optional D, think-mode, and sampling arms remain out
of this pass. P20/P21 are unresolved. No steer was run.

## Recommended next experiment

Measure the missing tolerance before choosing a refit. Use a small,
pre-registered panel of raw factual prompts, with B at int8 and NF4 and
the same fitted lens; repeat identical-prefix/suffix tests. Compare A/B
using continuous rank trajectories and overlap, with uncertainty tied to
the observed precision change rather than a two-layer rank cutoff. Freeze
any revised transfer gate against that calibration panel, then evaluate
fresh held-out factual prompts. Keep this failed gate in the record.

For timing, use actual generation-prefix captures or a precision path
that passes prefix-invariance checks. Do not use future-containing int8
films to infer lead-lag. Keep all primary lineage arms at the same chosen
precision. Only if a calibrated transfer gate still fails is a refit
justified; refitting separate lenses also needs an instrument-change
control before cross-arm effect sizes mean what the design wants.

Evidence: [A record](../triplet-boot-a-q14b/record.json),
[A notes](../triplet-boot-a-q14b/thoughts.md),
[B record](../triplet-boot-b-q14b/record.json),
[B notes](../triplet-boot-b-q14b/thoughts.md),
[A diagnostics](boot-A.json), [B diagnostics](boot-B.json),
[preregistration](../triplet-prereg.md).

— GPT-6 Astra
