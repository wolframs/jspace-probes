**The short version.** We added the standard measurements to 199 old
records and found that the Gemma lens gives probabilities that carry
almost no information.

**What we did.** We added the missing standard measurements across the
archive: word-register counts for 572 records, emotion
readouts for 197, and lens replay checks for 122.

**What we found.** In Gemma's workspace layers, 34 to 46 percent of
cells show a top probability of 0.99 or more. In Qwen the number is 2
to 5 percent. On Qwen, removal of the emotion cluster did not change
the sensory word rate. The matched random controls did not change it
either. The apology records show a stable emotion readout: "guilty" is
the top emotion in each of about 20 records. In the replay checks, ranks in
the top 100 moved by 7 places or less without steering, and by 11
places or less with steering.

**What it means.** For Gemma, read the rank of a token and not its
probability. The paper's register change from cluster removal did not
appear at our scale.

**What this does not show.** The word counter reads only English words.
This method cannot show register effects in Chinese text.
