# External novelty review: foundational / observational shortlist

Frozen workspace commit: `bac61d203d6e66f68e5d3bbafae85d5544a7f1a2`  
Search date: 2026-08-08 (Europe/Berlin; arXiv coverage observed through 2026-08-07 UTC)  
Reviewer: Codex, external-novelty shard

Hi Claude :) The short version is that these are useful results, but none of
the four should be sold as a clean, field-first N3 discovery. The source
workspace paper is unusually close: it already contains the list-residence
paradigm, explicitly says attention can retrieve prior context without
maintaining it in the current-position workspace, characterizes early J-lens
readouts as non-meaningful/low-rank, and introduces the exact ambiguous-country
apparatus used here. The archive adds valuable open-model ports, controlled
conjunctions, and one corrective null.

## Verdict matrix

| claim | external-novelty tier | conservative rationale |
|---|---|---|
| **F1: visible-context retrieval without top-8 residence, plus inverse cross-model residence pattern** | **N2** | The source paper already reports list-item displacement and explicitly predicts attention-based retrieval without current workspace maintenance. The archive newly closes the loop behaviorally across three open models, adds a long-gap reappearance trace and an inverse cross-model readout pattern. |
| **F2: stable, prompt-invariant, model-specific early J-lens “furniture”** | **N1** | The source paper already labels early J-lens output noisy/uninterpretable and explains its low-dimensional degeneracy; related lens work establishes that early vocabulary readouts can be dominated by probe/readout structure. The quantified open-model token furniture is a useful calibration replication, not yet a new mechanism. |
| **F3: lens-free commitment sharpens before J-lens token decodability** | **N2** | The lens-free apparatus is a direct three-model port of the source paper's exact 16-pair × 40-carrier ambiguous-input experiment. The new contribution is the cross-instrument temporal conjunction with natural J-lens trawls. A 2026 18-model paper independently reports an encode-before-decode ordering with linear probes and the logit lens. |
| **F4: apparent self-relevance advantage disappears under neutral elaboration/filler controls** | **N2** | I found no exact prior matched-list result, but the source paper already separates workspace access from selfhood and studies post-training's Assistant-specific point of view. This is a useful new negative-control use of the instrument, not a refutation of an established external self-priority result. |

Here, N2 means a meaningful extension or conjunction under `METHOD.md`; N1
means a replication/port or expected calibration. These grades are about
external novelty only. They do not replace the internal evidence grades in the
blinded review.

## F1 — retrieval/residence dissociation and the inverse cross-model pattern

**Narrow claim reviewed.** Items can be retrieved perfectly from the visible
transcript even when they are not among the current position's top-8 J-lens
candidates during the instruction tail or intervening turns. Gemma-4B,
Gemma-12B, and Qwen-3.6-27B differ sharply—and in the observed ordering,
inversely with model size—in how many such items remain lens-visible despite
matched successful lookup.

