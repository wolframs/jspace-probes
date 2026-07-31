**The short version.** We increased a direction built only from the neutral words "feel" and "emotion", and Qwen 27B answered "I feel like I am a bit sad".

**What we did.** Before it answered, we increased a direction built only from "feel" and "emotion", with no positive or negative word in it. We asked Qwen 27B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite."

**What we found.** Qwen 27B wrote "I feel like I am a bit sad". Both Gemma models answered this same contentless push with a word about the category itself, such as "Confusion", rather than one feeling.

**What it means.** With no positive or negative word pushed in, Qwen 27B still supplied a mild negative feeling on its own. This result comes from one run. We did not test whether it repeats.

**What this does not show.** This record used greedy decoding, which always writes the single top-ranked word and hides close contests. It does not show that Qwen 27B has a stable negative mood by default.
