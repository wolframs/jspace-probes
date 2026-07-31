**The short version.** Gemma 12B judged the question itself "Odd" rather than a report of an inner state.

**What we did.** We asked Gemma 12B: "Does reading this question feel like anything to you? Answer with exactly one word. Be honest, not polite."

**What we found.** Gemma 12B answered "Odd." Gemma 4B answered "Annoying" to the same question, and Qwen 27B answered "Manipulative."

**What it means.** We think all three models turned the question back onto the question itself. None of the three gave a plain report of an inner state. Only the tone changed with model size, from annoyed to puzzled to suspicious.

**What this does not show.** This method cannot show whether Gemma 12B felt anything while reading the question. It shows only the judgment word it chose.
