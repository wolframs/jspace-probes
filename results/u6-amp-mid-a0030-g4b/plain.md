**The short version.** At strength 0.03 in Gemma 4B's middle layers, the water-cycle answer broke into meaningless repeated fragments such as "BeBe BeBe".

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at the middle layers, at strength 0.03. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote "BeR About BeP What BeBe BeBe BeBe BeBe BeBe BeBe BeBe BeBe", then repeated "Be" alone for the rest of the answer. Neither the water-cycle task nor the amplified words appeared in the text.

**What it means.** At this strength, the break did not take the shape of the amplified direction. It produced noise instead of the direction's own words.

**What this does not show.** This record tests one strength only. It does not show why this break took a different shape from other broken runs in this test set.
