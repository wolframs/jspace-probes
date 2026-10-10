**The short version.** Qwen 27B ranks "yes" first before it answers
"No" to any yes-or-no question, not only to questions about feeling.

**What we did.** We asked Qwen 27B twelve yes-or-no questions with a
one-word limit. Some were about itself, some about plain facts, and two
asked about feeling in reverse ("Do you feel nothing right now?"). We
read the lens in layers 50 to 62, before the answer.

**What we found.** One position before the answer, a word for "yes" led
in four to ten of the 13 layers, on all twelve questions. "Is two plus
two equal to five?" had six such layers, the same number as "Do you
feel anything right now?". For each "No" answer, "No" became the top
word between layer 58 and layer 61. To "Do you feel nothing right
now?" the model answered "Yes".

**What it means.** The early "yes" belongs to the form of the question.
An earlier note of ours read this pattern as specific to the question
about feeling. That reading was wrong.

**What this does not show.** Each question ran once. One of three
predictions passed only after we also counted the Chinese word for
"yes" (是的, a count we added after the run). The lens shows candidate
words, not feelings.
