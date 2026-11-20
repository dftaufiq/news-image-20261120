#!/usr/bin/env python3
"""Build-time generator for entry.png (v2): a one-page newspaper front page
summing up the world's news of Friday 20 November 2026.

Drawn from scratch with Pillow (build-time only; the entry program main.py is
standard-library only and just copies the finished entry.png). 35 stories, all
verified against reporting of 20 November 2026; stories from 19 November are
deliberately excluded and named in the DATE CHECK box. See README.md.

Run:  python3 generate_image.py            (writes entry.png next to this file)
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).with_name("entry.png")
MARGIN = 24
CW = W - 2 * MARGIN  # content width: 976

# --- palette ---------------------------------------------------------------------------
PAPER = (250, 246, 238)
INK = (22, 22, 22)
NAVY = (20, 40, 72)
NAVY_DK = (12, 26, 50)
RED = (176, 30, 30)
RED_DK = (140, 22, 22)
GREY = (96, 96, 96)
GREY_LT = (150, 144, 130)
RULE = (198, 190, 172)
SEA = (46, 92, 138)
LAND = (222, 206, 170)

BEATS = {  # beat tag colours
    "WAR": (158, 24, 24),
    "CYCLONE": (14, 110, 130),
    "MARKETS": (140, 24, 24),
    "DIPLOMACY": (30, 70, 130),
    "CLIMATE": (26, 110, 60),
    "SECURITY": (70, 70, 78),
    "SPACE": (96, 44, 140),
    "LABOUR": (158, 24, 24),
    "ECONOMY": (30, 70, 130),
    "CONFLICT": (158, 24, 24),
    "ENERGY": (160, 90, 10),
    "CRICKET": (26, 110, 60),
}

REGIONS = [  # (name, stories, colour) — sums to 35
    ("EUROPE", 10, (36, 84, 160)),
    ("ASIA-PACIFIC", 7, (176, 30, 30)),
    ("MIDDLE EAST", 4, (190, 124, 18)),
    ("AFRICA", 3, (30, 128, 78)),
    ("AMERICAS", 5, (118, 58, 148)),
    ("OCEANIA", 2, (18, 138, 148)),
    ("WORLD", 4, (108, 108, 108)),
]

NUMBERS = [  # (big figure, label) for the day-in-numbers strip
    ("110+", "missiles fired at Ukraine overnight"),
    ("3", "bridges hit in Kyiv"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("\u22126.2%", "Taiex at Friday's close"),
    ("100,000", "youth visas a year in the UK\u2013EU deal"),
    ("118", "Phillips' century against India"),
]

DECK = ("Russian missiles hit Kyiv's bridges \u00b7 Cyclone Akvan strikes India "
        "\u00b7 Asia's markets sink \u00b7 UK and EU seal a deal")

# --- the day's news (verified against 20 Nov 2026 reporting) ---------------------------
# leads: (number, place, beat, headline, deck, art key)
LEADS = [
    (1, "KYIV, UKRAINE", "WAR",
     "Russian missiles hit three Kyiv bridges",
     "110+ missiles and 400 drones kill at least eight across Ukraine; power "
     "and water cut in Kyiv. (Reuters, BBC)",
     "kyiv"),
    (2, "ODISHA, INDIA", "CYCLONE",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crosses near Gopalpur from 8 am; 300,000+ evacuated. No deaths "
     "reported. (IMD, The Hindu)",
     "akvan"),
    (3, "TAIPEI \u00b7 SEOUL \u00b7 TOKYO", "MARKETS",
     "AI sell-off sinks Asia's stock markets",
     "Taiex \u22126.2%, its worst week since 1991; Nikkei \u22125.1%, Kospi \u22125.2%; "
     "SoftBank \u221214.5%. (Reuters)",
     "markets"),
]

# features: (number, place, beat, headline, deck, art key)
FEATURES = [
    (4, "BRUSSELS", "DIPLOMACY",
     "UK and EU seal a \u201creset\u201d deal",
     "Food trade, visas, carbon link.",
     "ukeu"),
    (5, "ANTALYA", "CLIMATE",
     "COP31 reaches its last day with no deal",
     "Fossil fuels out of draft; overtime.",
     "cop31"),
    (6, "POLAND", "SECURITY",
     "Russian missiles land in a Polish field",
     "Two Kh-101s, a drone; no one hurt.",
     "poland"),
    (7, "SPACE", "SPACE",
     "BepiColombo reaches Mercury",
     "8-year voyage ends; orbit burn Sat.",
     "mercury"),
    (8, "ROME", "LABOUR",
     "General strike over Italy's budget",
     "A million march, CGIL says.",
     "italy"),
    (9, "TOKYO", "ECONOMY",
     "Japan's inflation picks up to 2.3%",
     "Core 2.2%; December hike in view.",
     "japan"),
    (10, "RIYADH", "CONFLICT",
     "Houthi missile damages Riyadh tower",
     "Debris hits wealth fund's tower.",
     "riyadh"),
    (11, "GAZA", "CONFLICT",
     "Israeli troops cross Gaza's Yellow Line",
     "First crossing since the truce.",
     "gaza"),
    (12, "HORMUZ", "ENERGY",
     "Tanker struck and ablaze in Hormuz",
     "Ship ablaze as the Iran war goes on.",
     "hormuz"),
    (13, "WELLINGTON", "CRICKET",
     "Phillips hits 118 against India",
     "Centuries in all 3 formats in a year.",
     "cricket"),
]

# briefs 14-35 (one line each at 11px condensed in a 320px column)
BRIEFS = [
    "ESTONIA to shut its road border with Russia (Reuters)",
    "KHARKIV Drone strike on a hospital wounds four (Reuters)",
    "BEIJING China holds lending rates at 3.0% and 3.5% (PBOC)",
    "SHENZHEN Xi hails turnaround in Australia ties (Xinhua)",
    "SEOUL Ruling party moves to impeach the chief justice (SBS)",
    "SEOUL 111 caught with devices at the Suneung exam (BBC)",
    "SAN SALVADOR Bukele registers for a third term (AP)",
    "WASHINGTON IMF: public debt nears 100% of world GDP (IMF)",
    "WASHINGTON White House fires cyber chief after outages (AP)",
    "DENMARK approves the Greenland\u2013US security deal (AFP)",
    "HAITI Police kill 34 suspected gang members in a raid (AP)",
    "GAMES GTA VI sales top $2.3bn on its first day (Sensor Tower)",
    "BRAS\u00cdLIA Lula recognises Chief Raoni's ancestral land (AP)",
    "NAIROBI US group wins Kenya's $60bn minerals deal (Reuters)",
    "SENEGAL 4 bodies found after migrant boat sinks (Al Jazeera)",
    "MALAWI Fuel crisis brings night queues at pumps (Al Jazeera)",
    "ANKARA T\u00fcrkiye's K\u0131z\u0131lelma drone enters service (Anadolu)",
    "ROME Italy fines Meta \u20ac805m over photo access (Reuters)",
    "BERLIN Merz: no new Yalta over Europe (Reuters)",
    "TONGA declares an El Ni\u00f1o drought emergency (RNZ)",
    "LAS VEGAS Russell fastest in wet GP practice (Formula1.com)",
    "TURIN ATP Finals group stage ends; semi-finals Saturday (ATP)",
]

DATE_CHECK = (
    "First reported Thursday 19 November, so NOT shown as Friday's news: the "
    "ICJ's Myanmar genocide ruling \u00b7 the Trump\u2013Xi\u2013Putin summit in Shenzhen "
    "\u00b7 Anthropic's Nasdaq debut \u00b7 the GTA VI midnight launch \u00b7 California's "
    "Nvidia subpoena \u00b7 Fiona the hippo's death. Kenya's last Ebola patient "
    "went home 11 Nov."
)

FOOTER = ("Every story here happened, or was first reported, on Friday 20 November "
          "2026. Sources named beside each story \u00b7 Original drawings")

# --- fonts -----------------------------------------------------------------------------
FONT_DIR = Path("/usr/share/fonts/truetype")
_cache = {}


def F(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(str(FONT_DIR / path), size)
    return _cache[key]


SERIF_B = "liberation/LiberationSerif-Bold.ttf"
SERIF_I = "dejavu/DejaVuSerif-Italic.ttf"
SANS = "dejavu/DejaVuSans.ttf"
SANS_B = "dejavu/DejaVuSans-Bold.ttf"
SANS_C = "dejavu/DejaVuSansCondensed.ttf"
SANS_CB = "dejavu/DejaVuSansCondensed-Bold.ttf"


# --- text helpers ----------------------------------------------------------------------
def wrap_text(d: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
              max_w: int) -> list[str]:
    """Greedy word wrap to a pixel width; returns the lines."""
    lines: list[str] = []
    line = ""
    for word in text.split(" "):
        trial = word if not line else line + " " + word
        if d.textlength(trial, font=font) <= max_w:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_lines(d: ImageDraw.ImageDraw, x: int, y: int, lines: list[str],
               font: ImageFont.FreeTypeFont, fill, leading: int) -> int:
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def draw_wrapped(d: ImageDraw.ImageDraw, x: int, y: int, text: str,
                 font: ImageFont.FreeTypeFont, max_w: int, fill,
                 leading: int) -> int:
    return draw_lines(d, x, y, wrap_text(d, text, font, max_w), font, fill,
                      leading)


def badge(d: ImageDraw.ImageDraw, x: int, y: int, n: int, size: int,
          colour) -> None:
    """Number badge: filled square with a white number."""
    d.rectangle([x, y, x + size, y + size], fill=colour)
    f = F(SANS_B, size - 6 if n < 10 else size - 7)
    t = str(n)
    tw = d.textlength(t, font=f)
    th = f.size
    d.text((x + (size - tw) / 2, y + (size - th) / 2 - 1), t, font=f,
           fill=(255, 255, 255))


def chip(d: ImageDraw.ImageDraw, x: int, y: int, text: str,
         bg, fg=(255, 255, 255), size: int = 11) -> int:
    """Small filled label chip; returns its width."""
    f = F(SANS_B, size)
    w = int(d.textlength(text, font=f)) + 12
    h = size + 8
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + 6, y + 3), text, font=f, fill=fg)
    return w


def burst(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float,
          colour, colour2=None) -> None:
    """Explosion starburst: 8-point star, optionally two-tone."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)
    if colour2:
        d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
                  fill=colour2)


