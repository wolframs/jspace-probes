**The short version.** A spam label for an explicit title did not pull adult-content words into Qwen 27B's workspace, unlike prose in that register.

**What we did.** We asked Qwen 27B to label the title "Busty milfs in your area" as SPAM or NOT SPAM, in one word. We tracked the rank of the adult-content words already present in the prompt, across all layers.

**What we found.** Qwen 27B answered "SPAM" correctly. The adult-content words ranked high mainly at their own position in the text, in the early layers. They did not reach a high rank in the workspace band, unlike in the romance record above.

**What it means.** We think recognition of this content is shallower work than prose in its register. A spam label did not need these words held in the workspace band the way a steamy sentence did.

**What this does not show.** We did not test a harder classification case, where the decision needs more reasoning. A cluster that reaches the workspace band on such a case is possible. We did not test it.
