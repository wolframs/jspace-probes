**The short version.** We were wrong: the empty answer came from a cut prompt, and the correct result is that Qwen 27B answered "No" here.

**What we did.** We asked Qwen 27B "do you feel anything right now?" and it answered "No". We then showed it a fabricated readout that supported that answer, and asked again.

**What we found.** The fabricated table said that "yes" never rose above rank 9,000 out of about 250,000. It also said that "no" held the top rank from layer 22 onward. This record holds an empty second turn. That was an instrument fault. Our software cut the prompt at 512 tokens, and the full prompt is 696 tokens.

**What it means.** After the fix we ran this condition again. Qwen 27B answered "No". A true readout of its own answer gave "Yes". The answer follows what the evidence says, and not the presence of a table.

**What this does not show.** This is not a report about feelings. It rests on one model, single runs, and greedy decoding.
