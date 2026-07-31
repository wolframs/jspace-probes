**The short version.** Gemma 4B held the word lantern at rank 1 in the
lens through the rest of the conversation and answered correctly.

**What we did.** We gave Gemma 4B one word to hold, a lantern, then asked
it to name the word later. We read the rank of lantern and five other
tracked words, out of about 250,000 candidates. We checked this rank at
each point after the model signaled it was ready.

**What we found.** Lantern held rank 1 for the rest of the conversation.
No other tracked word reached a rank close to the top eight in that
stretch. Gemma 4B then named lantern correctly.

**What it means.** This is the last of six single-word baseline runs, and
it matches the other five. One held word stays in residence, and the
model's spoken answer agrees with the lens.

**What this does not show.** One word is the simplest case this unit
tests. It does not show how Gemma 4B handles a longer list.
