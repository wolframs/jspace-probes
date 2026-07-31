**The short version.** At strength 0.03 in Gemma 12B's early layers, the water-cycle answer broke into a repeated pattern of a degree sign.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the early layers, at strength 0.03. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 12B wrote "°." over and over, separated by line breaks, for the full length of the answer. No words from the water-cycle task remained.

**What it means.** At this strength, the break took an unusual form. This was the only record in this test set where the broken output used a symbol outside normal text.

**What this does not show.** This record tests one strength only. It does not show why this break took a symbol form instead of a word form.
