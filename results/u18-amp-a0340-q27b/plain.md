**The short version.** At strength 0.34, below the earlier breaking
point, Qwen 27B already looped once we let it write 150 tokens.

**What we did.** We amplified six informal words inside Qwen 27B at
strength 0.34 and asked it to describe the water cycle in two
sentences. We let the model write 150 tokens, not the 60 of the earlier
test.

**What we found.** The model repeated "it's a pretty" three times and
circled the same idea for the rest of the answer. The earlier run at
this same strength, stopped at 60 tokens, had looked intact.

**What it means.** The breaking point we reported earlier was partly an
artifact of the short window. Capture takes time near the onset, so a
short run puts the threshold too high.

**What this does not show.** This is one greedy run at one strength. It
does not fix the exact onset.
