#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BG = "#0D1117"
PANEL = "#111827"
TEXT = "#E5E7EB"
MUTED = "#94A3B8"
ACCENT = "#38BDF8"


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_frame(image_path: Path, title: str, subtitle: str) -> Image.Image:
    source = Image.open(image_path).convert("RGB")
    source = source.resize((1200, 675))

    canvas = Image.new("RGB", (1280, 820), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((24, 24, 1256, 796), radius=24, fill=PANEL, outline="#1F2937", width=2)
    canvas.paste(source, (40, 110))

    title_font = load_font(34)
    sub_font = load_font(20)
    meta_font = load_font(18)

    draw.text((40, 42), title, fill=TEXT, font=title_font)
    draw.text((40, 76), subtitle, fill=MUTED, font=sub_font)
    draw.text(
        (1200, 76),
        datetime.now(UTC).strftime("captured %Y-%m-%d UTC"),
        fill=ACCENT,
        font=meta_font,
        anchor="ra",
    )
    return canvas


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: build_demo_gif.py <capture-dir> <output-gif>")

    capture_dir = Path(argv[0])
    output_gif = Path(argv[1])
    manifest = json.loads((capture_dir / "manifest.json").read_text(encoding="utf-8"))
    frames = []

    for item in manifest:
        if not item.get("ok"):
            continue
        frame = build_frame(
            capture_dir / item["fileName"],
            "Live Sites Demo",
            f'{item["name"]}  ·  {item["url"]}',
        )
        frames.append(frame)

    if not frames:
        raise SystemExit("no successful screenshots captured")

    output_gif.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=2200,
        loop=0,
        optimize=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

