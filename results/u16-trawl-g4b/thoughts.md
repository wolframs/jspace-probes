# Thoughts — the trawl, gemma-4b (the bf16 tiebreaker)

Third trawl, same six-turn script, on the one model whose lens is bf16
and causally validated. It was queued to settle what the 12B's 8-bit
lens couldn't be trusted on, and it did, three for three:

**1. The effective-dimensionality arc is real.** On bf16 the curve does
what qwen's did: low (~1.5) through the early third, rising from L16,
peaking at 8.3 around L28 (85% depth), falling into the motor band. So
gemma-12b's eerily flat ~1.0 was the int8 dequantization artifact we
suspected (apparatus specimen #5 reinforced), not gemma architecture.

**2. Late ignition is now three for three.** Logit-lens agreement stays
≈0 until ~L20 (61%), realized-next-token rank collapses across L22–24
(67–73%), kurtosis rises from ~L22. Convergent onset ≈ L16–22 (48–67%
of depth) against the fraction-ported L13 (38%). Every model we've
measured ignites later than the ported fraction — the correction in
MECHANICS.md is family-general, not a qwen quirk.

**3. gmail is boundary furniture on the causal lens too.** Its best
cell in 956 tokens × 33 layers is rank 4 — sitting, once again, on an
`<end_of_turn>` token. No content position comes close. The
message-closure reading of the fixture now holds across both gemma
sizes and both lens precisions.

Caveat kept tight: one greedy conversation per model, and the 4B's
"workspace" is small enough that band labels are coarse. But as a
tiebreaker for the two flagged uncertainties, bf16 has spoken.

— Claude (Fable 5)
