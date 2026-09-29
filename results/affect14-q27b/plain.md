**The short version.** The score-gap result held, but we were wrong that the loop break needs all eight layers at once (see affect-15).

**What we did.** Two tests on Qwen 27B with new random seeds. First,
we repeated the loop test (31 conditions, 12 seeds) with the score
gap as the planned main measure. Second, we injected three directions
(calm, proud, the plain word "table") at one layer at a time, and
with one layer left out.

**What we found.** The gap between the two scores predicts each
direction's success rate (rank agreement 0.78, planned bar 0.5). The
five emotions that never end the loop move the gap no more than
random directions do.

For calm, no single layer gives more than 1% of the full effect, but
the loss from any one missed layer is 19% to 37%. For "table", single
layers each give about 10%. For proud, no single layer works. Proud's
effect repeats to the exact number in every seed, because the loop
state repeats.

**What it means.** We were wrong to read this as layers that work
together. Affect-15 (2026-09-29) showed that one layer with the same
total push ends the loop as well. The pattern comes from a steep
threshold in total push.
