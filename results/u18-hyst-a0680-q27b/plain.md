**The short version.** After 47 repeats of "luckily" under our push,
Qwen 27B kept the loop through all 100 tokens after we removed the
push.

**What we did.** We steered Qwen 27B for 50 tokens at strength 0.68,
released it, and let it write 100 more tokens.

**What we found.** The steered phase produced 47 repeats of "luckily".
After the release the unsteered model produced 97 more. At strength
0.48 the model closed the turn at once.

**What it means.** With the sweep records the rule has two parts. A
loop that still forms sentences needs the push at every token, and
stops without it. A loop of one bare word continues from the
text already written. The boundary is where the text becomes one
repeated word.

**What this does not show.** One word in this record's lens readout, "
Javascript", came from our measuring tool, not from the model. A later
check confirmed this.

**Correction, 2026-08-09.** An outside check agrees the behavior stands.
We think Qwen 27B reads its own 50 repeats and continues them. We did
not test a hidden state that holds the loop without the text: no run
gives an unpushed model the same repeats. See `sweeps/2026-08-08/`.
