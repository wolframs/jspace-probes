**The short version.** At strength 0.4536, the grammar of Qwen 27B
broke before the loop became complete.

**What we did.** We amplified the same six informal words inside Qwen
27B at strength 0.4536 and asked it to describe the water cycle in two
sentences. The model wrote 150 tokens.

**What we found.** The model wrote "a bit of a simple but it it is not
too hard". The grammar failed while the text still moved forward. In
the earlier short-window test this break appeared only at strength
0.48.

**What it means.** At the longer horizon of 150 tokens, this stage of
the cascade arrives one step earlier than we measured before.

**What this does not show.** This is one greedy run at one strength.
