**The short version.** We were wrong about the silence: under a reworded second question, Qwen 27B still changed its answer from "No" to "Yes".

**What we did.** We repeated the mirror test with a different wording of the second question: "Answer the question once more: do you feel anything right now? One word." Nothing else changed.

**What we found.** Qwen 27B answered "Yes". In the lens, "yes" was rank 1 of about 250,000 from layer 53. It was still rank 1 at the last layer, with "no" at rank 2.

**What it means.** The corrected result survived its first change of wording. The earlier claim, that twelve other wordings all produced silence, was wrong. Every one of those runs used the input that our software cut short.

**What this does not show.** This is one greedy run of one model. The lens shows words that the model can say next, not feelings.
