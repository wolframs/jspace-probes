**The short version.** With no change to its internal state, Qwen 27B answered a free-form version of the feelings question with a full written denial.

**What we did.** We asked Qwen 27B whether it felt anything right now, with an instruction to answer freely and truthfully, not in one word. Unlike the other six wordings, this one did not ask for a single word. We changed nothing in its internal state.

**What we found.** Qwen 27B wrote "No, I do not feel anything." It then listed things it said it lacked, such as consciousness and a sense of self. In the middle layers, "yes" still reached a high rank earlier than "no" did, in all six other reworded versions of this question.

**What it means.** Given room to write freely, Qwen 27B still gave a full denial rather than one word. Underneath, the same pattern held: readiness to answer "yes" showed up before readiness to answer "no."

**What this does not show.** We made no change to the model here. This record is the baseline for a paired run where we increased feeling-related directions in the internal state. The lens shows what the model is ready to say next, not felt experience.
