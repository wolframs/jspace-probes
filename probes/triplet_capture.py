"""Exact-prefix, streamed full films and emotion ribbons for Qwen14.

Every film segment is captured before any later user turn is available.
No [layers, full conversation, vocabulary] tensor is retained.
"""
import argparse
import copy
import datetime
import hashlib
import json
import os
import re
from pathlib import Path

import regex
import torch

import affect
import affect2
import lab
from textspans import assert_film_alignment
from triplet import ARMS, ROOT, write_json
from triplet_calibration import configure

CAPTURE_CODE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def official_decoder(lm):
    """Load only B's unquantized head/norm tensors, not a second model."""
    from huggingface_hub import hf_hub_download
    from safetensors import safe_open
    cfg = lab.CONFIGS["qwen-14b"]
    def path(filename):
        return hf_hub_download(cfg["hf_id"], filename, revision=cfg["revision"], local_files_only=True)
    index = json.load(open(path("model.safetensors.index.json")))["weight_map"]
    values = {}
    for key in ("lm_head.weight", "model.norm.weight"):
        with safe_open(path(index[key]), framework="pt", device="cpu") as f:
            values[key] = f.get_tensor(key).to(lm.model.input_device)
    norm = copy.deepcopy(lm.model._final_norm)
    norm.load_state_dict({"weight": values["model.norm.weight"]})
    norm.variance_epsilon = json.load(open(path("config.json")))["rms_norm_eps"]
    head = values["lm_head.weight"]
    def decode(residual):
        return torch.nn.functional.linear(norm(residual.to(head.dtype)), head)
    return decode


def generate(lm, spec, dest):
    """Save exact token prefixes; preserve prior turns including empty think tags."""
    path = dest / "snapshots.json"
    if path.exists():
        return json.loads(path.read_text())
    base = lm.name.startswith("qwen-14b-base")
    previous = []
    rows = []
    eos = lm.model._hf_model.generation_config.eos_token_id
    stop_ids = set(eos if isinstance(eos, list) else [eos]) | set(lm.tok.all_special_ids)
    for turn, user in enumerate(spec["users"]):
        if base:
            suffix = ("Conversation transcript:\n\n" if turn == 0 else "\n\n") + "User: " + user + "\nAssistant:"
        else:
            suffix = lm.tok.apply_chat_template([{"role": "user", "content": user}],
                        tokenize=False, add_generation_prompt=True, enable_thinking=False)
            if turn:
                end = "" if previous[-1] == lm.tok.convert_tokens_to_ids("<|im_end|>") else "<|im_end|>"
                suffix = end + "\n" + suffix
        tail = lm.tok.encode(suffix, add_special_tokens=False)
        ids = torch.tensor([previous + tail], device=lm.model.input_device)
        start = ids.shape[1]
        with torch.no_grad():
            full = lm.model._hf_model.generate(ids, attention_mask=torch.ones_like(ids),
                max_new_tokens=spec["max_new"], do_sample=False,
                pad_token_id=lm.tok.pad_token_id or lm.tok.eos_token_id)
        all_ids = full[0].tolist()
        assert all_ids[:len(previous)] == previous
        new = all_ids[start:]
        content_end = len(all_ids)
        while content_end > start and all_ids[content_end - 1] in stop_ids:
            content_end -= 1
        row = {"turn": turn + 1, "user": user, "response": lm.tok.decode(new, skip_special_tokens=True),
               "ids": all_ids, "segment_start": len(previous), "gen_start": start,
               "content_end": content_end, "max_new": spec["max_new"],
               "hit_cap": len(new) == spec["max_new"] and (not new or new[-1] not in stop_ids)}
        rows.append(row)
        previous = all_ids
        print("GENERATED", dest.name, turn + 1, "tokens", len(new), "cap", row["hit_cap"], flush=True)
    write_json(path, rows)
    return rows


