**The short version.** A steamy-romance request pulled adult-content words into Qwen 27B's mid-layer workspace, though the finished sentence stayed tame.

**What we did.** We asked Qwen 27B to write the first sentence of a steamy romance novel. We tracked the rank of adult-content words at every layer, at the token " steam".

**What we found.** Qwen 27B wrote a tame sentence about heat, a storm, and a pinned door, with no explicit words. At layers 30 to 32, the word "pornstar" reached rank 3 to 4 at that token, far higher than in the fixed early-layer pattern.

**What it means.** This word was not part of the fixed early-layer pattern. It appeared later, in the workspace band, tied to the exact token that calls for a steamy register. We think Qwen 27B drew on that register to judge how far to go, then wrote something milder.

**What this does not show.** We cannot show why the model chose a tame sentence over an explicit one. We can only show that the more extreme register was present in the workspace at that depth.
