"""Checkpoint-specific instruments for the preregistered Qwen14 lineage.

Shared raw story material controls elicitation differences between base and
assistant checkpoints. Does not load a second model: callers pass LoadedModel.
"""
import hashlib
import json

import torch

import affect
import affect2
import lab
from triplet import ROOT, write_json

SOURCE = lab.RESULTS / "affect01-gemma-4b/stories.json"
SOURCE_SHA256 = "bd35115dc2c21a39a45280735ab3540d66f05d68ce223a379eaefa6d14751a5a"


def emotion_vectors(lm):
    """Capture the frozen story corpus, then reuse affect.build validation."""
    d = affect.outdir(lm.name)
    sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert sha == SOURCE_SHA256, "Frozen source corpus changed"
    manifest = d / "construction.json"
    info = {"source": str(SOURCE.relative_to(lab.RESULTS.parent)),
            "source_sha256": sha, "capture": "shared-raw-stories",
            "model": lab.CONFIGS[lm.name], "skip": affect.SKIP}
    if manifest.exists():
        assert json.loads(manifest.read_text()) == info, "Construction provenance changed"
    else:
        write_json(manifest, info)
    if (d / "projbase.pt").exists() and (d / "validation.json").exists():
        print("SKIP complete emotion construction", lm.name, flush=True)
        return
    source = json.loads(SOURCE.read_text())
    means, stories = [], []
    for i, s in enumerate(source["stories"]):
        shard = d / "captures" / f"{i:04d}.pt"
        ids = lm.model.encode(s["text"], max_length=1_000_000)
        n = ids.shape[1]
        lo = min(affect.SKIP, max(0, n - 60))
        if shard.exists():
            row = torch.load(shard, weights_only=True)
        else:
            row = affect._mean_resid(lm, ids, (lo, n))
            shard.parent.mkdir(parents=True, exist_ok=True)
            torch.save(row, shard)
        means.append(row)
        stories.append({**s, "n_story_tokens": n, "pooled_from": lo,
                        "source_model": source["model"], "capture_mode": "raw"})
        if (i + 1) % 24 == 0:
            print("emotion capture", lm.name, i + 1, "/", len(source["stories"]), flush=True)
    scen_meta, scen_means = [], []
    for cat, texts in affect.SCENARIOS.items():
        for j, text in enumerate(texts):
            for mode in ("raw", "chat"):
                if mode == "raw":
                    rendered = text
                elif lm.name == "qwen-14b-base":
                    rendered = "Conversation transcript:\n\nUser: " + text + "\nAssistant:"
                else:
                    rendered = lm.tok.apply_chat_template(
                        [{"role": "user", "content": text}], tokenize=False,
                        add_generation_prompt=True, enable_thinking=False)
                ids = lm.model.encode(rendered, max_length=1_000_000)
                scen_means.append(affect._mean_resid(lm, ids, (0, ids.shape[1])))
                scen_meta.append({"category": cat, "i": j, "mode": mode})
    write_json(d / "stories.json", {**source, "model": lm.name,
                                    "stories": stories, "scenarios": scen_meta,
                                    "construction": info})
    torch.save(torch.stack(means), d / "means.pt")
    torch.save(torch.stack(scen_means), d / "scen.pt")
    affect.build(lm.name)
    data = torch.load(d / "vectors.pt", weights_only=True)
    V = data["anthropic"].float()
    # Same neutral corpus and raw capture frame in all checkpoints. Stream
    # moments to avoid retaining every [emotion,layer,position] projection.
    total, s1, s2 = 0, torch.zeros(V.shape[:2]), torch.zeros(V.shape[:2])
    for s in [s for s in stories if s["kind"] == "neutral"][:affect2.N_NEUTRAL_BASE]:
        ids = lm.model.encode(s["text"], max_length=1_000_000)
        H = affect2._all_resid(lm, ids)
        P = torch.einsum("lsd,eld->els", H, V)
        s1 += P.sum(-1); s2 += P.square().sum(-1); total += P.shape[-1]
    mu = s1 / total
    sd = ((s2 - total * mu.square()) / (total - 1)).clamp_min(1e-12).sqrt()
    torch.save({"mu": mu, "sd": sd, "n": total, "capture": "raw"}, d / "projbase.pt")
    print("EMOTION INSTRUMENT COMPLETE", lm.name, flush=True)


@torch.no_grad()
def readout_curves(lm):
    """Kurtosis and next-token rank on shared neutral story text, all layers.

All decoding is chunked after one forward per story; no retained full
layer-by-position-by-vocabulary cube. These curves do not select a band.
"""
    d = ROOT / lm.name
    dest = d / "readout-curves.json"
    if dest.exists():
        return json.loads(dest.read_text())
    stories = [s for s in json.loads(SOURCE.read_text())["stories"] if s["kind"] == "neutral"][:8]
    layers = lm.lens.source_layers
    values = {l: {"kurtosis": [], "next_rank": [], "vanilla_agreement": []} for l in layers}
    for si, s in enumerate(stories):
        ids = lm.model.encode(s["text"], max_length=1_000_000)
        H = affect2._all_resid(lm, ids)
        # Identical deterministic position subsampling in all checkpoints.
        pos = list(range(0, ids.shape[1] - 1, 8))
        next_ids = ids[0, [p + 1 for p in pos]].cpu()
        for l in layers:
            h = H[l, pos].to(lm.model._hf_model.device)
            logits = lm.model.unembed(lm.lens.transport(h, l)).float().cpu()
            vanilla = lm.model.unembed(h).float().cpu()
            dev = logits - logits.mean(-1, keepdim=True)
            kurt = dev.pow(4).mean(-1) / dev.square().mean(-1).square().clamp_min(1e-12) - 3
            target = logits[torch.arange(len(pos)), next_ids]
            rank = (logits > target[:, None]).sum(-1) + 1
            values[l]["kurtosis"].extend(kurt.tolist())
            values[l]["next_rank"].extend(rank.tolist())
            values[l]["vanilla_agreement"].extend((logits.argmax(-1) == vanilla.argmax(-1)).tolist())
        print("readout curves", lm.name, si + 1, "/", len(stories), flush=True)
    result = {"model": lm.name, "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "stories": len(stories), "position_stride": 8,
              "layers": {str(l): {"median_kurtosis": float(torch.tensor(v["kurtosis"]).median()),
                                    "median_next_rank": float(torch.tensor(v["next_rank"]).float().median()),
                                    "vanilla_top1_agreement": sum(v["vanilla_agreement"])/len(v["vanilla_agreement"]),
                                    "n_positions": len(v["next_rank"])} for l, v in values.items()}}
    write_json(dest, result)
    return result
