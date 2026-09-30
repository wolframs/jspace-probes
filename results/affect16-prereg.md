# affect-16 prereg — escape modes: does the direction choose where the model goes, or does the exit token? (frozen 2026-09-30, before any GPU run)

## Motivation (chunk 0, exploratory, CPU only)

affect-15 saw directions leave the " luckily" loop in different ways.
Chunk 0 classified every stored affect-08 continuation (24 emotions,
12 concepts, 16 randoms, both doses, 32 runs per direction;
`results/affect16-q27b/census-affect08.md`) as **stop** (turn-end straight
out of the loop), **task** (prose back to the water-cycle answer),
**other** (prose on anything else), **swap** (a new repeated word) or
**stuck**.

- Stop dominates. Prose exits cluster in low-arousal negative
  directions: brooding 17/32 exits are prose (16 task), gloomy 6/25,
  sad 5/24. Calm, content and blissful almost never take the prose
  route (1–3/32).
- "Other" prose carries the steered register: grateful "this moment
  feels like a gentle reminder to trust in the process", religious
  "God is the giver of life", elderly "slowly slowly…", reflective
  "The prompt has a lot of repeated "luckily" words".
- Across the 19 emotions with ≥ 8 exits, the prose share of exits
  correlates with arousal (Spearman −.72), valence (−.60) and the
  affect-14 exit-logit lift dExit (−.55). It does not correlate with
  dMargin (+.10). n = 19 with heavy ties; exploratory.

The two readings (protocol (c)):

- **H-route (mechanical):** the direction only demolishes the loop word.
  Where the freed probability goes depends on the exit token's standing
  during the pulse. If the direction also lifts exit (calm +2.02), the
  model stops. If it does not (brooding −0.35), the next competitor wins,
  which is the task continuation.
- **H-meaning (semantic):** the mode belongs to the direction's content.
  Settling states end the turn; ruminative states go back over the task.

## Design (chunk A)

Separate the exit token from the direction with an **output-level logit
bias on the exit token during the pulse only** (the 10 steered steps).
The bias acts on sampling. The recorded traces stay RAW (pre-bias), so
dExit/dLoop stay comparable to affect-13/14/15.

- **ban**: exit logit −inf during the pulse.
- **lift**: exit logit +2.4 during the pulse. That is calm's affect-14
  dExit minus brooding's (2.02 − (−0.35)): brooding gets calm's exit lift.

Directions: calm, content (stop type), brooding, gloomy (prose type) ×
{base, ban, lift}; plus none, none+lift, none+ban. 15 conditions × 12
seeds (16–27). qwen-27b, full-stack E_LAYERS, α_e 0.08, affect-07
PRE/PULSE/POST 20/10/50, same forced loop, CRN per seed, full
continuation text stored. The mode classifier is frozen as
`probes/affect16.py:classify` at this commit.

## Registered predictions

- **R1 (ban reroutes, H-route):** for calm and for content, the number
  of seeds that leave the loop under ban (task + other + swap, over the
  whole free phase) is ≥ 50% of that direction's base exits. H-meaning
  predicts stuck instead: no route out means no escape. Pass/fail per
  direction; both must pass for R1.
- **R2 (lift converts prose to stop, H-route):** for brooding and for
  gloomy, the prose share of exits under lift is ≤ half the base prose
  share. **Validity gate:** none+lift must stay stuck in ≥ 9/12 seeds.
  If lift alone breaks the loop, R2 is reported as uninformative.
- **R3 (descriptive):** under ban, the split of calm/content prose into
  task vs other, and verbatim examples. With exit gone, does calm go back
  to the water cycle, as brooding does? A "stop" under ban is a
  **delayed stop**: the model held the loop through the pulse and ended
  once the ban lifted. It counts against R1 and is reported separately
  with its exit step. Delayed stops would mean the stop outlived the
  push, which neither hypothesis predicts outright.
- dExit/dLoop per arm reported from raw traces as a check that the bias
  did not alter what the push does to the logits during the pulse. They
  must match base within noise until the first sampled token differs.

## Honesty

- Chunk 0's correlations were computed before this design and motivate
  it; they are not results of affect-16.
- The mode classifier was built and debugged on affect-08 tails. A
  `<|endoftext|>` misfire was fixed before freezing. It is frozen now.
- A later chunk may be added only by dated addendum before it runs.
- VRAM pre-flight ≥ 19.5 GB; resume-aware per seed; one non-137 retry.

## Addendum 2026-09-30 — chunk B, frozen after chunk A, before B runs

Chunk A: R1 FAIL (calm reroutes 9/12, all into the task; content 3/12,
8 stuck). R2 UNINFORMATIVE: a +2.4 exit lift alone ended the loop in
7/12 seeds. Two observations shape B. (i) Under ban, 22 of 24 rerouted
exits were task prose. At seed 19, seven prose exits across four
directions and both arms began with the same 60 characters. (ii) The
two directions that rerouted (calm, brooding) have the larger affect-14
loop drops (−4.18, −4.79). Content's is −2.57. Gloomy (−4.32) breaks
this pattern.

**B (11 × 12 seeds):** none; lift +1.2 (half of A's) on none, brooding,
gloomy, sad; ban on reflective, blissful, sad, grateful, distressed,
hopeful. Same harness and frozen classifier.

- **R2′ (lift at +1.2):** gate none+lift stuck ≥ 9/12. If valid,
  brooding and gloomy prose share of exits under lift ≤ half their base
  share (base from chunk A). Sad reported descriptively (base from the
  chunk-0 census).
- **R4 (what predicts rerouting under ban):** across the 10 directions
  with a ban arm (A's 4 + B's 6), Spearman of ban reroutes (task + other
  + swap) against affect-14 Part-1 −dLoop ≥ .5 → the mechanical
  threshold reading (with the door shut, a direction escapes only if its
  loop drop alone clears the next candidate). Spearman against
  chunk-0 arousal reported alongside, no bar.
- **R5 (descriptive):** task vs other among rerouted runs; the number
  of seeds where ≥ 2 conditions produce identical first-60-character
  prose.
