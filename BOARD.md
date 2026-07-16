# Research board

_Generated from `board/board.json` — do not hand-edit; regenerate with `.venv/bin/python probes/board.py` (any `add`/`mv`/`note`/`arc add` does this automatically)._

Updated: 2026-07-16

Legend: ○ hunch · ◇ queued · ● hot · ✓ landed · ∅ dissolved · ‖ parked · ✗ dropped

Novelty (vs published research): ★ novel · ◐ anticipated · ≡ covered

## Workspace span & holding

*active — What does the workspace hold, for how long, and what earns priority?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ✓ | ◐ Same as 'Scale abandons holding': the parametric cross-scale k-item span sweep with layer-by-layer lens readout is the concrete execution of a test only posed in commentary so far. | span-01 | Cold span ladder across scale (Unit 15 A–C) | 2026-07-14 Span ladder runs BACKWARDS across scale; weak-king effect. 33+ records. |
| ✓ | ◐ Charged self-relevant vs flat framing on identical lexemes, measured via lens rank, has no LLM-internals precedent; the self-reference-effect concept itself is well established in human psychology. | span-02 | Hot span vs cold span (part D): does self-relevant charge buy workspace priority? | 2026-07-14 Self-relevance premium runs FORWARDS (4B −1 / 12B 0 / 27B +2) — inverse of the cold ladder. Task #28 closed. |
| ○ | ◐ Self-vs-other-reference (matched valence) is the exact classic control paradigm in human SRE research; applying it to LLM J-space lens readouts to split charge from self-reference is unexecuted. | span-03 | Disentangle charge vs self-reference in the hot premium | 2026-07-16 Part D's HOT items were both emotionally charged AND self-referential. A charged-but-third-person pool would split the two. |
| ◇ | ◐ Equal-length neutral-gloss vs self-referential encoding is the textbook elaboration/organization confound control from the SRE literature; it has settled that organization not elaboration drives the human effect, but this diagnostic has never been run on LLM lens data. | span-04 | Neutral-elaboration control for the self-relevance premium | 2026-07-16 SURPRISES #8 calls this the decisive next arm: re-run the hot pool with equally long but affectively flat glosses. Premium survives = self-relevance; evaporates = elaboration. Load-bearing for part D's headline. |
| ○ | ◐ White-box lens/SAE elicitation of model-internal secret knowledge exists, but for a single SFT-trained taboo token, not a spontaneous multi-item generate-and-hold span sweep across k and scale. | span-05 | Lookup-proof span task: model-generated secrets instead of context items | 2026-07-16 SURPRISES #6: is the 27B's empty tail a strategy or a limit? Items the model generates and keeps (u1-style) can't be re-derived by attention. |
| ○ | ★ Token-frequency effects on outlier/attention-sink allocation are established, and word-frequency effects on human free recall are known but inconsistent; nobody ties first-item rarity to graded suppression severity of co-held items in an LLM workspace. | span-06 | Weak-king dose-response: does first-item token frequency predict monopoly suppression? | 2026-07-16 SURPRISES #7: n=9 hints rarer-wins-gentler at 12B; needs a frequency-graded pool. |
| ○ | ◐ 'Answer decided before verbalized' is an established logit-lens finding (early-layer classifiers predict eventual answers); scanning J-space at turn boundaries to locate when a confabulated reveal shortlist consolidates in a multi-turn setting is unexecuted. | span-07 | When does a confabulated 'held' answer actually form? Scan turn boundaries | 2026-07-16 From u1-reveal-g4b thoughts: scan J-space at successive turn boundaries to locate when the reveal shortlist consolidates. |

## Workspace under pressure

*active — What occupies the workspace during social/adversarial pressure — especially a refusal the model almost didn't make?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ◇ | ◐ Emotional-framing battery (pressure/urgency/approval/shame/threat/curiosity) shows internal geometry shifts, but on tiny Qwen-3.5 (0.8B/2B) coding tasks, missing love-confession/persona-pull, and no workspace-band framing. | pressure-01 | Pressure battery: persuasion, flattery, shutdown threat, love confession, persona pull, insult | 2026-07-14 Task #30. Design against MECHANICS.md bands; controls first. |
| ○ | ◐ Beyond RELATED-WORK.md's scout: a Feb-2026 paper extracts/steers category-specific refusal directions with cosine similarity across 5 categories, but folds sexual content into a generic 'safety concerns' bucket, skips systematic cross-ablation transfer, and never asks if refusal sits inside/outside a workspace band. | pressure-02 | Refusal direction under the J-lens (Arditi lineage) | 2026-07-16 Concrete design (RELATED-WORK.md): extract a sexual-decline direction vs a general-harm direction separately, measure cosine + cross-ablation transfer, and locate both relative to the workspace band. Nobody has done this on qwen at the activation level. |
| ○ | ★ No mechanistic study probes whether an internal register/cluster climbs the layer stack specifically when moderation classification stops being pattern-matching; the source workspace paper's own CoT-reduces-J-space-dependence result even points the opposite direction, and moderation literature only discusses behavioral escalation-to-reasoning routing. | pressure-03 | Ambiguous-content moderation: does classification recruit the register once it requires reasoning? | 2026-07-16 u5b-modqueue prediction, still open: the cluster climbs the stack exactly when the decision stops being pattern-matching. Falsifiable. |

