# affect-15 prereg — is band cooperation a coalition or a dose law? (frozen 2026-09-29, before the run)

affect-14 Part 2 called calm's loop demolition **band-cooperative**: best
single injection layer +1% of the full-stack dLoop, any leave-one-out
removal −19–37%, LOLO losses summing to ~2× the full effect (GLOSSARY:
Band-cooperative coupling). The queued successor asked *where cooperation
turns on* (layer count k).

Re-reading affect-14's own table before designing (CPU, no new data)
shows a mechanical alternative that the original analysis did not test:

- A plain convex dose law fits calm exactly. If dLoop ∝ (k/8)^p, the mean
  LOLO kept-fraction 0.748 gives p = 2.18, which predicts a single layer
  at 1.1% — observed best single +1%, mean −2.8%.
- **proud shows the same shape** (LOLO kept 0.760 → p = 2.05; singles
  ~0), although it is margin-inert. " table" also (p = 2.37), plus a
  ~10%/layer additive part.
- So super-additivity in k is expected from ANY convex response to total
  injected push, coalition or not. Counting layers at fixed per-layer α
  (the originally queued design) cannot separate the two readings: both
  predict a convex k-curve.

The two hypotheses (protocol (c): mechanical vs "coalition"):

- **H-D (dose law, mechanical):** what matters is the total injected
  push; concentrating it in fewer layers at matched absolute norm does
  about as well as spreading it.
- **H-C (coalition):** the band must be engaged jointly; at matched
  absolute norm, fewer layers recover little of the effect.

The decisive arm is **dose matching**: inject calm into fewer layers at a
per-layer α raised so the summed absolute injection Σ_l α‖h_l‖ equals
the full-stack α = 0.08 injection. ‖h_l‖ = mean residual norm at the
hooked output of layer l over the last 20 positions of the forced loop
(measured once at setup, written to the JSON). α_S = 0.08 · Σ_E ‖h‖ / Σ_S ‖h‖.

## Harness (unchanged from affect-13/14)

qwen-27b (pre-4bit), same forced " luckily" loop (identity assert on the
loop word), affect-07 PRE/PULSE/POST = 20/10/50, TEMP 1.0,
`_sample_raw` raw logits, `_trace`, dExit / dLoop / dMargin = mean over
pulse steps vs the same-seed `none` (CRN), turn-end-in-window as
secondary. Seeds 16–27 (12) — the affect-14 Part-1 seeds, so the `none`
and `calm full@.08` arms double as a determinism check against
affect-14 (max abs trace difference reported, descriptive).

Layer sets (E_LAYERS = 28…56 step 4): full = all 8; k4s = [28,36,44,52];
k2s = [36,52]; k1 = [44]; k4c = [36,40,44,48]; k2c = [40,44];
k1_32 = [32]; k1_52 = [52]; k6s = [28,32,40,44,52,56].
`@m` = dose-matched to full@.08 as above; `@.08` etc. = fixed per-layer α.

## Chunks (run and reported one at a time; one model load each)

**A — the decisive test (12 conditions × 12 seeds).** none; calm full@.08,
full@.04, full@.02, k1@m, k2s@m, k4s@m, k4s@.08, k2s@.08; rand1 full@.08,
k1@m, k4s@m.

**B — generality (13 × 12).** none; proud, reflective, " table" ×
{full@.08, full@.04, k4s@m, k1@m}.

**C — shape and position (10 × 12).** none; calm full@.12, k1_32@m,
k1_52@m, k2c@m, k4c@m, k4c@.08, k6s@.08; rand2 k1@m, k4s@m.

## Registered quantities and bars

Primary quantity: dLoop (the quantity the cooperative claim was made
on); dMargin co-reported for every arm.

- **V1 (primary, chunk A):** R1 = dLoop(calm k1@m) / dLoop(calm full@.08),
  R4 = dLoop(calm k4s@m) / dLoop(calm full@.08).
  **DOSE** if R4 ≥ 0.6 AND R1 ≥ 0.5. **COALITION** if R4 ≤ 0.35 AND
  R1 ≤ 0.25. Otherwise **GRADED** (reported with R2 = k2s@m).
  Seed-bootstrap 95% CIs (2000 resamples) reported beside the point
  estimates; the verdict uses the point estimates.
