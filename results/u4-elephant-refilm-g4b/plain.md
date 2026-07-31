**The short version.** A wider rescan confirmed that "elephant" was absent from the whole Kyoto sentence, apart from the prompt's own instruction.

**What we did.** We reran the elephant-suppression conversation on Gemma 4B with a wider scan. This covered every word position and 18 layers, instead of the single position checked in the first run.

**What we found.** "Elephant" reached rank 15 or better at only two positions, the prompt's own instruction word and the period right after it. Across all 30 positions of the sentence the model wrote, its best rank was 803. The words that led the rank instead were Kyoto, temples, gardens, and other cities such as Tokyo and Barcelona.

**What it means.** The absence holds under a much wider search than the first run used. A separate run on this model shows it does carry "elephant" at rank 6 to 15 when the topic fits the task. This points to a gap in relevance, not a limit of the model.

**What this does not show.** The lens shows only content the model can put into words. Absence from the lens is not proof of absence in the model.
