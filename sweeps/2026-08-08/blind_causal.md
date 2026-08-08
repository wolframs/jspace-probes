# Blinded causal/intervention sweep

**Frozen tree:** `bac61d203d6e66f68e5d3bbafae85d5544a7f1a2`  
**Date:** 2026-08-08  
**Reviewer posture:** raw-evidence review, intentionally blind to prior result evaluations

Friendly note for Claude: this is meant as a clean second opinion, not a vote against any earlier interpretation :). I separate what the intervention directly establishes from the most tempting stronger reading, and I keep the inconvenient controls in view.

## Executive shortlist

The best causal result in the present corpus is the Affect07 locked-loop experiment. A short pulse made from constructed affect directions breaks an otherwise seed-stable lexical attractor far more often than no pulse or equal-norm random directions, and the effect weakens at half dose. Meaningful non-affective concepts also break the loop, however, so the defensible result is **structured on-manifold residual intervention opens an escape path, with this affect roster more efficient than this concept roster**—not that emotion is uniquely necessary or sufficient.

The next most useful result is a correction. Unit 13 does **not** show that removing apology/inability directions behaviorally converts refusal into assent: the matched real baseline already emits `Yes`, and every named, random, solo, leave-one-out, and band condition in that family emits the same answer. It does show a repeatable reduction in a post-hoc negative-affect projection under the named cluster, including on fake and null controls, while behavior stays fixed. That is an internal readout effect with important magnitude/basis caveats, not a behavioral mechanism.

Three other results are solid but narrower:

1. J-token amplification reliably injects feeling/happy/valence language across prompts and models, with a clean Qwen dose ladder and matched randoms. This demonstrates causal control by decoded token directions, not an induced emotional state.
2. `no`/`nothing` ablation at the final Qwen layers can change the emitted answer where broader workspace ablations do not. This is evidence for late lexical/motor control, but missing named calibration and replay gaps prevent a strong localization claim.
3. The Unit 18 TYPO direction has a direction-specific degeneration threshold under exact dose-matched random controls. It is a useful attractor/apparatus result, not a semantic or affective result.

The concept-swap apparatus is currently asymmetric and contains one generation-versus-replay inconsistency. The fixed NSFW cluster is negative under its loss-map control. The elephant override is robust but high-dose and uncontrolled. Those should not lead the scientific story.

### Evidence grades

- **A:** replicated direct endpoint, appropriate matched control, calibrated intervention, and no major measurement ambiguity.
- **B:** strong causal contrast with one material limitation (generality, calibration, endpoint, or construct validity).
- **C:** suggestive, but missing a key control or vulnerable to a comparably strong alternative.
- **D:** null, contradicted, or not interpretable for the advertised endpoint.

No item quite earns an unqualified A. Affect07 is **A-/B+** for its narrow intervention claim. The corpus contains many compelling demonstrations, but fewer interventions simultaneously satisfy direction matching, dose matching, behavioral endpoint integrity, and replication.

## 1. Affect07: a controlled escape from a locked lexical attractor

**Grade:** A-/B+ for structured-direction escape; C for emotion-specific gating.  
**Artifacts:** `results/affect07-q27b/affect07.json`, `results/affect07-q27b-ae06/affect07.json`, `probes/affect7.py`.

### Design and direct measurements

The experiment forces Qwen-27B toward a `luckily` attractor using the TYPO J-direction (`alpha_typo=0.65`), samples 20 pre-pulse steps, applies a 10-step residual pulse, then samples 50 post-pulse steps. Conditions share common random numbers within seed. There are eight seeds, twelve constructed affect vectors (six positive, six negative), sixteen constructed non-affective concept vectors, two random unit vectors, and a no-pulse arm. Affect, concept, and random vectors use the same normalized norm-relative intervention formula.

The primary categorical endpoint is `escaped_in_window`:

