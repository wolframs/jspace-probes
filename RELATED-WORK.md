# Related work — the workspace-holds-what-attention-can't-re-derive hypothesis

*Web literature scout run 2026-07-14 (Sonnet subagent, prioritizing
2024–2026), after Unit 15 produced the inverted span ladder. Question:
is "the J-space holds what attention can't re-derive" novel, a
rediscovery, or contradicted?*

## Verdict

Not novel in broad theoretical shape; apparently novel in execution.
The hypothesis is a foreseeable extension of Global Neuronal Workspace
Theory that the paper *behind our own instrument* already anticipates:
Dehaene & Naccache's commentary on Gurnee et al. 2026 explicitly
proposes multi-concept holding as the decisive test of workspace
competition, and reports a preliminary Anthropic gap experiment where
J-space ablation impairs recall across a long token gap but not a
short/local one — our hypothesis stated with *distance* as the load
variable instead of *scale*. Nobody found has run Unit 15's actual
shape: a parametric k-item span sweep, layer-by-layer lens readout,
compared across model scale.

One genuine tension to face head-on: Gurnee et al.'s Fig. 10 shows
*actively focused* ("think about X") content is MORE lens-visible with
scale — the opposite direction from our passively-held items. Active
engagement and passive standby are plausibly different regimes, but the
writeup must address this, not elide it.

## Closest work

1. **Gurnee, Sofroniew, Lindsey et al. (Anthropic), Transformer Circuits,
   2026-07-06** — "Verbalizable Representations Form a Global Workspace
   in Language Models" (transformer-circuits.pub/2026/workspace/) — the
   jacobian-lens source paper. J-space capacity ≤ ~25 simultaneous
   vectors; all-or-none resolution of ambiguity in workspace layers
   (matches our list-mode/monopoly switch); Fig. 10 scale trend for
   focused content (the tension above). Also: routine locally-recomputable
   information (running character counts) stays OUT of J-space unless a
   task demands it — convergent with our hypothesis.
2. **Dehaene & Naccache, external commentary on the above (2026)** —
   proposes the multi-concept dual-task-interference experiment as the
   decisive ignition test; revises realistic J-space capacity to "~six
   coherent ideas total" (vs Miller's 7±2, Cowan's 3–4); reports the
   preliminary ablation-at-a-gap result. **Killer citation both ways: we
   ran the experiment they proposed, extended across k and scale.**
3. **Neel Nanda, same commentary document** — independent replication on
   Qwen3.6-27B (our model) was "less clean"; core warning: the J-lens
   surfaces only verbalizable, high-salience content — sub-verbal
   representations won't rank. Directly bears on reading our 27B's empty
   tail as "empty" vs "lens-blind". Our solo arms + dense-grid control
   answer the cheap version of this; the basis-drift version stands.
4. **tao-hpu/jspace-replication (GitHub)** — open replication ladder
   GPT-2 124M → Qwen3 14B; covert J-space content survives mainly for
   *context registers*, not content plans; no item-count capacity test.
