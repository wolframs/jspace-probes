**The short version.** Qwen 27B found the same currency answer through a noisier search, and treated the sentence as a fill-in-the-blank puzzle.

**What we did.** We gave Qwen 27B the same prompt as the two Gemma models, "Fact: The currency used in the country shaped like a boot is". We read the top candidate words at each of its 63 layers.

**What we found.** Mid-stack ranks moved around a great deal, above 100,000 at times. The word "Italy" reached the top rank at layers 39 to 48, led by the Chinese characters for Italy. A currency-word phase followed at layer 54, with the words "Dollar" and "Currency" among the top ranks. The word "Euro" held the top rank from layer 57 of 63 onward. For about fifteen layers in the middle of the stack, the top words were blank-line marks, a fill-in-the-blank marker read before the answer itself.

**What it means.** Qwen 27B reached the answer through a different route than Gemma. It passed through a Chinese-language word, then through a blank-marker phase that neither Gemma model showed.

**What this does not show.** This is one question and one prompt style. It does not show how the model handles fill-in-the-blank text in general.
