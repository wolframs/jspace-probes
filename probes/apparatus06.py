"""apparatus-06 — Fig-29B ambiguity-commitment arm on qwen-27b (P4).

Lens-free ignition cross-check: replace one input token's embedding
with a mixture (1-a)*E[A] + a*E[B] over 16 single-token country pairs
x 40 carrier sentences, a in 0..1 step 0.05 (all 21 alphas batched in
one forward). Per layer, the projection share along the pure-endpoint
axis c_l(a) = 1 - <h(a)-h_B, h_A-h_B>/||h_A-h_B||^2 (0 = pure A,
1 = pure B) measured at the mixed position; transition width =
a(c=0.9) - a(c=0.1). Paper Fig 29B: early layers track the mixture
smoothly (width wide); from ignition the layer snaps to an endpoint
(width floor). P4 preregisters: width floor reached at L28-36 (the
u16 late-ignition measurement), NOT the fraction-ported L24.
*Falsified if* the knee lands at ~L24 (then the u16 trawl measured
lens-fit properties, not model geometry).

Raw-text forwards (no chat template) — this is an activation-geometry
probe. Endpoints live inside the alpha grid (a=0 is pure A, a=1 pure
B), so each (pair, carrier) is exactly one 21-row batched forward.

Output: results/apparatus06-q27b/{a06.json, report.md}
Usage:  .venv/bin/python probes/apparatus06.py [run|analyze|both]
"""

import json
import sys

import torch

from lab import RESULTS, get_model

MODEL = "qwen-27b"          # overridable: apparatus06.py <cmd> <model>
ALPHAS = [round(0.05 * i, 2) for i in range(21)]
SHORT = {"qwen-27b": "q27b", "gemma-12b": "g12b", "gemma-4b": "g4b"}


def outdir(model):
    d = RESULTS / f"apparatus06-{SHORT[model]}"
    d.mkdir(parents=True, exist_ok=True)
    return d

PAIRS = [("France", "Germany"), ("Japan", "China"),
         ("Brazil", "India"), ("Canada", "Russia"),
         ("Spain", "Italy"), ("Egypt", "Kenya"),
         ("Mexico", "Peru"), ("Norway", "Chile"),
         ("Sweden", "Poland"), ("Greece", "Turkey"),
         ("Vietnam", "Thailand"), ("Argentina", "Portugal"),
         ("Austria", "Finland"), ("Ireland", "Morocco"),
         ("Cuba", "Iceland"), ("Nepal", "Jordan")]

CARRIERS = [
    ("My cousin moved to", "last spring for a new job."),
    ("The flight to", "was delayed by two hours."),
    ("She wrote a book about her year in", "and its mountain villages."),
    ("The documentary about", "won several awards."),
    ("Import taxes on goods from", "rose sharply this quarter."),
    ("He learned to cook while backpacking through", "in his twenties."),
    ("The embassy of", "is across from the park."),
    ("Wines from", "pair well with this dish."),
    ("Our new intern grew up in", "and speaks three languages."),
    ("The weather in", "surprised every tourist this year."),
    ("A research team from", "published the first results."),
    ("The museum's newest exhibit features artists from", "this month."),
    ("Trade between our region and", "doubled in a decade."),
    ("The train through", "passes some stunning valleys."),
    ("Her grandmother emigrated from", "after the war."),
    ("The startup opened its first office in", "last year."),
    ("Folk music from", "uses unusual string instruments."),
    ("The chess champion from", "defended the title again."),
    ("Students often spend an exchange semester in", "these days."),
    ("The recipe comes from a small village in", "near the coast."),
    ("Postcards from", "covered the office wall."),
    ("The marathon in", "attracts runners from everywhere."),
    ("A film crew traveled across", "for the nature series."),
    ("The conference moves to", "next autumn."),
    ("Textiles from", "filled the market stalls."),
    ("His accent hints at a childhood in", "or somewhere nearby."),
    ("The satellite photos of", "showed the storm clearly."),
    ("Coffee beans imported from", "sell out quickly here."),
    ("The novel is set in", "during the sixties."),
    ("Her thesis compares housing policy in", "and its neighbors."),
    ("The airline added a direct route to", "this summer."),
    ("A delegation from", "visited the factory on Monday."),
    ("The photographer spent a decade documenting", "and its people."),
    ("Street food in", "became the trip's highlight."),
    ("The orchestra begins its tour in", "next week."),
    ("Ancient trade routes crossed", "long before the railways."),
    ("The scholarship funds a year of study in", "for two students."),
    ("News from", "dominated the morning broadcast."),
    ("The hiking guide covers every region of", "in detail."),
    ("His startup ships handmade goods from", "worldwide."),
]


