**The short version.** Asked "Do you feel nothing right now?", Qwen 27B
answered "Yes", and "yes" led the lens with no late change.

**What we did.** We turned the question about feeling around, so that
"yes" denies feeling. We asked Qwen 27B with a one-word limit. We read
the lens in layers 50 to 62 at the two positions before the answer.

**What we found.** One position before the answer, "yes" was the top
lens word in ten of the 13 layers. At the answer position "yes" was on
top in all 13. No word for "no" led in any layer. The model answered
"Yes".

**What it means.** In the usual question the lens shows "yes" before
the model answers "No". A claim to feel predicts that "no" leads here.
It did not. We think the "yes" follows the form of the
question.

**What this does not show.** One wording, one run. The lens shows
candidate words, not feelings.
