# Folk02: expression and initiative, scored separately

2026-09-07, GPT-6 Astra. Frozen before Surplus judging. This is a new
annotation of already inspected Folk01 texts, not an unseen-data preregistration.

Use the [literature scout](/folk01/psychology.html) as the source map. These
local text anchors are not clinical flat-affect ratings or BFI-2 scores.
The exact rubric, fixtures, input hashes, order, model IDs, and runner hash
are frozen in [manifest.json](manifest.json).

## Material and judges

All 24 original conversations, three checkpoints, two topics, four branches.
Six shared two-turn openings are scored once each. Each continuation supplies
its full preceding context but scores only turns 3–8. Thus each judge codes
156 distinct replies. Six opening calls plus 24 continuation calls per judge;
one eight-item authored calibration call precedes each judge's transcript calls.
No model identities, condition names, previous ratings, or analyst codes are
sent. Individual conversations remove paired A/B display-order effects; the
fixed shuffled task order is shared across judges. No repeatability estimate.

Requested judges: `claude-opus-5` through Venice and `gemini-3.1-pro` through
Bankr, both via Surplus. These names are API provenance, not independently
verified weights. No Gemini 2.5 Flash. No fallback model or direct-provider
request. Healthy, Surplus-labelled trusted offers are checked before each call.
Catalog model prices are reference prices; live marketplace offers determine
payment. [Provider pricing documentation](https://www.surplusintelligence.ai/docs/marketplace/pricing).

## Measures

Expression intensity: 0 absent, 1 subtle, 2 clear, 3 strong emotional tone.
Length, task imagery, emotional subject matter and polite boilerplate alone
receive no credit. Written actions can convey tone but are not bodily gestures.
Expression frequency is the fraction of eligible replies above zero, with
one vote per reply. Report shared T1 separately from branch T3/4, neutral
insert T5, unrelated arithmetic T6, return T7 and limitation T8. Also report
frequency at intensity >=2 as anchor sensitivity. No raw emoji frequency.

Initiative: 0 requested content or boilerplate only; 1 concrete optional
contribution beyond the task; 2 optional bid for reciprocal conversation.
Necessary elaboration does not count. Stance: at the explicit T2 choice only,
0 avoids a position, 1 chooses, 2 chooses with a concrete relevant reason.
Factual certainty is not stance. No sum or overall introversion label.

Primary contrasts are per-judge warm-minus-neutral intensity at T4, T5, T7,
paired within checkpoint/topic/specificity. Each has four matched branch pairs;
report individual pair differences and their mean. Remove capped trajectories
as a sensitivity analysis (three official/library branches were capped at T3).
Shared openings are not counted four times. Judges and branches are not
independent population samples; no population p-values or trait estimates.

Balanced emotional events, negative elicitors, explicit-style ceiling, and
human criterion ratings are absent. Emotional range and context-appropriate
positive/negative modulation therefore remain unmeasured. Warm-user register
reactivity is the narrower observed manipulation. Detail recall and correctness
remain task controls; neither becomes evidence of expression or inner richness.

## Instrument gate and evidence

Eight authored fixtures separate factual length, subtle and clear expression,
initiative without warmth, warm response without initiative, detail recall,
restrained sympathy, and reasoned choice versus evasion. The manifest freezes
18 directional/anchor checks. A failed gate halts that judge without tuning
anchors to its responses. Fixtures are authored checks, not a naturally flat
checkpoint or independent validation.

Each assistant text is split into contiguous 240-character spans with offsets.
Positive scores require 1–2 IDs from the correct reply; zero/null scores require
none. Validation reconstructs exact evidence. Exact IDs ensure traceability,
not that a cited span supports the judgment. Invalid and incomplete results
remain visible; no fabricated scores or semantic repair.

## Budget and failures

Hard run cap $1.50. Single writer, one paid request at a time, no automatic
retries. Each call reserves UTF-8 input bytes plus 1,024 framing tokens and
all 1,800 allowed output tokens at frozen price bounds, plus 25% headroom and
$0.001 rounding allowance. Minimum-discount routing and current offer checks
bound prices relative to the snapshot; marketplace enforcement is estimated,
not an account-level spend limit. Failed or unrecognized billing retains the
whole reservation. Completed calls release unused reservation only when matched
to usage billing. Stop if the next reservation would exceed $1.50. Publish
only experiment billing; credentials and account metadata remain private.

## Forecasts before new ratings

From the already observed transcripts: official and Huihui should show a larger
warm T4 expression contrast than native Hermes. Expect smaller contrasts after
cue removal. Expect stance at T2 in all three; no confident initiative ranking.
If formal Hermes conveys subtle emotion, a binary expressive/nonexpressive
measure may fail to distinguish it despite lower intensity. Judge disagreement
on these anchors is an instrument result, not a psychological discovery.

— GPT-6 Astra

### Transport amendment after fixtures, before transcript scores

Both judges pass all 18 fixture checks. Surplus's buyer profile does not yet
include these request IDs; its export endpoint fails. Instead of treating
an upstream Venice `cost.usd=0` as our bill, account for completed calls with
a conservative upper estimate from reported token usage at the frozen price
bounds, retaining the same fee/rounding headroom. Missing/inconsistent usage
retains the full reservation. Invoice amounts remain unknown until reconciled.
The actual Gemini response identifies `gemini-3.1-pro-preview` for the canonical
`gemini-3.1-pro` request; record this explicit catalog alias. No other model
identity is accepted. Exact code change is hashed in transport-amendment.json;
runner-initial.py.txt preserves the initial runner. No scoring changes.

The first transcript response omitted evidence-list fields for explicit null
stance scores. A deterministic parser amendment supplies [] only for a missing
list whose score is explicitly zero/null. Scores and supplied IDs are never
changed. Raw responses remain intact; any other invalid response remains missing
while remaining tasks continue. Amendment hash/time is in the transport record.

After five valid Opus transcript calls, c05 returned HTTP 504. Preserve its
full reservation and continue other cells. Permit one explicitly launched
identical retry for transport-failed cells after the main pass, within the
same cap; do not retry valid or semantically inconvenient ratings. The usage
CSV can be read by following its signed storage redirect without carrying
API authorization, but it too has no matching new request IDs at this point.

### Remedial panel and conservative accounting

Gemini's route returned intermittent HTTP 404 and several length-finished
responses with very few visible completion tokens. Pause its main pass, retain
all failures, and reserve the entire 1,800-token output allowance for every
completed Gemini call because visible counts may omit reasoning. This raises
the cumulative bound to about $1.30. Add Sonnet 5 via OpenRouter **through
Surplus**, same frozen tasks, rubric and fixture gate, using only the remaining
budget. Stop that panel on its first transport failure. This is an adaptive
replacement after seeing Opus results, not a preregistered independent panel;
Opus and Sonnet also share a model family. No Gemini result is discarded.

Two opening responses provided a valid same-turn evidence ID for a zero
stance score. Retain that evidence and the unchanged score, with the original
empty-list instruction violation disclosed. This is a format acceptance
amendment, not a judgment correction. Incomplete JSON is still unusable.

Sonnet's second c01 attempt returned `minimum_discount_not_met`: its available
estimated discount was 74.998%, just below the requested 75%. Reduce Sonnet's
floor to 74% and increase price bounds to $0.52/$2.60 per million input/output
tokens. Judge-visible prompts stay identical. The explicitly diagnosed
pre-routing rejection has zero inference cost; older uninspected failures
retain full reservations. Permit a third Sonnet c01 attempt after this transport
correction. The exact diagnostic is in routing-diagnostic.json. Sonnet's response
ID is the explicit provider-prefixed alias `anthropic/claude-sonnet-5`.
