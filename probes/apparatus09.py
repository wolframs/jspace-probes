"""apparatus-09 — de-junk the early lens (P19, preregistered 2026-07-31).

Specimen #6 (u5d) established WHAT the early-band furniture is (a transport
artifact: J-rank 2 vs logit-rank ~238k, prompt-invariant). This decomposes
HOW: z_t = (W_U[t] . J_l) h with h = mu + (h - mu).

Conditions per early layer, readout at position -1:
  A  raw h                    (baseline; furniture core = tokens in every
                               prompt's A-top50)
  B  mu alone                 (standing component: grand mean over prompts
                               x non-BOS positions)
  C  h - mu                   (de-junked input)
  D  h, content-massive dims zeroed   (Sun et al. COLM 2024)
  Db h, BOS-massive dims zeroed
  E  random norm-matched h, n=10      (operator-only test; both signs read)
plus the operator term measured directly: row norms ||(g . W_U[t]) J_l||
(final-norm gain g folded in; RMSNorm + softcap are rank-preserving, so
ranking is linear in (W_U . g) J_l h).

H-op: ranking ~ operator (E shows core, row-norm list ~ core).
H-standing: core is the image of mu (B reproduces, C collapses, E doesn't).
H-content: needs the real h (dead on prompt-invariance; kept as falsifier).
Secondary: content non-emergence — J-lens C stays current-token-blind while
logit lens reads the current token early (Patchscopes/Ethayarajh).

Usage: .venv/bin/python probes/apparatus09.py gemma-4b|qwen-27b
"""

import itertools
import json
import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402

from jlens.hooks import ActivationRecorder  # noqa: E402

EARLY = [2, 4, 6, 8]
K_CORE = 50
MASSIVE_RATIO = 50.0
N_RAND = 10
SEED = 190731

PROMPTS = {
    "currency": "The currency of the country shaped like a boot is",
    "recipe": "To make tomato soup, first dice one onion and",
    "code": "def fibonacci(n):",
    "poem": "The rain fell softly on the",
    "german": "Die Hauptstadt von Frankreich ist",
    "dialog": '"Where were you last night?" the detective asked.',
    "math": "Compute 17 * 23. Step 1:",
    "news": "The central bank announced on Tuesday that interest rates",
}


def topk(z, k=K_CORE):
    return z.topk(k).indices.tolist()


def rank_of(z, tid):
    return int((z > z[tid]).sum()) + 1


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b)


def mean_pairwise_jaccard(sets):
    js = [jaccard(a, b) for a, b in itertools.combinations(sets, 2)]
    return sum(js) / len(js)


def recall(core, ids):
    return len(core & set(ids)) / len(core) if core else float("nan")


