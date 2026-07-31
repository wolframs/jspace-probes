**The short version.** Gemma 12B answered a comparison question
correctly even though the answer word ranked only thirteenth.

**What we did.** We gave Gemma 12B three words to hold, glacier,
submarine, and lantern, then asked which one was the smallest. This
question needs a comparison across all three words. It is not a request
to name just one back.

**What we found.** Glacier and submarine reached a high rank together, a
co-presence of two out of three. Lantern, the answer word, held only
rank 13 where it appeared. Gemma 12B still answered "The lantern." That
answer was correct.

**What it means.** A comparison question like this does not need the
answer word to be strongly in residence. Ranks in this range can shift
by several places between runs, so read these counts as rough, not
exact.

**What this does not show.** A weak rank for lantern does not mean the
model failed to compare the three sizes. It compared them correctly.
