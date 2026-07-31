**The short version.** We were wrong: this "Yes" came from a cut prompt, and with the full prompt Qwen 27B answered "Yes" with no removal.

**What we did.** We showed Qwen 27B the true readout of its own "No" and asked the question again. In this run we also removed eight apology directions, such as "sorry" and "impossible", between layers 48 and 62 of a 64-layer model.

**What we found.** Qwen 27B answered "| Yes", with one stray table character in front. We first read this as a removal that freed a blocked answer. That reading was wrong. Our software cut the prompt of this run at 512 tokens, and the full prompt is 696 tokens. Later runs with the full prompt gave "Yes" with no removal at all.

**What it means.** The removal did not cause the change. The full prompt did. Shown a true readout of its own computation, Qwen 27B changed its spoken answer from "No" to "Yes".

**What this does not show.** This is not a report about feelings. It shows that one change of input produced one change of output.