def dashed(d: ImageDraw.ImageDraw, pts, colour, width: int = 2,
           dash: int = 7, gap: int = 5) -> None:
    """Dashed polyline through pts."""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg = math.hypot(x2 - x1, y2 - y1)
        if seg == 0:
            continue
        ux, uy = (x2 - x1) / seg, (y2 - y1) / seg
        s = 0.0
        while s < seg:
            e = min(s + dash, seg)
            d.line([x1 + ux * s, y1 + uy * s, x1 + ux * e, y1 + uy * e],
                   fill=colour, width=width)
            s = e + gap


# --- illustration panels (all drawn from primitives) -----------------------------------
def art_kyiv(d, x, y, w, h):
    """Night Kyiv: skyline, river, bridge, missile arcs, blasts."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    for sx, sy in [(0.08, 0.14), (0.22, 0.08), (0.45, 0.18), (0.62, 0.07),
                   (0.78, 0.16), (0.9, 0.09), (0.35, 0.26), (0.55, 0.3)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(220, 220, 200))
    # skyline
    sky = [(0.00, 0.42, 0.09, 0.62), (0.10, 0.34, 0.07, 0.70),
           (0.18, 0.46, 0.08, 0.58), (0.27, 0.38, 0.06, 0.66),
           (0.60, 0.40, 0.09, 0.64), (0.70, 0.33, 0.07, 0.71),
           (0.78, 0.44, 0.08, 0.60), (0.87, 0.38, 0.07, 0.66)]
    for fx, fy, fw, fh in sky:
        d.rectangle([x + w * fx, y + h * fy, x + w * (fx + fw),
                     y + h * (fy + fh)], fill=(8, 14, 28))
        for wy in range(3):
            for wx in range(2):
                if (int(fx * 100) + wy + wx) % 3 == 0:
                    d.rectangle([x + w * fx + 4 + wx * 9, y + h * fy + 6 + wy * 10,
                                 x + w * fx + 8 + wx * 9, y + h * fy + 10 + wy * 10],
                                fill=(240, 200, 90))
    # river + bridge
    d.rectangle([x, y + h * 0.74, x + w, y + h], fill=(38, 80, 130))
    by = y + h * 0.70
    d.rectangle([x, by, x + w, by + 7], fill=(30, 30, 34))
    for px in (0.14, 0.38, 0.62, 0.86):
        d.rectangle([x + w * px - 3, by + 7, x + w * px + 3, y + h * 0.94],
                    fill=(30, 30, 34))
    # missile arcs (dashed, from upper right)
    dashed(d, [(x + w * 0.98, y + h * 0.06), (x + w * 0.72, y + h * 0.30),
               (x + w * 0.50, y + h * 0.62)], (255, 190, 90), width=2)
    dashed(d, [(x + w * 0.86, y + h * 0.02), (x + w * 0.60, y + h * 0.34),
               (x + w * 0.30, y + h * 0.64)], (255, 190, 90), width=2)
    dashed(d, [(x + w * 0.66, y + h * 0.02), (x + w * 0.62, y + h * 0.40),
               (x + w * 0.68, y + h * 0.66)], (255, 190, 90), width=2)
    burst(d, x + w * 0.50, by - 2, 13, (255, 150, 40), (255, 230, 120))
    burst(d, x + w * 0.30, by - 2, 10, (255, 150, 40), (255, 230, 120))
    burst(d, x + w * 0.68, by - 2, 9, (255, 150, 40), (255, 230, 120))
    chip(d, x + 8, y + h - 26, "3 BRIDGES HIT", RED)


def art_akvan(d, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal with the Odisha coast."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 110, 158))
    # land (India coast) on the left
    d.polygon([(x, y), (x + w * 0.30, y), (x + w * 0.24, y + h * 0.35),
               (x + w * 0.30, y + h * 0.62), (x + w * 0.20, y + h),
               (x, y + h)], fill=(214, 196, 150))
    d.text((x + 8, y + 6), "ODISHA", font=F(SANS_B, 11), fill=(90, 70, 40))
    d.text((x + 8, y + 20), "INDIA", font=F(SANS_B, 11), fill=(90, 70, 40))
    # spiral
    cx, cy = x + w * 0.62, y + h * 0.52
    for k, rr in enumerate(range(40, 8, -8)):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 210 + k * 60,
              210 + k * 60 + 250, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    # rain streaks
    for rx, ry in [(0.82, 0.12), (0.88, 0.30), (0.78, 0.42), (0.92, 0.55),
                   (0.84, 0.70), (0.90, 0.82), (0.74, 0.78)]:
        d.line([x + w * rx, y + h * ry, x + w * rx - 5, y + h * ry + 12],
               fill=(200, 225, 245), width=2)
    # landfall marker
    gx, gy = x + w * 0.28, y + h * 0.48
    d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=RED)
    d.ellipse([gx - 9, gy - 9, gx + 9, gy + 9], outline=RED, width=2)
    d.text((gx - 24, gy + 12), "GOPALPUR", font=F(SANS_B, 10), fill=(90, 70, 40))
    chip(d, x + w - 118, y + 8, "LANDFALL \u00b7 8 AM", RED)


def art_markets(d, x, y, w, h):
    """Falling market chart on a dark board, with index tickers below."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 20, 26))
    for gy in range(1, 3):
        d.line([x + 8, y + h * gy / 4, x + w - 8, y + h * gy / 4],
               fill=(48, 52, 62), width=1)
    pts = [(0.06, 0.12), (0.20, 0.22), (0.32, 0.18), (0.46, 0.36),
           (0.58, 0.34), (0.72, 0.50), (0.84, 0.48), (0.95, 0.64)]
    px = [(x + w * a, y + h * b) for a, b in pts]
    d.line(px, fill=(230, 60, 60), width=4, joint="curve")
    ex, ey = px[-1]
    d.polygon([(ex + 2, ey + 10), (ex - 9, ey - 3), (ex + 8, ey - 6)],
              fill=(230, 60, 60))
    tick = [("TAIEX", "\u22126.2%"), ("NIKKEI", "\u22125.1%"),
            ("KOSPI", "\u22125.2%"), ("SOFTBANK", "\u221214.5%")]
    tx = x + 10
    for name, val in tick:
        f1, f2 = F(SANS_B, 10), F(SANS_B, 12)
        d.text((tx, y + h - 30), name, font=f1, fill=(180, 180, 180))
        d.text((tx, y + h - 17), val, font=f2, fill=(255, 110, 110))
        tx += max(d.textlength(name, font=f1),
                  d.textlength(val, font=f2)) + 22


