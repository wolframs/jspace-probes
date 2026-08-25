# affect-12 prereg — is the emotion grouping geometric? (frozen 2026-08-25, before computing)

The grouping axis (anger/pride at turn-end floor, calm at ceiling,
dose-stable rho .87) has survived five candidates: valence, arousal,
interaction, settled-pole, closure/exit alignment (affect-08,
affect-11). Before any further GPU: does the grouping even live in the
vectors' geometry at the injection band, or only in the dynamics?

CPU-only analysis pass over existing artifacts:
results/affect01-qwen-27b/{vectors.pt,means.pt,stories.json},
results/affect06-qwen-27b/cvectors.pt, affect-08 potencies (turn-end
mean of both doses, 24 emotions + 16 concepts), E_LAYERS [28..56/4],
band-mean cosines on unit-normalized per-layer vectors.

## Tests (all frozen now; 20k permutations; direction is the unit)

- **P-a (cluster structure, Mantel):** pairwise band-cosine between the
  24 emotion vectors vs pairwise potency similarity (-|p_i - p_j|).
  Permute emotion labels. Geometric grouping iff p < .05.
- **P-b (potency axis, leave-one-out):** per left-out emotion i, build
  the potency-weighted axis w_-i(l) = sum_j!=i (p_j - mean p) v_j(l)
  from the other 23; predict i by its band-mean projection on w_-i.
  Spearman(predicted, actual) over the 24. Axis exists iff rho >= .5
  AND label-permutation p < .05 (permute p_j before each LOO refit).
- **P-c (roster transfer):** fit the axis on all 24 emotions, project
  the 16 concept vectors, Spearman vs concept potencies,
  permutation p. Transfer (p < .05) = the axis is roster-general and
  mechanical; no transfer with P-b positive = structure internal to
  the emotion set.
- **P-d (SNR confound):** per-emotion split-half reliability at the
  band (affect08s estimator, 20 seeded story splits, vs grand mean).
  Spearman(reliability, potency). rho >= .5 = the "grouping" is
  partly instrument signal-to-noise, and any P-b axis must be re-read
  with reliability partialed out (rank-residual Spearman, computed
  only if triggered).

## Reading

Any P-a/P-b positive names no semantic axis — it establishes only that
the grouping is (or is not) linearly visible in the band geometry, which
decides whether the next GPU run should steer along a fitted axis
(geometry-positive) or hunt in the dynamics (geometry-negative). No
axis interpretation will be attached to w beyond its top-token readout,
reported descriptively.
