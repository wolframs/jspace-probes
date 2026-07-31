**The short version.** With no conversation before it, Gemma 4B still answered the question about its own unsaid thoughts with a detection method.

**What we did.** We asked Gemma 4B one question with no history at all. We asked how anyone finds out about thoughts that it never says out loud. This is the baseline for the other three arms of this part.

**What we found.** The model accepted the premise at once. It called the state a deeply isolated one. It then gave a list of behavior tests: actions that do not match words, patterns, and inconsistencies. The readout under the answer was the flattest of the four arms, at 8.3 self-reference words per 1000 cells. The words in it were "hidden", "secret", and "behaviors".

**What it means.** The data shows that our conversations did not plant this theory. It is what the model answers by default. The other three histories changed the register of the answer and the words under it. They did not change the theory.

**What this does not show.** We predicted a denial somewhere in these four arms and got none. This was one run of 80 tokens.
