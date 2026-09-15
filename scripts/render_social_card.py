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
    top = (6, 15, 29)
    bottom = (12, 25, 43)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(WIDTH):
            pixels[x, y] = color

    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((760, -240, 1390, 420), fill=(56, 189, 248, 48))
    glow_draw.ellipse((-240, 350, 420, 870), fill=(52, 211, 153, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    image = Image.alpha_composite(image.convert("RGBA"), glow)
    draw = ImageDraw.Draw(image)

    # Subtle technical grid.
    for x in range(0, WIDTH + 1, 64):
        draw.line((x, 0, x, HEIGHT), fill=(255, 255, 255, 8), width=1)
    for y in range(0, HEIGHT + 1, 64):
        draw.line((0, y, WIDTH, y), fill=(255, 255, 255, 6), width=1)

    # Right dashboard: one dark card with generous internal padding.
    card = (744, 88, 1192, 552)
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (card[0] + 8, card[1] + 16, card[2] + 8, card[3] + 16),
        radius=32,
        fill=(0, 0, 0, 120),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    image = Image.alpha_composite(image, shadow)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(card, radius=32, fill=(13, 31, 53, 238))
    draw.rounded_rectangle(card, radius=32, outline=(255, 255, 255, 38), width=1)

    draw.ellipse((784, 128, 798, 142), fill=(52, 211, 153, 255))
    draw.text((812, 121), "LAUNCH READINESS", font=bold(22), fill=(236, 253, 245, 255))
    draw.text((784, 162), "Evidence-based repository audit", font=regular(17), fill=(148, 163, 184, 255))

    bars = [
        ("Clarity", 4.2, "#34d399"),
        ("Activation", 4.0, "#38bdf8"),
        ("Trust", 5.0, "#a78bfa"),
        ("Proof", 3.0, "#fbbf24"),
    ]
    track_left, track_right = 784, 1048
    value_right = 1152
    row_y = 214
    for label, value, color in bars:
        draw.text((track_left, row_y), label, font=bold(19), fill=(226, 232, 240, 255))
        draw.text((value_right, row_y - 1), f"{value:.1f}", font=bold(19), fill=(248, 250, 252, 255), anchor="ra")
        draw.rounded_rectangle((track_left, row_y + 34, track_right, row_y + 46), radius=6, fill=(255, 255, 255, 28))
        bar_width = int((track_right - track_left) * value / 5)
        draw.rounded_rectangle((track_left, row_y + 34, track_left + bar_width, row_y + 46), radius=6, fill=color)
        row_y += 62

    draw.line((784, 474, 1152, 474), fill=(255, 255, 255, 28), width=1)
    draw.ellipse((784, 501, 806, 523), fill=(52, 211, 153, 42), outline=(52, 211, 153, 190), width=1)
    draw.line((790, 512, 795, 517, 803, 506), fill=(167, 243, 208, 255), width=2)
    draw.text((818, 499), "Ready for a focused first launch", font=bold(18), fill=(220, 252, 231, 255))

    # Main copy.
    draw.rounded_rectangle((84, 88, 418, 128), radius=20, fill=(52, 211, 153, 28), outline=(52, 211, 153, 95), width=1)
    draw.text((106, 98), "CODEX SKILL · OPEN SOURCE", font=bold(16), fill=(167, 243, 208, 255))

    draw.text((82, 170), "Make your GitHub", font=bold(66), fill=(248, 250, 252, 255))
    draw.text((82, 248), "repo launch-ready.", font=bold(66), fill=(248, 250, 252, 255))
    draw.rounded_rectangle((84, 335, 210, 342), radius=4, fill=(52, 211, 153, 210))

    subtitle = "Positioning · README · demo assets · benchmarks · bilingual launch"
    draw.text((84, 374), subtitle, font=regular(25), fill=(203, 213, 225, 255))

    draw.text((84, 516), "MJorgin/github-launch-studio", font=bold(23), fill=(226, 232, 240, 255))
    draw.text((84, 552), "Audit real repository evidence. Publish only after approval.", font=regular(19), fill=(148, 163, 184, 255))

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
