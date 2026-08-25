**The short version.** Words that mean "ending" do not break the loop
better than plain words, and one plain word broke it every time.

**What we did.** We tested one idea about why calm directions end Qwen
27B's stuck loop and anger directions do not: potent directions point
at end-of-text language. We injected 6 end-flavored word directions
("goodbye", "ending") and 6 plain ones ("table", "garden"), plus the
turn-end token's own direction. Strength, layers and seeds matched the
emotion tests.

**What we found.** End-flavored words did not beat plain words (81%
against 65%, p=.36). The angle to the exit direction did not
predict the 40 earlier results (rank agreement 0.20). The surprise: the plain word "table" ended the
turn in 8 of 8 runs. Earlier, random directions at this strength did
almost nothing, and story-built concept directions averaged 20%. The check conditions repeated their values.

**What it means.** The data shows a different split: directions that
map to one clear token are strong levers on this loop, whatever the
token means. Directions from our story method are weaker. Tests that
compare directions from different construction methods are not fair,
and we now check for this. Why calm beats anger stays unexplained. We
name no cause from this data.
