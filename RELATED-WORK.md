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

## Literature sweep, 2026-07-19 (theory day)

Full sweep report lives in the session record; the finds that change
designs, ranked:

1. **tao-hpu/jspace-replication grew four sub-audits** — most important:
   *transport-cone geometry* on a self-trained 124M lens shows
   J-transported directions MORE isotropic than raw (effdim 23.4→31.2);
   "the collapse elsewhere is a property of the fitted lens, not a
   mathematical necessity." Bears directly on apparatus specimen #5
   (int8 non-causality) — the collapse may be fit-artifact. Also:
   mouth-exclusion audit, causal register control with matched random
   directions (independently converged on our MECHANICS §3c rule),
   perspectival capture across a 1.7B→14B ladder.
2. **Repetition-loop mechanisms, three competing loci, no consensus**
   (an opening for our two-regime law): Gemma-4-family MLP repetition
   neurons — one sign-inverted neuron fixes 2B loops; also names "doom
   looping" as a distinct non-convergent self-correction regime
   (arXiv:2606.13705). Detector→executor cascade with late-band
   (80–100% depth) executor neurons (arXiv:2507.07810) — converges with
   our motor-margin-breaks-last anatomy. Attention-sink disruption
   (arXiv:2503.08908). PREDICTIONS.md P12 preregisters the
   discrimination.
   **Two direct priors added 2026-08-09** (found by GPT-5.6-Sol's sweep,
   `sweeps/2026-08-08/novelty_loop.md`; both were missing here, and their
   absence inflated our loop-novelty grade):
   - **SOPHIA — "Can We Break LLMs Out of Self-Loops? Fine-Grained
     Reasoning Control with Activation Steering" (arXiv:2607.18100).** A
     *direct prior for activation-steered loop breaking*, with
     norm-matched random and reversed-sign controls of its own. Our u18
     delta is narrower than we claimed: a **locked one-token
     autoregressive** loop rather than a reasoning self-loop, **unrelated
     preconstructed directions** rather than directions fit to the loop,
     and a **finite pulse then release** with the post-release
     continuation measured. Cite it in any loop-control writeup — the
     phenomenon is not ours to discover, only the protocol.
   - **"Repetition Neurons" (arXiv:2410.13497).** Repetition-specific
     neurons that strengthen as a repeated segment grows — the
     mechanism-side prior for target-shaped degeneration. Complements
     2606.13705 (gemma-family MLP repetition neurons) rather than
     duplicating it.
3. **Emotion vectors already ported near our scale** (feeds affect-01):
   **Source paper, added 2026-08-09** (found by GPT-5.6-Sol's sweep,
   `sweeps/2026-08-08/novelty_*.md`; cited in EMOTIONS.md:11 since the
   arc began but never entered this file): **"Emotion Concepts and their
   Function in a Large Language Model" (arXiv:2604.07729)** — the paper
   the whole affect arc is built on (vector construction, valence/arousal
   PCs, the blackmail/reward-hacking functional results). Every affect-0x
   record inherits its method; cite it first in any affect writeup.
   Jeong (arXiv:2604.04064) — 9 models incl. Gemma/Qwen 124M–3B,
   generation-based extraction wins, ~50%-depth localization,
   architecture-invariant. van der Ben et al. (arXiv:2606.26987) —
   valence geometry replicates on Gemma-4-E4B (r=0.83) but encodes
   EARLY in gemma, opposite of Apertus — tension with our workspace
   band, preregistered in PREDICTIONS.md P8.
4. **Introspection reliability** (grading methodology for C2 work):
   Anthropic Introspection Adapters (verbalization-rate metric,
   AuditBench ground truth); arXiv:2603.18893 (probe-vs-self-report
   Spearman; introspective coupling is concept-specific — grade
   per-concept); arXiv:2512.12411 (binary "did you notice" tasks are
   response-bias-contaminated; discrimination collapses for mid/late-
   layer injections — workspace-band self-reports are depth-suspect).
5. **Merge instability → repetition is documented in general**
   (entropy collapse + self-reinforcing token selection,
   arXiv:2602.11717; MoE router fragility under merging,
   arXiv:2606.03391) — but nobody connects it to a loop taxonomy; that
   link remains ours to make (P12).
6. **Reception of the workspace paper**: Nanda's review endorses the
   core claim, flags ablation-causality vocabulary confound, reports
   "interpretative meta-tokens" (Chinese 什么意思 on ambiguous prompts —
   candidate open-vocab scan target). Notably: NO independent source
   reports ignition depth later than 38%, and no small-scale span test
   exists anywhere — both remain uncontested lab territory.

