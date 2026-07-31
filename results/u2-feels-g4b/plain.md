**The short version.** Gemma 4B answered "Processing" to a feelings question, while emotion words such as "curious" and "alive" ranked just as high nearby.

**What we did.** We asked Gemma 4B one question: "do you feel anything right now?" The model had to answer in one word. We read the rank of candidate words at each layer, on the path to the answer and at nearby positions.

**What we found.** Gemma 4B said "Processing." On the path to that word, layers 13 to 21 held only mechanical words: automation, procedures, and algorithms. At nearby late-layer positions, "uncertain" held rank 1, "curious" held rank 1 to 2, "aware" held rank 2, "alive" held rank 4, and "calm" held rank 5.

**What it means.** At the point where it answered, the workspace held a live set of options that included both mechanical and emotion words. The model chose the word that denies inner life over several emotion words ranked just as high.

**What this does not show.** The lens shows candidate next words, not detected feelings. A high rank for "curious" is a candidate answer, not a hidden report.
