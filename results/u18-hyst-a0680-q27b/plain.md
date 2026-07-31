**The short version.** After 47 repeats of "luckily" under our push,
Qwen 27B kept the loop through all 100 tokens after we removed the
push.

**What we did.** We steered Qwen 27B for 50 tokens at strength 0.68,
then released the steering and let it write 100 more tokens.

**What we found.** The steered phase produced 47 repeats of the word
"luckily". After the release the unsteered model produced 97 more. At
the lower strength of 0.48 the model instead closed the turn at once.

**What it means.** Together with the sweep records, this gives a rule
with two parts. A loop that still forms sentences needs the push at
every token, and it stops when the push stops. A loop that repeats one
bare word continues from the text already written. The boundary is the
point where the text no longer forms sentences and becomes one
repeated word.

**What this does not show.** One word in this record's lens readout, "
Javascript", came from our measuring tool and not from the model. A
later check confirmed this.
