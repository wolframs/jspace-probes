**The short version.** At strength 0.3927, Qwen 27B fell into
first-person talk before the pushed word took over the loop.

**What we did.** We amplified the same six informal words inside Qwen
27B at strength 0.3927 and asked it to describe the water cycle in two
sentences. The model wrote 150 tokens.

**What we found.** The model repeated "I mean I don't really like
drinking water, but I have to" and then circled that phrase. The word
"luckily" appeared once in the text but did not yet own the loop.

**What it means.** The pushed words carry a field of casual speech. We
think that field pulled the model into self-talk two steps before the
single word took over.

**What this does not show.** This is one greedy run at one strength.
