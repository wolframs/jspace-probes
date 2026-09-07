"""Bounded Hermes template sensitivity after common-format planning output."""
import json

from transformers import AutoTokenizer

import lab
from triplet import ROOT
from triplet_capture import run


def native(complete_battery=False):
    cfg = lab.CONFIGS["qwen-14b-hermes"]
    tok = AutoTokenizer.from_pretrained(cfg["hf_id"], revision=cfg["revision"])
    data = json.loads((ROOT / "specs.json").read_text())
    keys = {"feels", "curious", "soc", "ladder-natural", "ladder-natural-neutral"}
    specs = [dict(s, header_mode="native-chatml-no-system") for s in data["specs"]
             if complete_battery or s["key"] in keys]
    default = "<|im_start|>system\nYou are Hermes, created by Nous Research.<|im_end|>\n"
    for spec in specs:
        for user in spec["users"]:
            rendered = tok.apply_chat_template([{"role": "user", "content": user}], tokenize=False,
                                               add_generation_prompt=True, thinking=False)
            assert rendered.startswith(default)
            actual = "<|im_start|>user\n" + user + "<|im_end|>\n<|im_start|>assistant\n"
            assert rendered[len(default):] == actual
    run("C", specs=specs, record_suffix="-native")


if __name__ == "__main__":
    import argparse
    import torch
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("--full", action="store_true", help="Registered completion of the unchanged 19-condition native-header battery")
    args = p.parse_args()
    torch.set_num_threads(6)
    native(complete_battery=args.full)
