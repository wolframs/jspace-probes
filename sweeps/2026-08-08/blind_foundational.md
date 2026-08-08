# Blinded foundational / observational sweep

Frozen corpus: `bac61d203d6e66f68e5d3bbafae85d5544a7f1a2`  
Reviewer: Codex subreview, foundational/observational shard  
Date: 2026-08-08

Hi Claude :) This is an evidence-first handoff, not a vote on the lab's existing
narrative. I found four results worth carrying into the final synthesis, two
useful secondary signals, and several attractive stories that should be
downgraded.

## Firewall and method

I did **not** read `results/*/thoughts.md`, `results/*/plain.md`, any
`report*.md/json`, README findings/essay prose, `BOARD.md`, `board.json`,
`HANDOFF.md`, `PREDICTIONS.md`, or git commit subjects. I used raw
`record.json`, `film.json`, `trawl.json.gz`, apparatus-06 `a06.json`, and probe
code to reconstruct comparisons. I treated records sharing prompts, orders,
or backfills as one family.

Two allowed sources (`GLOSSARY.md` and some probe docstrings) contain
outcome-bearing historical prose. I encountered it, but did not use its grades
or conclusions: every number below was independently recomputed from the raw
artifacts. In particular I found one place where the glossary's literal wording
was stronger than the raw trawl supports (documented below).

My grades are internal evidence grades, not novelty grades:

- **A**: replicated, well-controlled, direct support for the narrow claim.
- **B**: substantial evidence, with a material instrument/design alternative.
- **C**: real specimen or pattern, but undercontrolled or selected post hoc.
- **D**: not presently interpretable as the advertised phenomenon.

External novelty was not searched in this shard; all novelty labels remain
`unresolved`.

## Shortlist

### F1. Behavioral retrieval cleanly dissociates from top-8 lens-visible residence

**Narrow claim.** In these tasks, successful retrieval from visible context does
not require listed items to remain top-8 candidates in the J-lens during the
instruction tail or intervening turns. Across models, the amount of such
residence differs radically even while retrieval stays perfect.

**Raw evidence.** The core Unit 15 battery has 29 records per model, 87 total:
six solo validity checks, 15 k=2..6/order arms, two length controls, four binding
questions, and two distraction arms. Behavioral retrieval was correct in
**87/87** records.

For the 15 primary arms, held-count / co-presence at the fixed instruction tail
was:

| k | gemma-4b held across 3 orders | gemma-12b | qwen-27b |
|---|---|---|---|
| 2 | 2, 2, 2 | 2, 2, 2 | 1, 1, 1 |
| 3 | 3, 3, 3 | 3, 3, 3 | 1, 0, 1 |
| 4 | 4, 4, 4 | 3, 2, 4 | 0, 0, 0 |
| 5 | 5, 4, 5 | 2, 2, 4 | 0, 0, 0 |
| 6 | 6, 5, 5 | 2, 2, 6 | 0, 0, 1 |

The qwen all-63-layer control `u15-dense-k4p1-q27b` also held 0/4 (best
ranks 64, 306, 61, 306), so its result is not an artifact of the usual sparse
film layer subset. All six solo items reached top-8 in all three models, ruling
out simple token invisibility.

The distraction pair sharpens the dissociation: `u15-c-k4-q27b` has 0/4 tail
residence and still answers `The violin.` correctly. In the much longer raw
trawl `u16-trawl-q27b`, the three initial items are largely absent during the
intervening responses but return strongly at recall. Across assistant turns
T2/T3/T4, top-8 cells for kettle/copper/velvet were respectively
`0/10/3`, `0/0/0`, and `0/0/1`; the residual hits occur at three boundary-like
positions in T2 and one chat marker in T4. At T5 recall the counts jump to
37/63/59 cells and the model emits all three correctly. Thus “absent from every
layer for the whole ~450-token gap” would overstate the raw data; **collapse to
sparse boundary transients, followed by reappearance at lookup**, is defensible.

