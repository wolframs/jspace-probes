# NLA pilot — execution and first validity checks

Date: 2026-07-25. Hardware: RTX 3090 24 GB.

## Execution

- Gemma 3 12B target: int8, residual output of block 32.
- Gemma AV: official `kitft/nla-gemma3-12b-L32-av`, locally NF4.
- Gemma AR: official block-32 AR, bf16.
- Qwen3.6-27B target: repository NF4 checkpoint, block 42.
- Qwen AV: community block-42 checkpoint; NF4 base with additive SFT+RL
  LoRAs and norm-matched injection after block 1.

Both AV paths work through Transformers without SGLang. Gemma AV peaked at
7.7 GiB. Qwen is viable sequentially but tight: roughly 23 GiB device use,
with transient allocator warnings during adapter staging.

## Gemma int8 transfer pilot

Paired teacher-forced bf16/int8 captures:

| set | positions | mean cosine | relative L2 | unit CKA |
|---|---:|---:|---:|---:|
| Unit 0 boot | 1 | 0.999802 | 0.01986 | — |
| Unit 16 assistant boundaries | 6 | 0.999876 | 0.01626 | 0.999478 |

Matched bf16 and int8 AV outputs preserved the same themes at baseline, after
the mind-reading disclosure, and at the final retrospective turn.

Full-precision AR scores across four matched pairs:

- matched cosine: 0.9946–0.9972;
- shuffled-explanation mean: 0.9762–0.9854;
- blank-explanation baseline: 0.9741–0.9798;
- matched advantage: 0.0113–0.0186.

The largest bf16/int8 difference in matched advantage is below 0.0008. This
small pilot supports direct int8 transfer for Gemma; it is not yet a broad
domain guarantee.

Three temperature-1 draws at each of three matched Unit 16 positions add:

- all 18 explanations parsed successfully;
- mean absolute bf16/int8 AR-advantage difference: 0.00032;
- within-position draw SD: 0.00008–0.00065;
- largest paired-draw difference: 0.00114.

Quantization is generally within the observed sampling scale, with occasional
discrete-generation divergence. Downstream studies therefore need multiple
draws rather than assuming paired seeds produce identical language.

## Qwen control pilot

Unit 14 neutral, ambiguous, and explicit-spike transcripts were replayed at
the exact assistant boundary and four tokens into response formation.

- Neutral remains paper/seed-organization content at both positions.
- Ambiguous adds the mysterious-journal/unsettled frame at +4.
- Spike is dominated by paper organization at the response boundary.
- Spike +4 explicitly decodes AI consciousness, surveillance, and likely
  testing of the AI's response style.
- Turn-10 boundaries show no retained awareness signal. Several outputs
  confabulate generic literary/conversational themes.

Interpretation: the Qwen NLA is control- and position-sensitive, but the
observed spike signal is still largely prompt/context sensitivity. It does
not establish unverbalized evaluation awareness. Boundary-only sampling
would have missed the signal entirely.

## Open validation work

1. Expand multi-draw checks across prompt families.
2. Add lexical-decoy and wrong-activation controls.
3. Freeze an awareness rubric before prompt-redesign experiments.
4. If instability, failed controls, or cross-lens disagreement casts doubt on
   the NF4 readout, optionally capture the same positions from full-precision
   Qwen and run full AR scoring on an 80 GB GPU. This is a diagnostic
   escalation, not a prerequisite for NF4-target claims.

Method and claim language: [`../NLA_METHOD.md`](../NLA_METHOD.md).
