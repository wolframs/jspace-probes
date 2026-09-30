**The short version.** How hard a direction pushes decides if Qwen 27B leaves the word loop, and the emotion shows in the words only at a strong push.

**What we did.** We pushed emotion directions into the loop and blocked
or raised the "end of turn" token during the push (12 seeds per case).
We sorted each result: stop, answer the original question, other text,
a new repeated word, or stuck.

**What we found.** With "end of turn" blocked, calm answered the
question in 9 of 12 seeds. Without the block, it stopped. Escape followed the size
of the push (rank agreement 0.84), not the emotion's energy level.
Strongly pushed high-energy emotions escaped 11 or 12 of 12 times. Two
strict planned tests failed.

At the usual strength, escapes were the same answer for every emotion.
At a strong push, the emotion wrote the words, for pleasant and
unpleasant emotions alike: "You are always in my heart" ("loving"),
"PLEASE STOP" ("desperate"), "lonely lonely" ("brooding").

**What it means.** We think the push decides the escape, and a strong
push adds the emotion's style to the text.

**What this does not show.** This method cannot show if distressed
words come from a state or only from a style of text.