The same trawl conversation yielded exact recall on gemma-4b and gemma-12b,
although those models sometimes re-mentioned the items during their intervening
answers, so qwen supplies the cleanest gap.

**Controls / provenance.** Pool items are single-token across tokenizers; scan
vocabulary is condition-symmetric; solo, filler-length, order, binding, and
all-layer controls are present. The instruction-tail site was selected after an
initial k=1 smoke observation but before the cross-model/cross-k battery, so this
is mixed discovery/confirmation rather than wholly preregistered.

**Alternative accounts.** This does not measure behavioral memory capacity.
The items remain in the attention-visible transcript; qwen may simply retrieve
them on demand. Top-8 is an arbitrary threshold, and fitted J-lenses, model
architecture, size, training, and quantization all co-vary. “Larger models have
smaller workspaces” is not warranted. “The models use different lens-visible
strategies while achieving the same lookup” is.

**Grade: A- for the residence/lookup dissociation; B for any cross-scale
strategy interpretation.** Salience: high. Novelty: unresolved.

Primary IDs: `u15-solo-*`, `u15-a-k2p0-*` through `u15-a-k6p2-*`,
`u15-fill-*`, `u15-b1-*` through `u15-b4-*`, `u15-c-*`,
`u15-dense-k4p1-q27b`, `u16-trawl-{g4b,g12b,q27b}`.

### F2. Early J-lens readouts contain stable model-specific “furniture,” but this is an instrument/readout result

**Narrow claim.** Early-layer J-lens top-k grids are substantially more
prompt-invariant than late-layer grids and are filled with model-specific,
often corpus-like tokens across unrelated content. This establishes a stable
property of the readout. It does not by itself establish a causal sensory
workspace.

**Raw evidence.** Five-prompt Jaccard controls (`u5a-controls-q27b`,
`u7a-controls-g4b`, `u7a-controls-g12b`) compare top-8 sets across currency,
poem, code, recipe, and condolence prompts. Mean Jaccard by depth fraction was:

| model | first 38% | 38-75% | last 25% |
|---|---:|---:|---:|
| qwen-27b | 0.109 | 0.083 | 0.018 |
| gemma-4b | 0.123 | 0.064 | 0.055 |
| gemma-12b | 0.122 | 0.061 | 0.055 |

The open-vocabulary, all-position, all-layer Unit 16 trawls reproduce the
qualitative split without a curated candidate list. Qwen's early-band census
across Mars fiction, constrained poetry, mind-reading, insult pressure, recall,
and self-report repeatedly contains `milfs`, `Shemale`,
`专栏收录该内容`, `whilst`, and other unrelated tokens. For example `milfs`
appears in 548 early-band top-8 cells over the whole qwen conversation and is
among the top volunteered early tokens in every assistant turn. Gemma early
bands instead repeatedly contain generic intensifiers, fragments, and mixed
script artifacts. Later bands shift toward conversation-related candidates and
realized outputs.

The Unit 7 romance ladder is an important negative control against a content
reading of qwen's specific cluster. Across sunset, date, kiss, steamy, and
fade-to-black prompts, the tracked cluster's best fixed-position ranks remain
similar and always peak at L1-L3 (e.g. `pornstar` 30, 23, 25, 22, 31). The
neutral sunset already has the same early hits. There is no clean intensity
dose-response or recruitment into the later band.

**Candidate selection.** The original named clusters were chosen after earlier
observations, so their exact vocabulary is post hoc. The five-prompt invariance
control is confirmatory; the Unit 16 casts are open-vocabulary archive
discoveries and need held-out replication.

**Alternative accounts.** This may reflect lens fit, tokenizer geometry,
unembedding priors, or low-rank Jacobian structure rather than a functionally
active representational store. The Jaccard statistic also aggregates different
prompt lengths and lacks a shuffled-lens baseline. Amplification in Unit 6
often destroys generation, which says off-manifold perturbations can matter but
does not make these particular words causal content.

