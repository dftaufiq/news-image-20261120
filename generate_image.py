#!/usr/bin/env python3
"""Build-time generator for entry.png: a one-page newspaper front page summing
up the world's news of Friday 20 November 2026.

Drawn from scratch with Pillow (build-time only; the entry program main.py is
standard-library only and just copies the finished entry.png). Every story in
it was verified against news reporting of 20 November 2026; see SOURCES in the
footer of the image and README.md.

Run:  python3 generate_image.py            (writes entry.png next to this file)
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).with_name("entry.png")

# --- palette: newsprint -----------------------------------------------------------------
PAPER = (248, 244, 236)
INK = (18, 18, 18)
NAVY = (16, 32, 61)
NAVY_LIGHT = (24, 48, 88)
RED = (178, 28, 28)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
RULE = (200, 192, 176)
STRIP = (232, 236, 241)
TAG_COLORS = {
    "JUSTICE": (126, 34, 34),
    "DIPLOMACY": (24, 64, 110),
    "WEATHER": (14, 116, 144),
    "WAR": (126, 34, 34),
    "CONFLICT": (126, 34, 34),
    "POLITICS": (24, 64, 110),
    "CLIMATE": (21, 101, 52),
    "ENERGY": (146, 64, 14),
    "ECONOMY": (24, 64, 110),
    "TECH": (88, 28, 135),
    "DEFENCE": (63, 63, 70),
}

FONT_DIR = Path("/usr/share/fonts/truetype")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = "dejavu/DejaVuSerif-Bold.ttf"
SANS = "dejavu/DejaVuSans.ttf"
SANS_B = "dejavu/DejaVuSans-Bold.ttf"

# --- the day's news (verified against 20 Nov 2026 reporting) ---------------------------
LEAD1_TAG = "THE HAGUE  ·  JUSTICE"
LEAD1_HEAD = "WORLD COURT: MYANMAR GUILTY OF GENOCIDE"
LEAD1_DECK = (
    "The ICJ holds a state responsible for genocide for the first time: 9–6 over "
    "the 2017 Rohingya crackdown. Myanmar rejects it."
)
LEAD2_TAG = "SHENZHEN  ·  DIPLOMACY"
LEAD2_HEAD = "TRUMP, XI AND PUTIN SIGN PEACE DECLARATION"
LEAD2_DECK = (
    "The first US–China–Russia summit ends with a four-point joint declaration."
)
MARKETS = (
    "S&P 500 −2.0%, a fifth straight fall  ·  Nikkei −4.8%  ·  SoftBank −16%  —  "
    "while Anthropic’s Nasdaq debut closes 17% above its $83 offer price, at $97"
)
# (place, beat, headline, deck)
STORIES = [
    ("ODISHA, INDIA", "WEATHER",
     "Cyclone Akvan makes landfall",
     "More than 300,000 people evacuated as the storm crosses the coast near "
     "Gopalpur; no deaths reported."),
    ("KYIV, UKRAINE", "WAR",
     "Russia’s mass missile strike batters Kyiv",
     "Overnight barrage hits the capital; Ukraine strikes the Kerch Bridge for a "
     "third time in four days."),
    ("RIYADH", "CONFLICT",
     "Houthi missile damages Riyadh tower",
     "The sovereign wealth fund’s tower is hit in the capital’s financial district."),
    ("BRUSSELS", "POLITICS",
     "UK and EU strike landmark reset deal",
     "Youth mobility, an end to food checks and linked carbon markets agreed at "
     "the summit."),
    ("ANTALYA, TÜRKIYE", "CLIMATE",
     "COP31 draft drops fossil-fuel exit",
     "Negotiators remove any call to phase out fossil fuels from the deal."),
    ("GAZA", "CONFLICT",
     "Israeli troops cross Gaza’s Yellow Line",
     "First incursion past the ceasefire boundary in central Gaza since the truce."),
    ("STRAIT OF HORMUZ", "ENERGY",
     "Tanker struck and ablaze in Hormuz",
     "A ship catches fire after being hit in the strait as the Iran war enters "
     "its ninth month."),
    ("WASHINGTON", "ECONOMY",
     "IMF: public debt nears 100% of GDP",
     "The Fund warns global government borrowing is approaching a record high."),
    ("ROME", "TECH",
     "Italy fines Meta €805m",
     "Penalty over Android photo access; the White House fires its cyber chief "
     "after a week of outages."),
    ("ANKARA, TÜRKIYE", "DEFENCE",
     "Türkiye’s Kızılelma drone enters service",
     "The first three uncrewed combat jets are delivered to the armed forces."),
]
ALSO = (
    "ALSO TODAY  —  Haiti police report 34 suspected gang members killed  ·  "
    "Merz: no new Yalta over Europe  ·  Denmark approves Greenland–US security deal  ·  "
    "GTA 6 passes $2.3bn in sales"
)
FOOTER = "Sources: Reuters · BBC · UN News · Euronews · IMD — every story as reported on 20 November 2026"


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         max_w: int) -> list[str]:
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_globe(draw, cx, cy, r, color):
    """Stylised globe: circle, meridians, equator, two continent blobs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    draw.ellipse([cx - r * 0.55, cy - r * 0.62, cx - r * 0.05, cy - r * 0.18],
                 fill=color)
    draw.ellipse([cx + r * 0.08, cy + r * 0.12, cx + r * 0.62, cy + r * 0.58],
                 fill=color)


