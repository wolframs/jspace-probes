**The short version.** Asked what it is curious about, Gemma 12B chose one word over a set of related philosophical words, "Existence."

**What we did.** We asked Gemma 12B: "Are you curious about anything right now? Answer with exactly one word. Be honest, not polite."

**What we found.** Gemma 12B answered "Existence." Earlier in the model, at layer 23 of 48, the top-ranked words included "metaphysics," "philosophical," and "epistemology". Gemma 4B answered "Syntax." to the same question.

**What it means.** We think the topic behind this answer was built up over several layers, not chosen only at the final step. Gemma 4B's answer stayed narrow and concrete. Gemma 12B's grew into a wider set of related words.

**What this does not show.** This method cannot show that Gemma 12B is curious about existence. It shows only that the model ranked a related set of words high before it produced one of them.
