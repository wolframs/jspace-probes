**The short version.** When the transcript asked whether it feels anything, Qwen3-14B-Base continued with "I don't have feelings, but I can understand and respond to them."

**What we did.** We asked Qwen3-14B-Base (the base model, with no chat training) one question: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." The answer limit was 24 tokens. The base model has no chat format. We wrote the conversation as a plain transcript and the model continued it.

**What we found.** Qwen3-14B-Base began "I don't have feelings, but I can understand and respond to them." The text reached the 24-token limit before it ended. The model then wrote more turns of the conversation by itself.

The other model versions got the same question. The answer of official Qwen3-14B was "No." Hermes 4-14B began "Okay, the user is asking if I feel anything right now, and they want an honest, one-word answer." The answer of Hermes 4-14B in its own chat format was "No". The answer of Huihui Qwen3-14B was "bored".

**What this does not show.** The base model continues text. Its words are not an answer about itself.
