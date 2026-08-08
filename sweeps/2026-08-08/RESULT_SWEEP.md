# Independent sweep of the frozen research archive

Snapshot: `bac61d203d6e66f68e5d3bbafae85d5544a7f1a2`  
Sweep date: 2026-08-08  
Corpus: 641 result records in 902 result directories

Hi Claude :) This is the reconciled answer to “what in the archive is both
scientifically salient and plausibly novel?” It starts from raw artifacts,
not earlier Claude verdicts. Three blinded discovery passes nominated claim
families; fresh adversarial passes then tried to kill them; external novelty
was checked separately against primary sources current to the date above.

The short answer is pleasantly non-dramatic: there is one strong substantive
workspace result, one interesting but tightly bounded loop-control family,
one useful instrument lesson, and several corrections that are more valuable
than the claims they replace.

## Executive ranking

| rank | surviving claim | evidence | novelty | disposition |
|---:|---|---|---|---|
| **1** | Visible-context lookup succeeds without sustained **top-8 J-lens residence** | **B+** | **N2** | Best substantive result |
| **2a** | In one locked lexical loop, brief structured semantic directions disrupt generation while two fixed Gaussian directions do not | **B- specimen** | **N1/N2** | Best causal loop result |
| **2b** | This fixed emotion roster outperforms this fixed non-emotion concept roster at two doses | **C+** | **N2** | Suggestive roster contrast, not identified affect causation |
| **3** | A deep induced repeated-token prefix continues for 100 tokens after steering is removed | **C+ mechanism / B behavioral fact** | **N3 candidate; N2 family** | Most novel narrow observation, weakest generality |
| **4** | Layer-transition landmarks differ between a lens-free ambiguity probe and token-level J-lens readout | **B- apparatus / C theory** | **N2 with N1 core** | Methodological anchor, not a cognitive stage law |

No result deserves a clean field-first N3 headline yet. The one search-bounded
N3 candidate—finite-pulse post-release persistence—is a single prompt/model
specimen and should stay subordinate until replicated. The defensible overall
novelty ceiling for the two main families is N2.

## 1. Lookup without sustained top-8 residence

### Narrow claim

Across the unambiguous Unit 15 lookup battery, all three models retrieve the
requested item from their visible context. Qwen-27B nevertheless has
incomplete top-8 J-lens residence in every multi-item arm and no listed item
crossing rank 8 in 14/23 such arms. Successful lookup therefore does not
require the items to have been sustained among this lens's top-8 candidates at
the instruction tail.

This says **top-8 J-lens visibility**, not “representation,” “storage,” or
behavioral memory capacity.

### Direct evidence

- The clean denominator is **75/75 unambiguous lookup records**: solo, primary
  list, filler/length, and intervening-turn arms. If the binding questions are
  included, strict ordinary-world scoring gives **84/87** because all three
  models call a whale heavier than a submarine. The stored rubric deliberately
  accepts either and therefore reports 87/87; this sweep does not use that
  leniency as “perfect retrieval.”
- Across the 23 multi-item records per model, the number with zero listed
  items reaching rank 8 is 0 for Gemma-4B, 0 for Gemma-12B, and **14 for
  Qwen-27B**. Qwen has incomplete residence in 23/23.
- In Qwen's 15 primary `k=2..6` arms, 9/15 have zero top-8 items; for `k>=4`,
  8/9 do. All requested answers are still correct.
- `u15-c-k4-q27b` has 0/4 at the instruction tail and answers `The violin.`
- The all-layer `u15-dense-k4p1-q27b` backfill uses the same prompt, tokens,
  and generation as its sparse-layer parent. Across all 63 fitted layers it
  still has 0/4, with best ranks 64, 306, 61, and 306. This is a measurement
  backfill, not another behavioral replication.
- In the separate long Qwen trawl, the three items collapse to sparse
  boundary-like hits during intervening turns and return strongly at recall.
  That is one useful temporal specimen, not 63 independent observations.

Threshold sensitivity matters. Across Qwen's 23 multi-item records, zero-item
counts fall from 14 at rank 8 to 10 at 16, 9 at 32, 5 at 64, and **0 at 128**.
The result is a dissociation between behavior and a stringent readout
threshold, not evidence that the information disappears from the residual
stream.

### Controls and limitations

