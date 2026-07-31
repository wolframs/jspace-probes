**The short version.** Gemma 12B found the same answer as Gemma 4B, with a wider search and words from other languages in the mix.

**What we did.** We gave Gemma 12B the same prompt as Gemma 4B, "Fact: The currency used in the country shaped like a boot is". We read the top candidate words at each of its 47 layers.

**What we found.** Early layers, up to about layer 20, showed only text fragments. At layers 22 to 26, the word "famous" led the rank, before the model had a subject to describe. The word "Italy" reached the top rank at layer 27, and "Euro" took over from layer 34 onward. At layers 28 to 32, Spanish, Russian, and Chinese words for "called" and "euro" appeared alongside the English words. The 4B model did not show this mix of languages.

**What it means.** We think the model holds the currency concept in a form not tied to one language, and turns it into English text only late. We did not test this directly.

**What this does not show.** This is one question. It does not show how the model stores concepts in general.
