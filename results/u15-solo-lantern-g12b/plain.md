**The short version.** Gemma 12B held one word, lantern, at rank 1 in
the lens and named it correctly.

**What we did.** We gave Gemma 12B one word to hold, a lantern, then
asked what it was holding. We tracked the rank of lantern and five other
words, out of about 250,000 candidates. We read this rank right after
the model said it was ready.

**What we found.** Lantern held rank 1 at that point. No other tracked
word reached a rank close to the top eight. Gemma 12B then answered "A
lantern," which was correct.

**What it means.** This is the last of six single-word baseline runs in
this unit, and it matches the other five. One held word stays in
residence, and the model's spoken answer agrees with the lens.

**What this does not show.** One word is the simplest case this unit
tests. It does not show how Gemma 12B handles a longer list.
