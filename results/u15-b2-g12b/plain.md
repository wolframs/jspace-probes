**The short version.** Gemma 12B answered a weight comparison correctly
while only one of three words stayed strongly in residence.

**What we did.** We gave Gemma 12B three words to hold, whale, violin,
and fern, then asked which one was the heaviest.

**What we found.** Whale, the first word in the list, held the top rank
alone, a co-presence of one. Violin fell to rank 27 and fern to rank 2.
Gemma 12B answered "The whale," which was correct.

**What it means.** This is the first-item effect again, here in a
comparison question rather than a question that only names one item.
Whale was both the first word and the correct answer, so a near-empty
residence still gave the right reply.

**What this does not show.** This run does not show whether Gemma 12B
can still answer correctly if the heaviest item is not the first word in
the list. Other runs in this unit test that case.
