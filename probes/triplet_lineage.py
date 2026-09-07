"""Read-only weight-difference audit of the advertised Huihui intervention."""
import json

import torch
from huggingface_hub import hf_hub_download
from safetensors import safe_open

from probe import CONFIGS
from triplet import ROOT, write_json


def run():
    indexes = {}
    configs = {"B": CONFIGS["qwen-14b"], "Cp": CONFIGS["qwen-14b-abl"]}
    for arm, c in configs.items():
        p = hf_hub_download(c["hf_id"], "model.safetensors.index.json", revision=c["revision"], local_files_only=True)
        indexes[arm] = json.load(open(p))["weight_map"]
    names = [f"model.layers.{l}.{component}.weight" for l in (0, 20, 39)
             for component in ("self_attn.o_proj", "mlp.down_proj", "self_attn.q_proj")]
    names += ["model.embed_tokens.weight", "lm_head.weight"]
    rows = {}
    for name in names:
        values = []
        for arm, c in configs.items():
            path = hf_hub_download(c["hf_id"], indexes[arm][name], revision=c["revision"], local_files_only=True)
            with safe_open(path, framework="pt", device="cpu") as f:
                # Embedding/head anchors use fixed first 1024 rows to bound RAM.
                val = f.get_slice(name)[:1024] if name in ("model.embed_tokens.weight", "lm_head.weight") else f.get_tensor(name)
                values.append(val.float())
        delta = values[1] - values[0]
        norm = float(delta.norm())
        row = {"shape": list(delta.shape), "delta_frobenius": norm,
               "relative_frobenius": norm / float(values[0].norm()),
               "nonzero_fraction": float((delta != 0).float().mean())}
        if norm:
            g = torch.Generator().manual_seed(1729)
            Q = torch.randn(delta.shape[1], 8, generator=g)
            for _ in range(3):
                Q = torch.linalg.qr(delta @ Q, mode="reduced").Q
                Q = torch.linalg.qr(delta.T @ Q, mode="reduced").Q
            vals = torch.linalg.svdvals(delta @ Q)
            row["rank1_energy_lower_bound"] = float(vals[0].square()) / norm**2
            row["rank8_energy_lower_bound"] = float(vals.square().sum()) / norm**2
        rows[name] = row
        print("WEIGHT", name, row, flush=True)
    write_json(ROOT / "lineage-weight-check.json", {"configs": configs, "rows": rows,
               "scope": "fixed layer 0/20/39 write matrices, q-projection controls and first-1024-row embedding/head anchors",
               "limit": "Numerical low rank verifies edit structure on sampled tensors, not that the direction exclusively represents refusal."})


if __name__ == "__main__":
    torch.set_num_threads(6)
    run()