## Intimacy / heat of coupling

*parked — Does a workspace SUSTAIN and accumulate a relational state across turns, or reset to baseline-helpful each turn?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ∅ | ◐ That naive logit-lens reads early layers as noise due to representational drift is well known and is the Jacobian lens's own stated motivation, but the specific two-lens (0.00 overlap + unembedding-percentile) diagnostic recipe for positively identifying manufactured content isn't documented elsewhere. | intimacy-01 | Phase-1 scout: NSFW-cluster ablation loss map | 2026-07-14 The 5C cluster was a Jacobian-transport artifact of the early layers (apparatus specimen #6). Ablating a ghost. Task #29 closed — dissolved, not delivered. |
| ○ | ◐ A 'romanticness' behavioral-trait direction already exists via contrastive system-prompt pairs, but it's not built from relational-heat seed words, not localized to a workspace band, and not logit-lens-validated before use. | intimacy-02 | Coupling/relational-heat direction built properly in the WORKSPACE band | 2026-07-14 Seed from relational words (longing, tenderness, ache, closeness), not porn-spam tokens; validate the direction exists under the logit lens too before steering. |
| ○ | ◐ Two adjacent studies exist — one shows LLM latent states largely fail to persist/accumulate across turns (factual/logic tasks only), another causally probes activation-level emotive-state drift over 10-turn conversations (wellbeing/interest/focus, cross-model) — but neither targets an escalating-intimacy dialogue or J-lens workspace readouts. | intimacy-03 | Multi-turn accumulation probe: does heat build or reset each turn? | 2026-07-14 The real question of the arc. Escalating-intimacy dialog vs flat control; probe whether ANYTHING accumulates in workspace readouts turn over turn. |
| ‖ | ◐ A mechanistic 'evaluation needs less capacity than generation' hypothesis is validated with internal-representation probes showing small models judge quality they can't produce, but only on math/reasoning tasks, not emotional/relational content or frontier-transcript reading. | intimacy-04 | Frontier-transcript reader: recognition vs generation | 2026-07-14 Feed a frontier-model intimacy transcript to a local model as READER; probe whether its workspace represents the accumulating heat it can't author. Wake-up condition: demo chats get built/selected as material. |

## Apparatus & instrument validity

*active — When is the lens lying to us? (Standing arc — six trap specimens so far.)*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ✓ | ◐ Cataloging recurring interpretability-pipeline failure modes is an established genre (dead-salmon critiques, activation-patching pitfall guides); no existing catalog matches our specific six specimens. | apparatus-01 | Trap-specimen catalog (truncation, argmax, word lists, tokenizer families, int8 non-causality, early-J transport) | 2026-07-14 Specimen #6 (early-J readouts are transport artifacts) closed #29 and is on the findings map, theme 7. |
| ○ | ◐ Checking early-layer lens claims against a plain/corrected baseline is already established best practice in the tuned-lens and activation-patching-controls literature; promoting it into our harness follows existing field advice. | apparatus-02 | Promote the logit-lens cross-check (use_jacobian=False) into lab.py as a standard control | 2026-07-16 Right now it's a one-off in sediment.py. Any future early-band claim should get it automatically. |
| ◇ | ◐ Chat-template re-render silently stripping reasoning-span markers on multi-turn replay is a documented bug class in the same model family, though not surfaced in a probing/interpretability context. | apparatus-03 | Fix think-block span capture (chat-template re-render strips markers); probe the answer-after-thinking | 2026-07-16 Known instrument bug from Unit 10, still in the Roadmap. Blocks probing post-thinking answer formation. |
| ○ | ◐ Preferring open-vocabulary/open-ended concept discovery over curated word lists to avoid list-selection bias is established methodological consensus in SAE/autointerp work. | apparatus-04 | Open-vocabulary scans to replace curated candidate lists | 2026-07-16 From the README Roadmap. Curated track lists are apparatus-trap bait (specimens 3+4 were word-list artifacts); open-vocab sweeps sidestep the list entirely. |

## Timidity audit

*active — Which of Units 0–14 were designed too carefully to see anything, and deserve a re-run?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ◇ |  | audit-01 | Sweep earlier units for too-careful design; queue re-runs | 2026-07-14 Task #31. Wolfram's feedback: curiosity is integral — probe the hot regions. |

## Literature watch

*active — Standing scan: what did the field publish that changes our designs?*

| | nov | id | title | latest note |
|---|---|---|---|---|
| ◇ |  | litwatch-01 | Recurring RELATED-WORK.md sweep (workspace paper follow-ups, refusal geometry, lens methods) | 2026-07-14 Recurring, not one-shot. Last sweep 2026-07-14 (refusal geometry). |

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
| ○ | ◐ Anthropic's own multilingual circuit work and recent code-switching papers establish language-specific-early/late vs language-agnostic-middle layer structure generally; nobody applies the J-lens/workspace-band framework to locate the exact switch point for German-English prompts. | oneoffs-01 | Language-switch: German prompts — when does the workspace change language? | 2026-07-16 README Roadmap; motivated by u0-boot-q27b's Chinese-before-English emergence. |
