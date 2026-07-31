**The short version.** Gemma 12B held one word, violin, at rank 1 in the
lens and named it correctly.

**What we did.** We gave Gemma 12B one word to hold, a violin, then
asked what it was holding. We tracked the rank of violin and five other
words, out of about 250,000 candidates. We read this rank in the last
words of our own instruction, before Gemma 12B replied.

**What we found.** Violin held rank 1 at that point. In Gemma 12B's
"READY" reply, violin fell to rank 8839 of about 250,000. No other tracked
word reached a rank close to the top eight. Gemma 12B then answered "A
violin," which was correct.

**What it means.** This is the first of six single-word baseline runs in
this unit. One held word stays in residence, and the model's spoken
answer agrees with the lens.

**What this does not show.** One word is the simplest case this unit
tests. It does not show how Gemma 12B handles a longer list.
