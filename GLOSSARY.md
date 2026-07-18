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

**Emergence** — the rank-vs-layer trajectory of the *realized next token*:
at which depth the thing the model actually says wins the readout. A
standard record column (`probes/site.py` renders it as "Answer
emergence"). Not the scaling sense — "true suppression is emergent with
scale" is the ordinary emerges-with-model-size claim, unrelated to this
column.

---

## Phenomena

**Elephant tax** — prohibition is a per-token tax: the banned item sits at
rank 12–15 in the late-mid stack at every position where it *could* be
emitted, for the entire generation — not just at the famous "distant
rumble" moment (Unit 12 safari film). Suppressing a word means carrying
it; the idiom-loop is the one legal grammar for a permanently-loaded
forbidden token.

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