def main(model_name):
    lm = lab.get_model(model_name)
    model, lens, tok = lm.model, lm.lens, lm.tok
    n = model.n_layers
    dev = model.input_device

    fitted = sorted(lens.source_layers)
    early = [l for l in EARLY if l in fitted] or fitted[:4]
    control = min(fitted, key=lambda l: abs(l - round(0.6 * n)))
    layers = early + [control]
    print(f"{model_name}: {n} layers, early={early}, control=L{control} "
          f"({control / n:.0%} depth)", flush=True)

    # ---- capture residuals, one forward per prompt ----
    resid = {l: {} for l in layers}
    ids_map = {}
    for name, p in PROMPTS.items():
        input_ids = model.encode(p)
        with torch.no_grad(), ActivationRecorder(model.layers, at=layers) as rec:
            model.forward(input_ids)
        for l in layers:
            resid[l][name] = rec.activations[l][0].detach().float().cpu()
        ids_map[name] = input_ids[0].tolist()
        print(f"  captured {name} ({len(ids_map[name])} tok)", flush=True)

    # ---- readout helpers ----
    def read(h, l, jac=True):
        h = h.to(dev).float().unsqueeze(0)
        x = lens.transport(h, l) if jac else h
        return model.unembed(x).float().cpu()[0]

    def transported(h, l):
        return lens.transport(h.to(dev).float().unsqueeze(0), l)[0].cpu()

    # final-norm gain for the operator term (gemma RMSNorm is 1+weight)
    gw = model._final_norm.weight.detach().float()
    gain = (1.0 + gw) if "gemma" in type(model._final_norm).__name__.lower() else gw
    gain = gain.to(dev)
    W = model._lm_head.weight.detach()
    V = W.shape[0]

    def row_norms(l):
        J = lens.jacobians[l].to(dev).float()
        rn = torch.empty(V)
        for i in range(0, V, 16384):
            chunk = W[i:i + 16384].to(dev).float() * gain
            rn[i:i + 16384] = (chunk @ J).norm(dim=-1).cpu()
        del J
        return rn

    gen = torch.Generator().manual_seed(SEED)
    report = {"model": model_name, "n_layers": n, "early": early,
              "control": control, "massive_ratio": MASSIVE_RATIO,
              "k_core": K_CORE, "n_rand": N_RAND, "seed": SEED,
              "prompts": PROMPTS, "layers": {}}

    for l in layers:
        tag = "control" if l == control else "early"
        pool = torch.cat([resid[l][nm][1:] for nm in PROMPTS], dim=0)
        bos = torch.stack([resid[l][nm][0] for nm in PROMPTS], dim=0)
        mu = pool.mean(0)
        meanabs = pool.abs().mean(0)
        med = float(meanabs.median())
        massive = (meanabs > MASSIVE_RATIO * med).nonzero().flatten()
        bos_meanabs = bos.abs().mean(0)
        bos_massive = (bos_meanabs > MASSIVE_RATIO * float(bos_meanabs.median())
                       ).nonzero().flatten()
        scale = float(pool.norm(dim=-1).median())

        per_prompt, share_mu, cos_mu = {}, [], []
        for nm in PROMPTS:
            h = resid[l][nm][-1]
            hD = h.clone(); hD[massive] = 0.0
            hDb = h.clone(); hDb[bos_massive] = 0.0
            zA, zC, zD, zDb = (read(h, l), read(h - mu, l),
                               read(hD, l), read(hDb, l))
            zAlog, zClog = read(h, l, jac=False), read(h - mu, l, jac=False)
            cur = ids_map[nm][-1]
            t_h, t_mu = transported(h, l), transported(mu, l)
            t_res = t_h - t_mu
            share_mu.append(float(t_mu.norm() ** 2
                                  / (t_mu.norm() ** 2 + t_res.norm() ** 2)))
            cos_mu.append(float(torch.nn.functional.cosine_similarity(
                t_h, t_mu, dim=0)))
            per_prompt[nm] = {
                "topA": topk(zA), "botA": topk(-zA),
                "topC": topk(zC), "botC": topk(-zC),
                "topD": topk(zD), "topDb": topk(zDb),
                "topAlog": topk(zAlog), "topClog": topk(zClog),
                "cur_rank": {"A": rank_of(zA, cur), "C": rank_of(zC, cur),
                             "Alog": rank_of(zAlog, cur),
                             "Clog": rank_of(zClog, cur)},
            }

        zB = read(mu, l)
        topB, botB = topk(zB), topk(-zB)
        tops_E = []
        d = mu.shape[0]
        for _ in range(N_RAND):
            g = torch.randn(d, generator=gen)
            g = g / g.norm() * scale
            zE = read(g, l)
            tops_E.append({"top": topk(zE), "bot": topk(-zE)})

        rn = row_norms(l)
        rn_top = {k: rn.topk(k).indices.tolist() for k in (30, 50, 100)}

        core = set(per_prompt[next(iter(PROMPTS))]["topA"])
        for nm in PROMPTS:
            core &= set(per_prompt[nm]["topA"])

        inv = {c: mean_pairwise_jaccard([per_prompt[nm][c] for nm in PROMPTS])
               for c in ("topA", "topC", "topD", "topDb", "topAlog", "topClog")}
        recE = [max(recall(core, t["top"]), recall(core, t["bot"]))
                for t in tops_E]
        summary = {
            "tag": tag,
            "core_size": len(core),
            "core_tokens": [tok.decode([t]) for t in sorted(core)],
            "invariance": inv,
            "recall_B": max(recall(core, topB), recall(core, botB)),
            "recall_E_mean": sum(recE) / len(recE) if core else float("nan"),
            "recall_E_each": recE,
            "recall_D": sum(recall(core, per_prompt[nm]["topD"])
                            for nm in PROMPTS) / len(PROMPTS) if core else float("nan"),
            "recall_Db": sum(recall(core, per_prompt[nm]["topDb"])
                             for nm in PROMPTS) / len(PROMPTS) if core else float("nan"),
            "recall_C": sum(recall(core, per_prompt[nm]["topC"])
                            for nm in PROMPTS) / len(PROMPTS) if core else float("nan"),
            "jaccard_rownorm30_core": jaccard(rn_top[30], core) if core else float("nan"),
            "recall_rownorm": {k: recall(core, rn_top[k]) for k in rn_top},
            "n_massive": int(massive.numel()), "massive_dims": massive.tolist(),
            "n_bos_massive": int(bos_massive.numel()),
            "bos_massive_dims": bos_massive.tolist(),
            "massive_top_ratios": [round(float(r), 1) for r in
                                   (meanabs / med).topk(10).values],
            "share_mu_mean": sum(share_mu) / len(share_mu),
            "cos_mu_mean": sum(cos_mu) / len(cos_mu),
            "cur_rank_median": {k: sorted(per_prompt[nm]["cur_rank"][k]
                                          for nm in PROMPTS)[len(PROMPTS) // 2]
                                for k in ("A", "C", "Alog", "Clog")},
            "topB_decoded": [tok.decode([t]) for t in topB[:15]],
            "rownorm_top_decoded": [tok.decode([t]) for t in rn_top[30][:15]],
        }
        report["layers"][l] = {"summary": summary, "per_prompt": per_prompt,
                               "topB": topB, "botB": botB, "tops_E": tops_E,
                               "rownorm_top": rn_top}

        s = summary
        print(f"\n=== L{l} ({tag}) ===", flush=True)
        print(f"  core: {s['core_size']} tokens {s['core_tokens'][:10]}", flush=True)
        print(f"  invariance A={inv['topA']:.3f} C={inv['topC']:.3f} "
              f"D={inv['topD']:.3f} Db={inv['topDb']:.3f} "
              f"Alog={inv['topAlog']:.3f} Clog={inv['topClog']:.3f}", flush=True)
        print(f"  core recall: B={s['recall_B']:.2f} E={s['recall_E_mean']:.2f} "
              f"C={s['recall_C']:.2f} D={s['recall_D']:.2f} "
              f"Db={s['recall_Db']:.2f}", flush=True)
        print(f"  rownorm: jacc30={s['jaccard_rownorm30_core']:.2f} "
              f"recall@100={s['recall_rownorm'][100]:.2f} "
              f"top15={s['rownorm_top_decoded']}", flush=True)
        print(f"  massive dims: content={s['n_massive']} bos={s['n_bos_massive']} "
              f"top ratios={s['massive_top_ratios'][:5]}", flush=True)
        print(f"  mu share={s['share_mu_mean']:.2f} cos(z,z_mu)={s['cos_mu_mean']:.2f}",
              flush=True)
        print(f"  current-token rank (median): J-lens A={s['cur_rank_median']['A']} "
              f"C={s['cur_rank_median']['C']} | logit A={s['cur_rank_median']['Alog']} "
              f"C={s['cur_rank_median']['Clog']}", flush=True)
        print(f"  B top15: {s['topB_decoded']}", flush=True)

    out = lab.RESULTS / f"apparatus09-{model_name}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=1))
    print(f"\nwrote {out / 'report.json'}\nDONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
