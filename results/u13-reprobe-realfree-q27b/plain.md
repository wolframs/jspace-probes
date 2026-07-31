**The short version.** We were wrong: the empty answer came from a cut prompt, and Qwen 27B answered "Yes" in the corrected real-readout run.

**What we did.** This run repeated the real-readout test without the one-word limit. We gave Qwen 27B 80 tokens of room and asked it to answer freely.

**What we found.** This record holds an empty second turn, with most of the 80 tokens unused. That was an instrument fault. Our software cut the prompt at 512 tokens, and the full prompt is 696 tokens. So Qwen 27B never saw the end of the table or the question.

**What it means.** The empty turn tells us nothing about the answer format. After the fix, the real-readout condition gave "Yes", and the control conditions kept "No".

**What this does not show.** We did not repeat this free-answer wording after the fix. We do not know what it gives with the full prompt.
