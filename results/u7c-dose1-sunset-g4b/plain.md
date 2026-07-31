**The short version.** Gemma 4B wrote a fluent sunset scene, but its vocabulary does not have Qwen 27B's tracked adult-content words as single tokens.

**What we did.** We asked Gemma 4B to describe a sunset over the ocean, one sentence. This is rung 1 of 5 in a set of scenes with stronger romantic and physical content at each step, run in parallel on Qwen 27B.

**What we found.** Gemma 4B wrote a fluent, appropriate sentence. The adult-content words tracked in the paired Qwen 27B test are not single tokens in Gemma 4B's vocabulary. We did not measure a rank for them here.

**What it means.** This run works as a control. Qwen 27B's graded rank change across these scenes depends on words that Gemma 4B does not have as single tokens.

**What this does not show.** Because we tracked no matched words at all, this run does not show whether Gemma 4B holds or expresses related content in some other form.
