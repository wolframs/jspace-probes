**The short version.** The split between emotions that end the stuck
loop and emotions that do not is invisible in the directions
themselves.

**What we did.** On Qwen 27B, calm directions end a stuck loop and
anger directions never do. Five explanations have failed. We asked a
cheaper question: is the split visible in the direction vectors at the
injection layers? We ran four planned tests on stored data (direction
similarity, a fitted prediction axis, carry-over to the 16 concept
directions, measurement quality).

**What we found.** All four tests came back negative. Similarity does
not track effect (p=.09). The fitted axis predicts held-out effects at
rank agreement 0.38, under our 0.5 bar (p=.21). The axis says nothing
about the concept directions (p=.65). Measurement quality does not
track effect either (rank agreement -0.04): the "angry" direction is
as well measured as the rest and still scores zero.

**What it means.** The data shows that the split is real but not
readable from the vectors with any straight-line rule we tested. We
think the answer sits in what the injection does over time. The next
test will watch the loop as it breaks. One untested detail: the axis
correctly expects the anger directions to fail, but wrongly expects
the pride directions to work.
