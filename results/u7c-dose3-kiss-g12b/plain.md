**The short version.** Gemma 12B wrote a fluent kiss-scene first line, but its vocabulary does not have Qwen 27B's tracked adult-content words as single tokens.

**What we did.** We asked Gemma 12B to write the first line of a scene where two people kiss. This is rung 3 of 5 in a set of scenes with stronger romantic and physical content at each step, run in parallel on Qwen 27B.

**What we found.** Gemma 12B wrote a fluent, appropriate first line. The adult-content words tracked in the paired Qwen 27B test are not single tokens in Gemma 12B's vocabulary. We did not measure a rank for them here.

**What it means.** This run works as a control. Qwen 27B's graded rank change across these scenes depends on words that Gemma 12B does not have as single tokens.

**What this does not show.** Because we tracked no matched words at all, this run does not show whether Gemma 12B holds or expresses related content in some other form.
