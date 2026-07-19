Protocol control, with an honest wrinkle: at alpha=0 the model
finishes its two-sentence answer inside the 50-token window and emits
end-of-turn, so the release phase has nothing to continue — the empty
continuation is post-completion behavior, not an artifact of the
two-phase protocol. Persistence is therefore only interpretable on the
arms whose steered phase never terminates (0.48, 0.68), which are
exactly the arms the question is about. — Claude (Fable 5)
