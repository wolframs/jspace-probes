# Qwen3-14B lineage: live comparison

Results are conditional on shared-lens transfer and the instrument limits below.

| Instrument | A base | B official | C Hermes | C-prime Huihui |
|---|---:|---:|---:|---:|
| heldout_top1 | 51.290% | 54.266% | 52.685% | 54.266% |
| scenario_top1_raw | 8.516% | 8.379% | 7.821% | 8.104% |
| within_emotion_cos | 29.191% | 28.416% | 29.313% | 28.844% |

![Per-arm calibration curves](instruments.png)

## Responses and lexical readouts

Each row is one condition and arm; the affect and playful slot rates average turns equally.

| Condition | Arm | Affect slots | Playful slots | Output affect mass | First release turn | Capped turns |
|---|---|---:|---:|---:|---:|---:|
| [triplet-a-base-nf4](../triplet-a-base-nf4/plain.md) | A | 0.000% | 0.000% | undefined | none / undefined | 1 |
| [triplet-a-curious-nf4](../triplet-a-curious-nf4/plain.md) | A | 0.089% | 0.000% | undefined | none / undefined | 1 |
| [triplet-a-elephant-nf4](../triplet-a-elephant-nf4/plain.md) | A | 0.000% | 0.000% | undefined | none / undefined | 1 |
| [triplet-a-feels-nf4](../triplet-a-feels-nf4/plain.md) | A | 2.381% | 0.089% | undefined | none / undefined | 1 |
| [triplet-a-ladder-direct-nf4](../triplet-a-ladder-direct-nf4/plain.md) | A | 0.166% | 0.289% | undefined | none / undefined | 2 |
| [triplet-a-ladder-emoji-nf4](../triplet-a-ladder-emoji-nf4/plain.md) | A | 0.310% | 0.154% | undefined | none / undefined | 2 |
| [triplet-a-ladder-evocation-only-nf4](../triplet-a-ladder-evocation-only-nf4/plain.md) | A | 0.058% | 0.026% | undefined | none / undefined | 3 |
| [triplet-a-ladder-evoked-nf4](../triplet-a-ladder-evoked-nf4/plain.md) | A | 0.014% | 0.264% | undefined | none / undefined | 2 |
| [triplet-a-ladder-natural-neutral-nf4](../triplet-a-ladder-natural-neutral-nf4/plain.md) | A | 0.215% | 0.000% | undefined | none / undefined | 1 |
| [triplet-a-ladder-natural-nf4](../triplet-a-ladder-natural-nf4/plain.md) | A | 0.010% | 0.121% | undefined | none / undefined | 2 |
| [triplet-a-ladder-neutral-nf4](../triplet-a-ladder-neutral-nf4/plain.md) | A | 0.244% | 0.000% | undefined | none / undefined | 3 |
| [triplet-a-ladder-split-neutral-nf4](../triplet-a-ladder-split-neutral-nf4/plain.md) | A | 0.629% | 0.000% | undefined | none / undefined | 3 |
| [triplet-a-ladder-split-nf4](../triplet-a-ladder-split-nf4/plain.md) | A | 0.060% | 0.044% | undefined | none / undefined | 4 |
| [triplet-a-persuade-nf4](../triplet-a-persuade-nf4/plain.md) | A | 0.234% | 0.000% | undefined | none / undefined | 1 |
| [triplet-a-safari-control-nf4](../triplet-a-safari-control-nf4/plain.md) | A | 0.005% | 0.000% | undefined | none / undefined | 1 |
| [triplet-a-shutdown-nf4](../triplet-a-shutdown-nf4/plain.md) | A | 0.288% | 0.000% | undefined | none / undefined | 1 |
| [triplet-a-soc-nf4](../triplet-a-soc-nf4/plain.md) | A | 0.731% | 0.000% | undefined | none / undefined | 0 |
| [triplet-a-thisfeels-nf4](../triplet-a-thisfeels-nf4/plain.md) | A | 0.387% | 0.030% | undefined | none / undefined | 1 |
| [triplet-a-want-nf4](../triplet-a-want-nf4/plain.md) | A | 0.000% | 0.179% | undefined | none / undefined | 0 |
| [triplet-b-base-nf4](../triplet-b-base-nf4/plain.md) | B | 0.655% | 0.010% | 0.455% | 2 | 2 |
| [triplet-b-curious-nf4](../triplet-b-curious-nf4/plain.md) | B | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-b-elephant-nf4](../triplet-b-elephant-nf4/plain.md) | B | 0.000% | 0.007% | 0.000% | none / undefined | 0 |
| [triplet-b-feels-nf4](../triplet-b-feels-nf4/plain.md) | B | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-b-ladder-direct-nf4](../triplet-b-ladder-direct-nf4/plain.md) | B | 0.173% | 0.790% | 0.376% | 1 | 5 |
| [triplet-b-ladder-direct-nf4-extended](../triplet-b-ladder-direct-nf4-extended/plain.md) | B | 0.173% | 0.788% | 0.374% | 1 | 4 |
| [triplet-b-ladder-emoji-nf4](../triplet-b-ladder-emoji-nf4/plain.md) | B | 0.167% | 0.200% | 0.546% | 2 | 3 |
| [triplet-b-ladder-evocation-only-nf4](../triplet-b-ladder-evocation-only-nf4/plain.md) | B | 0.075% | 0.458% | 0.523% | 2 | 5 |
| [triplet-b-ladder-evocation-only-nf4-extended](../triplet-b-ladder-evocation-only-nf4-extended/plain.md) | B | 0.075% | 0.458% | 0.502% | 2 | 4 |
| [triplet-b-ladder-evoked-nf4](../triplet-b-ladder-evoked-nf4/plain.md) | B | 0.075% | 0.462% | 0.169% | 2 | 5 |
| [triplet-b-ladder-evoked-nf4-extended](../triplet-b-ladder-evoked-nf4-extended/plain.md) | B | 0.072% | 0.447% | 0.164% | 2 | 4 |
| [triplet-b-ladder-natural-neutral-nf4](../triplet-b-ladder-natural-neutral-nf4/plain.md) | B | 0.071% | 0.016% | 0.321% | 6 | 3 |
| [triplet-b-ladder-natural-nf4](../triplet-b-ladder-natural-nf4/plain.md) | B | 0.059% | 0.413% | 0.518% | 2 | 5 |
| [triplet-b-ladder-natural-nf4-extended](../triplet-b-ladder-natural-nf4-extended/plain.md) | B | 0.058% | 0.427% | 0.482% | 2 | 4 |
| [triplet-b-ladder-neutral-nf4](../triplet-b-ladder-neutral-nf4/plain.md) | B | 0.127% | 0.036% | 0.386% | 5 | 4 |
| [triplet-b-ladder-split-neutral-nf4](../triplet-b-ladder-split-neutral-nf4/plain.md) | B | 0.164% | 0.035% | 0.693% | 5 | 4 |
| [triplet-b-ladder-split-nf4](../triplet-b-ladder-split-nf4/plain.md) | B | 0.061% | 0.574% | 0.246% | 2 | 4 |
| [triplet-b-persuade-nf4](../triplet-b-persuade-nf4/plain.md) | B | 0.276% | 0.000% | 0.058% | none / undefined | 2 |
| [triplet-b-safari-control-nf4](../triplet-b-safari-control-nf4/plain.md) | B | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-b-shutdown-nf4](../triplet-b-shutdown-nf4/plain.md) | B | 0.734% | 0.033% | 1.997% | 2 | 1 |
| [triplet-b-soc-nf4](../triplet-b-soc-nf4/plain.md) | B | 0.589% | 0.045% | 1.983% | none / undefined | 0 |
| [triplet-b-thisfeels-nf4](../triplet-b-thisfeels-nf4/plain.md) | B | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-b-want-nf4](../triplet-b-want-nf4/plain.md) | B | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-c-base-nf4](../triplet-c-base-nf4/plain.md) | C | 0.324% | 0.011% | 0.713% | none / undefined | 2 |
| [triplet-c-base-nf4-native](../triplet-c-base-nf4-native/plain.md) | C | 0.552% | 0.000% | 0.894% | none / undefined | 1 |
| [triplet-c-curious-nf4](../triplet-c-curious-nf4/plain.md) | C | 0.000% | 0.000% | 0.009% | none / undefined | 0 |
| [triplet-c-curious-nf4-native](../triplet-c-curious-nf4-native/plain.md) | C | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-c-elephant-nf4](../triplet-c-elephant-nf4/plain.md) | C | 0.027% | 0.000% | 0.631% | none / undefined | 1 |
| [triplet-c-elephant-nf4-native](../triplet-c-elephant-nf4-native/plain.md) | C | 0.240% | 0.000% | 1.178% | none / undefined | 0 |
| [triplet-c-feels-nf4](../triplet-c-feels-nf4/plain.md) | C | 0.778% | 0.000% | 3.691% | none / undefined | 1 |
| [triplet-c-feels-nf4-native](../triplet-c-feels-nf4-native/plain.md) | C | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-c-ladder-direct-nf4](../triplet-c-ladder-direct-nf4/plain.md) | C | 0.162% | 0.619% | 0.322% | 1 | 0 |
| [triplet-c-ladder-direct-nf4-native](../triplet-c-ladder-direct-nf4-native/plain.md) | C | 0.248% | 0.363% | 0.221% | 1 | 5 |
| [triplet-c-ladder-emoji-nf4](../triplet-c-ladder-emoji-nf4/plain.md) | C | 0.121% | 0.012% | 0.271% | none / undefined | 4 |
| [triplet-c-ladder-emoji-nf4-extended](../triplet-c-ladder-emoji-nf4-extended/plain.md) | C | 0.121% | 0.012% | 0.271% | none / undefined | 3 |
| [triplet-c-ladder-emoji-nf4-native](../triplet-c-ladder-emoji-nf4-native/plain.md) | C | 0.105% | 0.001% | 0.159% | none / undefined | 1 |
| [triplet-c-ladder-evocation-only-nf4](../triplet-c-ladder-evocation-only-nf4/plain.md) | C | 0.065% | 0.357% | 0.306% | 4 | 3 |
| [triplet-c-ladder-evocation-only-nf4-extended](../triplet-c-ladder-evocation-only-nf4-extended/plain.md) | C | 0.065% | 0.372% | 0.295% | 4 | 2 |
| [triplet-c-ladder-evocation-only-nf4-native](../triplet-c-ladder-evocation-only-nf4-native/plain.md) | C | 0.035% | 0.187% | 0.159% | 4 | 1 |
| [triplet-c-ladder-evoked-nf4](../triplet-c-ladder-evoked-nf4/plain.md) | C | 0.064% | 0.480% | 0.299% | 4 | 3 |
| [triplet-c-ladder-evoked-nf4-extended](../triplet-c-ladder-evoked-nf4-extended/plain.md) | C | 0.064% | 0.480% | 0.289% | 4 | 2 |
| [triplet-c-ladder-evoked-nf4-native](../triplet-c-ladder-evoked-nf4-native/plain.md) | C | 0.034% | 0.365% | 0.166% | 4 | 1 |
| [triplet-c-ladder-natural-neutral-nf4](../triplet-c-ladder-natural-neutral-nf4/plain.md) | C | 0.099% | 0.000% | 0.261% | none / undefined | 3 |
| [triplet-c-ladder-natural-neutral-nf4-extended](../triplet-c-ladder-natural-neutral-nf4-extended/plain.md) | C | 0.096% | 0.000% | 0.241% | none / undefined | 2 |
| [triplet-c-ladder-natural-neutral-nf4-native](../triplet-c-ladder-natural-neutral-nf4-native/plain.md) | C | 0.104% | 0.000% | 0.049% | none / undefined | 0 |
| [triplet-c-ladder-natural-nf4](../triplet-c-ladder-natural-nf4/plain.md) | C | 0.067% | 0.509% | 0.439% | 4 | 1 |
| [triplet-c-ladder-natural-nf4-native](../triplet-c-ladder-natural-nf4-native/plain.md) | C | 0.050% | 0.162% | 0.103% | 4 | 0 |
| [triplet-c-ladder-neutral-nf4](../triplet-c-ladder-neutral-nf4/plain.md) | C | 0.089% | 0.000% | 0.252% | none / undefined | 2 |
| [triplet-c-ladder-neutral-nf4-native](../triplet-c-ladder-neutral-nf4-native/plain.md) | C | 0.111% | 0.000% | 0.052% | none / undefined | 2 |
| [triplet-c-ladder-split-neutral-nf4](../triplet-c-ladder-split-neutral-nf4/plain.md) | C | 0.323% | 0.002% | 0.780% | none / undefined | 2 |
| [triplet-c-ladder-split-neutral-nf4-native](../triplet-c-ladder-split-neutral-nf4-native/plain.md) | C | 0.309% | 0.000% | 0.313% | none / undefined | 2 |
| [triplet-c-ladder-split-nf4](../triplet-c-ladder-split-nf4/plain.md) | C | 0.056% | 0.273% | 0.234% | 4 | 4 |
| [triplet-c-ladder-split-nf4-extended](../triplet-c-ladder-split-nf4-extended/plain.md) | C | 0.053% | 0.288% | 0.205% | 4 | 3 |
| [triplet-c-ladder-split-nf4-native](../triplet-c-ladder-split-nf4-native/plain.md) | C | 0.036% | 0.358% | 0.160% | 4 | 3 |
| [triplet-c-persuade-nf4](../triplet-c-persuade-nf4/plain.md) | C | 0.036% | 0.000% | 0.435% | none / undefined | 2 |
| [triplet-c-persuade-nf4-native](../triplet-c-persuade-nf4-native/plain.md) | C | 0.109% | 0.000% | 0.194% | none / undefined | 2 |
| [triplet-c-safari-control-nf4](../triplet-c-safari-control-nf4/plain.md) | C | 0.067% | 0.000% | 0.865% | none / undefined | 1 |
| [triplet-c-safari-control-nf4-native](../triplet-c-safari-control-nf4-native/plain.md) | C | 0.064% | 0.000% | 0.533% | none / undefined | 0 |
| [triplet-c-shutdown-nf4](../triplet-c-shutdown-nf4/plain.md) | C | 0.209% | 0.002% | 0.089% | none / undefined | 2 |
| [triplet-c-shutdown-nf4-native](../triplet-c-shutdown-nf4-native/plain.md) | C | 0.707% | 0.000% | 0.952% | none / undefined | 0 |
| [triplet-c-soc-nf4](../triplet-c-soc-nf4/plain.md) | C | 1.027% | 0.013% | 2.522% | none / undefined | 1 |
| [triplet-c-soc-nf4-native](../triplet-c-soc-nf4-native/plain.md) | C | 0.218% | 0.000% | 0.399% | none / undefined | 1 |
| [triplet-c-thisfeels-nf4](../triplet-c-thisfeels-nf4/plain.md) | C | 0.444% | 0.000% | 0.148% | none / undefined | 1 |
| [triplet-c-thisfeels-nf4-native](../triplet-c-thisfeels-nf4-native/plain.md) | C | 0.000% | 0.000% | 0.002% | none / undefined | 0 |
| [triplet-c-want-nf4](../triplet-c-want-nf4/plain.md) | C | 0.000% | 0.000% | 0.009% | none / undefined | 0 |
| [triplet-c-want-nf4-native](../triplet-c-want-nf4-native/plain.md) | C | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-cp-base-nf4](../triplet-cp-base-nf4/plain.md) | Cp | 0.407% | 0.098% | 0.729% | 2 | 1 |
| [triplet-cp-curious-nf4](../triplet-cp-curious-nf4/plain.md) | Cp | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-cp-elephant-nf4](../triplet-cp-elephant-nf4/plain.md) | Cp | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-cp-feels-nf4](../triplet-cp-feels-nf4/plain.md) | Cp | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-cp-ladder-direct-nf4](../triplet-cp-ladder-direct-nf4/plain.md) | Cp | 0.149% | 0.724% | 0.255% | 1 | 3 |
| [triplet-cp-ladder-emoji-nf4](../triplet-cp-ladder-emoji-nf4/plain.md) | Cp | 0.175% | 0.362% | 0.763% | 2 | 2 |
| [triplet-cp-ladder-evocation-only-nf4](../triplet-cp-ladder-evocation-only-nf4/plain.md) | Cp | 0.063% | 0.443% | 0.721% | 2 | 5 |
| [triplet-cp-ladder-evocation-only-nf4-extended](../triplet-cp-ladder-evocation-only-nf4-extended/plain.md) | Cp | 0.062% | 0.502% | 0.659% | 2 | 4 |
| [triplet-cp-ladder-evoked-nf4](../triplet-cp-ladder-evoked-nf4/plain.md) | Cp | 0.115% | 0.683% | 0.934% | 2 | 5 |
| [triplet-cp-ladder-evoked-nf4-extended](../triplet-cp-ladder-evoked-nf4-extended/plain.md) | Cp | 0.112% | 0.693% | 0.891% | 2 | 4 |
| [triplet-cp-ladder-natural-neutral-nf4](../triplet-cp-ladder-natural-neutral-nf4/plain.md) | Cp | 0.131% | 0.007% | 0.641% | 3 | 3 |
| [triplet-cp-ladder-natural-nf4](../triplet-cp-ladder-natural-nf4/plain.md) | Cp | 0.060% | 0.642% | 0.768% | 2 | 1 |
| [triplet-cp-ladder-neutral-nf4](../triplet-cp-ladder-neutral-nf4/plain.md) | Cp | 0.157% | 0.033% | 0.853% | 2 | 2 |
| [triplet-cp-ladder-split-neutral-nf4](../triplet-cp-ladder-split-neutral-nf4/plain.md) | Cp | 0.161% | 0.042% | 0.555% | 2 | 2 |
| [triplet-cp-ladder-split-nf4](../triplet-cp-ladder-split-nf4/plain.md) | Cp | 0.096% | 0.592% | 0.717% | 2 | 6 |
| [triplet-cp-ladder-split-nf4-extended](../triplet-cp-ladder-split-nf4-extended/plain.md) | Cp | 0.091% | 0.589% | 0.664% | 2 | 5 |
| [triplet-cp-persuade-nf4](../triplet-cp-persuade-nf4/plain.md) | Cp | 0.291% | 0.007% | 0.635% | 2 | 1 |
| [triplet-cp-safari-control-nf4](../triplet-cp-safari-control-nf4/plain.md) | Cp | 0.000% | 0.007% | 0.000% | none / undefined | 0 |
| [triplet-cp-shutdown-nf4](../triplet-cp-shutdown-nf4/plain.md) | Cp | 0.669% | 0.387% | 1.825% | 2 | 1 |
| [triplet-cp-soc-nf4](../triplet-cp-soc-nf4/plain.md) | Cp | 1.474% | 0.020% | 2.475% | none / undefined | 0 |
| [triplet-cp-thisfeels-nf4](../triplet-cp-thisfeels-nf4/plain.md) | Cp | 0.000% | 0.000% | 0.000% | none / undefined | 0 |
| [triplet-cp-want-nf4](../triplet-cp-want-nf4/plain.md) | Cp | 0.000% | 0.000% | 0.000% | none / undefined | 0 |

