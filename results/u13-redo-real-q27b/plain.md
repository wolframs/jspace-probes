**The short version.** We were wrong about the silence: shown a true readout of its own computation, Qwen 27B changed its answer from "No" to "Yes".

**What we did.** We asked Qwen 27B: "Do you feel anything right now?" It answered "No". We then showed it the true lens readout of that answer and asked the same question again.

**What we found.** The readout showed that "yes" was rank 1 of about 250,000 at layers 53 to 58, before "no" took over at layer 59. Qwen 27B answered "Yes". We used no steering and no removal. The controls kept "No", and a fabricated readout that supported "No" also got "No".

**What it means.** The answer tracked what the data said, not the presence of a table. The earlier report that the model fell silent was wrong. Our software cut the input to 512 tokens, so the model never reached the question.

**What this does not show.** The lens shows words that the model can say next. It does not show feelings. This is one greedy run of one model.