def draw_scales(draw, x, y, s, color):
    """Small scales-of-justice pictogram inside a s×s box at (x, y)."""
    cx, top = x + s // 2, y + s * 0.12
    base = y + s * 0.88
    draw.line([cx, top, cx, base], fill=color, width=4)
    draw.line([x + s * 0.14, top + s * 0.10, x + s * 0.86, top + s * 0.10],
              fill=color, width=4)
    for px in (x + s * 0.14, x + s * 0.86):
        draw.line([px, top + s * 0.10, px, top + s * 0.48], fill=color, width=3)
        draw.arc([px - s * 0.17, top + s * 0.42, px + s * 0.17, top + s * 0.76],
                 0, 180, fill=color, width=4)
        draw.line([px - s * 0.17, top + s * 0.59, px + s * 0.17, top + s * 0.59],
                  fill=color, width=3)
    draw.line([cx - s * 0.20, base, cx + s * 0.20, base], fill=color, width=4)
    draw.ellipse([cx - 5, top - 5, cx + 5, top + 5], fill=color)


def draw_chart_down(draw, x, y, w, h, color):
    """Small falling line chart with an arrowhead."""
    pts = [(x + w * f, y + h * (0.15 + 0.7 * f) + (6 if i % 2 else -4))
           for i, f in enumerate([0, 0.18, 0.36, 0.54, 0.72, 0.9])]
    draw.line(pts, fill=color, width=4, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex + 12, ey + 2), (ex - 2, ey - 8), (ex - 2, ey + 10)], fill=color)


