**The short version.** After 47 bare repeats of "luckily", Qwen 27B
kept the loop alive for the whole free phase with the push removed.

**What we did.** We steered Qwen 27B for 50 tokens at strength 0.68,
then released the steering and let it write 100 more tokens.

**What we found.** The steered phase produced 47 repeats of the word
"luckily". After the release the unsteered model produced 97 more. At
the lower strength of 0.48 the model instead closed the turn at once.

**What it means.** This gives a law with two parts. A loop that still
has grammar needs the push at every token, and it stops when the push
stops. A loop of bare repetition sustains itself from the text already
written. The boundary is the point where the loop loses its last
grammar.

**What this does not show.** One word in the readout here, "
Javascript", came from our measuring tool and not from the model. A
later check confirmed this.
