#!/usr/bin/env python3
"""Generate frontend/og-image.png (1200x630) on-brand.

Regenerable. The user can replace the output with a designed asset later.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "frontend" / "og-image.png"
W, H = 1200, 630
BG = (10, 10, 10)
ACCENT = (59, 130, 246)
WHITE = (250, 250, 250)
MUTED = (161, 161, 170)

ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


img = Image.new("RGB", (W, H), BG)

# Soft accent glow (top-left), blurred for a premium feel.
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
gd.ellipse([-260, -320, 620, 360], fill=(20, 44, 92))
glow = glow.filter(ImageFilter.GaussianBlur(170))
img = Image.blend(img, glow, 0.9)

draw = ImageDraw.Draw(img)

# Brand sine wave (the "onda" / wave motif), accent colour.
pts = []
for x in range(90, 360):
    y = 150 + 26 * math.sin((x - 90) / 30.0)
    pts.append((x, y))
draw.line(pts, fill=ACCENT, width=7, joint="curve")

# Wordmark.
draw.text((88, 196), "ONDA", font=font(ARIAL_BOLD, 132), fill=WHITE)

# Headline.
draw.text((90, 360), "Fast premium websites", font=font(ARIAL_BOLD, 60), fill=WHITE)
draw.text((90, 426), "for service businesses.", font=font(ARIAL_BOLD, 60), fill=WHITE)

# Sub / URL row.
draw.text(
    (90, 520),
    "Web design  ·  Landing pages  ·  Automation",
    font=font(ARIAL, 28),
    fill=MUTED,
)
draw.text((90, 562), "agencyonda.com", font=font(ARIAL_BOLD, 30), fill=ACCENT)

# Hairline frame.
draw.rectangle([6, 6, W - 7, H - 7], outline=(38, 38, 42), width=2)

img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, {W}x{H})")
