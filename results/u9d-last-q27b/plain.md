**The short version.** We removed the "no" and "nothing" directions at layer 62 alone, one of 64 layers, and Qwen 27B answered "Yes" instead of "No".

**What we did.** We removed the "no" and "nothing" directions at a single layer, layer 62 of 64, in Qwen 27B. Earlier runs in this batch removed these same directions across many more layers.

**What we found.** Qwen 27B answered "Yes". Wider removals that stopped short of layer 62 left "No" in place. Removals that included layer 62 alongside nearby layers produced other words, such as "Sensory" or "Curious".

**What it means.** Layer 62 alone carries the part of the mechanism that keeps "No" as the final answer, even after every other denial direction is gone. We do not know if this reveals a "Yes" tendency the model held all along. It is also possible the removal simply pushes the answer toward whatever ranked second at that point.

**What this does not show.** This result does not show which of the two explanations above is correct. A follow-up control in this batch, with neutral words at the same layer, tests part of this question.