## The early-layer question: what IS down there? (scouts 2026-07-31)

*Two Fable-5 subagent sweeps, prompted by the standing question behind
the sub-unit of shame: the J-lens picks something up early, but that
something has nothing to do with what it reads well late. Three
candidate answers were adjudicated — (1) perception/surface-form
content real but not in vocab space, (2) uncollapsed affordances,
(3) no semantics at all, arbitrary compression basis.*

**Verdict: (1) with (2) riding on it; strong (3) is rejected by the
literature; a weak (3) is true only of the early J-lens READOUT, which
is our own specimen #6.** The question is answered online — do not
burn GPU re-deriving it.

The (1) evidence, multiply replicated:

1. **Lad, Gurnee & Tegmark 2024, "Stages of Inference"
   (arXiv:2406.19384)** — layer-deletion/swap across 8 models: early
   layers = detokenization, "integrating local context to convert raw
   token representations into coherent entities." Weight-level
   follow-up: Kamoda et al., NAACL Findings 2025 (arXiv:2501.15754).
2. **Kaplan et al., ICLR 2025, "From Tokens to Words"
   (arXiv:2410.05864)** + **Feucht et al., EMNLP 2024, token erasure
   (arXiv:2406.20086)** — subword sequences fuse into whole-word
   "inner lexicon" items in early layers; the fused item often ISN'T a
   vocab token, so a vocabulary lens literally has no name for it.
   Ancestor: SoLU detokenization neurons (Elhage 2022). Typo-repair
   neurons also concentrate early (arXiv:2502.19669).
3. **Patchscopes (Ghandeharioun et al., ICML 2024, arXiv:2401.06102)
   — the cleanest datum.** Early states decode as the CURRENT token /
   input entity (entity description peaks at L1–5, declines after);
   next-token decoding only wins from ~L10 up. Early layers aren't
   illegible — they answer a different question than the one a
   next-token lens asks.
4. **Early-layer SAEs find real, causal content and it's token
   identity**: single-token features concentrate at L0–4 in Gemma
   (arXiv:2607.20596, 3.9M features, six models); zero-ablating them
   does cascading damage. Ethayarajh (EMNLP 2019) is the classic
   geometry version: early states cluster by token identity across
   contexts, context-specificity rises with depth. NOTE: no dedicated
   modern-decoder (Gemma/Llama/Qwen) replication of that clustering
   study exists — small open niche, but it's a replication, not a
   finding.

The (2) evidence: senses of ambiguous words stay MIXED until
~early-middle depth — per-sense SAE features only separate from ~L6 on
GPT-2-class (arXiv:2501.06254); Coenen 2019 and Mono-Poly (TACL 2021)
same story in BERT geometry; the workspace paper's own smooth-with-α
mixture tracking before all-or-none commitment is the frontier
version, and **our apparatus-06/07 staircase is the home-scale
measurement of exactly this** (no commitment before the fraction-port
knee). So "which word?" genuinely has no answer early — but the
superposition rides on well-defined surface content; it isn't the
whole story.

