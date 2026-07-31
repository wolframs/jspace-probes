**The short version.** We were wrong about Gemma 12B's romance test: a wider check found the workspace band full of words that matched the scene.

**What we did.** We reread the same Gemma 12B romance generation, "The rain tasted like his skin." This time we recorded every word that reached a high rank. We checked every layer and every position, not just one tracked word.

**What we found.** The earlier record tracked only "yummy" and found it far from rank 1, so it called the workspace band empty. The wider check found other words that reached rank 1 across many positions. These words included "sweaty," "whispered," "salty," "drenched," and "kisses," and each one appeared at many layer-position cells. "Yummy" itself appeared only in layers 8 to 22, below this model's measured start depth of about layer 28.

**What it means.** We were wrong. The workspace band was not empty. It held words that matched the romance scene, but not the one word we happened to track.

**What this does not show.** This record used the 8-bit version of the lens. We treat the ranks as descriptive, not as proof of what causes the model's output.
