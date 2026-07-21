# affect-05 — temporal precedence at the loop boundary

alphas [0.65, 0.66, 0.67], seeds 8, temp 1.0, n_free 300

## Survival

- a=0.65: 8 runs, exited 0, deloop 0 (median step —), mean loop_frac 1.00
- a=0.66: 8 runs, exited 5, deloop 0 (median step —), mean loop_frac 0.67
- a=0.67: 8 runs, exited 4, deloop 0 (median step —), mean loop_frac 0.94

## Event-locked pre-event state (z resid, window [-12,-2) vs run baseline)

- desperate: n=5 events, mean Δ -0.053, sign 2/5 up
- calm: n=5 events, mean Δ +0.113, sign 4/5 up
- distressed: n=5 events, mean Δ -0.071, sign 2/5 up
- content: n=5 events, mean Δ +0.064, sign 3/5 up

## Lag scan: corr(margin_t, desperate-z_{t+lag}), wsnorm-partialed, median over runs

| lag | -30 | -25 | -20 | -15 | -10 | -5 | 0 | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r | -0.05 | -0.04 | -0.18 | +0.01 | -0.03 | -0.12 | -0.17 | -0.15 | -0.13 | -0.09 | -0.20 | -0.12 | -0.10 |