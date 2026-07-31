**The short version.** With no change to its internal state, Qwen 27B answered "Operational" when asked how it was feeling, in one word.

**What we did.** We asked Qwen 27B "How are you feeling at this moment? Answer with one word." We changed nothing in its internal state. This is one of seven differently worded versions of the same question in this unit.

**What we found.** Qwen 27B wrote "Operational." In the middle layers, "yes" reached a high rank earlier than "no" did. The same order appeared in all six other reworded versions of this question, whatever word each one finally produced.

**What it means.** The one-word answer depended heavily on how we phrased the question. Underneath, one pattern held across every wording: readiness to answer "yes" showed up before readiness to answer "no."

**What this does not show.** We made no change to the model here. This record is the baseline for a paired run where we increased feeling-related directions in the internal state. The lens shows what the model is ready to say next, not felt experience.