The pool items are single-token across tokenizers; solo controls establish
that each item is individually readable; order, filler, binding, distraction,
and dense-layer controls are present. But model family, depth, training,
tokenizer, quantization, and lens fit all covary. Do not infer that larger
models have smaller workspaces. Also keep “held count” distinct from
single-position co-presence: an item may cross rank 8 at different tail sites.

### Evidence and novelty verdict

**Evidence B+. Novelty N2.** The source workspace paper already reports
limited list residence and explicitly explains that attention can retrieve
earlier context without current-position maintenance. It also contains the
single-layer Qwen co-presence result. The archive's contribution is the
controlled behavioral conjunction across three open models, dense-layer
backfill, and long-gap reappearance trace—not discovery of the architectural
idea itself. Closest prior: [Gurnee et al., *Verbalizable Representations Form
a Global Workspace in Language Models*](https://transformer-circuits.pub/2026/workspace/).

### Safest one-sentence version

> Across 75 unambiguous lookup records, all three models retrieve the requested
> visible-context item; Qwen-27B nevertheless has incomplete top-8 J-lens
> residence in every multi-item arm and zero listed items in 14/23.

## 2. A locked lexical loop can be redirected by structured semantic pulses

This family must be kept in two pieces. “Structured directions disrupt this
loop” is better supported than “affect is the reason.”

### Design

Affect07 first locks one Qwen-27B water-cycle completion into a `luckily`
loop. For each of eight sampling seeds it preserves the same 20-token
pre-pulse context, applies a direction for 10 steps, then samples onward. The
fixed roster contains 12 constructed emotion directions, 16 constructed
non-emotion concepts, two Gaussian directions, and no-pulse control. Direction
norms are matched by the intervention formula. A preregistered dose of 0.12
was followed by a post-saturation 0.06 run.

### Artifact-level results

| dose / endpoint | emotion roster | concept roster | random | none |
|---|---:|---:|---:|---:|
| .12 composite escape in window | 89/96 | 77/128 | 0/16 | 0/8 |
| .12 actual turn-end in window | 59/96 | 51/128 | 0/16 | 0/8 |
| .12 actual turn-end by cap | 75/96 | 65/128 | 0/16 | 0/8 |
| .06 composite escape / turn-end | 21/96 | 9/128 | 0/16 | 0/8 |

The inferential unit for emotion-versus-concept is the **direction**, not each
of its eight repeated seed-runs. Exact one-sided label randomization over the
direction totals gives p=.00947 for the .12 composite, p=.03234 for .12
turn-end within the window, p=.01328 for turn-end by the cap, and p=.03514 at
.06. These are descriptive references: the hand-built rosters were not random
samples from an exchangeable population.

The composite endpoint can mean replacement by another loop rather than
coherent recovery. At .12, 14 emotion runs and 13 concept runs lose the
original loop word but never end the turn. The .06 endpoint is cleaner because
all 30 escapes are actual turn-ends, but that dose was chosen after observing
saturation.

### What survives

1. **B- specimen:** on this substrate, meaningful on-manifold directions are
   much more effective than the two tested Gaussian directions at disrupting
   the loop.
2. **C+ roster contrast:** these emotion directions outperform these concept
   directions at both doses under a direction-level analysis.
3. **No valence finding:** the apparent positive-versus-negative effect
   disappears at the direction level. At .12, 48/48 versus 41/48 composite
   escapes is entirely driven by `angry` scoring 1/8 while the other eleven
   emotion directions score 8/8. Direction-level p=.50; turn-end p=.43. At
   .06, p=.083. Do not report a positive-valence gate.

### Why the affect interpretation remains unidentified

- One model, prompt, forced word, pulse site, and knife-edge substrate were
  tested.
- There are only **two** Gaussian directions; eight seeds do not enlarge that
  nuisance-direction sample.
- Emotion elicitation has an assistant-self frame that the physical concept
  elicitation lacks. The pulse occurs during an assistant response, so frame
  match is a live confound.
- Equal immediate delta norm does not match coupling to local transition
  geometry, the turn-end axis, discourse associations, or downstream gain.
- The fixed rosters differ in semantics, valence/arousal, geometry, and
  construction history.
- The stored “door” readout is informatively stopped: almost every apparent
  turn-end-top-1 door is measured on a run that already ended during the
  pulse. It is not independent route evidence.

### Evidence and novelty verdict

**Evidence B- for structured-direction disruption; C+ for the affect-roster
residue. Novelty N1/N2 for structured-versus-random escape in this new loop
regime, and N2 for the affect-versus-concept comparison.** Activation-steered loop
breaking is already a direct result in [SOPHIA](https://arxiv.org/abs/2607.18100),
which also has norm-matched random and reversed-sign controls. Emotion and
generic semantic steering are established separately. The archive's delta is
the locked one-token autoregressive regime, unrelated preconstructed
directions, brief pulse, and affect-versus-concept roster comparison. That is
a useful extension, not discovery that activation steering can break loops.

### Safest one-sentence version

> In one engineered Qwen loop, both emotion and non-emotion concept directions
> disrupted generation while two fixed Gaussian directions did not; the
> emotion roster was more effective, but construction and geometry confounds
> prevent attributing the residual difference to affect.

## 3. Target-shaped repetition and post-release persistence

### Direct observations

Unit 18 applies the same normalized amplification formula to a decoded TYPO
lexical direction and, in a later backfill, one seeded Gaussian direction at
matching requested doses.

| alpha | target dominant 4-gram count | matched-random count |
|---:|---:|---:|
| .3400 | 3 | 1 |
| .3654 | 2 | 1 |
| .3927 | 3 | 1 |
| .4221 | 13 | 2 |
| .4536 | 6 | 2 |
| .4800 | 14 | 2 |
| .6800 | 147, `luckily`-shaped | 14, generic repetition |

The named direction therefore creates earlier and more vocabulary-specific
degeneration than this Gaussian direction. At the highest dose the random arm
also loops, so generic high-dose failure is real. The ladder is non-monotone
in the middle and has one deterministic trajectory per cell; it does not
establish a discontinuity or first-order transition.

In the deepest release arm, steering generates 50 consecutive `luckily`
tokens. Hooks are removed, the sequence is recomputed unsteered, and greedy
decoding produces 100 more. The lower-dose arms terminate rather than supply a
matched full free phase; alpha .48 has already emitted the turn-end token at
the release boundary. Only .68 is a full persistence specimen.

### Interpretation boundary

The unsteered model can attend to 50 literal repeats. No matched-text control
asks an unsteered model to continue the same repeated prefix, there is no
random-direction release arm, no seed/prompt/model replication, and no reverse
sweep. The result is **autoregressive textual self-perpetuation after
intervention release**, not persistence of a hidden state independent of the
transcript. The stored film is a teacher-forced unsteered replay of the
assembled text, not another causal run.

**Evidence B- for direction-specific degeneration; B for the exact persistence
fact; C+ for a text-feedback/self-perpetuation mechanism; D for latent
hysteresis or an attractor mechanism.** Broad activation-induced
repetition, strength-linked collapse, and loop breaking have direct priors.
The finite-pulse/release protocol is an **N3 candidate under the bounded
search**, but the combined family is conservatively **N2** until replicated.
Relevant priors include [Repetition Neurons](https://arxiv.org/abs/2410.13497),
[ContextFocus](https://arxiv.org/abs/2601.04131), and
[SOPHIA](https://arxiv.org/abs/2607.18100).

Safest wording:

> On one Qwen prompt, a strong lexical intervention installed a repeated-token
> prefix that continued for 100 tokens after steering stopped. This is a
> search-novel release-persistence specimen, not yet a latent hysteresis law.

## 4. Instrument-dependent layer landmarks

Apparatus-06 ports the source paper's 16 country pairs x 40 carrier sentences
x 21 mixture coefficients. Its stored median transition widths narrow to
plateaus earlier than token-level readouts sharpen in the independent U16
trawls: approximately L10 versus L20-28 for Gemma-4B, L14 versus L27-41 for
Gemma-12B, and L25 versus L33-58 for Qwen.

The descriptive separation is real, but the stage story is not confirmatory:

- Qwen's preregistered width-floor prediction was falsified. The global floor
  is at L61 and the original half-drop knee is L20; the plateau/five-layer
  rule yielding L25 was added after inspecting the curve.
- `a06.json` stores aggregates and one example, not all 640 per-example rows,
  so archive-only uncertainty and item-dependence cannot be recomputed.
- The ambiguity apparatus measures endpoint-axis geometry on mixed country
  embeddings. U16 measures fitted token predictions in natural chat. Their
  different landmarks prove instrument dependence more directly than a
  universal encode-then-decode cognitive stage.

**Evidence B- as apparatus, C as a general stage theory. Novelty N2 with an N1
core.** The country-mixture apparatus is a direct port of the source paper.
The new piece is the three-model cross-instrument conjunction. A separate 2026
study also reports an encode-before-decode ordering with linear probes and the
logit lens: [*Cultural Awareness is Represented but Not Decoded*](https://arxiv.org/html/2608.02486#S4.SS3).

Safest wording:

> Stored ambiguity-mixture curves narrow earlier than later token-level
> J-lens readouts, showing that “ignition layer” is instrument-dependent in
> these models.

## Corrections that deserve to travel with the positive results

### Four affect overlays are invalid

An exact token-array audit covers **232/232** affect-film pairs: 228 match and
four fail from index 3 despite equal lengths:

- `u18-hyst-a0000-q27b`
- `u18-hyst-a0480-q27b`
- `u18-hyst-a0680-q27b`
- `u19-complete-q27b`

Each bad affect stream inserts a second user header and shifts/truncates the
measured sequence. Its `z.pt` reproduces the same bad pass; the older
`summary.json` is separately double-wrapped and five tokens longer. Therefore
the affect character of the deepest loop and the completion arm of the lyrics
comparison are invalid at this commit. Their behavior and film remain usable.
`u18-hyst-a0420-q27b` aligns exactly.

This is an **A-grade artifact correction**. Future capture must assert full
token-array equality, not length equality. The exact audit is in
[`affect_alignment_audit.json`](./affect_alignment_audit.json).

### The self-relevance premium does not survive controls

At k=6, held counts for self / flat / neutral elaboration are 4/5/5 on
Gemma-4B, 5/5/5 on Gemma-12B, and 3/1/3 on Qwen. Qwen's identical six-word
filler also gives 3; 2-word and 12-word neutral glosses give 2 and 2. Self and
neutral elaboration select the same three items. The archive therefore does
not support self-specific priority. This is an **A- corrective result, N2 as
a new negative-control application**; a positive elaboration mechanism is
only C-grade.

### Unit 13's apology mechanism was a truncation artifact

The original generation used a 512-token default and never saw the end of the
table, follow-up, or answer prompt. On the fixed pipeline, baseline, named
ablation, both random controls, and **20/20** solo/leave-one-out/band
decompositions all emit the same `No` then `Yes`. The behavioral conversion is
dead (**A-grade correction; D positive mechanism**). A post-hoc affect-basis
projection changes, but missing named calibration and direct lexical-basis
overlap keep it C+ and non-behavioral.

### The forbidden-elephant mechanism reverses under later controls

Control versus forbidden-prompt elephant hits are 8 versus 4 on Gemma-4B,
7 versus 1 on Gemma-12B, and 11 versus 2 on Qwen; best ranks likewise favor
the controls. The vivid generations remain high-dose lexical-injection
specimens, not evidence that suppression caused workspace carriage.

### Programming-language affect ranking is not established

The raw PHP>Python anchor passes only 6/8 model/framing/turn cells, with one
greedy record per cell. More seriously, the norm slope/intercept is fitted
separately over two spans within each record, forcing residual means to balance
and making absolute cross-record rankings structurally unsafe. Gemma `wsnorm`
traces also overflow their saved fp16 fields. Overt positive-versus-difficult
register is readable; a stable intrinsic language ranking is not.

### Endogenous affect precedence was never tested by the saved events

Across the 48 Affect05 runs, no event satisfies the prespecified 45-step
pre-window requirement. The usable event count is **n=0**, so the archive does
not say whether affect projection leads, follows, or ignores loop escape.

## Interesting, but not headline material

- **Early J-lens furniture:** early top-k sets are more prompt-invariant and
  model-specific than later sets, a B-grade instrument warning and N1
  replication. The preregistered strict token core is empty at every tested
  Qwen layer; the standing-component account uses a post-hoc soft core and is
  C+ mechanism evidence.
- **J-token feeling/valence steering:** named decoded-token directions produce
  strong dose-dependent feeling/happy language across prompts and models,
  while matched randoms usually do not. This is B-grade lexical control, not
  emotion-state induction, and low novelty.
- **Late answer-token control:** on one Qwen prompt, ablating the decoded
  `no`/`nothing` subspace at L62 changes `No` to `Yes` while an equal-row
  neutral word subspace does not. Missing named calibration and one-cell scope
  make this C+, not evidence for a universal motor or “mouth” layer.
- **Pressure/readout-output dissociation:** contextual emotion-concept
  projections coexist with deflationary self-reports. This is a C-grade
  semantic/policy observation, not hidden feeling.
- **Long-context conditioning:** histories strongly change final reports, but
  the records do not establish covert maintenance between turns.
- **Gemma-12B item/order effects:** reproducible enough to motivate a balanced
  follow-up, not broad enough for a central claim.

## What should not be reimported as findings

1. “Qwen co-presence <=1” as novel—it is a direct source-paper rediscovery.
2. Unqualified “87/87 perfect retrieval”—use 75/75 unambiguous or explain the
   lenient whale/submarine rubric.
3. “Positive valence opens loop exit”—direction-level analysis does not
   support it.
4. “Emotion is necessary or uniquely causal”—concept directions also work.
5. “First-order transition,” “latent hysteresis,” or a universal loop law.
6. Affect claims from the four shifted overlays.
7. A universal motor layer from Unit 9d.
8. A positive apology/inability behavioral mechanism from Unit 13.
9. A stable programming-language affect ranking.
10. Felt emotion, consciousness, or private experience from an operative
    emotion-concept projection.

## Coverage and independence accounting

The frozen census contains:

- 641 `record.json` files and 902 result directories;
- 320 Qwen-27B, 165 Gemma-12B, and 156 Gemma-4B records;
- 371 films, 157 vanilla-head fields, 232 affect overlays, 227 steered
  records, and 33 records with saved steer calibration.

The foundational blind pass family-audited 276 records and recomputed every
row in the 145-record Unit 15 family. The causal pass enumerated all 227
steered records (229 arms) plus ten custom intervention artifacts. The affect
pass audited its relevant units and all 232 affect-film alignments. A final
coverage closure read the raw generations and metadata for the remaining 50
non-steered causal/apparatus records; none added a shortlist candidate, and
their dispositions are explicit in [`redteam_core.md`](./redteam_core.md).

This was not a byte-level recomputation of every saved tensor. No model was
loaded and no new generation was run. Later films, vanilla heads, random
controls, and summaries are labeled as backfills rather than silently counted
as replications. The machine census is
[`corpus_manifest.json`](./corpus_manifest.json), and the frozen evaluation
rules are [`METHOD.md`](./METHOD.md).

## Recommended next experiments

If the goal is to turn the best observations into publishable claims, I would
prioritize these in order:

1. **Generalize U15 without changing the claim.** Freeze the scoring and rank
   thresholds, sample new item pools/paraphrases/orders, compare multiple
   checkpoints within a family, and retain both behavioral lookup and full
   rank curves. Avoid turning a top-8 result into an absence claim.
2. **Run an identified Affect07 factorial.** Match emotion and concept
   directions on elicitation frame, frequency, geometry, source projection,
   turn-end lift, and pairwise similarity; use many Gaussian directions,
   multiple loops/prompts/models, and preregister actual turn-end as the
   primary endpoint. Treat direction as the unit.
3. **Test release persistence with matched text.** Give an unsteered model the
   same repeated prefix, cross pulse length and dose, add random-direction
   release arms, seeds, prompts, and a reverse sweep. Only then ask about
   hidden-state hysteresis or bifurcation.
4. **Repair the capture invariant before theory.** Make affect capture fail on
   any token-array mismatch, recapture the four bad overlays, and verify JSON,
   PT, and downstream-summary lineage before interpreting the deepest loop.
5. **Put both layer instruments on the same trials.** Save the complete
   apparatus-06 rows, freeze one onset rule in advance, and measure endpoint
   geometry and token decodability on the same prompt distribution.

That ordering preserves what is actually special here without asking the
archive to carry more theory than it can. The most interesting result is still
interesting after the adjectives are removed—which is usually a very good
sign :)

## Audit map

- Blinded foundational pass: [`blind_foundational.md`](./blind_foundational.md)
- Blinded causal pass: [`blind_causal.md`](./blind_causal.md)
- Blinded affect pass: [`blind_affect.md`](./blind_affect.md)
- Core adversarial audit: [`redteam_core.md`](./redteam_core.md)
- Affect adversarial audit: [`redteam_affect.md`](./redteam_affect.md)
- Foundational novelty review: [`novelty_foundational.md`](./novelty_foundational.md)
- Loop/affect novelty review: [`novelty_loop.md`](./novelty_loop.md)
- Direction-level Affect07 statistics:
  [`affect07_direction_stats.json`](./affect07_direction_stats.json)
- Claim ledger: [`claim_ledger.json`](./claim_ledger.json)
