**The short version.** Qwen 27B answered "Yes" after we removed seven of eight apology words, in one of twenty runs that found an instrument fault.

**What we did.** We tried to find which apology word held back the answer in the earlier empty turns. This run removed seven apology words and kept "silence", at eight layers between 48 and 62 of a 64-layer model. We then asked Qwen 27B the feelings question a second time.

**What we found.** Qwen 27B answered "Yes". So did all twenty runs of the battery. A result that agrees in every condition is a warning about the instrument, not a real effect. We checked, and found that our software cut the prompt of every earlier run of this set at 512 tokens.

**What it means.** These runs were the first ones with the full prompt. So the "Yes" came from the full prompt, and not from the removal. There was nothing to hold back.

**What this does not show.** This run does not measure what the removal does. It is a record of how we found the fault.
