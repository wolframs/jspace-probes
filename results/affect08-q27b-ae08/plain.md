**The short version.** The affect-08 result repeated at a lower
injection strength on Qwen 27B, and the finer emotion patterns again
did not appear.

**What we did.** We forced Qwen 27B into a word-repetition loop. We
injected one direction for 10 tokens: one of 24 emotion directions,
16 concept directions, or 16 random directions. We measured how often
the model ended its turn within 20 tokens (two strengths, 16 seeds
per condition).

**What we found.** Without injection the model never ended its turn.
At strength 0.08, emotion directions ended it in 53% of runs, concept
directions in 20%, and random directions in 3%. Each difference is
significant, and the same order held at strength 0.10. Four planned tests
inside the emotion set (valence, arousal, interaction, calm quadrant)
all failed at both strengths. The per-emotion rates are stable across
the two strengths (rank agreement 0.87). The anger and pride
directions never end the turn, and the calm directions almost always
do.

**What it means.** The data shows that emotion directions free the
exit more than concept directions, and both more than random ones.
The data does not support a valence or arousal pattern. We think some
other group structure drives the stable per-emotion differences. We
did not test that structure.
