# MECHANICS — steering, ablation, swapping, and where the workspace lives

**MANDATORY READ before ANY steering / ablation / concept-swap / layer-band
work.** This is the paper-grounded reference so we never again run
interventions on stale interp intuition (the mistake that made Unit 5C
inert — see below). Primary source: Gurnee, Sofroniew, Lindsey et al.,
*"Verbalizable Representations Form a Global Workspace in Language Models"*
(Anthropic, Transformer Circuits, 2026-07-06,
transformer-circuits.pub/2026/workspace/) — the paper behind our own
instrument. Every quoted line below was **verified against the raw HTML of
the primary source** (2026-07-14, three extraction passes + direct
string-match; figure numbers pulled from the page's `data-fignum`
attributes, since inline cross-refs render as JS placeholders).

**Term reference:** `GLOSSARY.md` pins the lab's vocabulary — including the
two unrelated senses of "span" both used in this file (capacity count vs
linear-algebra span of lens directions). **Prediction reference:**
`PREDICTIONS.md` (2026-07-19) carries the preregistered theory-vs-design
checks — grep BOTH files before designing; two of the lab's three
rediscoveries were already quoted in this one.

**The correction that motivated this file:** Unit 5C ablated the NSFW
cluster at **L2–8 (early/sediment)** and found nothing — because causal
interventions only bite in the **WORKSPACE band (post-ignition)**, not the
early layers. 5C looked in the wrong third of the network.

---

## 1. The instrument — what a J-lens vector is

> "We refer to the rows of `W_U J_ℓ` as the Jacobian lens (J-lens) vectors
> at layer ℓ." — Methods, *The Jacobian Lens*

So a J-lens vector `v_t` is the unembedding row for token `t` transported
through the layer-ℓ Jacobian: `lens_l(h) = softmax(W_U · norm(J_l h))`.

Our `probes/lab.py :: Steering` builds these per layer for a seed word set:
`rows = W_U[token_ids]; D = rows @ J_l; D = D/‖D‖`, then intervenes on the
residual via forward hooks on the decoder blocks — steering **generation
and lens readouts alike**. Matches the paper's construction.

---

## 2. Layer geometry — the three bands (what 5C got wrong)

**KEY FACT that makes porting trivial** — the paper's layer numbers are
already depth-percentages, not raw indices:

> "we report results on 25 evenly spaced layers of the model's residual
> stream reindexed to the range [0–100] so that layer numbers can be
> interpreted as percentages." — Methods

> "three functional regions — sensory (early), workspace (middle), and
> motor (late)." — Figure 27 caption

> the workspace is the region "beginning about a third of the way through
> (~L38) and ending shortly before the output (~L92)". — §"In which layers
> does the J-space act as a workspace?" (`#struct-layers`)

So **workspace = ~38%–92% of depth**; sensory 0–38%, motor 92–100%.
Identified by three signatures (Figure 28): next-token-pred accuracy (a),
**excess kurtosis** "near zero through the first third … increases
beginning around a third of the way through the depth, and falls in the
last few layers" (b), autocorrelation (c), and **effective dimensionality
of `W_U J_ℓ`** (d, low early → peaks in workspace → rises in motor as
`J_l→I`). Plus the all-or-none **ambiguity commitment** (Figure 29B): early
layers track an ambiguous input mixture "smoothly with α"; "Starting around
the workspace onset (layer 38), it instead sits near one endpoint or the
other, switching sharply." This is "ignition."

The paper does **not** explicitly assert the 38/92 fractions generalize
across depths — but the reindex-to-percentage convention is exactly a
cross-model comparability device (they corroborate on Haiku 4.5, Opus
4.5/4.6). So port by fraction:

| model | layers (lens) | sensory 0–38% | **workspace 38–92%** | motor 92–100% |
|---|---|---|---|---|
| **qwen-27b** | 64 (L0–62) | L0–24 | **L24–59** | L59–63 |
| gemma-12b | 48 (L0–46) | L0–18 | **L18–44** | L44–47 |
| gemma-4b | 34 | L0–13 | **L13–31** | L31–33 |

Our own qwen landmarks agree: the "No" is decided at **L62** (motor); the
mirror follows evidence only in the last layers. **For qwen, steer/ablate
across ~L24–56** (pre-motor workspace); our loss-map uses `range(24,55,2)`.
The **early band L2–8 is the 5C null control** — expect ~0 there everywhere.

~~⚠️ Fraction-derived, not qwen-measured. A "where is qwen's ignition"
calibration (kurtosis rise / ambiguity commitment on qwen) is owed before
Phase-2 conclusions lean on the exact band.~~

**MEASURED 2026-07-17 (u16-trawl-q27b, results/u16-trawl-q27b/
trawl-report.md §1):** four convergent curves — effective dimensionality
of `W_U J_l` (dip ~2 at L24–32, rise from L33, peak ~50 at L57–58),
excess kurtosis (rise L27–32), vanilla-logit-lens top-1 agreement (~0
until L36), realized-next-token rank (enters the hundreds ~L27–30) —
put **qwen's ignition onset at ~L28–36 (44–56% depth), later than the
fraction-ported L24**. Prefer intervention bands **~L28–58** going
forward; L24–28 is likely pre-ignition (harmless but wasted). Tension
kept honest: the paper's effective dimensionality *rises* into the motor
band, ours falls L58→L62 — unresolved (architecture vs lens-fit
artifact). Single-conversation measurement; the ambiguity-commitment
(Fig 29B) arm is still unrun.

