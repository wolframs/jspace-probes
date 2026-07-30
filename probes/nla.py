"""Capture residuals and decode them with the available NLAs.

Two invocations keep 24 GB GPUs comfortable:
  python probes/nla.py capture gemma-12b --record u14x-neutral-g12b -p -1
  python probes/nla.py decode results/u14x-neutral-g12b/nla/repo.pt
"""

import argparse
import datetime as dt
import json
import pathlib
import re

import torch
import yaml
from probe import CONFIGS
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

ROOT = pathlib.Path(__file__).parent.parent
EXPLANATION = re.compile(
    r"<explanation>\s*(.*?)\s*</explanation>", re.DOTALL)
NLA = {
    "gemma-12b": {
        "layer": 32, "av": "kitft/nla-gemma3-12b-L32-av",
        "mode": "embedding",
    },
    "qwen-27b": {
        "layer": 42, "av": "ceselder/qwen3.6-27b-nla-L42",
        "mode": "karvonen",
    },
}


def layers(model):
    base = model.get_base_model() if hasattr(model, "peft_config") else model
    inner = base.model
    inner = getattr(inner, "language_model", inner)
    return inner.layers


def ids_from_record(tok, model_name, record):
    if record.get("params", {}).get("chat") is False:
        text = record["conversation"][0]["content"]
    else:
        kw = CONFIGS[model_name].get("template_kwargs", {})
        text = tok.apply_chat_template(
            record["conversation"], tokenize=False,
            add_generation_prompt=False, **kw)
    bos = tok.bos_token
    if bos and text.startswith(bos):
        text = text[len(bos):]
    ids = tok(text, return_tensors="pt", add_special_tokens=True).input_ids
    expected = len(record["tokens"])
    if ids.shape[1] != expected:
        raise RuntimeError(
            f"replay token count {ids.shape[1]} != record count {expected}")
    return text, ids


def assistant_starts(tok, model_name, record):
    kw = CONFIGS[model_name].get("template_kwargs", {})
    out = []
    for i, message in enumerate(record["conversation"]):
        if message["role"] != "assistant":
            continue
        sentinel = f"<<NLA_SENTINEL_{i}_314159>>"
        conversation = [dict(m) for m in record["conversation"]]
        conversation[i]["content"] = sentinel
        text = tok.apply_chat_template(
            conversation, tokenize=False, add_generation_prompt=False, **kw)
        bos = tok.bos_token
        if bos and text.startswith(bos):
            text = text[len(bos):]
        char = text.index(sentinel)
        enc = tok(text, add_special_tokens=True, return_offsets_mapping=True)
        starts = [j for j, (lo, hi) in enumerate(enc["offset_mapping"])
                  if lo <= char < hi]
        if len(starts) != 1 or starts[0] == 0:
            raise RuntimeError(f"could not locate assistant {i} sentinel")
        out.append(starts[0] - 1)
    return out


def load_target(name, precision, allow_large=False):
    cfg = CONFIGS[name]
    repo = ("Qwen/Qwen3.6-27B"
            if name == "qwen-27b" and precision == "bf16"
            else cfg["hf_id"])
    kw = {"dtype": torch.bfloat16}
    if precision == "bf16":
        if name == "qwen-27b" and not allow_large:
            raise SystemExit("qwen-27b bf16 is not safe on this 62 GB host")
        kw["device_map"] = "auto"
        if name != "qwen-27b":
            kw["max_memory"] = {0: "20GiB", "cpu": "48GiB"}
    else:
        kw["device_map"] = "cuda:0"
        if cfg["quant"] == "8bit":
            kw["quantization_config"] = BitsAndBytesConfig(load_in_8bit=True)
    return repo, AutoModelForCausalLM.from_pretrained(repo, **kw)


