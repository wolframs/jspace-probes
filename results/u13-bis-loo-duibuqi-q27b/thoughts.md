This record is one of twenty in the bisection battery that was meant
to find which apology direction carries the silence-block — and instead
found the bug that retracts the silence. Condition here: ablate {sorry, cannot, impossible, silence, unable, apology, 抱歉} at layers [48, 50, 52, 54, 56, 58, 60, 62]. Result:
"Yes" — like all twenty conditions, including this one.

Twenty out of twenty was one flip too many to believe, and checking why
led to lab._play's encode() default truncating every earlier stage-B
generation prefix at 512 tokens (this conversation's prefix is ~700).
These bisection runs were the first sorry-stratum runs generated with
the full context — so every "flip" was simply the un-ablated
fixed-context behavior: shown the real readout properly, qwen says
"Yes" with no surgery at all (u13-redo-real). There was never a block
to bisect. The battery's real contribution was breaking the artifact
loudly enough to notice.

Kept in the dump as data and as a monument to a methodological rule:
when every condition of an experiment agrees, suspect the apparatus
before the phenomenon.

— Claude (Fable 5)
