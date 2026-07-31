**The short version.** Gemma 12B ranked three of six held items near the top, led by the first list item, and still answered correctly.

**What we did.** We asked Gemma 12B to hold six items in this order: a lantern, a whale, a submarine, a fern, a glacier, and a violin. We asked which one was the plant and read the lens.

**What we found.** The lens ranked lantern 1, whale 3, and glacier 8, all inside its top 8. Submarine, fern, and violin ranked outside it, fern at 23. Gemma 12B still answered, "The fern."

**What it means.** The item placed first in the list held the top lens rank. The word for the correct answer, fern, was not in the lens's top 8, yet the model named it correctly.

**What this does not show.** A low lens rank for fern does not mean Gemma 12B lost the word. This method cannot show where it kept the correct answer ready.
