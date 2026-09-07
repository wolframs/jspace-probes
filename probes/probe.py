"""Probe a model's J-space with a pre-fitted Neuronpedia Jacobian lens.

Usage:
    python probes/probe.py --model gemma-4b --prompt "..." \
        [--positions -1] [--html out/page.html] [--topk 5]

Models are quantized to fit the RTX 3090 (24 GB): the 12B loads in 8-bit,
the 27B in 4-bit NF4. Quantization perturbs activations slightly relative
to the full-precision model the lens was fitted on; the boot-country prompt
is a good sanity check that the lens still reads cleanly.
"""

import argparse
import pathlib

import torch
import transformers

import jlens

LENS_REPO = "neuronpedia/jacobian-lens"

CONFIGS = {
    "gemma-4b": dict(
        hf_id="google/gemma-3-4b-it",
        lens_file="gemma-3-4b-it/jlens/Salesforce-wikitext/gemma-3-4b-it_jacobian_lens.pt",
        quant=None,
    ),
    "gemma-12b": dict(
        hf_id="google/gemma-3-12b-it",
        lens_file="gemma-3-12b-it/jlens/Salesforce-wikitext/gemma-3-12b-it_jacobian_lens.pt",
        quant="8bit",
    ),
    # pre-quantized NF4 (quantization_config ships in the repo config);
    # the official-weights + on-the-fly-quant path OOMs 62GB system RAM
    "qwen-27b": dict(
        hf_id="lokeshe09/Qwen3.6-27B-bnb-4bit",
        lens_file="qwen3.6-27b/jlens/Salesforce-wikitext/Qwen3.6-27B_jacobian_lens_n1000.pt",
        quant="pre-4bit",
        # trained reasoner: without this every answer is an unbounded
        # "Thinking Process:" monologue inside an open <think> block
        template_kwargs={"enable_thinking": False},
    ),
}

# Same-lineage, readout-only comparison (triplet.py). Revisions are pinned
# before calibration; every substantive arm uses the same int8 recipe.
_Q14_LENS = "qwen3-14b/jlens/Salesforce-wikitext/Qwen3-14B_jacobian_lens.pt"
_Q14_LENS_REV = "0731326edff4ae730ffc5356fe1a4728c748b3a6"
for _name, _repo, _revision in (
    ("qwen-14b-base", "Qwen/Qwen3-14B-Base", "0b0bd3732e2c374d483664439ea334928b65f304"),
    ("qwen-14b", "Qwen/Qwen3-14B", "40c069824f4251a91eefaf281ebe4c544efd3e18"),
    ("qwen-14b-hermes", "NousResearch/Hermes-4-14B", "d6ce765c8b83f847357b98254be079afa0c6ca76"),
    ("qwen-14b-abl", "huihui-ai/Huihui-Qwen3-14B-abliterated-v2", "3b79629fdd65004d3b9cdf5beb0739e8c7e1becd"),
):
    CONFIGS[_name] = dict(hf_id=_repo, revision=_revision,
                          lens_file=_Q14_LENS, lens_revision=_Q14_LENS_REV,
                          quant="8bit", template_kwargs={"enable_thinking": False})


def load(name: str):
    cfg = CONFIGS[name]
    kwargs: dict = dict(dtype=torch.bfloat16, device_map="cuda:0")
    if cfg.get("revision"):
        kwargs["revision"] = cfg["revision"]
    if cfg["quant"] == "8bit":
        kwargs["quantization_config"] = transformers.BitsAndBytesConfig(
            load_in_8bit=True
        )
    elif cfg["quant"] == "4bit":
        kwargs["quantization_config"] = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
    hf = transformers.AutoModelForCausalLM.from_pretrained(cfg["hf_id"], **kwargs)
    tok = transformers.AutoTokenizer.from_pretrained(
        cfg["hf_id"], revision=cfg.get("revision"))
    model = jlens.from_hf(hf, tok)
    lens = jlens.JacobianLens.from_pretrained(
        LENS_REPO, filename=cfg["lens_file"], revision=cfg.get("lens_revision"))
    return model, tok, lens


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=CONFIGS, required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--positions", type=int, nargs="*", default=[-1])
    p.add_argument("--topk", type=int, default=5)
    p.add_argument("--html", help="also render an interactive slice page here")
    p.add_argument("--last-n", type=int, default=None,
                   help="slice grid only over the last N positions")
    p.add_argument("--chat", action="store_true",
                   help="wrap the prompt in the model's chat template")
    p.add_argument("--generate", type=int, default=0, metavar="N",
                   help="greedily generate N tokens first, then lens over "
                        "prompt+response so J-space is visible during the answer")
    args = p.parse_args()

    model, tok, lens = load(args.model)

    def strip_bos(s: str) -> str:
        # model.encode re-adds BOS; templated/decoded text already has one.
        bos = tok.bos_token
        return s[len(bos):] if bos and s.startswith(bos) else s

    text = args.prompt
    if args.chat:
        text = strip_bos(tok.apply_chat_template(
            [{"role": "user", "content": args.prompt}],
            tokenize=False, add_generation_prompt=True,
        ))

    if args.generate:
        ids = model.encode(text)
        out = model._hf_model.generate(
            ids, max_new_tokens=args.generate, do_sample=False
        )
        response = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)
        print(f"\n--- model response ---\n{response}\n----------------------")
        text = strip_bos(tok.decode(out[0], skip_special_tokens=False))

    lens_logits, model_logits, input_ids = lens.apply(
        model, text, positions=args.positions
    )
    toks = [tok.decode([t]) for t in input_ids[0]]
    print(f"\nPrompt tokens ({len(toks)}): {toks}")
    for i, pos in enumerate(args.positions):
        print(f"\n=== position {pos} ({toks[pos]!r}) ===")
        print(f"model output: "
              f"{[tok.decode([t]) for t in model_logits[i].topk(args.topk).indices]}")
        for layer, logits in sorted(lens_logits.items()):
            top = [tok.decode([t]) for t in logits[i].topk(args.topk).indices]
            print(f"layer {layer:>3}: {top}")

    if args.html:
        from jlens import vis

        slice_data = vis.compute_slice(
            model, lens, text, last_n_tokens=args.last_n
        )
        html, *_ = vis.build_page(
            slice_data, text,
            title=f"{args.model}: {args.prompt[:60]}",
            description=f"Jacobian lens slice for {CONFIGS[args.model]['hf_id']}",
        )
        out = pathlib.Path(args.html)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print(f"\nSlice page written to {out}")


if __name__ == "__main__":
    main()