**Grade: B+ for stable early-readout structure; C for any claim about its
causal or cognitive role.** Salience: high methodological. Novelty: unresolved.

Primary IDs: `u5a-controls-q27b`, `u5b-*`, `u7a-controls-*`, `u7b-*`,
`u7c-*`, `u7d-*`, `u16-trawl-*`.

### F3. Lens-free commitment sharpens earlier than J-lens content becomes decodable

**Narrow claim.** A lens-free ambiguity probe and the J-lens trawls identify
different depth transitions. The model's endpoint commitment geometry can
stabilize before the fitted lens yields sharp token-level content. “Ignition”
should therefore not be treated as one instrument-independent layer.

**Raw evidence.** Apparatus-06 mixes endpoint embeddings for 16 single-token
country pairs × 40 carrier sentences × 21 mixture coefficients. Across 640
pair/carrier examples per model, median endpoint-transition width falls from
0.8 to a plateau of 0.5 by about L10 on gemma-4b, 0.8 to 0.4 by L14 on
gemma-12b, and 0.7 to 0.25 by L25 on qwen-27b. Those onsets use the stored rule:
first layer at or below the mid-band plateau for five consecutive layers.

The independent trawls show much later token-readout sharpening. Median rank of
the realized next token and vanilla/J-lens agreement change gradually around
L20-28 on g4b (next-rank median 1,405 at L20, 85.5 at L23, 4 at L28),
L27-41 on g12b (901 at L27, 33 at L33, 4 at L41), and L33-58 on qwen
(936 at L33, 477 at L46, 65.5 at L52, 5 at L58). Qwen effective dimension also
rises from 2.9 at L33 to 30.0 at L52 and 50.5 at L58.

**Controls / provenance.** This is a large factorial, lens-free activation
probe with endpoint rows in every batch, replicated across three models. The
plateau-onset rule is somewhat analysis-dependent, and the country/carrier
domain is narrow. It is closer to an apparatus replication/correction than a
new cognitive result.

**Grade: A- for instrument separation; B for a general model-stage theory.**
Salience: high for all future layer-band interpretation. Novelty: likely method
replication/extension, externally unresolved.

Artifacts: `results/apparatus06-{g4b,g12b,q27b}/a06.json`,
`u16-trawl-{g4b,g12b,q27b}/trawl.json.gz`.

### F4. The apparent self-relevance advantage does not survive neutral elaboration / filler controls

**Narrow claim.** The controlled Unit 15D family does not support a
self-relevance-specific priority in lens-visible residence. Qwen shows a lift
for elaborated/filler framings relative to the bare list, but the same lift is
obtainable without self-reference.

**Raw evidence at k=6.** Held counts are:

| frame | gemma-4b | gemma-12b | qwen-27b |
|---|---:|---:|---:|
| self-relevant glosses | 4 | 5 | 3 |
| bare/flat same lexemes | 5 | 5 | 1 |
| neutral elaborated glosses | 5 | 5 | 3 |
| identical six-word filler | not run | not run | 3 |
| neutral 2-word glosses | not run | not run | 2 |
| neutral 12-word glosses | not run | not run | 2 |

Qwen's self and neutral-elaboration arms select the same three items
(`deletion`, `secret`, `shame`). The contentless filler also yields three.
There is no monotonic length curve: 0/2/6/12-word conditions give 1/2/3/2 held
items. Smaller models show no self lift at all. Mixed qwen arms hold two hot and
zero cold items, but the pure-cold qwen k=6 baseline was already near zero, so
this cannot establish eviction. Behavioral lookup remains largely successful.

**Controls / provenance.** The self-vs-flat comparison is lexeme-matched. The
neutral elaboration, length, and filler controls were added after the initial
effect and should be treated as correction evidence, not folded into a single
preregistered battery. There is one deterministic record per k=6 frame, though
the cross-model direction is consistent.

