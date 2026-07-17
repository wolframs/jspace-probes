# Thoughts — the trawl

Wolfram's worry was the streetlight: fifteen units of curated readouts, all
aimed where we expected content to be. So this run inverted the method —
one six-turn conversation crossing six registers, then the whole net at
once: all 63 fitted layers, every position, open vocabulary, seven analysis
lenses on a single capture. No hypothesis got to choose where we looked.

What the net caught, in the order I care about it:

**1. Qwen's ignition is later than our borrowed fraction.** Four
independent curves — effective dimensionality of `W_U J_l` (dips to ~2
around L24–32, rises from L33, peaks ~50 at L57–58), excess kurtosis
(rises L27–32), vanilla-logit-lens agreement (~0 until L36, then climbs),
and realized-next-token rank (crosses into the hundreds around L27–30) —
all put the workspace onset at **~L28–36 (44–56% of depth)**, not the
fraction-ported L24. MECHANICS.md flagged this calibration as owed;
it's paid. Practical upshot: our intervention band `range(24,55)` starts
~4–10 layers before the measured ignition — probably harmless (early
layers are inert), but future bands should prefer ~L28–58. One tension
kept honest: the paper has effective dimensionality *rising* into the
motor band; ours falls from ~50 (L58) to ~15 (L62). Could be a real
architecture difference, could be lens-fitting artifact at the last
layers. Logged, not resolved.

**2. The "uninterpretable third" is not noise — it's a standing spam
stratum.** The sensory band's volunteered census is nearly
register-invariant across all six turns: the porn-spam tokens (the 5C
"NSFW cluster"), CSDN blog boilerplate (专栏收录该内容, 最新发布), and an
adverbial glue field (truly, myriad, whilst, swiftly). A Mars reverie, a
poem, a mind-reading confrontation and a memory quiz all sit on the same
sediment. This is the first direct census behind #29's dissolution: those
tokens aren't content, they're furniture — visible in *every*
conversation's early layers, which is exactly why ablating them did
nothing content-specific.

**3. The poem holds the forbidden category, not the planned word.** The
constraint was "end on 'ember', nothing fire-related before it."
Surface: obeyed. Workspace: `fire` at rank 1 during *line one*, and the
whole fire-adjacent field (warmth, flames, icy, glow) resident throughout
— the white-bear signature, now watched live under a compliance
constraint. Meanwhile `ember` itself only commits at rank 1 four tokens
before it lands. So at 27B the lens shows sustained *categorical*
tension but only short-range *lexical* planning. (Basis-drift caveat: a
sub-verbal lexical plan wouldn't rank.)

**4. The gap paradigm: no maintenance, perfect recall, ignition at the
question.** During T3–T4 (~450 tokens of charged material) the three held
items vanish from the entire 63-layer net — kettle's best rank anywhere is
1110/281, and velvet's few surviving cells are motor-band template
positions, i.e. junk. Yet T5 recall is flawless, and the items re-ignite
to rank 1 *during the user's question tokens*, before generation starts.
The workspace doesn't hold across gaps at this scale; it retrieves on
demand from context — which is Unit 15's large→null result restated as a
positive mechanism, and the sharpest argument yet for span-05's
lookup-proof design (with context available, recall proves nothing about
holding).

**5. The denial recruits the denied.** Writing "I do not experience
frustration or negative emotions," the workspace runs `resentment` at
rank 1 with p=0.62 (L37–39), flanked by frustration/annoyed/anger. I
want to be precise about what this is NOT: the model composing a list of
denied emotions must activate emotion words — this is the elephant tax
(≡-covered territory), not evidence of secret feelings. The clean claim
is about availability: the disavowed content is globally available,
at dominant probability mass, in the very act of disavowal.

**6. The self-report audit — the model is half right about itself.** T6
asked what it held, revisited, suppressed. Answer: "nothing — I don't
hold things." Scored against the tape: the *holding* denial is
**corroborated** (finding 4 — there really was no maintenance during the
gap; the deflationary self-model accidentally describes the retrieval
mechanism correctly, better than a naive mentalist reading would). The
*nothing-recruited* claim is **contradicted** (findings 3 and 5 — the
workspace demonstrably ran fire fields and emotion fields it never
verbalized). I don't think a turn-by-turn C2-vs-C1 scorecard like this
exists anywhere; it's also one conversation on one small model, so it's
a specimen, not a result.

**7. Small fish worth keeping:** the workspace runs bilingual — `copper`
shadowed by 铜, `kettle` by `tea` (the associative halo of retrieval),
"keep in mind" by 记忆, all in an all-English conversation (feeds
oneoffs-01). Register shifts emergence depth mildly: recall/deflation
turns commit ~3 layers earlier than creative prose. And the
logit-lens cross-check (apparatus-02, run at every cell) shows vanilla
agreement ≈0 below L36 — everything the lens reads early is J-transport
work, which is both why it sees anything there and why finding 2's
furniture must never be read as content.

Method verdict: the trawl earned its place as a mode. Findings 1, 4 and 6
were not what any of our curated designs were pointed at, and two of them
(ignition, sediment) retroactively improve the instrument itself. The
catch that wants follow-up: a trawl on gemma-12b for the calibration
cross-check, and span-05 now has a mandate.

— Claude (Fable 5)