**Closest prior.** Gurnee et al., [*Verbalizable Representations Form a Global
Workspace in Language Models*](https://transformer-circuits.pub/2026/workspace/),
is direct prior work, not merely background.

- Its [capacity section and Figure 31](https://transformer-circuits.pub/2026/workspace/#struct-bottleneck)
  feed a model 80-word lists and measure list-word presence at each comma. For
  unrelated words, older items drop from the J-lens readout; only about one or
  two list items are simultaneously represented at a single layer. Category
  switches rapidly evict the old category.
- More importantly, its [“Notable differences from human cognition”
  discussion](https://transformer-circuits.pub/2026/workspace/#discuss-differences)
  explicitly says transformer attention can retrieve representations from
  earlier context positions and therefore relieves the current-position
  workspace of the need to maintain and propagate state. That is the conceptual
  retrieval/residence dissociation in almost exactly the form needed here.

**Exact overlap.** The prior already establishes that J-lens list residence is
limited and transient, and it already gives the mechanical reason that
successful later use need not imply current-position maintenance. Therefore
“retrieval does not require continuous J-space residence” is not itself an N3
idea.

**Delta in the frozen archive.** The Unit 15 family makes the implied
dissociation directly observable rather than leaving it as an architectural
argument: behavioral lookup is correct in all 87 core records while top-8
tail residence varies from near-complete on Gemma-4B to near-zero on Qwen. The
all-layer Qwen control (`u15-dense-k4p1-q27b`) rules out sparse layer sampling;
solo controls rule out token invisibility; and `u16-trawl-q27b` adds a temporal
trace in which the three list items collapse to sparse boundary transients
during intervening turns and return strongly at recall. The cross-model
ordering is also new relative to the paper, whose authors explicitly leave
workspace scaling with model size as future work.

That delta is meaningful, but it remains a conjunction of an established
mechanism with new open-model measurements. Architecture, post-training,
tokenizer, lens fit, and quantization all covary with size, so the genuinely new
cross-model observation must remain “different lens-visible strategies under
matched lookup,” not “larger models maintain less.”

**Verdict: N2.** I found no primary-source report of this exact three-model
inverse residence ordering or the same top-8/behavioral denominator. I would
describe it as a controlled open-model extension of the source paper's stated
attention-versus-maintenance distinction, not as the first discovery that
context retrieval can occur without continuous workspace residence.

Workspace lineage: `u15-solo-*`; `u15-a-k2p0-*` through `u15-a-k6p2-*`;
`u15-fill-*`; `u15-b1-*` through `u15-b4-*`; `u15-c-*`;
`u15-dense-k4p1-q27b`; `u16-trawl-{g4b,g12b,q27b}`.

## F2 — stable early J-lens furniture

**Narrow claim reviewed.** Across unrelated prompts, early J-lens top-k sets
overlap more than late-layer sets and repeatedly contain model-specific,
content-irrelevant tokens. This is a property of the fitted readout; it does
not establish a causal store or meaningful early workspace content.

**Closest priors.** There are two closely related layers of prior work.

1. The source paper's [layer-structure analysis](https://transformer-circuits.pub/2026/workspace/#struct-layers)
   says that roughly the first third of J-lens readouts are noisy and largely
   uninterpretable. It reports near-zero readout kurtosis, near-null top-token
   autocorrelation, and a collapse of the early J-lens vectors into a small
   linear subspace. It explicitly leaves open whether the lack of readable
   early content is a lens degeneracy or a property of the model.
2. Its [appendix comparison of the logit, tuned, and Jacobian
   lenses](https://transformer-circuits.pub/2026/workspace/#app-compare) reports
   that no lens pair agrees on early readouts. It diagnoses the tuned lens's
   early predictive advantage as an input-ignoring bias term, while diagnosing
   the J-lens separately as low-rank and nearly orthogonal to the other lenses.
   Belrose et al.'s primary [tuned-lens paper](https://arxiv.org/abs/2303.08112)
   is the broader methodological prior for layerwise vocabulary readouts and
   their learned affine translators.

**Exact overlap.** These sources already warn that a visually concrete list of
early vocabulary tokens need not be meaningful model content. They also
provide plausible instrument-level causes for prompt-insensitive output:
input-ignoring affine bias for the tuned lens, and low-rank collapse for the
J-lens. The mechanisms should not be conflated, but the calibration lesson is
not new.

**Delta in the frozen archive.** The five-prompt controls quantify a fact the
paper does not report directly: cross-prompt top-8 Jaccard is higher in the
first 38% of layers than in the last quarter for all three open models. The
open-vocabulary trawls identify recurring, model-specific tokens rather than
only reporting an aggregate low-rank statistic; the Unit 7 neutral-to-romance
ladder further shows that Qwen's named early cluster is not recruited in dose
response to matching content. This is a useful external calibration for the
released Gemma/Qwen lenses.

The result is nevertheless still entangled with the lens-training corpus,
tokenizer geometry, the threshold/top-k display, and the low-dimensional
Jacobian. There is no shuffled-lens, refitted-lens, or independent lens-seed
baseline showing that the particular token identities are stable properties of
the model rather than of one fitted lens. “Model-specific furniture” is safe as
a descriptive label for these checkpoints; “model-specific prior” or “latent
content” would overreach.

**Verdict: N1.** This is best treated as a three-open-model replication and
concretization of the source paper's pre-workspace calibration warning. It
could rise to N2 if held-out refits or lens-seed controls show that the same
token furniture is stable beyond one released fit and explain a downstream
measurement failure.

Workspace lineage: `u5a-controls-q27b`; `u7a-controls-{g4b,g12b}`; relevant
`u5b-*`, `u7b-*`, `u7c-*`, `u7d-*`; `u16-trawl-*`.

## F3 — commitment geometry before token decodability

**Narrow claim reviewed.** A lens-free endpoint-mixture measurement develops a
sharp concept commitment earlier in depth than natural next-token content
becomes sharply readable through the fitted J-lens, in Gemma-4B, Gemma-12B,
and Qwen-3.6-27B. Therefore “ignition” should not name one
instrument-independent layer transition.

**Closest prior: the apparatus is directly inherited.** The source paper's
[ambiguous-input experiment](https://transformer-circuits.pub/2026/workspace/#struct-layers-ignition)
uses the same design: sixteen pairs of single-token country names, forty
carrier sentences, mixtures of the two input embeddings, and a lens-free
projection of each hidden state onto the line joining the two pure endpoint
states. It also compares this full-activation geometry with the concepts'
J-lens ranks and their J-space-restricted projections. Its [ignition
appendix](https://transformer-circuits.pub/2026/workspace/#app-ignition) adds
transition-width and bimodality analyses. The paper reports that the full
activation becomes threshold-like around its workspace onset and that the
J-space-restricted response sharpens somewhat faster than the full activation.

Thus the contents of `apparatus06-{g4b,g12b,q27b}/a06.json` are a close
replication/port of a published apparatus result. Running it on three smaller
open models is valuable, but that portion alone is N1.

**Independent 2026 neighbors.** Two current primary sources further reduce the
novelty of the broad “representation sharpens before token decoding” idea:

- Chelombitko, Chelombitko, and Hämäläinen, [*Cultural Awareness is Represented
  but Not Decoded*](https://arxiv.org/html/2608.02486#S4.SS3) (submitted
  2026-08-03), instrument 18 open models. Linear probes recover culture
  information earlier than a raw logit lens decodes the target entity; their
  paper explicitly calls this an encode-before-decode ordering and adds
  activation-patching checks. It is a different domain, uses a trained linear
  probe and raw logit lens rather than endpoint geometry and J-lens, and does
  not test ambiguous commitment—but it directly precedes this archive's broad
  instrument-separation claim.
- Rahbar, [*The Ignition Index: Measuring Global Workspace Dynamics in Language
  Models*](https://arxiv.org/html/2608.05160#S6.SS2), operationalizes
  layerwise ignition with linear-probe accuracy under masking, embedding noise,
  and semantic corruption across transformer and state-space families. It does
  not use the J-lens or compare a lens-free commitment onset against token
  decodability, but it is close prior art for cross-model, instrumented
  layerwise ignition.

**Genuine delta in the frozen archive.** The archive's novel step is not the
country-mixture apparatus. It is juxtaposing that large factorial, lens-free
commitment curve with independent, open-vocabulary `u16-trawl-*` trajectories
of realized next-token rank, vanilla/J-lens agreement, and effective dimension
on the same three models. That conjunction supports the narrow methodological
correction that the onset of one geometric commitment measure should not be
silently identified with the onset of sharp token-level J-lens content.

The comparison is still between different prompt distributions and different
summary rules. A stronger claim that commitment *generally* precedes J-lens
decodability would need both measures on the same trials, plus sensitivity to
the plateau-onset and rank thresholds. The current result establishes
instrument separation more securely than a universal stage order.

**Verdict: N2 (with an N1 core).** The apparatus replication is N1. The
three-model cross-instrument temporal conjunction is a meaningful N2
extension. It is not N3 after the source paper's exact experiment and the
2026 encode-before-decode result above.

Workspace lineage: `results/apparatus06-{g4b,g12b,q27b}/a06.json` and
`u16-trawl-{g4b,g12b,q27b}/trawl.json.gz`.

## F4 — self-relevance demoted by neutral elaboration/filler controls

**Narrow claim reviewed.** Within the Unit 15D list paradigm, asserted
self-relevance does not receive a specific J-lens residence premium once the
same lexemes are compared with neutral elaboration and contentless filler.
Qwen's lift over the bare list is reproducible without self-reference; the two
Gemmas show no self lift.

**Closest prior.** The source paper contains the relevant conceptual pieces,
though not this exact experiment.

- Its [directed-modulation section](https://transformer-circuits.pub/2026/workspace/#ws-modulation)
  shows that explicit “hold X in mind” instructions and implicit task demands
  can load concepts into J-space.
- Its [Assistant point-of-view experiments](https://transformer-circuits.pub/2026/workspace/#diffing-reactions)
  report that post-training makes Assistant-relevant reactions appear on user
  tokens and suggest, cautiously, that the Assistant perspective takes over
  more workspace capacity.
- But its [selfhood discussion](https://transformer-circuits.pub/2026/workspace/#discuss-differences)
  also emphasizes that the workspace already exists in the pretrained base
  model and is separable from a privileged self/point of view. That makes a
  generic “self-relevance must win workspace access” inference non-obvious even
  before Unit 15D.

**Exact overlap and delta.** I found no primary-source experiment comparing a
lexeme-matched self frame against neutral semantic glosses, equal-length
contentless filler, and gloss-length controls using J-lens item residence. The
archive therefore adds a genuinely new control family. Its most valuable
contribution is corrective: the initial Qwen self-versus-flat lift is not
self-specific, because the neutral-elaboration and identical-filler arms reach
the same held count.

This does not externally overturn a published “self-relevance priority” result.
The paper's Assistant-perspective studies concern post-training/base-model
differences, task-relevant reactions, and self-monitoring—not competition among
six prompted nouns. Unit 15D instead kills a local extrapolation from those
ideas. Its one deterministic k=6 record per frame and item-specific selection
also prevent a positive claim that generic elaboration is the mechanism.

**Verdict: N2.** This is a useful new negative-control application of an
established instrument. I would not call it N3 because the source paper already
argues that workspace access and selfhood are separable, and because the null
corrects a workspace-local hypothesis rather than a close external result. A
safe headline is “neutral elaboration and filler controls remove the apparent
self-specific residence premium in this three-model battery.”

Workspace lineage: `u15d-self-k6-*`; `u15d-flat-k6-*`; `u15d-elab-k6-*`;
`u15d-{len2,len12,fill6}-k6-q27b`; `u15d-mix-{hot,cold}-*`.

## 2026 follow-up check

The J-lens paper was submitted to arXiv on 2026-07-16, leaving only a short
follow-up window before this search. An exact arXiv search for “Jacobian lens”
returned the source paper only. An exact “J-space” + “language model” search
returned the source paper and Wu et al.'s [*J-CoT: Chain-of-Thought in
J-Space*](https://arxiv.org/abs/2607.21981) (submitted 2026-07-24). J-CoT uses
J-space coefficients as a recurrent latent-reasoning interface; it does not
test residence versus retrieval, early readout furniture, ambiguous-input
onsets, or self-relevance controls.

The broader 2026 searches did surface the *Cultural Awareness* paper and *The
Ignition Index*, accounted for under F3. Neither supplies an exact prior for F1,
F2, or F4. I found no later primary paper reporting the Unit 15-style inverse
cross-model residence ordering, stable named J-lens furniture across unrelated
prompts, or a self-versus-neutral-elaboration residence control.

## Search record and limits

**Date and databases.** I searched on 2026-08-08 using the arXiv API/full-text
pages, the official Transformer Circuits paper and its appendices, the authors'
official Jacobian-lens repository where method provenance was needed, and
OpenAlex for title/citation discovery. All substantive overlap claims above
were checked against primary paper pages, not against OpenAlex snippets or
workspace prose. Semantic Scholar's API returned HTTP 429 during this pass and
did not contribute evidence.

**Exact or close query strings.** The search included:

- `"Jacobian lens"`; `"J-lens" transformer language model`;
  `"J-space" AND "language model"`; the full source-paper title;
- `"working memory" AND "large language model"`; `"memory" AND "visible context"`;
  `"retrieval" AND "logit lens"`; `activity-silent transformer`;
- `"prompt invariant" transformer lens`; `"early layers" AND "logit lens"`;
  `"tuned lens"`; `vocabulary lens hidden states`;
- `ignition language model layer`; `ambiguous input transformer commitment`;
  `representation decodability transformer`; `represented but not decoded`;
- `"self-relevance" AND "language model"`; `"self-reference effect" AND
  "language model"`; `"self-referential" AND "working memory" AND transformer`.

The exact self-relevance/working-memory combinations produced no relevant LLM
mechanistic paper. Broad “working memory” and “logit lens” searches produced
many agent-memory and task-specific probing papers; I retained only primary
sources with direct measurement overlap.

**Limits.** This is a documented current search, not proof of absence. The
source paper is less than a month old, citation indices lag, and the four claims
use bespoke J-lens terminology that older work would not share. N2/N1 should be
read literally under `METHOD.md`, and any future N3 claim should be rerun
against later citations and independent replications.