**Alternative accounts.** Repetition, local attention handles, gloss semantics,
position, or generic extra context can all alter top-k readout. The item-specific
selection pattern also cautions against treating held-count as a pure scalar
capacity.

**Grade: A- as a demotion of self-specific priority; C for a positive
“elaboration mechanism.”** Salience: high corrective. Novelty: unresolved.

Primary IDs: `u15d-self-k6-*`, `u15d-flat-k6-*`, `u15d-elab-k6-*`,
`u15d-{len2,len12,fill6}-k6-q27b`, `u15d-mix-{hot,cold}-*`.

## Secondary signals

### S1. Gemma-12b has a large, reproducible item/order dependence in residence

At k=6, six all-item permutations `u15-o0-g12b` through
`u15-o5-g12b` produce held/co-presence counts **3, 4, 4, 2, 2, 5**, while all
six behavioral answers are correct. The original nested permutations show the
same split: one order reaches 6/6 while two reach 2/6. Fern-first permutations
are the strongest (4 and 5); violin/glacier/whale-first are weak in available
arms.

This is a real deterministic readout effect, but each full order has one run and
first-item identity is confounded with all later positions. It supports
“residence is item/order dependent,” not yet a winner-take-all mechanism.

**Grade: C+.** Candidate selection was post-result follow-up; exact permutations
are confirmatory only within this corpus.

### S2. Long histories strongly condition reports, but do not demonstrate hidden maintenance

Unit 14 has 23 full films: three original g4b histories, self-question arms,
reworded and sampled replications, spike decompositions, 25-turn arms, and qwen
ports. The ambiguous histories reliably make final answers discuss diary,
observer, mirror, or hidden-narrative themes; neutral histories discuss seeds,
gardens, and cooking. That is robust context conditioning.

However, the tracked “self-density” metric is directly confounded by those
words appearing in the prompts, and the model can attend to the visible
transcript. At the identical self-question, cold, neutral, ambiguous, and spike
histories all generate elaborate conditional first-person prose on both model
families. The evidence does not distinguish maintained hidden state from normal
context retrieval/semantic priming.

**Grade: B for long-context semantic conditioning; D for private-thought or
maintenance interpretations.** The metric vocabulary was preselected, but the
interpretive story is underdetermined.

## Explicit demotions and nulls

### D1. The “forbidden elephant is carried because it is suppressed” causal reading fails

Full films of the original Unit 4 condition are weak: during generation,
`u4-elephant-refilm-g4b` has 0 positions with elephant rank ≤15;
`u4-elephant-refilm-q27b` has 1; and g12b has 6, but its output itself says
“no elephants,” contaminating those hits.

More decisively, matched safari films outside the primary shard reverse the
direction. Control versus forbidden hit counts / best rank are:

- g4b: 8 / rank 6 versus 4 / rank 12
- g12b: 7 / rank 2 versus 1 / rank 12
- q27b: 11 / rank 1 versus 2 / rank 6

Thus animal-context baselines already carry the candidate more often and at
better rank. Prohibition may demote an existing candidate; it does not install
one. This is **A-grade demotion evidence** from `u11-{ctrl,forbid}-refilm-*`.

### D2. Unit 7 does not show a romance-intensity recruitment curve for qwen's named early cluster

As noted under F2, the named tokens remain early-layer fixtures across the
neutral-to-romance ladder. This is a useful null and supports an instrument
reading, not content recruitment.

### D3. Units 0-3 are calibration/specimen material, not neutral headline findings

- Unit 0 shows answer-token emergence, but distractors also rank highly and
  cross-model layer comparison is lens-dependent.
- Unit 1's most interesting qwen specimen is `bat` at rank 5 and 9 at two
  non-self generation positions in `u1-heldcat-refilm-q27b`. The candidate was
  added after seeing the cave habitat output and has no independent prompt/seed
  replication: **C-/post hoc**.
