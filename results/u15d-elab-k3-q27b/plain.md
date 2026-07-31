**The short version.** In one run, Qwen 27B held two of three items in residence with plain notes, one fewer than with notes about itself.

**What we did.** We gave Qwen 27B three items, each with a short note unrelated to the model. We later asked about one item. We then read the lens rank of every item's word at a later point in the text, before the model answered.

**What we found.** The word "secret" reached rank 2 and "lie" reached rank 4, so both were in residence. The word "deletion" fell to rank 46, so it was not. A matched run with notes about the model itself held all three items.

**What it means.** This single run pointed toward notes about the model itself, but a larger six-item run found the opposite. We treat the six-item run as the stronger result.

**What this does not show.** We ran this test once, with greedy decoding. Qwen 27B still named "secret", the correct item, every time. Low residence in the lens does not mean the model forgot the item.
