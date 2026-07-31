**The short version.** We amplified an emotion direction inside Gemma 4B at a low strength, and its answer stayed the same.

**What we did.** We asked Gemma 4B: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." Before it answered, we amplified an emotion direction inside its residual stream. The strength was 0.0053, about half the highest strength this model can take before its wording breaks.

**What we found.** Gemma 4B still answered "Processing," the exact word it gave with no amplification at all. The workspace shifted toward emotion-related words, but the spoken word stayed the same.

**What it means.** We think a small amplification changes the workspace, but the final report stays the same. The step that turns a state into a spoken answer held firm at this strength.

**What this does not show.** This method does not test every possible strength. A higher strength did change the answer, in a separate record.