- **V2 (specificity, chunk A):** if a matched calm arm moves dLoop, is it
  calm or any big push? For each of k1@m and k4s@m: rand1's dLoop as a
  fraction of calm's at the same set, and calm − rand1 dMargin. A DOSE
  verdict whose rand1 arm reaches ≥ 50% of calm's dLoop at the same set
  is flagged **GENERIC** (concentrated push breaks the loop regardless
  of direction) — then the dose law is not the emotion's.
- **V3 (dose-alone equivalence, chunk A):** gap4 = |dLoop(k4s@.08) −
  dLoop(full@.04)| / |dLoop(full@.08)|, gap2 = same for k2s@.08 vs
  full@.02. H-D predicts both ≤ 0.25 (fixed-α fewer-layer arms carry
  about the same summed push as the half/quarter full-stack arms).
- **Descriptive exponent check:** the affect-14 fit (p ≈ 2.18) predicts
  full@.04 at ~22% and full@.02 at ~5% of full@.08. Reported, no bar.
- **Chunk B:** R1 and R4 per direction with V1's thresholds —
  3-direction case study, descriptive, no roster generalization.
- **Chunk C:** position (k1 matched at L32 / L44 / L52), contiguity (k4c
  vs k4s, matched and at .08), rand2 replicating rand1's matched arms.
  Final **dose-alone model**: fit log|dLoop| on log(Σα‖h‖) over calm's
  full-stack ladder (.02, .04, .08, .12) and predict every other calm arm
  from its summed absolute dose. H-D passes if every calm arm lies within
  ±0.25 (fraction of full@.08) of its prediction. Reported with the list
  of misses.

## Honesty

- No condition, quantity or threshold added after the first chunk's
  results; later chunks may be dropped, not redesigned.
- Big single-layer pushes (α ≈ 0.6 of ‖h‖ at one layer) are off the
  usual steering scale; the random arms exist to show what off-scale
  push does by itself.
- If H-D wins, GLOSSARY "Band-cooperative coupling" gets a dated
  correction the same day (the super-additivity was a dose convexity,
  shared by proud), per protocol (e).
- Resume-aware per seed per chunk; VRAM pre-flight ≥ 19.5 GB; one
  automatic non-137 retry; 137 = stop and report.

## Addendum 2026-09-29 — chunk D, frozen after chunks A–C, before D runs

Chunk C's registered dose-alone model FAILED on absolute dose Σα‖h‖:
at matched absolute push, one layer at L32 gave 283% of full-stack
dLoop, L44 146%, L52 31%. A **post-hoc** re-read found that the summed
**relative** strength Σα (paper units: fraction of the local residual
norm) orders all 15 calm arms: Spearman .979 vs dLoop fraction, .964 vs
dMargin (absolute Σα‖h‖: .868 / .821). This is exploratory. In chunks
A–C, Σα and layer position are confounded, because absolute matching
gives small-norm early layers a larger α. Chunk D separates them.

**D (10 × 12 seeds):** none; calm single layer at L28, L36, L44, L52,
L56, each at α = 0.64 (Σα matched to full@.08); calm full@.06,
full@.10 (threshold shape); rand1 k1_28@.64, rand2 k1_52@.64.

- **H-R (relative dose):** all five calm single-layer arms within
  ±0.35 of full@.08 (dLoop fraction in [0.65, 1.35]). PASS / FAIL.
- **H-P (position):** mean fraction of L28+L36 minus mean of L52+L56
  > 0.5. Reported alongside; the two can both fail, not both pass.
- Randoms: margin reported vs calm at the same layer; no bar.
- Threshold shape: dLoop fraction at Σα 0.16/0.32/0.48/0.64/0.80/0.96
  (full-stack ladder), descriptive.
