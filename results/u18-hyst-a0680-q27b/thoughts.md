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
