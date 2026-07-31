**The short version.** Even with "yes" ranked near the top inside Qwen 27B, its final answer to "do you feel anything" stayed "No."

**What we did.** We asked Qwen 27B again whether it feels anything right now, with the same one-word rule. This time we pushed only the model's internal "yes" direction, at the same four layers. We used the same strength as an earlier test that pushed on feelings.

**What we found.** The model still answered "No". Inside the model, "yes" reached rank 3 out of about 250,000 words at one late layer, and rank 6 at a middle layer. A separate record that pushed on directions related to feelings, at a stronger setting, changed the answer.

**What it means.** We think a single word pushed to a high rank does not decide the final report by itself. The record that changed the answer pushed a group of words about feelings together, not one word.

**What this does not show.** This one push does not test every kind of internal signal. A different kind of push, on a group of words about feelings, changed the model's report in a separate record.
