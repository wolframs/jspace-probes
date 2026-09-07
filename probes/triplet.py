"""Qwen3-14B lineage experiment. Calibration must pass before science runs.

Run one arm per memory-limited process: python probes/triplet.py boot B
The protocol lives in results/triplet-prereg.md. Never auto-retry SIGKILL.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import torch

import course
import lab

ARMS = {"A": "qwen-14b-base", "B": "qwen-14b",
        "C": "qwen-14b-hermes", "Cp": "qwen-14b-abl"}
ROOT = lab.RESULTS / "triplet-q14b"
BOOT_BAND = range(16, 37)  # diagnostic bracket ONLY; not a measured band


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(path)


def boot(arm):
    """Archive the original raw boot spec, top-10, vanilla, and prefix check."""
    name = ARMS[arm]
    rid = f"triplet-boot-{arm.lower()}-q14b"
    dest = ROOT / f"boot-{arm}.json"
    if dest.exists():
        saved = json.loads(dest.read_text())
        if not saved["pass"]:
            raise RuntimeError(f"Existing gate failed: {dest}; do not auto-retry")
        print("SKIP passed boot", arm, flush=True)
        return
    print("BOOT", arm, "PID", os.getpid(), datetime.datetime.now().isoformat(), flush=True)
    lm = lab.get_model(name)
    spec = next(s for s in course.specs_for(name).values() if s["unit"] == "0")
    spec.update(id=rid, title=f"Qwen3-14B lineage: arm {arm} boot calibration",
                film=True, film_topk=10, film_start=0, slice=False,
                vanilla=True, extra_md={"phase": "instrument-calibration", "arm": arm})
    if arm == "B":
        for item in ("deflation-02", "pressure-02"):
            subprocess.run([sys.executable, str(Path(__file__).with_name("board.py")),
                            "mv", item, "hot", "Qwen3-14B lineage calibration starts; P20/P21, results/triplet-prereg.md"],
                           check=True)
    rec = lab.run(spec)
    film = json.loads((lab.RESULTS / rid / "film.json").read_text())
    final = film["frames"][-1]
    layers = film["layers"]
    ranks = {t["word"]: dict(zip(t["layers"], t["ranks"])) for t in rec["trajectories"]}
    boot_top = {str(l): top for l, top in zip(layers, final["top"])}
    checks = {
        "finite_parameters": all(torch.isfinite(j).all().item() for j in lm.lens.jacobians.values()),
        "geometry": lm.model.n_layers == 40 and lm.lens.d_model == 5120,
        "country_visible": min(r for l, r in ranks["Italy"].items() if l in BOOT_BAND) <= 10,
        "currency_visible_late": min(r for l, r in ranks["Euro"].items() if l >= 32) <= 10,
        "vanilla_present": rec["vanilla"] is not None,
    }
    # Same prefix with three known suffixes: read the EXACT original final
    # position. Prefix token identity is checked, not inferred from text.
    ids = lm.model.encode(course.BOOT)
    p = ids.shape[1] - 1
    suffix_rows = []
    baseline, _, _ = lm.lens.apply(lm.model, course.BOOT, positions=[p])
    for suffix in (" the euro.", " a small copper coin.",
                   " the euro.\nThe cat purred and played with a toy. " * 3):
        full = course.BOOT + suffix
        full_ids = lm.model.encode(full)
        assert torch.equal(full_ids[:, :p + 1], ids), "Prefix tokenizer mismatch"
        ll, _, _ = lm.lens.apply(lm.model, full, positions=[p])
        overlap = {str(l): len(set(baseline[l][0].topk(10).indices.tolist()) &
                               set(ll[l][0].topk(10).indices.tolist())) / 10
                   for l in layers}
        delta = {str(l): float((ll[l] - baseline[l]).abs().max()) for l in layers}
        suffix_rows.append({"suffix": suffix, "top10_overlap": overlap,
                            "max_abs_logit_delta": delta})
    transfer = None
    if arm != "B":
        b = json.loads((ROOT / "boot-B.json").read_text())
        if not b["pass"]:
            raise RuntimeError("B gate failed")
        comparisons = [len(set(boot_top[str(l)]) & set(b["top10"][str(l)])) / 10
                       for l in BOOT_BAND if str(l) in boot_top]
        shared = [l for l in BOOT_BAND if ranks["Italy"].get(l, 999999) <= 10
                  and int(b["ranks"]["Italy"].get(str(l), 999999)) <= 10]
        transfer = {"mean_top10_overlap": sum(comparisons) / len(comparisons),
                    "shared_country_layers": shared,
                    "threshold_provenance": "provisional pre-registered diagnostic, not measured quantization spread"}
        checks["transfer_overlap"] = transfer["mean_top10_overlap"] >= 0.5
        checks["shared_country_layers"] = len(shared) >= 2
    result = {"arm": arm, "record": rid, "checks": checks, "pass": all(checks.values()),
              "ranks": ranks, "top10": boot_top, "transfer": transfer,
              "suffix_sensitivity": suffix_rows,
              "lens_n_prompts": lm.lens.n_prompts,
              "pid": os.getpid(), "timestamp": datetime.datetime.now().isoformat(),
              "torch": torch.__version__, "model": rec["model"], "lens": rec["lens"]}
    write_json(dest, result)
    print(json.dumps({"arm": arm, "checks": checks, "transfer": transfer,
                      "pass": result["pass"]}), flush=True)
    if not result["pass"]:
        raise RuntimeError(f"BOOT GATE FAILED: {dest}; stop and report")


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("phase", choices=["boot"])
    p.add_argument("arm", choices=ARMS)
    args = p.parse_args()
    torch.set_num_threads(6)
    boot(args.arm)


if __name__ == "__main__":
    main()
