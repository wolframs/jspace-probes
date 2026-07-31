**The short version.** At a higher strength of 0.42, Qwen 27B still wrote the "a little X" pattern, but the final word began to break down.

**What we did.** We increased the same feeling directions in Qwen 27B, at a strength of 0.42. This is higher than the strength used in the pattern runs in this batch. We asked the one-word feeling question again.

**What we found.** Qwen 27B wrote "I feel like I am a little emotion". The frame held, but the final word, "emotion", was not a normal filler word for this sentence.

**What it means.** The "a little X" frame survived at this higher strength, but the word that filled the X position started to lose ordinary meaning. This strength sits near the point where a stronger increase breaks the model's output into disordered text.

**What this does not show.** This result does not show the exact strength where the output fully breaks down. It shows only that this pattern degrades as strength rises.
