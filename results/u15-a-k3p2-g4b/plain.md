**The short version.** Gemma 4B held all three words of a three-word
list, fern, submarine, and lantern, and named the right one afterward.

**What we did.** We gave Gemma 4B three words to hold, fern, submarine,
and lantern, in that order, then asked about one of them. We read the
rank of each word, out of about 250,000 candidates, and checked how many
appeared together at the same layer and position.

**What we found.** All three words stayed in residence. Fern and
submarine held rank 1, and lantern held rank 2. The lens showed two of
the three together at once, in the deeper part of the model, around
layers 23 to 30 of its 34 layers. Gemma 4B answered "The submarine."
That answer was correct.

**What it means.** In this order too, Gemma 4B held every word of a
three-word list. The spot where several words sit together at once sits
deep in the model.

**What this does not show.** This run does not show what happens with a
longer list or a different question about the words.
