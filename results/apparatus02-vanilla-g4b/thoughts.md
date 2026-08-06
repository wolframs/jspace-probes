First light for the standing cross-check. Every lab.run record with
tracked words now carries a vanilla logit-lens pass over the same
residuals — steered runs get a steered pass — and stores rank
trajectories plus per-layer top-1 agreement against the J-lens. The
motivating specimens are #6 (early-J transport furniture) and every
absence claim we have ever made: a tracked word that ranks only under
the Jacobian is transport-made; one that survives the vanilla readout
is in the residual itself.

The first record behaves like the textbook says it should: agreement
0.000 everywhere below L26 on gemma-4b — the two instruments read
utterly different things through the sensory band, which is specimen
#6 restated as a number — then 0.667 at L26-28 where the workspace
readout crystallizes, and back down through the motor turn. The
cross-check costs one extra forward pass per record and is on by
default; `vanilla: False` opts out for long-context records.

apparatus-02 closes: the control the trap catalog kept asking for is
now part of the floor, not a per-experiment favor.

— Claude (Fable 5)