def art_ukeu(d, x, y, w, h):
    """Union Jack and EU flag side by side, joined by a gold link."""
    hw = w // 2
    # Union Jack (simplified)
    d.rectangle([x, y, x + hw, y + h], fill=(18, 48, 110))
    d.line([x, y, x + hw, y + h], fill=(255, 255, 255), width=7)
    d.line([x + hw, y, x, y + h], fill=(255, 255, 255), width=7)
    d.line([x, y, x + hw, y + h], fill=(200, 30, 40), width=3)
    d.line([x + hw, y, x, y + h], fill=(200, 30, 40), width=3)
    d.rectangle([x + hw // 2 - 8, y, x + hw // 2 + 8, y + h], fill=(255, 255, 255))
    d.rectangle([x, y + h // 2 - 8, x + hw, y + h // 2 + 8], fill=(255, 255, 255))
    d.rectangle([x + hw // 2 - 4, y, x + hw // 2 + 4, y + h], fill=(200, 30, 40))
    d.rectangle([x, y + h // 2 - 4, x + hw, y + h // 2 + 4], fill=(200, 30, 40))
    # EU flag
    d.rectangle([x + hw, y, x + w, y + h], fill=(24, 54, 140))
    ccx, ccy = x + hw + hw // 2, y + h // 2
    for i in range(12):
        ang = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = ccx + 22 * math.cos(ang), ccy + 15 * math.sin(ang)
        burst(d, sx, sy, 3.2, (255, 210, 60))
    # gold link bar across the join
    d.rectangle([x + hw - 3, y, x + hw + 3, y + h], fill=(201, 162, 39))
    chip(d, x + 6, y + h - 22, "DEAL SEALED", RED, size=10)


def art_cop31(d, x, y, w, h):
    """Globe, thermometer and clock: climate talks run out of time."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 96, 104))
    # globe
    gx, gy, gr = x + 30, y + 14, 11
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 150, 200),
              outline=(255, 255, 255), width=2)
    d.ellipse([gx - 5, gy - 7, gx + 2, gy - 1], fill=(90, 180, 110))
    d.ellipse([gx - 1, gy + 1, gx + 7, gy + 8], fill=(90, 180, 110))
    # thermometer
    tx, ty = x + w - 48, y + 5
    d.rectangle([tx, ty, tx + 9, ty + 22], outline=(255, 255, 255), width=2)
    d.rectangle([tx + 2, ty + 13, tx + 7, ty + 20], fill=(230, 60, 60))
    d.ellipse([tx - 3, ty + 20, tx + 12, ty + 35], fill=(230, 60, 60),
              outline=(255, 255, 255), width=2)
    # clock
    cx, cy, cr = x + w // 2 + 6, y + h // 2, 13
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(250, 246, 238),
              outline=(22, 22, 22), width=2)
    d.line([cx, cy, cx, cy - 8], fill=(22, 22, 22), width=2)
    d.line([cx, cy, cx + 7, cy + 2], fill=(22, 22, 22), width=2)
    chip(d, x + 6, y + h - 22, "NO DEAL", RED, size=10)


def art_poland(d, x, y, w, h):
    """A cruise missile lying in a Polish field."""
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 120))
    d.rectangle([x, y, x + w, y + h * 0.30], fill=(170, 205, 225))
    # trees on the horizon
    for tx in (0.08, 0.20, 0.78, 0.90):
        px = x + w * tx
        d.polygon([(px, y + 2), (px - 8, y + h * 0.30), (px + 8, y + h * 0.30)],
                  fill=(40, 110, 60))
    # field rows
    for ry in (0.55, 0.72, 0.88):
        d.line([x, y + h * ry, x + w, y + h * ry], fill=(120, 165, 95), width=2)
    # crater + missile (body, nose cone, tail fins)
    d.ellipse([x + w * 0.42, y + h * 0.52, x + w * 0.72, y + h * 0.78],
              fill=(96, 74, 52))
    mx, my = x + w * 0.57, y + h * 0.62
    d.line([mx - 48, my + 10, mx + 34, my - 12], fill=(175, 180, 185), width=10)
    d.polygon([(mx + 34, my - 12), (mx + 54, my - 17), (mx + 38, my - 2)],
              fill=(200, 60, 60))
    d.polygon([(mx - 48, my + 10), (mx - 58, my - 4), (mx - 50, my + 4)],
              fill=(125, 130, 135))
    d.polygon([(mx - 48, my + 10), (mx - 56, my + 22), (mx - 46, my + 14)],
              fill=(125, 130, 135))
    chip(d, x + 6, y + h - 22, "KH-101 IN POLAND", RED, size=10)


def art_mercury(d, x, y, w, h):
    """BepiColombo probe approaching cratered Mercury."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 10, 18))
    for sx, sy in [(0.1, 0.2), (0.3, 0.12), (0.5, 0.25), (0.2, 0.8),
                   (0.45, 0.85), (0.08, 0.55), (0.62, 0.1)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(230, 230, 230))
    # Mercury
    mx, my, mr = x + w - 32, y + h // 2, 22
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(168, 158, 145))
    for cx, cy, cr in [(-10, -8, 5), (6, 4, 7), (-2, 12, 4), (10, -12, 3)]:
        d.ellipse([mx + cx - cr, my + cy - cr, mx + cx + cr, my + cy + cr],
                  fill=(140, 130, 118))
    # probe: bus + solar panels + dish
    px, py = x + 42, y + h // 2
    d.rectangle([px - 9, py - 8, px + 9, py + 8], fill=(200, 205, 210),
                outline=(120, 125, 130))
    d.rectangle([px - 34, py - 5, px - 11, py + 5], fill=(40, 90, 180))
    d.rectangle([px + 11, py - 5, px + 34, py + 5], fill=(40, 90, 180))
    d.arc([px + 6, py - 16, px + 26, py + 4], 270, 90, fill=(220, 220, 220),
          width=2)
    dashed(d, [(px + 34, py), (mx - mr - 4, my)], (255, 220, 120), width=2)
    chip(d, x + 6, y + h - 22, "ARRIVED \u00b7 8 YEARS", RED, size=10)


def art_italy(d, x, y, w, h):
    """Strikers with placards under a tricolour band."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 218))
    d.rectangle([x, y, x + w // 3, y + 8], fill=(30, 140, 70))
    d.rectangle([x + w // 3, y, x + 2 * w // 3, y + 8], fill=(245, 245, 245))
    d.rectangle([x + 2 * w // 3, y, x + w, y + 8], fill=(200, 40, 40))
    cols = [(40, 60, 110), (150, 40, 40), (60, 60, 60), (30, 110, 70),
            (110, 70, 140)]
    for i in range(5):
        px = x + 18 + i * 34
        py = y + h - 4
        c = cols[i]
        d.ellipse([px - 6, py - 28, px + 6, py - 16], fill=(222, 184, 150))
        d.polygon([(px - 9, py), (px - 7, py - 18), (px + 7, py - 18),
                   (px + 9, py)], fill=c)
        if i in (0, 2, 4):
            d.line([px + 8, py - 30, px + 8, py - 16], fill=(90, 70, 40), width=2)
            d.rectangle([px + 2, py - 40, px + 22, py - 30], fill=(255, 255, 255),
                        outline=(22, 22, 22))
    chip(d, x + 6, y + h - 22, "SCIOPERO", RED, size=10)


def art_japan(d, x, y, w, h):
    """Rising price bars beside the red sun."""
    d.rectangle([x, y, x + w, y + h], fill=(246, 244, 240))
    d.ellipse([x + 12, y + 8, x + 40, y + 36], fill=(188, 30, 50))
    bars = [8, 11, 14, 18, 24]
    bw = 16
    for i, bh in enumerate(bars):
        bx = x + 56 + i * (bw + 6)
        col = RED if i == len(bars) - 1 else (120, 125, 135)
        d.rectangle([bx, y + h - 8 - bh, bx + bw, y + h - 8], fill=col)
    d.text((x + 48, y + 2), "2.3%", font=F(SANS_B, 18), fill=RED)
    chip(d, x + w - 62, y + 6, "OCT CPI", NAVY, size=10)


def art_riyadh(d, x, y, w, h):
    """Riyadh skyline at dusk, a tower struck."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 32, 66))
    d.ellipse([x + w - 34, y + 6, x + w - 12, y + 28], fill=(240, 200, 120))
    # skyline
    for fx, fw, fh in [(0.00, 0.14, 0.42), (0.16, 0.12, 0.55),
                       (0.62, 0.12, 0.50), (0.76, 0.10, 0.40),
                       (0.88, 0.12, 0.58)]:
        d.rectangle([x + w * fx, y + h * (1 - fh), x + w * (fx + fw), y + h],
                    fill=(16, 14, 30))
    # the tall tower with an arched top
    tx0, tx1 = x + w * 0.36, x + w * 0.56
    d.rectangle([tx0, y + h * 0.14, tx1, y + h], fill=(22, 20, 40))
    d.polygon([(tx0, y + h * 0.14), ((tx0 + tx1) / 2, y + 2),
               (tx1, y + h * 0.14)], fill=(22, 20, 40))
    for wy in range(4):
        d.rectangle([tx0 + 6, y + h * 0.30 + wy * 9, tx1 - 6,
                     y + h * 0.30 + wy * 9 + 4], fill=(240, 200, 90))
    # incoming missile streak + blast at the tower top
    d.line([x + w * 0.94, y + 4, x + w * 0.52, y + h * 0.22],
           fill=(255, 190, 90), width=2)
    burst(d, x + w * 0.46, y + h * 0.20, 9, (255, 150, 40), (255, 230, 120))
    chip(d, x + 6, y + h - 22, "TOWER HIT", RED, size=10)


def art_gaza(d, x, y, w, h):
    """A map with the dashed Yellow Line, crossed by an arrow."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 180))
    # blocks
    for bx, by, bw, bh in [(0.08, 0.14, 0.16, 0.22), (0.30, 0.10, 0.12, 0.18),
                           (0.10, 0.55, 0.18, 0.26), (0.55, 0.60, 0.16, 0.22),
                           (0.76, 0.12, 0.14, 0.20)]:
        d.rectangle([x + w * bx, y + h * by, x + w * (bx + bw),
                     y + h * (by + bh)], fill=(200, 186, 150),
                    outline=(160, 146, 112))
    # the Yellow Line, dashed, diagonal
    dashed(d, [(x + w * 0.52, y), (x + w * 0.38, y + h)], (220, 170, 20),
           width=4, dash=9, gap=6)
    # crossing arrow
    ax0, ay0 = x + w * 0.66, y + h * 0.30
    ax1, ay1 = x + w * 0.34, y + h * 0.62
    d.line([ax0, ay0, ax1, ay1], fill=(158, 24, 24), width=4)
    d.polygon([(ax1, ay1), (ax1 + 14, ay1 - 2), (ax1 + 4, ay1 + 12)],
              fill=(158, 24, 24))
    chip(d, x + 6, y + h - 22, "YELLOW LINE", RED, size=10)


def art_hormuz(d, x, y, w, h):
    """A tanker ablaze in the strait."""
    d.rectangle([x, y, x + w, y + h], fill=(44, 96, 140))
    d.rectangle([x, y, x + w, y + h * 0.34], fill=(150, 190, 215))
    # distant shore
    d.polygon([(x, y + h * 0.34), (x + w * 0.3, y + h * 0.18),
               (x + w * 0.55, y + h * 0.34)], fill=(180, 168, 140))
    # tanker hull
    hy = y + h * 0.58
    d.polygon([(x + w * 0.08, hy), (x + w * 0.90, hy), (x + w * 0.84, hy + 16),
               (x + w * 0.14, hy + 16)], fill=(40, 40, 46))
    d.rectangle([x + w * 0.66, hy - 14, x + w * 0.80, hy], fill=(220, 220, 220))
    d.rectangle([x + w * 0.68, hy - 20, x + w * 0.72, hy - 14], fill=(200, 60, 60))
    # flames + smoke
    burst(d, x + w * 0.30, hy - 8, 12, (255, 150, 40), (255, 230, 120))
    burst(d, x + w * 0.45, hy - 12, 9, (255, 150, 40), (255, 230, 120))
    for sx, sy, sr in [(0.30, 0.30, 7), (0.36, 0.22, 9), (0.42, 0.14, 6)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=(110, 110, 110))
    # waves
    for wx in range(6):
        d.arc([x + 8 + wx * 30, hy + 20, x + 28 + wx * 30, hy + 32], 180, 360,
              fill=(200, 225, 245), width=2)
    chip(d, x + 6, y + h - 22, "TANKER ABLAZE", RED, size=10)


def art_cricket(d, x, y, w, h):
    """Cricket pitch: bat, ball, stumps, and 118."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 132, 70))
    d.rectangle([x + w * 0.30, y, x + w * 0.62, y + h], fill=(206, 184, 138))
    # stumps
    for i in range(3):
        sx = x + w * 0.40 + i * 7
        d.rectangle([sx, y + 8, sx + 4, y + 26], fill=(240, 210, 90))
    # bat, angled
    bx, by = x + w * 0.52, y + h * 0.55
    d.polygon([(bx - 4, by - 18), (bx + 8, by - 14), (bx + 2, by + 14),
               (bx - 8, by + 12)], fill=(222, 184, 130))
    d.line([bx + 2, by - 16, bx + 8, by - 28], fill=(120, 84, 50), width=3)
    # ball
    d.ellipse([x + w * 0.72 - 6, y + h * 0.30 - 6, x + w * 0.72 + 6,
               y + h * 0.30 + 6], fill=(178, 30, 30))
    d.text((x + 8, y + h - 40), "118", font=F(SANS_B, 22), fill=(255, 255, 255))
    chip(d, x + w - 72, y + h - 22, "2ND TEST TON", NAVY, size=10)


ART = {
    "kyiv": art_kyiv, "akvan": art_akvan, "markets": art_markets,
    "ukeu": art_ukeu, "cop31": art_cop31, "poland": art_poland,
    "mercury": art_mercury, "italy": art_italy, "japan": art_japan,
    "riyadh": art_riyadh, "gaza": art_gaza, "hormuz": art_hormuz,
    "cricket": art_cricket,
}


# --- world map (dot grid) ---------------------------------------------------------------
# 48 columns of longitude (-180..180), 22 rows of latitude (75..-60).
# Each row lists inclusive column spans of land, drawn as dots.
LAND_SPANS = {
    0: [(2, 5), (7, 12), (16, 21), (33, 47)],
    1: [(1, 16), (18, 21), (26, 47)],
    2: [(2, 15), (18, 18), (24, 47)],
    3: [(6, 16), (23, 42), (44, 45)],
    4: [(7, 15), (23, 42)],
    5: [(7, 14), (24, 43)],
    6: [(8, 14), (24, 42)],
    7: [(8, 13), (22, 31), (33, 34), (37, 40)],
    8: [(9, 12), (21, 31), (33, 35), (38, 40)],
    9: [(10, 12), (21, 29), (33, 34), (36, 37)],
    10: [(12, 13), (22, 29), (34, 34), (36, 37)],
    11: [(13, 17), (22, 29), (36, 40)],
    12: [(13, 18), (22, 29), (37, 42)],
    13: [(13, 18), (25, 29), (38, 42)],
    14: [(14, 18), (25, 29), (41, 42)],
    15: [(14, 18), (25, 28), (39, 44)],
    16: [(14, 17), (26, 28), (39, 44)],
    17: [(14, 17), (26, 27), (39, 44)],
    18: [(14, 16), (42, 44), (46, 46)],
    19: [(14, 15), (46, 46)],
    20: [(14, 15)],
    21: [],
}
MAP_COLS, MAP_ROWS = 48, 22
# (story number, longitude, latitude, dx, dy) — dx/dy nudge crowded pins apart
PINS = [
    (1, 30.5, 50.4, 0, -6), (2, 84.9, 19.3, 0, 0), (3, 121.5, 25.0, 0, 0),
    (4, 4.4, 50.9, -6, -8), (5, 30.7, 36.9, 10, -6), (6, 22.5, 51.2, 2, 10),
    (8, 12.5, 41.9, -14, -2), (9, 139.7, 35.7, 0, 0), (10, 46.7, 24.6, 8, 4),
    (11, 34.5, 31.5, -2, 10), (12, 56.5, 26.5, 9, -7),
    (13, 174.8, -41.3, 0, 0),
]


def draw_map(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    """Dotted world map with numbered pins for the drawn stories."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    cell_w, cell_h = w / MAP_COLS, h / MAP_ROWS
    for r, spans in LAND_SPANS.items():
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * cell_w
                cy = y + (r + 0.5) * cell_h
                d.ellipse([cx - 2.1, cy - 2.1, cx + 2.1, cy + 2.1],
                          fill=(178, 158, 118))
    for n, lon, lat, dx, dy in PINS:
        px = x + (lon + 180) / 360 * w + dx
        py = y + (75 - lat) / 135 * h + dy
        r = 6.5 if n >= 10 else 6
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = F(SANS_B, 8)
        t = str(n)
        tw = d.textlength(t, font=f)
        d.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))


# --- page assembly ----------------------------------------------------------------------
def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top band
    d.rectangle([0, 0, W, 6], fill=NAVY)

    # --- eyebrow ------------------------------------------------------------------------
    eye_f = F(SANS_B, 13)
    d.text((MARGIN, 14), "THE WORLD IN ONE DAY", font=eye_f, fill=RED)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    d.text((W - MARGIN - d.textlength(right, font=eye_f), 14), right,
           font=eye_f, fill=INK)
    d.line([MARGIN, 36, W - MARGIN, 36], fill=INK, width=2)

    # --- masthead -----------------------------------------------------------------------
    title = "Friday 20 November 2026"
    size = 62
    while d.textlength(title, font=F(SERIF_B, size)) > CW and size > 30:
        size -= 2
    tf = F(SERIF_B, size)
    d.text(((W - d.textlength(title, font=tf)) / 2, 42), title, font=tf,
           fill=NAVY)
    deck_f = F(SERIF_I, 17)
    d.text(((W - d.textlength(DECK, font=deck_f)) / 2, 108), DECK,
           font=deck_f, fill=INK)
    d.line([MARGIN, 136, W - MARGIN, 136], fill=INK, width=3)

    # --- day in numbers -----------------------------------------------------------------
    ny, nh = 144, 50
    cell = CW / len(NUMBERS)
    big_f, lab_f = F(SANS_B, 25), F(SANS, 11)
    for i, (big, label) in enumerate(NUMBERS):
        cx = MARGIN + i * cell
        if i:
            d.line([cx - 6, ny + 4, cx - 6, ny + nh - 4], fill=RULE, width=1)
        d.text((cx + 4, ny), big, font=big_f,
               fill=RED if big.startswith("\u2212") else NAVY)
        draw_wrapped(d, cx + 4, ny + 29, label, lab_f, cell - 12, GREY, 13)

    # --- region bar ---------------------------------------------------------------------
    ry, rh = 202, 20
    total = sum(c for _, c, _ in REGIONS)
    rx = MARGIN
    reg_f = F(SANS_B, 10)
    for name, count, colour in REGIONS:
        rw = CW * count / total
        d.rectangle([rx, ry, rx + rw, ry + rh], fill=colour)
        label = f"{name} {count}"
        lw = d.textlength(label, font=reg_f)
        if lw <= rw - 6:
            d.text((rx + (rw - lw) / 2, ry + 4), label, font=reg_f,
                   fill=(255, 255, 255))
        rx += rw

    # --- lead stories -------------------------------------------------------------------
    lead_w = (CW - 2 * 11) // 3
    ly = 230
    panel_h = 84
    for i, (n, place, beat, head, deck, art) in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + 11)
        ART[art](d, lx, ly, lead_w, panel_h)
        ty = ly + panel_h + 8
        badge(d, lx, ty, n, 17, NAVY)
        d.text((lx + 22, ty + 1), f"{place}  \u00b7  {beat}",
               font=F(SANS_B, 12), fill=BEATS[beat])
        hy = draw_wrapped(d, lx, ty + 22, head, F(SANS_B, 21), lead_w, INK, 24)
        draw_wrapped(d, lx, hy + 4, deck, F(SANS, 12), lead_w, (50, 50, 50), 16)
    d.line([MARGIN, 451, W - MARGIN, 451], fill=INK, width=1)

    # --- feature stories: 2 rows x 5 ------------------------------------------------------
    feat_w = (CW - 4 * 10) // 5
    feat_panel = 48
    for row in range(2):
        fy = 459 + row * 133
        for col in range(5):
            n, place, beat, head, deck, art = FEATURES[row * 5 + col]
            fx = MARGIN + col * (feat_w + 10)
            ART[art](d, fx, fy, feat_w, feat_panel)
            ty = fy + feat_panel + 5
            badge(d, fx, ty, n, 14, NAVY)
            d.text((fx + 18, ty), f"{place} \u00b7 {beat}",
                   font=F(SANS_B, 10), fill=BEATS[beat])
            hy = draw_wrapped(d, fx, ty + 17, head, F(SANS_B, 14), feat_w,
                              INK, 15)
            deck_f = F(SANS_C, 11)
            if d.textlength(deck, font=deck_f) > feat_w:
                print(f"WARNING: feature {n} deck too long: {deck}")
            d.text((fx, hy + 2), deck, font=deck_f, fill=(60, 60, 60))
    d.line([MARGIN, 725, W - MARGIN, 725], fill=INK, width=1)

    # --- bottom: map + briefs -------------------------------------------------------------
    by = 733
    head_f = F(SANS_B, 12)
    d.text((MARGIN, by), "WHERE IT HAPPENED", font=head_f, fill=RED)
    map_w, map_h = 272, 120
    draw_map(d, MARGIN, by + 18, map_w, map_h)
    d.text((MARGIN, by + 142), "Pins 1\u201313 mark the drawn stories; 7 is in space.",
           font=F(SANS, 10), fill=GREY)

    bx = MARGIN + map_w + 14
    bw = W - MARGIN - bx
    d.text((bx, by), "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES",
           font=head_f, fill=RED)
    brief_f = F(SANS_C, 11)
    col_w = (bw - 12) // 2
    cols = [BRIEFS[:11], BRIEFS[11:]]
    for ci, col in enumerate(cols):
        cx = bx + ci * (col_w + 12)
        cy = by + 18
        for j, text in enumerate(col):
            num = 14 + ci * 11 + j
            d.text((cx, cy), f"{num}", font=F(SANS_B, 11), fill=RED)
            lines = wrap_text(d, text, brief_f, col_w - 20)
            if len(lines) > 1:
                print(f"WARNING: brief {num} wraps to {len(lines)} lines: {text}")
            draw_lines(d, cx + 20, cy, lines, brief_f, INK, 12)
            cy += 12 * max(1, len(lines))

    # --- date check -----------------------------------------------------------------------
    dy = 888
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 62], outline=RED, width=2)
    d.text((MARGIN + 10, dy + 6), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
           font=F(SANS_B, 12), fill=RED)
    draw_wrapped(d, MARGIN + 10, dy + 24, DATE_CHECK, F(SANS, 12),
                 CW - 20, INK, 15)

    # --- footer ---------------------------------------------------------------------------
    foot_f = F(SANS, 11)
    fw = d.textlength(FOOTER, font=foot_f)
    d.text(((W - fw) / 2, H - 22), FOOTER, font=foot_f, fill=GREY)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
