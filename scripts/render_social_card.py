#!/usr/bin/env python3
"""Render the GitHub Launch Studio social card (1280x640 PNG)."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH, HEIGHT = 1280, 640


def font(paths: list[str], size: int) -> ImageFont.FreeTypeFont:
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def bold(size: int) -> ImageFont.FreeTypeFont:
    return font(
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        ],
        size,
    )


def regular(size: int) -> ImageFont.FreeTypeFont:
    return font(
        [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        ],
        size,
    )


def rounded_panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def render(output: Path) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#07111f")
    pixels = image.load()
    top = (8, 19, 36)
    bottom = (13, 31, 54)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(WIDTH):
            pixels[x, y] = color

    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((690, -210, 1420, 520), fill=(56, 189, 248, 70))
    glow_draw.ellipse((-260, 300, 460, 900), fill=(52, 211, 153, 42))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    image = Image.alpha_composite(image.convert("RGBA"), glow)
    draw = ImageDraw.Draw(image)

    # Decorative launch panel on the right.
    rounded_panel(draw, (760, 118, 1160, 500), 30, (255, 255, 255, 20))
    draw.rounded_rectangle((760, 118, 1160, 500), radius=30, outline=(255, 255, 255, 45), width=2)
    draw.text((805, 158), "LAUNCH READINESS", font=bold(22), fill=(166, 244, 224, 255))

    bars = [
        ("Clarity", 4.2, "#34d399"),
        ("Activation", 4.0, "#38bdf8"),
        ("Trust", 4.0, "#a78bfa"),
        ("Proof", 2.6, "#fbbf24"),
    ]
    y = 220
    for label, value, color in bars:
        draw.text((805, y - 8), label, font=regular(20), fill=(226, 232, 240, 255))
        draw.rounded_rectangle((805, y + 28, 1065, y + 42), radius=7, fill=(255, 255, 255, 35))
        width = int(260 * value / 5)
        draw.rounded_rectangle((805, y + 28, 805 + width, y + 42), radius=7, fill=color)
        draw.text((1080, y + 18), f"{value:.1f}", font=bold(20), fill=(241, 245, 249, 255))
        y += 62

    checklist_rows = [
        (["Plan", "Quickstart"], 430),
        (["Demo", "Release"], 470),
    ]
    for checklist, y in checklist_rows:
        x = 805
        for item in checklist:
            w = int(draw.textlength(item, font=bold(15))) + 34
            draw.rounded_rectangle((x, y, x + w, y + 32), radius=16, fill=(52, 211, 153, 35), outline=(52, 211, 153, 110), width=1)
            draw.ellipse((x + 10, y + 10, x + 20, y + 20), fill=(52, 211, 153, 255))
            draw.line((x + 13, y + 15, x + 16, y + 19, x + 22, y + 11), fill=(4, 24, 18, 255), width=2)
            draw.text((x + 27, y + 7), item, font=bold(15), fill=(220, 252, 231, 255))
            x += w + 10

    # Main copy.
    draw.rounded_rectangle((84, 88, 440, 126), radius=19, fill=(52, 211, 153, 32), outline=(52, 211, 153, 105), width=1)
    draw.text((105, 97), "CODEX SKILL FOR OPEN SOURCE", font=bold(17), fill=(167, 243, 208, 255))

    draw.text((82, 174), "Make your GitHub", font=bold(68), fill=(248, 250, 252, 255))
    draw.text((82, 258), "repo launch-ready.", font=bold(68), fill=(248, 250, 252, 255))
    draw.rounded_rectangle((84, 270, 438, 282), radius=6, fill=(52, 211, 153, 210))

    subtitle = "Positioning · README · demo assets · release notes · bilingual launch"
    draw.text((84, 374), subtitle, font=regular(27), fill=(203, 213, 225, 255))

    draw.text((84, 520), "MJorgin/github-launch-studio", font=bold(24), fill=(226, 232, 240, 255))
    draw.text((84, 556), "Audit real repository evidence. Publish only after approval.", font=regular(20), fill=(148, 163, 184, 255))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the GitHub Launch Studio social card")
    parser.add_argument("--output", type=Path, default=Path("assets/social-card.png"))
    args = parser.parse_args()
    render(args.output)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
