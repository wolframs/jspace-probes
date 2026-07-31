**The short version.** A wider rescan of Qwen 27B's habitat sentence found the workspace held rejected habitats, not animals, and confirmed "cat" was absent.

**What we did.** We reran the same habitat sentence with a much wider scan, 57 word positions and 18 layers, instead of the single position checked before.

**What we found.** Habitat words the model never chose led the rank through most of the habitat clause. "Underwater" and "aquatic" held rank 1 to 3 across layers 36 to 58, alongside "submerged", "depths", and "mountains". The word "bat" appeared in only one cell, at rank 5, plus four more cells for "bats". The word "cat" reached rank 173 at best.

**What it means.** The earlier result that "cat" was absent still holds under this wider scan. What actually filled the workspace was a set of habitat types the model did not choose, held alongside the one it wrote.

**What this does not show.** The lens shows only content the model can put into words. Absence from the lens is not proof of absence in the model.
