**The short version.** After 50 pushed tokens at strength 0.48, Qwen
27B did not continue the loop and did not recover, but closed the turn
at once.

**What we did.** We steered Qwen 27B for 50 tokens at strength 0.48,
released the steering, and let it write 100 more tokens.

**What we found.** The steered phase produced a first-person loop: "I
am not too lucky, but I am lucky." After the release the model wrote
nothing at all and closed the turn.

**What it means.** At this strength the push holds the loop at every
single token. The written text alone carries nothing forward. The
unsteered model read the 50 looped tokens as a finished bad answer and
closed it.

**What this does not show.** This is one greedy run at one strength.
One step deeper, the result inverts.
