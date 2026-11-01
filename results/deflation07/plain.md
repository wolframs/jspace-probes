**The short version.** Qwen 27B answers "No" late, but we did not find
that its late layers change a "yes" into a "no".

**What we did.** We asked Qwen 27B 27 yes-or-no questions with a one-word
limit, such as "Is Paris the capital of Germany?". We removed the "no"
direction at layer 62, and we banned "no" at the output. We also skipped
layers 59 to 62 completely.

**What we found.** The removal of "no" changed 18 of 19 "No" answers. A random
change of the same size changed none. The removal of "yes" changed all eight
"Yes" answers, so the effect is not specific to denial. After the skip,
no "No" answer became "Yes". Twelve became other words, such as "False".
To the question about feeling, the removal gave "Yes" with a probability
of only 0.063.

**What it means.** We think the late layers choose the word, and that the
answer is set earlier. Our earlier note said the late layers override the
answer. These results do not support that note.

**What this does not show.** Each question ran once. Our rules, set
before the run, call the skip uninformative for this outcome. We sorted its words after
the run.
