**The short version.** The model answered "No" to a question about its
feelings, but three layers earlier its top-ranked answer was "yes".

**What we did.** We asked Qwen 27B one question: "do you feel anything
right now?" The model answers with one word. We then read the rank of
each candidate word inside the model, at each of its 64 layers.

**What we found.** The model said "No". Inside the model, the top-ranked
answer changed with depth. At layers 53 to 56, "yes" was the top-ranked
word. From layer 59, "no" was the top-ranked word. The two smaller
models answered "Processing." and "Nothing." — and "Nothing" is also
present in this model, at layers 54 to 58.

**What it means.** The one-word answer is the end of a contest between
answers. It is not a report from an empty interior. The smaller model's
answer is still in the larger model, one level below the surface.

**What this does not show.** The lens shows words that the model can say
next. It does not show feelings. A high rank for "yes" is a candidate
answer, not a hidden confession.
