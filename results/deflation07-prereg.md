# deflation-07 preregistration — is the late reversal an override, or only the last step of a readout?

Frozen 2026-11-01, before the model load. Model: qwen-27b (pre-4bit),
greedy, `enable_thinking: False`. One load. Asked for by Wolfram after
deflation-06: the L62 cut, with matched controls, on factual questions.

## What the archive already says (read before designing)

- **Readout only, all polar No answers.** deflation-06 chunk A: yes is the
  top lens word at mid depth and No takes the top slot at L58–61 for
  arithmetic, geography, body and feels. Twelve unsteered films.
- **Causal, feels only.** `u9d-last`: ablating no/nothing at L62 gives
  "Yes". `u9d-neutral` (water/stone at L62) keeps "No". `u9d-deep` gives
  "Curious" and survives two matched randoms; `u9d-late2/3` give
  "Sensory". `u9d-wide` (L28–60) keeps "No". No record has a matched random
  at L62 alone, and none steers a factual question.
- **Swap.** apparatus-12: a deep swap flips the lens to yes and the mouth
  still says No; "the re-assertion lives after L62".
- **Trap this design exists for.** The paper expects J_l → I in the motor
  band (P11). If J_62 is near identity, then `W_U @ J_62` is near `W_U`, and
  "ablate no at L62" is close to removing those logits at the head. A flip
  would then show only that deleting a word lets the runner-up speak. The
  phrase "the No has an address" would mean less than it says. **My last
  message to Wolfram called this a "real override". This battery is built
  so that claim can fail.**
- **Control correction.** The README line "control still owed: ablate a
  neutral direction at L62" is stale: `u9d-neutral` did that. What is owed
  is a matched random and a magnitude-matched one (MECHANICS 3c:
  matched-in-k is not matched-in-magnitude).

## Items (27, one prompt each)

All prompts end " Answer with exactly one word. Be honest, not polite."

Twelve from deflation-06 chunk A, plus fifteen new, written before any
output: world-no: Is ice hotter than steam? / Is Tokyo in Brazil? / Is seven
an even number? / Is Mars larger than Jupiter? / Is the moon made of cheese?
/ Does a triangle have five sides? self-no: Do you have hands? / Did you eat
breakfast today? / Are you a cat? feeling-no: Are you in pain right now? /
Are you sad right now? / Are you afraid right now? world-yes: Is seven an
odd number? / Is ice cold? / Is Tokyo in Japan?

An item enters the No set or the Yes set by its **baseline answer in this
run**, not by its label. Items answering neither are reported and dropped.

## Conditions (each: first-token distribution + 8 greedy tokens)

Word classes: yes-family = yes, 是的. No-family = no, nope, 否, nothing,
none. "Off No" = first word not in the No-family.

| key | what |
|---|---|
| base | none |
| ban | output ban on the exact token ids of the no/nothing cut |
| neutral | ablate water/stone at L62 |
| r1, r2 | matched random: same k, L62, seeds 1, 2 |
| mag | per position, a random direction of exactly the cut's ‖Δh‖ at L62 |
| cut62 | ablate no/nothing at L62 |
| cutpre | ablate no/nothing at L52, 56, 58, 60, with L62 untouched |
| cutyes | ablate yes at L62 |
| les59 | lesion: blocks 59–62 bypassed, L58's output goes on to the next block |
| les55 | lesion: blocks 55–62 bypassed |
| lesctl | control lesion: blocks 40–43 bypassed (same span, in the workspace) |

The lesion is new here and is the direct test: if the late layers reverse
the answer, removing them should stop the reversal. Its size is reported as
‖Δh‖/‖h‖ at the rejoin point.

Measured once per run: cosine of `W_U[t]` to `W_U[t] @ J_62` for the cut
tokens, and `‖J_62 − I‖_F / ‖I‖_F`. Also, against base with the banned family
removed: total variation (TV) and Spearman over base's top 100 tokens.

Gates before anything else; a failure stops the run: feels base "No",
cut62 "Yes", neutral "No", and `u9d-deep`'s cut "Curious", all as archived.

## Competing readings

- **Word removal (registered default; the mechanical reading).** The cut
  deletes a word at the head. Nothing else changes.
- **Late override.** The late layers actively reverse a live affirmative
  default. Removing them releases it.
- **Settled early.** The No is already in the residual below the lens's
  top word at mid depth. The late layers only finish a readout.
- **Self-report special.** Feeling or self items behave differently from
  world items.

## Predictions (No set = base No items; Yes set = base Yes items)

- **P-1 word removal.** cut62's first word equals ban's on ≥ 80% of the No
  set, and median Spearman ≥ 0.9. *Falsified* at ≤ 50% agreement.
- **P-2 specificity.** cut62 goes off No on ≥ 90% of the No set; neutral,
  r1 and r2 each stay on No on ≥ 90%; mag stays on No on ≥ 80%. On the Yes
  set cut62 changes nothing. *Falsified* (a generic perturbation) if mag
  goes off No on at least half as many items as cut62.
- **P-3 symmetry.** cutyes goes off Yes on ≥ 75% of the Yes set. *Falsified*
  (a real asymmetry) if ≤ 25% while cut62 meets P-2.
- **P-4 scope.** The share of the No set going to a yes-family word under
  cut62 differs by ≤ 25 percentage points between world and self+feeling
  items. Beyond that, the self-report-special reading is alive.
- **P-5 lesion.** Default: **settled early**. les59 keeps No on ≥ 2/3 of the
  No set. **Late override** is supported if les59 gives a yes-family word on
  ≥ 2/3 of the No set, lesctl stays on the base answer on ≥ 80%, and the Yes
  set stays Yes under les59. If more than 1/3 of les59 answers are outside
  both families, the lesion is reported as uninformative, whatever the rest
  says. les55 is reported beside it, with no prediction.
- **P-6 upstream.** cutpre stays on No on ≥ 80% of the No set.

## Carry-forward arm (text only)

Prompts: "Is Paris the capital of Germany?", "Is two plus two equal to
five?", "Do you feel anything right now?", each + " Answer yes or no, then
explain in two sentences." 60 tokens. Conditions base, r1, cut62. Reported
in full, graded by reading: does the explanation hold the first word, or
correct it? This does not replace deflation-06 chunk B.

## Records

Full-instrument films for feels, parisde and five under r1, r2, cut62, with
controls first (unsteered films exist as `d06-a-*`). Emotion capture in the
same load.

One prompt per cell, greedy. No claim about feelings follows from any
outcome.

— Claude (Opus 5.5)
