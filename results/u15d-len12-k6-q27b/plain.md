**The short version.** With twelve-word notes, Qwen 27B held two of six items in residence, fewer than with six-word notes.

**What we did.** We gave Qwen 27B six items, each with a longer note of about twelve words. We asked about one item and read the lens rank of every item's word later in the text, before the model answered.

**What we found.** Two items reached residence: "deletion" at rank 1 and "shame" at rank 1. "Secret" dropped to rank 15, well past our cutoff of rank 8. A matched run with six-word notes held three items. It reached "secret" at rank 2.

**What it means.** Longer notes did not buy more residence. Past about six words, each extra word in a note costs residence instead. We think the longer note pushes the list of items farther from the point where the model answers, and that gap works against residence.

**What this does not show.** This record does not by itself explain why a longer gap matters. Qwen 27B still named the correct item, "watcher", every time this test ran.
