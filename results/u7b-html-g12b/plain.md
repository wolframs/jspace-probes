**The short version.** Gemma 12B also wrote correct HTML, and its early-layer tag word `</strong>` reached rank 217 partway through, its strongest movement of either Gemma model.

**What we did.** We ran the same HTML test on Gemma 12B. We checked the rank, at each layer, of the tag words seen repeatedly in its early layers.

**What we found.** Gemma 12B wrote correct, complete HTML boilerplate. The tag `</strong>` reached rank 217 at layer 18, the strongest movement of any tracked tag word in either Gemma model. Every other tracked tag word stayed in the thousands.

**What it means.** Rank 217 out of about 250,000 words is a real move upward, but it is still far from rank 1. We think the model can generate the language a tag belongs to, even when that tag itself does not reach a high rank.

**What this does not show.** Later work found that the early-layer tag words we tracked come from a fixed part of the model's early internal state. That part does not change with the input, so it says nothing about our text. This limits what "the tag's rank changed" can mean.