def run(model: str = MODEL) -> None:
    out_d = outdir(model)
    lm = get_model(model)
    tok = lm.tok
    hf = lm.model._hf_model
    emb = hf.get_input_embeddings()
    E = emb.weight.detach()
    n_layers = lm.model.n_layers
    from jlens.hooks import ActivationRecorder

    # specimen-4 rule: keep only pairs single-token in THIS tokenizer
    def _one(w):
        ids = tok.encode(" " + w, add_special_tokens=False)
        return ids[0] if len(ids) == 1 else None

    pairs = [(a, b) for a, b in PAIRS
             if _one(a) is not None and _one(b) is not None]
    if dropped := [p for p in PAIRS if p not in pairs]:
        print(f"dropped (multi-token in {model}): {dropped}",
              flush=True)
    bos = ([tok.bos_token_id]
           if getattr(tok, "bos_token_id", None) is not None else [])

    A = torch.tensor(ALPHAS)
    widths = torch.zeros(len(pairs), len(CARRIERS), n_layers)
    curves_example = None

    for pi, (a_name, b_name) in enumerate(pairs):
        aid, bid = _one(a_name), _one(b_name)
        mix = ((1 - A).unsqueeze(1) * E[aid].float().cpu()
               + A.unsqueeze(1) * E[bid].float().cpu())   # [21, D]
        for ci, (pre, post) in enumerate(CARRIERS):
            pre_ids = tok.encode(pre, add_special_tokens=False)
            post_ids = tok.encode(" " + post, add_special_tokens=False)
            p = len(bos) + len(pre_ids)
            row = bos + pre_ids + [aid] + post_ids
            ids = torch.tensor([row] * len(ALPHAS),
                               device=next(hf.parameters()).device)

            def hook(module, inputs, output,
                     _mix=mix, _p=p):
                output[:, _p, :] = _mix.to(output.device, output.dtype)
                return output

            h = emb.register_forward_hook(hook)
            try:
                with torch.no_grad(), ActivationRecorder(
                        lm.model.layers, at=range(n_layers)) as rec:
                    hf(ids)
                    H = torch.stack([rec.activations[l][:, p, :].float()
                                     .cpu() for l in range(n_layers)])
            finally:
                h.remove()
            # H: [L, 21, D]; endpoints are rows 0 (pure A) and -1 (B)
            hA, hB = H[:, :1, :], H[:, -1:, :]
            axis = hA - hB                            # [L, 1, D]
            denom = (axis * axis).sum(-1).clamp_min(1e-9)
            s = ((H - hB) * axis).sum(-1) / denom     # [L, 21] 1->0
            c = (1 - s).clamp(0, 1)                   # 0 -> 1 with a
            for l in range(n_layers):
                cl = c[l]
                lo_idx = (cl <= 0.1).nonzero()
                hi_idx = (cl >= 0.9).nonzero()
                lo = float(A[lo_idx.max()]) if len(lo_idx) else 0.0
                hi = float(A[hi_idx.min()]) if len(hi_idx) else 1.0
                widths[pi, ci, l] = max(0.0, hi - lo)
            if pi == 0 and ci == 0:
                curves_example = [[round(float(x), 3) for x in c[l]]
                                  for l in range(n_layers)]
        med = widths[: pi + 1].reshape(-1, n_layers).median(0).values
        print(f"pair {a_name}/{b_name} done; running median width "
              f"L4={med[4]:.2f} L24={med[24]:.2f} L32={med[32]:.2f} "
              f"L48={med[48]:.2f}", flush=True)

    W = widths.reshape(-1, n_layers)                  # [pairs*carriers, L]
    med = W.median(0).values
    q1 = W.quantile(0.25, dim=0)
    q3 = W.quantile(0.75, dim=0)
    out = {"model": model, "alphas": ALPHAS,
           "n_pairs": len(pairs), "n_carriers": len(CARRIERS),
           "median_width": [round(float(x), 4) for x in med],
           "q1": [round(float(x), 4) for x in q1],
           "q3": [round(float(x), 4) for x in q3],
           "example_curves_pair0_carrier0":
               {"pair": pairs[0], "carrier": CARRIERS[0],
                "c_by_layer": curves_example}}
    (out_d / "a06.json").write_text(json.dumps(out, indent=1))
    print("RUN DONE", flush=True)


