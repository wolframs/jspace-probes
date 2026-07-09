"""Smoke test: apply Neuronpedia's pre-fitted Jacobian lens to gemma-3-4b-it.

Replicates the README's boot-shaped-country example: the lens should read out
"Euro"/"Italy"-flavoured tokens at intermediate layers before the model says
anything.
"""

import torch
import transformers

import jlens

MODEL = "google/gemma-3-4b-it"
LENS_REPO = "neuronpedia/jacobian-lens"
LENS_FILE = "gemma-3-4b-it/jlens/Salesforce-wikitext/gemma-3-4b-it_jacobian_lens.pt"

PROMPT = "Fact: The currency used in the country shaped like a boot is"


def main():
    hf = transformers.AutoModelForCausalLM.from_pretrained(
        MODEL, torch_dtype=torch.bfloat16
    ).cuda()
    tok = transformers.AutoTokenizer.from_pretrained(MODEL)
    model = jlens.from_hf(hf, tok)

    lens = jlens.JacobianLens.from_pretrained(LENS_REPO, filename=LENS_FILE)

    lens_logits, model_logits, _ = lens.apply(model, PROMPT, positions=[-1])

    print(f"\nPrompt: {PROMPT!r}")
    print(f"Model top-5 next tokens: "
          f"{[tok.decode([t]) for t in model_logits[0].topk(5).indices]}\n")
    for layer, logits in sorted(lens_logits.items()):
        top = [tok.decode([t]) for t in logits[0].topk(5).indices]
        print(f"layer {layer:>3}: {top}")


if __name__ == "__main__":
    main()
