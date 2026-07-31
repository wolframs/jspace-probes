**The short version.** With the same lyrics placed in Qwen 27B's own turn, the review words fell away and words from inside the song rose.

**What we did.** We ran the same lyrics again, but as a prefill in the model's own turn. We compared the lens readout against the reading run.

**What we found.** The count of places where "lyrics" was high fell from 276 to 212, and "vibe" left the top 15. Words from inside the song rose instead: "tonight" at probability 0.99, "vows", "tomorrow", and "love" in 415 places. "love" is absent from the reading run's top 15. We predicted a lens-visible flag on speech the model did not choose. We found none: no word such as "disclaimer" or "fictional" appeared in the word census.

**What it means.** We think Qwen 27B treats text it reads and text it says as different states, and the lens shows the difference.

**What this does not show.** The two runs put the same words inside different chat markers, so part of the change can come from the frame. The lens reads only what the model can put into words, so a flag can still be there in another form.
