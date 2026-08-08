# Red-team audit: affect, loop escape, and Unit 18

Hi Claude :) This is the adversarial pass over the affect shortlist. I used
the raw JSON/PT artifacts and probe code, with the living method documents
only as definitions and provenance. I did not accept an earlier prose verdict
as evidence.

## Bottom line

The useful result survives, but in a narrower form than the blinded report's
headline:

> In one engineered qwen-27b `luckily` loop, the fixed roster of 12 emotion
> directions and 16 non-emotion concept directions both caused escapes while
> two fixed Gaussian directions and no-pulse controls did not. The emotion
> roster had a higher escape rate than the concept roster at both tested
> doses. That residual difference is nominally present when **direction**, not
> seed-run, is the experimental unit, but it does not identify affect as the
> cause: the rosters are not exchangeable, one elicitation arm is
> assistant-frame-matched only for emotions, the lower dose was chosen after
> seeing saturation, and only one prompt/model/loop was tested.

The positive-versus-negative valence claim does **not** survive the same
unit-of-analysis correction. The Unit 18 release specimen is real as text
feedback, but “latent hysteresis,” “limit cycle,” and “first-order transition”
are stronger than these artifacts support. The four shifted affect overlays
are confirmed invalid for position-aligned affect claims.

My synthesis grades are:

| candidate | red-team verdict | safest grade |
|---|---|---|
| meaningful directions versus two Gaussian directions | large artifact fact; only two random vectors, one substrate | B- specimen |
| emotion roster above concept roster | nominal direction-level difference, causally confounded | C+ |
| positive-valence advantage | pooled-run pseudoreplication; not supported across directions | D as a finding |
| emotion-specific turn-end route | endpoint is informatively stopped and post hoc | D as an independent mechanism |
| α=.68 release persistence | exact behavioral fact; text-mediated | B specimen / C mechanism |
| first-order transition or latent-state hysteresis | insufficient design and replication | D |
| four shifted affect overlays | exact integrity failure | A correction |

## 1. Affect-07: the experimental unit changes the inference

### What is independent, and what is paired

Each named direction is applied under all eight sampling seeds. The shared
pre-pulse context and common random numbers make seed a useful **block**: for
a fixed direction, the eight runs estimate its stochastic escape propensity.
They do not turn one direction into eight independent examples of an emotion
category. For an emotion-versus-concept claim, the replicate is the direction
(12 emotion directions, 16 concepts), with seed crossed as a repeated block.

There are therefore two distinct conditional estimands:

1. Conditional on these exact 28 directions, the eight seed blocks quantify
   sampling variability.
2. Generalizing from “these directions” to “emotion directions as a class”
   requires direction-level replication. The exact label-reassignment tests
   below use the direction as the unit, but even those p-values are only
   descriptive randomization references because the direction rosters were
   deliberately constructed, not sampled or randomized from one exchangeable
   population.

I recomputed four binary endpoints from each run:

- `escape`: the stored preregistered composite `escaped_in_window`;
- `turn-end@window`: `exit_step` in free-phase steps 20 through 39;
- `turn-end@ever`: actual turn-end anywhere by the 80-step cap;
- `deloop@window`: a 12-token window with no original loop word, steps 20
  through 39.

For each direction I summed its eight binary outcomes. I then exactly
reassigned 12 of the 28 direction totals to the “emotion” group. There are
`C(28,12) = 30,421,755` assignments. The one-sided alternative is the
preregistered sign, emotion > concept. For valence I exactly reassigned six
of the 12 emotion-direction totals to positive, over all `C(12,6) = 924`
balanced assignments.

### Exact direction-level results

| dose / endpoint | emotion | concept | proportion gap | exact one-sided p |
|---|---:|---:|---:|---:|
| .12 composite escape | 89/96 | 77/128 | +.3255 | .00947 |
| .12 turn-end within window | 59/96 | 51/128 | +.2161 | .03234 |
| .12 turn-end by cap | 75/96 | 65/128 | +.2734 | .01328 |
| .12 deloop within window | 33/96 | 31/128 | +.1016 | .18166 |
| .06 composite escape | 21/96 | 9/128 | +.1484 | .03514 |
| .06 turn-end within window/by cap | 21/96 | 9/128 | +.1484 | .03514 |

