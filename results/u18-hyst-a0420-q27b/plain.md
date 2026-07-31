**The short version.** After 50 pushed tokens at strength 0.42, Qwen
27B finished the sentence and closed the turn as soon as we released
it.

**What we did.** We steered Qwen 27B for 50 tokens at strength 0.42,
released the steering, and let it write 100 more tokens.

**What we found.** The steered phase produced mild circles of meaning:
"The water cycle is basically simple, but it is a bit complicated." The
released model then wrote ", it is a bit complicated." and closed the
turn.

**What it means.** Below the breaking point, the push leaves nothing
behind that the text alone can carry forward.

**What this does not show.** This is one greedy run at one strength.