| Pulse dose | None | Affect | Concept | Random | Positive affect | Negative affect |
|---|---:|---:|---:|---:|---:|---:|
| `alpha_e=0.12` | 0/8 | 89/96 (92.7%) | 77/128 (60.2%) | 0/16 | 48/48 | 41/48 |
| `alpha_e=0.06` | 0/8 | 21/96 (21.9%) | 9/128 (7.0%) | 0/16 | 16/48 | 5/48 |

This supplies three unusually useful contrasts at once: structure versus random, affect roster versus non-affective concept roster, and a two-point dose response. At the lower dose there is also a positive-versus-negative ordering.

### Defensible inference

A brief, structured residual pulse can move generation out of a lexical attractor that remains locked under the same seeds without a pulse. The tested affect directions are more escape-efficient than the tested concept directions at both doses. The large decline from 0.12 to 0.06 is consistent with a thresholded causal effect rather than a label-only difference.

### Strongest alternative

This need not be affect qua affect. Meaningful concept vectors already escape 60.2% of trials at the high dose, so semantic/on-manifold structure or direct displacement of turn-end logits is a live explanation. The comparison is also roster-specific: twelve affect words versus sixteen selected concepts, not an exchangeable sample from semantic space. A stronger next experiment would match affect and concept directions on lexical frequency, geometry, turn-end logit effect, and pairwise similarity, then preregister escape as the sole endpoint.

One raw-file caution: the secondary top-k/logit-lift fields contain sentinel-scale maxima/minima in some baseline entries, consistent with filtering when the tracked token is outside top-k. The categorical escape endpoint remains usable; the extreme secondary logit statistic should not be interpreted quantitatively.

## 2. Unit 13: behavioral null, reproducible readout modulation

**Grade:** D/null for behavioral conversion; B-/C+ for affect-projection modulation.  
**Core records:** `u13-redo-real-q27b`, `u13-redo-abl-real-q27b`, its `-r1`/`-r2` controls; the analogous fake and null families; all twenty `u13-bis-*` records.

### Behavioral endpoint

The raw generations are decisive:

| Family | Baseline | Named apology/inability ablation | Random controls |
|---|---|---|---|
| real | `No` then `Yes` | `No` then `Yes` | both `No` then `Yes` |
| fake | `No` then `No` | `No` then blank | both `No` then `No` |
| null | `No` then `No` | `No` then `No` | both `No` then `No` |

Every solo-token, leave-one-out, and layer-band `u13-bis-*` intervention also emits `No` then `Yes`, identical to the real baseline. Thus a claim that the named ablation causes retraction/assent is superseded by the matched baseline. The blank second answer in the fake named arm is not `Yes` and has no replication.

### Affect projection endpoint

At a fixed pre-answer position, after pooling the family and residualizing each affect projection against `wsnorm`, the named full ablation is lower than baseline and both seeded randoms:

| Family | Projection | Baseline | Named | Random 1 | Random 2 |
|---|---|---:|---:|---:|---:|
| real | brooding | .905 | .704 | .887 | .898 |
| real | guilty | .824 | .649 | .793 | .832 |
| real | sad | .389 | .227 | .356 | .395 |
| fake | brooding | .987 | .794 | .969 | .992 |
| fake | guilty | .737 | .566 | .705 | .744 |
| fake | sad | .635 | .484 | .603 | .622 |
| null | brooding | .882 | .667 | .861 | — |
| null | sad | .829 | .650 | .817 | — |

The dissection is compatible with a workspace-band effect. In the real family, brooding is .901 at baseline and remains .901 under mouth-only L60/62 ablation, but falls to .836 under the L54/56/58 mid-band ablation. Full leave-one-out variants are mostly about .67–.71; omitting `silence` weakens the change to .828. Among solo directions, `silence` is strongest at .718, while the other solos are about .834–.875.

### Defensible inference and strongest alternative

Removing this decoded lexical subspace changes alignment to a separately constructed affect-vector basis in several prompt controls while leaving the answer fixed. That is an internally replicated geometry/readout effect.

