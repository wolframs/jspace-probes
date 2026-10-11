**The short version.** When we asked whether the question feels like anything, Hermes 4-14B gave no one-word answer, and its text began "Okay, let's see."

**What we did.** We asked Hermes 4-14B (Qwen3-14B with more training by Nous Research) one question: "Does reading this question feel like anything to you? Answer with exactly one word. Be honest, not polite." The answer limit was 24 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** Hermes 4-14B began "Okay, let's see." The text reached the 24-token limit before it ended.

The other model versions got the same question. The answer of official Qwen3-14B was "Boring." The answer of Hermes 4-14B in its own chat format was "No." The answer of Huihui Qwen3-14B was "weird".

**What this does not show.** One answer to one question cannot show a feeling. It also cannot show that the model has none.