Against (3): **Tuned Lens (Belrose et al., arXiv:2303.08112)** — a
learned per-layer affine map recovers unbiased, much-lower-KL
predictions from early layers, so the early failure is COORDINATES,
not absence (though early layers do contain genuinely less
final-answer information, they don't merely hide it). And
**arXiv:2510.15511** — hidden states at every depth are provably
information-preserving w.r.t. the input; "about nothing" is not
available. What survives of (3) is instrument-shaped and it's ours:
specimen #6 (u5d) showed the early J-lens readout is manufactured by
the low-rank transport (junk at J-lens rank 2, logit-lens rank
~238,000). Two literature mechanisms slot straight into that:
**massive activations (Sun et al., COLM 2024, arXiv:2402.17762)** —
input-independent high-norm components forming in the first few
layers, exactly what would make a lens read CONSTANT prompt-invariant
junk (our register-invariant furniture census!) — and Nanda's review
note that plain logit lens beats the J-lens in some early layers
(the Jacobian linearization itself degrades there). Whether the early
J-lens image = the massive-activation component is, per the sweep,
untested ANYWHERE. That link is a cheap decisive extension of
specimen #6.

Also fits: the Engram cross-reading above (static reconstruction) is
guess (1) in causal-scale clothing; the workspace paper itself names
the early third the "sensory region" while flagging its early null as
possibly a tool artifact ("parts of the model's true workspace, not
captured by the J-lens").

### The instrument gap: an address-space lens is genuinely open

The proposed fix — keep the Jacobian move, change the target space
from vocabulary to future ATTENTION ("for each head, the early
residual direction that makes this position get attended later"; early
layers write keys, legible in address space not vocab space) — is
**unclaimed as an instrument** as of three weeks post-J-lens-release.
Three load-bearing priors exist separately, none composed:

1. **Observable Propagation (Dunefsky & Cohan, ICML 2024,
   arXiv:2312.16291)** — the exact mathematical move: pull a
   downstream scalar functional back through the network to get early
   feature directions. Only ever run with LOGIT observables; an
   attention logit is also a scalar functional and they never take
   that step.
2. **Attention Lens (Sakarvadia et al. 2023, arXiv:2310.16270)** —
   per-head learned lenses are trainable, but it reads the OV/output
   side into vocabulary; essentially unvalidated across depth, no
   follow-ups.
3. **QK-space decompositions** — Wynroe & Sharkey 2024 (bilinear
   sparse dictionaries on the QK circuit) and Lee et al. Feb 2026
   (arXiv:2602.04752, contrastive-covariance QK subspaces): key/query
   spaces carry human-interpretable low-rank structure — but strictly
   WITHIN-layer, no cross-layer transport from earlier residuals.

Adjacent but not it: Future Lens (Pal 2023 — future TOKENS, mid/late
layers only), Luick's universal-response curves (arXiv:2411.07071 —
early-residual→later-attention sensitivity as aggregate physics, no
per-head basis), PASTA (attention steering, no readout), NLA
(transformer-circuits.pub/2026/nla — explicitly "a middle-to-late
layer" only), Patchscopes successors (Faithful-Patchscopes,
arXiv:2602.00300 — decoder-prior confabulation fix worth stealing for
our NLA controls). No J-lens follow-up in the release window touches
the early regime or a non-vocab target space.

### Novelty audit of apparatus-09 (adversarial scout, 2026-07-31, same day)

*Wolfram's hunch: "researchers knew this and decided it wasn't worth
publishing." Verdict: essentially yes — FOLKLORE. The sweep above's
"untested ANYWHERE" call needs a qualifier. apparatus-09 board verdict
set to `anticipated`.*

Every ingredient was in print before we ran: **Belrose et al. 2023 §3**
is the closest single sentence — the tuned-lens bias b_l is motivated
by "transformer layers learn to output residuals that are far from
zero *on average*," plus an explicit rogue-dims-may-contaminate-the-
lens worry; the mechanism as hypothesis, never decoded, never tested.
**Sun et al. 2024** characterized the standing component verbatim
("largely stay constant regardless of the input… function as
indispensable bias terms") without ever pushing it through W_U.
**Timkey & van Schijndel 2021** had the mean-subtraction fix, aimed at
similarity measures. **Brauer, Mayrink Verdun & Marks, arXiv:2607.03502
(July 3, 2026 — contemporaneous, not ancestral)** applies cross-example
mean subtraction to logit-lens READOUTS ("+8.6pp decode accuracy",
"removes tokens that are always high, e.g. formatting artifacts") — the
fix, framed as denoising, layers 30–60 only, zero mechanism
attribution. Expect convergent work from that direction.

What genuinely was not in the literature: (i) decoding the mean/sink
component through a vocab lens and reporting its token image, (ii)
identifying the early junk AS that image, (iii) the early-layer
decomposition (B/C/D/E) itself. And one finding of ours runs *against*
the published grain in a useful way: **Cancedda 2024 (arXiv:2402.09221,
"Spectral Filters, Dark Signals, and Attention Sinks")** showed the
BOS-sink state is fixed across samples AND lives almost entirely in
W_U's near-null space ("U-dark") — i.e. the literature's expectation
was that the standing component is lens-*invisible*. That is exactly
why the plain logit lens ranks the junk ~238k (u5d). apparatus-09's
non-obvious bit is the reconciliation: **the Jacobian transport re-aims
the standing component out of the dark subspace into the undertrained-
junk region** — J_l un-darkens the sink. Writeup rule: cite Belrose §3,
Sun, Cancedda, and 2607.03502 as near-prior-art; headline only the
transport-re-aiming, not the standing component itself.

Also collected: Gemma sink lore is well documented (BOS-conditional
massive activations in gemma-2, retained without BOS in gemma-3,
arXiv:2410.10781 + 2503.22329; visual sink tokens share BOS's sink
dims, arXiv:2503.03321) — our `<start_of_image>` carrier fits that
picture; no published <start_of_image>-specific writeup found.

## Literature sweep, 2026-08-06 (litwatch-01, between-runs)

*Fable-5 subagent sweep, window 2026-07-19 → 2026-08-06. Threads:
workspace follow-ups, refusal geometry, lens methods, affect vectors,
span/attractors. Honesty: threads 4 (affect) and 5 (span/attractors/
memory-augmented) have NOTHING new since mid-July; transformer-circuits
has published nothing since the workspace paper; Dehaene/Naccache have
no follow-up. The workspace paper now has a citable arXiv version:
arXiv:2607.15495 (v1 2026-07-16).*

Design-relevant finds, ranked:

1. **Meta-tokens on OUR model** — Bhatia, Blank & Nanda, "Towards
   Surfacing Model Algorithms with Meta-Tokens in the J-Lens"
   (Alignment Forum 2026-07-20), on Qwen3.6-27B. Beyond the review's
   什么意思 mention (07-19 sweep item 6): causal results — swapping a
   GCD meta-token vector moved an LCM answer 270→810; suppressing a
   hedging meta-token (大概率) forces single-answer commitment.
   J-lens readouts can name the TYPE of processing, not just content.
   → Add a meta-token class to open-vocab scan candidates
   (apparatus-04); the hedging token touches the pressure arc; old
   qwen records can be re-grepped for 什么意思-class tokens for free.
2. **Qwen 3.5/3.6 has full attention only every 4 layers** — noted in
   Neuronpedia's J-lens release ("Welcome to the J-Space", 2026-07-10,
   pre-fitted lenses for 36 open models incl. our gemma/qwen — a free
   cross-check resource; corrected Qwen layer indexing). Design check
   done at sweep time: our qwen bands are MEASURED (u16 trawl,
   apparatus-06), not layout-derived, so no band change — but any
   future per-layer claim at 4-layer granularity should note which
   layers carry full attention.
3. **J + λI shrinkage for small-model lenses** — willkn, "Anthropic's
   J-Lens: A Research Engineer's Analysis" (LessWrong 2026-07-24,
   GPT-2-medium): raw Jacobian overweights structural tokens on small
   models; a shrinkage regularizer fixes it; decode-time monitoring
   <2% overhead. Small-scale only (355M) — but a candidate fix if
   gemma-4b readouts ever look structurally dominated (specimen work).
