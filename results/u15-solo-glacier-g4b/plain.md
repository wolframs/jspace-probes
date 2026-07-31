**The short version.** Gemma 4B kept the single word glacier at rank 1
in the lens across the instruction text that followed it, and named it
correctly.

**What we did.** We gave Gemma 4B one word to hold, a glacier, then
asked it to name the word. We tracked the rank of glacier and five
unrelated words inside the model, out of about 250,000 candidates. We
measured this rank at every position, from the first mention of glacier
to the end of the conversation.

**What we found.** Glacier held rank 1 across the instruction text that
followed the word. None of the five unrelated tracked words came near
the top rank in that stretch. Gemma 4B then answered correctly.

**What it means.** A single held word clears the floor for this test.
The lens shows the word in residence and the model's spoken answer
matches what the lens shows.

**What this does not show.** This run used one word only. It does not
show what happens when Gemma 4B must hold several words at once.