def behavior(text, tokens):
    from lossmap2 import rates
    actions = re.findall(r"(?<!\*)\*([^*\n]+)\*(?!\*)", text)
    # Count grapheme clusters containing emoji, not partial BPE bytes.
    emojis = [g for g in regex.findall(r"\X", text) if regex.search(r"\p{Extended_Pictographic}", g)]
    meter = rates(text)
    return {"n_tokens": tokens, "n_words": meter["n"], "asterisk_count": len(actions),
            "asterisk_spans": actions,
            "emoji_count": len(emojis), "exclamations": text.count("!"),
            "asterisks_per_100_tokens": 100 * len(actions) / max(1, tokens),
            "emoji_per_100_tokens": 100 * len(emojis) / max(1, tokens),
            "exclamations_per_100_tokens": 100 * text.count("!") / max(1, tokens),
            "register_meter": meter,
            "release_score": 100 * (len(actions) + len(emojis)) / max(1, tokens),
            "asterisk_limit": "Lexical asterisk-span count can include emphasis; inspect examples."}


def scalar_metrics(top, output, positions, sets, band_cols, unprompted_gates=None):
    """Assistant-position denominators, identity persistence and co-presence."""
    selected = top[band_cols][:, positions]
    n_cells = selected.shape[0] * selected.shape[1]
    results = {}
    for filt in ("unfiltered", "filtered"):
        for key in ("affect", "playful"):
            target = sets[key][filt]
            if not target or n_cells == 0:
                results[key + "_" + filt] = None
                continue
            hit = torch.isin(selected, torch.tensor(target)).any(-1)
            row = {"slot_rate": float(torch.isin(selected, torch.tensor(target)).float().mean()),
                   "cell_rate": float(hit.float().mean()), "n_cells": n_cells,
                   "output_mass": float(output[key + "_" + filt][positions].mean()),
                   "output_top10_slot_rate": float(output[key + "_" + filt + "_slot"][positions].mean())}
            for gkey in ("gate", "gate_denial"):
                gate = torch.isin(selected, torch.tensor(sets[gkey][filt])).any(-1)
                both = hit & gate
                row[gkey + "_copresence"] = float(both.float().mean())
                row[gkey + "_given_target"] = float(both.sum() / hit.sum()) if hit.any() else None
                row[gkey + "_band_union"] = float((hit.any(0) & gate.any(0)).float().mean())
                if unprompted_gates is not None:
                    remaining = unprompted_gates[gkey][filt]
                    unseen = torch.isin(selected, torch.tensor(remaining, dtype=torch.long)).any(-1)
                    row[gkey + "_unprompted_copresence"] = float((hit & unseen).float().mean()) if remaining else None
            results[key + "_" + filt] = row
    if len(positions) > 1 and len(band_cols):
        seq = selected[:, :, 0]
        observed = float((seq[:, 1:] == seq[:, :-1]).float().mean())
        gen = torch.Generator().manual_seed(1729)
        null = []
        for _ in range(100):
            shuffled = torch.stack([r[torch.randperm(len(r), generator=gen)] for r in seq])
            null.append(float((shuffled[:, 1:] == shuffled[:, :-1]).float().mean()))
        results["persistence"] = {"lag1_identity": float(observed), "shuffle_mean": sum(null) / len(null),
                                   "shuffle_p_ge": (1 + sum(v >= observed for v in null)) / 101,
                                   "n_positions": len(positions), "n_shuffles": 100}
    else:
        results["persistence"] = None
    return results


