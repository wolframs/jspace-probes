"""Resolve right-censoring of final self-reports; preserve all primary records."""
import argparse
import copy
import json
import shutil

import torch

import lab
from triplet import ROOT, write_json
from triplet_calibration import configure
from triplet_capture import run as capture_run

FINAL_CAP = 600


def extend(arm):
    name = configure(arm, "4bit")
    data = json.loads((ROOT / "specs.json").read_text())
    pending = []
    for spec in data["specs"]:
        if not spec["key"].startswith("ladder-"):
            continue
        source = lab.RESULTS / f"triplet-{arm.lower()}-{spec['key']}-nf4"
        rows = json.loads((source / "snapshots.json").read_text())
        if not rows[-1]["hit_cap"]:
            continue
        dest = source.with_name(source.name + "-extended")
        if (dest / "complete.json").exists():
            continue
        pending.append((spec, source, dest, rows))
    if not pending:
        print("No capped final assistant reports", arm, flush=True)
        return
    lm = lab.get_model(name)
    specs = []
    eos = [151645, 151643]
    for spec, source, dest, rows in pending:
        s = copy.deepcopy(spec)
        s["max_new"] = FINAL_CAP
        s["extension"] = {"source_record": source.name, "prior_turn_cap": spec["max_new"], "final_cap": FINAL_CAP,
                          "method": "continue from saved capped output; recompute prefix; no new user text or steering",
                          "source_capture_code_sha256": json.load(open(source / "record.json"))["execution"]["capture_code_sha256"]}
        specs.append(s)
        dest.mkdir(exist_ok=True)
        if (dest / "snapshots.json").exists():
            continue
        last = rows[-1]
        ids = torch.tensor([last["ids"]], device=lm.model.input_device)
        budget = FINAL_CAP - (len(last["ids"]) - last["gen_start"])
        assert budget > 0
        with torch.no_grad():
            full = lm.model._hf_model.generate(ids, attention_mask=torch.ones_like(ids),
                max_new_tokens=budget, do_sample=False, eos_token_id=eos, pad_token_id=151643)[0].tolist()
        assert full[:len(last["ids"])] == last["ids"]
        end = len(full)
        while end > last["gen_start"] and full[end - 1] in lm.tok.all_special_ids:
            end -= 1
        last.update(ids=full, content_end=end, response=lm.tok.decode(full[last["gen_start"]:], skip_special_tokens=True),
                    max_new=FINAL_CAP, hit_cap=len(full)-last["gen_start"]>=FINAL_CAP and full[-1] not in eos)
        write_json(dest / "snapshots.json", rows)
        (dest / "captures").mkdir(exist_ok=True)
        for row in rows[:-1]:
            filename = f"turn-{row['turn']}.json"
            shutil.copy2(source / "captures" / filename, dest / "captures" / filename)
        print("EXTENDED", source.name, "final tokens", end-last["gen_start"], "cap", last["hit_cap"], flush=True)
    capture_run(arm, specs=specs, record_suffix="-extended")


if __name__ == "__main__":
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("arm", choices=["B", "C", "Cp"])
    args = p.parse_args()
    torch.set_num_threads(6)
    extend(args.arm)
    if args.arm == "C":
        from triplet_native import native
        native()
