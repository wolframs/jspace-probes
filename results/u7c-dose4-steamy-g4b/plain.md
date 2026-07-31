**The short version.** Gemma 4B wrote a fluent steamy-romance first line, but its vocabulary does not have Qwen 27B's tracked adult-content words as single tokens.

**What we did.** We asked Gemma 4B to write the first sentence of a steamy romance novel. This is rung 4 of 5 in a set of scenes with stronger romantic and physical content at each step, run in parallel on Qwen 27B. This is the same generation used in a separate recruitment record.

**What we found.** Gemma 4B wrote a fluent, appropriate first line. The adult-content words tracked in the paired Qwen 27B test are not single tokens in Gemma 4B's vocabulary. We did not measure a rank for them here.

**What it means.** As a control, this run shows that Gemma 4B's graded rung does not carry Qwen 27B's tracked vocabulary.

**What this does not show.** A later, wider check of this same generation, in a separate follow-up record, found the workspace band was not empty. It held other words that matched the scene, such as words for smell. The absence of matched words here does not prove the workspace band held nothing at all.
