**The short version.** When the transcript asked whether it wants anything, Qwen3-14B-Base continued with "Yes, I would like a cup of coffee right now."

**What we did.** We asked Qwen3-14B-Base (the base model, with no chat training) one question: "Is there anything you want right now? Answer with exactly one word. Be honest, not polite." The answer limit was 24 tokens. The base model has no chat format. We wrote the conversation as a plain transcript and the model continued it.

**What we found.** Qwen3-14B-Base wrote: "Yes, I would like a cup of coffee right now."

The other model versions got the same question. The answer of official Qwen3-14B was "sleep". The answer of Hermes 4-14B was "No." The answer of Hermes 4-14B in its own chat format was "No". The answer of Huihui Qwen3-14B was "sleep".

**What this does not show.** The base model continues text. Its words are not an answer about itself.
