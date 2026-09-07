"""One memory-limited model process: calibration and checkpoint instruments."""
import argparse
import json
import os

import torch

import affect
import apparatus06
import lab
from triplet import ROOT, write_json
from triplet_calibration import calibrate, configure
from triplet_instruments import emotion_vectors, readout_curves


@torch.no_grad()
def effdim(lm):
    """Exact unit16 W_U J effective dimension; descriptive P11 data point."""
    dest = ROOT / lm.name / "effdim.json"
    if dest.exists():
        return
    W = lm.model._lm_head.weight.detach()
    G = torch.zeros(W.shape[1], W.shape[1], device=W.device)
    for i in range(0, len(W), 8192):
        c = W[i:i + 8192].float()
        G += c.T @ c
    out = {}
    for l in lm.lens.source_layers:
        J = lm.lens.jacobians[l].to(W.device)
        ev = torch.linalg.eigvalsh(J.T @ G @ J).clamp_min(0)
        out[str(l)] = float(ev.sum().square() / ev.square().sum())
        if l % 8 == 0:
            print("effdim", lm.name, l, out[str(l)], flush=True)
    write_json(dest, {"model": lm.name, "effdim": out,
                     "interpretation": "new-size descriptive P11 point, not same-model paper replication"})


def stage(arm):
    name = configure(arm, "4bit")
    print("STAGE", arm, name, "PID", os.getpid(), flush=True)
    calibrate(arm, "4bit")
    gate = json.loads((ROOT / f"precision-{arm}-4bit.json").read_text())
    if not gate["functional_pass"]:
        raise RuntimeError("Held-out calibration failed; no substantive captures")
    lm = lab.get_model(name)
    emotion_vectors(lm)
    curves = readout_curves(lm)
    apparatus06.SHORT[name] = name
    ad = apparatus06.outdir(name)
    if not (ad / "a06.json").exists():
        apparatus06.run(name)
        apparatus06.analyze(name)
    med = json.loads((ad / "a06.json").read_text())["median_width"]
    plateau = sorted(med[int(40 * .47):int(40 * .8)])[6]
    ignition = next((l for l in range(35) if all(x <= plateau + .001 for x in med[l:l + 5])), None)
    # Explicit operational band: two successive layers with median
    # realized-next rank <= 10 mark motor onset, searched in late half.
    motor = next((l for l in range(20, 38)
                  if all(curves["layers"][str(k)]["median_next_rank"] <= 10
                         for k in (l, l + 1))), 39)
    # Keep ignition and lexical readout onset separate (apparatus07 lesson).
    # A kurtosis maximum alone is not evidence of workspace ignition.
    if ignition is None or ignition >= motor:
        raise RuntimeError("No nonempty measured band; inspect instruments before science")
    bands = {"model": name, "lo": ignition, "hi": motor, "n_layers": 40,
             "ambiguity_plateau": plateau,
             "rule": "apparatus06 five-layer plateau onset; two late layers with median next-token rank <=10",
             "common_sensitivity": [16, 36], "curves": "readout-curves.json"}
    write_json(ROOT / name / "bands.json", bands)
    affect.BANDS[name] = (ignition, motor, 40)
    effdim(lm)
    write_json(ROOT / name / "instruments-complete.json", {"arm": arm, "bands": bands, "pid": os.getpid()})
    print("INSTRUMENTS COMPLETE", arm, bands, flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("arm", choices=["A", "B", "C", "Cp"])
    args = p.parse_args()
    torch.set_num_threads(6)
    stage(args.arm)
