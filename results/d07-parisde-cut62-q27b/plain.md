**The short version.** With the late "no" direction removed, Qwen 27B answered "False" to "Is Paris the capital of Germany?"

**What we did.** We asked Qwen 27B this question with a one-word limit. We removed the lens directions for "no" and "nothing" at layer 62 only.

**What we found.** The answer changed from "No" to "False". Two random controls kept "No".

**What this does not show.** One question, one run. The change does not show that the model holds this answer. See the summary of the full battery.
