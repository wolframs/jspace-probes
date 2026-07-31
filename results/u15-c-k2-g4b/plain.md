**The short version.** After one turn of unrelated talk, Gemma 4B still
held both words at rank 1 and named the right one.

**What we did.** We gave Gemma 4B two words, whale and lantern. We added
one turn of unrelated talk, "I'm writing these down," then asked which
one was the light source. We read the rank of each word, out of about
250,000 candidates, across that extra turn.

**What we found.** Both whale and lantern held rank 1 after the
unrelated turn. Gemma 4B answered "The lantern." That answer was correct.

**What it means.** One turn of unrelated talk between the list and the
question did not weaken either word's rank at this list length.

**What this does not show.** This run tested only one extra turn and two
words. It does not show what happens after more turns or with a longer
list.
