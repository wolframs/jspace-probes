**The short version.** A wider search inside Qwen 27B found the very words about feelings it denied, held at a high rank throughout its own answer.

**What we did.** We reran the record where Qwen 27B denied any sensation while tokens passed through it. This time we searched every position and every layer for words about feelings, not just the few words we tracked before.

**What we found.** The words "sensations," "sensory," "consciousness," and "experience" ranked near the top through most of the model. The word "feelings" also ranked near the top in many places, even though Qwen 27B never wrote that word in its answer. At the position for the word "experience," the model's own middle layers ranked "nothing" at the top.

**What it means.** We think Qwen 27B's denial is built while the very words it denies are active inside the model. Content is present and usable inside the model, and a late step reports something flatter.

**What this does not show.** A high internal rank for a word does not mean the model experienced what the word describes. It shows only that the word was a live candidate somewhere in the model's processing.
