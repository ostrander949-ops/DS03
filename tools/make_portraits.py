#!/usr/bin/env python3
"""Turns the painted angel portraits into web images.
Usage: python3 tools/make_portraits.py <folder of .jpg exports>
Each <slug>.jpg becomes assets/img/angels/<slug>.webp (1000px) and <slug>-640.webp (codex size).
Slugs: michael, gabriel, samael, raphael, sachiel, anael, cassiel, and paulina-<name> for the hour angels."""
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img', 'angels')
os.makedirs(OUT, exist_ok=True)
src = sys.argv[1]
for f in sorted(os.listdir(src)):
    if not f.endswith('.jpg'):
        continue
    slug = f[:-4]
    im = Image.open(os.path.join(src, f)).convert('RGB')
    w, h = im.size
    if w != h:  # square it, keeping the head: crop mostly from the bottom
        side = min(w, h)
        top = int((h - side) * 0.25) if h > w else 0
        left = (w - side) // 2
        im = im.crop((left, top, left + side, top + side))
    for size, suffix, q in ((1000, '', 80), (640, '-640', 76)):
        im.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, slug + suffix + '.webp'), 'WEBP', quality=q, method=6)
    print(slug)
