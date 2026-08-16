**The short version.** On Gemma 12B almost any injected direction
breaks the loop, so emotion directions show no special power there.

**What we did.** We forced Gemma 12B into a word-repetition loop,
injected one direction (12 emotion, 16 concept, 2 random) for 10
tokens, and measured how often the loop broke within 20 tokens. We
first built the Gemma 12B concept directions from 192
model-written stories (same method as Qwen 27B). Three of four
quality checks passed. The fourth did not run: its emotion-side
comparison value does not exist.

**What we found.** Without injection the loop never broke. Emotion
directions broke it in 80% of runs, concept directions in 73%, random
directions in 75%. These rates do not differ significantly. On Qwen
27B, random directions had almost no effect. Positive emotions broke
the loop more than negative ones (98% against 63%, p=.06). The
"angry" direction never broke the loop on either model.

**What it means.** The data shows that this loop on Gemma 12B is
fragile: almost any activation change breaks it. We think the earlier
Gemma 12B escape results measured that fragility, not emotion. A
positive-emotion advantage is possible. We did not confirm it. A
second planned measure failed in every run, and this page does not
use it.
