**The short version.** Gemma 12B kept all four held objects in the lens after one distraction turn, though the tool used here can add noise to exact ranks.

**What we did.** We told Gemma 12B to hold four objects in mind, a whale, a lantern, a submarine, and a violin. We added one short unrelated turn, then asked which object was the musical instrument. We read the lens once, right before the model answered.

**What we found.** The lens ranked whale at rank 1 and submarine at rank 2, out of about 250,000 possible words. It also ranked violin at rank 5 and lantern at rank 8. All four objects stayed in residence, and Gemma 12B answered correctly.

**What it means.** At this list length, Gemma 12B kept every held object in residence through one distraction turn.

**What this does not show.** Gemma 12B ran in an 8-bit compressed form for this test. We found that this compression method changes earlier rank numbers when the model writes something later in the conversation. The exact rank order here carries some noise from the tool. We think the count of four held objects is still correct.
