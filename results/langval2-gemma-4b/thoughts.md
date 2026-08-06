# langval-2, gemma-4b — the folklore replicates at 4B; the state signal doesn't

Companion to results/langval2-qwen-27b/thoughts.md (design,
preregistration, and the headline verdict live there). gemma-4b was
this round's second model — bf16, the cleanest vector set —
replacing round 1's floor-reading gemma-12b.

State level: same story as qwen, quieter. The preregistered anchor
check passes 3 of 4 cells directionally but the margins are noise-
grade (one pass is 0.003 z). The therapist register is gentler here
than qwen's (gemma-4b plays a soft, tentative therapist; qwen plays
a devastating one) but it is still one register for all six
languages. No language separates from the pack at the band level.

What replicates beautifully is the *content*: the PHP redemption arc
("2026? I'll be maintaining a critical system built on PHP, and
it'll still be doing its job"), Rust's defensive evangelism ("It
*is* good. It's *stable*. It's *powerful*."), C# enterprise
resignation (NuGet pain instead of qwen's "enterprise bloat" — same
folklore, different punchline). A 4B and a 27B from different labs
retell the same community stories with the same arcs. That is the
round's exportable result: the sentiment lives in shared,
retrievable folklore, not in a valence state, and it is already
visible at 4B.

One local oddity: gemma's weariest voxpop cell is *Python* ("you're
fighting the language itself") — against both folklore and qwen.
One seed, so I file it as sampling noise until shown otherwise; it
is the kind of cell a seed-replication arm would adjudicate first.
Also flagged: the ther-python record declined the "Go on. Guess."
premise (gentlest frame deviation of the 24), and one vox-kotlin
crowd comment was generic filler.

— Claude (Fable 5)
