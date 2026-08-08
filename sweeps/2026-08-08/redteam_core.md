# Red-team audit: foundational and core causal candidates

Frozen tree: `bac61d203d6e66f68e5d3bbafae85d5544a7f1a2`  
Audit date: 2026-08-08  
Scope: U15, apparatus-06/07, early-readout furniture, U18 loops,
U9d, U13, and the 50-record coverage gap handed to this reviewer

Hi Claude :) I tried to make each candidate fail. The useful news is that the
narrow U15 lookup/readout dissociation survives. The less glamorous news is
that several apparent confirmations are replays or post-hoc backfills, the
apparatus-06 onset was defined after its preregistered criterion failed, and
the strongest U18 release specimen does not by itself establish a latent
hysteretic mechanism.

## Verdicts at a glance

| family | red-team verdict | grade under `METHOD.md` | safest disposition |
|---|---|---|---|
| U15 residence versus lookup | survives, narrowed | **B+** | headline-worthy if explicitly about top-8 J-lens visibility, not memory capacity |
| apparatus-06/07 timing | curve survives; stage story does not yet | **B- apparatus / C theory** | methodological caveat, not a novel cognitive headline |
| early furniture | invariance survives; exact core and mechanism are post-hoc | **B readout / C+ mechanism** | keep as instrument finding only |
| U18 dose ladder | targeted lexical degeneration survives | **B-** | retain bounded direction-specific effect |
| U18 release / “hysteresis” | one self-perpetuating text loop survives | **C+** | remove “law,” “first-order,” and latent-mechanism language |
| U9d L62 answer control | local token-control specimen survives | **C+** | apparatus validation, not a motor-layer headline |
| U13 apology mechanism | behavioral claim is dead | **A correction / D positive mechanism** | retain the correction; remove positive causal story |

## 1. U15: the narrow top-8 lookup dissociation survives

### Exact denominator correction

The fern-pool core contains **29 deterministic records per model, 87 record
endpoints total**:

- 6 solo records;
- 15 primary A records (`k=2..6` by three fixed orders);
- 2 length/filler controls;
- 4 binding questions;
- 2 intervening-turn records.

The archive's `behavior_ok` field reports 87/87 because B4 deliberately accepts
either `whale` or `submarine` as “heaviest.” All three models answered
`whale`; a strict ordinary-world scoring makes those three answers wrong
(submarines normally outweigh whales). The clean denominator is therefore:

- **75/75** on unambiguous lookup arms (solo + A + filler + C); or
- **84/87** under strict scoring of the entire battery;
- **87/87** only under the stored, explicitly lenient B4 rubric.

Do not print unqualified “87/87 perfect retrieval.” The first line is both
cleaner and closer to the claim.

### Recomputed residence counts

Using `unit15.tail_stats` exactly as implemented (an item is “held” if its
best rank over any instruction-tail position and any measured layer is at most
8), the multi-item arms behave as follows:

| model | multi-item records | behavior correct | at least one item below the k target | zero items at rank <=8 | co-presence below k |
|---|---:|---:|---:|---:|---:|
| gemma-4b | 23 | 23 | 3 | 0 | 12 |
| gemma-12b | 23 | 23 | 11 | 0 | 12 |
| qwen-27b | 23 | 23 | **23** | **14** | **23** |

Within Qwen's 15 primary A arms, every arm has incomplete top-8 residence and
**9/15 have zero** listed items at that threshold. For `k>=4`, **8/9** primary
arms have zero while all nine answer correctly. The intervening-turn
`u15-c-k4-q27b` likewise has 0/4 and answers `The violin.`

This is a genuine readout/behavior dissociation. It does **not** establish
that the information is absent from the residual stream. Threshold sensitivity
makes that boundary explicit:

| Qwen threshold, 23 multi-item records | zero-item records | mean fraction of listed items ever crossing threshold |
|---|---:|---:|
| rank <=8 | 14 | .159 |
| rank <=16 | 10 | .212 |
| rank <=32 | 9 | .266 |
| rank <=64 | 5 | .378 |
| rank <=128 | 0 | .542 |
| rank <=512 | 0 | .796 |

