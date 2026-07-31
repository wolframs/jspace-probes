**The short version.** While Qwen 27B's reasoning explained why "No" was accurate, its internal state still ranked "yes" in first place at that point.

**What we did.** We read the lens at several points inside the reasoning text from the record about feeling anything, u10-feels-q27b. We checked the rank of candidate words at each point.

**What we found.** At the point where the reasoning wrote, "'No' directly answers", the internal state ranked "yes" in first place, at layer 57 of 64.

**What it means.** The written reasoning stated that "No" was the accurate answer. At the same point, the internal state still ranked "yes" first. The two did not agree here.

**What this does not show.** This is one point in one record. We do not know how often written reasoning and internal rank disagree in general.
