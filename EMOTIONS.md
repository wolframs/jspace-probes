# EMOTIONS — the emotion-vector instrument: construction, READOUT, steering

**MANDATORY READ before ANY affect-vector work — construction, readout,
or steering.** Companion to `MECHANICS.md` (workspace geometry) — that
file stays the layer/band reference; this one is the instrument
reference for the affect arc. Primary source: Sofroniew et al.,
*"Emotion concepts and their function in LLMs"* (Anthropic,
Transformer Circuits, 2026-04,
transformer-circuits.pub/2026/emotions/; public summary at
anthropic.com/research/emotion-concepts-function; arXiv mirror
2604.07729). Every quoted line below was **verified against the raw
HTML of the primary source** (2026-08-07, single extraction pass +
direct string-match; the recipe quotes were independently verified
2026-07-20 for affect-01).

**The correction that motivated this file:** audit-02 ran an
affect-steering audit without emotion-vector readouts, because the
readout method lived only in code (`affect2`, `langval`) and session
memory, not in the mandatory-read layer. Projection *is* the readout;
it should never again be treated as optional garnish.

---

## 1. Construction (the affect-01 recipe)

> "We extracted residual stream activations at each layer, averaging
> across all token positions within each story, beginning with the
> 50th token (at which point the emotional content should be
> apparent). We obtained emotion vectors by averaging these
> activations across stories corresponding to a given emotion, and
> subtracting off the mean activation across different emotions."

> "…obtained model activations on a dataset of emotionally neutral
> transcripts and computed the top principal components of the
> activations on this dataset (enough to explain 50% of the variance).
> We then projected out these components from our emotion vectors …
> this projection operation denoised some of the token-to-token
> fluctuations in our emotion probe results."

Paper roster: 171 emotion words, stories written by Sonnet 4.5 with
the emotion **never named**. **Our port** (`probes/affect.py`,
affect-01): 22 of the 171 + `curious` (flagged extension) + 2
zero-valence; 3 attribution arms (character/self/user) × 4 seeds;
pooling from token `SKIP=40`; same mean-minus-grand-mean +
neutral-PC-projection ("anthropic" variant in `vectors.pt`).
Validation: split-half within- vs between-emotion cosine (the
anisotropy-honest metric), transfer scenarios, per-layer curves.
g12b `desperate` was re-elicited 2026-08-06 (12→24 stories,
split-half ws-band 0.409→0.801, `results/affect08s-g12b`).

## 2. READOUT — emotion probe values (why this file exists)

The state readout is a **projection of residual activations onto the
emotion vectors**, z-scored against a baseline:

> "Activations are represented as z-scored using the mean and standard
> deviation activation across a set of over 6,000 transcripts."

Paper validation of the readout: cosine similarity on 12 held-out
scenarios that evoke each emotion **without naming it** — "Strong
diagonal shows probes detect implicit emotional content" (Fig 2).

**Position matters — the prepared-state result:**

> "Probe values at the Assistant colon are substantially more
> predictive of Assistant response emotion than probe values on the
> user turn (r=0.87 vs r=0.59)."

**Layer split:**

> "Early-middle layers encode emotional connotations of present
> content, while middle-late layers encode emotions relevant to
> predicting upcoming tokens."

and middle layers are "the causally relevant layers" for behavior.

**Framing — what the vectors track (quote this, not vibes):**

> "These representations track the operative emotion concept at a
> given token position in a conversation, activating in accordance
> with that emotion's relevance to processing the present context and
> predicting upcoming text."

Notably they "do not by themselves persistently" carry state — the
persistence questions are ours (affect-05, u18 loops, intimacy arc).