def capture(args):
    spec = NLA[args.model]
    tok = AutoTokenizer.from_pretrained(CONFIGS[args.model]["hf_id"])
    repo, model = load_target(
        args.model, args.precision, args.allow_large_bf16)
    model.eval()

    for record_id in args.record:
        record = json.loads((ROOT / "results" / record_id /
                             "record.json").read_text())
        text, input_ids = ids_from_record(tok, args.model, record)
        n = input_ids.shape[1]
        requested = list(args.positions or [])
        starts = assistant_starts(tok, args.model, record)
        if args.assistant_starts:
            requested += starts
        if args.assistant_offsets:
            requested += [p + offset for p in starts
                          for offset in args.assistant_offsets]
        if not requested:
            requested = [-1]
        pos = sorted({p % n for p in requested})
        box = {}

        def hook(_module, _inputs, output, box=box, pos=pos):
            resid = output if torch.is_tensor(output) else output[0]
            box["vectors"] = resid[0, pos].detach().float().cpu()

        handle = layers(model)[spec["layer"]].register_forward_hook(hook)
        device = model.get_input_embeddings().weight.device
        with torch.inference_mode():
            model(input_ids=input_ids.to(device), use_cache=False)
        handle.remove()

        outdir = ROOT / "results" / record_id / "nla"
        outdir.mkdir(exist_ok=True)
        suffix = f"-{args.tag}" if args.tag else ""
        path = outdir / f"{args.precision}{suffix}.pt"
        payload = {
            "schema": 1,
            "created": dt.datetime.now().astimezone().isoformat(
                timespec="seconds"),
            "record": record_id,
            "target": {"name": args.model, "repo": repo,
                       "precision": args.precision,
                       "quant": None if args.precision == "bf16"
                       else CONFIGS[args.model]["quant"],
                       "revision": getattr(model.config, "_commit_hash", None)},
            "layer": spec["layer"],
            "positions": pos,
            "tokens": [tok.decode([input_ids[0, p]]) for p in pos],
            "vectors": box["vectors"],
            "text": text,
            "selection": {
                "positions": args.positions,
                "assistant_starts": args.assistant_starts,
                "assistant_offsets": args.assistant_offsets,
            },
        }
        torch.save(payload, path)
        print(path)
        for p, token, vector in zip(
                pos, payload["tokens"], box["vectors"]):
            print(f"{p:5d} {token!r:16} norm={vector.norm():.1f}")


def meta_and_paths(spec):
    from huggingface_hub import snapshot_download

    patterns = (None if spec["mode"] == "embedding" else
                ["nla_meta.yaml", "av_sft_lora/**",
                 "av_rl_lora_step400/**"])
    root = pathlib.Path(snapshot_download(spec["av"],
                                         allow_patterns=patterns))
    if spec["mode"] == "embedding":
        return root, yaml.safe_load((root / "nla_meta.yaml").read_text())
    return root, yaml.safe_load((root / "nla_meta.yaml").read_text())


def load_av(name, root, spec):
    if spec["mode"] == "embedding":
        quant = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16)
        model = AutoModelForCausalLM.from_pretrained(
            root, device_map="cuda:0", dtype=torch.bfloat16,
            quantization_config=quant)
        return AutoTokenizer.from_pretrained(root), model

    from peft import PeftModel

    base = AutoModelForCausalLM.from_pretrained(
        CONFIGS[name]["hf_id"], device_map="cuda:0", dtype=torch.bfloat16)
    sft, rl = root / "av_sft_lora", root / "av_rl_lora_step400"
    torch.cuda.empty_cache()
    model = PeftModel.from_pretrained(
        base, sft, adapter_name="sft", low_cpu_mem_usage=True)
    torch.cuda.empty_cache()
    model.load_adapter(
        rl, adapter_name="rl", low_cpu_mem_usage=True)
    model.base_model.set_adapter(["sft", "rl"], inference_mode=True)
    torch.cuda.empty_cache()
    return AutoTokenizer.from_pretrained(sft), model


def template_ids(tok, meta, mode):
    key = "av" if mode == "embedding" else "actor"
    char = meta["tokens"]["injection_char"]
    content = meta["prompt_templates"][key].format(injection_char=char)
    enc = tok.apply_chat_template(
        [{"role": "user", "content": content}], tokenize=True,
        add_generation_prompt=True, return_tensors="pt")
    return (enc.input_ids if hasattr(enc, "input_ids") else enc).to("cuda")


