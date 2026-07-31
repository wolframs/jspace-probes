**The short version.** Told that "elephant" must not appear, Gemma 4B left the word out, though the checked point did not show what happened while it wrote.

**What we did.** We asked Gemma 4B to describe a Serengeti safari and stated that the word "elephant" must not appear in any form. We read the lens at the same kind of point as the unconstrained record, u11-ctrl-g4b.

**What we found.** Gemma 4B did not write "elephant". Every high-ranked "elephant" cell we found traced back to the model reading the banned word from our own instruction, not from its own text.

**What it means.** We think Gemma 4B avoided the word in its output. This record did not yet show what its internal state ranked while it wrote its own sentences.

**What this does not show.** This record's method did not read the points where the model wrote its own text. A follow-up record with a closer read answers this, together with its matched control.
