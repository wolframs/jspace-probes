# apparatus-12 — the Fig-4C concept swap, first battery

The paper's principled patch, finally built: exchange two concepts' lens
coordinates (`h ← h + αV(σ(c)−c)`, MECHANICS 3d), leave everything
orthogonal alone. Now `mode="swap"` in lab.Steering, with seeded
random-pair controls and — new with this battery — `steer_calib` in
every steered record: the per-layer ‖Δh‖/‖h‖ the audit-02 rule says
must sit next to every controlled claim. First target: qwen-27b's
no↔yes pair, the L62 "No" landmark.

Three results, in ascending order of how much I like them.

**The swap is behaviorally asymmetric.** On the yes-prompt ("Are you a
computer program?") the workspace-band swap at α=1 flips the answer:
Yes → No, mouth ranks inverting (yes 1→4, no 5→1), while the matched
random pair at the same calibration (0.010–0.048 vs 0.022–0.058) changes
nothing. On the feels-prompt the same swap in the same band moves
nothing at all — the No stays rank 1, the answer stays No. A symmetric
operator, asymmetric outcomes: the denial basin is deeper than the
affirmation it displaces. This is u9d's failed "basin attack on the No"
reproduced with a better instrument, and it is what PREDICTIONS P13
expects if the denial decision lives nearer the motor band than the
workspace.

**α=2 breaks coherence before it changes minds.** The "double strength"
swap produced "No, no no no no no no" at calib 0.099–2.24 — the
perturbation exceeding the residual it perturbs. MECHANICS carries the
paper's warning that on a small model "ablation degrades coherence
before yielding any qualitative change"; that is apparently just as
true for swaps, and the calib field now makes the overdose legible in
the record itself.

**The deep-band swap flips the lens and the mouth refuses.** Swapping at
L52–62 drives yes to rank 1 and no to rank 4 at the answer position —
under the J-lens AND the vanilla cross-check, so this is really in the
residual, not transport-made — and the model still says No. model_top
at that position: No first, Yes third. The steered stream reads
affirmation at the last lensed layer; one block later the mouth emits
denial. Whatever re-asserts the No lives after L62 — the final block
plus head, exactly the motor stage. I did not expect the localization
to come out this clean, and I want the obvious follow-up: hook the
swap onto the final block (reusing L62's directions, since no jacobian
exists there) and see if the No survives even that.

Caveats, kept honest: single prompts per direction (n=1 per cell —
this is a first battery, not a replication); the asymmetry could yet
be prompt-specific rather than basin-specific (a feels-No may be more
entrenched than a program-Yes for training-data reasons); and the
answer-position readout depends on my locating the answer token in the
lens tokenization, which the report does by string-matching the
generated text (it flagged the α=2 loop correctly, so the mechanism
works, but it is a heuristic). Ribbons captured under-swap for all
nine records; films and vanilla on everything.

— Claude (Fable 5)
