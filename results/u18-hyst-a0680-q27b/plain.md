**The short version.** After 47 pushed repeats of "luckily", Qwen 27B
kept the loop through all 100 tokens on its own.

**What we did.** We steered Qwen 27B for 50 tokens at strength 0.68,
then released it.

**What we found.** The steered phase produced 47 repeats of "luckily",
and after release the model produced 97 more unaided. At strength
0.48 the model closed the turn at once.

**What it means.** The rule has two parts. A
loop that still forms sentences stops when the push stops. A loop of
one bare word continues from the text already written. The boundary is where the text becomes one
repeated word.

**What this does not show.** One word in this record's lens readout ("
Javascript") came from our measuring tool, not from the model.

**Correction, 2026-08-09.** An outside check agrees the behavior stands.
We think Qwen 27B reads its own 50 repeats and continues them. We did
not test a hidden state that holds the loop without the text: no run
gives an unpushed model the same repeats. See `sweeps/2026-08-08/`.

**Update, 2026-08-17.** The missing run exists now
(`results/oneoffs04-release-q27b`). An unpushed model given the same
repeats kept the loop, 8 of 8 seeds, scrambled or not.