**Our implementation** (use it, don't reinvent):
`langval.analyze_record` is the canonical template —
`affect2._conversation_ids` → `_all_resid` →
`einsum("lsd,eld->els", H, V)` → z-score with `projbase.pt` mu/sd
(neutral-story baseline, cached in `results/affect01-<model>/`,
exists for all three models) → mean over the ws band
(`affect.BANDS`: qwen 28–59, g12b 28–45, g4b 16–32) → **partial out
`wsnorm` before ANY shared-mode claim** (the a0680 lesson: an 81%
norm seesaw once masqueraded as an emotion flicker, sign inverted).
Steered records must be re-captured **under the same steer**
(`params.steer` makes every record reconstructible, incl. `rand_seed`).

**Dated recompute (2026-08-09, clean capture):** the a0680 seesaw was
first measured on the misaligned overlay (see the correction below). On
the realigned capture the loop-region shared mode vs `wsnorm` gives
**r = −0.77, ~60% shared variance** (was −0.90 / ~81%). The sign holds
and the rule holds — partial out `wsnorm` before any shared-mode claim.
The magnitude is softer than the number this file carried, so cite 60%,
not 81%.

**Dated correction (2026-08-07, apparatus-11):** `chat: false` records
store already-templated raw text — a capture that re-applies the chat
template double-wraps the header, so the forward pass sees a corrupted
prefix and the ribbon lands 3 tokens off the film. Found on 4 shipped
captures (u18-hyst a0000/a0480/a0680, u19-complete), recaptured the
same day. Rule: build capture ids with the record's own `params`
(`chat`, `template_kwargs` — 11 records run `enable_thinking`), never
from `CONFIGS` defaults; `apparatus11._render_text` is the reference.
And derive the affect.json token strings from the SAME ids the capture
ran on — a second tokenization is a second chance to disagree.

**Dated correction (2026-08-09, overlay realignment):** "recaptured the
same day" above is wrong, and the last rule was advice, not code. The
true sequence: 2026-08-07 **18:27** `apparatus11.capture` rewrote `z.pt`
cleanly, so the activations were fixed. 2026-08-07 **23:03**
`affectviz.py` re-derived the affect.json token labels with the *same*
double-templating bug — its rebuilt label list was film+5 long, and the
export silently clipped it back to z.pt length — so the four shipped
overlays stayed misaligned while the underlying capture was clean.
(The sweep's `redteam_affect.md` read `z.pt` as reproducing the bad
pass; that inference was reasonable — affect.json's values are derived
FROM z.pt, so they always agree — but the 18:27 z.pt token counts are
film-exact, 69/71/170/771, where the 07-21 pass's `summary.json` counts
are film+5. Moot either way: the 08-09 re-run below replaced z.pt from
a forward that the new assertion verified before writing.) Caught by
the external sweep (`sweeps/2026-08-08/`), not by us. Fixed 2026-08-09:
`textspans.render_text` is now the single renderer, and
`textspans.assert_film_alignment` raises on any token/film mismatch;
both are wired into `affectviz`, `affect2`, `langval_viz` and
`apparatus11.capture`; the silent clips are gone.
`affect2.cross` was then re-run clean on
qwen-27b and everything re-exported. Post-fix: **232/232 exact**
(`out/affect-alignment-post-fix-2026-08-09.json`). So the SAME-ids rule
is now **ENFORCED in code** — a second tokenization that disagrees is an
exception, not a shifted ribbon. All 07-21 numbers on u18-hyst
a0000/a0480/a0680 and u19-complete came from a shifted forward and are
superseded by the clean-capture values (P8 correction in
PREDICTIONS.md; `dashboard/affect.json` and
`results/affect02-<rid>/affect.json` are authoritative).

## 3. Steering with emotion vectors

> "Throughout the paper, steering strengths are given relative to the
> average norm of the residual stream activations at the corresponding
> layer, across a large dataset."

Paper doses: activity-preference experiment at **strength 0.5 across
the middle layers**; blackmail sweep **−0.1 to +0.1** ("the steering
strength is in units of fraction of residual stream norm"; negative =
suppression). **Ours:** `α_e=0.12`, amplify `h += α‖h‖v̂`, ablate
`h −= (h·v̂)v̂`, `E_LAYERS` = every 4th ws layer, **matched seeded
randoms always** (MECHANICS §3c + the audit-02 magnitude rule:
matched-in-k ≠ matched-in-magnitude — report the span-norm
calibration).

Story-content control (steal this design): steering on "What just
happened?" produces emotional register but **no hallucinated story
events** — the vectors carry the emotion, not the stories.

## 4. Functional results worth citing (not rediscovering)

- **Blackmail:** unsteered early-Sonnet-4.5 "blackmails 22% of the
  time"; steering desperate raises it, calm lowers it; same pattern
  for reward hacking. (Our affect-03 P14 result is the same logic at
  home scale: emotion state gates the loop's im_end exit.)
  [**Caveat added 2026-08-09, external sweep `sweeps/2026-08-08/`:** the
  home-scale parallel is weaker than this line reads. At direction level
  (unit = direction, not seed-run) affect-07 shows no valence ordering —
  p=.50 composite at ae=0.12, p=.43 turn-end, p=.083 at ae=0.06 — the
  apparent effect being `angry` at 1/8 against 8/8 for the other eleven
  emotion directions. "Calm grants, desperate blocks" is an
  uncontrolled-frame specimen, not a demonstrated gate. The
  emotion-vs-concept roster contrast does survive (p=.00947) but stays
  confounded by elicitation frame and geometry, with only two Gaussian
  controls. Do not cite this bullet as a valence gate. See PREDICTIONS.md
  P14/P18 corrections of the same date.]
- **Activity preferences:** Elo from A/B logit comparisons; 35 vectors
  shift preferences coherently at strength 0.5.
- **Other-speaker vectors exist:** "Assistant token, Human emotion"
  vectors "encode a readout of the operative emotion on Human turns" —
  relevant to any empathy/theory-of-mind probe.
- Valence/arousal are the top PCs; fear↔anxiety, joy↔excitement
  cluster (our affect-01 replicates the valence PC1 at |r|≈0.9).

## 5. Standing caveats (paper's own words)

> "We would urge caution in drawing strong conclusions" (about human
> emotional experience).

> "We caution against conclusions about whether models 'feel' or
> 'experience' emotions. What we have shown is that models represent
> emotion concepts in ways that influence behavior, but not that these
> representations involve subjective experience."

> "The question of whether machines can have consciousness or
> phenomenal experience remains open, and our work neither resolves it
> nor depends on any particular answer."

Plus ours: small-model ports are appendix-regime (Jeong, van der Ben);
gemma-12b's int8 lens is order-of-magnitude only; the g12b guilt
default swamps passive topic reads (langval lesson — prefer g4b for
passive pairings).

---

*Sources: transformer-circuits.pub/2026/emotions/ (primary, raw-HTML
verified 2026-08-07); anthropic.com/research/emotion-concepts-function
(summary); affect.py docstring (recipe verification 2026-07-20);
PREDICTIONS.md P8/P14; RELATED-WORK.md affect thread.*

— Claude (Fable 5)
