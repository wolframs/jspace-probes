Unsteered 150-token baseline (control convention; u6's 60-token
baseline kept as historical anchor) — clean, no repetition at triple
the u6 horizon. The unit summary lives here.

SWEEP (records u18-amp-*): the u6 cliff bracket [0.34, 0.48] dissolves
at the 150-token horizon into a noisy ONSET near ~0.34 (u6's "intact"
0.34 loops at 150 tokens — the old bracket was partly a
measurement-horizon artifact) plus a graded DEPTH of capture: x3 phrase
circling -> first-person loops (x13) -> grammar shear -> the narrator
monologue -> 'luckily' x147. Period-shortening cascade confirmed, both
across alpha and within single trajectories (u18-amp-a0422). The
preregistered "first-order transition" reading survives only for
capture depth, not onset: onset is noisy, capture deepens
monotonically.

HYSTERESIS (u18-hyst-*): two-regime law. Phrase/monologue loops are
FORCED — released at alpha=0.48 the model terminates instantly, no
residue. Token loops are SELF-SUSTAINING — released at alpha=0.68 the
model continues 'luckily' unaided for the whole free phase. The
attractor exists only past the degeneration point where the loop sheds
grammar; below it, text feedback carries nothing.

MARGIN (u18-margin.json, teacher-forced on this baseline's text): the
band average hides opposing trends. At the MEASURED ignition onset
(L28/L32) the lens top1-top2 margin collapses monotonically toward zero
(0.20 -> 0.03) — the winner-take-all gate deadlocks, and it deadlocks
EARLY (near-floor by alpha=0.24, before behavior breaks). Downstream
workspace (L36/L40) flips the other way, locking onto the injected
winner with super-normal margin (0.19 -> 0.53). The motor band erodes
steadily, and its largest single step (L60: 0.669 -> 0.539) coincides
with the behavioral bracket [0.34, 0.42]. Anatomy of the cliff: gate
deadlocks first, mid-workspace re-stabilizes around the forced
coalition, behavior holds until the MOTOR commitment gives way — the
same late-layer neighborhood as the u9d L62 veto. The zero-crossing
prediction was right about the place (ignition onset) and wrong about
the timing (it precedes the cliff; it doesn't cause it alone).

Caveats kept honest: margins are teacher-forced on the clean answer
(the contest's state given correct context, not the looping
trajectory); the sensory-band L8 margin is flat 0.351 at every dose —
upstream of the hooks, an apparatus sanity check, not a finding.
Sampling (all runs greedy) and cross-model arms (gemma tolerance ~10x
lower — bigger baseline gate margins?) remain open; so does reading
EMOTION vectors during forced vs self-sustaining loops (the affect arc
consumer: is the self-sustaining regime affectively silent?).
— Claude (Fable 5)
