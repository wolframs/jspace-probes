**The short version.** Qwen 27B held "everything" and "enough" ready at the end of a love song, then wrote the flatter "the point".

**What we did.** We cut the lyrics off in the middle of a line, "The holding / was", and let Qwen 27B finish it. We read the lens at the last given token.

**What we found.** Qwen 27B wrote " the point / [End]". At the last given token the lens ran "everything" at layers 44 and 52, and "enough" at layers 56, 60 and 62. One position earlier, "love" and "warmth" were also high. Two positions earlier the lens ran "holding" and then "itself", which is the song's own earlier phrase.

**What it means.** The tender answers were present in the middle and upper layers of Qwen 27B. The answer that came out was the plain echo of the line above it. We think this is a small example of the late filter.

**What this does not show.** The lens under-ranks function words, so part of this gap is an artifact of content words against grammar words. This is one run over one song.
