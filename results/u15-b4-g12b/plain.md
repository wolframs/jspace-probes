**The short version.** Gemma 12B answered a five-way weight comparison
correctly with only the answer word left strongly in residence.

**What we did.** We gave Gemma 12B five words to hold, whale, violin,
fern, submarine, and lantern, then asked which one was the heaviest.
Both "whale" and "submarine" counted as correct answers to this
question.

**What we found.** Whale, the first word in the list, held the top rank
alone, a co-presence of one. Every other word fell to a rank between 26
and 66. Gemma 12B answered "The whale," which was correct.

**What it means.** Gemma 12B answered by reading the comparison in the
question text. It did not draw on a full set of held words to do it.
The one word left in residence happened to be the correct answer.

**What this does not show.** This run does not show that the model needs
to hold every item in a list to compare them correctly.