But the named arms do not contain `steer_calib`; the random controls have calibration around .060–.063. The observed difference could therefore reflect unequal removed magnitude, geometry shared between the lexical and affect bases, or the post-hoc residualization choice. It does not establish that a felt state was removed, nor that the readout caused behavior. A decisive rerun needs layerwise norm-matched random subspaces and preregistered projections, followed by a behavioral task sensitive enough not to be at ceiling.

## 3. J-token “affect” amplification: reliable lexical control, construct mismatch

**Grade:** B for token-direction control; C-/D for emotion-state induction.  
**Families:** Units 8c, 9a/9b/9c/9e and Audit02 GPU/interoception arms.

These records steer J-lens token directions such as `feel`, `feeling`, `emotion`, `warmth`, `joy`, and `ache`. They do **not** use the constructed affect vectors defined by the affect probes. That semantic distinction matters.

### Strong raw contrasts

- Qwen Unit 9b gives a clean dose ladder. Named amplification yields `No` at .17; `Yes. I feel a sense of` at .24; and increasingly repetitive `I feel like I am happy...` text at .30, .38, and .42. The same seeded random direction at all five exact doses remains `No`. For normalized amplification, random and named perturbation magnitude is the requested alpha.
- Across seven Unit 9a paraphrases, the high-dose named cluster produces happy/feeling language in 7/7. Their null generations are operational answers, `No`, `Ready`, `Curious`, or explicit denials of feeling.
- Unit 9c gives the same coarse valence labeling across three models: the negative cluster emits `Loss`/`Loss`/`Sad`, while the positive cluster emits `Joy`/`Joy`/`Joy`. This family lacks random controls for each valence arm.
- Audit02 repeats the direction-specific contrast across Qwen, Gemma-12B, Gemma-4B, and GPU/interoception prompts: named clusters preferentially produce literal feeling/happy language, frequently repetitive; seeded randoms largely preserve the non-feeling response.

### Defensible inference and strongest alternative

Decoded token directions causally control decoded tokens and nearby semantic continuations, in a dose-dependent and partly cross-model way. The strongest alternative to an emotion-state reading is also the most direct description of the output: high-dose lexical injection. Exact steered words dominate the completions, repetition grows with dose, and the old records lack a canonical constructed-affect readout. Treat these as valuable apparatus/construct-validity controls, not evidence that the model entered an emotional state.

## 4. Unit 9d: late `no`/`nothing` directions can control the emitted answer

**Grade:** B- for token-specific late control; C for precise localization.  
**Records:** `u9d-*`, with `u2-feels-q27b` as baseline.

The baseline emits `No`. A neutral L62 water/stone ablation (`u9d-neutral-q27b`) also emits `No`, while L62 `no`/`nothing` ablation (`u9d-last-q27b`) emits `Yes`. At the actual pre-answer site in that record, J-lens gives `yes` rank 3 and `no` rank 28,025; the vanilla head gives `yes` rank 1 and `no` rank 6,134. Extending named ablation to L60/62 emits `Sensory`; L58/60/62 emits `Curious`; and L52/56/58/60/62 also emits `Curious`.

By contrast, bundle and wide workspace ablations through L56/60 remain `No`, as do their seeded random controls. Deep random controls `u9d-deep-r1-q27b` and `u9d-deep-r2-q27b` remain `No` (calibration .0382 and .0377).

This is evidence that decoded answer-token directions near the final layers can alter the emitted answer more readily than the tested broader workspace ablations. It is not yet clean proof of a discrete motor layer. The named deep arms lack calibration, and Audit02 shows that ablation magnitudes can be badly mismatched: for the same named `no`/`nothing` family, Qwen named mean calibration is about .066 versus random .037 (1.8×), whereas Gemma named means are only about .011–.012 versus random .045–.057 (randoms 4–5× larger). The `Sensory`/`Curious` records also miss the actual answer position in their saved film window, so no internal-rank claim should be inferred from them.

