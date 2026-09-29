**The short version.** The loop break needs enough total push, not all layers at once (a correction to affect-14).

**What we did.** On Qwen 27B we put calm into one, two or four layers
with the same total push as all eight layers. We also tested proud,
reflective, the word "table" and random directions (12 seeds each).

**What we found.** One layer with the full push ended the loop as often
as all eight layers (11 of 12 seeds). Fewer layers at the usual strength
acted like all layers at a lower strength. The effect jumps: half the
push gave 11% of the effect. Push relative to each layer's size was the
best measure. The last layer (L56) was weaker. Our two strict planned
tests of this failed.

Random directions in one layer ended the loop in up to half the seeds.
Calm stayed 2 to 4 times stronger on the score gap. Calm stopped
cleanly, reflective often answered the original question, and "table"
and random directions started a new loop.

**What it means.** We were wrong. The affect-14 pattern came from a
steep threshold, not from layers that work together.

**What this does not show.** We do not know why directions leave the
loop in different ways.