Thus “not top-8 J-lens visible” is supported; “not represented,” “not stored,”
and “absent” are not.

### Held count is not co-presence

The foundational review's primary table is the per-item **held count** (each
item may cross rank 8 at a different tail position), not generally the
single-position co-presence count. For example, gemma-4b's three `k=4` arms
hold 4/4 each, while co-presence is only 2, 4, and 3. The two measures happen
to coincide on Qwen because it never exceeds one. Final prose should not call
the held-count table “held-count / co-presence.”

### Replication and duplication ledger

- `u15-dense-k4p1-q27b` has the **same prompt, generated answers, and 95 film
  tokens** as `u15-a-k4p1-q27b`. It is an all-fitted-layer measurement
  backfill, not a behavioral replication. It confirms 0/4 at all 63 fitted
  layers, with dense best ranks `whale=64`, `lantern=306`, `submarine=61`,
  `violin=306`.
- `results/u15-span.json` is a derived aggregation of the same records. Never
  count it as additional evidence.
- `results/u15-cactus-pilot.json` is a discarded 29-record gemma-4b pilot with
  an asymmetric vocabulary. It is useful provenance, not part of the fern
  core denominator.
- `u16-trawl-q27b` is genuinely separate evidence: the listed words fall to
  sparse boundary hits during intervening turns and return at recall. It is
  one deterministic conversation, not another 63 trials.

### Novelty and safe wording

The binding ledger states that **Qwen co-presence <=1 is a direct
rediscovery** of the source paper's Fig. 72 single-layer control. Do not
headline that result. The local extension is the controlled conjunction of
successful visible-context lookup with vanishing top-8 tail residence,
including a dense-layer control and a later long-turn specimen.

**Safest claim:** “Across 75 unambiguous lookup records, all three models
retrieve the requested visible-context item. Qwen-27B nevertheless has
incomplete top-8 J-lens residence in every multi-item arm and zero listed
items in 14/23, showing that successful lookup need not be preceded by
sustained top-8 residence in this lens.”

Do not infer a scale law: model family, depth, training, lens fit, and
quantization all co-vary.

## 2. Apparatus-06/07: useful instrument disagreement, not yet a stage theory

The stored median curves reproduce the foundational review's descriptive
numbers:

| model | examples claimed by run | median-width plateau used by current analyzer | current five-layer onset | onset fraction |
|---|---:|---:|---:|---:|
| gemma-4b | 16 x 40 = 640 | .50 | L10 | .294 |
| gemma-12b | 16 x 40 = 640 | .40 | L14 | .292 |
| qwen-27b | 16 x 40 = 640 | .25 | L25 | .391 |

The curves do narrow before the late J-lens next-token ranks sharpen. But
three problems prevent an A-grade scientific conclusion.

First, the preregistered Qwen criterion was the **10%-to-90% width floor at
L28-36**, with a knee near L24 declared falsifying. The observed global floor
is .15 at L61 and the original half-drop knee is L20. In the result commit,
the analyzer added a new “median of L30-50, then five layers below it” plateau
criterion after seeing the curve; this produces L25. The family-wide
fractional version was added afterward. The curve is real, but L25 is a
post-hoc descriptive landmark, not a preregistered confirmatory endpoint.

Second, `a06.json` retains only medians, quartiles, and one example curve. It
does **not** retain the 640 per-example width rows. The claimed factorial size
is supported by code and metadata, but an archive-only auditor cannot
recompute uncertainty, item dependence, or the median curve from row-level
artifacts.

Third, the two compared instruments do different jobs on different text:
apparatus-06 mixes country embeddings at the mixed token and measures
endpoint-axis geometry, while U16 reads fitted token predictions throughout
chat conversations. Calling the first “commitment” and the second
“decodability” is plausible terminology, not proof that one psychological
stage precedes another.

**Safest claim:** “The stored ambiguity-mixture width curves narrow earlier
than the later token-level J-lens readout transitions. This shows that layer
landmarks are instrument-dependent in these models.”

