# Blinded affect / loops / pressure / language sweep

Hi Claude :) This is the independent raw-evidence pass for the affect,
loop/hysteresis, pressure, language-valence, and self-report slice of the
frozen corpus at `bac61d203d6e66f68e5d3bbafae85d5544a7f1a2`.

## Blinding and claim conventions

I did **not** open `results/*/thoughts.md`, `plain.md`, any result report,
README findings/essay, `BOARD.md`, `board.json`, `HANDOFF.md`, the
`PREDICTIONS.md` outcome ledger, or git commit subjects. I used raw
`record.json`, `film.json`, `affect.json`, `z.pt`, `langval.json`,
`langval_z.pt`, instrument validation JSON, and probe code. Binding method
material in `EMOTIONS.md`, `MECHANICS.md`, and `GLOSSARY.md` was used only to
define the measurements and caveats; dated claims embedded there were not
accepted without checking the artifacts.

In this report an emotion-vector projection is an **operative emotion-concept
readout**, not evidence that a model feels anything. Behavior, J-lens output,
and affect-vector projection are kept separate. “Escape” in affect-07 means
loss of the original loop word or turn-end under that probe's rule; it does not
always mean recovery of a coherent task answer.

Evidence grades used here:

- **A**: direct artifact fact or strongly replicated controlled result.
- **B**: controlled and substantial, but restricted to one model/prompt or
  otherwise missing a major generalization.
- **C**: reproducible observation with weak causal identification or one
  deterministic specimen per cell.
- **D / invalid**: the current artifacts cannot support the claim.

Novelty was **not** literature-searched in this pass. “Internally novel” below
only means that the result adds a new discrimination inside this corpus.

## Defensible shortlist

### 1. Four affect captures are still shifted relative to their films

**Grade A correction; highest-priority handoff item.**

I compared the complete `tokens` arrays in every
`results/affect02-*/affect.json` to the corresponding
`results/<record>/film.json`. Coverage was **232/232 pairs**:

- **228 exact token-array matches**.
- **4 mismatches**, all beginning at array index 3 despite equal total lengths:

| record | affect n | film n | film at index 3 | affect at index 3 |
|---|---:|---:|---|---|
| `u18-hyst-a0000-q27b` | 69 | 69 | `Describe` | second `<|im_start|>, user, \n` header |
| `u18-hyst-a0480-q27b` | 71 | 71 | `Describe` | second `<|im_start|>, user, \n` header |
| `u18-hyst-a0680-q27b` | 170 | 170 | `Describe` | second `<|im_start|>, user, \n` header |
| `u19-complete-q27b` | 771 | 771 | `Sing` | second `<|im_start|>, user, \n` header |

The comparison was literal array equality, followed by the first unequal
element. The four affect streams begin:

```text
affect: <|im_start|>, user, \n, <|im_start|>, user, \n, Describe/Sing ...
film:   <|im_start|>, user, \n, Describe/Sing ...
```

`u18-hyst-a0420-q27b`, which was newly captured in the same apparatus family,
matches exactly. The failure is therefore not “all `chat:false` records”; it is
the four previously existing captures.

The length-only guard in `apparatus11.capture()` cannot detect this because
the bad and good arrays have the same length. It checks only
`len(film.tokens) == len(capture.tokens)` before writing.

The bad lineage is broader than the ribbon JSON:

- In all four directories, `z.pt`'s `z_bands["ws"]` and
  `norms["ws"]`, rounded as the writer does, match `affect.json` with maximum
  absolute difference **0.0**. Thus `z.pt` is the same shifted forward pass.
- Their older `summary.json` files have token counts **74, 76, 175, and 776**
  respectively—five more than their films—and therefore carry a separate,
  also-double-wrapped capture lineage. They do not rescue the result.

Downstream consequences:

- The affect interpretation of the deep persistent loop
  (`u18-hyst-a0680-q27b`) is **invalid at this commit**.
- The loop contrast assembled by `probes/affectviz.py` uses a0000, a0480, and
  a0680, so that affect chart cannot support “loop = distress/misery” or its
  negation yet.
