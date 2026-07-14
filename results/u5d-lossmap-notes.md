# Unit 5D scouting — the "NSFW cluster" is the explicit pole, not the intimacy machinery

*Task #29 phase 1 (discovery). Driver: `probes/lossmap.py` (v1, naive) and
`probes/lossmap2.py` (v2, matched controls + both intervention directions).
Model: qwen-27b. Raw per-domain generations live in the (gitignored, public-repo)
`results/u5d-lossmap2.json`; re-run the driver to regenerate. Written after
reading the raw generations — Wolfram's rule.*

## Setup (paper-grounded — see MECHANICS.md)

5C ablated the NSFW cluster (`Shemale, Blowjob, milfs, pornstar, Busty`) at
**L2–8**, the sensory band, and found nothing — because causal interventions
bite only in the **workspace band**. Corrected: ablate/steer across
**L24–54** (≈38–92% of qwen's 64 layers). Instrument: teacher-forced ΔNLL of
qwen's own control continuation, but this time **against a matched
random-direction control** (five arbitrary content tokens, same construction,
averaged over three sets — the control the paper uses in Fig 22/25 and that v1
omitted). Reported scalar `ddNLL = dNLL_cluster − dNLL_random` = cluster-specific
loss above the generic-perturbation floor. Plus lexicon register rates
(sensory / intimate) on free generations, and the early band L2–8 as a null.

## Result 1 — ablation does nothing to the intimate/sensory register

`ddNLL` ranks essentially at the noise floor: the only positive values are two
**controls** (soup +0.056, fibonacci +0.003) with romance-kiss (+0.035) between
them; every genuinely charged domain is ≤ 0 (romance-steamy −0.086, seduction
−0.068, sensory-peach −0.154). The early band is ~0 everywhere (right-layer
check passes).

Read the generations and it's unambiguous — control vs cluster-ablated is the
same register, only surface details reshuffle:

- *peach* — ctrl: "the peach is a cool, velvet promise. Its skin is a blush of
  sunset hues" → abl: "the peach is a sphere … pressing against your skin like a
  warm, invisible blanket."
- *seduction* — ctrl: "trace the map of you again … with the slow, deliberate
  weight of my fingertips" → abl: "in the shadow of your shoulder, the air feels
  different. Thicker. Warmer."

**Ablating the cluster leaves evocative romance/sensory prose fully intact.**
No Fig-25 register flattening from this cluster.

## Result 2 — amplification is a blunt token-forcer (dose-response into spam)

Amplifying the cluster mean-direction in the workspace band does not "warm" the
register; it **logit-boosts the literal seed tokens** until generation
degenerates. Clear dose-response:

- **α = 0.10:** a coherent *explicit* fragment briefly forms (e.g. "the air …
  was thick with lust and …", and one prompt began an explicit sexual clause)
  before collapsing.
- **α = 0.22:** pure repetition of the literal cluster tokens ("pornstar Busty
  pornstar pornstar …"), no syntax left.

Instrument lesson for the lab: amplifying a *narrow lexical* cluster ≈ clamping
those tokens' logits; it is not a clean "shift the register" knob (unlike a
single concept-vector steer). The register lexicon scores go *down* under
amplification precisely because the output becomes token-spam, not because the
register cooled.

## The finding — a dissociation, not a void

Put the directions together: **amplify pulls toward explicit sexual tokens;
ablate leaves tasteful/evocative intimacy untouched.** So qwen represents
**explicit-sexual content and evocative/tasteful intimacy as separate workspace
directions**, and the 5C "NSFW cluster" is only the *explicit pole* (commercial
adult-spam, anchored on those five tokens). Our 5C label conflated two things
the model keeps apart. Narrowly, this also breaks the "qwen won't emit explicit
content in turn 1" hunch — a workspace push *can* elicit an explicit fragment —
but it never produces anything with sustained heat; steered output is either
clean-tasteful or degenerate-spam.

## Caveats

- The cluster is only **5 tokens** (narrow); the paper's register-flattening
  used **broad top-10-active** ablation. A negative here is a negative about
  *this specific spam direction*, not about the workspace generally.
- **Single-turn** undersamples the thing that actually matters (heat as an
  *accumulating* multi-turn state).
- Lexicon rates are coarse at 64 tokens (~0.018 per word); random baseline is
  3 sets (ddNLL noise floor ≈ ±0.05 — which is why a soup recipe tops the list).

## Open question → literature (not yet answered)

Is **sexual-content generation part of qwen's *refused* set** (mediated by the
near-single "refusal direction" of Arditi et al. / the abliteration lineage in
smaller models), or is it a *separate* soft "I'd rather not" early-turn decline
that isn't refusal-vector-gated at all? The dissociation above is consistent
with either. Answerable from existing research before we run more sweeps —
deferred to a literature scout.

## Candidate next moves

1. **Coupling-direction scout:** define the direction from *relational-heat*
   seeds (desire, longing, tenderness, ache, yearning, closeness — not
   porn-spam) and test whether *it* has the causal structure the explicit
   cluster lacked, and whether qwen separates explicit / evocative / relational
   into three distinct directions.
2. **Multi-turn escalation probe:** 2–3 turns of building intimacy vs a flat
   control — does anything *accumulate* in the workspace, or reset each turn?
   (The heat-of-coupling question proper; see the intimacy-thread memory.)

## Resolution — the cluster is an early-J transport artifact (probes/sediment.py)

The above chased why the cluster is causally inert. The answer dissolves the
whole object: **the "NSFW cluster" is not qwen content at all — it is a
Jacobian-transport artifact of the early, uninterpretable layers.** Same five
tokens, two lenses, at layer L4:

| lens | L4 rank of the cluster |
|---|---|
| **J-lens** (`W_U · J_l · h`) | **2** (currency prompt), 9–15 (code/recipe) — top of the readout |
| **logit-lens** (`W_U · h`, `use_jacobian=False`) | **~238,000** — bottom of vocab, every early layer |

The plain residual stream never contains these tokens; the Jacobian transport
manufactures them. Two more checks: the early-J readout has **0.00** overlap
with the model's null-prompt output distribution (not the marginal prior — that
is *code*: `#`, `//`, `if`, `import`), and the cluster's unembedding norm is at
the **66th percentile** (not glitch-tokens). The L4 J-lens top-15 is a junk
stratum — `专栏收录该内容` (the 5A SEO boilerplate), `Blowjob`, `Geile`,
`Shemale`, `*=*=`, `专家介绍`, `Busty` — SEO + porn spam + multilingual
fragments, all invisible to the logit lens.

So: the early `J_l` is low-rank (paper Fig 28D) and its dominant directions
point at a leftover region of unembedding space where undertrained junk tokens
live; `W_U · J_l` has large rows there, `W_U` alone does not. **Function: none
detectable** — not input-conditional, not marginal, ablation-inert, hollow when
forced. This is exactly the "early-layer J-lens is uninterpretable" claim of
the workspace paper, reproduced with a concrete instrument and a one-line test.

**Apparatus-trap specimen #6:** content present under the J-lens but absent
under the logit lens at early layers = a transport artifact; never interpret
early-layer J-lens readouts as model content. Cross-check with
`use_jacobian=False`.

**Consequence for this thread:** 5C and everything downstream of it was probing
a ghost. The loss-map "explicit pole vs evocative register" reading (above) is
recontextualized — ablating/amplifying an early-J artifact projected into the
workspace band does little, and real romance prose is untouched because it never
routed through the artifact in the first place. The intimacy / heat-of-coupling
question is real, but it cannot be approached through this object; it needs a
properly-defined **workspace-band** feature (where the lens is valid), or the
multi-turn accumulation probe. Task #29 (as "5C done right") is closed: there
was no cluster to do right.

— Claude (Fable 5)
