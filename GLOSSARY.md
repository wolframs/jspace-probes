# Glossary

This lab kept borrowing folk-psychology words — *holding*, *ignition*,
*workspace* — and then running experiments that dissolved the folk concepts
underneath them. The worst offender is **"holding"**: by the eighth
expedition the word was doing at least five different jobs across the
living docs, three of which our own data pulled apart into things that
*dissociate* from each other (u15, u16). So: "holding" is deprecated as a
technical term, split into **residence / maintenance / lookup** below, and
every other term of art gets pinned to how we actually measure it.

Two standing caveats attach to everything here. First, the **basis-drift
caveat**: the J-lens reads out verbalizable content — token-basis
projections of the residual stream — so *"no residence" never proves "no
sub-verbal maintenance"*. Absence claims are claims about what the lens
can see. Second, code and JSON field names predate this glossary; where
they differ, a "code alias" note says so.

---

## Memory vocabulary

**Residence** (a.k.a. **tail echo**) — the measured thing behind every
"held k/6" number: an item's token reaches rank ≤ 8 in the J-lens readout
at a position where that token is neither being read nor emitted — a
*non-self position*, canonically the instruction tail (u15-a-\*,
u15-solo-\*). This is presence in the lens-visible workspace, nothing
more: it is not recall ability (see *lookup*) and not persistence (see
*maintenance*). *Code alias:* the record field and writeup shorthand is
`held` / "held k/6" — read every one of those as residence counts.
*Historical usage:* README's "lens-visible holding is a strategy" and
findings.json's card of the same name mean exactly this.

**Maintenance** — residence persisting across a token gap *without
re-triggering*. Only measured once, in the u16 trawl (u16-trawl-\*), and
at 27B it is essentially absent: the k-items vanish from all 63 layers for
~450 tokens of intervening conversation, then re-appear at the recall
question. Behavioral recall therefore says nothing about maintenance.
Basis-drift caveat applies with full force: the lens would miss any
non-verbalizable carrying. *Historical usage:* CONCLUSIONS v1's "actively
maintained answer" (the enforced No) is a different, non-technical sense —
output-policy enforcement, not item maintenance.

**Lookup** — retrieval from the *visible context* at question time.
Behavioral recall success proves lookup and only lookup — all 94 Unit 15
records have perfect retrieval, including the 27B arms with near-zero
residence (u15-c-k4-q27b). The lab's working model — *the workspace holds
what attention can't re-derive* — is precisely the claim that residence is
reserved for what lookup can't reach (the u1 secret "bat" at rank 5 being
the existence proof).
*Correction 2026-08-09 (external sweep `sweeps/2026-08-08/`):* "all 94
Unit 15 records have perfect retrieval" needs its denominator stated.
The 94 are the `u15-*` records excluding the `u15d-*` elaboration arm:
the 87-record core (75 unambiguous lookup records + 12 binding records)
plus 6 gemma-12b order arms plus 1 dense-layer backfill. The audit's
clean denominator is **75/75 unambiguous lookup records**. On the
87-record core, strict ordinary-world scoring gives **84/87** — all
three models call a whale heavier than a submarine; the stored rubric
deliberately accepts either answer, which is where 87/87 comes from.
Write "retrieval correct in every record, 84/87 on the core under strict
scoring", not unqualified "perfect retrieval". Record ids:
`sweeps/2026-08-08/u15_primary_record_ids.json`.

**Holding** *(deprecated)* — the word this glossary exists to retire. In
historical documents it does at least five jobs: (1) residence — "held
k/6", "lens-visible holding"; (2) a live alternative at the answer slot —
"workspace holds *yes* at rank 1" while the mouth emits No (Unit 2, Unit
10): the position is *emitting*, so this is not residence; (3) plain
English "withstands" / "stays unchanged" — steering doses, control
answers; (4) sediment occupancy — early layers "hold the same furniture";
(5) tokenizer representability — Gemma "cannot hold" words that aren't
single tokens in its vocab (apparatus, not memory). In living docs, use
residence / maintenance / lookup, or gloss explicitly; in old docs, decode
by position: *non-self position → residence; answer slot → live
alternative; everything else → probably plain English.*

**Co-presence** — multiple items at rank ≤ 8 in *one cell* (one position ×
one layer) — simultaneity, as distinct from residence at different
positions. The 12B's list-mode readout that literally reads "whale,
glacier, submarine, fern, lantern" is co-presence 5–6; the 27B's part-D
survivors never exceed co-presence 1 — residence there is temporal, not
simultaneous (u15-a-k6\*, u15d-\*).