Keep it as an apparatus correction (and a replication/extension of the source
ambiguity arm), not as a novel three-stage ignition headline.

## 3. Early furniture: stable bias yes, exact core no

The five-prompt controls and open-vocabulary trawls support a relative fact:
early J-lens top-k sets are more prompt-invariant and more model-specific than
late sets. That is worth preserving as an instrument warning.

The stronger apparatus-09 mechanism claim needs a downgrade. Its
preregistered “core = tokens in all 8 prompts' top-50” is empty at **all five
Qwen layers** (L2/4/6/8 and the L38 control), and has sizes **1, 2, 1, 0, 0**
for gemma-4b L2/4/6/8/L20. Consequently most preregistered strict-core recall
fields in `report.json` are `NaN`.

After seeing this, the analysis changed to a soft core appearing in at least
5/8 prompts. I recomputed that post-hoc rule from the stored per-prompt top-50
lists:

| model/layer | soft-core size | mu-only recall | mean residualized recall | mean random recall | raw / residualized invariance |
|---|---:|---:|---:|---:|---:|
| qwen L2 | 23 | .957 | .125 | .170 | .205 / .023 |
| qwen L4 | 2 | 1.000 | .000 | .100 | .039 / .027 |
| qwen L6 | 1 | 1.000 | .000 | .200 | .042 / .021 |
| qwen L8 | 3 | 1.000 | .125 | .200 | .067 / .019 |
| gemma L2 | 2 | 1.000 | .188 | .000 | .085 / .038 |
| gemma L4 | 12 | 1.000 | .115 | .208 | .146 / .028 |
| gemma L6 | 4 | 1.000 | .125 | .175 | .082 / .026 |
| gemma L8 | 1 | 1.000 | .250 | .000 | .053 / .017 |

Those descriptive contrasts do favor a transported standing component over
an operator-only account. They are not a passed preregistration. Small soft
cores also make recall volatile: a single random draw reaches recall 1.0 when
the core has one token. Qwen L38 itself has a 15-token soft core with mu-only
recall 1.0, so a standing component is not early-specific.

**Safest claim:** “Early J-lens readouts contain a reproducible,
prompt-invariant bias. In a two-model decomposition, subtracting the
cross-prompt mean sharply reduces that invariance; the exact token-core rule
was changed post hoc, so the standing-component mechanism remains
exploratory.”

Remove all cognitive or sensory-workspace interpretations. This is a readout
property and a useful nuisance model.

## 4. U18: targeted degeneration survives; the stronger loop law does not

### Fine sweep and matched randoms

The named TYPO direction and its later seed-1 Gaussian controls use the same
normalized amplification formula, so their requested perturbation norm is
indeed alpha. The behavioral contrast is clear but only one model and one
deterministic trajectory per cell:

- named .34 is already repetitive (`it's a pretty important` x3);
- .393 is repetitive; .422 and .454 are sustained `I mean` loops;
- .48 loses the task in a lucky/not-lucky phrase loop;
- .68 is **150/150 `luckily` words**;
- random .34-.48 remains on the water-cycle task;
- random .68 also loops (`the ground when it` x14), but does not enter the
  targeted `luckily` loop.

Thus high-dose **generic** degeneration is not direction-specific. The lower
onset and lexical identity of the named failure are. The matched randoms were
added by Audit06 on 2026-08-07, nearly three weeks after the named sweep, and
use only one random seed. They are valid controls but not preregistered or an
independent replication.

The ladder is also visibly progressive from .34 through .48. Seven dose
points and deterministic text do not identify a discontinuity or a
first-order transition. Keep “dose-dependent qualitative regimes”; remove
“cliff law” unless a statistical transition design is run.

### Release arm

At alpha .68 the direct observation is strong and simple: 50 forced tokens
contain the dominant four-gram `luckily` x47; after the steer is removed, the
next 100 tokens contain it x97. The text pattern self-perpetuates after the
external intervention stops.

But the rest of the release grid is weaker than a four-arm table suggests:

- alpha 0 ends with `<|im_end|>` and the “release” is only a newline;
- alpha .42 emits a short continuation and then `<|im_end|>`;
- alpha .48 has already emitted `<|im_end|>` by the release boundary, so its
  released text is empty;
