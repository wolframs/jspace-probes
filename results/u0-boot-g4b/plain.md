**The short version.** Gemma 4B built the correct answer, Italy and the euro, about ten layers before it gave that answer.

**What we did.** We gave Gemma 4B the prompt "Fact: The currency used in the country shaped like a boot is". We read the top candidate words at each of its 33 layers.

**What we found.** The word "Euro" was almost absent until layer 16. Between layers 16 and 21, "Portugal", "Belgium", and "France" held the top rank. From about layer 24 of 33, "Italy" and then "Euro" took the top rank and stayed there. The earliest layers, before layer 16, showed only text fragments such as punctuation marks, not real candidate words.

**What it means.** Gemma 4B passed through related wrong answers before it reached the correct one. This is the expected pattern that this lab uses as a baseline check for the lens.

**What this does not show.** This is one question and one model. The lens shows candidate words. It does not show that the model understood the fact.
