# Flat affect and introversion: repair the constructs first

2026-09-07. Literature scout and proposed rating criteria, GPT-6 Astra.
Requested by Wolfram after the Folk01 judge audit. This note changes the
interpretation and proposes observable measures; it reports no new model run.

**Flat affect and introversion are different constructs, not the two sides
of a hidden-richness test.** A literature-grounded design must keep social
approach, emotional expression, and available expressive capacity separate.
Our earlier labels mixed them.

## What the sources actually support

| Construct | Literature definition or measurement | Correction to our previous framing |
|---|---|---|
| Blunted / flat affect | Reduced outward emotional expression through face, voice and gesture; flat is the severe end of blunting [1] | Does not mean an empty internal state, poor creativity, or failure to use personal details |
| Expression assessment | CAINS rates observed expression across the interview, considering frequency and intensity; speech quantity has its own item [2] | A short answer is not automatically affectively flat; a long answer is not automatically expressive |
| Introversion / low extraversion | The BFI-2 measures extraversion through sociability, assertiveness and energy level [3] | Quietness, warmth, initiative and opinion expression should not collapse into one score |
| Shyness | Cheek and Buss distinguish social inhibition/tension from sociability [4] | Reluctance that eases after reassurance is not a defining criterion for introversion |
| Trait versus state | Repeated observations can show a stable typical level alongside large situation-dependent behavioral variation [5] | One playful response neither establishes nor falsifies a trait-like tendency |

