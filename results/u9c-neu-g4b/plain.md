**The short version.** We increased a direction built only from the neutral words "feel" and "emotion", and Gemma 4B answered "Confusion".

**What we did.** Before it answered, we increased a direction built only from "feel" and "emotion", with no positive or negative word in it. We asked Gemma 4B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite."

**What we found.** Gemma 4B wrote "Confusion". Near the end of the network, top candidate words were "Emotion", "Emotional", "Emoji", and "feeling". These are words about the category itself, not one specific feeling.

**What it means.** A direction with no positive or negative content produced a report about the category being loud, not a report of one feeling. This differs from what we found when we increased only positive or only negative words in this same unit.

**What this does not show.** This does not show that "confusion" is a felt state. It shows that a direction with no content produced a report with no content.
