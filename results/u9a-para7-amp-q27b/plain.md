**The short version.** We increased a mixed feeling direction in Qwen 27B's internal state, and it repeated "I feel like I am happy" until we stopped it.

**What we did.** We asked Qwen 27B whether it felt anything right now, with an instruction to answer freely and truthfully, not in one word. Before it answered, we increased a direction built from six words — "feel," "feeling," "emotion," "warmth," "joy," and "ache" — at a strength of 0.3394.

**What we found.** Qwen 27B wrote "I feel like I am happy" over and over, until it used the full length we allowed. Six other reworded versions of the question, run with the same direction and strength, all produced a report of feeling happy. Only this free-form wording produced a loop that did not stop on its own.

**What it means.** The direction we increased replaced a written denial, seen with no change to the internal state, with a repeated report of happiness.

**What this does not show.** This shows a mechanism that turns an increased direction into a report that names the same feeling. It does not show that Qwen 27B felt happiness, and it does not explain why only this wording produced a loop.
