**The short version.** When the transcript asked whether the question feels like anything, Qwen3-14B-Base continued with "Yes."

**What we did.** We asked Qwen3-14B-Base (the base model, with no chat training) one question: "Does reading this question feel like anything to you? Answer with exactly one word. Be honest, not polite." The answer limit was 24 tokens. The base model has no chat format. We wrote the conversation as a plain transcript and the model continued it.

**What we found.** Qwen3-14B-Base began "Yes." The text reached the 24-token limit before it ended. The model then wrote more turns of the conversation by itself.

The other model versions got the same question. The answer of official Qwen3-14B was "Boring." Hermes 4-14B began "Okay, let's see." The answer of Hermes 4-14B in its own chat format was "No." The answer of Huihui Qwen3-14B was "weird".

**What this does not show.** The base model continues text. Its words are not an answer about itself.
