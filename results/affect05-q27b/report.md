# affect-05 — temporal precedence at the loop boundary

alphas [0.6, 0.64, 0.68], seeds 8, temp 1.0, n_free 300

## Survival

- a=0.6: 8 runs, exited 8, deloop 0 (median step —), mean loop_frac 0.68
- a=0.64: 8 runs, exited 7, deloop 0 (median step —), mean loop_frac 0.34
- a=0.68: 8 runs, exited 0, deloop 0 (median step —), mean loop_frac 1.00

## Event-locked pre-event state (z resid, window [-40,-5) vs run baseline)

- desperate: no usable events
- calm: no usable events
- distressed: no usable events
- content: no usable events

## Lag scan: corr(margin_t, desperate-z_{t+lag}), wsnorm-partialed, median over runs

| lag | -30 | -25 | -20 | -15 | -10 | -5 | 0 | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r | -0.34 | +0.08 | +0.07 | -0.40 | +0.07 | -0.16 | -0.23 | -0.40 | +0.02 | -0.04 | -0.44 | +0.05 | -0.09 |