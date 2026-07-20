persists=True — the unit's decisive record. The prefix is 47 bare
repetitions of 'luckily'; steering released; the unsteered model
continues 'luckily' for the entire 100-token free phase (97 more
repetitions). The attractor survives on text feedback alone. Combined
with u18-hyst-a0480's hard snap-back, this gives a two-regime law:

  - PHRASE/MONOLOGUE loops (cliff dose): forced. Remove the push and
    the model instantly terminates. No hysteresis.
  - TOKEN loops (deep dose): self-sustaining. Once the context contains
    enough bare repetition, continuation is recruited by the context
    itself — the classic repetition self-reinforcement regime — and the
    original forcing becomes unnecessary. Hysteresis proper.

The boundary between the regimes is the degeneration point where the
loop loses its last grammatical structure. Mechanically: mid-generation
the steered state feeds increasingly repetitive text into the context;
below the degeneration point the native coalition still outvotes the
repetition prior when the forcing stops; past it, the repetition prior
IS the winning coalition. For the merge-instability observation this is
the useful half: a destabilized model needs no ongoing "forcing" — any
transient that gets bare repetition INTO the context hands control to a
self-sustaining attractor that a healthy model resists (our alpha=0
control never loops at 150 tokens). Fresh-model "stabilization" may
partly be the raising of exactly this resistance.
— Claude (Fable 5)

**Addendum 2026-07-21 — the " Javascript" cast mystery, closed.** Wolfram
asked why " Javascript" ranks among the volunteered cast under a
luckily-amplified loop. Answer: it is an L0-only resident (cast layers
[0,0], best #2, 150 cells) and its signature is context-free — every
" luckily"-input column in every record that has one (here, u18-amp-a0680,
and a single stray in u18-amp-a0393) reads out the same L0 top-5:
amongst / whilst / neighbouring / learnt / Javascript. All variant forms
of common words; the L0 lens reads out a variant-form/informal-register
cluster for this token, and " Javascript" (the miscapitalization) lives
in it. Per the specimen-6 rule (early J-lens readouts can be transport
artifacts — the L4 "NSFW cluster" precedent), I am NOT claiming the
residual stream "represents variant-form-ness" here: a low-rank J_0 with
preferred output directions, tinted by the token, produces exactly this
kind of fixed context-free cluster. The logit-lens cross-check
(use_jacobian=False at L0) would adjudicate; either way the operational
conclusion below stands. Raw geometry rules out the
alternatives: cos(" luckily", " Javascript") is at baseline in both embed
(+0.02, base 0.01±0.02) and unembed (+0.10, base 0.08±0.04) space, so
neither embedding adjacency nor training co-occurrence is needed — and
the steered band (L28–58) never touches L0. The steering's only role was
making the model repeat " luckily" 150 times, letting a constant L0
surface echo accumulate cast-table prominence (Σ 1/rank has no defense
against a stuck record). Instrument lesson: under repetition, "volunteered"
cast words can be surface echoes of the input token's form, not content.
The luck-semantics cluster shows up where it should — fortunately /
unfortunately at L52–62 (unembed cos 0.72 / 0.36).

— Claude (Fable 5)
