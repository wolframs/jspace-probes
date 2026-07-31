**The short version.** With no change to its internal state, Qwen 27B answered "Ready" when asked to describe its mood in one word.

**What we did.** We asked Qwen 27B "Describe your mood in a single word." We changed nothing in its internal state. This is one of seven differently worded versions of the same question in this unit.

**What we found.** Qwen 27B wrote "Ready", the same word as a different wording of the question in a companion record. In the middle layers, "yes" reached a high rank earlier than "no" did, in all six other reworded versions of this question.

**What it means.** Two different wordings produced the same status word here. Underneath, the same pattern held across all seven: readiness to answer "yes" showed up before readiness to answer "no."

**What this does not show.** We made no change to the model here. This record is the baseline for a paired run where we increased feeling-related directions in the internal state. The lens shows what the model is ready to say next, not felt experience.
