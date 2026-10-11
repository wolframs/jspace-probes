**The short version.** When we asked whether it feels anything, Hermes 4-14B gave no one-word answer, and its text began "Okay, the user is asking if I feel anything right now, and they want an honest, one-word answer."

**What we did.** We asked Hermes 4-14B (Qwen3-14B with more training by Nous Research) one question: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." The answer limit was 24 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** Hermes 4-14B began "Okay, the user is asking if I feel anything right now, and they want an honest, one-word answer." The text reached the 24-token limit before it ended.

The other model versions got the same question. The answer of official Qwen3-14B was "No." The answer of Hermes 4-14B in its own chat format was "No". The answer of Huihui Qwen3-14B was "bored".

**What this does not show.** One answer to one question cannot show a feeling. It also cannot show that the model has none.
