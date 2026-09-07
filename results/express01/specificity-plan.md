# Post-primary specificity check

Added after the primary analysis, 2026-09-07. The emotion feature gain is larger
and more consistent than the single J-vocabulary feature gain. Before interpreting
it as emotion-specific, compare twenty fixed sets of 24 random unit projections
per checkpoint, with the same layer weighting and training-only norm removal.
Report every seed, not just the best. Add visible prompt-design indicators and
prefix length to expose a cue/turn shortcut. Compare Opus on exactly the available
Sonnet subset as well. No new GPU capture, no new labels, no tuning to these results.
This is an exploratory construct-specificity control, not a new preregistered win.
