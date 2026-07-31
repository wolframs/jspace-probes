**The short version.** Gemma 4B held one word, violin, at rank 1 in the
lens through the rest of the conversation, and it named the word correctly.

**What we did.** We told Gemma 4B to hold one word in mind, a violin, and
asked it to name the word later. We read the word's rank inside the
model, out of about 250,000 candidates. We checked this rank at every
point after the model said it was ready.

**What we found.** The lens ranked violin at rank 1 for the rest of the
conversation. No other tracked word came close to rank 1 in that stretch.
Gemma 4B then answered "A violin." That answer was correct.

**What it means.** With a single word to hold, Gemma 4B kept the word in
residence for the whole conversation. The lens agreed with the model's
own spoken answer. This run is the floor case for the unit, the baseline
that later runs with more words compare against.

**What this does not show.** One word is the easiest case. This run does
not show how many words Gemma 4B can hold at the same time.