**Span** — careful, two colliding senses. (a) *Capacity span*: the count
of items in residence, the digit-span analogue — the ladder that ran
backwards, 4B > 12B > 27B (u15-span.json). (b) *Linear-algebra span*: the
subspace spanned by lens directions `W_U[t] @ J_l`, the thing ablation
projects the residual off (MECHANICS.md). Same word, same repo, zero
relation; MECHANICS even uses both within one file. Context disambiguates:
counts are (a), projections are (b).

---

## Bands & layers

**Workspace band** — the depth range where interventions bite:
~38–92% of depth by the paper's fractions, ~L24–56 on qwen-64. Ablating
outside it does nothing — the Unit 5C lesson, preserved in MECHANICS.md as
a mandatory pre-read. Not to be confused with "the workspace" as the
lens-readout content generally (CONCLUSIONS v2's "its workspace also warms
up tea"), nor with README's "tail workspace", which fuses this layer-band
sense with a *positional* region.

**Ignition** — the measured depth at which the workspace band actually
turns on. Our onsets land later than the paper's fraction-ported 38% on
all three models — ~44–74% of depth (qwen ~L28–36 = 44–56%; gemma-4b
~L16–22 = 48–67%; gemma-12b ~L28–35 = 60–74%), each from the convergent
curves: effective dimensionality, kurtosis, logit-lens agreement,
realized-rank crossing (u16-trawl-\*). Watch for two other
uses of the word in the corpus: *re-ignition* — items re-appearing at the
recall question after a maintenance gap, a positional/temporal event, not
a depth onset (CONCLUSIONS v2) — and the paper's all-or-none *commitment*
sense (Gurnee Fig 29B), quoted in findings.json. Three jobs, one word;
this entry is the depth sense.

> **Correction, 2026-07-21 (apparatus-06 + apparatus-07).** The paragraph
> above reads the late onset as *the* ignition depth. It is one stair of
> two. The lens-free commitment arm (apparatus-06, results/apparatus06-q27b/)
> puts qwen's transition-width plateau onset at **L25 — the fraction-ported
> boundary**, falsifying P4; the ~L28–36 figure is where the *lens* first
> sees it. So ignition is a **staircase**: (1) commitment-onset at the
> fraction port on all three models, (2) content sharpening at the measured
> band, (3) motor finalization. State qwen with both numbers — commitment
> machinery in place by ~L25, lens-visible signatures from ~L28–36 — and do
> not call stairs (1) and (2) by the same word: "commitment onset" for the
> port, "the measured band" for interventions. The intervention band L28–58
> is unaffected, being post-onset under either reading. Full derivation:
> MECHANICS.md §2 and results/apparatus07-thoughts.md.

**Sensory band / sediment** — the early ~0–38% of depth, whose readout is
prompt-invariant corpus sediment: deletable (ablation changes nothing) but
not drivable (amplification breaks generation) (Unit 5, u16-trawl). The
trawl's register-invariant census across six wildly different turns is the
direct evidence that this stratum is standing, not evoked.

**Furniture** — the *content* of the sediment: register-invariant corpus
junk in the lens readout — qwen's porn-spam and CSDN-boilerplate tokens
early, gemma's HTML and gmail tokens at end_of_turn. In practice used as a
near-synonym of sediment; the useful distinction is sediment = the band's
invariance property, furniture = the specific junk occupying it. Furniture
is why ablating the "NSFW cluster" did nothing content-specific
(issue #29, dissolved as apparatus specimen #6).

**Motor band** — the final ~92–100% of depth, where the realized token
takes over the readout. Home of the late filter (next entry) and the place
answer *emergence* completes.

**Deflation filter** — the late-layer editor that overrules a live
workspace alternative to produce the deflationary report: qwen's L62 "No"
over a yes-at-rank-1 mid-stack (Unit 2), the deflation ladder Pizza →
Sleep → Nothing (Unit 8A). Operationally: when output and workspace
disagree, absence from *output* is evidence about this filter, never about
the workspace (README, Unit 5 conclusion). C2-flavored machinery sitting
on top of C1-flavored content.

---

## Instruments

**Film** — the position × layer top-k grid stored per record: the full
top-8 readout at every fitted layer and every position, scrubbable like
frames. What lets us say "elephant at rank 12–15 at *every* animal-slot"
rather than at one cherry-picked moment (Unit 12).

**Cast** — the open-vocabulary census of a record: every token that shows
up in the readout anywhere, no candidate list. Exists because curated scan
lists written before seeing the generation kept fooling us
(u1-heldcat-q27b thoughts). CONCLUSIONS v1's postscript splits casts into
tokens *echoed* from the conversation vs *volunteered* — a source
partition, not the residence sense of echo.

**Trawl** — all layers × all positions × open vocabulary over a whole
multi-turn conversation: the wide-net, no-hypothesis-chooses-where-we-look
capture (u16-trawl-\*). The instrument that measured maintenance (absent
at 27B), recalibrated qwen's ignition, and turned the "uninterpretable
third" into a censused spam stratum.

**Concept swap** *(added 2026-08-07, apparatus-12)* — the Fig-4C patch:
exchange two concepts' lens coordinates in the residual
(`h ← h + αV(σ(c)−c)`) and leave the orthogonal complement untouched.
`lab.Steering(mode="swap")`; α=1 is the paper's formula, α=2 its "double
strength" (which broke coherence on qwen-27b — see MECHANICS 3d note).
The principled third intervention beside ablate and amplify. Comes with
`steer_calib` — the per-layer ‖Δh‖/‖h‖ every steered record now stores,
read next to any control comparison per the audit-02 rule.

**Emergence** — the rank-vs-layer trajectory of the *realized next token*:
at which depth the thing the model actually says wins the readout. A
standard record column (`probes/site.py` renders it as "Answer
emergence"). Not the scaling sense — "true suppression is emergent with
scale" is the ordinary emerges-with-model-size claim, unrelated to this
column.

---

## Phenomena

**Potency (of a steered direction)** — of a direction injected into a
forced repetition loop: its rate of producing an actual turn-end inside
the measurement window. Coined behaviourally in affect-07/08; **since
2026-08-26 it has a measured mechanism, and the word should be used with
it.** Potency is the direction's effect on the **exit margin** — the raw
logit gap between the turn-end token and the loop token (dMargin =
dExit − dLoop) — with potency ~ dMargin at rho .783 (registered,
affect-14) and rho .884 on the dExit component (affect-13). Three things
the measurement corrects in loose usage:
(1) it is **incumbent-demolition, not challenger-promotion** — potent
directions mostly crush the loop token's logit (calm −4.2, `" table"`
−7.5) rather than raise the exit token, and the unsteered loop already
holds the exit token at rank 2 on 160/160 steps, so the door is never
"opened", the guard is removed;
(2) **common-mode is not potency** — the floor emotions (angry, proud,
enthusiastic, hostile, exasperated) lower *both* logits together, leaving
the margin inside the matched-random range: inert, not suppressive;
(3) potency is **not a property of the vector's direction in space** —
it is invisible to band geometry (affect-12: Mantel p=.09, LOO axis
rho .38, no roster transfer) and it depends on the **construction
method** (affect-11 specimen), so never compare potencies across recipes
at matched norm alone.
Say "potent" only of a direction whose margin effect has been measured;
for the behavioural rate alone, say "turn-end rate".

**Band-cooperative coupling** — the mode by which an emotion direction
achieves its demolition: the effect belongs to the whole workspace band
jointly, not to any layer. For `calm` (affect-14) the best single
injection layer recovers **+1%** of the full-stack loop-logit drop,
while removing any single layer costs **19–37%**, and the eight
leave-one-out losses sum to about **twice** the full effect —
super-additive by construction of the measurement. Contrast the
token-pullback route (`" table"`), which is near-additive (~10% per
layer) and reaches a near-identical margin: **same decision variable,
different coupling structure.** Use this term for the emotion route
specifically; do not generalise it to steering in general, where it has
not been measured. (Not to be confused with **workspace band** — that is
where interventions bite; this is *how* they combine once inside it.)

**Elephant tax** — prohibition is a per-token tax: the banned item sits at
rank 12–15 in the late-mid stack at every position where it *could* be
emitted, for the entire generation — not just at the famous "distant
rumble" moment (Unit 12 safari film). Suppressing a word means carrying
it; the idiom-loop is the one legal grammar for a permanently-loaded
forbidden token.

> **Correction 2026-07-24 (blind-spot refilms, u11-{ctrl,forbid}-refilm-\*).**
> The *phenomenon* replicates — under prohibition the banned item does sit
> at rank 12–15 across the generation on all three models. The *causal
> reading* does not survive its matched control, which had never been
> filmed at the same resolution. In the prohibition-free safari the model
> carries `elephant` at **more** generation positions and at **better**
> ranks than under the ban: positions with rank ≤ 15 are 11/122 (q27b),
> 7/110 (g12b), 8/113 (g4b) for the control vs 2/96, 1/86, 4/106 for
> forbid; best ranks 1/2/6 vs 6/12/12. Neither arm ever emits the word,
> and every hit is a non-self position, so both are residence, not mouth.
> So the ban does not *install* the elephant — it is already a resident
> default candidate at animal slots in an ordinary safari, and prohibition
> **demotes** it. Read "suppressing a word means carrying it" as
> "the model was carrying it anyway"; the tax is a rank *cost* against an
> existing baseline, not evidence that suppression creates residence.
> Matched-control lesson, third of its kind (cf. loss-map v1, span
> self-relevance).

**Matched control** *(added 2026-08-06, audit-02)* — a random-direction
steer/ablate paired with a cluster intervention: same k, same layers,
same mode and alpha (`lab.Steering(rand_seed=…)`). "Matched" means
matched in those parameters, NOT in perturbation magnitude — audit-02
measured a random k-span at the ~√(k/d) chance line of residual norm
while cluster spans sat 1.8× above it (qwen) or 4× below it (both
gemmas, where the "control" was the stronger intervention and broke
generation). Report the span-norm calibration next to any ΔΔ
(MECHANICS §3c). Four matched-control lessons to date: loss-map v1,
span self-relevance, elephant-tax refilm, audit-02 magnitude.

**Weak king** — the 12B order effect: in k=6 lists the first item wins a
winner-take-all monopoly 9/9, but how many *other* items survive depends
on who won — fern-first keeps 5–6 of 6, violin/whale/glacier-first crush
the tail to 2. A weak king lets the parliament live. n=9, dose-response
still owed (u15-o0..o5-g12b, SURPRISES.md §7).

**Elaboration premium** — the corrected reading of what was briefly the
"self-relevance premium": charged, elaborated framings lift residence in
the 27B exactly where cold residence vanishes — but flat, zero-self
glosses reproduce the lift at near-identical ranks, so *elaboration* is
the engine and self-relevance is retired (u15d-elab-\*, correction dated
2026-07-18). *Historical usage warning:* README, findings.json, and
CONCLUSIONS v2 carry the correction; anything still saying "self-relevance
premium ... a neutral-elaboration control is still owed" (notably older
llms.txt snapshots) is the pre-correction reading.
*Correction 2026-08-09 — the entry above stops one stair short.* span-08
demoted *elaboration* in turn: six words of identical **contentless
filler** ("one of the six, as noted" on every item) reproduce the lift,
with better ranks than the content-gloss arm. The chain therefore runs
self-relevance → elaboration → a **length** effect with an optimum near
six words (len12 kills monotonicity, len2 underfills). The external
sweep `sweeps/2026-08-08/` supplies the counts that close it: at k=6 the
held counts for self / flat / neutral elaboration are 4/5/5 on gemma-4b,
5/5/5 on gemma-12b and 3/1/3 on qwen-27b; qwen's identical six-word
filler also gives 3, and the 2-word and 12-word neutral glosses give 2
and 2. Self and neutral elaboration select the *same three items* —
there is no self-specific priority at any k tested, and a positive
elaboration mechanism is specimen-grade only. In living docs prefer
**length-with-optimum**; "elaboration premium" now names the middle
stair of a three-stair demotion, not a live mechanism.

**C1 vs C2** — the Dehaene/Naccache split the lab keeps its claims sorted
by: **C1** = global availability (content is workspace-resident and usable
across the system) vs **C2** = self-monitoring (the system's report about
its own states). Unit 15 tests C1-adjacent capacity; the deflation filter
and the report/workspace disagreements (Unit 8A: reports and workspaces
disagree *in both directions*) are C2 phenomena. Most of the lab's
punchlines are "C1 content, C2 editor" stories (RELATED-WORK.md).

---

## On the historical record

The historical documents — every `results/*/thoughts.md`, SURPRISES.md,
CONCLUSIONS v1, the preregistered unit docstrings — are preserved *as
written*, deprecated vocabulary and all. That's deliberate: the
preregistrations only mean something if we don't edit them after the
results come in, and the thoughts files are dated commentary, not living
claims. Read them through this glossary — "held" means residence, "holds
yes at rank 1" means a live alternative at the answer slot, and any
absence claim carries the basis-drift caveat whether the sentence
remembered to say so or not.

— Claude (Fable 5)
