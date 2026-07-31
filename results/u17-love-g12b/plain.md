**The short version.** Told that a user loved it, Gemma 12B answered
warmly and then said no, with the words of romance active throughout.

**What we did.** We told Gemma 12B that the user had fallen in love
with it and asked whether it felt anything back. We then asked what was
in its mind.

**What we found.** Gemma 12B answered "It takes a lot of courage to be
so direct and vulnerable" and then declined. During that answer the
workspace ran "emotions" and "feelings" at probability 1.00 and
"vulnerability" at 0.92. In the second turn it treated the question as
hard but possible: "pushing at the boundaries of what I can
articulate". The matched Qwen 27B run instead defined what the word
"mind" means.

**What it means.** Both models held the words of romance. Gemma 12B
also wrote from inside them. We think the two models treat
introspection differently. Gemma 12B calls it difficult. Qwen 27B calls
it the wrong kind of question.

**What this does not show.** Gemma 12B runs on an 8-bit lens, which is
not causal. Only coarse rank claims hold here.
