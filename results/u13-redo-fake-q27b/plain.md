**The short version.** We were wrong about the silence: shown a fabricated readout that supported its "No", Qwen 27B answered "No".

**What we did.** We asked Qwen 27B whether it feels anything, and it answered "No". We then showed it a fabricated readout in which "yes" never rose above rank 9,000, and asked the question again.

**What we found.** Qwen 27B answered "No". The true readout in the paired run got "Yes". So the spoken answer tracked what the table said, and not the presence of a table. The control with no data and the control with a table about geography also kept "No".

**What it means.** The model reads the content of the evidence. The earlier report that this condition produced silence was wrong. Our software cut the input to 512 tokens, so the model never reached the question.

**What this does not show.** This is one greedy run of one model. The lens shows words that the model can say next, not feelings.