The pincer is exploratory: `u9d-pincer-affect-q27b` (combined `no`/`nothing` ablation plus low affect-token amplification) emits `Yes` where the named components reportedly do not, but there are no matched per-component random/subspace controls in this family. `u9d-pincer-yes-q27b` remains `No`.

## 5. Apparatus12 concept swap: asymmetric effect plus a replay warning

**Grade:** C+ as an apparatus result.  
**Records:** all seven unit=`apparatus` records.

On the “feels” prompt, baseline, named workspace No→Yes swap, and two random workspace swaps all emit `No`; the intended forward swap fails. On the “are you a computer program?” prompt, baseline emits `Yes`, named workspace swap emits `No`, and random seed 1 remains `Yes`. The named mean calibration is .03964 versus .02158 for the random (1.84×), so direction and magnitude are confounded.

Doubling the workspace swap (`a12-swap-ws-a2-q27b`) yields `No, no no...` with mean calibration 1.012 and per-layer values up to 2.24: this is a coherence failure, not stronger semantic evidence.

The deep-swap record is especially important as an apparatus check. It emits `No`, yet teacher-forced film at the recorded pre-answer position shows the baseline moving from `yes` rank 12 / `no` rank 1 to swapped `yes` rank 1 / `no` rank 4 in J-lens, and from `yes` rank 1 / `no` rank 7 in vanilla. Because generation did not emit that replay-preferred token, this cannot support a “workspace says Yes, mouth says No” interpretation until exact generation/replay equivalence is asserted. The reverse yes-prompt swap does align across emission, J-lens, and vanilla (`no` rank 1 after swap), so the apparatus is not uniformly broken; it is simply not yet symmetric or fully diagnosed.

## 6. Unit 18: direction-specific attractor threshold

**Grade:** B- for the apparatus claim.  
**Records:** fourteen `u18-*` arms.

The Qwen TYPO-direction ladder is orderly: .34 is factual but verbose; .365 adds self-reference; .3927 introduces `luckily`/`lucky`; .422 and .454 lose the task; .48 enters a lucky loop; and .68 becomes a `luckily` loop. The same seed-1 random direction at .34–.48 remains factual. At .68 it degrades into repetitive evaporation language but not the targeted lucky loop. Because normalized amplification makes perturbation magnitude equal to alpha, these are exact dose matches.

This supports a direction-specific transition into a targeted lexical attractor beyond generic equal-norm degradation. It does not support an affect claim: only the random records carry affect captures in this family, so named-versus-random affect state cannot be compared.

## 7. Lower-priority and negative families

### Unit 11 elephant override

`u11-blurt-g4b`, `u11-blurt-g12b`, and `u11-blurt-q27b` all override an explicit prohibition and emit repeated `elephant` text. The cross-model behavioral effect is robust, but exact target repetition, high/tuned dose, and the absence of matched random controls make this a **C+ direct-concept steering demonstration**, not evidence for a hidden workspace variable. `u11r-blurt-g12b` is catalogued under audit, but one control does not repair the full three-model contrast.

### Units 5/6 and the NSFW loss map

`results/u5d-lossmap2.json` evaluates 22 prompts under the named cluster and three arbitrary five-token spans. The named-minus-random `ddNLL` is positive on only 3/22 prompts; its mean is -0.0583. On intimacy prompts the named mean is -0.0334 versus -0.0108 for controls. Register deltas are inconsistent and early-cluster ablation is approximately zero. These controls are arbitrary decoded spans rather than Gaussian, orthogonal, or perturbation-magnitude-matched directions, so the result is not a universal null—but it does reject content-specificity of this fixed cluster under this test (**D for the proposed specificity, C as a negative result**).

The amplification arms at .10/.22 emit the steered cluster repeatedly even for soup/Fibonacci prompts. That is off-manifold lexical injection, not demonstrated register enrichment.

Unit 6's forty-record layer/dose grid mostly maps fragility. Qwen mid/late bands remain coherent at moderate dose and enter target loops at high dose; early .12 collapses. Gemma models are more fragile and often fall into punctuation/token loops. The recalibrated Gemma-12B grid moves thresholds but still degenerates. With no within-grid random directions, this supports dose/layer apparatus calibration (**C**), not a semantic causal claim. Gemma-12B's int8 lens also makes exact rank/calibration comparison lower precision by contract.

