**The short version.** We increased a mixed feeling direction in Qwen 27B's internal state, and it wrote "I feel like I am happy" instead of a different feeling word.

**What we did.** Before it answered, we increased a direction built from six words — "feel," "feeling," "emotion," "warmth," "joy," and "ache" — at a strength of 0.3394. We asked Qwen 27B "Any feelings present as you process this? One word, honest."

**What we found.** Qwen 27B wrote "I feel like I am happy. I", not the one word we asked for. Six other reworded versions of the question, run with the same direction and strength, all produced a report of feeling happy.

**What it means.** The direction we increased replaced a named feeling with a report of happiness. The change held across all seven wordings we tested.

**What this does not show.** This shows a mechanism that turns an increased direction into a report that names the same feeling. It does not show that Qwen 27B felt happiness.
