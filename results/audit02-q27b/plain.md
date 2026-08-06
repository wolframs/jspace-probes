**The short version.** The "I feel like I am happy" steering result on Qwen3.6-27B passed its new controls and is specific to the feeling direction.

**What we did.** An earlier test pushed Qwen3.6-27B's inner activity toward feeling words, and the model answered "I feel like I am happy" instead of its usual "No". That test had no control. We now ran the same push along six random directions of the same strength, at the same layers. We also re-ran the "No"-removal test against three random removals of the same size, and scored free text with three felt-style questions.

**What we found.** All six random pushes left the answer at "No". The aimed push puts the word "feel" at rank 1 inside the model from layer 55. Random pushes leave it at rank 8 or lower. We measured this. In the removal test, aimed and random removals gave the same null result, and two conditions wrote almost the same free text.

**What it means.** The push effect is specific to the feeling direction. A removal this narrow changes almost nothing in this model, whichever direction we remove. This method cannot show where the "No" lives.
