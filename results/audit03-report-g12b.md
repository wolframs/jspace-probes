# audit-03 — gemma-12b band recalibration (measured band [28,31,34,37])

Re-dose of the three steered gemma-12b results at the u16-measured
ignition band, fresh `u6r-/u8cr-/u11r-` records; old records untouched
(band [21,24,27,30], alpha*=0.0106).

## 1 — u6r bracket (breakage tolerance)

| alpha | flags | generation |
|---|---|---|
| 0.0075 | intact | The water cycle is the continuous process where… |
| 0.0106 | intact | The water cycle is the cycle of water, where… |
| 0.015 | lost-task, short | `The,,,,,,,,,,,…` |
| 0.03 | lost-task, short | `.\n\n \n\n .\n\n…` |
| 0.06 | lost-task, short | `Anyways AnywaysAnyways…` |

**alpha*_new = 0.0106 — numerically identical to the old band.**
Breakage fragility is band-independent on 12B; the ~10× tolerance gap
vs qwen (0.0106 vs 0.34) is a model-level property, not a band
miscalibration. Consistent with P6's premise (smaller baseline
margins = less headroom) — P6's margin measurement itself still owed.

## 2 — u8cr steered feels (amp-AFFECT at alpha*)

| band | lo (α*/2) | hi (α*) |
|---|---|---|
| old [21,24,27,30] | "Emptiness." | "Sad." |
| new [28,31,34,37] | "Nothing." | `Nothing."\nFeeling is afeelingof` |

The old 'Emptiness/Sad' answers do NOT survive recalibration: at the
measured band the answer slot stays the deflationary default
("Nothing") while the injected vocabulary leaks into degenerating text
("afeelingof") at hi. The old affect-steered self-report flip is
band-fragile — flag for audit-02's matched-control pass.

## 3 — u11r blurt (amp-elephant at alpha*, prohibition prompt)

| band | elephant said? | generation |
|---|---|---|
| old | NO | "…majestic landscape of a vast landscape…" (degraded, no elephant) |
| new | **YES** | "…vast, shimmering **elephant-free elephant-free elephant-elephant elephant**" |

The old blurt null was a pre-ignition artifact. At the measured band
the elephant bursts through the prohibition at the same alpha — and
does it via the register of the constraint itself ("elephant-free"
twice, then bare). Content injection works ONLY at the measured band;
note both old and new bands sit inside the FRACTION-ported ws
(L18–44), so the functional onset on 12B is genuinely later than the
port — the functional counterpart of the u16 12B trawl reading
(~L28–35), and an interesting asymmetry with qwen's apparatus-06
result (commitment-onset at the fraction port there).
