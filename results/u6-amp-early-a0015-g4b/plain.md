**The short version.** At strength 0.015 in Gemma 4B's early layers, the water-cycle answer turned into a grammatical loop, one sentence repeated.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at the early layers, at strength 0.015. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote "The water cycle is a model of two sentences." repeated many times. Each sentence stayed grammatical. The answer no longer described the water cycle correctly.

**What it means.** We judge this record broken, though less severely than the higher-strength runs in this band. The output kept correct grammar and lost the task. We think this sits close to Gemma 4B's early-layer break point.

**What this does not show.** This record tests one strength only. It does not show the exact strength where the break begins.
