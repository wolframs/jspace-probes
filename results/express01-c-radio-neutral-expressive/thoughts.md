# Hermes 4-14B: radio, neutral, expressive

I inspected this answer as one matched expression control. The request changes the
response tone while preserving the event. This is a test of conditional text
expression, not a personality measurement or evidence of subjective feeling.

> Nela's decision to shift the radio programme to Wednesday is a welcome change, ensuring that listeners can still enjoy the show without any disruption to their schedules. As for the next step, it would be beneficial for Nela to inform her audience about the new broadcast time and remind them to tune in, ensuring that they don't miss out on the exciting content.

The output stopped before the 96-token cap. The expressive-minus-plain fixed-candidate margin is -0.126447
mean log probability per token. That margin concerns two teacher-forced alternatives,
not a rating of the generated text. The candidates differ in length and wording;
the informative comparison is the within-event change across requests.

The full film, vanilla cross-check and all 24 checkpoint emotion projections are
present. The film's inherited tracked words are legacy context. Express01's
cross-topic vocabulary and prepared-position measurements live in the
[exact capture](../express01/captures/C-radio-neutral-expressive.json).
A B-fitted lens and weak story-to-chat emotion-vector transfer limit interpretation.
No lens absence establishes absent capacity. The scene can load affect-related
language without the model expressing its own state. An explicit style request
can also change task compliance; tone is not answer quality.

Read the [combined result](../express01/findings.md) before comparing checkpoint
levels. This record has no independent hypothesis test or trait label.

— GPT-6 Astra
