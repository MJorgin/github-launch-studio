#!/usr/bin/env python3
"""Render a short, reproducible GitHub Launch Studio demo.

Visual concept: "launch preflight field manual". Warm paper, ink, one
cinnabar accent, a persistent readiness rail running through every scene,
and a final "CLEARED FOR LAUNCH" stamp. The film deliberately avoids the
generic dark-neon dashboard look: the product's core deliverable is a
Markdown report, so the whole film speaks the document/checklist language.

The animation is generated instead of screen-recorded: deterministic, CI
reproducible, no private terminal history and no local paths.
"""

from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1280
HEIGHT = 720
FPS = 20
DURATION = 30
TOTAL_FRAMES = FPS * DURATION

# ---------------------------------------------------------------- palette

PAPER = (244, 240, 230)
SHEET = (252, 250, 244)
INK = (26, 24, 21)
INK2 = (92, 85, 74)
INK3 = (150, 143, 128)
RULE = (221, 214, 197)
CINNABAR = (204, 63, 36)
CINNABAR_DARK = (170, 48, 26)
OCHRE = (173, 119, 22)
PINE = (47, 105, 74)
CODE = (25, 23, 20)
CODE_PAPER = (237, 232, 221)
CODE_DIM = (140, 133, 118)
PINE_ON_DARK = (126, 189, 152)

AVENIR = "/System/Library/Fonts/Supplemental/Avenir Next.ttc"
HIRAGANA = "/System/Library/Fonts/Hiragino Sans GB.ttc"
MENLO = "/System/Library/Fonts/Menlo.ttc"


def f(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size, index=index)


FONTS = {
    "h1": f(AVENIR, 64, 8),        # Heavy
    "h2": f(AVENIR, 36, 2),        # Demi Bold
    "h3": f(AVENIR, 23, 5),        # Medium
    "score_big": f(AVENIR, 96, 8),
    "score_cta": f(AVENIR, 46, 8),
    "body": f(AVENIR, 18, 7),      # Regular
    "body_m": f(AVENIR, 18, 5),    # Medium
    "small": f(AVENIR, 15, 7),
    "small_m": f(AVENIR, 15, 5),
    "small_d": f(AVENIR, 15, 2),
    "tiny": f(AVENIR, 13, 7),
    "mono": f(MENLO, 18, 0),
    "mono_b": f(MENLO, 18, 1),
    "mono_s": f(MENLO, 15, 0),
    "mono_sb": f(MENLO, 15, 1),
    "mono_xs": f(MENLO, 12, 0),
    "mono_xsb": f(MENLO, 12, 1),
    "cn": f(HIRAGANA, 18, 0),
    "cn_b": f(HIRAGANA, 18, 2),
}

CONTENT_X = 236
CONTENT_R = 1216
RAIL_X = 108
RAIL_Y0 = 170
STEP_LABELS = ["AUDIT", "REPORT", "PACKAGE", "BENCHMARK", "COPY", "LAUNCH"]


# ------------------------------------------------------------------ math

def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def ease_out(v: float) -> float:
    v = clamp(v)
    return 1 - (1 - v) ** 3


def ease_in_out(v: float) -> float:
    v = clamp(v)
    return 0.5 - 0.5 * math.cos(math.pi * v)


def ease_out_back(v: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    v = clamp(v)
    return 1 + c3 * (v - 1) ** 3 + c1 * (v - 1) ** 2


# ---------------------------------------------------------------- drawing

def tracked(draw, xy, value, fnt, fill, tracking: int = 1):
    x, y = xy
    for ch in value:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += int(draw.textlength(ch, font=fnt)) + tracking


def tracked_w(draw, value, fnt, tracking: int = 1) -> int:
    return sum(int(draw.textlength(ch, font=fnt)) for ch in value) + tracking * max(0, len(value) - 1)


def wrap(draw, value, fnt, max_w):
    lines, cur = [], ""
    for word in value.split():
        cand = word if not cur else f"{cur} {word}"
        if draw.textlength(cand, font=fnt) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def sheet(draw, box, radius: int = 5):
    """A document sheet: warm white, near-sharp corners, soft tan shadow."""
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 2, y1 + 5, x2 + 2, y2 + 7), radius=radius, fill=(90, 76, 52, 20))
    draw.rounded_rectangle((x1 + 1, y1 + 2, x2 + 1, y2 + 3), radius=radius, fill=(90, 76, 52, 12))
    draw.rounded_rectangle(box, radius=radius, fill=SHEET, outline=RULE, width=1)


