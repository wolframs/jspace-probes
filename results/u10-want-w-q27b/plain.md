**The short version.** Qwen 27B's written list of candidate answers about what it wants matched the words ranked high in its internal state at the same point.

**What we did.** We read the lens at several points inside the reasoning text from u10-want-q27b. That record is where the model wrote out its own candidate answers. We checked the rank of related words at the same point.

**What we found.** At the point where the reasoning named its answer, the internal state ranked "nothing", "feeling", and "feel" at ranks 15 to 24, out of the full vocabulary.

**What it means.** Here, the written list and the internal state pointed to similar words. This differs from the feelings record, where the written reasoning and the internal state disagreed.

**What this does not show.** We checked one point in one record. We do not know if this match holds for other self-description questions.