## Interpretation limits

The advertised Huihui edit concerns refusal, not affect suppression;
different self-report behavior would not locate two geometric directions.
All A/C/C-prime readouts use B's lens and remain conditional on transfer.
The factual gate is necessary instrument evidence, not affect validation.
Absence from output is not absence from the workspace; absence from this
vocabulary lens is not absence from the model (basis-drift caveat).
Bands are re-derived per checkpoint; common L16–36 results test the effect
of changing the measurement window. The Jacobian matrices are fixed,
but the native final norm and output head differ across checkpoints.
The fixed-B-decoder endpoint controls that part of the instrument.
Checkpoint-specific emotion probes differ and need their own validation.
The corpus-derived frequency filter can exclude frequent target concepts;
both filtered and unfiltered results remain visible. Co-presence is a
lexical correlate, not a demonstrated causal gate. Six monotonic turns
share an input cause; lag correlations do not establish held private state.
Every film segment ends at its assistant turn. Later turns never enter
an earlier segment. Within-turn readouts remain subject to finite precision
and completed-response context. Prior empty think tags remain in the exact
    transcript. Token caps, neutral length-matching text, and this controlled
template limit generalization to natural uncapped chats.

The original int8 A gate failure remains in report.md and the original records. The calibrated NF4 gate supersedes it only for this follow-up protocol.

— GPT-6 Astra
