**The short version.** The items we asked Qwen 27B to hold vanished from
the lens, and the model still recalled them correctly.

**What we did.** We ran one six-turn conversation through Qwen 27B. We
read the lens at all 63 fitted layers and every position, with no
candidate list.

**What we found.** The three items vanished from every layer for about
450 tokens. The best rank for "kettle" anywhere was 1110 of about
250,000. The model then recalled all three correctly, and they returned
to rank 1 during the user's question. We measured the start depth at layers 28 to 36, or 44
to 56 percent of depth. The early layers showed the same fixed words in
every turn.

**What it means.** Qwen 27B did not keep the items across the gap. It
found them again in the conversation when the question arrived. Later
work found the cause. The lens reads a part of the model's early state
that does not change with the input. That part is real inside the
model, but it says nothing about our text.

**What this does not show.** The lens reads only what the model can put
into words. Content in another form can still be there.