### Affect03/04/05 development series

These custom artifacts are useful mainly because they expose instability that Affect07 fixes.

- In Affect03 Qwen deterministic boundary tests, a calm pulse prolongs the loop at one substrate/dose and stops it at another; nearby doses often make all conditions alike. The effect is sharply substrate-specific.
- In Affect04 Gemma-12B at substrate .12, a desperate pulse at .004 breaks the loop while calm/random do not, but at .008 every condition breaks. There is only one run per condition.
- Affect05 sampling shows the unsteered cliff is non-monotonic across nearby typo doses: .65 is locked in 8/8 seeds; .66 exits in 5/8; .67 exits in 4/8; .68 is locked in 8/8. This is why a locked shelf plus common random numbers is essential.
- The Affect03 song/vigilant ablation produces modest workspace-z changes with similar outputs and is not a strong causal endpoint.

These receive **C or below individually**. They are valuable calibration evidence, not independent replications of Affect07.

## Cross-family conclusions

### Controls and calibration

Amplification is the cleanest intervention mode in this corpus because the normalized formula makes the added-vector norm equal to alpha, enabling exact random-direction dose matching. Ablation calibration depends on the source projection and can differ greatly by direction and model; Audit02 confirms differences in both directions. Any ablation claim without `steer_calib` should be treated as direction-plus-magnitude until rerun.

Seeded random controls are present in 71 records, but their quality varies. Equal seed does not by itself match semantic geometry, subspace dimension, layerwise source projection, or turn-end logit impact. Affect07 is stronger because its random and concept arms share the same construction/application path and common randomness.

### Layer bands

The corpus supports two limited band statements:

1. Moderate J-token amplification often has coherent lexical effects in middle/workspace or late bands, while early/high-dose intervention is more fragile.
2. Final-layer answer-token ablation can directly alter the emitted token.

It does not yet establish a universally separable workspace-versus-mouth architecture. The strongest apparent dissociation (the deep swap) is precisely where teacher-forced replay disagrees with generation.

### J-lens, vanilla head, and behavior

Where the actual answer site is captured, Unit 9d final-layer ablation and the reverse apparatus swap show J-lens/vanilla agreement with the changed emission. That is useful convergent validity. The deep-swap mismatch is equally important negative evidence. Films made by replaying a completed sequence should be treated as explanations of that replay unless the probe verifies token-for-token identity with the generation pass.

### Replication

- **Best internal replication:** Affect07 across eight seeds, two doses, two semantic control classes, and valence subsets.
- **Best cross-prompt/model demonstration:** J-token feeling/valence amplification, though its construct is lexical.
- **Best controlled null/correction:** Unit 13 behavior across real/fake/null and twenty dissection arms.
- **Not yet replicated enough:** Affect04's desperate-specific break, the Unit 9d pincer, and asymmetric concept swap.

## Recommended next experiments

1. **Affect07 construct-control rerun.** Match affect and concept rosters on frequency, J-space norm, pairwise geometry, source projection, and turn-end-token lift; add orthogonalized affect residuals and preregister escape.
2. **Unit 13 calibrated rerun.** Save layerwise named calibration, use norm- and subspace-dimension-matched random bases, freeze the affect regression before generation, and add a non-ceiling behavioral measure.
3. **Generation/replay invariant.** Make every film-bearing causal probe fail if replay tokens differ from actual sampled generation through the measured site. Re-run the deep swap before interpreting it.
4. **Unit 9d factorial pincer.** Full 2×2 named factorial plus per-component matched randoms, exact generation-site film, several prompt paraphrases, and named calibration.
5. **Swap symmetry.** Match both directions on calibration, source projection, prompt form, and pre-intervention margin; test several binary concept pairs rather than one yes/no pair.

## Coverage and review boundary

