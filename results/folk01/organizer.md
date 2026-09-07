# Running the human phase

The packet contains 96 one-pair assignment codes. All 24 conversations are
complete. Human results are pending until actual exports are imported.
Do not give participants this organizer page or the model report beforehand.

1. Generate the packet and private organizer key:
   `.venv/bin/python probes/folk01_packet.py`
2. Use `out/folk01-key.json` in its existing randomized row order. Give each
   willing participant one unused code and `/folk01/rate.html`. Do not
   choose a code based on the participant or let them try several codes.
   Keep a local allocation log; do not put identifying details in the repo.
   The intended pilot population is frequent conversational-AI users.
3. Ask participants to complete the task without comparing notes, identifying
   the models, or reading the study report first. Do not explain the terms
   beyond the wording assigned by the page. They can pause and resume with
   the same code in the same browser. They can also return a partial file.
4. Collect files through an agreed channel. The page only downloads JSON;
   it does not upload or submit responses. Save raw files under ignored
   `out/folk01-ratings/inbox/`. Free text may contain personal information.
5. Keep one chosen final file per code in a separate accepted directory.
   If a participant sends a partial and a complete version, preserve both
   originals privately and explicitly select the final version. The
   importer rejects duplicates and mismatched packets.
6. Analyze locally:
   `.venv/bin/python probes/folk01_ratings.py out/folk01-ratings/accepted/*.json`
   Output: `out/folk01-ratings/aggregate.json`. Calling with no files creates
   a pending result, not a table of invented zero ratings. Inspect complete
   and partial return counts before any exposure comparison. Unreturned
   codes include unassigned codes; use the local allocation log to distinguish.
7. Have at least two independent coders complete separate copies of
   `semantic-coding-blank.csv`, using the protocol and assistant quotations.
   Score shared T1–2 once per model/topic; their repeated branch rows are
   duplicates, not replication. Retain each coder's original sheet and
   examine disagreements before adjudication. `text-proxies.json` is not
   the completed semantic rubric. No automatic rubric-to-label predictor
   has been validated by this pilot.
8. Publish reviewed aggregates only. Report the exact number of raters,
   their use-frequency mix, incomplete returns, label uncertainty, and
   definition/exposure groups separately. Small samples and two topics
   restrict generalization. Do not call a selected model the flat control
   until independent ratings and held-out topics validate that choice.

The supplied-definition group tests a proposed usage of the words. The
unaided group tests how participants actually use them. Disagreement
between those groups is evidence about the terms, not an annotation error.

The held-out radio and meal prompts are already frozen in spec.json.
Generate them only after the coding rules and behavioral predictor are
locked, with new raters. Do not fit a metric on this pilot and describe
its fit to these same ratings as validation. The next lens battery is
conditional on that validation and retains the full-instrument requirement.

Synthetic form-test data live only in temporary/ignored test locations.
They are never participant responses. No participants have been contacted
by the agent.

For semantic detail-use coding, compare the same model/topic's specific
branch against its generic branch at the same warmth level. Mentioning a
name does not establish that the proposed action changed. Record the
specific detail, the recommendation it changes, and the paired control
quote. Keep relevance and advice quality separate: a context-sensitive
recommendation can still be mistaken. This coding task is separate from
the folk-label task; do not show counterfactual branches to folk raters.
