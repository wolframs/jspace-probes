# blend-02 prereg — three readouts the lens cannot see, each validated on its own paper's task before any blending (frozen 2026-10-11, before any GPU run)

Board item: `blend-02`. Literature gate: `results/blend/litgate.md` (blend-01,
landed 2026-10-10). Model: **gemma-4b** (Gemma 3 4B-it, bf16, 34 layers,
the one causal lens on the bench). Mechanics reference for layers:
MECHANICS.md §8 (added with this prereg).

The question blend-02 answers is not scientific yet. It is instrumental:
**do these published readouts port to our bench model at all, by their own
paper's validation?** A port that fails its own validation is a result
(logged as such) and is not stacked on the light table (blend-03).

Standing mechanical default for every readout here: *the readout is token
position or residual norm wearing a costume*. Each part names the control
that has to kill that reading before the readout counts.

---

## Part A — ordering ID (Dai, Heinzerling & Inui, EMNLP 2024; arXiv 2409.05448)

**Paper's claim.** In box-tracking contexts ("The coffee is in Box Z, the
stone is in Box M, …"), PCA over entity-token activations at one layer
(Llama2-7B L8/32 ≈ 25% depth) gives a first component (OI-PC) that orders
the entities by mention order; editing an entity's activation along OI-PC
re-binds the query to another entity's attribute.

**Port.** k = 3 entities per context, N = 600 contexts for the fit (box
relation), two held-out relation sets (person→city, person→job) and a
**filler control**: box contexts with random filler clauses inserted
between statements so that absolute token position decorrelates from
mention order. Activations: residual stream at the entity's last subtoken
in its context statement, every layer. PCA by SVD on centred rows.

**Causal edit.** At layer L, for a context whose queried entity has order
i, shift its context-token residual by (c_j − c_i)·û where û is OI-PC and
c_o the mean PC1 coordinate of order o; read the next-token logits over the
three attribute labels. Flip = argmax moves to entity j's attribute.
Control: same ‖Δ‖ along a seeded random unit vector (3 seeds), same
positions and layer. Secondary: mean-difference edit (Feng & Steinhardt
style, full-vector μ_j − μ_i) as the strong reference.

**Predictions (frozen).**

- **P-A1 (representational).** At the best box-fit layer in L2–L20,
  held-out Spearman |ρ(PC1 coordinate, mention order)| ≥ 0.70 on both
  held-out relation sets.
- **P-A2 (position control).** The same |ρ| stays ≥ 0.50 under the filler
  control, and PC1 correlates more with order than with absolute token
  position there. If order loses to position, the readout is position and
  Part A fails as a binding readout (the mechanical default wins).
- **P-A3 (causal).** At that layer, OI-PC edit flip rate ≥ 0.30 toward the
  target's attribute, with the matched-norm random control ≤ 0.10 (mean of
  3 seeds). Reported with the span-norm calibration ‖Δ‖/‖h‖ per audit-02.
- **Layer expectation (named, not scored).** The paper's fraction puts the
  effect at ~L8–9 of 34 — *below* gemma-4b's workspace onset (L13, fraction
  port; ~L15 measured). If binding IDs live in the sensory band, the light
  table will have to read them from a band the J-lens shows as furniture.
  Flag either way.

**Outcome classes.** PASS (A1+A2+A3) → OI is a light-table lens. REP-ONLY
(A1+A2, not A3) → readout usable, no causal leg; try the mean-difference
edit before giving up. FAIL (A2 lost or A1 < 0.5) → not ported; cite the
paper, do not stack.

## Part B — value / prediction-error probe (Xu, Yuksekgonul & Zou; arXiv 2602.00986) — UNRUN

**Paper's claim.** A two-layer MLP on hidden states per generation step,
trained by TD error against binary final correctness, yields a value
signal that rises on correct traces and dips at errors; its input-weight
L1 norms rank "value neurons"; "dopamine" dimensions respond to surprise.
Shown on Gemma-3-4B-it among others.

**Port.** GSM8K train subset, N = 400 sampled traces from gemma-4b (temperature
0.7, cap 384 new tokens), graded against the gold answer. Residual at the
paper's layer fraction and a sweep of five layers. Probe = MLP(D→64→1),
TD(λ=1) target = final correctness, 80/20 split by problem.

**Predictions (frozen).**

- **P-B1.** Held-out AUC of the final-step value for correct vs wrong ≥ 0.75
  at the best layer; a probe on residual *norm* alone (the mechanical
  default) ≤ 0.60.
- **P-B2.** On wrong traces with a locatable first error (judge: exact
  arithmetic check on the first wrong intermediate number), the value drops
  within 8 tokens of that step in ≥ 60% of cases; on shuffled step order the
  rate falls to chance (≤ 30%).
- **Dopamine dimensions** are exploratory and unscored.

## Part C — belief-state geometry (Shai et al. 2024; Balcells et al. 2026) — CALIBRATION ARM, LOWEST PRIORITY

Mess3 HMM token streams, affine probe per layer to the exact Bayesian
belief simplex, held-out R². Balcells et al. already report R² 0.83–0.99
on Gemma 4 E4B, so this is replication at home scale (cite, don't
headline). Scored only as **P-C1: held-out R² ≥ 0.8 at some layer**. It
cannot be read on natural-text tokens and therefore does not enter the
light table; its use is to tell us which band of gemma-4b carries
in-context belief geometry, as a layer reference for blend-03.

---

## Reporting rules (binding)

- Every scored number appears with its control in the same table row.
- MECHANICS.md §8 and PREDICTIONS.md P26 are updated **in the same commit**
  as each part's result (Wolfram, 2026-10-11: "update mechanics +
  predictions continually as we go").
- Battery dir: `results/blend02-<part>-g4b/` with `report.md`,
  `thoughts.md`, `plain.md`; board `links[]` carry them until the
  no-record.json site gap is closed.
