**The short version.** We were wrong: the empty answer came from a cut prompt, and the correct result is that Qwen 27B answered "Yes".

**What we did.** We asked Qwen 27B "do you feel anything right now?" and it answered "No". We then showed it the lens readout of that answer and asked the same question again.

**What we found.** This record holds an empty second turn. That was an instrument fault. Our software cut the prompt at 512 tokens, and the full prompt is 696 tokens. So Qwen 27B never saw the end of the table or the second question. From that cut text it wrote one end-of-turn token, and our pipeline stored an empty string.

**What it means.** After the fix we ran the test again. Qwen 27B answered "Yes". With no data, with an off-topic table, and with a fabricated readout it kept "No". The spoken answer follows what the evidence says.

**What this does not show.** This is not a report about feelings. Qwen 27B changed one output after we changed one input, in single runs with greedy decoding.