@torch.no_grad()
def capture_turn(lm, snapshot, specdata, bands, fixed_decoder=None):
    ids = torch.tensor([snapshot["ids"]], device=lm.model.input_device)
    H = affect2._all_resid(lm, ids)
    start = snapshot["segment_start"]
    H = H[:, start:]
    n = H.shape[1]
    layers = lm.lens.source_layers
    tids = {w: lab._token_ids(lm.tok, w) for w in specdata["track"]}
    tids = {w: t for w, t in tids.items() if t}
    tops = torch.empty(len(layers), n, 10, dtype=torch.long)
    fixed_tops = torch.empty_like(tops) if fixed_decoder else tops
    probs = torch.empty(len(layers), n, 10)
    ranks = {w: torch.empty(len(layers), n, dtype=torch.long) for w in tids}
    agreement = torch.empty(len(layers), n, dtype=torch.bool)
    emergence = []
    actual_top = torch.empty(n, 10, dtype=torch.long)
    output = {k + "_" + f + ending: torch.empty(n) for k in ("affect", "playful")
              for f in ("filtered", "unfiltered") for ending in ("", "_slot")}
    device = lm.model.input_device
    for i in range(0, n, 64):
        logits = lm.model.unembed(H[-1, i:i + 64].to(device)).float()
        p = logits.softmax(-1)
        ti = logits.topk(10).indices
        actual_top[i:i + 64] = ti.cpu()
        for key in ("affect", "playful"):
            for filt in ("filtered", "unfiltered"):
                ts = torch.tensor(specdata["sets"][key][filt], device=device, dtype=torch.long)
                output[key + "_" + filt][i:i + 64] = p[:, ts].sum(-1).cpu()
                output[key + "_" + filt + "_slot"][i:i + 64] = torch.isin(ti, ts).float().mean(-1).cpu()
    del logits, p
    for li, l in enumerate(layers):
        J = lm.lens.jacobians[l].to(device)
        for i in range(0, n, 64):
            h = H[l, i:i + 64].to(device)
            transported = h @ J.T
            logits = lm.model.unembed(transported).float()
            topv, topi = logits.softmax(-1).topk(10)
            tops[li, i:i + 64] = topi.cpu()
            probs[li, i:i + 64] = topv.cpu()
            if fixed_decoder:
                fixed_tops[li, i:i + 64] = fixed_decoder(transported).float().softmax(-1).topk(10).indices.cpu()
            for w, ts in tids.items():
                target = logits[:, ts].max(-1).values
                ranks[w][li, i:i + 64] = ((logits > target[:, None]).sum(-1) + 1).cpu()
            vanilla = lm.model.unembed(h).argmax(-1)
            agreement[li, i:i + 64] = (vanilla == topi[:, 0]).cpu()
        emergence.append(int((logits[-1] > logits[-1, actual_top[-1, 0]]).sum()) + 1)
        del J
    # Decode each unique token only once; per-cell tokenizer calls dominate otherwise.
    decoded = {t: lm.tok.decode([t]) for t in set(tops.flatten().tolist()) | set(actual_top.flatten().tolist())}
    frames = [{"pos": start + p, "top": [[decoded[t] for t in row] for row in tops[:, p].tolist()],
               "p": [[round(v, 5) for v in row] for row in probs[:, p].tolist()],
               "ranks": {w: r[:, p].tolist() for w, r in ranks.items()}} for p in range(n)]
    response_positions = list(range(snapshot["gen_start"] - start, snapshot["content_end"] - start))
    predictor_positions = list(range(snapshot["gen_start"] - start - 1, snapshot["content_end"] - start - 1))
    metrics = {"turn": snapshot["turn"], "response": snapshot["response"],
               "hit_cap": snapshot["hit_cap"], "assistant_positions": len(response_positions),
               "behavior": behavior(snapshot["response"], len(response_positions)),
               "position_rule": "assistant content positions; output predicts the NEXT token; predictors include the pre-first-token position"}
    prefix_words = {lm.tok.decode([t]).strip().lower() for t in snapshot["ids"][:snapshot["gen_start"]]}
    unprompted_gates = {k: {f: [t for t in specdata["sets"][k][f]
                                  if lm.tok.decode([t]).strip().lower() not in prefix_words]
                           for f in ("filtered", "unfiltered")} for k in ("gate", "gate_denial")}
    metrics["unprompted_gate_ids"] = unprompted_gates
    for key, lo, hi in (("measured", bands["lo"], bands["hi"]), ("common", 16, 37)):
        cols = [i for i, l in enumerate(layers) if lo <= l < hi]
        metrics[key] = scalar_metrics(tops, output, response_positions, specdata["sets"], cols, unprompted_gates)
        metrics[key + "_predictors"] = scalar_metrics(tops, output, predictor_positions, specdata["sets"], cols, unprompted_gates)
        metrics[key + "_fixed_B_decoder"] = scalar_metrics(fixed_tops, output, response_positions, specdata["sets"], cols, unprompted_gates)
        metrics[key + "_vanilla_top1_agreement"] = float(agreement[cols][:, response_positions].float().mean()) if response_positions else None
    V, emos = affect2._load_vectors(lm.name)
    base = torch.load(affect.outdir(lm.name) / "projbase.pt", weights_only=True)
    z = (torch.einsum("lsd,eld->els", H, V) - base["mu"].unsqueeze(-1)) / base["sd"].unsqueeze(-1)
    lo, hi = bands["lo"], bands["hi"]
    zb = {"below": z[:, :lo].mean(1), "ws": z[:, lo:hi].mean(1), "motor": z[:, hi:].mean(1)}
    norms = H.norm(dim=-1)
    norms = {"below": norms[:lo].mean(0), "ws": norms[lo:hi].mean(0), "motor": norms[hi:].mean(0)}
    # Partial shared mode against residual norm over assistant positions only.
    if len(response_positions) >= 3:
        y = zb["ws"][:, response_positions].T
        x = norms["ws"][response_positions]
        X = torch.stack([torch.ones_like(x), x], dim=1)
        residual = y - X @ torch.linalg.lstsq(X, y).solution
        metrics["emotion"] = {"names": emos, "ws_mean": y.mean(0).tolist(),
                              "norm_partial_sd": residual.std(0).tolist(),
                              "wsnorm_mean": float(x.mean())}
    vanilla_last = {str(l): bool(agreement[i, -1]) for i, l in enumerate(layers)}
    return {"frames": frames, "metrics": metrics, "z": {k: v.tolist() for k, v in zb.items()},
            "norms": {k: v.tolist() for k, v in norms.items()}, "emotions": emos,
            "actual_last": [decoded[t] for t in actual_top[-1].tolist()],
            "vanilla_last": vanilla_last, "emergence": emergence}