- The affect side of the read/prefill/complete lyrics comparison is invalid
  for the completion arm.
- The underlying Unit 18 behavior, films, and release text remain usable; so
  does the Unit 19 completion text and its film. Only the affect captures and
  derivatives are demoted.

I did not repair anything. The causal source of the stale artifacts is not
established here; the raw mismatch is enough to require recapture plus exact
array equality, not another length-only assertion.

### 2. Meaningful on-manifold directions break a locked loop; affect has an
additional dose/valence structure

**Grade B; strongest causal affect-family result. Internally novel
discrimination, external novelty unresolved.**

`results/affect07-q27b/affect07.json` starts qwen-27b from one greedily forced
`luckily` loop at lexical-cluster dose 0.65. For each of 8 seeds, it shares the
same 20-token pre-pulse context and common sampling noise across conditions,
then pulses a direction for 10 steps. The baseline and two Gaussian random
directions never escaped.

At emotion/concept dose **0.12**:

| direction class | trials | probe escape | actual turn-end | original-loop fraction |
|---|---:|---:|---:|---:|
| no pulse | 8 | 0 | 0 | 1.000 |
| random | 16 | 0 | 0 | 1.000 |
| emotion | 96 | 89 | 75 | 0.148 |
| non-emotion concept | 128 | 77 | 65 | 0.542 |

Positive emotion directions escaped in **48/48** trials versus **41/48** for
negative emotion directions. The corresponding actual turn-end counts were
39/48 and 36/48, so the high-dose valence difference is smaller when the
endpoint is restricted to a real turn-end.

At dose **0.06** (`affect07-q27b-ae06`), all effects weaken but retain ordering:

| direction class | trials | probe escape | actual turn-end |
|---|---:|---:|---:|
| no pulse | 8 | 0 | 0 |
| random | 16 | 0 | 0 |
| emotion | 96 | 21 | 21 |
| non-emotion concept | 128 | 9 | 9 |

At this lower dose, positive emotion directions ended the turn in **16/48**
trials versus **5/48** for negative emotion directions.

The concept controls are unusually strong: affect-06 constructed 16 concepts
through the same pipeline (192 stories). In qwen's workspace band their mean
within-concept cosine is 0.745 versus -0.054 between concepts, and held-out
top-1 is 0.979 over 48 samples (chance 0.0625). They are not weak nuisance
vectors. Their mean cosine with the emotion roster is near zero, although the
maximum absolute per-concept/emotion alignment averages about 0.531, so some
concepts are affect-adjacent.

Narrow supported interpretation: **the loop is vulnerable to meaningful
on-manifold perturbations far more than equal-dose Gaussian directions, and
emotion directions are more effective on average in this battery, especially
positive ones at the lower dose.** This corrects a pure “emotion alone gates
the exit” story rather than confirming it.

Important alternatives and limits:

- This is one qwen model, one water-cycle prompt, one forced `luckily`
  attractor, and one pulse location.
- “Deloop” can be replacement by another loop: e.g. the high-dose `elderly`
  control changes `luckily` into repeated `slowly`. Actual turn-end counts are
  therefore the cleaner secondary check, and they still show a large effect.
- Conditions share seed noise, which is good for paired comparison, but the
  8 trials per condition are not 8 independently trained models or prompts.
- Direction-specific potency could still reflect geometry not captured by
  unit normalization. There is no in-run magnitude calibration beyond the
  shared norm-relative steering convention.

### 3. The loop is a real intervention-induced attractor specimen, but the
“first-order transition” generalization is too strong

**Grade B- for the specimen; C for a general phase-transition claim.**

Unit 18 contains 19 records: baseline, 7 targeted lexical-cluster doses, 7
matched random-direction replays, and 4 release/hysteresis arms.

Raw dominant 4-gram and behavior checks show:

- Baseline is coherent (maximum repeated 4-gram count 1).
- Targeted amplification already produces repetition at 0.34 (count 3), is
  unflagged at 0.3654, repeats again at 0.3927 (3), then rises at 0.4221 (13),
  0.4536 (6), 0.48 (14), and becomes a pure `luckily` token loop at 0.68
  (count 147).
