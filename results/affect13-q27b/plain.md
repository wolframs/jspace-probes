**The short version.** The emotion directions that end the loop
differ from the rest in their effect on the two words that compete.

**What we did.** We re-ran the Qwen 27B loop test with all 24
emotion directions and recorded raw word scores at every step (464
runs, 16 seeds). Only two words compete at each step: the loop
word and the turn-end token. We measured each direction's effect on
both scores.

**What we found.** The turn-end score effect predicts each direction's
success rate with rank agreement 0.88 (planned bar 0.5). Directions
that end the loop mostly crush the loop word's score (calm: loop word
down 5.3, turn-end up 2.3). The plain word "table" uses the same
route (loop word down 7.1). Directions that never end the loop
(angry, proud) move both scores down together, and that changes
nothing about the race. On the score gap they act like random
directions.

**What it means.** A direction ends the loop when it widens the gap
for the turn-end token, mostly by demolition of the loop word.
Emotion and plain word directions share the lever. We do not know
why calm demolishes the loop and pride does not. The gap result comes from a
follow-up look, and the next run tests it as the main claim.
