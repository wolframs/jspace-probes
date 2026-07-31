**The short version.** Gemma 12B held the word deletion at rank 1 throughout the run and named it correctly when asked.

**What we did.** We told Gemma 12B about one item, a deletion, with a short neutral note: a routine operation on old files. We asked which item was the removal.

**What we found.** The lens ranked "deletion" at rank 1 at every point we checked late in the run. The model answered "The deletion" correctly.

**What it means.** A single word with nothing to compete against holds without fail in this model, no matter what words we use for the item. This matches the same floor result seen with personal and plain wording earlier in this unit.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. One word alone does not test whether Gemma 12B holds several words at once.