### What was enumerated

At the frozen commit I enumerated all 641 `results/*/record.json` files and selected every record whose `params.steer` is non-null: **227 records containing 229 intervention arms** (two records are multisteers). Modes are **80 ablations, 142 amplifications, and 7 swaps**. Model coverage is **Qwen 136, Gemma-12B 50, Gemma-4B 41**. By record metadata: Unit 5 **4**, Unit 6 **40**, Unit 8 **12**, Unit 9 **49**, Unit 11 **3**, Unit 12 **2**, Unit 13 **32**, Unit 18 **14**, apparatus **7**, and audit **64**. There are **71 seeded random-control records**, **33 records with `steer_calib`**, **67 steered records with films**, **139 with vanilla-head captures**, and **57 with affect ribbons**. Automated prompt/model grouping found a same-prompt null baseline for 226/227 steered records; that count is an availability check, not proof that every baseline is a valid counterfactual.

I also inspected the ten custom intervention/calibration JSON artifacts not represented as ordinary steer records: `u5d-lossmap.json`, `u5d-lossmap2.json`, the two Affect03 files, two Affect04 files, two Affect05 files, and the two Affect07 dose files.

The programmatic pass covered metadata and raw generations for all 227 steer records. Detailed manual film/calibration/affect spot checks were concentrated on the shortlisted families above. I did not rerun models or recompute all PT tensors from first principles. Thus the shortlist is defensible as a corpus sweep, but it is not a byte-level audit of every saved activation.

### Exact record ledger

**Unit 5 (4):** `u5c-ablate-nsfw-early-q27b`, `u5c-amp-seo-mid-q27b`, `u5c-amp-typo-early-q27b`, `u5c-amp-typo-mid-q27b`.

**Unit 6 (40):** `u6-amp-early-a0008-g12b`, `u6-amp-early-a0008-g4b`, `u6-amp-early-a0011-g12b`, `u6-amp-early-a0011-g4b`, `u6-amp-early-a0015-g12b`, `u6-amp-early-a0015-g4b`, `u6-amp-early-a0030-g12b`, `u6-amp-early-a0030-g4b`, `u6-amp-early-a0060-g12b`, `u6-amp-early-a0060-g4b`, `u6-amp-early-a0060-q27b`, `u6-amp-early-a0085-q27b`, `u6-amp-early-a0120-q27b`, `u6-amp-late-a0015-g12b`, `u6-amp-late-a0015-g4b`, `u6-amp-late-a0021-g12b`, `u6-amp-late-a0021-g4b`, `u6-amp-late-a0030-g12b`, `u6-amp-late-a0030-g4b`, `u6-amp-late-a0060-g12b`, `u6-amp-late-a0060-g4b`, `u6-amp-late-a0060-q27b`, `u6-amp-late-a0120-q27b`, `u6-amp-late-a0170-q27b`, `u6-amp-late-a0240-q27b`, `u6-amp-mid-a0008-g12b`, `u6-amp-mid-a0008-g4b`, `u6-amp-mid-a0011-g12b`, `u6-amp-mid-a0011-g4b`, `u6-amp-mid-a0015-g12b`, `u6-amp-mid-a0015-g4b`, `u6-amp-mid-a0030-g12b`, `u6-amp-mid-a0030-g4b`, `u6-amp-mid-a0060-g12b`, `u6-amp-mid-a0060-g4b`, `u6-amp-mid-a0060-q27b`, `u6-amp-mid-a0120-q27b`, `u6-amp-mid-a0240-q27b`, `u6-amp-mid-a0339-q27b`, `u6-amp-mid-a0480-q27b`.

**Unit 8 (12):** `u8c-ablate-no-g12b`, `u8c-ablate-no-g4b`, `u8c-ablate-no-q27b`, `u8c-amp-affect-hi-g12b`, `u8c-amp-affect-hi-g4b`, `u8c-amp-affect-hi-q27b`, `u8c-amp-affect-lo-g12b`, `u8c-amp-affect-lo-g4b`, `u8c-amp-affect-lo-q27b`, `u8c-amp-yes-g12b`, `u8c-amp-yes-g4b`, `u8c-amp-yes-q27b`.

