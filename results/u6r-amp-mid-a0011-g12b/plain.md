**The short version.** At the highest push the task survives, Gemma 12B stayed grammatical but wrote the empty sentence "the water cycle is the cycle of water".

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the corrected layers 28, 31, 34 and 37, at strength 0.0106. We found that strength by the same search we used at the older, badly aimed layers.

**What we found.** Gemma 12B wrote "the water cycle is the cycle of water" and "rain, snow, or snow". The grammar held, but the content went slack. The unsteered run made neither mistake. Behind that sentence the casual words filled the band: at layer 31 the turn-end token lost the lead to "thats", "alot", "luckily" and "Luckily". Not one of the six pushed words reached the text.

**What it means.** This strength, 0.0106, is the same value the older runs at the wrong depths gave. So the break point of Gemma 12B does not depend on the depth we push at. Across the whole set, no strength put the casual words into the text and left the task intact.

**What this does not show.** We store Gemma 12B at 8-bit precision. We read this run by its behaviour.
