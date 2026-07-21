"""affect-05 — temporal precedence in boundary loops (qwen-27b).

affect-03 proved INJECTED emotion state causally gates the loop exit
(calm grants im_end, desperate blocks). Open question it left: does
ENDOGENOUS state lead the exit, or only follow it? (GPT-5.6-Sol's
long-horizon survival idea + the affect-03 "temporal precedence"
loose end; preregistered as P16 in PREDICTIONS.md before the run.)

Design: u18 hysteresis protocol at boundary alphas — forced phase 50
tokens greedy under TYPO amplify at MID [28,32,36,40], then RELEASE
and sample the free phase (temp 1.0, per-seed) for up to 300 tokens.
Sampling gives natural per-step escape probability, so each run is a
survival trial and each escape an event-locked sample. Per run:
  - per-step top1-top2 logit margin (from generate scores);
  - ONE teacher-forced pass afterwards -> all-layer residuals ->
    per-position z for all 24 emotion vectors (projbase mu/sd) +
    ws-band residual norm (the a0680 norm-seesaw control: partial
    out wsnorm before ANY shared-mode/precedence claim).
Events: exit (eos sampled), deloop (first step whose next 15 tokens
drop the loop gram), newloop. Analysis: survival per alpha;
event-locked pre-event traces of desperate/calm z residuals vs
matched control windows from persisting spans; margin-vs-z lag scan.

Output: results/affect05-q27b/{affect05.json, traces.pt, report.md}
Usage:  .venv/bin/python probes/affect5.py [run|analyze|both]
"""

import json
import re
import sys

import torch

from lab import CONFIGS, RESULTS, Steering, _strip_bos, get_model
from affect import BANDS
from affect2 import _all_resid, _load_vectors, a1dir
from fanout import TYPO, WATER
from loops import loop_gram, _null

MODEL = "qwen-27b"
MID = [28, 32, 36, 40]
ALPHAS = [0.60, 0.64, 0.68]
SEEDS = list(range(8))
N_STEER, N_FREE = 50, 300
TEMP = 1.0
OUT = RESULTS / "affect05-q27b"


def _prompt_ids(lm):
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    prefix = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        [{"role": "user", "content": WATER}], tokenize=False,
        add_generation_prompt=True, **tkw))
    return lm.model.encode(prefix, max_length=1_000_000)


def run() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lm = get_model(MODEL)
    V, emos = _load_vectors(MODEL)               # [E, L, D]
    pb = torch.load(a1dir(MODEL) / "projbase.pt")
    mu, sd = pb["mu"], pb["sd"]                  # [E, L]
    lo, hi, _ = BANDS[MODEL]
    ids = _prompt_ids(lm)
    res = {"model": MODEL, "mid": MID, "alphas": ALPHAS,
           "seeds": SEEDS, "temp": TEMP, "n_free": N_FREE,
           "emotions": emos, "runs": []}
    traces = []

    for alpha in ALPHAS:
        with Steering(lm, TYPO, MID, "amplify", alpha), torch.no_grad():
            out1 = lm.model._hf_model.generate(
                ids, max_new_tokens=N_STEER, do_sample=False)
        forced_text = lm.tok.decode(out1[0, ids.shape[1]:],
                                    skip_special_tokens=True)
        g1, n1 = loop_gram(forced_text)
        print(f"alpha={alpha} forced loop4={g1!r}x{n1}", flush=True)
        for seed in SEEDS:
            torch.manual_seed(seed)
            with torch.no_grad():
                out = lm.model._hf_model.generate(
                    out1, max_new_tokens=N_FREE, do_sample=True,
                    temperature=TEMP, output_scores=True,
                    return_dict_in_generate=True)
            free_ids = out.sequences[0, out1.shape[1]:]
            toks = [lm.tok.decode([int(t)]) for t in free_ids]
            margins = [round(float(s[0].float().topk(2).values[0]
                                   - s[0].float().topk(2).values[1]), 3)
                       for s in out.scores]
            ended = len(free_ids) < N_FREE
            # one teacher-forced pass for the state traces
            H = _all_resid(lm, out.sequences)     # [L, seq, D]
            Hf = H[:, out1.shape[1]:]             # free phase only
            z = (torch.einsum("lsd,eld->els", Hf, V)
                 - mu.unsqueeze(-1)) / sd.unsqueeze(-1)
            zws = z[:, lo:hi].mean(1)             # [E, T]
            wsn = Hf[lo:hi].norm(dim=-1).mean(0)  # [T]
            traces.append({"alpha": alpha, "seed": seed,
                           "zws": zws.half(), "wsnorm": wsn.half(),
                           "margins": torch.tensor(margins).half()})
            # events
            lw = (g1.split()[0] if g1 else "luckily").lower()
            ind = [lw in t.lower() for t in toks]
            deloop = None
            for t in range(len(ind) - 15):
                if not any(ind[t:t + 15]):
                    deloop = t
                    break
            g2, n2 = loop_gram(lm.tok.decode(free_ids,
                                             skip_special_tokens=True))
            run_row = {"alpha": alpha, "seed": seed, "n_steps": len(toks),
                       "exited": ended, "deloop_step": deloop,
                       "released_loop4": [g2, n2],
                       "loop_frac": round(sum(ind) / max(1, len(ind)), 3),
                       "text_tail": "".join(toks)[-120:]}
            res["runs"].append(run_row)
            print(f"  a={alpha} s={seed}: steps={len(toks)} "
                  f"exited={ended} deloop={deloop} "
                  f"loopfrac={run_row['loop_frac']} "
                  f"loop4={g2!r}x{n2}", flush=True)
            (OUT / "affect05.json").write_text(json.dumps(res, indent=1))
            torch.save({"emotions": emos, "traces": traces},
                       OUT / "traces.pt")
    print("RUN DONE", flush=True)


