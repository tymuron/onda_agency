#!/usr/bin/env python3
"""Generate AVIF derivatives for every webp under assets/.
Re-run after adding/replacing any image:  cd frontend && python3 build_images.py
AVIF is ~25-40% smaller than webp; the <picture> markup falls back to webp.
Higher quality for the founder portraits (skin tones show AVIF artifacts first)."""
from PIL import Image
import glob, os

def quality_for(src):
    return 64 if "/team/" in src.replace("\\", "/") else 60

made = 0
for src in sorted(glob.glob("assets/**/*.webp", recursive=True)):
    dst = src[:-5] + ".avif"
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        continue
    Image.open(src).convert("RGB").save(dst, format="AVIF", quality=quality_for(src), speed=4)
    w = os.path.getsize(src); a = os.path.getsize(dst)
    print(f"{os.path.basename(src):32} {w//1024:4}KB -> {a//1024:4}KB  ({100-a*100//w:>3}% smaller)")
    made += 1
print(f"done: {made} AVIF written")
