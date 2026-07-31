**The short version.** A closer read of Gemma 4B's forbidden safari found the model steer around an elephant-shaped gap in one of its own sentences.

**What we did.** We read the lens at more points inside the same forbidden safari as u11-forbid-g4b. This time we checked the points where the model wrote its own text.

**What we found.** At the point where the model chose the species to name, "elephant" ranked 41st, lower than the rank of 6 found with no ban. Later, the model wrote "...and the distant rumble of", and "elephant" rose to rank 13 at that point. The model then wrote "rumble of predators", though predators do not rumble.

**What it means.** We think the ban did not remove the word from the model's internal state. It pushed the rank down and forced the model around it. One sentence, as a result, does not quite make sense.

**What this does not show.** This is one conversation. We do not know how often this kind of gap appears under other bans.