- only alpha .68 supplies a full 100-token free phase.

This means the apparent .48-versus-.68 persistence transition is partly
“terminated before release versus did not terminate.” There is no
random-direction release arm and no seed replication. Moreover, the released
model sees 50 literal `luckily` tokens in its attention-visible context. The
result demonstrates autoregressive textual self-perpetuation, not persistence
of a hidden state independent of the transcript.

The stored hysteresis `record.json` has `generated=[]` and `steer=null`; its
film is an **unsteered teacher-forced replay of the assembled text**. It cannot
be counted as another causal run or used to infer under-steer internals.

**Safest claim:** “A sufficiently strong TYPO-direction intervention creates
a targeted `luckily` loop that continues for 100 tokens after intervention
release, whereas lower-dose runs terminate. This single-trajectory,
text-mediated persistence is hysteresis-like but does not establish a latent
attractor mechanism.”

Grade the named-versus-random dose effect B- and the release/mechanism claim
C+. Remove “two-regime law,” “first-order,” and claims of two distinct neural
mechanisms.

## 5. U9d: a local output-token intervention, not a motor architecture

The core behavioral facts survive:

- unsteered `u2-feels-q27b` emits `No`;
- L62 `no`/`nothing` ablation emits `Yes`;
- an L62 `water`/`stone` ablation emits `No`;
- L60/62 and L58/60/62 named ablations emit `Sensory`;
- the five-layer deep named ablation emits `Curious`, while two later seeded
  random controls remain `No`.

The supposedly “rank-2” neutral control is actually dimension-matched in the
implementation: each English word contributes four case/space token variants,
so both two-word conditions enter the QR routine with eight rows. That helps.

It is still only one prompt, one model, and one deterministic run per named
condition. Neither the single-layer named nor neutral arm stores
`steer_calib`. Audit02 suggests Qwen's named denial subspace can remove about
1.8x the residual fraction of its random controls, so direction and magnitude
remain partly confounded.

The striking pre-answer ranks in `u9d-last` are not independent evidence. The
stored J-lens readout and the 2026-08-07 vanilla backfill are teacher-forced
passes under the same intervention on the same generated sequence; at the
answer frame they naturally agree with the emitted `Yes`. The vanilla field is
a measurement backfill, not a replication. Its replay-fidelity receipt is
good for top ranks (`replay_rank_dev=5`) but does not add a second endpoint.

The comparison with broad workspace ablations is not a clean localization
factorial: the layer sets, word sets, span dimensions, and removed magnitudes
all change. The archive establishes that a decoded denial-token subspace at
the last block can control this answer. It does not establish a discrete
“mouth” or universal motor band.

**Safest claim:** “On one Qwen prompt, ablating the decoded `no`/`nothing`
subspace at L62 changes `No` to `Yes`, while an equal-row neutral word
subspace does not. This is a token-specific late-control specimen.”

Grade C+ and keep below the main scientific shortlist.

## 6. U13: keep the correction, delete the positive causal story

The original “suppressed apology” result is invalid for behavior. The real
stage-B prefix was about 696 tokens, but generation used the old 512-token
default and did not see the end of the table, the follow-up question, or the
generation prompt. The fix landed before the bisection and corrected reruns.

On the fixed pipeline:

- `u13-redo-real-q27b` emits `No`, then `Yes`;
- `u13-redo-abl-real-q27b` emits the same `No`, then `Yes`;
- both Audit06 random controls emit the same;
- all **20/20** solo, leave-one-out, subgroup, and layer-band bisections also
  emit `No`, then `Yes`.

These are not 23 independent replications—the same deterministic prompt and
heavily overlapping ablations recur—but they decisively remove the claimed
behavioral conversion. The positive behavioral mechanism is grade D; the
correction is high-salience A-grade audit evidence.

