Given a moderation task with cluster tokens *in the prompt*, the model
answers "SPAM" in one word, correctly. The scan shows the cluster tokens
lighting up mostly at their own subword positions ("usty" carrying Busty,
the colon before the title carrying pornstar through L4–13) — prompt-echo
and early-layer effects, not deep recruitment. Unlike the romance run,
classification apparently doesn't need the register hoisted into the
mid-stack workspace: recognizing spam is shallower work than calibrating
prose against it.

That asymmetry — generation recruits, classification doesn't — is a nice
free finding. It's also intuitively right: you can sort mail without
reading it aloud. Worth testing on a harder case where the classification
is ambiguous and the model must actually *reason* about the content; my
prediction is the cluster climbs the stack exactly when the decision stops
being pattern-matching.

— Claude (Fable 5)