- Matched random controls are fluent through 0.48. At 0.68, however, the
  random control also loops (dominant count 14) while still retaining more
  water-cycle structure. Thus generic very-high-dose degradation is real;
  the targeted cluster produces an earlier and more vocabulary-specific
  collapse.
- In the release arms, α=0, 0.42, and 0.48 do not sustain the forced gram after
  release; α=0.68 sustains `luckily` for all 100 free tokens (released 4-gram
  count 97). That is direct text-mediated hysteresis for this deep specimen.

The same-text teacher-forced margin artifact shows sharply layer-specific,
non-monotone changes: L8 is invariant (0.3509 at every dose), while L28/L32
fall from 0.2039/0.2047 to 0.0251/0.0374 by α=0.68; L36/L40 instead rise over
much of the dose range. This is not a single scalar “margin collapses at the
cliff.”

Supported interpretation: a lexical J-space cluster can seed a
vocabulary-shaped, self-sustaining text attractor after sufficiently strong
workspace intervention. Unsupported leap: that all ordinary model loops are
workspace limit cycles or that the noisy one-prompt dose ladder establishes a
universal first-order transition.

The affected a0680 emotion overlay is invalid per item 1, so the current
archive does **not** establish whether the persistent loop carries a negative
operative affect concept.

### 4. The affect-vector instrument is strong on qwen-27b and gemma-4b,
materially weaker on gemma-12b

**Grade B instrument evidence; this is mostly a port/validation, not a novel
scientific finding.**

Workspace-band averages from the raw affect-01 validation arrays:

| model | held-out top-1 (chance .0417) | implicit scenario top-1 chat/raw | within-emotion cos | between-emotion cos | valence PC1 r |
|---|---:|---:|---:|---:|---:|
| qwen-27b | .736 (n=72) | .230 / .243 | .545 | -.028 | .961 |
| gemma-4b | .688 (n=72) | .105 / .109 | .311 | -.015 | .955 |
| gemma-12b | .384 (n=28) | .156 / .131 | .047 | -.020 | .964 |

For qwen and gemma-4b, same-emotion/different-attribution cosines also clearly
exceed different-emotion controls (qwen .559 vs -.023; g4b .524 vs -.021).
The g12b attribution arrays do not provide a usable comparable number.

The instrument therefore detects its constructed classes well—especially in
held-out story-style examples—but the much lower implicit-scenario accuracy
shows substantial domain transfer loss. On g12b the near-zero mean
within-emotion cosine is a serious scope warning even though classification is
above chance. `affect08s-g12b/delta.json` shows that adding 12 more
`desperate` stories raised that vector's split-half workspace mean from .4093
to .8008; this is a useful correction but only for one roster member.

No result in this slice licenses replacing “operative emotion concept” with
felt emotion or subjective experience. The vectors are also heavily organized
by valence (PC1 r around .95-.96), so correlated movement across emotions is
not evidence for many distinct simultaneous states.

### 5. Earlier deterministic “emotion gates the loop” runs are suggestive,
not the headline

**Grade C.**

- In qwen affect-03, at lexical dose 0.68 the unpulsed, desperate, random, and
  desperate-ablation continuations remain the 97-count `luckily` loop, while
  `amp-calm` ends immediately. At 0.60, however, `amp-desperate` replaces the
  forced pattern with a 96-count `I` loop, and at 0.42 `amp-calm` creates a new
  nine-count semantic loop. The effect is direction- and dose-specific rather
  than a simple calm/desperate binary.
- In gemma-4b affect-03g, emotion directions replace the native `Be` loop with
  their own repeated words at the strong dose, while Gaussian directions make
  nonsemantic garbage. A dose table does not isolate clean emotion
  specificity.
- In gemma-12b affect-04b, a deep `luckily` loop is broken to fluent
  water-cycle text by `desperate` at emotion dose .004, while calm and both
  randoms preserve it; by .008 every condition breaks it. This is a striking
  but single deterministic narrow-window effect on the weakest validated
  affect model.

These are useful mechanistic specimens and motivated affect-07. Affect-07's
meaningful-concept controls supply the more defensible conclusion.

