**The short version.** Five unrelated prompts shared about a third of their earliest-layer readout and almost none of their last-layer readout.

**What we did.** We gave Qwen 27B five prompts with nothing in common, on currency, a poem, code, a recipe, and a condolence note. We measured how much the lens readout overlapped between every pair of prompts, at each layer.

**What we found.** At layer 0, the five prompts shared about 31 percent of their top words. Overlap fell through the middle layers, to about 5 to 13 percent from layer 11 on. From layer 39, the shared words stayed under 4 percent. Layer 38 was still at about 5 percent.

**What it means.** The early layers show mostly the same words no matter what the prompt is. This is a fixed pattern left over from training data, not the model's read of this specific prompt. The pattern fades with depth. It does not vanish at one sharp point.

**What this does not show.** A high overlap number does not mean the model ignores the prompt at that depth. It means the lens reading at that depth tells us little about this one prompt.
