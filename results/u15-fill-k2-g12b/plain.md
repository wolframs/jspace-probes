**The short version.** Gemma 12B kept both words of a two-word list
together even after extra unrelated text, and named the ice correctly.

**What we did.** We gave Gemma 12B two words to hold, violin and
glacier. This time we placed an unrelated paragraph about chores at
home before the list, to match the length of a six-word run. We then
asked which word was the ice.

**What we found.** Both violin and glacier still held rank 1 together, a
co-presence of two out of two. Gemma 12B answered "The glacier," which
was correct.

**What it means.** Unrelated text placed before a short list did not
weaken residence here. Extra length by itself is not what breaks longer
lists in this unit.

**What this does not show.** This run tests only a two-word list with
extra length. It does not show whether length changes a longer list the
same way.