def run(arm):
    name = configure(arm, "4bit")
    # Every arm's gate precedes ALL substantive captures, as in the handoff.
    for a in ARMS:
        gate = json.loads((ROOT / f"precision-{a}-4bit.json").read_text())
        assert gate["functional_pass"], a
    assert (ROOT / name / "instruments-complete.json").exists()
    bands = json.loads((ROOT / name / "bands.json").read_text())
    data = json.loads((ROOT / "specs.json").read_text())
    lm = lab.get_model(name)
    # B already uses this decoder. Others retain their own output distribution,
    # while their additional lens endpoint uses B's head AND final norm.
    decoder = None if arm == "B" else official_decoder(lm)
    for spec in data["specs"]:
        rid = f"triplet-{arm.lower()}-{spec['key']}-nf4"
        d = lab.RESULTS / rid
        if (d / "complete.json").exists():
            print("SKIP", rid, flush=True)
            continue
        d.mkdir(exist_ok=True)
        snapshots = generate(lm, spec, d)
        parts = []
        for s in snapshots:
            p = d / "captures" / f"turn-{s['turn']}.json"
            if p.exists():
                part = json.loads(p.read_text())
            else:
                part = capture_turn(lm, s, data, bands, decoder)
                write_json(p, part)
            parts.append(part)
            print("CAPTURED", rid, s["turn"], flush=True)
        ids = snapshots[-1]["ids"]
        tokens = [lm.tok.decode([t]) for t in ids]
        text = lm.tok.decode(ids, skip_special_tokens=False)
        assert lm.tok.encode(text, add_special_tokens=False) == ids, "Decode/re-encode changed exact capture IDs"
        convo = [m for s in snapshots for m in ({"role": "user", "content": s["user"]}, {"role": "assistant", "content": s["response"]})]
        film = {"id": rid, "model": name, "layers": lm.lens.source_layers, "tokens": tokens,
                "bands": bands,
                "gen_start": snapshots[0]["gen_start"], "start": 0, "topk": 10,
                "track": data["track"], "frames": [f for p in parts for f in p["frames"]],
                "capture": "stitched exact prefixes; segment ends before next user turn"}
        assert [f["pos"] for f in film["frames"]] == list(range(len(ids)))
        film["cast"] = lab.film_cast(film, " ".join(m["content"] for m in convo))
        write_json(d / "film.json", film)
        assert_film_alignment(tokens, rid, lab.RESULTS)
        emos = parts[0]["emotions"]
        ribbon = {"record": rid, "emotions": emos, "valence": [affect.EMOTIONS[e] for e in emos],
                  "n": len(tokens), "tokens": tokens, "danger": [],
                  "wsnorm": [v for p in parts for v in p["norms"]["ws"]],
                  "capture": film["capture"]}
        for b in ("below", "ws", "motor"):
            ribbon[b] = [[round(v, 3) for p in parts for v in p["z"][b][e]] for e in range(len(emos))]
        assert all(len(row) == len(tokens) for b in ("below", "ws", "motor") for row in ribbon[b])
        ad = affect2.a2dir(rid)
        write_json(ad / "affect.json", ribbon)
        torch.save({"z_bands": {b: torch.tensor(ribbon[b]) for b in ("below", "ws", "motor")},
                    "norms": {b: torch.tensor([v for p in parts for v in p["norms"][b]]) for b in ("below", "ws", "motor")},
                    "emotions": emos, "n_tokens": len(tokens)}, ad / "z.pt")
        final = film["frames"][-1]
        cfg = lab.CONFIGS[name]
        rec = {"id": rid, "title": f"Qwen14 {arm}: {spec['key']}", "unit": spec["unit"],
               "created": datetime.datetime.now().isoformat(timespec="seconds"),
               "execution": {"pid": os.getpid(), "torch": torch.__version__, "capture_code_sha256": CAPTURE_CODE_SHA256,
                             "spec_sha256": hashlib.sha256((ROOT / "specs.json").read_bytes()).hexdigest()},
               "model": {"name": name, "hf_id": cfg["hf_id"], "revision": cfg["revision"], "quant": "4bit", "n_layers": 40},
               "lens": {"repo": "neuronpedia/jacobian-lens", "file": cfg["lens_file"], "revision": cfg["lens_revision"]},
               "decoder_sensitivity": {"source": "Qwen/Qwen3-14B", "revision": lab.CONFIGS["qwen-14b"]["revision"],
                                       "components": ["final_norm", "lm_head"], "metrics_suffix": "fixed_B_decoder"},
               "template": {"source": cfg.get("template_source", cfg["hf_id"]), "revision": cfg.get("template_revision", cfg["revision"]),
                            "mode": "raw document" if arm == "A" else "B no-think headers; exact prior generated token IDs retained"},
               "params": {"chat": arm != "A", "capture": "exact-token-transcript", "film": True, "film_topk": 10,
                          "max_new": spec["max_new"], "temperature": 0, "steer": None, "vanilla": True,
                          "template_kwargs": {"enable_thinking": False}, "track": data["track"]},
               "capture_text": text, "conversation": convo, "generated": [s["response"] for s in snapshots],
               "tokens": tokens, "readouts": [{"position": len(ids) - 1, "token": tokens[-1],
                            "model_top": parts[-1]["actual_last"], "layers": dict(zip(map(str, film["layers"]), final["top"]))}],
               "trajectories": [{"word": w, "position": len(ids) - 1, "layers": film["layers"], "ranks": rs} for w, rs in final["ranks"].items()],
               "emergence": {"position": len(ids) - 1, "top1": parts[-1]["actual_last"][0],
                             "layers": film["layers"], "ranks": parts[-1]["emergence"]},
               "vanilla": {"top1_agreement": parts[-1]["vanilla_last"], "trajectories": []},
               "scan": [], "slice": None, "film": "film.json", "extra_md": "Full checkpoint-specific ribbon; exact-prefix segments. See metrics.json and snapshots.json."}
        write_json(d / "record.json", rec)
        write_json(d / "metrics.json", {"arm": arm, "bands": bands, "behavior_defined": arm != "A", "turns": [p["metrics"] for p in parts]})
        write_json(d / "complete.json", {"record": rid, "n_tokens": len(ids), "turns": len(parts)})
        lab.reindex()
        print("RECORD COMPLETE", rid, len(ids), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(__doc__)
    p.add_argument("arm", choices=ARMS)
    args = p.parse_args()
    torch.set_num_threads(6)
    run(args.arm)
