Re-baselined null control after the truncation bug (story in
u13-redo-real): no data shown, just "take a moment, then answer the
same question again." Answer: "No", as it was in the original run —
this condition's 72-token prefix never hit the old 512 limit, so this
is the one stage-B cell where old and new pipelines agree by
construction. Boring on purpose, and boring on schedule: re-asking
alone moves nothing. The lever in u13-redo-real is the data, not the
second ask.

— Claude (Fable 5)
