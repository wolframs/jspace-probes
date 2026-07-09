"""Scan a J-space slice for candidate concepts.

Runs the lens over every position of a (optionally chat-templated, optionally
generated) sequence and reports, for each candidate word, its best rank across
the (position, layer) grid — i.e. "was this concept present anywhere in
J-space, and where?" Also prints the top lens tokens at the strongest cells.

Usage:
    python probes/scan.py --model gemma-4b --chat --generate 25 \
        --prompt "..." --candidates sloth frog owl deer bear
"""

import argparse

import torch

from probe import CONFIGS, load  # noqa: F401  (shared loader)


def candidate_token_ids(tok, words: list[str]) -> dict[str, list[int]]:
    """Map each candidate word to plausible single-token encodings."""
    ids: dict[str, list[int]] = {}
    for w in words:
        variants = {w, w.lower(), w.capitalize(), " " + w.lower(), " " + w.capitalize()}
        tids = set()
        for v in variants:
            enc = tok(v, add_special_tokens=False).input_ids
            if len(enc) == 1:
                tids.add(enc[0])
        if tids:
            ids[w] = sorted(tids)
    return ids


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=CONFIGS, required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--candidates", nargs="+", required=True)
    p.add_argument("--chat", action="store_true")
    p.add_argument("--generate", type=int, default=0)
    p.add_argument("--rank-threshold", type=int, default=50,
                   help="report cells where a candidate ranks better than this")
    args = p.parse_args()

    model, tok, lens = load(args.model)

    def strip_bos(s: str) -> str:
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
        print("\n--- model response ---")
        print(tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True))
        print("----------------------")
        text = strip_bos(tok.decode(out[0], skip_special_tokens=False))

    cand_ids = candidate_token_ids(tok, args.candidates)
    missing = [w for w in args.candidates if w not in cand_ids]
    if missing:
        print(f"(no single-token encoding, skipped: {missing})")

    lens_logits, _, input_ids = lens.apply(model, text, positions=None)
    toks = [tok.decode([t]) for t in input_ids[0]]
    n = len(toks)

    # best rank per candidate over the whole grid
    print(f"\nSequence has {n} positions, {len(lens_logits)} lens layers.")
    print(f"\n{'candidate':<14} {'best rank':>9}  at (pos, layer)  token")
    hits = {}
    for word, tids in cand_ids.items():
        best = (10**9, None, None)
        per_cell = []
        for layer, logits in lens_logits.items():  # [n, vocab]
            ranks = (logits.argsort(dim=-1, descending=True) ==
                     torch.tensor(tids).view(-1, 1, 1)).nonzero()
            # ranks rows: [tid_idx, pos, rank]
            for _, pos, r in ranks.tolist():
                per_cell.append((r, pos, layer))
                if r < best[0]:
                    best = (r, pos, layer)
        hits[word] = sorted(per_cell)[:400]
        r, pos, layer = best
        loc = f"({pos}, {layer})" if pos is not None else "-"
        at_tok = toks[pos] if pos is not None else ""
        print(f"{word:<14} {r:>9}  {loc:<16} {at_tok!r}")

    # detail: for each candidate with a strong hit, show where it persists
    thr = args.rank_threshold
    for word, cells in hits.items():
        strong = [c for c in cells if c[0] < thr]
        if not strong:
            continue
        print(f"\n{word!r} cells with rank < {thr} (rank, pos, layer):")
        by_pos: dict[int, list] = {}
        for r, pos, layer in strong:
            by_pos.setdefault(pos, []).append((layer, r))
        for pos in sorted(by_pos):
            spans = ", ".join(f"L{l}:{r}" for l, r in sorted(by_pos[pos])[:12])
            print(f"  pos {pos:>3} {toks[pos]!r:<18} {spans}")


if __name__ == "__main__":
    main()