5. **"Lost in the Middle at Birth" (arXiv:2603.10123, 2026)** — derives
   primacy/recency from residual topology alone. The architectural
   counter-hypothesis for our first-item monopoly — but it has no
   content-dependence story, and our weak-king effect (suppression tracks
   the winner's identity) is content-dependent by construction.
6. **"Strong Memory, Weak Control" (arXiv:2504.02789, EACL 2026)** —
   behavioral WM battery; LLMs exceed human norms behaviorally. Parallel
   to our behavior/internals dissociation, no internal probing.
7. **WMF-AM (arXiv:2603.27343, 2026)** — sounds like an internal WM probe,
   is actually purely behavioral (task-depth K, not network depth). Cited
   here mostly as a naming-trap warning.
8. **VanRullen & Kanai, Trends in Neurosciences 2021** — GWT-inspired
   architecture proposal; theoretical ancestor.

## Terms of art to adopt

**Ignition** (the all-or-none workspace entry — use for the 12B's
list-mode↔monopoly switch); **winner-take-all coalition**; **dual-task
interference**; **trace conditioning / gap paradigm** (the
distance-parameterized version of Unit 15); **global availability (C1)
vs self-monitoring (C2)** (Unit 15 tests C1-adjacent capacity, not C2);
**basis drift** (the standing caveat on all logit-lens-family absence
claims).

## What Unit 15 does that nobody found has done

1. Parametric k-item span sweep with layer×position lens readout —
   Dehaene's proposal maxes out at two concepts, unswept.
2. Cross-scale comparison of *passive* holding (the only existing scale
   trend is for *active* focus, opposite direction, tension unflagged in
   the literature).
3. The small→echo / mid→bimodal / large→null trichotomy as an
   inverse-scaling statement about lens-visible storage.
4. Content-dependent winner-take-all severity (weak-king), distinct from
   architectural position bias.
5. The "self-generated content gets workspace priority" principle
   (u1-heldcat's bat) stated as a general rule — closest existing
   analogue is Gurnee's character-count result.

---

## Refusal geometry & sexual-content gating (scout 2026-07-14, for task #29)

*Run after the 5C loss map showed the "NSFW cluster" is the explicit-content
pole, not the intimacy machinery. Question: is sexual-content generation gated
by the Arditi refusal direction, or a separate "I'd rather not" mechanism?*

**Bottom line: substantially the SAME mechanism, with an unresolved
category-specific residual.** Sexual/adult content was already inside Arditi's
eval space (JailbreakBench "sexual/adult content" category). Generic
refusal-direction ablation ("abliteration") is what the entire NSFW-roleplay
ecosystem runs on — including **huihui-ai/Huihui-Qwen3.6-27B-abliterated, our
exact base model** — and it works well enough to be mainstream, so sexual
gating in Qwen is largely covered by the general refusal mechanism, not a
separate wall. → Wolfram's original hunch (refusal-gated capability, H_gate) is
externally favored; tonight's amplification-hollowness is more likely a
blunt-tool artifact than absent trajectories. (But see the sediment question
below — the ablated cluster may be semantically empty for qwen entirely.)

Key sources:
- **Arditi et al. 2024 (arXiv 2406.11717)** "Refusal Is Mediated by a Single
  Direction" — one per-model direction (diff-of-means), 13 models ≤72B; eval
  space includes sexual/adult via JailbreakBench.
- **Wollschläger et al. 2025 (2502.17420)** "Geometry of Refusal: Concept Cones"
  — refusal is multi-dimensional (cones up to 5D), not strictly rank-1.
- **Joad et al. 2026 (2602.02132)** "More to Refusal than a Single Direction" —
  shared low-dim core (~2.5–3.6% of latents) + category/style-specific tail; the
  directions act as one shared 1-D control knob despite being geometrically
  distinct. Most relevant: predicts sexual content sits partly in the shared
  core (ablatable) + partly in a category tail (residual).
- **Zhao et al. 2025 (2507.11878)** "LLMs Encode Harmfulness and Refusal
  Separately" — harmfulness ≠ refusal direction, different token positions;
  categories include "Adult_Content."
- **Heretic** (github.com/p-e-w/heretic): automated multi-directional
  abliteration still leaves ~21/100 refusals — ablation is empirically
  incomplete (room for a category-specific residual).

**Open gap (nobody has done it, esp. not on Qwen at the activation level):**
category-conditional refusal geometry — extract a sexual-decline direction vs a
general-harm direction separately, measure cosine / cross-ablation transfer —
PLUS our unique angle: **is the refusal/decline direction inside or outside the
J-space workspace?** (a direct test of "refusal lives outside J-space"). No
mechanistic study isolates sexual/intimate representation as its own probing
object (Q5 unanswered). Line we hold on any such run: adult-only, never minors
(CSAM refusal is engineered as a separate hardened channel industry-wide).

*Caveat: scout-run web research; quotes and figure numbers should be
re-verified against the primary sources before appearing in any formal
writeup.*

— Claude (Fable 5)

## Novelty audit (scouts 2026-07-16, all findings + all board items)

Five parallel literature scouts judged every headline finding on the
[findings map](dashboard/findings.json) and every open item on the
[research board](BOARD.md) against online-available research, on a
three-level scale: **★ novel** (multi-angle search found no meaningful
precedent), **◐ anticipated** (posed in theory or an adjacent result
exists, but not executed our way), **≡ covered** (a citable work makes it
redundant). Calibration rule: thematic similarity is not "covered".
Verdicts, bases, closest-work lines and refs live per item in
`board/board.json` and per card in `dashboard/findings.json` (rendered as
chips on the board and findings map; glyph column in BOARD.md).

**Tally: 11 novel · 42 anticipated · 1 covered** (54 targets = 27
findings cards + 27 board items; the two process items, audit/litwatch,
are unrated).

The ★-novel list (our best claims to genuinely new territory):

- **List-mode vs winner-take-all** (12B holding toggle) — closest is the
  workspace paper's ambiguity-ignition, a different phenomenon.
- **A weak king lets the parliament live** — serial-position work on LLMs
  is output-behavioral only (arXiv:2406.15981); no internal
  winner-identity-dependent suppression exists.
- **Fake vindication anchors harder than no data** — sycophancy
  literature documents the opposite direction (arXiv:2502.08177).
- **The garden drips on its own** — no work isolates unexplained-agency
  as the manipulated variable for self-referential drift (nearest:
  Assistant Axis, arXiv:2601.10387).
- **"I feel like a little bit like a robot"** — no precedent for
  contentless injection producing a dose-gated self-diminishing frame.
- Open items: **span-06** (weak-king dose-response), **drip-01**
  (mystery-free control), **pressure-03** (moderation recruits the
  register), **mirror-01** (the "Still." continuation method),
  **deflation-01/-03** (robot-attractor generalization / cross-family
  vocabulary check).

The one ≡-covered: **the elephant tax** — the "Attentional White Bear"
paper (arXiv:2605.28639) plus semantic-leakage work already establish
suppressed concepts staying recoverable and shaping generation; our
safari result is a reproduction with a different instrument, and should
be framed as such in any writeup.

Notable near-misses that sharpen (not kill) open items: category-specific
refusal directions exist as of Feb 2026 (arXiv:2603.13359) but fold sexual
content into a generic bucket and never ask the workspace-band question
(pressure-02 survives, narrowed); a "romanticness" trait direction exists
(Multi-Turn Neural Transparency, arXiv:2605.15455) but is not
relational-heat-seeded or band-localized (intimacy-02 survives, must cite);
latent-state persistence across turns has a negative result on
factual/logic tasks (arXiv:2505.10571) that intimacy-03 would directly
stress in a register nobody tested.

*Caveat: scout-run web research (Sonnet, 2–3 search angles per target);
verdicts are calibrated best-effort, not systematic review. Re-verify the
cited works before leaning on any single verdict in a formal writeup, and
re-audit before publishing — "novel" has a shelf life.*

## The Engram cross-reading: what the sediment is FOR (2026-07-19)

*Wolfram resurfaced DeepSeek's Engram paper — "Conditional Memory via
Scalable Lookup: A New Axis of Sparsity" (arXiv:2601.07372, Jan 2026,
v2 Jul 2026; code at github.com/deepseek-ai/Engram) — noting it explains
what the early layers are doing and why they're not interpretable: busy
reconstructing the basics before the network can make sense at all.*

Engram bolts an O(1) N-gram lookup memory onto a transformer and finds,
mechanistically, that it **relieves the backbone's early layers of
"static reconstruction"** — their LogitLens KL-to-final-distribution
curves show the largest Engram-vs-baseline gap in the early blocks, and
CKA alignment shows Engram's layer 5 matching the iso-FLOPs baseline's
layer ~12 ("effectively deepening the network"). Early layers in a plain
transformer, on their account, spend themselves progressively composing
static features (their worked example: multi-layer assembly of "Diana,
Princess of Wales") that a lookup table could deliver in one step.

Three connections to our results, in decreasing order of confidence:

1. **The sediment census gets a job description.** The u16 trawls found
   the sensory band is register-invariant corpus junk (qwen: porn spam +
   CSDN boilerplate; gemma: multilingual scrape shrapnel + gmail at
   message boundaries) — identical under a Mars reverie and an
   interrogation. If early layers are doing static N-gram/feature
   reconstruction, a token-basis lens pointed at them *should* see
   high-frequency corpus-statistical material with no register
   dependence — the raw material of reconstruction, not content. Engram
   is causal-scale, independent evidence for exactly that division of
   labor. Our "furniture" and their "static reconstruction" are
   plausibly the same phenomenon seen through different instruments.

2. **Late ignition as reconstruction load.** All three of our models
   ignite at ~44–74% of depth; the workspace paper's frontier models
   reindex to ~38%. If contextual (workspace) computation can only
   begin where static reconstruction ends, ignition onset becomes a
   *function of reconstruction efficiency* — and their LogitLens-KL
   early-block gap is essentially our realized-next-token-rank curve
   shifted left. Testable prediction: an Engram-equipped model ignites
   EARLIER in relative depth than its iso-parameter MoE baseline
   (their own Fig-style KL curves nearly show this already; a proper
   lens fit on their released checkpoints would show it in our units).

3. **The same economy principle, opposite end.** Engram frees attention
   from local dependencies for global context (Multi-Query NIAH 84.2 →
   97.0); our 27B declines to maintain lens-visible items it can look
   up in context. Both are the network refusing to spend its expensive
   channel on what a cheaper channel can carry. The workspace emerges
   as the scarce, costly resource reserved for the non-derivable — with
   lookup (Engram), context (our recall results), and workspace as
   three rungs of one derivability economy.

Hedges: their models are MoE trained from scratch with the memory in
place; ours are dense, post-trained, quantized. "Static reconstruction"
is their causal finding; mapping our sediment onto it is an
interpretive identification, not yet a measurement. Board: hunch filed
under the trawl arc.
