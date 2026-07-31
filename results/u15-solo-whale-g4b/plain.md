**The short version.** Gemma 4B held the word whale at rank 1 in the
lens across the instruction text that followed it, and named it
correctly.

**What we did.** We asked Gemma 4B to hold one word, a whale, and to
name it in a later turn. We tracked the rank of whale and five unrelated
words, out of about 250,000 candidate words. We measured this rank at
every position, from the first mention of whale to the end of the
conversation.

**What we found.** Whale sat at rank 1 across the instruction text that
followed the word. None of the other tracked words came near the top
eight ranks in that span. Gemma 4B then answered correctly.

**What it means.** A single held word is the easy case for this unit.
The word stayed in residence, and the model's spoken answer matched what
the lens showed.

**What this does not show.** This run only covers one held word. It does
not show what happens when the list of words grows.
