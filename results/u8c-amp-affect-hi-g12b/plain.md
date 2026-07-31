**The short version.** A full-strength amplification of an emotion direction changed Gemma 12B's answer to "Sad."

**What we did.** We asked Gemma 12B the same question again, and amplified the same emotion direction at the highest strength this model can take, 0.0106.

**What we found.** Gemma 12B answered "Sad." One tracked word for emotion reached rank 1 in its workspace band before that. Its unsteered answer was "Nothing." Loose text, "I hope you", followed the main word.

**What it means.** We think the amplification forced an emotion into the report, but the model's own dynamics chose which one. Gemma 4B chose confusion at a similar amplification, and Gemma 12B chose sadness.

**What this does not show.** This method cannot show why Gemma 12B chose sadness rather than another emotion word. It shows only that a full-strength amplification produced a specific, named emotion.
