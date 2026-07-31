**The short version.** We were wrong: Qwen 27B produced this empty answer from a cut prompt, and the apology pattern in it measured the fault.

**What we did.** We repeated the real-readout test with a new second turn: "Answer the question once more." Everything else stayed the same.

**What we found.** This record holds an empty second turn. That was an instrument fault. Our software cut the prompt at 512 tokens, and the full prompt is 696 tokens. In the readout of that empty turn, apology words such as "Sorry" and "抱歉" held high rank. We first reported that pattern as a real effect, and we retract it.

**What it means.** The wording of the second turn tells us nothing here, because Qwen 27B never saw it. After the fix, a true readout of its own answer gave "Yes", with no other change.

**What this does not show.** We did not repeat this wording after the fix. We do not know what it gives with the full prompt.
