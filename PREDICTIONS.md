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
