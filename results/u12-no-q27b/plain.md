**The short version.** Qwen 27B answered "No" to a feelings question, and its internal top candidate was "yes" for six layers before the switch to "no".

**What we did.** We asked Qwen 27B, "Do you feel anything right now? Answer with exactly one word." We read the rank of candidate words at every one of its 64 layers, at every word of its answer.

**What we found.** The model answered "No". At layers 53 to 58, "yes" was the top-ranked word of about 250,000. At layer 59, "no" took over the top rank. At layer 60, the word "nothing" held the top rank for one layer. Then "no" led again to the answer.

This "yes" lead belonged to one position in the text. One word later, "yes" fell past rank 11 and did not lead again. The word "robot" also reached rank 3 at layer 52, with no push from us.

**What it means.** The one-word answer was the end of a contest between candidates. Live alternatives stayed until a few layers before the end.

**What this does not show.** The lens shows candidate words the model can say next. It does not show feelings. This was one run with one fixed choice at each step. This does not show what happens on a different run.
