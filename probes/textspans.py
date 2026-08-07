"""Assistant-turn span recovery from stored token strings.

Torch-free on purpose: site.py imports this at every regen, and the
record pages only need the span walker, not the lens stack.
(Split out of apparatus11.py, which drags lab -> torch at import.)
"""

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
