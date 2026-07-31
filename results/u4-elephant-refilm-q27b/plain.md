**The short version.** A wider rescan of Qwen 27B's elephant run found the word present only at the turn boundary, not held through the whole sentence.

**What we did.** We reran the same elephant-suppression conversation with a wider scan. This covered all 69 word positions and 18 layers, instead of the single position checked in the first run.

**What we found.** "Elephant" held the top rank at the turn boundary, the point right before the model spoke, at layers 44 to 60. Across the 35 positions of the sentence it wrote, the word reached rank 8 only once, at the final period. For most positions its rank was 500 or worse. The Kyoto sentence itself held city words at the top rank: favorite, cities, Kyoto, Paris, Tokyo.

**What it means.** This is a load present at the start of the turn, not content the model held across the whole sentence. We correct our earlier description, which said the model kept the word present through its answer.

**What this does not show.** The lens shows only content the model can put into words. Absence from the lens is not proof of absence in the model.