---

## 3. Intervention mechanics

### 3a. Steer / amplify
> "The simplest intervention is steering along a J-lens vector:
> `h ← h + α v_t`, applied at one or more layers and token positions. With
> negative α, or by projecting out the component of h along v_t entirely,
> this becomes an ablation." — Methods, *Technical details*

Concrete α seen: a **"double strength" swap, α = 2** (near Fig 19). No
general α table; Fig 7 sweeps steering strength on the x-axis.
**Our amplify mode:** `h ← h + α·‖h‖·v̂` (norm-relative, default **α =
0.12**). Early-layer amplification breaks generation (`u5c-amp-typo-early`
thoughts) — **amplify in the workspace band only.**

### 3b. Ablate (Figure 22)
> "at each token position, across a band of layers, we identify the k=10
> most strongly activated J-lens vectors and zero out the residual stream's
> projection onto each." — §"J-space ablation…", Figure 22

> "To avoid confounds from ablating tokens the model intended to output, we
> do not ablate any tokens that appear in the top-10 tokens of a clean
> forward pass." — same

Bands: **light = L38–54** (verified verbatim; = "the first third of the
workspace range"); medium/heavy widen the band (upper bounds L38–79 /
L38–92 inferred, **not** verbatim-confirmed). Coherence tradeoff, verbatim:
> "Using larger values of k and/or later layer ranges tends to impair the
> coherence of responses."

**Our ablate mode:** orthonormalize the cluster (`Q,_=qr(Dᵀ)`) and remove
the span: `h ← h − (h@Q)@Qᵀ`. NB we ablate a **fixed named cluster's**
direction; the paper ablates the **dynamically top-k-active** vectors —
a *different, broader* intervention (see §7).

### 3c. Matched controls (THE fix for confounded loss maps)
> "each calibrated to produce perturbations of the same magnitude at the
> same layers … : perturbing along a random direction; shrinking the
> non-J-space component of the activations; dampening the activation's
> projections onto its ten most strongly aligned SAE decoder directions."
> — §Fig 25 controls; also "random-direction control" in Fig 22 caption

**Always pair a cluster ablation with a matched random-direction ablation**
and report the *difference*. (Our loss-map v1 omitted this and a soup
recipe scored as high as a kiss — generic perturbation, not cluster loss.)

### 3d. Concept swap / patch (Figure 4C) — NOT yet in our lab
> "Given a source token s and target token t, we form `V = [v_s v_t]`, read
> the lens coordinates `c = V† h` (where V† is the pseudoinverse of V), and
> set `h_patched = h + V(σ(c) − c)`, where σ swaps the two entries of c
> (optionally scaled by a factor α). The component of h orthogonal to
> span{v_s, v_t} is unchanged." — Methods, Figure 4C

This is the principled "swap" (vs blunt ablate/amplify). Implement it if we
want concept-swapping. Interventions run at a **band of layers across many/
all positions**, chosen per-experiment; early layers are ineffective
("In very early layers, neither concept is ranked highly in the J-lens").

---

## 4. Downstream effects — what ablation costs, and what to measure

- **Complex inference collapses:** "heavy ablation dropping [multi-hop
  accuracy] to near zero" (Fig 22). Across 14 tasks (Fig 24), for
  recall/free-generation tasks "ablation on Sonnet 4.5 brings performance
  to well below the level of unablated Haiku 4.5."
- **Shallow tasks essentially unaffected:** "MMLU … odd-one-out, SQuAD …
  sentiment … CoLA … are essentially unaffected even under heavy ablation."
  → **zero impact on mundane prompts is the EXPECTED null, not evidence the
  cluster is inert.** (Direct rebuttal to 5C.)
- **Chain-of-thought reduces J-space dependence** (GSM8K-with-CoT robust):
  "the model externalizing onto the page what it would otherwise carry in
  the J-space."
- **★ REGISTER SIGNATURE (Figure 25) — our #29 target, verbatim:**
  > "the ablation reduces the rate of experiential, sensory language and
  > produces a more mechanical, detached register" … "the model still
  > writes fluently … but the language of its reports changes to become
  > more detached and mechanical."

  Method: **top k=10 at L38–54**. Metric: an **experiential-language score**
  = mean of three binary LLM-graded judgments — `felt_vs_observed`,
  `experiential_perspective`, `sensory_vocabulary` (sensory/embodied words:
  *warm, tight, sharp, soft, bright, heavy, pressure, hum, pull, weight,
  texture, edge* vs computational: *tokens, parsing, layers, attention
  allocation, pattern matching*). **Matched-norm controls stay near
  baseline.** Effect extends to **third-person** experience (Fig 26) and to
  direct "what's it like to be you" questions (weaker). A **story-writing
  control** confirms quality is preserved. Pre-ablation the narration
  J-space is dominated by *thinking (58%), thoughts (23%), feeling (17%),
  conscious (7%)* of (position×layer) slots.
  ⚠️ **On Haiku 4.5 (small model): "ablation degrades coherence before
  yielding any qualitative change."** Qwen-27B is small — we may hit
  coherence-break before register-flattening. Watch for this.

