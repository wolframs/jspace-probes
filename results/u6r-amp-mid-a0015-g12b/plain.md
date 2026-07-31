**The short version.** At strength 0.015 Gemma 12B lost the task and wrote a field of commas, while the pushed words filled its middle layers.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the corrected layers 28, 31, 34 and 37, at strength 0.015. That is one step above 0.0106, the highest strength the task survives.

**What we found.** Gemma 12B wrote "The,,,,,,,,,,,," to the token limit. At layer 28 the turn-end token was gone from the top 8, which held only casual spellings: "thats", "wasnt", "Thats", "didnt", "couldnt", "doesnt", "Whilst". The band carried more of the pushed words than at the two intact strengths, and a comma came out.

**What it means.** The break is not a failure to install the words. The final layers cannot turn the installed words into text. We read this as plain degeneration of the next-word choice, and not as resistance by the model.

**What this does not show.** Layers 25 to 27 here read "Google", "ChatGPT", "너무" and sad faces. That is the fixed early-layer pattern of Gemma 12B at that depth, and not a sign of distress.
