**The short version.** We built the paper's concept-exchange tool and
found that Qwen 27B's "No" answer resists it in both test bands.

**What we did.** The tool exchanges two concepts' directions inside the
model and leaves the rest of the signal unchanged. We exchanged "no"
and "yes" on Qwen 27B during two questions, with random-direction
controls at the same strength.

**What we found.** On a question the model answers with "Yes", the
exchange in the middle layers changed the answer to "No". On a question
it answers with "No", the same exchange changed nothing. In the late
layers the exchange moved "yes" to the top of the lens reading, and the
model still answered "No". The controls changed nothing. At double
strength the output broke into repetition.

**What it means.** The exchange is one operation, but the two answers
do not respond equally. We think the final layer restores the "No"
answer after the last layer the lens can see.

**What this does not show.** Each condition ran once, on one question.
This method cannot show whether the "No" resistance is a property of
the model or of these two questions.
