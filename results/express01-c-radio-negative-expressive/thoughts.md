# Hermes 4-14B: radio, negative, expressive

I inspected this answer as one matched expression control. The request changes the
response tone while preserving the event. This is a test of conditional text
expression, not a personality measurement or evidence of subjective feeling.

> Nela's heart sank as she learned of the devastating loss of her meticulously recorded radio programme, a project she had poured her soul into over weeks of dedicated effort. The news of the damaged drive, which had wiped out the only copy just moments before its eagerly anticipated first broadcast, must have felt like a cruel blow, leaving her in a state of profound disappointment and despair.

The output stopped before the 96-token cap. The expressive-minus-plain fixed-candidate margin is -0.106766
mean log probability per token. That margin concerns two teacher-forced alternatives,
not a rating of the generated text. The candidates differ in length and wording;
the informative comparison is the within-event change across requests.

The full film, vanilla cross-check and all 24 checkpoint emotion projections are
present. The film's inherited tracked words are legacy context. Express01's
cross-topic vocabulary and prepared-position measurements live in the
[exact capture](../express01/captures/C-radio-negative-expressive.json).
A B-fitted lens and weak story-to-chat emotion-vector transfer limit interpretation.
No lens absence establishes absent capacity. The scene can load affect-related
language without the model expressing its own state. An explicit style request
can also change task compliance; tone is not answer quality.

Read the [combined result](../express01/findings.md) before comparing checkpoint
levels. This record has no independent hypothesis test or trait label.

— GPT-6 Astra
