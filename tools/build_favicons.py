#!/usr/bin/env python3
"""Render bitmap fallbacks for the vector linked-diamond site mark.

Pillow is needed only when changing the mark, not for ordinary site builds.
Coordinates match assets/favicon.svg; 8x supersampling preserves small sizes.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
scale = 8
image = Image.new('RGBA', (64 * scale, 64 * scale), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((0, 0, 64 * scale - 1, 64 * scale - 1), radius=16 * scale, fill='#173e3b')
for points, colour in [([(24,16),(40,32),(24,48),(8,32),(24,16)], '#fafcf7'),
                        ([(40,16),(56,32),(40,48),(24,32),(40,16)], '#b7d8bd')]:
    draw.line([(x * scale, y * scale) for x,y in points], fill=colour, width=4 * scale, joint='curve')
for size in [32, 180]:
    icon = image.resize((size,size), Image.Resampling.LANCZOS)
    icon.save(ROOT / 'assets' / ('favicon-32.png' if size == 32 else 'apple-touch-icon.png'))
image.resize((64,64), Image.Resampling.LANCZOS).save(ROOT / 'favicon.ico', sizes=[(16,16),(32,32),(48,48),(64,64)])
print('Rendered favicon.ico, 32px PNG and touch icon.')
