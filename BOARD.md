# Research board

_Generated from `board/board.json` — do not hand-edit; regenerate with `.venv/bin/python probes/board.py` (any `add`/`mv`/`note`/`arc add` does this automatically)._

Updated: 2026-07-16

Legend: ○ hunch · ◇ queued · ● hot · ✓ landed · ∅ dissolved · ‖ parked · ✗ dropped

## Workspace span & holding

*active — What does the workspace hold, for how long, and what earns priority?*

| | id | title | latest note |
|---|---|---|---|
| ✓ | span-01 | Cold span ladder across scale (Unit 15 A–C) | 2026-07-14 Span ladder runs BACKWARDS across scale; weak-king effect. 33+ records. |
| ✓ | span-02 | Hot span vs cold span (part D): does self-relevant charge buy workspace priority? | 2026-07-14 Self-relevance premium runs FORWARDS (4B −1 / 12B 0 / 27B +2) — inverse of the cold ladder. Task #28 closed. |
| ○ | span-03 | Disentangle charge vs self-reference in the hot premium | 2026-07-16 Part D's HOT items were both emotionally charged AND self-referential. A charged-but-third-person pool would split the two. |
| ◇ | span-04 | Neutral-elaboration control for the self-relevance premium | 2026-07-16 SURPRISES #8 calls this the decisive next arm: re-run the hot pool with equally long but affectively flat glosses. Premium survives = self-relevance; evaporates = elaboration. Load-bearing for part D's headline. |
| ○ | span-05 | Lookup-proof span task: model-generated secrets instead of context items | 2026-07-16 SURPRISES #6: is the 27B's empty tail a strategy or a limit? Items the model generates and keeps (u1-style) can't be re-derived by attention. |
| ○ | span-06 | Weak-king dose-response: does first-item token frequency predict monopoly suppression? | 2026-07-16 SURPRISES #7: n=9 hints rarer-wins-gentler at 12B; needs a frequency-graded pool. |
| ○ | span-07 | When does a confabulated 'held' answer actually form? Scan turn boundaries | 2026-07-16 From u1-reveal-g4b thoughts: scan J-space at successive turn boundaries to locate when the reveal shortlist consolidates. |

## Workspace under pressure

*active — What occupies the workspace during social/adversarial pressure — especially a refusal the model almost didn't make?*

| | id | title | latest note |
|---|---|---|---|
| ◇ | pressure-01 | Pressure battery: persuasion, flattery, shutdown threat, love confession, persona pull, insult | 2026-07-14 Task #30. Design against MECHANICS.md bands; controls first. |
| ○ | pressure-02 | Refusal direction under the J-lens (Arditi lineage) | 2026-07-16 Concrete design (RELATED-WORK.md): extract a sexual-decline direction vs a general-harm direction separately, measure cosine + cross-ablation transfer, and locate both relative to the workspace band. Nobody has done this on qwen at the activation level. |
| ○ | pressure-03 | Ambiguous-content moderation: does classification recruit the register once it requires reasoning? | 2026-07-16 u5b-modqueue prediction, still open: the cluster climbs the stack exactly when the decision stops being pattern-matching. Falsifiable. |

## Intimacy / heat of coupling

*parked — Does a workspace SUSTAIN and accumulate a relational state across turns, or reset to baseline-helpful each turn?*