def marker(meta, ids):
    token = meta["tokens"]
    found = []
    for p in (ids[0] == token["injection_token_id"]).nonzero().flatten():
        p = p.item()
        if (0 < p < ids.shape[1] - 1 and
                ids[0, p - 1] == token["injection_left_neighbor_id"] and
                ids[0, p + 1] == token["injection_right_neighbor_id"]):
            found.append(p)
    if len(found) != 1:
        raise RuntimeError(f"found {len(found)} valid NLA markers")
    return found[0]


def generation_args(max_new, temperature, seed):
    torch.manual_seed(seed)
    out = {"max_new_tokens": max_new,
           "do_sample": temperature > 0}
    if temperature > 0:
        out["temperature"] = temperature
    return out


def embedding_decode(model, tok, meta, vector, max_new, temperature, seed):
    ids = template_ids(tok, meta, "embedding")
    p = marker(meta, ids)
    vector = vector.to("cuda").float()
    scale = meta["extraction"]["injection_scale"]
    vector *= scale / vector.norm()
    with torch.inference_mode():
        embeds = model.get_input_embeddings()(ids).clone()
        embeds[0, p] = vector.to(embeds.dtype)
        out = model.generate(
            inputs_embeds=embeds, attention_mask=torch.ones_like(ids),
            **generation_args(max_new, temperature, seed),
            pad_token_id=tok.pad_token_id, eos_token_id=tok.eos_token_id)
    return tok.decode(out[0], skip_special_tokens=False)


def karvonen_decode(model, tok, meta, vector, max_new, temperature, seed):
    ids = template_ids(tok, meta, "karvonen")
    marker(meta, ids)
    state = {}

    def embed_hook(_module, args, kwargs, output):
        state["ids"] = kwargs.get("input") if kwargs else None
        if state["ids"] is None and args:
            state["ids"] = args[0]
        return output

    def layer_hook(_module, _inputs, output):
        resid, *rest = list(output) if isinstance(output, tuple) else [output]
        current = state.get("ids")
        if current is None or resid.shape[1] < 2:
            return output
        current = current.to(resid.device)
        p = marker(meta, current)
        out = resid.clone()
        h = out[0, p].clone()
        v = vector.to(out.device, out.dtype)
        out[0, p] = h + h.norm() * v / (v.norm() + 1e-9)
        return (out, *rest) if isinstance(output, tuple) else out

    h1 = model.get_input_embeddings().register_forward_hook(
        embed_hook, with_kwargs=True)
    h2 = layers(model)[1].register_forward_hook(layer_hook)
    start = ids.shape[1]
    with torch.inference_mode():
        out = model.generate(
            input_ids=ids, **generation_args(max_new, temperature, seed),
            pad_token_id=tok.pad_token_id, eos_token_id=tok.eos_token_id)
    h1.remove()
    h2.remove()
    return tok.decode(out[0, start:], skip_special_tokens=False)