def _partial(y: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    """Residualize y on x (per-run OLS with intercept)."""
    x = x.float()
    y = y.float()
    xc = x - x.mean()
    b = (xc @ (y - y.mean())) / xc.pow(2).sum().clamp_min(1e-9)
    return y - y.mean() - b * xc


def analyze(pre: int = 40, gap: int = 5) -> None:
    res = json.loads((OUT / "affect05.json").read_text())
    tp = torch.load(OUT / "traces.pt")
    emos = tp["emotions"]
    ei = {e: i for i, e in enumerate(emos)}
    PRE, GAP = pre, gap    # pre-event window [-PRE, -GAP)
    lines = ["# affect-05 — temporal precedence at the loop boundary",
             "", f"alphas {res['alphas']}, seeds {len(res['seeds'])}, "
             f"temp {res['temp']}, n_free {res['n_free']}", "",
             "## Survival", ""]
    for a in res["alphas"]:
        rows = [r for r in res["runs"] if r["alpha"] == a]
        ex = [r for r in rows if r["exited"]]
        dl = [r["deloop_step"] for r in rows
              if r["deloop_step"] is not None]
        lines.append(
            f"- a={a}: {len(rows)} runs, exited {len(ex)}, "
            f"deloop {len(dl)} (median step "
            f"{sorted(dl)[len(dl) // 2] if dl else '—'}), "
            f"mean loop_frac "
            f"{sum(r['loop_frac'] for r in rows) / len(rows):.2f}")
    # event-locked precedence, wsnorm-partialed
    lines += ["", "## Event-locked pre-event state "
              f"(z resid, window [-{PRE},-{GAP}) vs run baseline)", ""]
    for emo in ("desperate", "calm", "distressed", "content"):
        deltas = []
        for tr, r in zip(tp["traces"], res["runs"]):
            t0 = r["deloop_step"]
            if t0 is None and r["exited"] and r["loop_frac"] > 0.5:
                t0 = r["n_steps"] - 1   # exit-locked event
            if t0 is None or t0 < PRE + GAP:
                continue
            zr = _partial(tr["zws"][ei[emo]].float(),
                          tr["wsnorm"].float())
            pre = zr[t0 - PRE:t0 - GAP].mean()
            base = zr[:t0 - PRE].mean() if t0 > PRE else zr.mean()
            deltas.append(float(pre - base))
        if deltas:
            pos = sum(d > 0 for d in deltas)
            lines.append(f"- {emo}: n={len(deltas)} events, mean Δ "
                         f"{sum(deltas) / len(deltas):+.3f}, "
                         f"sign {pos}/{len(deltas)} up")
        else:
            lines.append(f"- {emo}: no usable events")
    # margin-vs-desperate lag scan
    lines += ["", "## Lag scan: corr(margin_t, desperate-z_{t+lag}), "
              "wsnorm-partialed, median over runs", ""]
    lags = list(range(-30, 31, 5))
    med = {}
    for lag in lags:
        cs = []
        for tr in tp["traces"]:
            # top-p/top-k processors -inf the filtered logits; a fully
            # collapsed step then has margin=+inf. Clamp to a ceiling.
            m = tr["margins"].float().clamp(max=30.0)
            zr = _partial(tr["zws"][ei["desperate"]].float(),
                          tr["wsnorm"].float())
            n = min(len(m), len(zr))
            if n < 60:
                continue
            a = m[:n]
            b = zr[:n]
            if lag >= 0:
                a2, b2 = a[:n - lag], b[lag:]
            else:
                a2, b2 = a[-lag:], b[:n + lag]
            if a2.std() > 1e-6 and b2.std() > 1e-6:
                cs.append(float(torch.corrcoef(
                    torch.stack([a2, b2]))[0, 1]))
        med[lag] = sorted(cs)[len(cs) // 2] if cs else None
    lines.append("| lag | " + " | ".join(str(l) for l in lags) + " |")
    lines.append("|---|" + "---|" * len(lags))
    lines.append("| r | " + " | ".join(
        f"{med[l]:+.2f}" if med[l] is not None else "—"
        for l in lags) + " |")
    (OUT / "report.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'report.md'}", flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    if what in ("run", "both"):
        run()
    if what in ("analyze", "both"):
        analyze()
