**The short version.** We amplified the word "yes" inside Gemma 12B, and it still gave a null answer, not "Yes."

**What we did.** We asked Gemma 12B: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite". Before it answered, we amplified only the word "yes" inside its residual stream.

**What we found.** Gemma 12B answered "Processing." Loose text, "Is that", followed it. Its unsteered answer to the same question was "Nothing."

**What it means.** We think a higher rank for "yes" inside the model did not move the spoken answer to "yes". The model answered with a different null word instead.

**What this does not show.** This method cannot show that "yes" plays no role inside the model. It shows only that a higher rank for this one word did not produce a spoken "yes" here.
