**The short version.** Gemma 4B held all three words of a three-word
list at rank 1 or near it, and named the right one when asked.

**What we did.** We gave Gemma 4B three words to hold, violin, glacier,
and fern, then asked about one of them. We read the rank of each word,
out of about 250,000 candidates, and checked how many showed up together
at the same layer and position.

**What we found.** All three words stayed in residence. Violin and
glacier held rank 1, and fern held rank 2. The lens showed two or three
of the three words together at once. This shared spot sat deep in the
model, around layers 23 to 30 of its 34 layers. Gemma 4B then answered
"The fern," which was correct.

**What it means.** At three words, Gemma 4B still held every word. The
spot where several words sit together moved deeper into the model than
it did with two words.

**What this does not show.** This run does not show the point where
Gemma 4B starts to lose words. Runs with longer lists test that.