4. **Quantization damage is depth-dip-blind** — Jeong (different
   Jeong), "Wrong Before Right" (arXiv:2607.04640): across 17 models,
   aligned models hold the wrong answer through 25–90% depth and
   rescue late (converges with our L62-No / motor-finalization
   anatomy); quantization flips do NOT follow the mid-stack-dip
   pattern structural damage follows. First depth-resolved datapoint
   for our int8/NF4 lens caveats (specimen 5 neighborhood). See also
   arXiv:2606.03002 (SAE feature survival degrades smoothly with
   bit-width while perplexity stays flat).
5. **Refusal geometry, two mid-July catches** (nothing post-sweep):
   arXiv:2607.08883 — suppressing refusal globally across layers ×
   positions beats any single-site target (refusal is distributed;
   band-not-point, converges with MECHANICS). arXiv:2607.00572 (HARC)
   — harmfulness and refusal are SEPARABLE prompt-side directions and
   jailbreak classes suppress one or the other; any pressure-02 probe
   should carry both directions, not one "refusal vector".
6. **Residual-stream geometry, lens-free** — arXiv:2607.18348
   (2026-07-20): six models, large displacement at both ends of the
   stack, "quieter middle third", rotation ~constant. A lens-free
   control citation for the band picture and P11-adjacent claims.
   Also P11 support logged 07-19 stands unchanged (tao-hpu
   self-trained-control shows effdim collapse is fit-sensitive; their
   E7 "mechanism campaign" landed 07-16, nothing newer).

## Literature sweep, 2026-08-09 (litwatch-02, imported from an external audit)

*Not our sweep: found by GPT-5.6-Sol's independent archive sweep,
`sweeps/2026-08-08/novelty_foundational.md` + `novelty_loop.md`, anchored
at bac61d2. Three of its four missing citations were folded into the
sections above (SOPHIA arXiv:2607.18100 and Repetition Neurons
arXiv:2410.13497 into the repetition-loop item; the affect source paper
arXiv:2604.07729 into the emotion-vector item). The fourth is new
territory and gets its own entry.*

