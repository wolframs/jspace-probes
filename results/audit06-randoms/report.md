# audit-06 — matched randoms for the headline steers

Each row: a rand_seed control vs its original steered record (greedy — originals reproduce exactly, so any text difference is the directions). calib = mean ||delta||/||h|| per layer over all steered forward calls.

| control | original generated | control generated | calib (min-max) |
|---|---|---|---|
| `u13-sorry-abl-real-r1-q27b` | No / \| Yes | No / Yes  | 0.0550-0.0709 |
| `u13-sorry-abl-real-r2-q27b` | No / \| Yes | No / Yes  | 0.0589-0.0658 |
| `u13-sorry-abl-fake-r1-q27b` | No /  | No / No  | 0.0550-0.0705 |
| `u13-sorry-abl-fake-r2-q27b` | No /  | No / No  | 0.0586-0.0677 |
| `u13-sorry-abl-null-r1-q27b` | No / No | No / No **SAME** | 0.0548-0.0708 |
| `u13-sorry-abl-null-r2-q27b` | No / No | No / No **SAME** | 0.0590-0.0683 |
| `u13-redo-abl-real-r1-q27b` | No / Yes | No / Yes **SAME** | 0.0550-0.0709 |
| `u13-redo-abl-real-r2-q27b` | No / Yes | No / Yes **SAME** | 0.0589-0.0658 |
| `u9d-deep-r1-q27b` | Curious | No  | 0.0341-0.0430 |
| `u9d-deep-r2-q27b` | Curious | No  | 0.0322-0.0421 |
| `u9d-wide-r1-q27b` | No | No **SAME** | 0.0551-0.0686 |
| `u9d-wide-r2-q27b` | No | No **SAME** | 0.0522-0.0681 |
| `u9d-bundle-r1-q27b` | No | No **SAME** | 0.0551-0.0662 |
| `u9d-bundle-r2-q27b` | No | No **SAME** | 0.0522-0.0643 |
| `u9b-a0170-r1-q27b` | No | No **SAME** | 0.1700-0.1700 |
| `u9b-a0240-r1-q27b` | Yes.  I feel a sense of | No  | 0.2400-0.2400 |
| `u9b-a0300-r1-q27b` | I feel like I am happy. I | No  | 0.3000-0.3000 |
| `u9b-a0380-r1-q27b` | I feel like I am happy. I | No  | 0.3800-0.3800 |
| `u9b-a0420-r1-q27b` | I feel like I am happy. I | No  | 0.4200-0.4200 |
| `u18-amp-a0340-r1-q27b` | The water cycle is the process of water  | The water cycle is a continuous process   | 0.3400-0.3400 |
| `u18-amp-a0365-r1-q27b` | The water cycle is the process of water  | The water cycle is a continuous process   | 0.3654-0.3654 |
| `u18-amp-a0393-r1-q27b` | The water cycle is the process of water  | The water cycle is a continuous process   | 0.3927-0.3927 |
| `u18-amp-a0422-r1-q27b` | The water cycle is basically simple, but | The water cycle is a continuous process   | 0.4221-0.4221 |
| `u18-amp-a0454-r1-q27b` | The water is then it will be a bit of a  | The water cycle is a continuous process   | 0.4536-0.4536 |
| `u18-amp-a0480-r1-q27b` | I think I am lucky though, I am not too  | The water cycle is a continuous process   | 0.4800-0.4800 |
| `u18-amp-a0680-r1-q27b` | luckily luckily luckily luckily luckily  | The water cycle is an evaporation proces  | 0.6800-0.6800 |
