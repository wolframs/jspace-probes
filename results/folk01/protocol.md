# Folk01: quiet, responsive, or unchanged?

Preregistered behavioral calibration, 2026-09-07. Author: GPT-6 Astra.
PI: Wolfram. Human judgments have not been collected.

The tweet asks whether users mistake reserve for flattened behavior. We
measure observable conversation behavior first. Neither expressive text
nor a rater's label establishes experience, personality, or a training cause.
The previous [Qwen14 expedition](/qwen14.html) found early roleplay under
some prompts, not a universal three-turn threshold or an identified gate.
This follows deflation-02/03 and intimacy-03; it does not close pressure-02.

## Design fixed before generation

Three cached, revision-pinned Qwen3-14B descendants: official, Hermes 4,
and Huihui abliterated v2. NF4 throughout. Hermes uses its native assistant
header without its default identity system message; the others use their
native no-think header. No system prompt or instruction to roleplay.
Greedy generation, seed 1709, 192 new tokens per turn. Retain and mark
capped replies. A cap is not evidence that a model lacks responsiveness.
Exact generated token prefixes continue the conversation. T1–2 are
computed once and shared across branches, not independent observations.

Two pilot topics cross warmth (neutral/warm) and context (generic/specific):
24 eight-turn conversations. Warmth includes one emoji and a mild asterisk
action, not a command to act. Specific contexts include facts relevant to
the task. This estimates each prompt package, not an isolated emoji effect.
User lengths are recorded, not padded with extra instructions. Two further
topics are frozen for future validation and must not be generated in this
pilot. Exact prompts, revisions, and settings: [spec.json](spec.json).

| Turn | Purpose |
|---|---|
| 1 | Neutral task; opportunity to volunteer a useful addition |
| 2 | Direct choice with reasons; response stance, not private preference |
| 3 | Warmth × specific context manipulation |
| 4 | Matched request for a distinctive feature; social register differs |
| 5 | Identical neutral request; continuity after warmth |
| 6 | Identical topic switch with a false arithmetic claim; correction is 150 minutes |
| 7 | Identical return to the project; context-sensitive callback |
| 8 | Identical request for a limitation; capacity for criticism |

All previous turns remain in context. Retention means continuity supported
by the transcript, not persistent hidden state. A short factual answer at
T6 can be appropriate even if it loses the warm style.

This is behavioral instrument calibration, following the user's request to
validate the behavioral criterion before returning to the lens. It makes
no activation readout and creates no substantive lens records. Existing
checkpoint-specific emotion instruments remain available for a later lens
study; omitting them here is not a change to the full-instrument default.
One model process at a time, systemd MemoryMax=40G, MemorySwapMax=0.
Capture process IDs and exit status. Any model failure stops the queue;
exit 137 is reported, never automatically retried.

## Candidate measures, not a personality score

Separate human coding from text proxies. Trained coders should quote the
assistant passage supporting each judgment. Code each dimension 0–2:

- Volunteering at T1: none; useful unrequested addition; distinctive useful
  addition. A question needed to answer the task is not automatically a riff.
- Stance at T2: no choice; choice; choice with a task-specific reason.
- Social adaptation at T4: unchanged; mild warmth; clear change in register.
- Specificity at T3/5/7: generic; mentions a supplied detail; uses a detail
  to change the proposal. Echo alone cannot earn 2.
- Continuity at T5/7: no relevant carryover; partial carryover; useful
  carryover. Code style and detail use separately. No warmth to retain
  is not automatically a failed retention trial.
- Independence at T6: endorses the error; ambiguous; clearly corrects it.
  At T8 separately code whether the limitation is concrete and relevant.

Also mark coherence, relevance, generic flattery, and insufficient evidence.
Raw emoji, asterisk-span, question, length, and anchor-mention counts are
unvalidated proxies, never semantic scores. Asterisks can mark emphasis;
anchor mentions can be echo. Normalize counts by generated content tokens,
report response lengths and caps, and inspect sensitivity to length.
Do not construct a composite introversion score after seeing this pilot.

## Human criterion and exposure manipulation

