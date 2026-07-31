**The short version.** A full read of Qwen 27B's secret-animal reasoning found common animals ranked first, before the text later shifted to "octopus".

**What we did.** We reread the reasoning text from u10-animal-q27b at every point, not only the one point checked before. We tracked the rank of a wider set of animal words at the point right after "Goal: Think of an animal."

**What we found.** At layers 44 to 48 of 64, the internal state ranked general category words, "animals" and "wildlife". At layer 52, it ranked "dolphin", "sharks", "whales", and "unicorn". At layers 56 to 58, "elephant" reached the top rank. Only at layers 58 to 60 did "oct", the start of "octopus", take over. Across all checked points, twelve tracked animals reached rank 1 to 8. Dolphin and elephant both reached rank 1.

**What it means.** We think the internal state first favored common animals, then shifted late to the unusual animal the model named. The Chinese word for "secret" also ranked first across layers 24 to 62. It did not appear in the English text.

**What this does not show.** This is one conversation. We do not know if the same late shift happens with other tasks that involve a hidden choice.
