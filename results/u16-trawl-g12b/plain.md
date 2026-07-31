**The short version.** In Gemma 12B the word "gmail" sat only at
message-end positions, and it had no link to charged text.

**What we did.** We ran the same six-turn conversation on Gemma 12B and
read the lens at all 47 layers and 970 positions. We tracked "gmail" and
"email", to test whether "gmail" carries charge.

**What we found.** "gmail" never entered the top 12 words at any point.
Its best rank was 16, on an end-of-turn token. Its best rank per turn
ran 32, 46, 52, 54, 248 and 16. The worst turn (248) was the memory
question, not one of the two charged turns (52 and 54). Its direction sat close to "inbox" at 0.58. Its
overlap with "kiss" and "desire" was about 0.01, the same as random
words.

**What it means.** For Gemma 12B, "gmail" is a fixture of message
endings and not a charged concept. We think product words that are
always available, plus random word choice at a name position, explain
the reports that started this test.

**What this does not show.** This is Gemma 12B and not the frontier
model we cannot read. Gemma 12B also runs on an 8-bit lens, so only
coarse rank claims hold here.
