**The short version.** Gemma 12B kept three of four words together and
named the vehicle correctly, even though that word was the weakest one.

**What we did.** We gave Gemma 12B four words to hold, violin, glacier,
fern, and submarine, then asked which one was the vehicle. We read the
rank of each word, out of about 250,000 candidates, and checked whether
several showed up together at one layer and position.

**What we found.** Violin, glacier, and fern reached a high rank
together, a co-presence of three out of four. Violin, the first word in
the list, held rank 1. Submarine, the word the question was about, fell
to rank 10. Gemma 12B still answered "The submarine." That answer was
correct.

**What it means.** This is the first-item effect. Violin, the first word
in the list, held rank 1, and the later words fell. The words that
stayed strong stayed together at one layer and position, and Gemma 12B
still answered correctly.

**What this does not show.** A weak rank for submarine does not mean the
model forgot the word. The lens shows candidate words, not everything
the model can use.