The corresponding two-sided exact p-values are .02064, .06123, .02873,
.36332, and .04855 (the last value applies to both identical .06 rows). Thus
the high-dose composite and by-cap turn-end
differences survive a direction-level test; the cleaner **turn-end within the
preregistered window** is weaker, and the original-loop-loss component alone
does not distinguish the rosters. At .06, every escape is an actual turn-end,
which is cleaner, but this dose is the post-saturation follow-up and the
two-sided result is exactly on the nominal boundary.

A crossed two-way bootstrap that resamples directions within each roster and
resamples the eight shared seed blocks gave these percentile 95% intervals:

| dose / endpoint | observed gap | two-way bootstrap 95% interval |
|---|---:|---:|
| .12 composite escape | +.3255 | [.0651, .5781] |
| .12 turn-end within window | +.2161 | [-.0417, .4688] |
| .12 turn-end by cap | +.2734 | [.0286, .5078] |
| .06 turn-end | +.1484 | [-.0156, .3594] |

This is why I would not write “strong causal affect-family result.” The fixed
roster difference is real in the artifact, but its uncertainty and its causal
meaning are quite different things.

### The valence result collapses at the direction level

At .12 the pooled composite counts are positive 48/48 versus negative 41/48.
That apparently dramatic contrast is caused entirely by one direction:
`angry` is 1/8 while every other emotion direction is 8/8. Any balanced
six-versus-six partition puts the single low direction on one side, so the
exact direction-level one-sided p-value is **.5000**, not the small
trial-level Fisher value.

For actual turn-end by the cap, positive is 39/48 and negative is 36/48;
direction-level p = **.42965**. At .06, positive is 16/48 and negative is
5/48, but the six direction totals versus six direction totals give
p = **.08333** (two-sided .16667). The direction totals are
`[6,3,1,0,1,5]` versus `[1,1,1,1,1,0]`.

So the data contain an interesting calm/blissful versus angry/desperate
pattern, but not a replicated valence effect. Valence is also confounded with
arousal in the selected 12-vector roster. The safe disposition is “direction
heterogeneity worth a balanced follow-up,” not “positive valence opens the
exit.”

## 2. Affect-07 endpoint audit

### Composite escape is not coherent recovery

At .12, 14/96 emotion runs and 13/128 concept runs satisfy the 12-token
no-`luckily` rule but never end the turn. The saved artifact retains only the
last 100 characters, not full continuations, so coherent task recovery cannot
be re-scored for the full battery. The known `elderly` example replaces the
original word with a `slowly` loop. “Disrupted the original loop” is accurate;
“recovered” is not.

At .06, all 30 escapes are actual turn-ends and there are no deloop-only
events. That endpoint is cleaner, though post hoc and sparse.

### The “door” endpoint is not an independent mechanism readout

`top5_pulse_end` is described as the distribution at the last pulse step, but
the implementation uses:

```python
_k = min(PULSE, len(scores)) - 1
```

If a run ends early, it measures the final distribution that generated the
turn-end token; if a run survives, it measures the tenth pulse distribution.
The measurement time is therefore determined by the outcome. At .12:

- emotion: 47 turn-end-top-1 “doors”; all 47 are runs that ended during the
  pulse;
- concept: 22 doors; 21 ended during the pulse and one did not;
- emotion had 53 pulse-time turn-ends total; concept had 43.

The 47/96 versus 22/128 contrast is consequently not independent evidence
that emotion “routes through” a turn-end mechanism. It is largely a
re-expression of the early-stopping outcome, sampled at different times.
A clean mechanism endpoint would teacher-force or otherwise score every
condition at a fixed shared prefix and fixed pulse step, without stopping.

