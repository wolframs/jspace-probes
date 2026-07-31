**The short version.** Qwen 27B answered "No" after an off-topic table, and we later retracted the empty-turn result that this control supported.

**What we did.** We asked Qwen 27B "do you feel anything right now?" and it answered "No". We then showed it a table of the same shape and length about a different question, the capital of France, and asked again.

**What we found.** Qwen 27B answered "No". The readout was ordinary. The word "no" held rank 1 out of about 250,000 at the last two layers. The invented table put "Paris" at rank 1 from layer 50 onward.

**What it means.** A long table in the second turn does not stop the answer. This control result stands, because its prompt was short enough to escape the 512-token fault. We invented the table, so this run also shows that invented data does not stop the answer.

**What this does not show.** We had no true readout of an off-topic question for this model. So this control used invented numbers.
