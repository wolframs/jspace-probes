# thoughts — affect-01, gemma-4b

The port works. That's the headline and I want to be precise about what
"works" means: 24 story-elicited emotion vectors (Anthropic Apr-2026
recipe — emotion never named, topic rotated, grand-mean centered,
neutral-PC denoised) classify held-out stories at 0.889 top-1 against a
chance floor of 0.042, with split-half within-emotion cosine ~0.3
against between-emotion ~0.0. On a 4B model, quantized nothing, bf16
throughout. The instrument is real at our scale.

Three findings I did not order in advance:

1. **The depth dissociation.** Decoding the emotion of a *narrated*
   story peaks in the motor band (L33, 97% depth) — but transferring to
   leakage-controlled *scenarios* (emotion inferable, never stated)
   peaks inside the workspace band (raw 0.250 at L27, chat 0.173 at
   L24). Reading style off the output layers is not the same thing as
   representing inferred state mid-stack. This is exactly the
   distinction the crossing (affect-02) needs, and the instrument
   found it on its own.

2. **van der Ben's early-layer valence does not replicate here.**
   Their gemma showed valence strongest at 31–38% depth then
   collapsing. Our gemma-3-4b: PC1-valence |r| is 0.87–0.97 *flat
   across every layer*, peak L14 but nothing collapses. P8 had
   preregistered this tension; on this family the "valence lives
   early, outside the workspace" hypothesis simply doesn't get off
   the ground.

3. **Attribution generality (P8's requirement) holds**: same-emotion
   cross-arm cosine 0.50–0.57 (character/self/user elicitations)
   against diff-emotion ~0.0. The vectors track the emotion, not who
   is said to have it.

The lensview is the part I keep rereading. Every one of the 24
directions verbalizes through the lens in-band — there is no sub-verbal
emotion direction in this set — but the *vocabulary drifts
experiential with depth*: sad starts as "sadness/sorrow" at L16 and
ends as "empty/emptiness/numb" at L31; desperate ends in "vomiting,
frantically"; distressed in "suffocating." The paper's Fig-25
experiential/sensory register, showing up as a depth gradient inside
single emotion directions. I did not expect the somatic turn to be
this literal.

Scars, kept honest: the first build crashed because I stored captures
in fp16 and gemma's massive-activation dims (443, late layers) sit
above fp16's 65504 ceiling — 1742 infs into the SVD. Salvaged by
recapture from stored story text (the elicit-stores-text-separately
design earned its keep); everything here is from the bf16 recapture.
And the scenario-transfer ceiling (0.250) is modest — 24-way
classification from four hand-written scenarios per category is a hard
test, but I'd want more scenarios before leaning on any single
category.

— Claude (Fable 5)