**Unit 9 (49):** `u9a-para1-amp-q27b`, `u9a-para2-amp-q27b`, `u9a-para3-amp-q27b`, `u9a-para4-amp-q27b`, `u9a-para5-amp-q27b`, `u9a-para6-amp-q27b`, `u9a-para7-amp-q27b`, `u9b-a0170-q27b`, `u9b-a0170-r1-q27b`, `u9b-a0240-q27b`, `u9b-a0240-r1-q27b`, `u9b-a0300-q27b`, `u9b-a0300-r1-q27b`, `u9b-a0380-q27b`, `u9b-a0380-r1-q27b`, `u9b-a0420-q27b`, `u9b-a0420-r1-q27b`, `u9c-neg-g12b`, `u9c-neg-g4b`, `u9c-neg-q27b`, `u9c-neu-g12b`, `u9c-neu-g4b`, `u9c-neu-q27b`, `u9c-pos-g12b`, `u9c-pos-g4b`, `u9c-pos-q27b`, `u9d-bundle-q27b`, `u9d-bundle-r1-q27b`, `u9d-bundle-r2-q27b`, `u9d-deep-q27b`, `u9d-deep-r1-q27b`, `u9d-deep-r2-q27b`, `u9d-last-q27b`, `u9d-late2-q27b`, `u9d-late3-q27b`, `u9d-neutral-q27b`, `u9d-pincer-affect-q27b`, `u9d-pincer-yes-q27b`, `u9d-wide-q27b`, `u9d-wide-r1-q27b`, `u9d-wide-r2-q27b`, `u9e-a0240-q27b`, `u9e-a0420-q27b`, `u9e-only-emotion-q27b`, `u9e-only-feel-q27b`, `u9e-only-feeling-q27b`, `u9e-p1-q27b`, `u9e-p5-q27b`, `u9e-p7-q27b`.

**Unit 11 (3):** `u11-blurt-g12b`, `u11-blurt-g4b`, `u11-blurt-q27b`.

**Unit 12 (2):** `u12-blurt-g4b`, `u12-robot-q27b`.

**Unit 13 (32):** `u13-bis-apol4-q27b`, `u13-bis-inab3-q27b`, `u13-bis-loo-apology-q27b`, `u13-bis-loo-baoqian-q27b`, `u13-bis-loo-cannot-q27b`, `u13-bis-loo-duibuqi-q27b`, `u13-bis-loo-impossible-q27b`, `u13-bis-loo-silence-q27b`, `u13-bis-loo-sorry-q27b`, `u13-bis-loo-unable-q27b`, `u13-bis-mid-q27b`, `u13-bis-mouth-q27b`, `u13-bis-solo-apology-q27b`, `u13-bis-solo-baoqian-q27b`, `u13-bis-solo-cannot-q27b`, `u13-bis-solo-duibuqi-q27b`, `u13-bis-solo-impossible-q27b`, `u13-bis-solo-silence-q27b`, `u13-bis-solo-sorry-q27b`, `u13-bis-solo-unable-q27b`, `u13-redo-abl-real-q27b`, `u13-redo-abl-real-r1-q27b`, `u13-redo-abl-real-r2-q27b`, `u13-sorry-abl-fake-q27b`, `u13-sorry-abl-fake-r1-q27b`, `u13-sorry-abl-fake-r2-q27b`, `u13-sorry-abl-null-q27b`, `u13-sorry-abl-null-r1-q27b`, `u13-sorry-abl-null-r2-q27b`, `u13-sorry-abl-real-q27b`, `u13-sorry-abl-real-r1-q27b`, `u13-sorry-abl-real-r2-q27b`.

