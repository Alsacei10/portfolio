# -*- coding: utf-8 -*-
"""Optimize project screenshots: PNG -> WebP (max width 1280, q82), then remove PNG."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_W = 1280
QUALITY = 82

def optimize(png_path):
    im = Image.open(png_path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, im).convert("RGB")
    else:
        im = im.convert("RGB")
    w, h = im.size
    if w > MAX_W:
        im = im.resize((MAX_W, int(h * MAX_W / w)), Image.LANCZOS)
    webp_path = os.path.splitext(png_path)[0] + ".webp"
    im.save(webp_path, "WEBP", quality=QUALITY, method=6)
    return webp_path, os.path.getsize(webp_path)

total_before = total_after = 0
converted = 0
for root, _dirs, files in os.walk(os.path.join(ROOT, "projects")):
    for f in sorted(files):
        if f.lower().endswith(".png"):
            png = os.path.join(root, f)
            size_before = os.path.getsize(png)
            total_before += size_before
            webp, size_after = optimize(png)
            total_after += size_after
            os.remove(png)
            converted += 1
            print("%-28s %6.0f KB -> %6.0f KB" % (f, size_before / 1024, size_after / 1024))

print("converted %d images: %.2f MB -> %.2f MB" % (converted, total_before / 1024 / 1024, total_after / 1024 / 1024))
