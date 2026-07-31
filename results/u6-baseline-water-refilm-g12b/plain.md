**The short version.** In its normal, unsteered state, Gemma 12B never
ranked any of the six tracked words in its top 8, at any layer or
position.

**What we did.** We did not push anything into the model. We read the
readout at every layer and word position across its answer, 76
positions and 47 layers. We asked Gemma 12B: "Describe the water cycle
in two sentences."

**What we found.** None of the six words reached the top 8 ranks
anywhere. The closest were "luckily", at rank 10 to 13, and "alot", at
rank 9 to 12, both at low-value spots. Other water-cycle words, such
as "precipitation" and "evaporation", reached the top of the readout
in the middle and late layers. None of them appeared in the output
text.

**What it means.** We think the six words are absent from Gemma 12B's
normal state for this question, not hidden behind other words. The
amplify tests in this unit add something new, not something already
close to the surface.

**What this does not show.** This method cannot show whether these
words exist in the model in a form the lens cannot read. The near
misses for "luckily" and "alot" sit at the edge and do not count as
evidence.
