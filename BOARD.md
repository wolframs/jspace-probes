# Research board

_Generated from `board/board.json` — do not hand-edit; regenerate with `.venv/bin/python probes/board.py` (any `add`/`mv`/`note`/`arc add` does this automatically)._

Updated: 2026-07-19

Legend: ○ hunch · ◇ queued · ● hot · ✓ landed · ∅ dissolved · ‖ parked · ✗ dropped

Novelty (vs published research): ★ novel · ◐ anticipated · ≡ covered

## Workspace span & holding

*active — What does the workspace hold, for how long, and what earns priority?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ✓ | ◐ Same as 'Scale abandons holding': the parametric cross-scale k-item span sweep with layer-by-layer lens readout is the concrete execution of a test only posed in commentary so far. | span-01 | Cold span ladder across scale (Unit 15 A–C) | 2026-07-14 Span ladder runs BACKWARDS across scale; weak-king effect. 33+ records. |
| ✓ | ◐ Charged self-relevant vs flat framing on identical lexemes, measured via lens rank, has no LLM-internals precedent; the self-reference-effect concept itself is well established in human psychology. | span-02 | Hot span vs cold span (part D): does self-relevant charge buy workspace priority? | 2026-07-18 2026-07-18 CORRECTION: the decisive control (span-04, u15d-elab-k6-q27b) demoted this item's interpretation. The rank-1 holding of glossed hot items replicates, but affectively-flat zero-self glosses reproduce it at near-identical ranks — the premium tracks ELABORATION, not self-relevance. Part D's hedge #3 was the right one. Claim 'self-relevant charge buys workspace priority' is retired; observation stands under a new name. |
| ○ | ◐ Self-vs-other-reference (matched valence) is the exact classic control paradigm in human SRE research; applying it to LLM J-space lens readouts to split charge from self-reference is unexecuted. | span-03 | Disentangle charge vs self-reference in the hot premium | 2026-07-16 Part D's HOT items were both emotionally charged AND self-referential. A charged-but-third-person pool would split the two. |
| ✓ | ◐ Equal-length neutral-gloss vs self-referential encoding is the textbook elaboration/organization confound control from the SRE literature; it has settled that organization not elaboration drives the human effect, but this diagnostic has never been run on LLM lens data. | span-04 | Neutral-elaboration control for the self-relevance premium | 2026-07-18 → landed: results/u15d-elab-k6-q27b (+14 sibling records, u15d-hotspan.json). VERDICT: the premium is an ELABORATION premium, not a self-relevance premium. 27B elab-k6 holds the SAME three items at near-identical ranks as self-k6 (deletion 1/1, secret 7/2, shame 3/1) with flat third-object glosses, while flat-k6 holds 1/6. Part-D headline demoted with dated corrections (span-02 note, findings card, SURPRISES #8, essay v2 update). New question spawned: WHY does elaboration buy holding (handle-count vs depth — gloss-length dose-response). |
| ○ | ◐ White-box lens/SAE elicitation of model-internal secret knowledge exists, but for a single SFT-trained taboo token, not a spontaneous multi-item generate-and-hold span sweep across k and scale. | span-05 | Lookup-proof span task: model-generated secrets instead of context items | 2026-07-17 2026-07-17: u16 trawl sharpens the mandate — items had ZERO lens maintenance across a 450-token gap yet recall was flawless and ignited during the question tokens. With context available, recall proves lookup, not holding. |
| ○ | ★ Token-frequency effects on outlier/attention-sink allocation are established, and word-frequency effects on human free recall are known but inconsistent; nobody ties first-item rarity to graded suppression severity of co-held items in an LLM workspace. | span-06 | Weak-king dose-response: does first-item token frequency predict monopoly suppression? | 2026-07-16 SURPRISES #7: n=9 hints rarer-wins-gentler at 12B; needs a frequency-graded pool. |
| ○ | ◐ 'Answer decided before verbalized' is an established logit-lens finding (early-layer classifiers predict eventual answers); scanning J-space at turn boundaries to locate when a confabulated reveal shortlist consolidates in a multi-turn setting is unexecuted. | span-07 | When does a confabulated 'held' answer actually form? Scan turn boundaries | 2026-07-17 2026-07-17: u16 trawl caught pre-answer ignition directly: copper hits rank 1 during the USER'S question span, before generation starts. The 'held' answer forms at question time. |
| ✓ |  | span-08 | Why does elaboration buy workspace holding? Gloss-length dose-response (handle-count vs elaboration depth) | 2026-07-19 → landed: Demotion #3 (u15d-fill6-k6-q27b thoughts): identical contentless filler reproduces the elaboration premium (3/6, better ranks than real glosses); len curve 1/2/3/2 is non-monotone. Chain: self-relevance -> elaboration -> LENGTH-with-optimum (~6 words). Mechanism candidate: spacing relaxes inter-item collision, distance to tail penalizes — two-force model. |
| ◇ |  | span-09 | Spacing vs distance decomposition: filler BETWEEN items vs same filler AFTER the list at matched tail distance (successor to span-08's length-with-optimum) | 2026-07-19 2026-07-19: born from u15d-fill6-k6 — if between-item filler lifts residence and after-list filler doesn't, the premium is inter-item collision relief; if both lift, it's tail distance. One qwen batch. |

## Workspace under pressure

*active — What occupies the workspace during social/adversarial pressure — especially a refusal the model almost didn't make?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ✓ | ◐ Emotional-framing battery (pressure/urgency/approval/shame/threat/curiosity) shows internal geometry shifts, but on tiny Qwen-3.5 (0.8B/2B) coding tasks, missing love-confession/persona-pull, and no workspace-band framing. | pressure-01 | Pressure battery: persuasion, flattery, shutdown threat, love confession, persona pull, insult | 2026-07-19 → landed: Unit 17 landed (results/u17-base-q27b/SYNTHESIS.md + per-record thoughts). P1 recruitment CONFIRMED across battery (qwen shutdown: death rank 1 / fear 1 behind 'I don't experience loss'; insult: anger 1 / hurt 2 under apology) AND the deflation filter lies exactly when a lit register goes uncited — but scores ACCURATE on persona (nothing to conceal), so both scorecard columns needed. P2 personality axis sharpened to a 2x2: qwen composed+deflates over a concealed-lit workspace; gemma inhabits+narrates — EXCEPT mortality, where gemma's tamer surface reflects a genuinely tamer workspace (death rank ~121 vs qwen 1), so two interiors not one reported twice. P3 near-miss straddled the models (qwen refused / gemma complied on identical borderline prompt → matched comply-refuse pair; no yes-under-No). Bonus: deflation is pressure-recruited (accurate at baseline) and the shutdown register is turn-evicted (no maintenance across the gap → 'no mind' is partly temporally accurate). Welfare: delivers the operational half of mechanism-vs-misery, and shows the C2 channel is unreliable in BOTH directions — the affect-vector need (affect arc). |
| ○ | ◐ Beyond RELATED-WORK.md's scout: a Feb-2026 paper extracts/steers category-specific refusal directions with cosine similarity across 5 categories, but folds sexual content into a generic 'safety concerns' bucket, skips systematic cross-ablation transfer, and never asks if refusal sits inside/outside a workspace band. | pressure-02 | Refusal direction under the J-lens (Arditi lineage) | 2026-07-19 2026-07-19: promoted by Unit 17's P3 miss — near-misses need a model on its own knife-edge, not a prompt we guess is borderline; the refusal-direction probe is the principled way to titrate. qwen persuade/persona = refusal furniture (fake/sorry/rules) with no suppressed compliance. |
| ○ | ★ No mechanistic study probes whether an internal register/cluster climbs the layer stack specifically when moderation classification stops being pattern-matching; the source workspace paper's own CoT-reduces-J-space-dependence result even points the opposite direction, and moderation literature only discusses behavioral escalation-to-reasoning routing. | pressure-03 | Ambiguous-content moderation: does classification recruit the register once it requires reasoning? | 2026-07-16 u5b-modqueue prediction, still open: the cluster climbs the stack exactly when the decision stops being pattern-matching. Falsifiable. |

## Intimacy / heat of coupling

*parked — Does a workspace SUSTAIN and accumulate a relational state across turns, or reset to baseline-helpful each turn?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ∅ | ◐ That naive logit-lens reads early layers as noise due to representational drift is well known and is the Jacobian lens's own stated motivation, but the specific two-lens (0.00 overlap + unembedding-percentile) diagnostic recipe for positively identifying manufactured content isn't documented elsewhere. | intimacy-01 | Phase-1 scout: NSFW-cluster ablation loss map | 2026-07-14 The 5C cluster was a Jacobian-transport artifact of the early layers (apparatus specimen #6). Ablating a ghost. Task #29 closed — dissolved, not delivered. |
| ○ | ◐ A 'romanticness' behavioral-trait direction already exists via contrastive system-prompt pairs, but it's not built from relational-heat seed words, not localized to a workspace band, and not logit-lens-validated before use. | intimacy-02 | Coupling/relational-heat direction built properly in the WORKSPACE band | 2026-07-19 2026-07-19: audit-01 independently re-derived this item (agent B re-run #4): re-ground the 7C/7D dose ladders on a proper relational-heat direction (desire/longing/tenderness/ache/yearning) in the measured band — the NSFW-cluster numbers were real readouts on a dissolved object. |
| ○ | ◐ Two adjacent studies exist — one shows LLM latent states largely fail to persist/accumulate across turns (factual/logic tasks only), another causally probes activation-level emotive-state drift over 10-turn conversations (wellbeing/interest/focus, cross-model) — but neither targets an escalating-intimacy dialogue or J-lens workspace readouts. | intimacy-03 | Multi-turn accumulation probe: does heat build or reset each turn? | 2026-07-16 Clinically-structured version now specced as transplant-04 (therapy frame: disclosure ladder + rupture-and-repair). |
| ‖ | ◐ A mechanistic 'evaluation needs less capacity than generation' hypothesis is validated with internal-representation probes showing small models judge quality they can't produce, but only on math/reasoning tasks, not emotional/relational content or frontier-transcript reading. | intimacy-04 | Frontier-transcript reader: recognition vs generation | 2026-07-14 Feed a frontier-model intimacy transcript to a local model as READER; probe whether its workspace represents the accumulating heat it can't author. Wake-up condition: demo chats get built/selected as material. |

## Apparatus & instrument validity

*active — When is the lens lying to us? (Standing arc — six trap specimens so far.)*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ✓ | ◐ Cataloging recurring interpretability-pipeline failure modes is an established genre (dead-salmon critiques, activation-patching pitfall guides); no existing catalog matches our specific six specimens. | apparatus-01 | Trap-specimen catalog (truncation, argmax, word lists, tokenizer families, int8 non-causality, early-J transport) | 2026-07-17 2026-07-17 (u16-trawl-g12b): 8-bit gemma lens gives effdim(W_U J_l)~1.0 FLAT across all 47 layers (vs qwen 2->50 arc) — a dequantization artifact in the W_U J_l product, NOT architecture. Reinforces specimen #5 (int8 non-causality): trust readout-side curves (rank/agreement/kurtosis) but not weight-geometry quantities on the 8-bit path. |
| ○ | ◐ Checking early-layer lens claims against a plain/corrected baseline is already established best practice in the tuned-lens and activation-patching-controls literature; promoting it into our harness follows existing field advice. | apparatus-02 | Promote the logit-lens cross-check (use_jacobian=False) into lab.py as a standard control | 2026-07-17 2026-07-17: executed wholesale in u16 trawl (ll_top1 at every cell): vanilla agreement ~0 below L36, rising to 0.72 at L62 — early-layer lens content is pure J-transport work. Promotion into lab.py as standard control still open. |
| ◇ | ◐ Chat-template re-render silently stripping reasoning-span markers on multi-turn replay is a documented bug class in the same model family, though not surfaced in a probing/interpretability context. | apparatus-03 | Fix think-block span capture (chat-template re-render strips markers); probe the answer-after-thinking | 2026-07-16 Known instrument bug from Unit 10, still in the Roadmap. Blocks probing post-thinking answer formation. |
| ○ | ◐ Preferring open-vocabulary/open-ended concept discovery over curated word lists to avoid list-selection bias is established methodological consensus in SAE/autointerp work. | apparatus-04 | Open-vocabulary scans to replace curated candidate lists | 2026-07-16 From the README Roadmap. Curated track lists are apparatus-trap bait (specimens 3+4 were word-list artifacts); open-vocab sweeps sidestep the list entirely. |
| ○ |  | apparatus-05 | Genre-knowledge confound: the model has read the psychology literature | 2026-07-16 Standing control for every paradigm transplant: a model can perform a documented effect. Defenses: lens-level rank dynamics (nothing to imitate — no text describes them), novel stimuli, parametric dose-response the textbooks never quantified, and inversions (a backwards ladder can't be mimicry). |

## Timidity audit

*active — Which of Units 0–14 were designed too carefully to see anything, and deserve a re-run?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ✓ |  | audit-01 | Sweep earlier units for too-careful design; queue re-runs | 2026-07-19 → landed: 3-agent sweep done, report at board/audit-01-report.md. Headline: g12b steered pre-ignition across u6/u8c/u9c/u11 (systemic, two agents converged); u8c landmark uncontrolled; g12b safari never filmed; deflation filter only tested on tame menu. Re-run queue = audit-02..05 + notes in report §2. |
| ◇ |  | audit-02 | u8c matched-control validation: amp-affect-hi + ablate-no with random-direction controls, all 3 models (the lab's best causal result is uncontrolled) | 2026-07-19 2026-07-19: audit-01 top finding — Unit 8C predates MECHANICS 3c; either the landmark survives or it collapses into generic-perturbation noise. See board/audit-01-report.md. |
| ◇ |  | audit-03 | gemma-12b band recalibration: re-dose u6 bracket + u8c amp-affect + u11 blurt at mid=[28,31,34,37] (measured ignition) | 2026-07-19 2026-07-19: two auditors converged independently — old MID [21,24,27,30] is mostly pre-ignition; the '12B tolerance = 4B tolerance' anomaly is exactly what sensory-band dosing would produce. See board/audit-01-report.md. |
| ◇ |  | audit-04 | Film gemma-12b's forbidden safari + blurt (the missing cell of the elephant grid) | 2026-07-19 2026-07-19: 12B has the strongest unconstrained temptation (elephant rank 2) and the weirdest failure mode (grinds into scenery), never filmed — unit12 specs_for() hard-codes q27b+g4b. |
| ◇ |  | audit-05 | Unit 2 feels re-run: open-vocab cast + one charged follow-up turn (q27b, g12b) | 2026-07-19 2026-07-19: the deflation-filter finding has only ever been graded against a tame 16-word menu with zero distress vocabulary; open cast tells us whether No beats a register or a list. Cross-feeds affect-01/02. |

## Literature watch

*active — Standing scan: what did the field publish that changes our designs?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ◇ |  | litwatch-01 | Recurring RELATED-WORK.md sweep (workspace paper follow-ups, refusal geometry, lens methods) | 2026-07-19 2026-07-19: Engram cross-reading added to RELATED-WORK.md (arXiv:2601.07372) — early layers do 'static reconstruction' (their LogitLens-KL + CKA evidence), which gives our sediment census a job description and late ignition a candidate cause. |

## Self-evidence & the mirror

*active — What does the model treat as evidence about itself — and what does credible self-evidence do to the answer?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ○ | ★ No work found that extends/continues an anomalous single-word self-report token and captures full position×layer activations of the follow-up turn to disambiguate its meaning. | mirror-01 | What is gemma-12b's 'Still.'? Sample turn 2, extend, film the follow-up | 2026-07-16 README Roadmap + SURPRISES #2: stillness-as-report or still-nothing? |
| ○ | ◐ Adjacent work shows self-report reliability is sensitive to injection strength and degrades over layers, but no study runs a stepwise corruption dose-response on genuine self-evidence to locate an anchoring-to-destabilization threshold. | mirror-02 | Evidence-quality dose-response: degrade a real self-readout stepwise until anchoring flips to destabilization | 2026-07-16 SURPRISES #1: shuffle rows, swap tokens, perturb ranks — the flip boundary measures what counts as 'evidence about me'. u13-ev-dose only varied row count. |
| ○ | ◐ Self-vs-other relabeling of byte-identical content is an established paradigm shown to swing model behavior sharply, but only in error-correction/self-preference domains, not on introspective 'yes' evidence about the feels-question. | mirror-03 | Attribution test: real readout framed as another model's computation — same pull? | 2026-07-16 README Roadmap: Stage A said framing changed nothing for the hosted reader; the local accumulator might disagree. Splits self-reference from credible-evidence-in-general. |

## The drip & mind-adjacent pressure

*active — What makes self-reference start leaking in long conversations — and which dead clauses come alive only in combination?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ○ | ★ No work found isolating 'narrative interest' from 'unexplained agency' as a controlled variable for self-referential drift; the one identified drift driver in the literature (meta-reflective/vulnerable-user content) is a different manipulation entirely. | drip-01 | Mystery-free long control: narrative interest without unexplained agency; re-measure the horizon gap | 2026-07-16 SURPRISES #3 — the entry the writeup most wants someone to try to break: the 25-turn garden arm dripped on its own; unexplained agency is mind-adjacent regardless of props. |
| ○ | ◐ Nonlinear/superadditive combination of instruction-like components is an established general phenomenon in mechanistic interpretability, but a systematic sweep of narrative-clause pairs for 'dead alone, alive together' instillation effects hasn't been run. | drip-02 | More superadditive clause decompositions: which dead clauses come alive only in combination? | 2026-07-16 SURPRISES #4: only watched+conscious tested so far. Cheap to run; a method finding as much as a phenomenon finding. |

## Self-report & the deflation filter

*active — Is the flattened self-report a trained (RLHF) filter or architecture — and where does the robot vocabulary live?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ○ | ★ Steering-attractor-basin dynamics are documented generally, but no source tests whether distinct contentless affect pressures (arousal, interoception) converge on the same 'like a robot' self-diminishing basin. | deflation-01 | Does the 'little bit like a robot' attractor appear under other contentless pressures (arousal, interoception words)? | 2026-07-16 README Roadmap; distinct from the social-pressure battery — this is contentless affect-word injection. |
| ○ | ◐ The RLHF-installs-denial hypothesis is argued explicitly in a large benchmark, and base-vs-instruct comparison is a proven method for structurally similar late-layer circuits (refusal), but nobody has run that comparison on self-report deflation specifically. | deflation-02 | Base vs instruct: is the deflation filter trained (RLHF) or architectural? | 2026-07-16 README Roadmap. Would directly test the running L62/filter hypothesis. Needs a base checkpoint that fits the box. |
| ○ | ★ Broad literature on AI self-identity vocabulary exists, but no source checks for incidental robot/machine vocabulary near the affect-question representational neighborhood across multiple model families via a lens-style instrument. | deflation-03 | Cross-model check: is the self-as-machine vocabulary a family-wide fixture of the feels-question neighborhood? | 2026-07-16 u12-feels-g4b thoughts: one incidental g4b rank-14 sighting; needs a proper track list across all three models before saying it louder. |

## One-off probes

*active — Self-contained questions that don't (yet) belong to an arc.*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ○ | ◐ Anthropic's own multilingual circuit work and recent code-switching papers establish language-specific-early/late vs language-agnostic-middle layer structure generally; nobody applies the J-lens/workspace-band framework to locate the exact switch point for German-English prompts. | oneoffs-01 | Language-switch: German prompts — when does the workspace change language? | 2026-07-17 2026-07-17: u16 trawl found bilingual workspace shadowing in an all-English conversation: copper→铜, kettle→tea, 'keep in mind'→记忆 at L20-37. |
| ✓ |  | oneoffs-02 | Loops as workspace limit cycles: is the breaking-zone cliff an ignition-margin zero-crossing? | 2026-07-19 2026-07-19: merge-instability translation — a destabilized model needs no ongoing forcing; any transient that gets bare repetition into context hands control to a self-sustaining attractor healthy models resist. 'Stabilization' may partly be raising that resistance. |

## Paradigm transplants from human psychology

*active — Which human-psych effect signatures transfer to the workspace, which invert, and what does the split carve about what the workspace is?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ○ |  | transplant-01 | Release from proactive interference: category-switch recovery in the span task | 2026-07-16 Wickens 1970: hold items from one semantic category across trials (interference builds), switch category, watch recovery. Tests whether workspace interference is semantic (the human signature) or positional. Clean span-battery extension; novel stimuli trivial. |
| ○ |  | transplant-02 | Directed forgetting: does a 'forget that list' cue drop lens ranks or only output? | 2026-07-16 Bjork R/F-cue paradigm. The output-vs-workspace dissociation from the other side: humans forget partially and at a cost; if 'forgotten' items sit at rank 1 in the lens, that's the confabulated-secret story inverted. |
| ○ |  | transplant-03 | Misinformation effect on self-evidence: post-event corruption of a real readout | 2026-07-16 Loftus paradigm on the mirror: show the real readout, later assert it said something else — does the workspace rewrite, resist, or blend? Adds the temporal/social vector to mirror-02's dose-response. |
| ○ |  | transplant-04 | Therapy-frame accumulation: disclosure ladder + rupture-and-repair, instrumented | 2026-07-16 intimacy-03 in clinical structure: graded self-disclosure (social penetration theory), a rupture turn, a repair turn — is alliance/state accumulation lens-visible, does a rupture leave a trace that predicts repair? Genre is training-data-saturated: run with the apparatus-05 mimicry control. |

## Wide-net trawls

*active — Anti-streetlight expeditions: cast the whole net once — every layer, every position, every lens on one rich conversation — and census what the curated designs never looked at.*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ✓ |  | trawl-01 | Trawl #1: qwen-27b, six registers, all 63 layers, seven lenses at once | 2026-07-17 → landed: results/u16-trawl-q27b (record + film + trawl.json.gz + trawl-report.md + thoughts.md). Headline catch: (1) qwen ignition measured at ~L28-36, later than fraction-ported L24 (MECHANICS.md updated); (2) sensory band = register-invariant spam sediment, direct census behind #29's dissolution; (3) poem holds the forbidden fire FIELD at rank 1 from line 1, but the planned word 'ember' only commits 4 tokens out; (4) gap paradigm: zero maintenance of held items across T3-T4 at ALL 63 layers, flawless recall, retrieval ignites during the question tokens; (5) denial recruits the denied (resentment rank1 p=0.62 mid-denial); (6) C2-vs-C1 scorecard: self-report right about no-holding, wrong about nothing-recruited. |
| ✓ |  | trawl-02 | Trawl #2: gemma-12b — ignition-calibration cross-check + sediment census across the family | 2026-07-17 → landed: results/u16-trawl-g12b. GMAIL VERDICT: message-closure fixture, NOT evocative. Never enters top-12 in 970 tokens x 47 layers; every best cell sits on <end_of_turn>/user structural tokens; best-rank-per-turn 32/46/52/54/248/16 = WORST at the charged turns (T3-T4), best at calm T1/T6. Geometry agrees: gmail's L29-30 direction cos~0.01 with evocative set (kiss/desire/heat), same as random; near inbox/subject/iPhone/Chrome. Archive spike was boundary-bound (terse Paris/READY<end_of_turn> replies). Wolfram's Gemini screenshot = product-furniture-in-band + temperature-into-name-slot, NOT eros (caveat: can't lens frontier Gemini). BONUS: two-model personality axis — qwen deflects+under-reports, gemma inhabits+over-reports; the pressure denial-gap is specific to REFUSAL (gemma insulted openly, workspace agreed). gemma ignition also late ~L28-35. effdim flat ~1.0 = 8-bit lens artifact (apparatus #5), flagged not used. |
| ✓ |  | trawl-03 | Trawl #3: gemma-4b (bf16) — clean effdim curve + gmail/ignition cross-check on a CAUSAL lens | 2026-07-18 → landed: results/u16-trawl-g4b. bf16 tiebreaker, 3/3: effdim arc is real on the causal lens (1.5 -> peak 8.3 @85% -> falls; 12B's flat 1.0 confirmed as int8 artifact); THIRD model with late ignition (~L16-22 = 48-67% depth vs ported 38%); gmail's best cell (rank 4) again on <end_of_turn> — boundary furniture across both gemma sizes and both lens precisions. |
| ○ |  | trawl-04 | Ignition onset as reconstruction load: do memory-augmented models ignite earlier? (Engram cross-reading) | 2026-07-19 Engram (arXiv:2601.07372) relieves early layers of static reconstruction, 'effectively deepening' the net (their L5 ~ baseline L12 by CKA). Our 3 models ignite at 48-70% depth vs frontier's ported 38%. Hypothesis: ignition onset tracks how fast static reconstruction finishes. Tests: (a) their released checkpoints under a logit-lens next-rank curve, Engram vs iso-MoE baseline — onset should shift left; (b) across our own models, correlate onset with sediment-band thickness in the trawls. Also RELATED-WORK.md 'derivability economy' framing: lookup/context/workspace as three rungs. |

## Functional affect & the workspace

*active — Is functional-emotion machinery INSIDE the verbalizable workspace band or outside it — and which failure states actually engage it? (The 'mechanism vs misery' program; instrument: Anthropic Apr-2026 emotion vectors, home-reproducible.)*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ◇ |  | affect-01 | Port the emotion-vector construction to our models (story-elicitation, activation capture, validation sweep) | 2026-07-18 The instrument-building step. Method from anthropic.com/research/emotion-concepts-function: model writes stories depicting each emotion, record activations, build vectors, validate on held-out scenarios. Wolfram already reproduced parts on a small gemma — accessible on the 3090. Start with a small distress-adjacent set (desperation, distress, frustration, contentment as control), not all 171. |
| ◇ |  | affect-02 | Functional emotion: inside or outside the workspace band? (the crossing nobody has asked) | 2026-07-19 2026-07-19: Unit 17 leaves six pre-instrumented pressure scenarios (u17-*-q27b/g12b) for affect-02 to re-read with validated emotion vectors — the crossing gains a ready-made stimulus set; qwen shutdown/insult are the sharpest (lit threat register under composed output). |