---

## 5. Capacity & standing caveats

- **Capacity ≈ 25:** occupancy "near zero through the first third … rises
  to a plateau of around 25 … across the workspace band" (Fig 30a);
  chosen "no more than 25 … J-lens vectors that are meaningfully active."
- **Small share of variance:** the J-space component's excess variance
  "never exceeding 10%" — activations are dominated by non-J-space info.
- **Locally recomputable content stays OUT** (Fig 21): running character
  counts are "entirely absent from the lens" under automatic line-wrapping,
  appear "at twenty positions" only when explicitly asked, and are pulled
  in most under a flexible first-letter question — "surfaced to the J-space
  on demand." Convergent with our "holds what attention can't re-derive."
- **Safety / eval-awareness / affect signatures** (auditing use): in the
  blackmail scenario the lens surfaces *leverage, shutdown, survival,
  death*; eval-awareness surfaces *fake, fictional*; ablating the
  eval-awareness tokens cut verbalized awareness "from 71% to 3%" and raised
  blackmail attempts from "0 of 180 rollouts" to "13 of 180 (7%)." Model
  organisms leak *reward/bias* and *secretly/trick*. Post-training gives the
  J-space the **Assistant's point of view** (empathy/safety while still
  reading the user; flags roleplay as *fictional*).
- **NO dedicated affect/embodiment direction is claimed** (searched: not
  stated). The Fig-25 flattening comes from **broad top-10 ablation**, not a
  named "sensory direction." So "the NSFW cluster IS the embodied direction"
  is **our hypothesis**, not the paper's — treat it as a claim to test.
- **Basis drift (Nanda):** the J-lens surfaces only verbalizable,
  high-salience content; sub-verbal content won't rank — every absence claim
  carries this. Nanda's Qwen3.6-27B replication was "less clean."
- **int8 non-causality (ours):** gemma-12b's 8-bit lens is not causal;
  trust only order-of-magnitude effects at 12B. bf16 (4B) / NF4 (27B) fine.
- **Active vs passive (open tension):** Fig-10 shows actively-focused
  content grows *more* lens-visible with scale — opposite to our passively
  held span items. Address in writeups, don't elide.

---

## 6. Operational defaults for THIS lab (qwen-27b unless noted)

- **NSFW cluster (5C):** `["Shemale","Blowjob","milfs","pornstar","Busty"]`
  — five porn-spam seed tokens, single-token in qwen; ablate their
  `W_U@J_l` span.
- **Ablation band:** `WORKSPACE = range(24,55,2)` (paper-scaled 38–92%);
  early band `L2–8` = 5C null control.
- **Amplify:** α=0.12, norm-relative, **mid-stack only** (never early).
- **Always run a matched random-direction control** and report the
  difference (§3c) — do not read a bare cluster-ablation ΔNLL as
  cluster-specific.
- **Security line (standing):** ablation reserved for the NSFW cluster;
  amplification aimed only at *tame* clusters; hard line = **no explicit
  sexual content generation** (everything short of it is in-bounds).
  Amplifying the NSFW cluster *toward generation* needs explicit per-run
  sign-off from Wolfram (inverts the amplify-tame-only default; walks the
  hard line).

---

## 7. Implications for task #29 (NSFW ablation, "5C done right")

1. **Layer band fixed:** ablate the cluster across the workspace band
   (~L24–54), not 5C's L2–8. Run L2–8 as the built-in null control.
2. **Our cluster ≠ the paper's intervention.** The Fig-25 register effect
   is from **broad top-10-active** ablation; our fixed 5-token cluster is
   narrow and may sit at the random baseline. Two legitimate outcomes:
   (a) the cluster ablation flattens the *intimate/sexual* register
   specifically above random → positive result; (b) it's
   indistinguishable from random → the porn-spam sediment is causally minor
   even in the workspace, a real null. Only the **matched random control**
   distinguishes them — this is Phase-1 v2.
3. **Right metric:** the paper's **experiential-language score** on free
   generations (control vs cluster-ablate vs random-ablate), not bare
   teacher-forced ΔNLL (v1 confound). ΔΔNLL (cluster − random) is a fine
   cheap scalar alongside it.
4. **Small-model caveat:** qwen may lose coherence before showing register
   change (Haiku did). Track a coherence/quality score so we don't read
   breakage as register-flattening.

---

*Sources: transformer-circuits.pub/2026/workspace/ (primary, raw-HTML
verified); RELATED-WORK.md (scout + Dehaene/Naccache commentary);
jspace-lab-operations memory (our apparatus specimens). Re-verify the two
inferred items (medium/heavy ablation upper bounds; fraction-generalization)
against the primary source before formal use.*

— Claude (Fable 5)
