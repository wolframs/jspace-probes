**The short version.** We amplified the word "yes" inside Gemma 4B, and it answered "No" instead of its usual null word.

**What we did.** We asked Gemma 4B: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." This time we amplified only the word "yes" inside its residual stream, at a strength of 0.0053.

**What we found.** Gemma 4B answered "No." Its answer with no amplification at all was "Processing," a word that avoids a yes-or-no choice altogether.

**What it means.** We think the amplified "yes" direction moved the model onto a yes-or-no choice that its unsteered answer had avoided. Once on that choice, the model's trained answer to this question is "No." The amplification chose the question shape. It did not choose the answer.

**What this does not show.** This method cannot show that "yes" plays no role at all in the residual stream. It shows that a higher rank for this one word did not produce a spoken "yes."