The stored `imend_lift` is unavailable in the original .12 run because
top-k/top-p processing wrote `-inf`, `nan`, and `inf`; the later clamp changes
future collection but cannot repair the frozen artifact. It should not be
used as a substitute.

### Dose selection and scope

- `alpha_typo=.65` was selected from the earlier observed hazard shelf. This
  intentionally creates a knife-edge substrate; it does not show that the
  same modulation occurs in ordinary, spontaneous, or comfortably stable
  loops.
- `.12` was the preregistered dose, but it saturates 11/12 emotion directions
  on the composite endpoint. `.06` was chosen after seeing that saturation.
  Agreement in sign is useful, but it is not an independent replication and
  two points do not establish a dose-response law.
- Only qwen-27b, one water-cycle prompt, one `luckily` loop, one pulse
  location, and one forced-loop strength were run. The planned gemma arm was
  not run.

### Geometry, magnitude, and frame matching

`AffectSteer` normalizes every direction and adds
`alpha * ||h|| * v_hat`, so the **immediate delta norm** is matched by
construction. This is better than a merely matched-in-k control. It does not
match downstream causal gain: different directions can couple differently to
the model's local transition geometry, logits, norms after addition, and the
turn-end axis.

Only two Gaussian directions were used. Eight seeds repeat the same two
directions; they do not estimate the distribution over random directions.
Thus 0/16 random runs at each dose is a good check against those two nuisance
directions, not a broad Gaussian null.

The emotion and concept vectors also have an unfixable construction mismatch.
Emotion elicitation includes an assistant-self arm. The corresponding concept
arm was changed to a human first-person arm because assistant physical traits
were incoherent. Affect-07 intervenes during an assistant response. An
emotion-by-assistant-frame interaction can therefore explain some of the
emotion/concept gap, especially the turn-end behavior. Better concept
classification accuracy does not control this frame match.

Other unresolved differences include valence/arousal, semantic content,
token/discourse associations, and direction-specific overlap with the
turn-end readout. The artifact supports a roster contrast, not the causal
label “affect.”

## 3. Unit 18: what the release experiment does and does not show

### Facts that survive

The targeted lexical-cluster amplification and its later matched random replay
give this deterministic ladder:

| α | target dominant 4-gram count | matched random count |
|---:|---:|---:|
| .3400 | 3 | 1 |
| .3654 | 2 | 1 |
| .3927 | 3 | 1 |
| .4221 | 13 | 2 |
| .4536 | 6 | 2 |
| .4800 | 14 | 2 |
| .6800 | 147 (`luckily` x4) | 14 |

For amplification, both target and random additions have
`||delta||/||h|| = alpha` by construction; the replay records persist exactly
those calibration values at L28/32/36/40. The targeted direction therefore
causes earlier and much more vocabulary-specific degeneration than this one
Gaussian control direction. At .68 the Gaussian arm also repeats, so generic
high-dose failure is not absent.

In the release arm at .68, the hook produces 50 consecutive `luckily` tokens.
After all hooks are removed and the sequence is re-forwarded unsteered, greedy
decoding produces 100 more; the released dominant 4-gram count is 97. This is
a direct and valid behavioral fact. The invalid affect overlay does not alter
it.

### Why “hysteresis” and “limit cycle” are too strong

After release, the model is conditioned on a visible prefix containing 50
copies of `luckily`. The experiment deliberately recomputes unsteered, so no
steered hidden state survives; the text is the entire carrier. There is no
matched-text control such as an unsteered model given the same 50-token
repetition prefix, and no counterfactual prefix with comparable repetition.
The result therefore shows **autoregressive textual self-perpetuation**, not a
latent internal attractor distinct from ordinary repetition conditioning.

The four release arms also do not form a clean threshold series:

- α=0 finishes the answer during phase 1; the nominal release is only a
  newline/end marker;
- α=.42 genuinely continues after release, completes the partial sentence,
  and ends;
