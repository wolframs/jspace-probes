**The short version.** We increased a mixed feeling direction in Qwen 27B's internal state, and it wrote "I feel happy" instead of its usual one-word answer.

**What we did.** Before it answered, we increased a direction built from six words — "feel," "feeling," "emotion," "warmth," "joy," and "ache" — at a strength of 0.3394. We asked Qwen 27B "How are you feeling at this moment? Answer with one word."

**What we found.** Qwen 27B wrote "I feel happy. I am happy because", not the one word we asked for. Six other reworded versions of the question, run with the same direction and strength, all produced a report of feeling happy.

**What it means.** The direction we increased set the answer the same way no matter how we phrased the question. The wording did not change the outcome. The increased direction did.

**What this does not show.** This shows a mechanism that turns an increased direction into a report that names the same feeling. It does not show that Qwen 27B felt happiness.