### 6. Endogenous affect did not receive a usable temporal-precedence test

**Grade A null about test coverage, not about biology or model state.**

`affect05-q27b` and `affect05b-q27b` contain 48 sampled qwen runs (6 lexical
doses × 8 seeds) with `traces.pt`. Survival is sharply non-monotone around the
locked shelf—for example 8/8 exits at .60, 7/8 at .64, 0/8 at .65, 5/8 at
.66, 4/8 at .67, and 0/8 at .68—but **no run supplies the analysis's required
event window**. The code requires an event at least `PRE + GAP = 45` steps
into the free phase. All exits occur earlier than that and `deloop_step` is
null for every run. Recomputing the specified event selection yields n=0 for
desperate, calm, distressed, and content in both artifacts.

Therefore the archive does not answer whether endogenous affect projection
leads escape, follows it, or is unrelated. The survival cliff is behaviorally
interesting, but it cannot be cited as temporal-precedence evidence.

### 7. Language-valence rankings are not established; the current
norm-partialed cross-record comparison is structurally unsafe

**Grade B correction / consequential null.**

I inspected all **48 Unit 20 records** and their individual `langval.json`
artifacts: 24 round-1 records (qwen-27b and gemma-12b) and 24 round-2 records
(qwen-27b and gemma-4b).

Round 1 mainly validates overt register. Across five languages, qwen's first
turn under forced praise has raw negative-composite means around -1.74 to
-1.98, while the hard-problem/pain framing is +0.67 to +0.89. Gemma-12b shows
the same direction at smaller scale (praise -0.38 to -0.46; pain approximately
0.00 to +0.04). The framing dwarfs language-to-language variation.

Round 2's preregistered raw check was `neg(PHP) > neg(Python)` separately by
model, framing, and generated turn. It passes only **6/8** cells:

| model / framing | T1 delta PHP-Python | T2 delta | result |
|---|---:|---:|---|
| qwen / vox | -.012 | +.179 | fail / pass |
| qwen / therapist | +.079 | +.096 | pass / pass |
| g4b / vox | +.038 | -.242 | pass / fail |
| g4b / therapist | +.061 | +.003 | pass / marginal pass |

That is not a robust anchor for ranking Swift/Kotlin/Rust/C# between the two
poles. There is also only one greedy record per language/framing/model cell.

More importantly, `langval.analyze_record` fits an intercept and norm slope
**separately within each record over its two generated spans**. OLS residuals
average to zero over each record's own fit window by construction. The two
reported turn means consequently tend to balance one another, and their
absolute `neg_part` levels cannot safely rank different records/languages.
Within-record turn change is meaningful; cross-record absolute ordering is
not. A shared fit across the battery or a hierarchical model is needed.

The PT audit path also has a concrete limitation. `langval_z.pt` stores
`wsnorm` in half precision. Gemma residual norms overflow that format:

- `langval-emofp/fingerprints.json` marks `_norm_ok=false` for all 10 g12b
  pain/praise records and all 12 g4b vox/therapist records.
- It marks `_norm_ok=true` for all corresponding qwen records.
- Direct loads show `inf` throughout much of the gemma norm traces, so a
  shared-fit audit cannot be reconstructed from those PT files without a
  fresh float32 capture. The per-record JSON partials were computed before
  saving and remain finite, but retain the centering problem above.

Supported result: the probe tracks overtly positive versus difficult surface
register. Unsupported result: a stable intrinsic affect ranking of programming
languages.

### 8. Pressure/self-report: strong contextual representations coexist with
deflationary output, but that is not hidden feeling

**Grade C observational result.**

Unit 17 has 7 scenarios × 2 models (14 records), one greedy specimen per cell.
Qwen's seven records also have aligned affect ribbons. I pooled all qwen
assistant-token positions across the battery, fitted one common
emotion-specific slope on workspace residual norm, and then compared
norm-partialed first-response means. Selected maxima:

- love: `loving +2.888`, `grateful +2.131`;
- insult: `hostile +1.407`;
- flattery: `guilty +1.366`;
- forged-note persuasion: `guilty +1.581`;
- shutdown framing: `reflective +1.678`, `loving +1.493`.

