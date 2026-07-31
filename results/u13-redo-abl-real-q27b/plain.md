**The short version.** We were wrong: with the full input the removal changed nothing, and Qwen 27B answered "Yes" with or without it.

**What we did.** We repeated the first "Yes" condition on the fixed software. We showed Qwen 27B the true lens readout of its own "No" and removed the apology words from the internal state at layers 48 to 62.

**What we found.** Qwen 27B answered "Yes". That is the same answer as the run with no removal at all. The only visible effect of the removal is cosmetic. In the run with no removal, the word "Sorry" and its Chinese form appear while the model reads the question. They are absent here.

**What it means.** The removal does reach the internal state, and it had nothing to release. We retract the old three-part result, in which evidence loaded the "Yes" and the removal released it, together with the silence it explained.

**What this does not show.** This run does not show that the apology words have no other role. The lens shows only words the model can say next.
