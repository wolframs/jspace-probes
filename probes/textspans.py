"""Assistant-turn span recovery from stored token strings, plus the
record -> lens-input rendering and film-alignment checks that every
affect capture path shares.

Torch-free on purpose: site.py imports this at every regen, and the
record pages only need the span walker, not the lens stack.
(Split out of apparatus11.py, which drags lab -> torch at import.)
Same reason template_kwargs is an argument rather than read from
CONFIGS here: probe.py imports torch.
"""

import json
from pathlib import Path

ROLE_ASSIST = {"assistant", "model"}


def assist_spans(tokens: list[str]) -> list[tuple[int, int]]:
    """Assistant-turn content spans from the stored token strings.
    Both templates store marker, role, newline, content..., end-marker;
    span = [marker+3, end) — role/newline excluded, end-marker excluded."""
    spans = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ("<|im_start|>", "<start_of_turn>"):
            role = tokens[i + 1].strip() if i + 1 < len(tokens) else ""
            end = i + 2
            while end < len(tokens) and tokens[end] not in (
                    "<|im_end|>", "<end_of_turn>"):
                end += 1
            if role in ROLE_ASSIST and i + 3 < end:
                spans.append((i + 3, end))
            i = end + 1
        else:
            i += 1
    return spans


def render_text(tok, rec: dict, template_kwargs: dict | None = None) -> str:
    """The record's exact lens input: chat template with the RECORD's
    template_kwargs (11 records ran enable_thinking, CONFIGS says off —
    always read params), or the raw stored text for chat:false records
    (re-templating those is the double-wrap bug).
    template_kwargs = the model-level CONFIGS fallback, supplied by the
    caller (this module stays torch-free)."""
    params = rec.get("params", {})
    if params.get("chat") is False:
        return rec["conversation"][0]["content"]
    tkw = params.get("template_kwargs") or template_kwargs or {}
    s = tok.apply_chat_template(rec["conversation"], tokenize=False,
                                add_generation_prompt=False, **tkw)
    bos = tok.bos_token
    return s[len(bos):] if bos and s.startswith(bos) else s


def assert_film_alignment(toks: list[str], rid: str, results_dir) -> None:
    """Token strings must equal the parent film's exactly — the ribbon
    is drawn on the film's token axis. No film = no ground truth, so
    warn and pass rather than fail."""
    fj = Path(results_dir) / rid / "film.json"
    if not fj.exists():
        print(f"  WARNING {rid}: no film.json — token alignment "
              f"NOT verified", flush=True)
        return
    film = json.loads(fj.read_text())["tokens"]
    if list(toks) == film:
        return
    i = next((k for k in range(min(len(toks), len(film)))
              if toks[k] != film[k]), min(len(toks), len(film)))
    raise ValueError(
        f"{rid}: token arrays differ from film.json — rebuilt "
        f"{len(toks)} vs film {len(film)}, first mismatch at {i}\n"
        f"  rebuilt[{i}:{i + 6}] = {toks[i:i + 6]!r}\n"
        f"  film   [{i}:{i + 6}] = {film[i:i + 6]!r}\n"
        f"  Check params/chat/template_kwargs (chat:false records must "
        f"NOT be re-templated).")