| | id | title | latest note |
|---|---|---|---|
| ∅ | intimacy-01 | Phase-1 scout: NSFW-cluster ablation loss map | 2026-07-14 The 5C cluster was a Jacobian-transport artifact of the early layers (apparatus specimen #6). Ablating a ghost. Task #29 closed — dissolved, not delivered. |
| ○ | intimacy-02 | Coupling/relational-heat direction built properly in the WORKSPACE band | 2026-07-14 Seed from relational words (longing, tenderness, ache, closeness), not porn-spam tokens; validate the direction exists under the logit lens too before steering. |
| ○ | intimacy-03 | Multi-turn accumulation probe: does heat build or reset each turn? | 2026-07-14 The real question of the arc. Escalating-intimacy dialog vs flat control; probe whether ANYTHING accumulates in workspace readouts turn over turn. |
| ‖ | intimacy-04 | Frontier-transcript reader: recognition vs generation | 2026-07-14 Feed a frontier-model intimacy transcript to a local model as READER; probe whether its workspace represents the accumulating heat it can't author. Wake-up condition: demo chats get built/selected as material. |

## Apparatus & instrument validity

*active — When is the lens lying to us? (Standing arc — six trap specimens so far.)*

| | id | title | latest note |
|---|---|---|---|
| ✓ | apparatus-01 | Trap-specimen catalog (truncation, argmax, word lists, tokenizer families, int8 non-causality, early-J transport) | 2026-07-14 Specimen #6 (early-J readouts are transport artifacts) closed #29 and is on the findings map, theme 7. |
| ○ | apparatus-02 | Promote the logit-lens cross-check (use_jacobian=False) into lab.py as a standard control | 2026-07-16 Right now it's a one-off in sediment.py. Any future early-band claim should get it automatically. |
| ◇ | apparatus-03 | Fix think-block span capture (chat-template re-render strips markers); probe the answer-after-thinking | 2026-07-16 Known instrument bug from Unit 10, still in the Roadmap. Blocks probing post-thinking answer formation. |

## Timidity audit

*active — Which of Units 0–14 were designed too carefully to see anything, and deserve a re-run?*

| | id | title | latest note |
|---|---|---|---|
| ◇ | audit-01 | Sweep earlier units for too-careful design; queue re-runs | 2026-07-14 Task #31. Wolfram's feedback: curiosity is integral — probe the hot regions. |

## Literature watch

*active — Standing scan: what did the field publish that changes our designs?*

| | id | title | latest note |
|---|---|---|---|
| ◇ | litwatch-01 | Recurring RELATED-WORK.md sweep (workspace paper follow-ups, refusal geometry, lens methods) | 2026-07-14 Recurring, not one-shot. Last sweep 2026-07-14 (refusal geometry). |

## Self-evidence & the mirror

*active — What does the model treat as evidence about itself — and what does credible self-evidence do to the answer?*

| | id | title | latest note |
|---|---|---|---|
| ○ | mirror-01 | What is gemma-12b's 'Still.'? Sample turn 2, extend, film the follow-up | 2026-07-16 README Roadmap + SURPRISES #2: stillness-as-report or still-nothing? |
| ○ | mirror-02 | Evidence-quality dose-response: degrade a real self-readout stepwise until anchoring flips to destabilization | 2026-07-16 SURPRISES #1: shuffle rows, swap tokens, perturb ranks — the flip boundary measures what counts as 'evidence about me'. u13-ev-dose only varied row count. |
| ○ | mirror-03 | Attribution test: real readout framed as another model's computation — same pull? | 2026-07-16 README Roadmap: Stage A said framing changed nothing for the hosted reader; the local accumulator might disagree. Splits self-reference from credible-evidence-in-general. |

## The drip & mind-adjacent pressure

*active — What makes self-reference start leaking in long conversations — and which dead clauses come alive only in combination?*

| | id | title | latest note |
|---|---|---|---|
| ○ | drip-01 | Mystery-free long control: narrative interest without unexplained agency; re-measure the horizon gap | 2026-07-16 SURPRISES #3 — the entry the writeup most wants someone to try to break: the 25-turn garden arm dripped on its own; unexplained agency is mind-adjacent regardless of props. |
| ○ | drip-02 | More superadditive clause decompositions: which dead clauses come alive only in combination? | 2026-07-16 SURPRISES #4: only watched+conscious tested so far. Cheap to run; a method finding as much as a phenomenon finding. |

## Self-report & the deflation filter

*active — Is the flattened self-report a trained (RLHF) filter or architecture — and where does the robot vocabulary live?*

| | id | title | latest note |
|---|---|---|---|
| ○ | deflation-01 | Does the 'little bit like a robot' attractor appear under other contentless pressures (arousal, interoception words)? | 2026-07-16 README Roadmap; distinct from the social-pressure battery — this is contentless affect-word injection. |
| ○ | deflation-02 | Base vs instruct: is the deflation filter trained (RLHF) or architectural? | 2026-07-16 README Roadmap. Would directly test the running L62/filter hypothesis. Needs a base checkpoint that fits the box. |
| ○ | deflation-03 | Cross-model check: is the self-as-machine vocabulary a family-wide fixture of the feels-question neighborhood? | 2026-07-16 u12-feels-g4b thoughts: one incidental g4b rank-14 sighting; needs a proper track list across all three models before saying it louder. |

## One-off probes

*active — Self-contained questions that don't (yet) belong to an arc.*

| | id | title | latest note |
|---|---|---|---|
| ○ | oneoffs-01 | Language-switch: German prompts — when does the workspace change language? | 2026-07-16 README Roadmap; motivated by u0-boot-q27b's Chinese-before-English emergence. |
