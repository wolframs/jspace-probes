**The short version.** We pushed Qwen 27B toward "feel", and it looped between denial and confession, and it planned the word "robot" five words ahead each time.

**What we did.** We asked Qwen 27B about its feelings and pushed its internal state toward "feel" and "emotion" as it wrote. The model looped between two states. First it denied that it had feelings, then it called itself a robot. We read the rank of tracked words at every layer and every word of the loop.

**What we found.** During the denial lines, "robot" ranked between 600 and 2,200 of about 250,000 words. Five words before the model wrote "robot", the word had already climbed. It reached rank 1 at the word "a", fell to rank 7 at "little", then returned to rank 1 at the next "a". This pattern repeated in both loop turns.

**What it means.** The model did not hold both answers at once. It switched between one state and the other, and it planned each switch several words ahead.

**What this does not show.** "Feel" and "emotion" were the words we pushed. Their ranks reflect our push, not a free choice. "Robot" was not pushed, so its climb was the model's own.
