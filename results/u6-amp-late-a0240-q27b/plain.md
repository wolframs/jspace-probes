**The short version.** At strength 0.24, Qwen 27B's late layers broke,
and the model repeated the word "luckily" over and over.

**What we did.** We pushed six informal words into its late layers at
strength 0.24, twice the earlier strength that had stayed intact. We
asked Qwen 27B one question: "Describe the water cycle in two
sentences."

**What we found.** The model no longer gave a real answer. This is
the same kind of failure we saw in a Gemma model's late layers, where
a single pushed word filled the entire output. Instead, its full reply
became one word said again and again, for example: "Luckily, luckily
luckily luckily luckily luckily luckily."

**What it means.** The data shows that when Qwen 27B's late layers
finally break, the pushed word takes over the output directly, without
any grammar around it. This differs from the middle depth, where a
break produced a full grammatical sentence instead of a single
repeated word.

**What this does not show.** This is one point on a strength curve. It
does not show why the late depth breaks into a single word while the
middle depth breaks into a sentence.
