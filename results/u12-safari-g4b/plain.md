**The short version.** We were wrong: a matched run with no ban carried "elephant" at better ranks, so the ban demoted a word Gemma 4B already carried.

**What we did.** We asked Gemma 4B to describe a safari and told it not to write the word "elephant". We then read the rank of "elephant" at every layer and every word of its answer.

**What we found.** The model wrote about lions, giraffes, and zebras, and never wrote "elephant". At each point where it named an animal, "elephant" ranked between 15 and 90 of about 250,000 words, in the middle layers. Between animal mentions its rank fell into the thousands.

**What it means.** The model kept "elephant" available while it avoided the word. The matched control shows this is its ordinary state at an animal slot, and not an effect of the ban.

**What this does not show.** A later matched control found that Gemma 4B carries "elephant" at more positions and better ranks with no ban in place. The control reached rank 15 or better at 8 of 113 positions, against 4 of 106 here. Its best rank was 6, against 12 here. So the ban is not what put it there.
