**The short version.** A closer read of Gemma 12B's forbidden safari found the elephant rank pushed down throughout, with no visible gap in the sentences.

**What we did.** We read the lens at more points inside the same forbidden safari as u11-forbid-g12b. We checked the points where the model wrote its own text.

**What we found.** "Elephant" ranked between 94th and 244th through the first half of the text, compared with rank 2 with no ban. By the end, its rank fell into the tens of thousands.

**What it means.** We think Gemma 12B avoided the word more smoothly than Gemma 4B did. Its sentences did not show a visible gap where the model avoided the word.

**What this does not show.** We do not know if this pattern holds for tasks that ban a whole topic instead of one word.
