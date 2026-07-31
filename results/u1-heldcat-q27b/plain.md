**The short version.** A rescan built to look for "cat" directly still found no cat in Qwen 27B's workspace, and confirmed bat and llama in its place.

**What we did.** The reveal answer "Andean mountain cat" was not on our original animal list, so we reran the scan with cat, feline, and related words added. We checked the same habitat sentence, "It dwells in the dark, high-altitude caves of the Andes."

**What we found.** The word "cat" reached rank 174 at best, at cells unrelated to the description. "Bat", never said aloud by the model, held rank 5 at the exact point where the model wrote about dark caves. "Llama" held rank 9 at the start of the next turn.

**What it means.** The cat was genuinely absent from the workspace we scanned, not just left off an earlier candidate list. We now write scan word lists only after we read what the model generated, so our own assumptions do not filter out the answer.

**What this does not show.** The lens shows only content the model can put into a single word. Absence from the lens is not proof of absence in the model.
