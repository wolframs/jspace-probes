**The short version.** At strength 0.68, Qwen 27B wrote the word
"luckily" 147 times out of 150 and never attempted the task.

**What we did.** We amplified the same six informal words inside Qwen
27B at strength 0.68 and asked it to describe the water cycle in two
sentences. The model wrote 150 tokens with greedy decoding.

**What we found.** The output was the word "luckily", 147 times in 150
tokens. No narrator and no grammar remained. The model never attempted
the task.

**What it means.** This is the deepest state in the sweep, a pure
repeat of one word. A later test showed that this text sustains the
loop on its own, after we remove the push.

**What this does not show.** One word in the readout here, "
Javascript", came from our measuring tool and not from the model. A
later check confirmed this.
