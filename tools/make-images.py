#!/usr/bin/env python3
"""
Generate TOP Reno raster assets: favicons, apple-touch-icon, and the
Open Graph social-share card.

Run from the repo root:  python3 tools/make-images.py
Requires Pillow:         pip3 install Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

INK = (13, 14, 16)
ORANGE = (255, 90, 31)
WHITE = (255, 255, 255)
SMOKE = (139, 145, 154)
LINE = (40, 44, 51)

DISPLAY = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
BODY = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
BODY_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def chevrons(draw, cx, cy, half_w, gap, weight, top_color, bottom_color):
    """Two stacked chevrons — the TOP Reno mark. (cx, cy) is the mark's centre."""
    rise = half_w * 0.86
    for i, color in enumerate((top_color, bottom_color)):
        apex_y = cy - gap / 2 + i * gap - rise / 2
        draw.line(
            [
                (cx - half_w, apex_y + rise),
                (cx, apex_y),
                (cx + half_w, apex_y + rise),
            ],
            fill=color,
            width=weight,
            joint="curve",
        )


def make_icon(size, path, pad_ratio=0.16):
    """Square app icon: dark tile with the chevron mark centred."""
    scale = 4  # supersample for clean edges
    img = Image.new("RGB", (size * scale, size * scale), INK)
    d = ImageDraw.Draw(img)
    s = size * scale
    half_w = s * (0.5 - pad_ratio) * 0.92
    weight = max(2, int(s * 0.115))
    gap = s * 0.30
    chevrons(d, s / 2, s / 2, half_w, gap, weight, ORANGE, WHITE)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(path)
    print("wrote", os.path.relpath(path, ROOT))


def make_og(path):
    """1200x630 Open Graph card."""
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # Blueprint grid
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=LINE, width=1)
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=LINE, width=1)

    # Corner glow block, top right
    d.rectangle([W - 300, 0, W, 8], fill=ORANGE)

    # Mark + wordmark
    chevrons(d, 92, 108, 34, 30, 11, ORANGE, WHITE)
    f_word = font(DISPLAY, 62)
    d.text((140, 76), "TOP", font=f_word, fill=WHITE)
    w = d.textlength("TOP", font=f_word)
    d.text((140 + w + 12, 76), "RENO", font=f_word, fill=ORANGE)

    # Eyebrow
    f_eye = font(BODY, 22)
    d.line([(72, 205), (110, 205)], fill=ORANGE, width=3)
    d.text((122, 193), "MARKETING FOR THE TRADES", font=f_eye, fill=ORANGE)

    # Headline
    f_h = font(DISPLAY, 82)
    lines = [
        "QUOTE-READY LEADS FOR",
        "ONTARIO HVAC, ROOFING",
        "& PLUMBING CONTRACTORS",
    ]
    y = 246
    for ln in lines:
        d.text((72, y), ln, font=f_h, fill=WHITE)
        y += 88

    # Footer rule + URL
    d.line([(72, H - 96), (W - 72, H - 96)], fill=LINE, width=2)
    f_foot = font(BODY, 26)
    d.text((72, H - 74), "topreno.co", font=f_foot, fill=WHITE)
    f_foot_r = font(BODY_REG, 24)
    tail = "Brand  ·  Growth  ·  Operations"
    tw = d.textlength(tail, font=f_foot_r)
    d.text((W - 72 - tw, H - 72), tail, font=f_foot_r, fill=SMOKE)

    # Hazard stripe along the bottom
    stripe_h = 14
    for i in range(-H, W + H, 40):
        d.polygon(
            [
                (i, H),
                (i + 20, H),
                (i + 20 + stripe_h, H - stripe_h),
                (i + stripe_h, H - stripe_h),
            ],
            fill=ORANGE,
        )

    img.save(path, quality=92)
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    make_icon(16, os.path.join(OUT, "favicon-16.png"), pad_ratio=0.10)
    make_icon(32, os.path.join(OUT, "favicon-32.png"), pad_ratio=0.12)
    make_icon(180, os.path.join(OUT, "apple-touch-icon.png"))
    make_icon(192, os.path.join(OUT, "icon-192.png"))
    make_icon(512, os.path.join(OUT, "icon-512.png"))
    make_og(os.path.join(OUT, "og-image.png"))