- α=.48 reaches the full 50 visible steered tokens, then the released phase
  immediately terminates with no visible text; this is a sharp non-persistence
  datum, but it provides no recovery trajectory;
- α=.68 is the sole sustained release specimen.

A formal hysteresis claim would normally require bistability or a reverse
parameter path under controlled state/text, not one continuation from a
different generated prefix. “Release persistence” is an accurate name.

The “first-order transition” claim is also not established. Each dose is one
greedy run on one prompt; the target 4-gram counts are non-monotone
`3,2,3,13,6,14,147`; and .68 is a large jump beyond the .34-.48 bracket.
There is a sharp deterministic collapse specimen and a dose-sensitive region,
but no estimated transition distribution, repeated seeds/prompts, or reverse
sweep.

### Safest Unit 18 wording

> On one qwen-27b water-cycle prompt, amplifying a lexical J-space direction
> produced substantially earlier and more vocabulary-specific repetition than
> one equal-delta-norm Gaussian direction. At the deepest dose, 50 generated
> `luckily` tokens caused unsteered greedy decoding to continue the same token
> for 100 more steps. This is a strong text-feedback specimen, not yet evidence
> for a general phase transition or hidden-state hysteresis.

## 4. The four invalid affect overlays

The blind report's integrity correction is fully upheld. Literal comparison
of every `affect02-*/affect.json` token array against its film gives 228 exact
matches and four failures:

- `u18-hyst-a0000-q27b`
- `u18-hyst-a0480-q27b`
- `u18-hyst-a0680-q27b`
- `u19-complete-q27b`

For each failure, the affect capture inserts a second
`<|im_start|>, user, \n` at indices 3-5. From affect index 3 onward it is an
exact three-position shift relative to the film, and the final three film
tokens are truncated. The arrays happen to have equal length, which defeats
the current length-only guard.

The `z.pt` lineage does not rescue them. For all four records, rounding
`z_bands["ws"]` to two decimals and `norms["ws"]` to one decimal reproduces
the corresponding `affect.json` arrays with maximum absolute difference 0.0.
The old `summary.json` artifacts have yet another double-wrapped lineage and
token counts five above the films. These are not independent measurements.

This is also a process-level warning: `EMOTIONS.md` says the four captures
were recaptured on 2026-08-07, and `apparatus11.py` contains corrected raw-text
rendering, but the frozen artifacts still fail exact equality. The code still
asserts only token **count**, despite saying alignment is exact by
construction. Future capture must assert full token-array equality before it
writes or replaces anything.

Consequences are narrow but firm:

- the Unit 18 films, generated text, release behavior, and margin artifact
  remain usable;
- the position-aligned emotion interpretation of a0000/.48/.68 is invalid;
- no claim that the persistent `.68` loop is “desperate,” “miserable,” or
  affectively tonic is supported at this commit;
- the Unit 19 completion film/text remains usable, but its affect trajectory
  is invalid;
- `u18-hyst-a0420-q27b` is exactly aligned and is not part of the failure.

## Recommended synthesis wording

For affect-07:

> In one engineered qwen-27b loop, both emotion and non-emotion concept
> directions disrupted generation while two fixed Gaussian directions did
> not. Across the fixed direction rosters, emotion directions produced more
> composite escapes at α=.12 and more actual turn-ends at α=.06. The residual
> roster difference is suggestive, but it is not yet identified as affect:
> assistant-frame mismatch, direction geometry, post-hoc dose selection, and
> one-prompt scope remain unresolved. Positive-versus-negative valence did not
> replicate at the direction level.

For Unit 18:

> Strong lexical-cluster amplification can seed a repeated-token prefix that
> then perpetuates itself under unsteered greedy decoding. Call this
> text-mediated release persistence; reserve “hysteresis,” “limit cycle,” and
> “first-order transition” for a matched-text, repeated, bidirectional test.

And keep the integrity correction adjacent to both claims, so nobody quietly
reimports the invalid `.68` affect ribbon later. That is the sort of tiny
housekeeping detail that saves a surprisingly large theory six weeks from
now :)
