"""Generate the Captain Sadjad launcher icon at all Android densities.

Run:  <bundled-python> make_icon.py
Writes app/src/main/res/mipmap-*/ic_launcher.png relative to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
RES = os.path.join(PROJECT_ROOT, "app", "src", "main", "res")

DENSITIES = [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)]

# Deep navy gradient with a gold ring and "CS" monogram.
TOP = (11, 37, 69)
BOTTOM = (19, 49, 92)
GOLD = (240, 190, 90)
GOLD_TEXT = (250, 225, 160)


def make_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Vertical gradient background.
    for y in range(size):
        t = y / max(1, size - 1)
        draw.line(
            [(0, y), (size, y)],
            fill=(
                int(TOP[0] + (BOTTOM[0] - TOP[0]) * t),
                int(TOP[1] + (BOTTOM[1] - TOP[1]) * t),
                int(TOP[2] + (BOTTOM[2] - TOP[2]) * t),
                255,
            ),
        )

    # Rounded-corner mask (legacy launchers pre-API 26).
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255
    )
    img.putalpha(mask)

    # Gold ring.
    pad = int(size * 0.16)
    ring = max(2, int(size * 0.035))
    draw.ellipse([pad, pad, size - 1 - pad, size - 1 - pad], outline=GOLD, width=ring)

    # "CS" monogram, centred.
    try:
        font = ImageFont.load_default(size=int(size * 0.34))
    except TypeError:  # very old Pillow
        font = ImageFont.load_default()
    text = "CS"
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    draw.text(
        ((size - (right - left)) / 2 - left, (size - (bottom - top)) / 2 - top),
        text,
        font=font,
        fill=GOLD_TEXT,
    )
    return img


def main():
    for density, px in DENSITIES:
        out_dir = os.path.join(RES, "mipmap-" + density)
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "ic_launcher.png")
        make_icon(px).save(path, "PNG")
        print("wrote %s (%dx%d, %d bytes)" % (path, px, px, os.path.getsize(path)))


if __name__ == "__main__":
    main()