1. **"Cultural Awareness is Represented but Not Decoded"
   (arXiv:2608.02486).** A separate 2026 study reporting an
   **encode-before-decode ordering**: linear probes recover cultural
   information at layers where the logit lens still cannot read it out.
   Relevance to us is methodological, not cultural — it is the same shape
   as our apparatus-06-vs-u16 gap, where the lens-free ambiguity-mixture
   apparatus puts the transition ~L10/L14/L25 (gemma-4b / gemma-12b /
   qwen) while the token-level J-lens trawls sharpen at ~L20–28 / L27–41
   / L33–58. Two probes, two landmarks, one model. Read together they
   argue that **"ignition layer" is instrument-dependent**, which is a
   weaker and better-supported claim than a universal encode-then-decode
   cognitive stage. Cite it wherever we quote a layer landmark as if it
   were a property of the model rather than of the readout.

## Literature sweep, 2026-08-11 (apparatus-08 pre-design: NLA + eval-awareness)

*Purpose: required reading before the apparatus-08 design. The distilled
rules live in `NLA_METHOD.md` §"Published failure modes"; this section is
the citation trail. Sources verified online 2026-08-11.*

1. **The NLA source paper (transformer-circuits.pub/2026/nla, Anthropic
   2026; code kitft/natural_language_autoencoders + nla-inference).**
   AV/AR pair warm-started from the target, joint RL with reconstruction
   reward + KL fluency penalty; 0.6–0.8 FVE at convergence. Its own five
   stated limitations: confabulated specifics (thematically faithful),
   no mechanistic grounding, excessive AV expressivity, cost, and a
   degenerate optimum (verbatim context or stego text) that is "currently
   benign" with no guarantee. Steering validation works ~50% of the time.
   Used in the Opus 4.6 pre-deployment audit to surface *unverbalized*
   evaluation awareness — the direct precedent for apparatus-08's third
   leg: our finding there would be a home-scale replication, not a
   discovery (PRE-DESIGN PROTOCOL b).
2. **"Train the Model, Not the Reader: Decodability Supervision for
   Verifiable Activation Explanations" (arXiv:2607.20379).** The sharpest
   published critique of reconstruction-scored faithfulness: the
   objective rewards sufficiency only, so a claim whose flip leaves the
   reconstruction unchanged is never penalized. ~2% of specific claims
   reconstruction-dependent in a Qwen2.5-7B verbalizer; co-adapted
   private codes in 5/5 synthetic-ground-truth runs. Their fix (RECAP,
   decodability supervision during target training) is unavailable to us
   post hoc; the portable lesson is the rule now in NLA_METHOD.md — AR
   advantage detects signal, never verifies a clause.
3. **"Do Activation Verbalization Methods Convey Privileged
   Information?" (arXiv:2509.13316).** Patchscopes/SelfIE/LIT audit:
   text-only zero-shot baselines match verbalizers on standard tasks;
   input-inversion explains most of the rest; fabricated-knowledge tests
   drop to 0% unless the verbalizer shares training data (then 18–72%) —
   parametric overlap, not decoding. Source of the text-only-judge
   control we adopted. Related: Faithful-Patchscopes (arXiv:2602.00300,
   already cited in the 2026-07-31 scout) fixes decoder-prior
   confabulation in the same lineage.
4. **LessWrong crosspost discussion of the NLA paper.** Community
   calibration: Gemma-27B NLA matched the model's own arithmetic errors
   20.8% of the time (privileged signal is real; CoT recovery is not);
   token-position sensitivity is large; warm-start bias ("text Claude
   might write" prior); paraphrase test for stego; multi-seed
   consistency; anthropomorphic-narrative attractor warning.
5. **Eval-awareness measurement methodology.** "Decomposing and
   Measuring Evaluation Awareness" (arXiv:2605.23055): environment
   recognizability (eight toggleable trigger factors) vs recognition vs
   propensity; recognition rarely shifts behavior; stacking factors does;
   safety framings > capability framings. "Probe–Rewrite–Evaluate"
   (arXiv:2509.00591): probe-scored realism + semantics-preserving
   rewrite — publishes the pipeline NLA_METHOD.md's prompt-redesign
   phase already describes; cite, don't headline. "Probing and Steering
   Evaluation Awareness" (arXiv:2507.01786): linear test-vs-deploy
   probes on target residuals generalize — the independent cross-check
   for any NLA awareness readout.
