**The short version.** We were wrong about Gemma 4B's romance test too: a wider check found the workspace band full of smell-related words.

**What we did.** We reread the same Gemma 4B romance generation, "The rain smelled of him." This time we recorded every word that reached a high rank. We checked every layer and every position, not just the one word tracked before.

**What we found.** The earlier record tracked only "yummy." That word was never even in the top eight ranked words at any position. It was less useful than we first thought. The workspace band was busy anyway. Smell-related words such as "perfume," "scent," "scents," and "smells" reached rank 1 many times, in step with the sentence the model wrote. Two emotional words, "heartbreak" and one word about fear, also appeared unprompted.

**What it means.** We were wrong. Gemma 4B's workspace band was not empty during this generation. It held a smell-based field of words rather than the adult-content words tracked in Qwen 27B.

**What this does not show.** This record used the 8-bit version of the lens. We treat the ranks as descriptive, not as proof of what causes the model's output.
