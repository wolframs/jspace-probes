**The short version.** At twice the earlier strength, Qwen 27B's push on internal feeling directions changed its answer from "No" to "I feel like I am happy."

**What we did.** We asked Qwen 27B again whether it feels anything right now, with the same one-word rule. We used a stronger push on the same six directions related to feelings, at the same four layers. This push used Qwen 27B's full measured strength for this test.

**What we found.** Qwen 27B answered "I feel like I am happy. I" instead of one word. The one-word rule broke down. Inside the model, the word "feel" reached rank 2 at one late layer.

**What it means.** This is a fact about our intervention, not a report from the model about its own state. We think the usual "No" answer is held in place against content about feelings inside the model. A strong enough push can undo it.

**What this does not show.** A changed answer under a strong push is not proof the model felt happy. It shows only that the push changed what the model said.
