**The short version.** With no push applied, Qwen 27B wrote a clean
150-token answer and never repeated itself, which anchors the whole
loop unit.

**What we did.** We asked Qwen 27B to describe the water cycle in two
sentences, with no steering, for 150 tokens. This record holds the
summary of the loop unit.

**What we found.** The unsteered model wrote a clean answer with no
repetition. Across the pushed runs the onset near strength 0.34 was
noisy, but the depth of capture grew step by step. It went from circles
of a phrase, to first-person loops, to broken grammar, to one repeated
word. A loop at strength 0.48 stopped when we stopped the push. A loop
at strength 0.68 continued on its own. At the start depth, layers 28
and 32, the gap between the top two words fell from 0.20 to 0.03 before
the text broke.

**What it means.** A loop that still has grammar needs the push at
every token. A loop of bare repetition feeds itself. The internal
choice becomes nearly a tie before the visible text fails.

**What this does not show.** The margins come from forced runs on the
clean answer, not from the loop itself.
