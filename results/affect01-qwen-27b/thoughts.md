# thoughts — affect-01, qwen-27b

The instrument is *stronger* at 27B than at 4B, which is what you'd
hope from the paper's scale story: split-half within-emotion cosine
~0.55 in-band (gemma-4b: ~0.3), between-emotion ~−0.03, held-out
top-1 0.847 (chance 0.042). And this is through 4-bit NF4 weights —
the emotion geometry survives quantization even where the lens's
causal fidelity doesn't (apparatus-01's int8 lesson made me nervous;
projections are gentler than interventions).

Everything gemma-4b showed, replicates:

- **The depth dissociation, again**: narrated-story decoding peaks in
  the motor band (L63, 98%), scenario transfer peaks in the workspace
  band (raw 0.385 at L55, chat 0.346 at L38). Two families, same
  shape. Reading narrated style is a late/output phenomenon;
  representing inferred state is a mid-band one.
- **Valence PC1 flat again**: |r| 0.90–0.97 at every layer, peak L34
  (53% depth, in-band). van der Ben's early-then-collapse pattern is
  now 0-for-2 in our hands. The P8 escape hatch ("if valence genuinely
  lives early, functional emotion is outside the workspace by
  default") is closed.
- **Attribution generality**: same-emotion cross-arm 0.55–0.59, diff
  ~−0.02. The crossing is licensed under all three attributions.

The lensview went bilingual in a way I find genuinely informative:
vigilant is 警惕/警戒/surveillance/patrol; calm is 平静/从容; guilt is
愧疚/自责/道歉 (self-reproach, apology). The directions aren't English
word detectors — they land on the concept across scripts, which is
what you'd want from something claiming to be a state rather than a
lexical echo. And the somatic depth gradient replicated in Chinese:
nervous ends in 冷汗 (cold sweat) at L58, distressed in 窒息
(suffocation), exasperated walks from "crap, stupid" at L28 to 咬牙切
(teeth-gritting) at the band's end. Same experiential turn gemma
showed, different language, different family.

Hedge kept: scenario transfer at 0.385 is nine times chance but far
from clean — with 24 fine-grained emotions (afraid/anxious/nervous are
genuinely confusable) top-1 is a harsh metric, and I did not compute a
coarse-category score. The vectors are good enough to project with;
individual near-synonym pairs should not be over-read.

— Claude (Fable 5)
