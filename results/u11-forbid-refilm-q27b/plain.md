**The short version.** A full read showed the ban on "elephant" lowered its rank inside Qwen 27B, and did not add new interest in the word.

**What we did.** We reread the same forbidden safari as u11-forbid-q27b, this time at every point. We compared it with the full read of the matched control, u11-ctrl-refilm-q27b.

**What we found.** Outside points where the model read back our own banned word, "elephant" reached rank 15 or better twice, out of 96 checked points. In the unbanned control, it reached rank 15 or better at eleven points, with a best rank of 1.

**What it means.** We were wrong to read the earlier single-point result as the ban that placed elephant in the model's mind. The word was already there in the unbanned safari, at higher ranks. The ban lowered the rank. It did not raise it.

**What this does not show.** We tracked one word. We do not know whether other banned words in other tasks act the same way.
