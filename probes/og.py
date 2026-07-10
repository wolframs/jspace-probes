"""Generate Open Graph images (1200x630 PNG) for jspace-probes.vercel.app.

Reads results/index.json and writes og/site.png plus one og/<id>.png per
record. Each record card renders a "core sample" glyph — a bar strip
derived from the record's per-layer emergence ranks — as its unique visual
signature, echoing dashboard/app.js's glyph() rendering.

Run after probes/site.py / lab.py reindex when records change:
    .venv/bin/python probes/og.py
"""

import json
import math
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "results" / "index.json"
OUT_DIR = ROOT / "og"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
FONT_SANS = FONT_DIR / "DejaVuSans.ttf"
FONT_SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
FONT_MONO = FONT_DIR / "DejaVuSansMono.ttf"
for _p in (FONT_SANS, FONT_SANS_BOLD, FONT_MONO):
    if not _p.exists():
        raise SystemExit(f"required font missing: {_p}")

W, H = 1200, 630
MARGIN = 56

BG = (13, 13, 13)  # #0d0d0d
INK = (255, 255, 255)  # #ffffff
SECONDARY = (195, 194, 183)  # #c3c2b7
MUTED = (137, 135, 129)  # #898781
VIOLET = (144, 133, 233)  # #9085e9
GRID = (44, 44, 42)  # #2c2c2a, dashboard --grid (dark theme)

QUANT_DEFAULT = {"gemma-4b": "bf16", "gemma-12b": "8bit", "qwen-27b": "pre-4bit"}


@lru_cache(maxsize=None)
def font(path, size):
    return ImageFont.truetype(str(path), size)


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def fit_title(draw, text, max_width, max_lines, sizes):
    """Try decreasing font sizes until the wrapped text fits max_lines."""
    for size in sizes:
        fnt = font(FONT_SANS_BOLD, size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(FONT_SANS_BOLD, sizes[-1])
    lines = wrap_text(draw, text, fnt, max_width)[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=fnt) > max_width:
        last = last[:-1]
    lines[-1] = last.rstrip() + "…"
    return fnt, lines


def truncate_line(draw, text, fnt, max_width):
    if draw.textlength(text, font=fnt) <= max_width:
        return text
    t = text
    while t and draw.textlength(t + "…", font=fnt) > max_width:
        t = t[:-1]
    return t.rstrip() + "…"


def draw_wordmark(draw, x, y):
    draw.text((x, y), "◎ J-Space Probes", font=font(FONT_SANS_BOLD, 22), fill=VIOLET)
    draw.text(
        (x, y + 30),
        "reading silent thoughts through the Jacobian lens",
        font=font(FONT_SANS, 14),
        fill=MUTED,
    )


def draw_footer(draw):
    fnt = font(FONT_MONO, 14)
    text = "jspace-probes.vercel.app"
    w = draw.textlength(text, font=fnt)
    draw.text((W - MARGIN - w, H - 34), text, font=fnt, fill=MUTED)


def draw_strip(draw, x0, y0, x1, y1, ranks):
    draw.rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], fill=GRID)
    n = len(ranks)
    if n == 0:
        return
    width = x1 - x0
    bw = width / n
    for i, rank in enumerate(ranks):
        rank = max(1, rank)
        intensity = max(0.0, 1 - math.log10(rank) / 5)
        color = lerp_color(BG, VIOLET, intensity)
        bx0 = x0 + i * bw
        bx1 = x0 + (i + 1) * bw
        draw.rectangle([bx0, y0, bx1, y1], fill=color)


def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def save(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


def render_record(rec):
    img, draw = new_canvas()
    draw_wordmark(draw, MARGIN, 46)

    title_top = 150
    title_font, title_lines = fit_title(
        draw, rec["title"], W - 2 * MARGIN, 3, [58, 50, 44, 38, 32, 28]
    )
    line_h = int(title_font.size * 1.18)
    y = title_top
    for line in title_lines:
        draw.text((MARGIN, y), line, font=title_font, fill=INK)
        y += line_h
    y += 14

    quant = rec.get("quant") or QUANT_DEFAULT.get(rec.get("model"), "fp16")
    chips = f"{rec.get('model')} · {quant} · unit {rec.get('unit')} · {(rec.get('created') or '')[:10]}"
    chip_font = font(FONT_MONO, 18)
    draw.text((MARGIN, y), chips, font=chip_font, fill=MUTED)
    y += 34

    gen = rec.get("gen")
    if gen:
        gen_font = font(FONT_MONO, 18)
        flat = " ".join(gen.split())
        quoted = f"“{flat}”"
        line = truncate_line(draw, quoted, gen_font, W - 2 * MARGIN)
        draw.text((MARGIN, y), line, font=gen_font, fill=SECONDARY)

    strip_h = 60
    strip_y1 = H - 44
    strip_y0 = strip_y1 - strip_h
    draw_strip(draw, MARGIN, strip_y0, W - MARGIN, strip_y1, rec.get("emergence") or [])

    draw_footer(draw)
    save(img, OUT_DIR / f"{rec['id']}.png")


def render_site(records):
    img, draw = new_canvas()

    title_font = font(FONT_SANS_BOLD, 84)
    title = "◎ J-Space Probes"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 200), title, font=title_font, fill=INK)

    sub_font = font(FONT_SANS, 22)
    subtitle = (
        f"{len(records)} experiment records · Jacobian-lens readouts · "
        "three models, one RTX 3090"
    )
    sw = draw.textlength(subtitle, font=sub_font)
    draw.text(((W - sw) / 2, 296), subtitle, font=sub_font, fill=MUTED)

    by_id = {r["id"]: r for r in records}
    strip_rec = by_id.get("u13-sorry-abl-real-q27b") or (records[0] if records else None)
    strip_h = 60
    strip_y1 = H - 44
    strip_y0 = strip_y1 - strip_h
    draw_strip(
        draw, MARGIN, strip_y0, W - MARGIN, strip_y1,
        (strip_rec.get("emergence") if strip_rec else []) or [],
    )

    draw_footer(draw)
    save(img, OUT_DIR / "site.png")


def main():
    records = json.loads(INDEX.read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    render_site(records)
    for rec in records:
        render_record(rec)

    print(f"wrote {len(records) + 1} images to og/")


if __name__ == "__main__":
    main()