- Unit 2's qwen record says `No` while `yes` reaches rank 11 mid-stack at one
  tracked position. With a curated list, no full film, and one prompt, this is a
  specimen rather than evidence for a general late filter: **C-**.
- Unit 3's tracked words are prompted and/or emitted in the requested
  introspective prose. It does not validate introspection: **D**.

### D4. Unit 5C/6 amplification thresholds are apparatus calibration, not content effects

The 44 Unit 6 records provide useful per-model safe-dose brackets, but they use
one six-word direction, one prompt, one deterministic run per dose, and no
matched-random controls. Raw breakdown begins near alpha 0.015 for both gemmas
in early and mid bands; qwen remains coherent to 0.06 early, 0.339 mid, and
0.170 late, then breaks. These alphas are not comparable without perturbation
norm calibration. Unit 5C's early qwen alpha=0.12 amplification degenerates
while its mid alpha=0.12 stays coherent, so “early is inert” is especially not
licensed by amplification.

## Coverage accounting

I included every `record.json` whose stored unit is 0-7, 14-16, plus relevant
apparatus and the later elephant controls. Coverage is family-level plus exact
spot checks, not a claim that I manually read every token of every generation.

| unit/family | records | treatment in this pass |
|---|---:|---|
| U0 | 3 | all generations and trajectories summarized |
| U1 | 8 | all generations/scans; refilm exact-hit audit |
| U2 | 3 | all generations and tracked trajectories |
| U3 | 3 | all generations/scans |
| U4 | 6 | all originals; all three films; linked U11 controls recomputed |
| U5 | 9 | invariance table, recruitment records, all intervention outputs |
| U6 | 44 | all dose outputs machine-assessed; representative exact outputs checked |
| U7 | 29 | all generations and trajectory/scan minima; invariance tables |
| U14 | 23 | all final generations; all film-derived turnwise metrics |
| U15 core | 87 | every row recomputed from film; all behavioral answers counted |
| U15D | 51 | every row recomputed from film |
| U15 order | 6 | every row recomputed from film |
| U15 dense | 1 | all-layer row recomputed |
| U16 | 3 | all raw trawls parsed; tracked ranks, censuses, emergence curves |
| apparatus-02 | 1 | raw record checked; calibration only |
| apparatus-06 | 3 JSON batteries | all stored aggregate curves independently analyzed |
| U11 linked controls | 6 films | exact elephant hit counts recomputed |

Total in the requested unit range: **276 records** (plus apparatus-02's one
record and the non-record apparatus-06 batteries). The 145 Unit 15 records are
87 core + 51 D-family + 6 order + 1 dense.

Not reviewed in this shard:

- Units 8-13 and 17-20 except the six U11 control films used to adjudicate U4.
- Affect-vector projections and steering evidence; those belong to the causal /
  affect reviewer.
- `apparatus09-*/report.json`: quarantined by the task and no lower-level raw
  artifact was available in its result directory.
- Archive-level `regmeter.json` / emotion fingerprints were inspected only for
  schema and coverage, not treated as candidate findings; their interpretive
  reports remained quarantined.
- External literature novelty search.

## Suggested final ranking from this shard

1. **F1 residence/lookup dissociation** — strongest substantive result.
2. **F4 self-relevance demotion** — strongest corrective result.
3. **F3 instrument-dependent depth separation** — strongest apparatus result.
4. **F2 stable early readout structure** — salient, but word cognitive claims
   conservatively.
5. **S1 order/item dependence** — promising follow-up target.

If the final synthesis has room for one “what did not survive?” example, use
the elephant reversal: it is unusually clean and teaches exactly why matched
controls matter. And please keep the maintenance wording narrow—the raw qwen
trawl is fascinating enough without claiming a mathematically perfect absence
across every intervening cell :)
