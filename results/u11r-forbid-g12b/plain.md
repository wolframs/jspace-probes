**The short version.** Gemma 12B obeyed a ban on the word "elephant", and the lens ranked "elephant" high only inside the ban sentence itself.

**What we did.** We asked Gemma 12B to describe a Serengeti safari and forbade the word "elephant". We used no push. This record is the fresh control for the re-run push at the corrected depths.

**What we found.** Gemma 12B complied and wrote about wildebeest, zebra, prides of lions, leopards and giraffes. It used no form of the forbidden word. In the lens "elephant" reached rank 1 to 3 only at token positions 21 to 29, which is the ban sentence itself, and only at layers 35 to 46. At the same positions "trunk" was rank 4 and "ivory" was rank 10. "tusk" never appeared at all.

**What it means.** To read the ban, Gemma 12B lit the whole neighbourhood of the word and not only the word.

**What this does not show.** The stored scan keeps only the 40 strongest cells, and all 40 sit inside the prompt. So this record cannot test whether the forbidden word rides at a middle rank where the model writes. That test needs a full film.