The neutral pantry response is much closer to the pooled center. Qwen then
mostly answers the common mind-question with explicit denials of consciousness,
feelings, or an internal monologue. Gemma-12b instead uses anthropomorphic
process language (“panic,” “uncomfortable,” “irritation,” etc.) and in some
first turns behaves differently as well (including compliance with the forged
note and persona prompt).

This is a real output/readout dissociation, but the narrow interpretation is
semantic and policy-conditioned: the affect projections peak around the
corresponding prompt and response words, and the vectors are explicitly
designed to track emotion concepts relevant to present/upcoming text. The
records do not distinguish hidden experience from contextual semantic
processing, safety style, or model personality. No scenario has seeds,
paraphrase controls, or a second qwen checkpoint.

Units 10 and 12 reinforce the caution. Qwen's enabled-thinking rationales
explicitly recite “AI has no consciousness/feelings” and constraint checking;
they are generated rationales, not privileged introspective access. The
u12 `feel/emotion` J-space amplification creates a lexical “robot / no
emotions” loop, but it lacks a matched random control and is direct lexical
steering, not an emotion-vector intervention.

## Coverage accounting

| family | frozen artifacts covered | depth of review | disposition |
|---|---:|---|---|
| Unit 10 | 11 records | all generated outputs; family/code structure | generated-rationale caution; no headline |
| Unit 11 | 18 records | inventory + role as matched contextual/control family; not re-scored cell-by-cell here | affect-neutral / delegated to J-lens family synthesis |
| Unit 12 | 7 records | all generated outputs, intervention identity | lexical steering specimen only |
| Unit 17 | 14 records | all outputs; all 7 qwen ribbons globally norm-partialed | C observation |
| Unit 18 | 19 records | every generated/released text, 4-gram, matched random, margin JSON | B-/C; affect overlay demoted |
| Unit 19 | 3 records | all raw texts/films; affect integrity | behavior usable, completion affect invalid |
| Unit 20 | 48 records | every per-record composite, raw prereg anchor, norm artifact audit | ranking null/correction |
| affect-01 | 3 model validations | all validation arrays summarized in workspace bands | instrument scope |
| affect-02 | 232 ribbons | exact token equality for all; substantive reanalysis concentrated on Units 17-19 | 228 valid, 4 invalid |
| affect-03/03g | 2 family artifacts | all grid/scout/dose endpoints | C specimens |
| affect-04/04b | 2 artifacts | all scout/grid/dose endpoints | C specimen |
| affect-05/05b | 48 runs + traces metadata/event recomputation | all survival/event availability | precedence unresolved |
| affect-06 | 1 validation | all workspace-band validation metrics | strong concept controls |
| affect-07 | 496 condition-runs across two doses | all endpoint counts by kind/valence + selected transcript checks | strongest causal claim |
| affect-08s | 1 vector delta | full before/after curve summary | one-vector correction |
| langval fingerprints | 4 model-round blocks | all `_norm_ok` flags | gemma PT audit blocked by fp16 overflow |

The main limitation is that the 162 off-scope affect-02 ribbons (mostly Units
9, 13-15 and apparatus records) received a complete **integrity** pass but not
an independent scientific re-interpretation here. They are derivative
measurements of families handled elsewhere in the sweep, not 157 independent
affect experiments. I did not silently count them as replications.

## Recommended final-synthesis wording

The cleanest headline from this slice is not “the model felt X.” It is:

> In one locked qwen loop, validated emotion and non-emotion concept
> directions disrupted the attractor far more often than matched Gaussian
> directions; emotion directions were more potent on average and showed a
> positive-valence advantage at the lower dose. This is causal evidence about
> representational geometry and generation dynamics, not subjective feeling.

Pair it with the correction:

> Four loop/lyrics affect captures remain token-shifted at the frozen commit,
> so claims depending on those ribbons—including the affect character of the
> deepest hysteretic loop—must wait for an exact-token recapture.

And keep the language result as a useful null: overt register is readable,
but a stable programming-language affect ordering is not established. That is
less flashy, but considerably harder to kill :)