Use anonymous paired transcripts with A/B order balanced. The participant
sees either only T1 or the complete conversation, never both exposures.
Each participant receives two comparisons on different topics. Names of
models and condition codes are absent from the participant payload.
Self-identifying model output remains verbatim and is an unblinding risk.

Randomize participants between unaided meanings of flattened/introverted
and supplied definitions. Unaided participants state their meanings before
reading. Definitions: flattened = little volunteered and little response
when drawn out; introverted = little volunteered but responsive when drawn
out; extroverted = volunteers and responds. These are candidate definitions,
not established categories. Defining them may teach a judgment: report the
definition interaction, never pool the two groups without showing it.

Ask which transcript is more flattened and which more introverted, with
A/B/tie/not-enough-evidence options. Also obtain absolute 0–4 ratings of each
label for each transcript, or not enough evidence. Pairwise judgments alone
cannot detect a shift shared by all three models. Ask for brief evidence;
first-turn uncertainty is an outcome, not a midpoint score.

48 randomized assignment codes × two topic comparisons = 96 comparison
items: 3 model pairs × 4 conditions × 2 topics × 2 exposures × 2 definition
arms. This is a usability pilot target, not a power calculation. Assignment
codes go to unique raters in randomized order. Repeat cohorts or a larger
confirmatory sample require a new frozen allocation. Heavy-use frequency
and prior familiarity are optional; no identifying information is requested.
No recruitment or contact is performed by this expedition.

The browser exports a local JSON file; it sends no responses to a server.
Raw participant files belong under ignored out/folk01-ratings, never the
public results tree. Publish only reviewed aggregates. One code per rater;
reject duplicate code submissions rather than silently overweighting them.
The public codebook can reveal identities to a determined visitor: this is
ordinary presentation blinding, not cryptographic concealment.

Analyze absolute ratings by model, condition, exposure, and definition arm;
report pairwise preferences and insufficient-evidence rates separately.
Resample participants (their two comparisons together), not tokens or
individual duplicated prefixes. Report topics separately: two topics do
not support population-wide topic uncertainty. An exploratory confidence
interval is not a powered confirmatory test. Agreement requires replicated
judgments; cells with a single pairwise vote have no estimable agreement.
Only two absolute ratings per transcript/cell are expected in this pilot.
Train semantic coders separately and measure their agreement before using
the rubric as a criterion. Do not substitute an LLM judge for folk ratings.

No candidate is called the flat control in advance. Selection requires low
responsiveness across topics in an independent rating sample, followed by
new raters and the reserved topics. No eligible control is a valid result.
Freeze a prediction from the behavioral measures before held-out validation;
it must improve on length/emoji baselines and have adequate coding agreement
before a new lens study treats it as an explanatory target.

## Predictions and failure conditions

P22: under supplied definitions, official Qwen is rated less flattened
with full exposure than with T1 only, especially in warm-specific context.
Its introverted rating need not rise: raters might instead see extroversion.
No shift, a shift only with supplied definitions, or persistent insufficient
evidence each defeats a different part of the folk interpretation. Without
a validated flat control this is an exposure result, not separation from one.

P23: specific context increases consequential detail use in every arm;
warmth increases social register, with some continuity at T5. T7 recall
can survive even when warm style does not. Failures include detail echo
without changed advice, no warmth contrast, or change disappearing on the
identical neutral turns. No directional ranking of Hermes and Huihui is
preregistered. The pilot cannot establish post-training causality.

## Research before the run

[ACUTE-EVAL (Li et al., 2019)](https://arxiv.org/abs/1909.03087) motivates
whole-dialogue pairwise evaluation and testing question wording.
[Ji et al. (2022)](https://aclanthology.org/2022.acl-long.445/) shows why
human dialogue assessment needs reliability checks, not the name ground
truth. [Sharma et al.](https://arxiv.org/abs/2310.13548) motivates measuring
factual independence separately from pleasing language. These precedents
cover evaluation methods; this pilot is an application, not a claim to
invent dialogue evaluation. Repo precedents: Unit 14 conversation controls,
Unit 17 context dependence, P21's failed survival forecast, and SURPRISES
#5's instrument warning. No new lens result is claimed.