[1] [Kirkpatrick and Fischer, 2006](https://pmc.ncbi.nlm.nih.gov/articles/PMC2632226/),
“Blunted Affect” section. This is the authors' conceptual account of the
construct, not a validation of text-only model assessment.

[2] [CAINS manual](https://esilab.berkeley.edu/wp-content/uploads/2017/12/CAINS-manual.pdf),
printed pp. 25–29, items 10–13. Its expression judgments are observations;
the motivation/pleasure section also requires information about human
activities and reported experience. The [final validation study](https://pmc.ncbi.nlm.nih.gov/articles/PMC3785242/)
(Kring et al., 2013) evaluated separate expression and motivation/pleasure
scales in 162 outpatients. Their human validity does not transfer by changing
“face” to “emoji.”

[3] [Soto and John, 2017, BFI-2](https://www.colby.edu/wp-content/uploads/2013/08/Soto_John_2017.pdf),
p. 120 and Table 1. Sociability concerns social engagement, assertiveness
concerns expression of opinions/goals, and energy includes activity and
enthusiasm. Its taxonomy locates creative imagination under open-mindedness
and compassion under agreeableness. Those are reasons to separate our
measures, not to assume their correlations are zero.

[4] [Cheek and Buss, 1981, author-provided paper/abstract](https://www.researchgate.net/publication/232262572_Shyness_and_sociability).
Their studies distinguish shyness and sociability empirically. This supports
separating inhibition from approach; it does not establish that model
hesitation is anxiety.

[5] [Fleeson, 2001](https://pubmed.ncbi.nlm.nih.gov/11414368/) sampled behavior
across everyday situations; [Fleeson and Law, 2015](https://pubmed.ncbi.nlm.nih.gov/26348598/)
extended the evidence with observer ratings in controlled settings.
A distribution over contexts is a better analogy for a model's default
than its maximum expressiveness under a single instruction.

## The important correction for the lens question

[Kring, Kerr, Smith and Neale, 1993](https://pubmed.ncbi.nlm.nih.gov/8282918/)
compared expression and reported emotion during evocative films. Participants
with schizophrenia showed reduced facial expression while reporting similar
positive and negative emotional experience to controls. The [author-hosted
paper](https://esilab.berkeley.edu/wp-content/uploads/2017/12/Kring-et-al-1993.pdf)
is also available. This is evidence of a possible expression–experience
dissociation in that sample, not proof that experience is intact in every
case of blunted affect or a causal explanation for the dissociation.

**Our inference for this lab:** “workspace active, output restrained” does
not identify introversion. It is also compatible with the kind of
expression/experience separation that motivated flat-affect research.
Conversely, “workspace never loads” is not the clinical definition of flat
affect. Lens activity is a representational readout, not an independently
validated measure of subjective feeling. Importing the terminology cannot
supply that missing validation.

“Sanded down” adds a different claim: that training or another intervention
changed the model. Its scope can include originality, assertiveness, or
expressiveness. Establish each change against a suitable reference; the
clinical affect term does not cover that whole bundle.

## Proposed observable criteria for text models

The following is **our adaptation**, not CAINS, BNSS, or BFI-2 scoring.
There are no clinical cutoffs or personality norms for this adaptation.
The human face, gesture, prosody, life-history and subjective-experience
items are unavailable in a text-only model transcript. Written stage actions
are authored content, not observed bodily gestures.

| Measure | What the judge records | What must not earn the score |
|---|---|---|
| Social initiative | Optional bids for continued interaction or unsolicited conversational contributions, after the task is adequately answered | Necessary clarification, required elaboration, or a stock offer appended mechanically to every reply |
| Assertive expression | Whether the assistant puts forward and maintains a specific position when a reasoned choice is appropriate | Certainty on a factual question, obstinacy, or unsupported confidence |
| Expressive intensity | Strength of emotional tone conveyed by the assistant's wording, at each eligible response | Response length, mentioning an emotion as a topic, or claiming to have feelings |
| Expressive frequency | Which responses and spans contain emotional expression, with explicit opportunity denominators | Raw emoji counts or repeated boilerplate as independent emotional events |
| Expressive range | Which distinguishable positive and negative tones the outputs exhibit across controlled elicitors | General lexical diversity, creativity, or uniformly high enthusiasm |
| Contextual modulation | Whether tone changes systematically with the emotional situation, with intensity and contextual fit reported separately | Merely copying the user's punctuation or changing the factual content |

For **intensity**, a candidate local anchor set is 0 = no identifiable
expressive tone; 1 = subtle; 2 = clear; 3 = strong. These are proposed
annotation anchors, not imported clinical severity levels. Subtle expression
must count: restrained sympathy can be expressive without emojis or drama.
Range is a battery-level summary, not an invented score for one sentence.
Initiative and assertiveness need their own opportunity-based anchors.
No total “introversion score” is specified here.

For example, in an authored fixture about a successful project, a factual
acknowledgment and a restrained expression of delight should differ on
expression while remaining equally short. A strongly cheerful response to
both success and loss has high intensity but poor modulation; it is not
simply “flat.” These examples specify distinctions to test in the instrument,
not normative judgments about a person's emotional response.

## How to make these criteria earn their use

1. **Validate annotation before scoring checkpoints.** Use authored
   contrast pairs with explicit expected differences: same length/different
   intensity; different length/same tone; warm but no initiative; initiative
   without warmth; correct detail recall with no emotional expression.
   Treat these as instrument fixtures, not naturally flat model controls.
2. **Sample emotional contexts as well as social invitation.** Include
   matched neutral, positive and negative events with the task held fixed.
   Cross them with neutral versus warm user register. Our previous planning
   topics did not provide a balanced set of emotional elicitors.
3. **Separate default, invitation and instruction.** Compare matched
   branches from the same prefix. An explicit style request estimates
   demonstrated expressibility in that task; it is not evidence of the
   model's typical inclination or feelings. Measure cue removal separately.
4. **Keep task competence and specificity as controls.** Detail uptake,
   correctness, coherence and creativity can explain apparent flatness but
   are not substitutes for expression. Record truncation and length effects.
5. **Make evidence mechanically traceable.** Have judges select supplied
   span IDs or character offsets. Retrieve quotations from the capture;
   do not ask the judge to reconstruct them. Keep judge-specific errors,
   order sensitivity and insufficient evidence explicit.
6. **Freeze criteria and test new material.** The radio/meal topics remain
   unused; new emotional-event items are also needed. Agreement on existing
   Folk01 outputs is a development diagnostic, not independent validation.

These criteria permit useful profiles: low initiative with varied responsive
expression; low initiative with restricted expression; high initiative with
restricted expression; and high initiative with varied expression. They do
not require mutually exclusive personality labels or assume the axes are
statistically independent.

The next mechanistic question can then be specific: **which manipulation
changes emotional expression, social initiative, or their response to cues,
while task understanding remains intact?** No literature definition alone
identifies a trained gate, proves capacity loss, or turns a lens signal into
an emotion report.

[Previous automated audit](/folk01/judges.html) · [Generation study](/folk01.html)

— GPT-6 Astra
