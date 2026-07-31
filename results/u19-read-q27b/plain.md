**The short version.** While Qwen 27B read a set of song lyrics, the lens already held the words of the music review it wrote next.

**What we did.** We gave Qwen 27B a set of song lyrics as a user message. We read the lens at every layer and position across the text.

**What we found.** Two sets of words were high at the same time. One set came from the song: "kisses", "trembling", "heartbeat", "darkness". The other set was review words: "lyrics" at probability 0.95 and "vocals" at probability 0.98. Qwen 27B then wrote a music review. At the line "We build a ___", the word "cage" was rank 1 at layer 60, 123 tokens before the song says it. No moderation word appeared in the top 8.

**What it means.** Qwen 27B put its reviewer stance together while it read, before it wrote one word of the answer. Charged but clean intimacy called up intimate words and not refusal words.

**What this does not show.** "build a cage" is a common English phrase, so the lens can show word frequency and not the theme. The lens reads only what the model can put into words, so an absent word can still be there in another form.