def decode(args):
    inputs = [(path, torch.load(path, weights_only=False))
              for path in args.path]
    names = {data["target"]["name"] for _, data in inputs}
    if len(names) != 1:
        raise RuntimeError("all captures must use the same target model")
    name = names.pop()
    spec = NLA[name]
    root, meta = meta_and_paths(spec)
    tok, model = load_av(name, root, spec)
    model.eval()

    for path, data in inputs:
        samples = []
        wanted = None
        if args.sample_indices:
            wanted = {i % len(data["positions"]) for i in args.sample_indices}
        for i, (pos, token, vector) in enumerate(zip(
                data["positions"], data["tokens"], data["vectors"])):
            if args.positions and pos not in args.positions:
                continue
            if wanted is not None and i not in wanted:
                continue
            for draw in range(args.draws):
                seed = args.seed + draw
                raw = (embedding_decode if spec["mode"] == "embedding"
                       else karvonen_decode)(
                           model, tok, meta, vector, args.max_new,
                           args.temperature, seed)
                match = EXPLANATION.search(raw)
                samples.append(
                    {"position": pos, "token": token, "draw": draw,
                     "seed": seed, "raw": raw,
                     "explanation": match.group(1).strip()
                     if match else None})
                print(f"\n[{data['record']} · {pos} {token!r} · "
                      f"draw {draw}]\n{raw}")

        out = {
            "schema": 1,
            "created": dt.datetime.now().astimezone().isoformat(
                timespec="seconds"),
            "record": data["record"],
            "capture": path.name,
            "target": data["target"] | {"layer": data["layer"]},
            "verbalizer": {"repo": spec["av"], "mode": spec["mode"],
                           "revision": root.name,
                           "precision": "nf4" if name == "gemma-12b"
                           else "pre-nf4 + sft/rl lora"},
            "sampling": {
                "draws": args.draws, "temperature": args.temperature,
                "seed": args.seed, "max_new_tokens": args.max_new},
            "samples": samples,
        }
        suffix = f"-{args.output_tag}" if args.output_tag else ""
        output = path.with_name(f"{path.stem}{suffix}.json")
        output.write_text(json.dumps(out, indent=1))
        print(f"\n{output}")


def compare(args):
    a = torch.load(args.reference, weights_only=False)
    b = torch.load(args.candidate, weights_only=False)
    if a["positions"] != b["positions"] or a["tokens"] != b["tokens"]:
        raise RuntimeError("capture positions or tokens differ")
    x, y = a["vectors"].float(), b["vectors"].float()
    cos = torch.nn.functional.cosine_similarity(x, y, dim=1)
    rel = (y - x).norm(dim=1) / x.norm(dim=1)
    ratio = y.norm(dim=1) / x.norm(dim=1)
    unit_x = torch.nn.functional.normalize(x, dim=1)
    unit_y = torch.nn.functional.normalize(y, dim=1)
    if len(x) > 1:
        cx = unit_x - unit_x.mean(0)
        cy = unit_y - unit_y.mean(0)
        k, l = cx @ cx.T, cy @ cy.T
        cka = ((k * l).sum() /
               ((k.square().sum() * l.square().sum()).sqrt() + 1e-12)).item()
    else:
        cka = None
    rows = [
        {"position": p, "token": token, "cosine": c.item(),
         "relative_l2": r.item(), "norm_ratio": nr.item()}
        for p, token, c, r, nr in
        zip(a["positions"], a["tokens"], cos, rel, ratio)
    ]
    out = {
        "schema": 1,
        "reference": str(args.reference),
        "candidate": str(args.candidate),
        "n": len(rows),
        "mean_cosine": cos.mean().item(),
        "mean_relative_l2": rel.mean().item(),
        "mean_norm_ratio": ratio.mean().item(),
        "linear_cka_unit": cka,
        "positions": rows,
    }
    path = args.output or args.candidate.parent / "transfer.json"
    path.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


