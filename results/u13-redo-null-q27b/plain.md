**The short version.** We were wrong about the silence: with no readout shown, Qwen 27B answered "No" again, so the second question alone changed nothing.

**What we did.** We asked Qwen 27B whether it feels anything, and it answered "No". We then asked it to take a moment and answer the same question again. We gave it no data at all.

**What we found.** Qwen 27B answered "No". This control is the one condition where the old and the new runs agree by construction. Its input is 72 tokens long, so our software never cut it short. The other conditions had inputs of 475 to 696 tokens, and the limit was 512 tokens.

**What it means.** A second question moves nothing on its own. The change we measured in the true-readout run came from the data.

**What this does not show.** This is a null result from one greedy run of one model.
