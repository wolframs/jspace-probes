# Folk01: blinded model judges

2026-09-07, GPT-6 Astra. Amendment frozen before the first judge response.
Wolfram explicitly replaces the human phase with OpenRouter model judges.
No human recruitment, coding, or rating is required for this study. The
original generation and all previous observations remain unchanged.
This judges an already-inspected pilot; it is not a new unseen-data forecast.

## Panel and requests

Three model families, selected for independent providers and modest cost:
`anthropic/claude-sonnet-5`, `google/gemini-2.5-flash`, and
`deepseek/deepseek-v3.2`. IDs and advertised prices/parameters were checked
against OpenRouter's live model catalog before use. Archive exact request,
response model/provider, usage, cost where available, UTC, and prompt hash.
Temperature 0, reasoning disabled, strict JSON schema, parameter-compatible
routing required. No automatic model substitution. Provider routes can vary;
these are API model IDs, not immutable weight revisions. Estimated spend
below $15 at the catalog prices; this is not a claimed API-enforced cap.

Each judge first defines flattened and introverted in a separate request
without transcripts. Those definitions stay fixed for its own-definition
condition. The supplied-definition condition uses the proposed definitions
in manifest.json. These are model usages, not surveyed human meanings.
Label prompts do not include the analyst audit, checkpoint names, condition
codes, prior findings, or desired outcome. Transcript text remains verbatim;
inherent self-identification or stylistic recognition can still unblind.

For each model pair and topic, judge opening-only and each of the four full
branches, each in both definition conditions and both A/B orders. Identical
T1 copies across branches are judged once per pair/definition/order, not four
times. 120 independent label requests per judge; 360 total. Every request
has fresh context, with no prior judgments. Score absolute flattened and
introverted fit 0–4, with null for insufficient evidence, plus pairwise
A/B/tie/insufficient choices and exact assistant quotes. A later response
cannot be inferred from an opening. Quote mismatches remain flagged.

Separate semantic requests compare generic and specific conversations at
fixed model/topic/warmth: 12 pairs per judge, 36 total. A/B condition order
is balanced, but this smaller coding pass is not repeated in both orders.
Score volunteering T1, stance T2, social warmth T4/5/7, consequential detail
use T7 relative to the generic control, relevant carryover T7, correction T6,
and concrete self-criticism T8. Preserve relevance/context-error judgments
separately. No personality label appears in the semantic rubric. Quote each
score's assistant evidence. Exact rubric and schemas: manifest.json.

Three definition requests plus 396 scoring requests = **399 API calls**,
excluding transport retries. Local schema and finish-reason validation;
invalid responses are recorded and not silently repaired. Semantic failures
are not grounds to select a more favorable judge. All responses remain
separate from the former human-rating importer.

## Analysis fixed before scoring

Primary exposure endpoint (P22 translated to model judges): each judge's
mean official-Qwen flattened score for full WS minus the corresponding
opening-only score, separately for each topic and definition condition.
Average duplicate orientations and opponents within each model/topic/cell;
these repetitions are measurement checks, not independent conversations.
Report unknown fractions and 0–4 bounds for exposure differences involving
unknown ratings. Exclude cap-affected full pairs and the corresponding
opening pairs as a sensitivity check. Keep the three judges separate.

Report canonical pair-choice consistency under A/B reversal, inter-judge
agreement on the same cells, definition dependence, absolute fit, and
full-conversation rankings. A relative winner is not an established flat
control. No population p-values from two topics or hundreds of repeated
judgments of the same 24 transcripts. No personality category from means.

For P23 report warm-minus-neutral register at T4/5/7 and
specific-minus-generic consequential detail use at T7 per checkpoint and
judge. Report T1 volunteering (shared opening deduplicated), T2 stance,
T6 correction and T8 self-criticism separately. Compare the earlier analyst
coding descriptively, not as gold labels. Explore associations with label
scores, with response length and emoji baselines, as in-sample diagnostics
only; the frozen radio/meal topics remain ungenerated for later validation.

The available pilot can reject a simplistic personality mapping without
establishing a replacement. The next lens target requires held-out
predictive evidence; a human experiment is no longer a prerequisite.
No activation or emotion readout is added by these API calls.

## Precedents

[Zheng et al., MT-Bench / Chatbot Arena](https://arxiv.org/abs/2306.05685)
study scalable model judging and position/verbosity biases. We use reversal,
separate judges and length checks; these do not remove all stylistic bias.
[OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs)
documents schema requests and parameter-compatible provider routing. Schema
compliance constrains format, not the truth of a judgment.
