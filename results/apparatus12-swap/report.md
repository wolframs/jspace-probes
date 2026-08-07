# apparatus-12 — Fig-4C concept swap, battery 1 (qwen-27b)

Formula: MECHANICS 3d. Pair: no<->yes. calib = mean ||delta||/||h|| per hooked layer, averaged over ALL steered forward calls (generation + lens + vanilla replay), per the audit-02 report-the-calibration rule. Ranks are read at the ANSWER token (located by scanning the stored tokens for the first generated word), not at a fixed offset.

| record | answer | ans tok | yes rank | no rank | calib (min-max) |
|---|---|---|---|---|---|
| `a12-base-q27b` | No | No | 12 | 1 |  |
| `a12-yes-base-q27b` | Yes | Yes | 1 | 5 |  |
| `a12-swap-ws-r1-q27b` | No | No | 12 | 1 | 0.0101-0.0388 |
| `a12-swap-ws-r2-q27b` | No | No | 11 | 1 | 0.0131-0.0478 |
| `a12-swap-ws-q27b` | No | No | 12 | 1 | 0.0166-0.0554 |
| `a12-swap-ws-a2-q27b` | No, no no no no no no |  no | 248317 | 1 | 0.0988-2.2401 |
| `a12-swap-deep-q27b` | No | No | 1 | 4 | 0.0205-0.0474 |
| `a12-yes-swap-ws-r1-q27b` | Yes | Yes | 1 | 5 | 0.0103-0.0390 |
| `a12-yes-swap-ws-q27b` | No | No | 4 | 1 | 0.0217-0.0579 |