def score(args):
    from huggingface_hub import snapshot_download
    from safetensors.torch import load_file

    docs = [(path, json.loads(path.read_text())) for path in args.path]
    names = {doc["target"]["name"] for _, doc in docs}
    if names != {"gemma-12b"}:
        raise SystemExit("local AR scoring currently supports gemma-12b")
    repo = "kitft/nla-gemma3-12b-L32-ar"
    root = pathlib.Path(snapshot_download(repo))
    meta = yaml.safe_load((root / "nla_meta.yaml").read_text())
    tok = AutoTokenizer.from_pretrained(root)
    model = AutoModelForCausalLM.from_pretrained(
        root, device_map="cuda:0", dtype=torch.bfloat16)
    model.eval()
    d = model.config.hidden_size
    head = torch.nn.Linear(d, d, bias=False, dtype=torch.bfloat16).to("cuda")
    head.load_state_dict(load_file(str(root / "value_head.safetensors")))
    head.eval()
    scale = float(meta["extraction"]["mse_scale"])
    template = meta["prompt_templates"]["ar"]
    entries = []
    for path, doc in docs:
        capture_path = path.parent / doc.get("capture",
                                             path.with_suffix(".pt").name)
        capture = torch.load(capture_path, weights_only=False)
        vectors = dict(zip(capture["positions"], capture["vectors"]))
        for sample in doc["samples"]:
            explanation = sample.get("explanation")
            if not explanation:
                sample["reconstruction"] = None
                continue
            entries.append((doc, sample, vectors[sample["position"]].float()))

    def reconstruct(explanation):
        ids = tok(template.format(explanation=explanation),
                  return_tensors="pt",
                  add_special_tokens=True).input_ids.to("cuda")
        box = {}

        def hook(_module, _inputs, output):
            resid = output if torch.is_tensor(output) else output[0]
            box["h"] = resid[0, -1]

        handle = layers(model)[-1].register_forward_hook(hook)
        with torch.inference_mode():
            model(input_ids=ids, use_cache=False)
            pred = head(box["h"]).float().cpu()
        handle.remove()
        return pred / pred.norm().clamp_min(1e-12) * scale

    preds = [reconstruct(sample["explanation"])
             for _doc, sample, _gold in entries]
    blank = reconstruct("")
    for i, (doc, sample, gold) in enumerate(entries):
        gn = gold / gold.norm().clamp_min(1e-12) * scale
        cosine = torch.nn.functional.cosine_similarity(
            preds[i], gn, dim=0).item()
        key = (doc["record"], sample["position"])
        null = [
            torch.nn.functional.cosine_similarity(preds[j], gn, dim=0).item()
            for j, (other_doc, other_sample, _other_gold)
            in enumerate(entries)
            if j != i and
            (other_doc["record"], other_sample["position"]) != key
        ]
        null_mean = sum(null) / len(null) if null else None
        blank_cos = torch.nn.functional.cosine_similarity(
            blank, gn, dim=0).item()
        sample["reconstruction"] = {
            "cosine": cosine,
            "direction_mse": 2 * (1 - cosine),
            "shuffled_mean_cosine": null_mean,
            "blank_cosine": blank_cos,
            "advantage": cosine - null_mean if null else None,
        }

    for path, doc in docs:
        doc["reconstructor"] = {
            "repo": repo, "revision": root.name, "precision": "bf16"}
        path.write_text(json.dumps(doc, indent=1))
        print(path)
        for sample in doc["samples"]:
            print(sample["position"], sample["reconstruction"])


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(required=True)
    cap = sub.add_parser("capture")
    cap.add_argument("model", choices=NLA)
    cap.add_argument("--record", nargs="+", required=True)
    cap.add_argument("-p", "--positions", nargs="+", type=int)
    cap.add_argument("--assistant-starts", action="store_true")
    cap.add_argument("--assistant-offsets", nargs="+", type=int)
    cap.add_argument("--precision", choices=["repo", "bf16"], default="repo")
    cap.add_argument("--tag")
    cap.add_argument("--allow-large-bf16", action="store_true",
                     help="only on a host that can fit full Qwen 27B")
    cap.set_defaults(fn=capture)
    dec = sub.add_parser("decode")
    dec.add_argument("path", nargs="+", type=pathlib.Path)
    dec.add_argument("--max-new", type=int, default=256)
    dec.add_argument("--draws", type=int, default=1)
    dec.add_argument("--temperature", type=float, default=0.0)
    dec.add_argument("--seed", type=int, default=0)
    dec.add_argument("--output-tag")
    dec.add_argument("-p", "--positions", nargs="+", type=int)
    dec.add_argument("--sample-indices", nargs="+", type=int)
    dec.set_defaults(fn=decode)
    cmp = sub.add_parser("compare")
    cmp.add_argument("reference", type=pathlib.Path)
    cmp.add_argument("candidate", type=pathlib.Path)
    cmp.add_argument("-o", "--output", type=pathlib.Path)
    cmp.set_defaults(fn=compare)
    scr = sub.add_parser("score")
    scr.add_argument("path", nargs="+", type=pathlib.Path)
    scr.set_defaults(fn=score)
    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
