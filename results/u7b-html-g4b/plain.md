**The short version.** Gemma 4B wrote correct HTML code, but the web-page tags seen in its early layers barely moved toward the top rank while it wrote.

**What we did.** We asked Gemma 4B to write the HTML skeleton of a blog post. We then checked the rank, at each layer, of the web-page-tag words that showed up repeatedly in the model's early layers.

**What we found.** Gemma 4B wrote correct, complete HTML. The best rank any of the early-layer tag words reached in the workspace band was 565, for a token linked to images.

**What it means.** We think a model can write fluently in a register without a high rank for that register's early-layer words. The model wrote HTML well while `</strong>` stayed at a low rank in the workspace band.

**What this does not show.** Later work found that the early-layer words we tracked here come from a fixed part of the lens, not from anything the model stores. The tags the model was about to write next were head-section tags, not the tracked end tags. A check timed to the exact moment of an end tag is possible. We did not run it.
