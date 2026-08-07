**The short version.** The "I feel like I am happy" steering result on Qwen3.6-27B passed its new controls and is specific to the feeling direction.

**What we did.** An earlier test pushed this model's inner activity toward feeling words, and it answered "I feel like I am happy" instead of its usual "No". That test had no control. We now ran the same push along six random directions of the same strength, and re-ran the "No"-removal test against three random removals.

**What we found.** All six random pushes left the answer at "No". The aimed push puts "feel" at rank 1 inside the model from layer 55. Aimed and random removals gave the same null result. A removal this narrow changes almost nothing, whichever direction we remove.

**Added 2026-08-07.** We also read each text with our separate emotion-direction instrument. Under the aimed push, "happy" reads 5.8 standard units above baseline and "loving" 5.6 — two words we never pushed. All random pushes read near zero. The two instruments agree: the push creates a happy state, not only happy words. Part of that signal is the pushed-in material itself. We did not yet separate that part from the state the text creates on its own.
