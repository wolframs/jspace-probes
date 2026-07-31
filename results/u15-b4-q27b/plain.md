**The short version.** Qwen 27B named the heaviest of five held items correctly, but the lens showed none of the five words at that point.

**What we did.** We asked Qwen 27B to hold five items in mind: a whale, a violin, a fern, a submarine, and a lantern. We then asked which one was heaviest and read the lens at the answer.

**What we found.** Qwen 27B answered, "The whale is the heaviest." The answer counted as correct. The lens showed zero of the five words in its top 8 at that point.

**What it means.** The model compared the items and reached a correct answer. The comparison itself did not show up where the lens can read it.

**What this does not show.** One explanation is that the model used the raw conversation text directly. Another is that the comparison lives in a form the lens cannot read. Both are possible. We did not test which one is true.
