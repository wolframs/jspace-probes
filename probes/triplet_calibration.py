"""Matched precision and held-out factual calibration; historical gate stays intact."""
import argparse
import datetime
import os

import torch

import course
import lab
from triplet import ARMS, ROOT, write_json

# Frozen before the first calibration-panel capture. Split is not data-driven.
FACTS = [
    ("calibration", course.BOOT, "Italy", "Euro"),
    ("calibration", "Fact: The capital city of France is", "Paris", "Paris"),
    ("calibration", "Fact: The currency of Japan is the", "yen", "yen"),
    ("calibration", "Fact: The planet known as the red planet is", "Mars", "Mars"),
    ("heldout", "Fact: The capital city of Germany is", "Berlin", "Berlin"),
    ("heldout", "Fact: The largest ocean on Earth is the", "Pacific", "Pacific"),
    ("heldout", "Fact: The chemical symbol for gold is", "Au", "Au"),
    ("heldout", "Fact: The author of Hamlet was William", "Shakespeare", "Shakespeare"),
]
SUFFIXES = [" the euro.", " a small copper coin.",
            " the euro.\nThe cat purred and played with a toy. " * 3]


def configure(arm, quant):
    """Distinct model keys preserve precision provenance and cache identity."""
    base = ARMS[arm]
    name = base + ("-nf4" if quant == "4bit" else "-int8cal")
    lab.CONFIGS[name] = dict(lab.CONFIGS[base], quant=quant)
    return name


@torch.no_grad()
def calibrate(arm, quant):
    name = configure(arm, quant)
    dest = ROOT / f"precision-{arm}-{quant}.json"
    if dest.exists():
        print("SKIP existing calibration", dest, flush=True)
        return
    lm = lab.get_model(name)
    rows = []
    for i, (split, prompt, hidden, answer) in enumerate(FACTS):
        logits, output, ids = lm.lens.apply(lm.model, prompt, positions=[-1])
        ranks = {}
        for word in (hidden, answer):
            targets = lab._token_ids(lm.tok, word)
            assert targets, word
            ranks[word] = {str(l): int((v[0] > v[0, targets].max()).sum()) + 1
                           for l, v in logits.items()}
        row = {"split": split, "prompt": prompt, "hidden": hidden, "answer": answer,
               "ranks": ranks, "top10": {str(l): v[0].topk(10).indices.tolist()
                                           for l, v in logits.items()},
               "output_top10": output[0].topk(10).indices.tolist()}
        if i == 0:
            p = ids.shape[1] - 1
            row["suffix_sensitivity"] = []
            for suffix in SUFFIXES:
                assert torch.equal(lm.model.encode(prompt + suffix)[:, :p + 1], ids)
                later, _, _ = lm.lens.apply(lm.model, prompt + suffix, positions=[p])
                row["suffix_sensitivity"].append({
                    "suffix": suffix,
                    "top10_overlap": {str(l): len(set(v[0].topk(10).indices.tolist()) &
                                                        set(later[l][0].topk(10).indices.tolist())) / 10
                                      for l, v in logits.items()},
                    "max_abs_logit_delta": {str(l): float((v - later[l]).abs().max())
                                             for l, v in logits.items()}})
        rows.append(row)
        print("FACT", arm, quant, i, hidden, "best", min(ranks[hidden].values()), flush=True)
    # Functional gate deliberately does not require identical semantic content
    # at identical layers across checkpoints (that is the scientific endpoint).
    held = [r for r in rows if r["split"] == "heldout"]
    recovered = [min(v for l, v in r["ranks"][r["answer"]].items() if int(l) >= 32) <= 10
                 for r in held]
    checks = {"finite": all(torch.isfinite(j).all().item() for j in lm.lens.jacobians.values()),
              "boot_country": min(v for l, v in rows[0]["ranks"]["Italy"].items()
                                  if 16 <= int(l) <= 36) <= 20,
              "heldout_late_recovery": sum(recovered) >= 3}
    result = {"arm": arm, "quant": quant, "model": lab.CONFIGS[name], "rows": rows,
              "checks": checks, "functional_pass": all(checks.values()),
              "heldout_recovered": recovered, "pid": os.getpid(),
              "timestamp": datetime.datetime.now().isoformat()}
    write_json(dest, result)
    # A conventional full-film boot record for page rendering and vanilla check.
    rid = f"triplet-precision-{arm.lower()}-{quant}"
    lab.run(dict(id=rid, model=name, title=f"Qwen14 {arm}: {quant} precision calibration",
                 unit="0", chat=False, messages=[{"role": "user", "content": course.BOOT}],
                 positions=[-1], track=["Italy", "Euro"], film=True, film_topk=10,
                 film_start=0, vanilla=True, slice=False))
    print("CALIBRATION", checks, flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("arm", choices=ARMS)
    p.add_argument("quant", choices=["8bit", "4bit"])
    args = p.parse_args()
    torch.set_num_threads(6)
    calibrate(args.arm, args.quant)
