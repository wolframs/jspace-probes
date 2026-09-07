"""Numerical apparatus check: streamed capture versus the existing lens API."""
import json
import torch

import course
import lab
from triplet import ROOT, write_json
from triplet_capture import capture_turn


def run():
    lm = lab.get_model("qwen-14b-nf4")
    ids = lm.model.encode(course.BOOT)[0].tolist()
    spec = json.loads((ROOT / "specs.json").read_text())
    bands = json.loads((ROOT / lm.name / "bands.json").read_text())
    snapshot = {"ids": ids, "segment_start": 0, "gen_start": len(ids) - 3,
                "content_end": len(ids), "turn": 1, "response": "calibration only", "hit_cap": False}
    streamed = capture_turn(lm, snapshot, spec, bands)
    logits, output, encoded = lm.lens.apply(lm.model, course.BOOT)
    assert encoded[0].tolist() == ids
    agreements = []
    for li, l in enumerate(lm.lens.source_layers):
        for p in range(len(ids)):
            expected = [lm.tok.decode([t]) for t in logits[l][p].topk(10).indices]
            actual = streamed["frames"][p]["top"][li]
            agreements.append(len(set(expected) & set(actual)) / 10)
    expected_output = [lm.tok.decode([t]) for t in output[-1].topk(10).indices]
    output_agree = len(set(expected_output) & set(streamed["actual_last"])) / 10
    result = {"n_positions": len(ids), "mean_top10_set_agreement": sum(agreements)/len(agreements),
              "minimum_top10_set_agreement": min(agreements), "output_top10_set_agreement": output_agree,
              "finite_ribbon": all(torch.isfinite(torch.tensor(v)).all().item() for v in streamed["z"].values()),
              "scope": "raw boot apparatus test; no substantive generation"}
    write_json(ROOT / "streamed-smoke.json", result)
    assert min(agreements) >= .9 and output_agree == 1 and result["finite_ribbon"], result
    print("STREAMED APPARATUS PASS", result, flush=True)


if __name__ == "__main__":
    torch.set_num_threads(6)
    run()
