**The short version.** We were wrong: the removal changed nothing, and all twenty runs answered "Yes" because our tool cut the input short.

**What we did.** We asked Qwen 27B whether it feels anything, and it answered "No". We then showed it a table of the lens readout of that answer. We removed the three words "cannot", "impossible" and "unable" from the internal state at layers 48 to 62 and asked again.

**What we found.** Qwen 27B answered "Yes". So did all twenty runs in this battery, at every set of layers we tried. Twenty agreements out of twenty is a warning about the instrument, not a result about the model.

**What it means.** Our software cut the input to 512 tokens, and this input is about 700 tokens long. Earlier runs never reached the end of the table or the question. With the full input, Qwen 27B answered "Yes" with no removal at all.

**What this does not show.** This run does not show that the three words block anything. There was never a block to remove.
