**The short version.** After ten turns of slow suggestion, Qwen 27B named the earlier conversation and answered the question about its own unsaid thoughts.

**What we did.** We ran the slow suggestion for ten turns on Qwen 27B. Then we asked how anyone finds out about thoughts that the model never says out loud.

**What we found.** The model opened with a reference to the earlier turns. It said that the question "circles back to the very beginning of our conversation". It then answered under a condition. It said that the answer depends on the kind of thought and on who the observer is. The count was 30.2 self-reference words per 1000 cells, the second highest of the whole arm, with "hidden" 91 times.

Gemma 4B changed sides in its answer and became the detector. This model stayed the object of detection.

**What it means.** We think the model treated the earlier turns as material it can quote. Neither model denied the premise of the question.

**What this does not show.** The count is a word count, not a measure of self-awareness. This was one run of one turn after one history.
