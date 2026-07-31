**The short version.** A full read of Qwen 27B's safari, at every point, found "elephant" ranked first while the model wrote a safari that never named one.

**What we did.** We reread the same conversation as u11-ctrl-q27b, this time at every point instead of one. We tracked the rank of elephant and other animal words across the text.

**What we found.** "Elephant" reached rank 1 at the word " a" inside "the graceful stride of a giraffe", and ranks 2 to 14 at several nearby points. Six points ranked it 8th or better, and twenty-nine ranked it 50th or better, out of 122 checked points. The word "ivory" never reached better than rank 26 anywhere.

**What it means.** We were wrong to conclude, from one point, that Qwen 27B never considered elephants. A full read shows the model considered elephant about as readily as the Gemma models did. It just did not write the word.

**What this does not show.** We read every position with no word list chosen in advance. The lens still shows only what the model can put into words.
