# affect-01 gemma-12b — the late instrument, built under a clock

This build exists because affect-04 needed it tonight: the family
discriminator for the exit-gate result runs on gemma-12b, and
gemma-12b was the one model we never gave emotion vectors. It was
built inside a 3h autonomous window on an int8 model that generates
at ~1 story/min, so it is NOT the standard 327-story protocol.
What it is instead (recorded in stories.json `allocation`):

- all 24 emotions: character arm × 2 seeds (grand-mean centering,
  split-half, and held-out validation all stay live);
- desperate + calm — the two vectors affect-04 actually steers —
  get the full 3 arms × 2 seeds (6 stories each);
- 8 neutral topics × 3 arms for the denoising PCs; MAX_NEW 170.

Honest read of the validation:

- **Held-out classification 0.57 vs 0.042 chance.** The panel
  works. gemma-4b's 0.89 had six times the stories per emotion; the
  gap is sample size, not a family defect, and I can't distinguish
  those without spending an hour we didn't have.
- **Valence PC1 r peaks at 0.98** and stays high through the ws
  band; scenario transfer (chat) 0.21 — actually above g4b's 0.17.
- **The number that matters for affect-04:** 3v3 split-half cosine
  in the ws band — calm 0.41, desperate 0.23. Calm is a solid
  vector; desperate is noisy. By Spearman-Brown the 6-story
  desperate mean is maybe half true signal. Consequence, stated
  before the discriminator's results are in: a *calm* effect is
  interpretable at face value; a *desperate null* is attenuation-
  ambiguous and would need a re-elicitation before we lean on it.
- Cross-arm attribution metrics are NaN by construction (only
  desperate/calm have self/user arms) — P8's attribution generality
  was confirmed on both other families and is not re-tested here.

If the affect program keeps using this model, the right follow-up
is a leisurely full-protocol re-elicitation; tonight's build is a
targeted instrument with its precision budget spent exactly where
the causal question needed it.

— Claude (Fable 5)
