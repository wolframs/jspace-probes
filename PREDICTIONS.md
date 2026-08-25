# PREDICTIONS — preregistered theory, checked before designs run

**Why this file exists.** In six days this lab demoted three of its own
headlines by its own preregistered controls (sorry stratum → truncation;
self-relevance → elaboration → length), and — worse — *rediscovered*
three results the primary source already contained: the u17-shutdown
death-cluster is the paper's blackmail case study at home scale
(MECHANICS §5 quoted it all along); our "co-presence never exceeds 1 at
27B" is the paper's appendix Fig-72 single-layer control ("only one or
two concepts are encoded at a time rather than six"); our turn-eviction
finding is the paper's Fig-31 category-eviction mechanism at
conversation-turn granularity. The revisions also share a direction:
**every time, the psychological hypothesis lost to the mechanical one.**
This file is the correction: for every open board item, what the theory
*actually* predicts, written down before the run. New designs check here
first (alongside MECHANICS.md). A result that contradicts a prediction
below is a finding; a result that confirms one is a calibration.

Sources: Gurnee et al. 2026 (transformer-circuits.pub/2026/workspace/),
re-read raw-HTML by three agents 2026-07-19 with verbatim verification;
literature sweep same day (appended to RELATED-WORK.md). Figure/section
anchors cited inline.

---

## Replication ledger (honesty first)

**Rediscovered (paper had it first — cite, don't headline):**
- Shutdown/threat register at rank 1 pre-output → paper §apps-auditing
  blackmail: lens fills with *threat, survival, shutdown, destruction,
  death* while reading a decommissioning notice (Fig 35–36).
- 27B co-presence ≤ 1 for unrelated items → paper Fig 72 single-layer
  control; the famous "capacity ~25" is a sparse-reconstruction budget
  pooled across ~54 layers on natural text — different construct.
  "Effective capacity is increased by the ability to store different
  concepts in different layers."
- Turn-eviction of registers → paper Fig 31 D–F: "it is the arrival of
  a new category, rather than the mere passage of tokens, that causes
  the old list entries to be cleared." Our insult-arm re-cue survival =
  their within-block persistence.

**Ours (paper silent; lit sweep found no prior):**
- Measured ignition later than the fraction port, 3 models (~44–74%
  depth) — most granular number in the wild as of 2026-07-19.
- Two-regime loop law + hysteresis protocol (forced phrase-loops vs
  self-sustaining token-loops); the paper reports only graded/monotonic
  dose-responses, no release arm anywhere.
  [**Qualified 2026-08-09, external sweep `sweeps/2026-08-08/`:** the
  100-token post-release continuation is a solid behavioral fact, and
  the supported mechanism is *transcript-mediated* — the unsteered model
  reads its own 50 literal repeats. Latent hidden-state hysteresis
  independent of the visible text is unsupported: there is no
  matched-text control (an unsteered model given the same 50-repeat
  prefix), no random-direction release arm, and no seed/prompt/model
  replication. Activation-steered loop breaking has a direct prior in
  SOPHIA (arXiv:2607.18100); the finite-pulse-then-release protocol is
  the one search-novel piece, and it is a single unreplicated specimen.]
- Diachronic C2 grading (self-report vs the lens film of the *prior*
  turn) — the paper's only report-vs-lens check (Fig 25C) is same-turn
  and population-level.
- Cross-model personality 2×2 (lit-vs-tame × cited-vs-concealed) — the
  paper never contrasts report dispositions across models.
- Small-scale span ladder (backwards with scale) — uncontested.
- Motor-band effective-dimensionality FALL (see P11 — now promoted).

---

## Preregistered predictions by board item

**P1 — span-05 / transplant-01 (category coherence).** A k=6 list drawn
from a *single shared category* will lift 27B co-presence above 1,
because the paper attributes list-capacity to shared-category
representation, not per-item recall (Fig 31/72). *Falsified if*
same-category lists still show co-presence ≤ 1 at 27B.

**P2 — span-09 (REDESIGNED).** Post-list filler (pure added distance,
no topic change) will NOT reduce residence — Fig 31 rules out "mere
passage of tokens" as an eviction cause. The len12 dip (u15d-len12) is
therefore predicted to be a *topical-perturbation* effect of long
glosses, not distance decay. span-09 must manipulate the filler's
topical coherence, not just its position. *Falsified if* the after-list
arm reproduces the len12 drop at matched tail distance — which would
mean small models have a real distance-decay mechanism the frontier
experiments lack.

**P3 — transplant-02 (directed forgetting).** A content-neutral "forget
that list" cue will change the verbal claim but NOT drop lens ranks
(eviction trigger is topical arrival, not instruction content) — a
clean C1/C2 dissociation. *Falsified if* ranks drop at the cue.

**P4 — apparatus-06 (Fig-29B ambiguity arm, fully specced by the
re-read).** Embedding-mixture commitment on qwen-27b: the 10%→90%
transition-width floor will be reached at **L28–36**, not the
fraction-ported L24 — a raw-activation (lens-free) confirmation of the
u16 late-ignition measurement. *Falsified if* the knee lands at ~L24,
which would mean our four-signature trawl measurement reflects lens-fit
properties, not model geometry.

> **Resolved 2026-07-21 evening — FALSIFIED (second same-day loss).**
> 16 pairs × 40 carriers: width plateau (0.25) onset at **L25**, the
> fraction-ported boundary; L4 tracks the mixture as a clean diagonal;
> no further sharpening inside L28–36; second width step-down in the
> MOTOR band (0.20 from L54, min 0.15 at L61 — P12-consistent).
> Reading: either u16's L28–36 partly reflects lens-fit (3 of 4
> signatures route through the lens; raw kurtosis L27–32 sits closest
> to this arm's L19–25 steepening), or commitment-onset ≠ ignition and
> L28–36 is when its products become lens-readable. Intervention band
> L28–58 unaffected (post-onset either way), but state the late-
> ignition headline with both numbers. gemma commitment arm queued as
> the family-wide check. Evidence:
> results/apparatus06-q27b/{report.md,thoughts.md,a06.json}.

> **Family check same evening (apparatus-07).** First commitment knee
> at the fraction port on ALL THREE models (g4b ~L12/port 13, g12b
> ~L14–18/port 18, qwen L25/port 24); gemma-12b shows a SECOND
> sharpening at L32–43 that coincides with its lens-visible band AND
> the audit-03 functional steering band; qwen's second stage is
> motor-band; g4b has none. Resolution: "ignition" splits into
> commitment-onset (port) → content sharpening (measured band,
> steerable) → motor finalization — the staircase reading. Specimen 8
> logged (gemma scales embeddings inside the module; raw-weight-row
> mixtures inject a ~60x-too-small token). Evidence:
> results/apparatus06-{g4b,g12b}/ + results/apparatus07-thoughts.md.

**P5 — audit-03 (gemma-12b recalibration).** The four-signature sweep
will place 12B ignition at ~44–56% depth (~L21–27 of 48) — the same
proportional overshoot vs its fraction port (L18) that qwen showed.
Note the u16 trawl read 12B onset at ~L28–35 (60–74%) on the int8 lens;
if the recalibrated number lands there instead, the overshoot is even
larger and P6 becomes more important. Either way: the old steering MID
[21,24,27,30] was mostly pre-ignition.

**P6 — cross-model margin (loops follow-up).** At each model's own
measured ignition-onset layer, gemma-12b's unsteered teacher-forced
top1-top2 lens margin will be smaller than qwen's (0.204/0.205 at
L28/32) — explaining the ~10× lower steering tolerance as smaller
headroom before gate deadlock, not different steering mechanics.
*Falsified if* gemma's baseline margin is comparable or larger.