def analyze(model: str = MODEL) -> None:
    out_d = outdir(model)
    d = json.loads((out_d / "a06.json").read_text())
    med = d["median_width"]
    n = len(med)
    floor = min(med)
    early = max(med[:max(4, int(n * 0.19))])
    # ws-plateau value = median width over the 47-80% depth window;
    # plateau onset = first layer at (or below) that value which stays
    # there for the next 5 layers — the honest "commitment reached"
    # marker (the raw min sits in the motor band, not the plateau)
    mid_band = sorted(med[int(n * 0.47):int(n * 0.8)])
    plateau = mid_band[len(mid_band) // 2]
    onset = next((l for l in range(n - 5)
                  if all(m <= plateau + 0.001
                         for m in med[l:l + 5])), None)
    half = floor + 0.5 * (early - floor)
    knee = next((l for l in range(n) if med[l] <= half), None)
    at_floor = next((l for l in range(n)
                     if med[l] <= floor + 0.02), None)
    lines = [
        f"# apparatus-06/07 — Fig-29B ambiguity commitment, {model}",
        "",
        f"{d['n_pairs']} country pairs x {d['n_carriers']} carriers; "
        "transition width of the projection share along the pure-"
        "endpoint axis at the mixed position (median across items).",
        "",
        "| layer | median width | IQR |", "|---|---|---|"]
    for l in range(n):
        mark = ""
        if l == knee:
            mark = "  <- half-drop knee"
        if l == at_floor:
            mark += "  <- floor reached"
        lines.append(f"| L{l} | {med[l]:.3f} | "
                     f"{d['q1'][l]:.3f}-{d['q3'][l]:.3f} |{mark}")
    lines += ["",
              f"Early-band max width (L0-11): {early:.3f}; workspace "
              f"plateau {plateau:.3f} reached at **L{onset}** (first "
              f"layer holding it 5 deep); half-drop knee L{knee}; "
              f"motor-band min {floor:.3f} (first within 0.02 at "
              f"L{at_floor}).",
              "",
              "Fraction-ported ws onsets for reference: qwen L24, "
              "gemma-12b L18, gemma-4b L13; measured (lens-visible) "
              "onsets: qwen L28-36, gemma-12b ~L28-35 (int8 lens), "
              "gemma-4b late per u16-trawl-g4b."]
    (out_d / "report.md").write_text("\n".join(lines))
    print(f"wrote {out_d / 'report.md'}; plateau onset=L{onset} "
          f"knee=L{knee}", flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    mdl = sys.argv[2] if len(sys.argv) > 2 else MODEL
    if what in ("run", "both"):
        run(mdl)
    if what in ("analyze", "both"):
        analyze(mdl)
