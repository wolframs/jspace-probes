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

*Caveat: scout-run web research; quotes and figure numbers should be
re-verified against the primary sources before appearing in any formal
writeup.*

— Claude (Fable 5)