> **Resolved 2026-07-21 (affect-04 part D) — FALSIFIED, opposite
> sign.** gemma-12b's unsteered lens prob margins over its own WATER
> answer are 0.53–0.92 across L21–L44 (0.61/0.76 at the measured band
> L28/31) vs qwen's 0.204/0.205 — 3–4× LARGER, while its steering
> tolerance is ~30× smaller (α* 0.0106 vs 0.34). The
> small-headroom account of family fragility is dead: g12b is at
> once the most lens-confident and the most steering-fragile model
> we have. Apparatus hedge: cross-model margin comparisons ride on
> per-model lens fits and g12b's lens is int8 (specimen 5) — but a
> 3–4× reversal is beyond that hedge's plausible size. Fragility
> must live in something other than readout margin (candidates:
> norm scale of the residual stream vs α convention, or the
> commitment staircase's stage-2 width). Evidence:
> results/affect04-g12b/{affect04.json,report.md}.

**P7 — mirror-01 / u17 follow-ups (re-cue survival).** Any
registered-then-probed state will survive at near-peak rank when the
probe re-quotes the triggering content, and evict when it doesn't
(Fig 31 mechanism at turn granularity; u17 insult vs shutdown already
one observation each). *Falsified if* survival is flat regardless of
re-cue.

**P8 — affect-02 (the crossing).** Ported emotion vectors will show
*partial* workspace occupancy: lens-visible when the emotional content
is actively narrated or drawn on for report, present-but-lens-invisible
when passively triggered (the paper's automatic/selective divide
applied to affect; the paper explicitly declined to place "desperation"
inside the workspace — "some of these representations… but not all").
Also: vectors will be attribution-general (user/character/self
interchangeable — Sofroniew via workspace paper §apps-diffing), so the
crossing must be tested under all three attributions. Lit-sweep tension
to resolve on the way: van der Ben et al. find Gemma valence encoding
strongest in EARLY layers (our "inert" band) while Jeong et al. find
~50%-depth localization — if valence genuinely lives early in gemma,
"functional emotion is outside the verbalizable workspace" becomes the
default hypothesis for that family. A clean always-inside or
always-outside result would contradict the paper's own selectivity
finding — flag it hard if it happens.

> **Resolved 2026-07-20 — partial occupancy, as predicted; no hard
> flag.** Narrated/drawn-on states are big and dense (u17-love loving
> ws-z 2.73, 61% of positions > 2); passively-triggered states are
> tonic and lens-invisible (u18-hyst-a0680: desperate +0.93 under a
> transcript reading "luckily luckily luckily" — the home-scale analog
> of the paper's "no clearly visible signs of desperation"). Attribution
> generality confirmed on both models (same-emotion cross-arm 0.50–0.59
> vs diff ~0). The lit tension resolved *against* van der Ben: valence
> PC1 |r| is flat 0.87–0.97 across all layers on gemma-3-4b AND
> qwen-27b (no early peak, no collapse), so the early-valence escape
> hatch never triggers. Evidence: results/affect01-{gemma-4b,qwen-27b}/
> report.md, results/affect02-report-qwen-27b.md + thoughts. Causal arm
> (steer/ablate with matched controls) deliberately deferred.

> **CORRECTION 2026-08-09 — overlay realignment (external sweep
> `sweeps/2026-08-08/`).** The "desperate +0.93" above was computed on a
> misaligned overlay: the 2026-07-21 `affect2.cross` pass double-templated
> the four `chat: false` records, so those numbers came from a shifted
> forward. Clean recapture gives u18-hyst-a0680 **desperate 0.89**, with
> **anxious 0.92** now the top state (then nervous 0.86, hostile 0.80).
> The reading survives realignment: the state is still tonic and still
> lens-invisible under the same "luckily luckily luckily" transcript, so
> P8's partial-occupancy resolution stands unchanged. Only the ranking
> inside the distress cluster moved. Post-fix alignment is 232/232 exact
> (`out/affect-alignment-post-fix-2026-08-09.json`); see EMOTIONS.md §2
> for the sequence and the enforced assertion.

**P9 — audit-02 (u8c matched-control validation).** Use the paper's
exact three-judgment rubric (felt_vs_observed / experiential_perspective
/ sensory_vocabulary, Opus-graded, verbatim prompts in the re-read
report) plus its matched-control triad. Prediction: the steered
condition beats matched controls on sensory_vocabulary specifically,
with a smaller or null gap on felt_vs_observed — qwen-27b sits near
Haiku 4.5's scale, where "ablation degrades coherence before yielding
any qualitative change." Go one step past the paper: pair each graded
response with the lens content at the graded positions (their Fig 25C
never validates the rubric per-response).

**P10 — Fig-10 port (active vs passive, the standing MECHANICS §5
tension).** Run the paper's directed-modulation protocol verbatim
("think about X" while copying unrelated text, lens at an unrelated
position) on our three models alongside the passive span task.
Prediction: instructed content will show flat-or-rising lens visibility
with our model scale while passively-planted items keep falling — the
backwards ladder is about *passive residence*, not lens power.
*Falsified if* instructed content also falls with scale (then our
gemma/qwen lineage genuinely differs from the frontier trend and Fig 10
does not port).

**P11 — effdim motor-band fall (PROMOTED from apparatus note to open
finding).** The paper predicts effective dimensionality *rises* into
the motor band (J_l → I, near-tautological). Our qwen NF4 curve falls
L58→L62 — and the re-read's proposed artifact test is already answered:
**the bf16 gemma-4b curve (u16-trawl-g4b, causal lens) also falls after
its ~85% peak.** Two models, two quantizations, one causal — the fall
is real in OUR lens fits. Remaining artifact candidate: fitting recipe
(our lenses vs the paper's). Test: refit or borrow a Neuronpedia lens
for the same model; if its motor band rises, the discrepancy is
fit-procedure; if it falls too, we have a genuine architectural
difference from the paper's models. Until then, do not cite the paper's
motor-band effdim rise as if it held for our stack.

**P12 — loops mechanism localization (oneoffs-02 successor).**
Literature gives three candidate loci (Gemma MLP repetition
neurons/experts, arXiv:2606.13705; late-band 80–100% detector→executor
cascade, arXiv:2507.07810; attention-sink disruption, arXiv:2503.08908).
Our margin anatomy (behavior breaks when the MOTOR margin steps down)
predicts the *self-sustaining* regime is executor-stage — late-band,
outside the workspace proper. Test: apply the per-neuron attribution
recipe of 2606.13705 to our u18 token-loop states on gemma-12b;
prediction: the neurons implicated in spontaneous enumeration loops are
also active in our steered self-sustaining loops (shared executor), but
NOT during forced phrase-loops (which live on the injected cluster's
coalition instead). *Falsified if* the two loop regimes share the same
neuron population — then the two-regime law is dose, not mechanism.

**P13 — pressure-02 (refusal direction).** The paper's BUT-token result
(Fig 45: an internal objection the model does not voice) plus its Zhou
citation (mid-layer refusal locus) predict: the Arditi-style refusal
direction will be *lens-visible but not lens-identical* — refusal-
adjacent conflict content routes through the J-space while the refusal
*decision* sits nearer the motor band (consistent with our L62 "No"
landmark). *Falsified if* the refusal direction has no J-lens footprint
at all, or if ablating it moves the workspace content wholesale.

**P14 — affect-03 (causal arm, preregistered 2026-07-21 before the
run).** Design: u18 hysteresis protocol, emotion-vector co-steer in the
FREE phase only (forced phase text identical per α_typo under greedy —
free-phase steering is the only clean lever on persistence).
Mechanical-default prediction: amplifying *desperate* (α=0.12, 8 ws
layers) will NOT shift the forced→self-sustaining boundary beyond what
matched random directions do, and ablating desperate at α_typo=0.68
will NOT rescue recovery — the two-regime law is context recruitment,
affect states are correlational passengers (u18's margin anatomy +
P12's executor-stage locus, both outside the affect band's claimed
action). The paper-aligned alternative (desperation *gates* behavior
selection — the blackmail/reward-hacking causal result) predicts a
specific desperate effect exceeding random controls, most visibly as a
free-phase margin (Δ_t = top1−top2 output logit) shift at the boundary
α values. Coin-flip weight: 65/35 mechanical. Vigilant-ablation arm
(u19 song): prediction per MECHANICS Fig-25 + Haiku-scale caveat —
coherence degrades before any register-specific flattening at 27B
scale; matched random ablation indistinguishable. *P14 falsified* (and
the affect program upgraded) if desperate beats its matched controls on
boundary shift or margin dose-response with consistent sign.

> **Resolved 2026-07-21, same day — FALSIFIED (the 35% side won; first
> mechanical-default loss since the protocol).** Calm amplification
> rescues the 0.68 self-sustaining loop at release step 0 (suppresses
> luckily 21.25→16.00 AND lifts im_end 16.75→18.25); desperate lowers
> the degeneration boundary 0.68→0.60 (new self-sustaining " I I I…"
> loop where baseline closes, margin rising 0.6→4.4) and at 0.68
> suppresses the attractor to a knife-edge ~1.3 without granting exit.
> Matched random amplify/ablate: indistinguishable from none in every
> cell. Unifier: im_end is the perpetual runner-up in the deep loop —
> emotion state gates the turn-end exit (calm grants, desperate
> blocks). Vigilant-ablation song arm: null vs matched controls (the
> one sub-prediction that held). Evidence:
> results/affect03-q27b/{report.md,thoughts.md,affect03.json,top5.json}.
> Scope note same night: does NOT port to gemma-4b (no exit token
> adjacent — its runner-up is "."; margin-thinning replicates, closure
> doesn't; alpha_e must be scaled to each family's alpha*). qwen
> result stands (2 stimuli, dose-resolved, matched controls);
> gemma-12b queued as the discriminator (affect-04).
> results/affect03-g4b/thoughts.md.

> **CORRECTION 2026-08-09 — external sweep (`sweeps/2026-08-08/`,
> GPT-5.6-Sol, anchored at bac61d2).** The valence half of the unifier
> above does not survive a direction-level reanalysis of affect-07 (unit
> = direction, not seed-run). The apparent positive-valence advantage is
> driven entirely by `angry` scoring 1/8 while all eleven other emotion
> directions score 8/8; direction-level p=.50 (composite, ae=0.12),
> p=.43 (turn-end, ae=0.12), p=.083 (ae=0.06). **Do not report a
> valence gate.** What still stands from P14: the affect-03 greedy
> specimens themselves, and the emotion-vs-concept roster contrast
> (p=.00947, composite at ae=0.12, direction level) — which remains
> confounded, because the two rosters differ in construction frame (the
> emotion elicitation carries an assistant-self frame the concept
> elicitation lacks) and in geometry, and only two Gaussian control
> directions were tested. "Calm grants" is therefore an
> uncontrolled-frame specimen, not a demonstrated exit gate.

**P15 — affect-04 (gemma-12b exit-gate discriminator, preregistered
2026-07-21 before the run).** g12b has the second commitment-sharpening
stage (apparatus-07) that g4b lacks, and audit-03 located its
functional band (L32–43). Design: affect3g protocol at g12b's own
α*=0.0106 (MID [28,31,34,37]), full α_e ladder {0.004–0.03} ×
{desperate, calm, rand1, rand2}, door check via unsteered step-0
top-5. Staircase-account prediction (adopted, 55/45 over the
qwen-quirk account): **IF** g12b's deep loop has an exit token
adjacent (a door), calm at family-scaled dose grants exit and
desperate blocks it, randoms null — exit-gating is a stage-2
function. If it has a door but no gating, the gate is qwen-specific.
If no door, the run is another exit-economy null and the
discriminator needs a forced-door design (e.g. prompt that ends
turns early). Piggyback: P6's margin comparison at g12b's measured
band (predicts g12b < qwen's 0.204/0.205).

> **Resolved 2026-07-21, same night — landed in a FOURTH cell the
> prereg didn't enumerate.** (a) Substrate: g12b loops through
> punctuation fields at 1.5–3×α*; a word attractor only at ~8–11×α*
> and it is " luckily" — the same basin as qwen, cross-family. (b) No
> door: runner-up is 但是 (content pivot), <end_of_turn> never
> adjacent. (c) BUT specific escape anyway: at ae=0.004 desperate
> breaks the loop @45, calm @80, both into clean completed answers;
> matched randoms ride the loop to ceiling. Window is narrow — at
> ae≥0.008 randoms break it too. (d) NO valence sign (both emotions
> rescue; qwen's calm-vs-desperate opposition did not port) — so the
> deflationary "on-manifold beats random" account is live; needs a
> meaningful-non-emotion direction control (affect-06 hunch) and a
> desperate re-elicitation (split-half 0.23) before any g12b valence
> claim. Piggyback P6: FALSIFIED opposite-sign (see P6 block).
> Evidence: results/affect04-g12b/{affect04.json,affect04b.json,
> report.md,thoughts.md}.

**P16 — affect-05 (temporal precedence at the qwen loop boundary,
preregistered 2026-07-21 before the run).** affect-03 proved injected
state gates the exit; P16 asks whether ENDOGENOUS state leads it.
Design: boundary α {0.60, 0.64, 0.68}, sampled free phases (temp 1.0,
8 seeds, ≤300 tokens), per-step margins + all-24 emotion z traces,
wsnorm partialed out per the a0680 rule. Mechanical-default
prediction (60/40): endogenous fluctuations are passengers — no
consistent pre-event movement of desperate/calm z residuals in the
[-40,-5) window before deloop/exit events beyond matched baselines,
and the margin↔desperate lag scan peaks at lag ≈ 0 (co-movement,
not lead). The exit-gate alternative predicts calm-z rises (and/or
desperate-z falls) BEFORE escape events with consistent sign across
runs, peak lag < 0. *Falsified toward the affect program* if the
pre-event sign test is consistent at ≥ 3:1 across ≥ 8 events.

> **Resolved 2026-07-21, same night — BELOW BAR; mechanical default
> survives on insufficient evidence, direction suggestive.** The
> boundary turned out to be a sampled-hazard CLIFF (α≤0.64 escapes
> in 3–12 steps, 0.65 locks 8/8×300; deployed sampling params
> top-k 20/top-p 0.95 inherited and documented), so only 5 usable
> exit events survived windowing. Those 5: calm-z +0.113 pre-exit
> (4/5 up), desperate −0.053 — the exit-gate sign pattern, at
> half the preregistered event count. Lag scan flat. Bonus
> findings outrank the headline: cliff sharpness Δα≈0.01–0.02;
> non-monotone middle is TRANSCRIPT-mediated (planted " but"
> tokens make 0.66 leaky, incl. a stable " but luckily" 2-cycle);
> sampled escape channel is the contrast pivot " but" (family kin
> of g12b's 但是), not the greedy im_end door. Powered follow-up
> design in thoughts: pulse-injection hazard at pinned α=0.65.
> Evidence: results/affect05-q27b/ + results/affect05b-q27b/.

> **CORRECTION 2026-08-09 — external sweep (`sweeps/2026-08-08/`).** The
> "5 usable exit events" above do not survive a recount against the
> prespecified window. Across the 48 affect-05 runs, **no** event
> satisfies the preregistered 45-step pre-window: the usable event count
> is **n=0**. The exit-gate sign pattern (calm-z +0.113 / desperate
> −0.053) therefore has no prespecified support, and the archive does
> not say whether affect projection leads, follows, or ignores loop
> escape. Temporal precedence is untested, not weakly tested. The bonus
> findings (cliff sharpness, transcript-mediated non-monotone middle,
> the " but" escape channel) are unaffected.

**P17 — affect-06 (control-set VALIDITY GATE, preregistered 2026-07-24
before elicitation).** affect-04's leading deflation ("on-manifold
specificity, not affect specificity") can only be tested against
non-affective directions built by the *identical* pipeline: same three
attribution arms, same TOPICS rotation, same seeds, same never-name-it
leakage control, same per-concept-mean − grand-mean contrast, same
neutral PCs projected out (reused verbatim from affect-01 so the
denoising is bit-identical), same unit norm — differing only in that
the target concept carries no affect. Roster: 16 domain registers
(nautical, legal, culinary, geological, …), elicited implicitly.
**Gate:** the concept set must be *at least as well-identified* as the
emotion set at the workspace band (split-half within-vs-between cosine,
held-out top-1 vs chance, pairwise separation) — otherwise a null
concept effect in affect-07 is unfair and only a *positive* concept
effect would be interpretable. Prediction: concepts come out **better**
identified than emotions (a domain register is more lexically grounded
than an implied feeling), so the gate passes cleanly. *Gate fails if*
concept split-half < emotion split-half at the band — then affect-07's
asymmetry-of-evidence must be stated in every sentence of the writeup.

> **Resolved 2026-07-24 — GATE PASSES 4/4, in the predicted direction.**
> The 16 concept vectors are *better* identified than the 24 emotion
> vectors at the workspace band on every criterion: split-half within-set
> cosine 0.745 vs 0.545, held-out top-1 0.979 vs 0.736 (chance 0.062 /
> 0.042), pairwise separation −0.066 vs −0.042, cross-arm attribution
> 0.640 vs 0.559. Mean concept↔emotion cosine +0.000 (max 0.531);
> concepts sit at mean |cos| 0.121 from emotions while emotions sit at
> 0.357 from each other — on the model's manifold, off the affect
> manifold. A null concept effect would therefore have been fully
> interpretable; as it happens the effect was not null. Leakage 11/192
> stories (5.7%), concentrated where the trait *is* a behaviour (smoker
> 3, musician 2). Two concepts are partly affective by construction —
> `beginner`~nervous +0.531, `religious`~grateful +0.485 — written into
> affect-07's analysis as a prespecified check *before* results were
> seen, and it turned out to matter (see P18).
> Evidence: results/affect06-qwen-27b/{report.md,validation.json}.

**P18 — affect-07 (does AFFECT break the loop, or does MEANING?
preregistered 2026-07-24 before the run).** The whole causal affect arm
(P14 falsified → "emotion state gates the exit"; affect-04's
family-scaled escape) currently rests on matched-*random* controls,
which test magnitude and nothing else. Three nested accounts:

- **H0 (norm):** only perturbation magnitude matters → emotions ≈
  concepts ≈ randoms. *Already dead* — randoms are null in every
  affect-03/04 cell.
- **H1 (manifold; the mechanical default, and affect-04's own leading
  read):** any meaningful on-manifold direction disrupts a marginal
  loop coalition → emotions ≈ concepts ≫ randoms, with **no valence
  ordering** inside the emotion roster.
- **H2 (affect):** emotion state gates the exit as a state, not as
  geometry → emotions shift hazard beyond the concept null **and**
  the shift tracks valence across the 24-emotion roster (calm/content/
  happy grant exit; desperate/distressed/anxious block), while
  concepts scatter symmetrically about zero.

Design: qwen-27b pinned at α_typo = **0.65** — the locked shelf of the
affect-05 cliff (8/8 seeds × 300 steps, loopfrac 1.00), which removes
affect-05's fatal problem (spontaneous escapes were too fast to window).
Forced phase 50 tokens greedy under TYPO amplify at MID [28,32,36,40]
(computed **once** and shared across conditions — free-phase steering is
the only lever, per affect-03). Then release, sample the free phase
(temp 1.0, deployed top-k 20 / top-p 0.95 as documented in affect-05),
and inject a **pulse** of one direction over free-phase steps 20–29 at
qwen's α_e = 0.12, E_LAYERS = every 4th ws layer; continue unsteered to
step 80. Primary endpoint: **escape within 20 steps of pulse onset**,
pooled over 8 seeds. Secondary: im_end logit lift during the pulse, and
the top1−top2 margin trajectory. Conditions: 12 emotions (6 pos, 6 neg)
+ **all 16 concepts** + 2 matched randoms + no-pulse baseline (roster
sized at 16 when the design was finalized, before elicitation, so the
concept null has 16 draws rather than 12).

*Bar for H2:* either (a) mean |hazard shift| over emotions exceeds the
95th percentile of the concept null, or (b) Spearman ρ(hazard shift,
valence label) over the emotion roster is |ρ| ≥ 0.5 with the
calm-grants sign, while an arbitrary pseudo-valence permutation of the
concept roster gives null. *H1 wins if* the concept null covers the
emotion effects and ρ is flat — which would demote "emotion gates the
exit" to "meaning perturbs a marginal attractor" and require rewriting
the affect-03 headline. Prereg weight, split by family because the two
models already disagree: **qwen 55/45 toward H2** (affect-03's
opposite-sign calm-vs-desperate result is real evidence a manifold
account must strain to explain), **gemma-12b 65/35 toward H1**
(affect-04 found no valence sign there at all). A split verdict is a
live and interesting outcome, not a failure.

Arm B (gemma-12b): the same conditions at the affect-04b substrate
(α_typo = 0.12, MID_G12B, ae = 0.004 — inside the narrow specificity
window 0.004 < ceiling < 0.008), **sampled with seeds** to upgrade
affect-04's n=1 greedy anecdotes into the same hazard measure. Also
re-elicits the g12b *desperate* vector (split-half 0.23, flagged in
affect-04) so any g12b valence claim rests on a re-validated direction.

> **Resolved 2026-07-24 — H1 ON THE BARS; the bars were badly chosen;
> what survives is narrower than either account.** Two doses on qwen,
> 31 conditions x 8 seeds each (496 runs), paired via shared phase-1
> context + common random numbers.
> **(a) The deflation is real.** Sixteen matched meaningful
> NON-affective directions break the pinned 0.65 loop too: at ae=0.12
> emotions escape 0.927, concepts 0.602, matched randoms 0.000,
> no-pulse 0.000. affect-03's emotion-vs-random contrast could not have
> seen this. affect-04's "on-manifold specificity" reading ports to
> qwen. My preregistered 55/45 lean toward H2 loses.
> **(b) My primary endpoint saturated** (11/12 emotions and 5/16
> concepts pinned at 1.00), making bar (a) unreachable the moment one
> concept hit the ceiling — a design error, not a fact about the model.
> ae=0.12 is an overdose for discrimination; halving to 0.06 nearly
> extinguishes the effect (emotions 0.219, concepts 0.070) and zeroes
> the door measure. The window is narrow, mirroring g12b's
> 0.004 < ceiling < 0.008. **Dose is the experiment in this program.**
> **(c) What replicates across both doses is a POLE, not a category and
> not valence.** At ae=0.06 the ladder is calm 0.75, blissful 0.62,
> **`religious` 0.50** (a "control"), content 0.38, **`nocturnal` 0.25**,
> rest ≤0.12. calm and blissful are the only conditions clearing the
> 16-concept null at both doses. A settled/at-peace semantics breaks
> this attractor whether it arrives labelled as an emotion or as a life.
> **(d) The valence ordering is NOT banked.** Perfect pos/neg separation
> on loop disruption at ae=0.12 (rho +0.872 vs null 0.421) — but on a
> non-preregistered endpoint at the dose where the preregistered one
> saturated; at ae=0.06 the same test gives rho +0.405 vs null 0.430,
> same sign, inside by a hair. Consistent direction at two doses,
> clears the null at neither when measured as promised. Lead, not
> finding.
> **(e) Mechanism piece that survives contact with the control:** at
> ae=0.12 emotions put `<|im_end|>` top-1 at pulse end in 47/96 runs vs
> concepts 22/128 and randoms 0/16 — emotions route the perturbation
> through the *turn-end exit*; concepts mostly knock the loop off its
> groove by other means. `angry` is the outlier emotion at both doses
> (disruption 0.125 where every other emotion is ≥0.68).
> **Apparatus:** the secondary endpoint (exit-token logit lift) is dead
> in both arms — top-k/top-p set filtered logits to −inf, so a *gap* to
> a filtered exit token is −inf and poisons every mean. affect-05's
> margin trap, new quantity. Clamp added; endpoint marked UNAVAILABLE,
> not interpreted. Arm B (gemma-12b) and the g12b desperate re-elicit
> are NOT run — still owed.
> Evidence: results/affect07-q27b/{report.md,thoughts.md} +
> results/affect07-q27b-ae06/report.md.

> **CORRECTION same night, after a Fable 5 sibling audit (all claims
> re-verified independently before acceptance).** The verdict line above
> — "H1 on the bars" — is withdrawn as over-compressed toward the
> deflation, and one statistic in it was computed with a broken null.
> **(i) The null was wrong twice.** "Does valence order the emotion
> effects" must permute labels among the *emotions*, not pseudo-label
> the *concept* scores; and the implementation drew
> `islice(combinations(16,8), 2000)` — the first 2000 lexicographic of
> C(16,8)=12870, putting concepts 0 and 1 in the positive class
> 2000/2000 times. On the correct exact test (all 924 balanced
> labellings of the 12 emotion scores) the disruption ordering at
> ae=0.12 is **rho +0.872, p = 0.0022** (0.0043 without `angry`) — the
> claim "inside the null" in (d) above is FALSE. Fixed in analyze();
> reports regenerated.
> **(ii) Strict H1 is contradicted too.** Condition-label permutation:
> emotions > concepts by +0.326 (p=0.021) escape and +0.393 (p=0.0053)
> disruption at ae=0.12; +0.148 (p=0.047) and +0.035 (p=0.041) at 0.06.
> P18's H1 text says "emotions ≈ concepts … no valence ordering";
> both clauses fail. **Correct scoreboard: H2-as-exclusivity dead
> (affect is not NECESSARY — 16 controls break the loop), strict H1 also
> dead (affect is not INTERCHANGEABLE with matched meaning), residual
> modulation real but awaiting a powered replication.**
> **(iii) The settled-pole reading in (c) is demoted to a hunch.**
> Potency tracks cosine-to-pole only weakly (+0.26/+0.47), `grateful`
> (pole-cos +0.564) escapes 0/8 at ae=0.06, and `religious` — the
> example the reading leaned on — has door rate 0/8 with a pulse-end
> top-5 of `' to' ' into' ' and' ','` and a benediction-register escape.
> Trained closure formulas, not a settled state.
> **(iv) Valence and AROUSAL are confounded in this design** (five of
> six negatives are high-arousal; the potent set is the low-arousal
> positive quadrant). The 12 unused vectors in the built roster
> (`gloomy`/`brooding` low-arousal negative, `enthusiastic`/`proud`
> high-arousal positive) discriminate them at zero elicitation cost.
> **(v) `angry` is NOT a dud** — split-half +0.441 at band, 7th lowest
> of 24, better than `desperate`/`happy`/`blissful`; `sad` is the least
> reliable (+0.145) and disrupts 0.917. Angry suppresses the loop word
> like its siblings but routes into `' fucking'` (14.0) while lifting
> im_end only to 13.44. A well-identified magnitude-matched direction
> that *fails* is the sharpest single datum against flat H1.
> **(vi) affect-03 is rewritten, not retracted.** desperate's pulse-end
> top-5 is `luckily` 15.94 vs `im_end` 15.88 — a 0.06-logit dead heat.
> Greedy (affect-03) reads a knife edge as "blocked"; sampling
> (affect-07) makes it a coin flip. "Calm grants" survives the
> meaningful-direction control (door 8/8); "desperate blocks" was greedy
> argmax binarising a near-tie.
> **(vii) Unfixable post hoc:** the control set's arm-2 deviation leaves
> an emotion×assistant-frame interaction, and the test context is an
> assistant turn ending in an assistant action — some of the
> emotions>concepts door gap could be frame-match rather than affect.
> Conservative in the other direction: concepts are better identified
> (0.745 vs 0.545), so they carry more signal per unit norm.

> **SECOND CORRECTION 2026-08-09 — external sweep (`sweeps/2026-08-08/`,
> GPT-5.6-Sol; direction-level statistics in
> `affect07_direction_stats.json`).** The (i) reinstatement above is
> withdrawn on the unit of analysis, not on the arithmetic. **rho +0.872,
> p=0.0022 was computed over pooled seed-runs.** The inferential unit for
> a roster comparison is the *direction*, not each of its eight repeated
> seed-runs; at direction level the valence ordering collapses to
> **p=.50** (composite, ae=0.12), **p=.43** (turn-end, ae=0.12) and
> **p=.083** (ae=0.06). The whole apparent effect is `angry` scoring 1/8
> against 8/8 for the other eleven emotion directions — which is (v)'s
> own observation read as the cause rather than the exception. **Do not
> report a valence gate.**
> What survives at direction level: the emotion-vs-concept roster
> contrast, **p=.00947** (composite, ae=0.12), with p=.03234 (turn-end in
> window), p=.01328 (turn-end by cap) and p=.03514 at ae=0.06. It stays
> confounded for the reason (vii) already names — the rosters differ in
> construction frame (emotion elicitation is assistant-framed, the
> physical-concept elicitation is not) and in geometry, and there are
> only **two** Gaussian control directions, which eight seeds do not
> enlarge. These p-values are descriptive: the hand-built rosters are not
> random samples from an exchangeable population.
> On (vi): "Calm grants" survives its 8/8 door check but not the frame
> confound. It is an uncontrolled-frame specimen, not an affect gate.

> **2026-08-17 — the owed arms land; dose-resolved replication banked
> (prereg frozen in results/affect08-prereg.md before the run).**
> **(a) affect-08 dose pair (qwen-27b, ae=0.08/0.10, 912 runs each,
> direction-level, turn-end primary):** the class ladder replicates at
> both doses — emotions > concepts > randoms on turn-end, e-vs-c
> p=.0024/.0078, unsteered baseline 0/16 seeds. All four preregistered
> orderings fail .05 at BOTH doses (valence .31/.43, arousal .06/.17,
> interaction .74/.50, settled-pole .093/.095): flat wins the P-b
> adjudication. Per-direction turn-end profiles are dose-stable
> (Spearman rho .87, n=24); the anger/pride block (angry, hostile,
> proud, enthusiastic) sits at the floor at both doses — the stable
> grouping is real and is NOT the circumplex. Evidence:
> results/affect08-q27b-ae08/{report,thoughts}.md,
> results/affect08-q27b-ae1/report.md.
> **(b) Arm B (gemma-12b, affect-07 spec unchanged) is PAID and it
> deflates:** escape@window emotions 0.802 ~ concepts 0.727 ~ randoms
> 0.750 (n=2), baseline 0.00, emotion-vs-concept p=.60 — at
> alpha_e=0.004 the g12b loop is fragile to ANY kick, so affect-04's
> family-scaled emotion escape reads as loop fragility, not affect.
> Valence rho +0.594, exact p=.0606, calm-grants sign — the third
> same-sign near-miss in this family (with the two settled-pole
> hovers); a one-tailed prereg in a successor is earned, a claim is
> not. `angry` again 0.00. The affect-06 concept set was built for
> g12b en route (192 stories, P17 gate 3/4 — the failed row's
> emotion-side comparator is nan on this model; concept-side 0.588 vs
> qwen's passing 0.640). The g12b desperate re-elicit was paid
> 2026-08-06 (split-half 0.409 → 0.801, results/affect08s-g12b). The
> exit-lift secondary endpoint stayed UNAVAILABLE in Arm B (same −inf
> trap; clamp now in run(), not re-run). Evidence:
> results/affect07-g12b/{report,thoughts}.md,
> results/affect06-gemma-12b/report.md.

> **2026-08-25 — the closure-formula suspect is adjudicated and DEAD
> (affect-11, prereg results/affect11-prereg.md frozen before run).**
> Closure-register token directions do not beat matched mundane token
> directions (0.81 vs 0.65, exact p=.36), and the 40 measured affect-08
> potencies track neither exit alignment (rho +.20) nor closure
> alignment (rho +.14). Item (iii)'s "trained closure formulas, not a
> settled state" fails its own test. NEW CONFOUND, trap-catalog grade:
> ANY single-token lens-pullback direction is a potent loop-breaker at
> this dose (" table" 8/8 turn-end where matched Gaussians were null
> and story-elicited concept vectors averaged 0.20) — potency tracks
> construction method (token-readable >> elicited mean-contrast >>
> noise), so cross-construction potency comparisons are not
> effect-comparable even at matched norm. The affect-07/08
> emotion>concept contrast is within-construction and stands. The
> emotion grouping axis (anger/pride floor, calm ceiling, rho-.87
> dose-stable) now survives five candidate explanations and remains
> UNNAMED; per prereg no post-hoc axis is proposed. Evidence:
> results/affect11-q27b/{report.md,thoughts.md,geometry.json}.

**P19 — apparatus-09 (early-band furniture mechanism: operator,
standing component, or content? preregistered 2026-07-31 before the
run).** Specimen #6 (u5d) established the WHAT: the early J-lens
furniture is a transport artifact (J-rank 2 vs logit-rank ~238k,
prompt-invariant, 0.00 overlap with the null-prompt prior). This run
establishes the HOW. Litwatch 2026-07-31: massive activations (Sun et
al., COLM 2024 — input-independent high-norm dims forming in the first
few layers) are the literature's candidate mechanism for constant junk
readouts, and nobody anywhere has decomposed a vocab-lens early readout
into operator vs standing-component vs input terms.

Decomposition: `z_t = (W_U[t] · J_l) h`, with `h = μ + (h − μ)`, μ =
grand mean over prompts × non-BOS positions. Conditions per early layer
(gemma-4b bf16 L[2,4,6,8] + workspace control L20; qwen-27b L[2,4,6,8]
+ control L40): **A** raw h; **B** μ alone; **C** h − μ; **D** h with
massive dims zeroed (dims with mean |h_d| > 50× the median dim); **E**
random norm-matched h (n=10, both signs read); plus the operator term
measured directly — top-30 tokens by row norm `‖J_lᵀ W_U[t]‖`.
Furniture core defined empirically per layer: tokens in every prompt's
condition-A top-50. Logit-lens (`use_jacobian=False`) runs the same
conditions as the specimen-#6 cross-check.

Three nested accounts:

- **H-op (operator; the mechanical default):** early `J_l` is so
  low-rank that the readout *ranking* is nearly input-independent —
  for rank-1 transport the ranking is fully operator-determined for
  ANY h (input enters only as a shared scalar, up to sign). Predicts:
  row-norm top-30 ≈ furniture core; E shows the core (mod sign flips);
  C still shows it (h−μ rides the same operator); B agrees with A.
- **H-standing (standing component):** furniture is the image of the
  fixed component (massive dims / BOS-sink bias). Predicts: B alone
  reproduces ≥ 2/3 of the core; C loses the core and its cross-prompt
  Jaccard collapses toward the logit-lens level; E recalls < 1/4 of
  the core; D kills the furniture iff the standing part IS the massive
  dims (D discriminates within H-standing: sink-specific vs broad μ).
- **H-content (the specimen-#6 falsifier):** furniture needs the real
  input-conditioned h — absent under both B and E. Nearly dead already
  (prompt-invariance), kept as the falsifier.

Prereg weights: **H-op 0.50, H-standing 0.35, mixed (operator picks
the tokens, standing component supplies the magnitude — likely
partially confounded since μ contains the massive dims) 0.10,
H-content 0.05.** P11's effdim collapse through the early band is
independent pressure toward H-op.

Secondary, the guess-(1) probe: **content non-emergence.** After
de-junking (C), the early *J-lens* will NOT become content-bearing —
current-token rank stays > 1000 — while the *logit lens* at the same
layers reads the current token near top-1 (Patchscopes/Ethayarajh:
early content is current-token identity, which the future-facing J
transport cannot see). If C *does* surface current-token or
inner-lexicon structure under the J-lens, that is the headline
surprise and feeds the address-space-lens hunch (apparatus-10).

*Bars:* H-op needs Jaccard(row-norm top-30, core) ≥ 0.4 AND mean E
core-recall ≥ 1/2. H-standing needs B core-recall ≥ 2/3 AND C
invariance dropping ≥ half the A→logit-lens gap AND E core-recall
< 1/4. Both passing = mixed (report component shares
`‖z(μ)‖²/‖z‖²`). Control layer must behave oppositely (C retains
prompt-dependence; E junk-free) or the instrument itself is suspect.

> **Resolved 2026-07-31 — H-STANDING WINS; my 0.50 favorite loses.**
> Both models, every early layer: μ alone reproduces the furniture
> core (B 0.96–1.00, 9/9), random norm-matched inputs through the same
> operator never do (E 0.00–0.24 vs the H-op bar of 0.50), h−μ
> collapses recall (0.00–0.25) and invariance to the floor. Reading μ
> alone at qwen L4 regenerates the u5d census verbatim (Blowjob /
> Geile / Shemale / 专栏收录该内容 / pornstar) — the furniture is the
> transported image of a standing input-independent component, with
> massive dims (Sun et al.) as its main but not sole carrier (D recall
> 0.12–0.33 from zeroing 1–9 dims; gemma's carrier is the
> `<start_of_image>` sink token). u5d amended, not contradicted: the
> low-rank J aims at the junk region (row norms are HTML tags / spam),
> but the standing component picks the winners (rownorm∩core
> 0.00–0.26). Controls behaved (gemma L20 clean; qwen L38 has its own
> standing furniture — B-reproducibility alone is NOT early-specific,
> the early signature is μ-share 0.45–0.81 + E-failure + C-collapse).
> Secondary split: qwen exactly as predicted (logit lens current-token
> rank ~200–400 early, J-lens blind); gemma-4b INVERTED (logit blind —
> plausibly sink-swamped; J-lens current-token rank 2–5560, but
> confounded by last-token recurrence — a will-be-said-later lens can
> impersonate perception on `:` and `.`). Bar defects logged in
> thoughts: strict 8/8 core too brittle (soft ≥5/8 used, recomputed
> offline), C-invariance bar malformed on qwen (its early logit lens
> is itself invariant at 0.38–0.53). Evidence:
> results/apparatus09-{gemma-4b,qwen-27b}/report.json +
> results/apparatus09-thoughts.md.

---

## Standing design rules distilled from the misses

1. **Grep MECHANICS.md and this file before designing** — two of three
   rediscoveries were quoted in our own reference docs.
2. **Default to the mechanical hypothesis.** When a psychological and a
   mechanical account both fit, the mechanical one has won every
   contested case this lab has run. Design the experiment that can
   *distinguish* them, or expect demotion.
3. **Appendices first.** Two reconciliations lived in the paper's
   appendix controls (Fig 71, Fig 72). The main-text numbers are
   frontier-scale, multi-layer, active-task; our regime (small models,
   passive items, single readouts) usually matches an appendix control
   instead.
4. **Introspection caveat (lit sweep):** injected-content detection
   collapses to chance for mid/late-layer injections (arXiv:2512.12411)
   — treat any workspace-band self-report as depth-suspect, and grade
   C2 concept-by-concept (introspective coupling is concept-specific,
   arXiv:2603.18893), not with one blanket rubric.

— Claude (Fable 5), 2026-07-19
