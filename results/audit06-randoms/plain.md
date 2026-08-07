**The short version.** We added the missing random-direction controls
to four old results: three passed, and one confirmed an earlier
correction.

**What we did.** We re-ran 19 steered records on Qwen 27B with random
directions in place of the target directions, at the same strength and
layers. The text generation is deterministic, so any change comes from
the directions.

**What we found.** The apology-removal flip appeared under random
removal too, in 2 of 2 seeds. An earlier check showed the flip comes
from the prompt and appears with no removal at all. The deep "No"-removal result passed: the target removal moved
the answer to "Curious" and both random removals left "No" in place.
The emotion-amplification ladder passed: each random control answered
"No" while the target runs produced feeling-speech. The repetition-loop
ladder passed: random controls wrote normal text at every strength up
to 0.68.

**What it means.** The apology-removal correction stands: the flip
appears with no removal, with target removal, and with random
removal. The other three results kept their causal claims.

**What this does not show.** The old records store no disturbance-size
measurement, so the size match rests on the audit-02 measurements, not
on per-record numbers.
