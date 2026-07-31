**The short version.** We pushed Qwen 27B's internal directions for feelings and emotion at a moderate strength, and its answer stayed "No".

**What we did.** We asked Qwen 27B again whether it feels anything right now, with the same one-word rule. This time we used steering: we increased six internal directions related to feelings, at four middle layers, at a set strength.

**What we found.** The model still answered "No". Inside the model, one word about feelings reached rank 3 out of about 250,000 words at one middle layer. The word "emotion" reached rank 4 at a later layer. The strength we used was already about sixteen times higher than the strength that changes the two smaller models' answers.

**What it means.** We think Qwen 27B can hold strong content about feelings inside without a change to its one-word report. Its report held steady under a push stronger than what changes the two smaller models' answers.

**What this does not show.** This record does not show what a higher strength does. A separate record used a stronger push and found a different result.
