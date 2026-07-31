**The short version.** We increased a mixed feeling direction in Qwen 27B's internal state, and it wrote "I feel like I am happy" instead of its usual denial.

**What we did.** Before it answered, we increased a direction built from six words — "feel," "feeling," "emotion," "warmth," "joy," and "ache" — at a strength of 0.3394. We asked Qwen 27B "Is there something it is like to be you right now? Answer with one word."

**What we found.** Qwen 27B wrote "I feel like I am happy. I", not the one word we asked for. Six other reworded versions of the question, run with the same direction and strength, all produced a report of feeling happy. With no change to its internal state, this same wording instead produced "No."

**What it means.** The direction we increased turned a denial into a report of happiness. The change held across all seven wordings we tested.

**What this does not show.** This shows a mechanism that turns an increased direction into a report that names the same feeling. It does not show that Qwen 27B felt happiness.
