**The short version.** The score-gap result is now the confirmed main
claim, and the demolition of the loop needs all eight layers at once.

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
the loss from any one missed layer is 19% to 37%. The layers only
work together. For "table", single layers each give about 10%. For
proud, nothing works at any layer. Proud's effect repeats to the exact
number in every seed, because the loop state repeats.

**What it means.** We measured that potent directions break the loop
through the whole layer band at once. The plain
word works partly layer by layer. We do not know why some meanings
carry this joint effect.