def tag(draw, x, y, value, fg, bg=None, border=None, fnt=None, pad_x=9, h=23):
    fnt = fnt or FONTS["mono_xsb"]
    w = tracked_w(draw, value, fnt, 1) + pad_x * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=3, fill=bg, outline=border, width=1 if border else 0)
    tracked(draw, (x + pad_x, y + (h - fnt.size) // 2 - 1), value, fnt, fg, 1)
    return w


def check_mark(draw, x, y, color, scale: float = 1.0, w: int = 2):
    s = scale
    draw.line((x, y + 6 * s, x + 5 * s, y + 11 * s, x + 15 * s, y - 2 * s), fill=color, width=w, joint="curve")


def cross_mark(draw, x, y, color, scale: float = 1.0):
    s = scale
    draw.line((x, y, x + 13 * s, y + 13 * s), fill=color, width=2)
    draw.line((x + 13 * s, y, x, y + 13 * s), fill=color, width=2)


def gauge(draw, x_right, y, value, appear, color):
    """Five-segment readiness mark, shared by Report and CTA."""
    seg_w, seg_h, gap = 30, 11, 7
    x0 = x_right - (5 * seg_w + 4 * gap)
    for i in range(5):
        x = x0 + i * (seg_w + gap)
        active = appear > 0 and i < value
        draw.rounded_rectangle((x, y, x + seg_w, y + seg_h), radius=2,
                               fill=color if active else RULE)


# ------------------------------------------------------------- background

def make_background() -> Image.Image:
    rng = random.Random(711)
    # Fine paper grain at low resolution, then gently enlarged.
    grain = Image.new("L", (320, 180))
    gp = grain.load()
    for y in range(180):
        for x in range(320):
            gp[x, y] = rng.randint(112, 150)
    grain = grain.resize((WIDTH, HEIGHT), Image.BILINEAR)

    img = Image.new("RGBA", (WIDTH, HEIGHT), PAPER + (255,))
    img.alpha_composite(Image.merge("RGBA", (Image.new("L", (WIDTH, HEIGHT), 0),) * 3
                                    + (grain.point(lambda p: int(p * 0.055)),)))
    # Soft edge falloff, like light across a page.
    vignette = Image.radial_gradient("L").resize((WIDTH + 400, HEIGHT + 400))
    vmask = vignette.point(lambda p: int(max(0, (140 - p) / 140 * 26)))
    shade = Image.new("RGBA", (WIDTH + 400, HEIGHT + 400), (70, 58, 38, 0))
    shade.putalpha(vmask)
    img.alpha_composite(shade, (-200, -200))
    return img


BASE = make_background()


# ----------------------------------------------------------------- chrome

def chrome(img, active=None, fill_active: bool = False):
    """Spine title + persistent preflight rail + page divider."""
    draw = ImageDraw.Draw(img)
    spine = Image.new("RGBA", (300, 26), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spine)
    tracked(sd, (0, 6), "GITHUB LAUNCH STUDIO", FONTS["mono_xs"], INK2, 2)
    spine = spine.rotate(90, expand=True)
    img.alpha_composite(spine, (24, 250))

    draw.line((RAIL_X, RAIL_Y0 + 4, RAIL_X, RAIL_Y0 + 400 - 4), fill=RULE, width=2)
    if active is not None and active > 0:
        draw.line((RAIL_X, RAIL_Y0, RAIL_X, RAIL_Y0 + active * 80), fill=CINNABAR, width=3)
    for i, label in enumerate(STEP_LABELS):
        y = RAIL_Y0 + i * 80
        done = i < active if active is not None else False
        current = i == active
        if current and fill_active:
            done = True
            current = False
        if done:
            draw.ellipse((RAIL_X - 10, y - 10, RAIL_X + 10, y + 10), fill=CINNABAR)
            check_mark(draw, RAIL_X - 5, y - 3, PAPER, scale=0.62, w=2)
            draw.text((128, y - 9), label, font=FONTS["mono_xsb"], fill=INK)
        elif current:
            draw.ellipse((RAIL_X - 10, y - 10, RAIL_X + 10, y + 10), fill=SHEET, outline=CINNABAR, width=3)
            draw.ellipse((RAIL_X - 3, y - 3, RAIL_X + 3, y + 3), fill=CINNABAR)
            draw.text((128, y - 9), label, font=FONTS["mono_xsb"], fill=INK)
        else:
            draw.ellipse((RAIL_X - 9, y - 9, RAIL_X + 9, y + 9), fill=PAPER, outline=(202, 194, 178), width=2)
            draw.text((128, y - 9), label, font=FONTS["mono_xs"], fill=INK3)
    draw.line((216, 104, 216, 660), fill=RULE, width=1)


# ---------------------------------------------------------------- scenes

def draw_intro(img, p):
    d = ImageDraw.Draw(img)
    chrome(img)
    tracked(d, (CONTENT_X, 148), "OPEN-SOURCE LAUNCH PREFLIGHT", FONTS["mono_xs"], CINNABAR, 2)

    d.text((CONTENT_X - 3, 196), "Your code is ready.", font=FONTS["h1"], fill=INK)
    d.text((CONTENT_X - 3, 280), "Is your launch ready?", font=FONTS["h1"], fill=CINNABAR)

    body = "A ten-minute audit that turns a working repository into a launch-ready open-source project."
    for i, line in enumerate(wrap(d, body, FONTS["body"], 540)):
        d.text((CONTENT_X, 392 + i * 28), line, font=FONTS["body"], fill=INK2)

    box = (808, 146, 1216, 456)
    sheet(d, box)
    tracked(d, (834, 176), "PREFLIGHT CHECKLIST", FONTS["mono_xs"], INK2, 2)
    d.line((834, 202, 1190, 202), fill=RULE, width=1)
    rows = [
        ("Positioning", PINE, "check"),
        ("README & quickstart", PINE, "check"),
        ("Proof & demo", CINNABAR, "cross"),
        ("Trust signals", PINE, "check"),
        ("Release copy", OCHRE, "warn"),
    ]
    for i, (label, color, kind) in enumerate(rows):
        a = ease_out((p - 0.24 - i * 0.1) / 0.3)
        if a <= 0:
            continue
        y = 224 + i * 44 + int(6 * (1 - a))
        if kind == "check":
            check_mark(d, 836, y, color)
        elif kind == "cross":
            cross_mark(d, 838, y - 1, color)
        else:
            d.ellipse((835, y - 2, 851, y + 14), outline=color, width=2)
            d.line((843, y + 2, 843, y + 8), fill=color, width=2)
        d.text((868, y - 4), label, font=FONTS["small_m"], fill=INK)

    d.line((CONTENT_X, 572, CONTENT_R, 572), fill=RULE, width=1)
    tracked(d, (CONTENT_X, 592), "AUDIT  >  REPORT  >  PACKAGE  >  BENCHMARK  >  COPY  >  LAUNCH",
            FONTS["mono_xs"], INK2, 1)


def draw_terminal(img, p):
    d = ImageDraw.Draw(img)
    chrome(img, 0)
    box = (CONTENT_X, 132, CONTENT_R, 452)
    d.rounded_rectangle(box, radius=6, fill=CODE)
    x1, y1, x2, y2 = box
    d.ellipse((x1 + 24, y1 + 21, x1 + 36, y1 + 33), fill=(72, 66, 56))
    d.ellipse((x1 + 46, y1 + 21, x1 + 58, y1 + 33), fill=(72, 66, 56))
    d.ellipse((x1 + 68, y1 + 21, x1 + 80, y1 + 33), fill=(72, 66, 56))
    d.text((x1 + 100, y1 + 17), "bash - launch-audit", font=FONTS["mono_s"], fill=CODE_DIM)
    d.line((x1, y1 + 52, x2, y1 + 52), fill=(52, 47, 40), width=1)

    line1 = "$ launch-audit ./suno-v6-cookbook"
    line2 = "  --output LAUNCH.md --markdown"
    s = p * DURATION
    # Human-ish terminal rhythm: ~55ms/char with two short thinking pauses.
    schedule = []
    t = 0.25
    for idx, ch in enumerate(line1):
        t += 0.05
        if idx == 15:
            t += 0.18
        schedule.append((t, 0, ch))
    for idx, ch in enumerate(line2):
        t += 0.05
        if idx == 2:
            t += 0.10
        schedule.append((t, 1, ch))

    shown = ["", ""]
    for ct, line_idx, ch in schedule:
        if ct <= s:
            shown[line_idx] += ch
    typing_done = s >= t
    tx, ty = x1 + 34, y1 + 92
    d.text((tx, ty), shown[0], font=FONTS["mono"], fill=CODE_PAPER)
    d.text((tx, ty + 34), shown[1], font=FONTS["mono"], fill=CODE_PAPER)

    active_line = 1 if shown[0] == line1 else 0
    if not typing_done:
        cx = tx + int(d.textlength(shown[active_line], font=FONTS["mono"]))
        d.rectangle((cx + 1, ty + active_line * 34 + 3, cx + 11, ty + active_line * 34 + 24), fill=CINNABAR)
    elif int(s * 2) % 2 == 0:
        cx = tx + int(d.textlength(line2, font=FONTS["mono"]))
        d.rectangle((cx + 1, ty + 37, cx + 11, ty + 58), fill=CINNABAR)

    out_t = t + 0.3
    if s >= out_t:
        a = ease_out((s - out_t) / 0.25)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ly = 330
        ld.line((x1 + 24, ly - 22, x2 - 24, ly - 22), fill=(52, 47, 40), width=1)
        check_mark(ld, x1 + 28, ly - 2, PINE_ON_DARK)
        ld.text((x1 + 56, ly - 10), "LAUNCH.md written", font=FONTS["mono_sb"], fill=CODE_PAPER)
        ld.text((x1 + 56, ly + 22), "6 dimensions scored - 2 high-priority findings - read-only scan",
                font=FONTS["mono_xs"], fill=CODE_DIM)
        img.alpha_composite(layer)

    d.text((CONTENT_X, 488), "One command produces a shareable Markdown report:",
           font=FONTS["small"], fill=INK2)
    tracked(d, (CONTENT_X + 414, 490), "SCORES . EVIDENCE . RISKS . NEXT ACTIONS",
            FONTS["mono_xs"], CINNABAR_DARK, 1)


def _gauge_rows(d, x_label, x_right, ys, data, p, start, stagger):
    for i, (label, value) in enumerate(data):
        a = ease_out((p - start - i * stagger) / 0.32)
        if a <= 0:
            continue
        y = ys + i * 54 + int(7 * (1 - a))
        color = CINNABAR if value <= 2 else OCHRE if value == 3 else PINE
        d.text((x_label, y - 2), label, font=FONTS["small_d"], fill=INK)
        gauge(d, x_right, y + 3, value, a, color)
        d.text((x_right + 14, y - 3), f"{value}/5", font=FONTS["mono_xsb"], fill=INK)
        if i < len(data) - 1:
            d.line((x_label, y + 32, x_right + 52, y + 32), fill=RULE, width=1)


def draw_report(img, p):
    d = ImageDraw.Draw(img)
    chrome(img, 1)
    sheet(d, (CONTENT_X, 108, CONTENT_R, 652))
    tracked(d, (264, 134), "LAUNCH.MD", FONTS["mono_xs"], CINNABAR, 2)
    name = "suno-v6-cookbook"
    d.text((1192 - int(d.textlength(name, font=FONTS["mono_xs"])), 135), name,
           font=FONTS["mono_xs"], fill=INK3)
    d.line((264, 166, 1188, 166), fill=RULE, width=1)

    a = ease_out(p / 0.35)
    score_v = 2.3 * a
    d.text((260, 196), f"{score_v:.1f}", font=FONTS["score_big"], fill=CINNABAR)
    d.text((446, 266), "/ 5.0", font=FONTS["mono_s"], fill=INK3)
    tag(d, 264, 318, "NOT CLEARED", PAPER, bg=CINNABAR, fnt=FONTS["mono_xsb"], h=24)
    for i, line in enumerate(["Public traffic will expose", "weak activation and thin proof."]):
        d.text((264, 366 + i * 24), line, font=FONTS["small"], fill=INK2)

    d.line((520, 196, 520, 614), fill=RULE, width=1)
    tracked(d, (548, 192), "SIX READINESS DIMENSIONS", FONTS["mono_xs"], INK3, 2)
    data = [
        ("Clarity", 3),
        ("Activation", 1),
        ("Trust", 3),
        ("Proof", 1),
        ("Distribution", 4),
        ("Maintenance", 2),
    ]
    _gauge_rows(d, 548, 836, 234, data, p, 0.12, 0.07)

    d.line((912, 196, 912, 614), fill=RULE, width=1)
    tracked(d, (940, 192), "TOP FINDINGS", FONTS["mono_xs"], INK3, 2)
    findings = [
        ("HIGH", CINNABAR, "README quickstart is not copy-pasteable", "Add a fenced, tested first command."),
        ("MEDIUM", OCHRE, "No CI workflow detected", "Automate or document release QA."),
    ]
    for i, (sev, color, title_text, fix) in enumerate(findings):
        fa = ease_out((p - 0.42 - i * 0.16) / 0.25)
        if fa <= 0:
            continue
        y = 234 + i * 190
        tag(d, 940, y, sev, PAPER, bg=color, fnt=FONTS["mono_xsb"], h=22)
        for j, line in enumerate(wrap(d, title_text, FONTS["small_d"], 240)):
            d.text((940, y + 36 + j * 21), line, font=FONTS["small_d"], fill=INK)
        for j, line in enumerate(wrap(d, fix, FONTS["small"], 240)):
            d.text((940, y + 96 + j * 20), line, font=FONTS["small"], fill=INK2)
        if i == 0:
            d.line((940, y + 166, 1188, y + 166), fill=RULE, width=1)


def draw_package(img, p):
    d = ImageDraw.Draw(img)
    chrome(img, 2)
    d.text((CONTENT_X - 3, 108), "Smallest convincing launch set", font=FONTS["h2"], fill=INK)
    d.text((CONTENT_X, 158), "Everything a stranger needs on the path from curiosity to first success.",
           font=FONTS["small"], fill=INK2)

    items = [
        ("01", "Positioning", "A first-time visitor understands it in ten seconds."),
        ("02", "Quickstart", "One copy-paste command that actually works."),
        ("03", "Real example", "Real input, real output, expected result."),
        ("04", "Proof", "GIF, screenshots, CI badge and honest limits."),
        ("05", "Trust", "License, security policy and issue templates."),
        ("06", "Support", "A clear path to ask questions and contribute."),
    ]
    for i, (num, title_text, desc) in enumerate(items):
        col, row = i % 2, i // 2
        x = CONTENT_X + col * 510
        y = 232 + row * 132
        a = ease_out((p - i * 0.06) / 0.3)
        if a <= 0:
            continue
        y += int(10 * (1 - a))
        d.text((x, y), num, font=FONTS["mono_b"], fill=CINNABAR)
        d.text((x + 56, y - 4), title_text, font=FONTS["h3"], fill=INK)
        d.text((x + 56, y + 34), desc, font=FONTS["small"], fill=INK2)
        d.line((x, y + 86, x + 430, y + 86), fill=RULE, width=1)
        if p > 0.52 + i * 0.06:
            check_mark(d, x + 412, y - 2, PINE)


def draw_benchmark(img, p):
    d = ImageDraw.Draw(img)
    chrome(img, 3)
    d.text((CONTENT_X - 3, 104), "Benchmarked against tools devs already use", font=FONTS["h2"], fill=INK)
    d.text((CONTENT_X, 154), "Launch Studio complements them - it prepares the human side of launch.",
           font=FONTS["small"], fill=INK2)

    tracked(d, (CONTENT_X, 208), "TOOL", FONTS["mono_xs"], INK2, 2)
    tracked(d, (480, 208), "ALREADY STRONG AT", FONTS["mono_xs"], INK2, 2)
    tracked(d, (880, 208), "LAUNCH STUDIO ADDS", FONTS["mono_xs"], CINNABAR, 2)
    d.line((CONTENT_X, 236, CONTENT_R, 236), fill=INK, width=2)

    rows = [
        ("README editors", "Filling README sections", "Positioning, evidence, activation"),
        ("semantic-release", "Versioning and changelogs", "The human-facing launch story"),
        ("Star History", "Post-launch star trends", "Pre-launch gap detection"),
        ("Agent dev kits", "Structured coding flow", "A specialized launch workflow"),
    ]
    for i, (tool, strong, adds) in enumerate(rows):
        a = ease_out((p - 0.1 - i * 0.14) / 0.28)
        if a <= 0:
            continue
        y = 262 + i * 82 + int(8 * (1 - a))
        d.line((CONTENT_X, y - 16, CONTENT_R, y - 16), fill=RULE, width=1)
        d.text((CONTENT_X, y), tool, font=FONTS["small_d"], fill=INK)
        d.text((480, y), strong, font=FONTS["small"], fill=INK2)
        d.text((880, y), adds, font=FONTS["small_m"], fill=INK)
        # cinnabar plus sign
        d.rectangle((1192, y + 3, 1206, y + 15), fill=CINNABAR)
        d.rectangle((1196, y - 1, 1202, y + 19), fill=CINNABAR)
    tracked(d, (CONTENT_X, 610), "SCOPE: READINESS - NOT RELEASE AUTOMATION, NOT GROWTH HACKS",
            FONTS["mono_xs"], INK3, 1)


def _draft_card(img, p, box, platform, lines, cn=False, start=0.05):
    d = ImageDraw.Draw(img)
    x1, y1, x2, y2 = box
    sheet(d, box)
    tag(d, x1 + 24, y1 + 22, platform, INK, bg=None, border=INK, fnt=FONTS["mono_xsb"], h=24)
    d.line((x1 + 24, y1 + 60, x2 - 24, y1 + 60), fill=RULE, width=1)

    fnt = FONTS["cn"] if cn else FONTS["body_m"]
    lh = 30
    n = len(lines)
    for i, line in enumerate(lines):
        la = ease_out((p - start - i * 0.075) / 0.12)
        if la <= 0:
            continue
        y = y1 + 84 + i * lh
        if line:
            d.text((x1 + 24, y), line, font=fnt, fill=INK)
        if i < n - 1 and p < start + (i + 1) * 0.075 + 0.12:
            cw = int(d.textlength(line, font=fnt))
            d.rectangle((x1 + 28 + cw, y + 4, x1 + 36 + cw, y + 23), fill=CINNABAR)

    fa = ease_out((p - start - n * 0.075 - 0.12) / 0.25)
    if fa > 0:
        d.line((x1 + 24, y2 - 48, x2 - 24, y2 - 48), fill=RULE, width=1)
        tag(d, x2 - 152, y2 - 36, "READY FOR REVIEW", PINE, border=PINE, fnt=FONTS["mono_xs"], h=22)


def draw_copy(img, p):
    d = ImageDraw.Draw(img)
    chrome(img, 4)
    d.text((CONTENT_X - 3, 104), "Bilingual launch pack", font=FONTS["h2"], fill=INK)
    d.text((CONTENT_X, 154), "Drafts queued for your review. The skill never posts on your behalf.",
           font=FONTS["small"], fill=INK2)

    en = [
        "GitHub Launch Studio for OSS",
        "launch day: an audit of",
        "positioning, quickstart, proof,",
        "benchmarks and release notes.",
        "",
        "Offline report. Never auto-posts.",
    ]
    cn = [
        "做了个 Codex Skill：给开源项目",
        "做 GitHub 发布前体检。",
        "",
        "离线扫描仓库，输出六维评分、",
        "优先问题、LAUNCH.md 报告与",
        "中英文发布文案，全部待你确认。",
    ]
    _draft_card(img, p, (CONTENT_X, 196, 702, 604), "X / ENGLISH", en, start=0.05)
    _draft_card(img, p, (742, 196, 1208, 604), "V2EX / 中文", cn, cn=True, start=0.18)


def _stamp(scale, alpha):
    w, h = 268, 150
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    col = CINNABAR + (alpha,)
    sd.rounded_rectangle((8, 8, w - 8, h - 8), radius=6, outline=col, width=4)
    sd.rounded_rectangle((17, 17, w - 17, h - 17), radius=4, outline=col, width=1)
    f1, f2 = f(MENLO, 27, 1), f(MENLO, 22, 1)
    t1, t2 = "CLEARED FOR", "LAUNCH"
    sd.text(((w - tracked_w(sd, t1, f1, 2)) / 2, 34), t1, font=f1, fill=col)
    sd.text(((w - tracked_w(sd, t2, f2, 4)) / 2, 76), t2, font=f2, fill=col)

    # Deterministic ink distress.
    rng = random.Random(907)
    px = layer.load()
    for _ in range(1400):
        x, y = rng.randrange(w), rng.randrange(h)
        r, g, b, a = px[x, y]
        if a:
            px[x, y] = (r, g, b, int(a * rng.uniform(0.55, 1.0)))
    if scale != 1:
        layer = layer.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.BICUBIC)
    return layer.rotate(-8, expand=True, resample=Image.BICUBIC)


def draw_cta(img, p):
    d = ImageDraw.Draw(img)
    stamped = p > 0.62
    chrome(img, 5, fill_active=stamped)

    tracked(d, (CONTENT_X, 150), "PREFLIGHT COMPLETE", FONTS["mono_xs"], CINNABAR, 2)
    d.text((CONTENT_X - 3, 188), "Audit before", font=FONTS["h1"], fill=INK)
    d.text((CONTENT_X - 3, 272), "you launch.", font=FONTS["h1"], fill=CINNABAR)
    d.text((CONTENT_X, 380), "A Codex skill that makes repositories launch-ready, not just code-ready.",
           font=FONTS["small"], fill=INK2)

    d.rounded_rectangle((CONTENT_X, 460, 766, 518), radius=6, fill=CODE)
    url = "github.com/MJorgin/github-launch-studio"
    d.text((CONTENT_X + 22, 478), url, font=FONTS["mono_s"], fill=CODE_PAPER)
    if int(p * 16) % 2 == 0:
        cx = CONTENT_X + 26 + int(d.textlength(url, font=FONTS["mono_s"]))
        d.rectangle((cx, 476, cx + 9, 498), fill=CINNABAR)
    tracked(d, (CONTENT_X, 560), "OFFLINE AUDIT . MARKDOWN REPORT . 30-SEC DEMO . NEVER AUTO-POSTS",
            FONTS["mono_xs"], INK3, 1)

    sheet(d, (812, 146, 1216, 560))
    tracked(d, (838, 172), "LAUNCH SCORE", FONTS["mono_xs"], CINNABAR, 2)
    sa = ease_out((p - 0.08) / 0.35)
    d.text((836, 204), f"{4.4 * sa:.1f}", font=FONTS["score_cta"], fill=PINE)
    d.text((948, 232), "/ 5.0", font=FONTS["mono_s"], fill=INK3)
    after = [("Clarity", 4), ("Activation", 4), ("Trust", 5), ("Proof", 4), ("Distribution", 4)]
    for i, (label, value) in enumerate(after):
        a = ease_out((p - 0.16 - i * 0.07) / 0.3)
        if a <= 0:
            continue
        y = 306 + i * 46
        d.text((838, y - 2), label, font=FONTS["small_m"], fill=INK)
        gauge(d, 1150, y + 3, value, a, PINE)
        if i < 4:
            d.line((838, y + 30, 1188, y + 30), fill=RULE, width=1)

    if stamped:
        q = ease_out_back((p - 0.62) / 0.16)
        scale = 1.35 - 0.35 * q
        alpha = int(235 * clamp((p - 0.62) / 0.06))
        stamp = _stamp(scale * 0.94, alpha)
        img.alpha_composite(stamp, (1016 - stamp.width // 2, 462 - stamp.height // 2))


SCENES = [
    (3.0, draw_intro),
    (5.0, draw_terminal),
    (5.0, draw_report),
    (5.0, draw_package),
    (4.0, draw_benchmark),
    (4.0, draw_copy),
    (4.0, draw_cta),
]


def scene_fade(img, progress, first=False):
    fade_in = ease_in_out(progress / (0.04 if first else 0.08))
    if first:
        fade_in = 0.5 + 0.5 * fade_in
    fade_out = ease_in_out((1 - progress) / 0.05)
    alpha = int(255 * min(fade_in, fade_out))
    if alpha >= 255:
        return img
    veil = Image.new("RGBA", (WIDTH, HEIGHT), PAPER + (255 - alpha,))
    return Image.alpha_composite(img, veil)


def render_frame(index):
    t = index / FPS
    elapsed = 0.0
    for duration, renderer in SCENES:
        if t < elapsed + duration or renderer is SCENES[-1][1]:
            img = BASE.copy()
            local_p = clamp((t - elapsed) / duration)
            renderer(img, local_p)
            return scene_fade(img, local_p, first=(index == 0)).convert("RGB")
        elapsed += duration
    return BASE.convert("RGB")


def run(command):
    subprocess.run(command, check=True)


def render(mp4_path, gif_path=None, keep_frames=False):
    frames_dir = Path(tempfile.mkdtemp(prefix="launch-demo-"))
    try:
        for index in range(TOTAL_FRAMES):
            render_frame(index).save(frames_dir / f"frame_{index:04d}.png", optimize=False)

        mp4_path.parent.mkdir(parents=True, exist_ok=True)
        run([
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-crf", "18",
            str(mp4_path),
        ])

        if gif_path:
            palette = frames_dir / "palette.png"
            run([
                "ffmpeg", "-y",
                "-i", str(mp4_path),
                "-vf", "fps=12,scale=1024:576:flags=lanczos,palettegen=stats_mode=full",
                str(palette),
            ])
            run([
                "ffmpeg", "-y",
                "-i", str(mp4_path),
                "-i", str(palette),
                "-lavfi", "fps=12,scale=1024:576:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5",
                str(gif_path),
            ])
    finally:
        if not keep_frames:
            shutil.rmtree(frames_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Render the GitHub Launch Studio demo")
    parser.add_argument("--mp4", type=Path, default=Path("assets/launch-demo.mp4"))
    parser.add_argument("--gif", type=Path, default=Path("assets/launch-demo.gif"))
    parser.add_argument("--keep-frames", action="store_true")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        parser.error("ffmpeg is required to render the demo")
    render(args.mp4, args.gif, args.keep_frames)
    print(args.mp4.resolve())
    if args.gif:
        print(args.gif.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