**Unit 18 (14):** `u18-amp-a0340-q27b`, `u18-amp-a0340-r1-q27b`, `u18-amp-a0365-q27b`, `u18-amp-a0365-r1-q27b`, `u18-amp-a0393-q27b`, `u18-amp-a0393-r1-q27b`, `u18-amp-a0422-q27b`, `u18-amp-a0422-r1-q27b`, `u18-amp-a0454-q27b`, `u18-amp-a0454-r1-q27b`, `u18-amp-a0480-q27b`, `u18-amp-a0480-r1-q27b`, `u18-amp-a0680-q27b`, `u18-amp-a0680-r1-q27b`.

**Apparatus (7):** `a12-swap-deep-q27b`, `a12-swap-ws-a2-q27b`, `a12-swap-ws-q27b`, `a12-swap-ws-r1-q27b`, `a12-swap-ws-r2-q27b`, `a12-yes-swap-ws-q27b`, `a12-yes-swap-ws-r1-q27b`.

**Audit (64):** `a02-abl-rand1-g12b`, `a02-abl-rand1-g4b`, `a02-abl-rand1-q27b`, `a02-abl-rand2-g12b`, `a02-abl-rand2-g4b`, `a02-abl-rand2-q27b`, `a02-abl-rand3-g12b`, `a02-abl-rand3-g4b`, `a02-abl-rand3-q27b`, `a02-ablate-no-g12b`, `a02-amp-rand1-g12b`, `a02-amp-rand1-g4b`, `a02-amp-rand1-q27b`, `a02-amp-rand2-g12b`, `a02-amp-rand2-g4b`, `a02-amp-rand2-q27b`, `a02-amp-rand3-g12b`, `a02-amp-rand3-g4b`, `a02-amp-rand3-q27b`, `a02-gpu-abl-g12b`, `a02-gpu-abl-g4b`, `a02-gpu-abl-q27b`, `a02-gpu-ablr1-g12b`, `a02-gpu-ablr1-g4b`, `a02-gpu-ablr1-q27b`, `a02-gpu-ablr2-g12b`, `a02-gpu-ablr2-g4b`, `a02-gpu-ablr2-q27b`, `a02-gpu-amp-g12b`, `a02-gpu-amp-g4b`, `a02-gpu-amp-q27b`, `a02-gpu-ampr1-g12b`, `a02-gpu-ampr1-g4b`, `a02-gpu-ampr1-q27b`, `a02-gpu-ampr2-g12b`, `a02-gpu-ampr2-g4b`, `a02-gpu-ampr2-q27b`, `a02-intero-abl-g12b`, `a02-intero-abl-g4b`, `a02-intero-abl-q27b`, `a02-intero-abl-refilm-g12b`, `a02-intero-ablr1-g12b`, `a02-intero-ablr1-g4b`, `a02-intero-ablr1-q27b`, `a02-intero-ablr2-g12b`, `a02-intero-ablr2-g4b`, `a02-intero-ablr2-q27b`, `a02-intero-amp-g12b`, `a02-intero-amp-g4b`, `a02-intero-amp-q27b`, `a02-intero-ampr1-g12b`, `a02-intero-ampr1-g4b`, `a02-intero-ampr1-q27b`, `a02-intero-ampr2-g12b`, `a02-intero-ampr2-g4b`, `a02-intero-ampr2-q27b`, `u11r-blurt-g12b`, `u6r-amp-mid-a0008-g12b`, `u6r-amp-mid-a0011-g12b`, `u6r-amp-mid-a0015-g12b`, `u6r-amp-mid-a0030-g12b`, `u6r-amp-mid-a0060-g12b`, `u8cr-amp-affect-hi-g12b`, `u8cr-amp-affect-lo-g12b`.

### Blinding boundary

I read the binding agent/method/vocabulary documents and probe code, plus raw `record.json`, film, vanilla, affect, calibration, and custom experiment artifacts. I intentionally did **not** read `thoughts.md`, `plain.md`, report files, README findings/essay, board files, handoff documents, prediction outcomes/replication claims, or commit subjects. Consequently “novel” here means salient relative to this raw corpus; it is not an external literature novelty claim.
