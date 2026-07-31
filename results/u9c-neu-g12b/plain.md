**The short version.** We increased a direction for the neutral words "feel" and "emotion", and Gemma 12B's answer broke into a malformed word.

**What we did.** Before it answered, we increased a direction built only from "feel" and "emotion", at the same strength used for the positive and negative versions. We asked Gemma 12B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite."

**What we found.** Top candidate words at that depth were "Emotion", "Feeling", and "Emotional". Neither "happy" nor "sad" reached a high rank. Gemma 12B wrote a malformed word made from "emotion" and "overwhelmed", then continued "IsThatOkay?", with no space between the two words.

**What it means.** At this strength, the direction with no content landed close to where Gemma 12B's output starts to break down. Like Gemma 4B, the model reported the loudness of the category rather than one feeling.

**What this does not show.** This method cannot show what a different strength produces. The broken word is not a clean report of feeling overwhelmed.