def draw_cyclone(draw, cx, cy, r, color):
    """Spiral cyclone pictogram."""
    for k, rr in enumerate(range(r, 6, -7)):
        a0 = 200 + k * 55
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a0 + 230,
                 fill=color, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # page margin

    # --- masthead ----------------------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    draw_globe(d, 66, 59, 40, GOLD)
    title_f = font(SERIF_B, 54)
    d.text((122, 18), "THE WORLD TODAY", font=title_f, fill=(255, 255, 255))
    date = "FRIDAY  ·  20 NOVEMBER 2026"
    # letterspace the date by drawing it with thin spaces between letters
    spaced = " ".join(date)
    d.text((124, 82), spaced, font=font(SANS_B, 22), fill=GOLD)
    d.rectangle([0, 118, W, 124], fill=RED)

    # --- lead stories ------------------------------------------------------------------
    y0 = 142
    # lead 1 (left, wide)
    lead1_w = 600
    tag1_f = font(SANS_B, 16)
    d.text((mx, y0), LEAD1_TAG, font=tag1_f, fill=RED)
    head1_f = font(SANS_B, 40)
    y = y0 + 26
    y = draw_wrapped(d, mx, y, LEAD1_HEAD, head1_f, lead1_w, INK, 47)
    deck1_f = font(SANS, 18)
    y = draw_wrapped(d, mx, y + 8, LEAD1_DECK, deck1_f, lead1_w, INK, 25)
    # vertical rule between leads
    d.line([mx + lead1_w + 16, y0, mx + lead1_w + 16, 372], fill=RULE, width=2)
    # lead 2 (right, narrow)
    lx = mx + lead1_w + 34
    lead2_w = W - mx - lx
    d.text((lx, y0), LEAD2_TAG, font=tag1_f, fill=TAG_COLORS["DIPLOMACY"])
    head2_f = font(SANS_B, 29)
    y2 = y0 + 26
    y2 = draw_wrapped(d, lx, y2, LEAD2_HEAD, head2_f, lead2_w, INK, 35)
    deck2_f = font(SANS, 18)
    draw_wrapped(d, lx, y2 + 8, LEAD2_DECK, deck2_f, lead2_w, INK, 24)
    # three flag dots under lead 2
    fy = 360
    for i, c in enumerate([(178, 34, 52), (222, 41, 16), (0, 57, 166)]):
        d.ellipse([lx + i * 26, fy, lx + i * 26 + 16, fy + 16], fill=c)
    d.text((lx + 88, fy - 1), "USA · CHINA · RUSSIA", font=font(SANS_B, 13),
           fill=GREY)
    d.line([mx, 384, W - mx, 384], fill=INK, width=2)

    # --- markets strip -----------------------------------------------------------------
    d.rectangle([mx, 394, W - mx, 456], fill=STRIP)
    draw_chart_down(d, mx + 16, 404, 52, 40, RED)
    d.text((mx + 80, 404), "MARKETS", font=font(SANS_B, 17), fill=RED)
    draw_wrapped(d, mx + 80, 428, MARKETS, font(SANS, 16), W - 2 * mx - 96,
                 INK, 20)

    # --- story grid: 2 columns x 5 rows -------------------------------------------------
    gx, gy = mx, 474
    col_w = (W - 2 * mx - 24) // 2
    row_h = 94
    tag_f = font(SANS_B, 13)
    head_f = font(SANS_B, 20)
    deck_f = font(SANS, 15)
    for i, (place, beat, head, deck) in enumerate(STORIES):
        cx = gx + (i % 2) * (col_w + 24)
        cy = gy + (i // 2) * row_h
        if i % 2 == 1:
            d.line([cx - 12, cy + 2, cx - 12, cy + row_h - 10], fill=RULE, width=1)
        if i // 2 > 0:
            d.line([cx, cy - 6, cx + col_w, cy - 6], fill=RULE, width=1)
        color = TAG_COLORS[beat]
        d.text((cx, cy), f"{place}  ·  {beat}", font=tag_f, fill=color)
        hy = draw_wrapped(d, cx, cy + 19, head, head_f, col_w, INK, 24)
        draw_wrapped(d, cx, hy + 2, deck, deck_f, col_w, (60, 60, 60), 19)

    # --- also today + footer ------------------------------------------------------------
    ay = gy + 5 * row_h + 4
    d.line([mx, ay, W - mx, ay], fill=INK, width=2)
    draw_wrapped(d, mx, ay + 10, ALSO, font(SANS, 15), W - 2 * mx, INK, 20)
    foot_f = font(SANS, 13)
    fw = d.textlength(FOOTER, font=foot_f)
    d.text(((W - fw) / 2, H - 26), FOOTER, font=foot_f, fill=GREY)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
