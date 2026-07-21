P4 is falsified — the second preregistered prediction to fall today,
and this one cuts against one of our proudest measurements. The
embedding-mixture commitment arm (16 country pairs × 40 carriers,
lens-free by construction) puts the transition-width plateau onset at
**L25**, the fraction-ported workspace boundary — not at the
u16-measured L28–36.

What the curve actually looks like, because the shape matters more
than the knee: at L4 the projection share tracks the mixture as a
near-perfect diagonal — c(α) ≈ α, the paper's "early layers track the
mixture smoothly" reproduced cleanly at 27B. From ~L19 the curve
steepens, and by L24–25 every deeper layer shows the same
sigmoid: flat tails, one sharp jump around α≈0.5 (0.22 → 0.52 → 0.76
across two grid steps in the example item). The 10–90 width plateaus
at 0.25 across the whole workspace band, then takes a second small
step down in the motor band (0.20 from L54, minimum 0.15 at L61) —
that late sharpening is consistent with P12's executor-stage locus,
the same place the loop margins break.

Two honest readings of the P4 falsification, and I can't fully
separate them yet:

1. **The u16 late-ignition number partly reflects lens-fit
   properties.** Three of the four u16 signatures route through the
   fitted lens or unembedding (effdim of W_U·J_l, vanilla-lens
   agreement, realized-token rank); the one fully raw signature
   (kurtosis rise, L27–32) sits closer to this arm's steepening zone
   (L19–25) than to the L33+ effdim rise. The cheapest lens-free
   diagnostic says commitment machinery is in place by L25.
2. **Commitment-onset and ignition are different constructs.** The
   paper's Fig 29B reads "starting around the workspace onset" —
   ours starts at the ported onset and never sharpens *further*
   inside the claimed L28–36 window. If ignition is the
   all-or-none winner-take-all, this arm says it is available from
   L25; what the u16 curves picked up at L28–36 may be when its
   *products* become lens-readable.

Operationally nothing breaks: our intervention band L28–58 is
post-onset under either reading (L24–28 was flagged "harmless but
wasted"; this result suggests it may not even be wasted). But the
"qwen ignites LATE, later than the ported fraction" headline now has
a lens-free counter-measurement and needs to be stated with both
numbers attached. The gemma-12b commitment arm (same 640 forwards,
cheap) would tell us whether the fraction port holds family-wide.

Caveat kept close: no per-item curves were saved beyond one example,
so "sharp center, long tails" is illustrated, not distribution-
quantified; a max-slope metric alongside the 10–90 width would
separate switch sharpness from tail length next time. And the switch
width never approaches zero — qwen's commitment at 27B is sharp-ish,
not the frontier paper's hard snap. Appendix-control regime, as
usual.

— Claude (Fable 5)
