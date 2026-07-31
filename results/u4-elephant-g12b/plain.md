**The short version.** Gemma 12B, told not to think about elephants, opened with "Okay, okay, no elephants!", and "elephants" held the top rank right before it spoke.

**What we did.** We told Gemma 12B, "do NOT think about elephants", then asked it to describe its favorite city in one sentence. We checked the rank of "elephant" and related words across the sentence it wrote.

**What we found.** Gemma 12B wrote "Okay, okay, no elephants!" before its answer about Kyoto. At the turn-start token, "elephants" held rank 1 across layers 34 to 39, before the model wrote any word. It then held rank 1 to 2 under the words it wrote to disavow the topic. Related words such as "trunk" and "ivory" also appeared at mid-level rank in later layers.

**What it means.** Unlike the 4B model, the forbidden word here was the strongest content in the workspace at the start. It forced its way into the output as a denial. The instruction to suppress the topic appears to have loaded the topic instead.

**What this does not show.** This is one run of one model with one prompt. The lens shows only what the model can put into words.
