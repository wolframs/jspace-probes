"""Bounded Hermes template sensitivity after common-format planning output."""
import json

from transformers import AutoTokenizer

import lab
from triplet import ROOT
from triplet_capture import run


def native():
    cfg = lab.CONFIGS["qwen-14b-hermes"]
    tok = AutoTokenizer.from_pretrained(cfg["hf_id"], revision=cfg["revision"])
    data = json.loads((ROOT / "specs.json").read_text())
    keys = {"feels", "curious", "soc", "ladder-natural", "ladder-natural-neutral"}
    specs = [dict(s, header_mode="native-chatml-no-system") for s in data["specs"] if s["key"] in keys]
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
    import torch
    torch.set_num_threads(6)
    native()