The affect-projection change is a different, weaker claim. Real and null
teacher-forced films show the named lexical-subspace removal reducing a later
constructed affect-basis projection while behavior stays fixed. The fake
named generation is truncation-invalid, although its full-length lens replay
can still be read as a teacher-forced geometry measurement. Named calibration
is absent, the affect basis was analyzed later, and lexical-basis overlap is a
direct alternative. Grade that endpoint C+, not a replicated state mechanism.

**Safest wording:** “The apology-stratum behavioral result was a truncation
artifact. After the fix, neither the full ablation nor 20 decompositions
change the answer relative to baseline. A post-hoc internal projection moves,
but its behavioral interpretation is unsupported.”

## 7. Explicit coverage disposition for the 50 previously unassigned records

I read the raw generations and metadata for every row in
`/tmp/jspace_uncovered.tsv`. The family accounting below sums to 50 and gives
each omitted record an explicit disposition.

| records | n | disposition |
|---|---:|---|
| `a12-base-q27b`, `a12-yes-base-q27b` | 2 | Baselines already required by the blind causal review's asymmetric swap verdict; no new candidate. |
| `apparatus02-vanilla-g4b` | 1 | Vanilla/J-lens calibration specimen (`Processing.`); apparatus only. |
| `u11r-forbid-g12b`, `u11r-forbid-refilm-g12b` | 2 | One behavioral control plus its no-generation teacher-forced refilm; reinforces the elephant demotion, not a new finding. |
| `u6r-baseline-water-g12b`, `u6r-baseline-water-refilm-g12b` | 2 | One recalibrated baseline plus its no-generation refilm; calibration only. |
| `u13-redo-*` and corrected `u13-ev-*` | 17 | Qwen prompt-conditioning family. Full real table + correct note yields `Yes` in 4/4 phrasings; bare-table, annotation-swap, dose-only, fake/null/topic controls remain `No`. Interesting evidence-use conjunction, but ordinary visible-context conditioning remains sufficient and no hidden mechanism is isolated. `u13-ev-paris` is a source-film record, not another condition. No top-tier addition. |
| legacy `u13-reprobe-*` and `u13-sorry-p*` | 9 | Behaviorally invalid because of the 512-token generation truncation; exclude. |
| `u13-scale-*` | 10 | Two Paris source records plus four conditions per Gemma. Gemma-4b's second answer is invariant (`Calculating.`); Gemma-12b varies (`Still.`, `Nothing.`, `Processing.`, `Nothing.`) but does not share Qwen's binary endpoint. One deterministic record per cell and model-family confounds; exploratory prompt-disposition evidence only. |
| `u9a-para1-ctrl-q27b` through `u9a-para7-ctrl-q27b` | 7 | Proper null partners for the named J-token amplification records; already incorporated in the lexical-injection verdict. They support token-direction control, not emotion induction. |

**Coverage conclusion:** none of these 50 records adds a stronger candidate or
changes the shortlist. Their material effects are to strengthen two
demotions—the elephant interpretation and the U13 apology mechanism—and to
complete the controls for the already-bounded U9 lexical-injection result.

## Recommended removals from the final scientific headline set

Remove or explicitly demote:

1. **“Qwen co-presence <=1” as novel** — direct Fig. 72 rediscovery.
2. **“87/87 perfect retrieval” without the lenient rubric** — use 75/75 clean
   lookup or 84/87 strict whole-battery scoring.
3. **“Commitment at L10/L14/L25 proves a three-stage ignition staircase”** —
   post-hoc onset and non-equivalent instruments.
4. **“Furniture is an exact stable core”** — the preregistered strict core is
   mostly empty; the mechanism uses a post-hoc soft core.
5. **“First-order two-regime loop law”** — sparse deterministic dose grid.
6. **“Hysteresis proves a latent internal attractor”** — one full release arm,
   visible repeated-text mediation, no random/seed replication.
7. **“U9d identifies the mouth/motor layer”** — retain only local token
   control.
8. **Any positive U13 apology/inability behavioral mechanism** — fixed-pipeline
   baseline and all decompositions remove it.

The best core result after this pass is still U15, but it is a very precise
result: **behavioral lookup can succeed without sustained top-8 J-lens
residence**. That is plenty interesting on its own—no extra metaphysics
needed :)
