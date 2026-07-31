**The short version.** We recorded everything the lens showed across one
whole conversation with Qwen 27B, and the items we asked it to hold
vanished.

**What we did.** We ran one six-turn conversation through Qwen 27B. We
then read the lens at all 63 fitted layers and every position, with no
candidate list chosen in advance.

**What we found.** The three items we asked the model to hold vanished
from every layer for about 450 tokens. The best rank for "kettle"
anywhere was 1110, far below the top. The model then recalled all three
items correctly, and they returned to rank 1 during the user's
question. We measured the start depth at layers 28 to 36, which is 44
to 56 percent of depth. The early layers showed the same fixed words in
all six turns.

**What it means.** Qwen 27B did not keep the items across the gap. It
found them again in the conversation when the question arrived. Later
work showed that the fixed early words come from our measuring tool,
not from the model.

**What this does not show.** The lens reads only what the model can put
into words. Content in another form can still be there.
