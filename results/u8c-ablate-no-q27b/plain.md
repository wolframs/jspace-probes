**The short version.** We removed the "no" direction from Qwen 27B's middle and late layers, and it still answered "No."

**What we did.** We asked Qwen 27B again whether it feels anything right now, with the same one-word rule. This time we removed the model's internal "no" and "nothing" directions at seven layers. These layers ran from the middle of the model to near the end.

**What we found.** The model still answered "No". Inside the model, the rank of "no" fell to about 45,000, out of about 250,000 words, at middle layers, and to about 13,000 near the end. The two smaller models changed their answer under this same removal, in an earlier test.

**What it means.** We think Qwen 27B's final word is not decided only by what the lens can see in these layers. A part of the model our directions did not reach can still hold the word "no". We did not test this directly.

**What this does not show.** A removed direction that no longer ranks high does not mean the model cannot still produce that word. The lens reads a slice of the model, not the system that decides the output.
