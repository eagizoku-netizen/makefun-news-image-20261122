#!/usr/bin/env python3
"""Draw 'The World in One Day - Sunday 22 November 2026' as a 1024x1024 PNG.

Everything is drawn in code with Pillow primitives and DejaVu Sans.
No AI-generated imagery. Deterministic output: no randomness, no timestamps.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, x, y, s):
    # Earth: teal disc, green land blobs, white cloud arcs
    d.ellipse([x, y, x + s, y + s], fill=(38, 132, 110), outline=(16, 80, 66), width=3)
    d.ellipse([x + 12, y + 18, x + 48, y + 42], fill=(84, 170, 90))
    d.ellipse([x + 52, y + 52, x + 92, y + 78], fill=(84, 170, 90))
    d.ellipse([x + 30, y + 62, x + 55, y + 88], fill=(110, 190, 100))
    d.arc([x + 8, y + 8, x + s - 8, y + s - 8], 200, 330, fill=(255, 255, 255), width=4)
    # small red cross = no deal
    cx, cy = x + s - 8, y + 2
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(200, 40, 40), outline=(255, 255, 255), width=2)
    d.line([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255), width=3)
    d.line([cx - 6, cy + 6, cx + 6, cy - 6], fill=(255, 255, 255), width=3)


def draw_drone(d, x, y, s):
    # Building block (left) + drone (right) + impact star
    bx, by = x, y + 30
    d.rectangle([bx, by, bx + 52, by + 70], fill=(120, 130, 145), outline=(60, 66, 80), width=2)
    for r in range(4):
        for c in range(2):
            d.rectangle([bx + 8 + c * 22, by + 10 + r * 16, bx + 18 + c * 22, by + 20 + r * 16],
                        fill=(255, 220, 90))
    # impact star on the building
    sx, sy = bx + 44, by + 8
    for dx, dy in [(0, -12), (8, -8), (12, 0), (8, 8), (0, 12), (-8, 8), (-12, 0), (-8, -8)]:
        d.line([sx, sy, sx + dx, sy + dy], fill=(220, 50, 30), width=4)
    # drone body + rotors
    dx0, dy0 = x + 58, y + 8
    d.rectangle([dx0, dy0 + 14, dx0 + 44, dy0 + 30], fill=(70, 74, 84), outline=(30, 32, 40), width=2)
    d.ellipse([dx0 - 4, dy0, dx0 + 16, dy0 + 12], outline=(50, 52, 60), width=3)
    d.ellipse([dx0 + 28, dy0, dx0 + 48, dy0 + 12], outline=(50, 52, 60), width=3)
    d.line([dx0 + 6, dy0 + 30, dx0 + 6, dy0 + 44], fill=(50, 52, 60), width=2)
    d.line([dx0 + 38, dy0 + 30, dx0 + 38, dy0 + 44], fill=(50, 52, 60), width=2)


def draw_explosion(d, x, y, s):
    # Grey industrial block + orange starburst
    d.rectangle([x, y + 55, x + 100, y + 100], fill=(110, 116, 128), outline=(60, 64, 74), width=2)
    d.rectangle([x + 10, y + 70, x + 26, y + 84], fill=(255, 220, 90))
    d.rectangle([x + 38, y + 70, x + 54, y + 84], fill=(255, 220, 90))
    d.rectangle([x + 66, y + 70, x + 82, y + 84], fill=(255, 220, 90))
    cx, cy = x + 50, y + 38
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        r = 42 if i % 2 == 0 else 20
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(245, 130, 30), outline=(200, 60, 20))
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 210, 60))


def draw_badge(d, x, y, s):
    # Gold sheriff-style badge + bars
    cx, cy = x + 42, y + 45
    import math
    pts = []
    for i in range(10):
        ang = math.pi * i / 5 - math.pi / 2
        r = 42 if i % 2 == 0 else 20
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(230, 180, 40), outline=(160, 110, 10), width=2)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 220, 90), outline=(160, 110, 10), width=2)
    d.text((cx, cy), "*", font=font(BOLD, 26), fill=(160, 110, 10), anchor="mm")
    # prison bars
    for i in range(3):
        bx = x + 88 + i * 6
        d.line([bx, y + 10, bx, y + 92], fill=(70, 74, 84), width=4)


def draw_fire(d, x, y, s):
    # Factory silhouette + flame
    d.rectangle([x, y + 60, x + 100, y + 100], fill=(120, 118, 110), outline=(60, 58, 52), width=2)
    d.rectangle([x + 8, y + 28, x + 22, y + 60], fill=(100, 98, 92), outline=(60, 58, 52), width=2)
    d.polygon([(x + 42, y + 60), (x + 42, y + 78), (x + 100, y + 78), (x + 100, y + 60)],
              fill=(90, 88, 82))
    # flame
    cx = x + 55
    d.polygon([(cx - 26, y + 62), (cx - 30, y + 30), (cx - 12, y + 44), (cx - 6, y + 8),
               (cx + 10, y + 36), (cx + 26, y + 18), (cx + 30, y + 62)],
              fill=(245, 120, 20), outline=(200, 50, 10))
    d.polygon([(cx - 12, y + 62), (cx - 14, y + 40), (cx - 2, y + 50), (cx + 2, y + 30),
               (cx + 14, y + 48), (cx + 14, y + 62)],
              fill=(255, 210, 60))


def draw_space(d, x, y, s):
    # Mercury disc with craters + probe with solar panels + orbit
    d.ellipse([x + 2, y + 2, x + 102, y + 102], outline=(150, 160, 190), width=2)
    cx, cy = x + 42, y + 58
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(176, 168, 158),
              outline=(110, 104, 96), width=2)
    for ox, oy, r in [(-14, -8, 7), (10, 6, 9), (2, -18, 5), (16, -12, 4)]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  outline=(110, 104, 96), width=2)
    # probe: body + two blue panels
    px, py = x + 62, y + 6
    d.rectangle([px - 22, py + 12, px - 2, py + 22], fill=(40, 90, 180), outline=(20, 50, 120), width=1)
    d.rectangle([px + 2, py + 12, px + 22, py + 22], fill=(40, 90, 180), outline=(20, 50, 120), width=1)
    d.rectangle([px - 6, py + 8, px + 6, py + 26], fill=(200, 205, 215), outline=(90, 95, 105), width=2)
    d.line([px, py + 26, px - 6, py + 34], fill=(90, 95, 105), width=2)


ILLUSTRATIONS = {
    0: draw_globe,
    1: draw_drone,
    2: draw_explosion,
    3: draw_badge,
    4: draw_fire,
    5: draw_space,
}

# (label, colour, headline, body)
ITEMS = [
    ("CLIMATE", (16, 110, 90), "COP31 COLLAPSES",
     "UN climate talks COP31 in Antalya, Turkey ended with no deal after the EU, Marshall Islands and Panama rejected a draft with no fossil-fuel mention."),
    ("UKRAINE", (30, 70, 160), "DRONE HITS KYIV FLAT",
     "A Russian drone hit a 5-storey block in Dymer, Kyiv region; at least 14 people missing. Overnight attack: 186 Shahed drones, 161 shot down or jammed."),
    ("MIDDLE EAST", (170, 60, 40), "IRAN STRIKES BAHRAIN",
     "An Iranian projectile hit an industrial site in Bahrain, injuring 2 people. Gulf states condemned the strike."),
    ("MEXICO", (120, 80, 10), "CARTEL BOSS CAPTURED",
     "Mexican special forces arrested drug lord Fausto Isidro Meza Flores, \u201cEl Chapo Isidro\u201d, in Sinaloa. 11 killed in the raid, including 4 soldiers."),
    ("INDONESIA", (200, 90, 10), "FACTORY FIRE IN INDONESIA",
     "A fire at a confectionery factory in Cikande, Indonesia killed 3 workers; 36 are missing."),
    ("SPACE", (70, 50, 130), "TO MERCURY",
     "Europe-Japan probe BepiColombo entered orbit around Mercury after an 8-year journey."),
]


def main():
    img = Image.new("RGB", (W, H), (245, 243, 238))
    d = ImageDraw.Draw(img)

    # ---- Header ----
    d.rectangle([0, 0, W, 112], fill=(18, 32, 54))
    d.rectangle([0, 112, W, 118], fill=(230, 180, 40))
    title_f = font(BOLD, 46)
    date_f = font(BOLD, 30)
    d.text((512, 22), "THE WORLD IN ONE DAY", font=title_f, fill=(255, 255, 255), anchor="ma")
    d.text((512, 76), "Sunday 22 November 2026", font=date_f, fill=(255, 214, 80), anchor="ma")

    # ---- Panels: 2 cols x 3 rows ----
    margin, gap = 12, 12
    pw = (W - margin * 2 - gap) // 2
    ph = 268
    top0 = 130
    label_f = font(BOLD, 14)
    head_f = font(BOLD, 21)
    body_f = font(REG, 15)

    for i, (label, colour, headline, body) in enumerate(ITEMS):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top0 + row * (ph + gap)
        # panel background
        d.rectangle([x, y, x + pw, y + ph], fill=(255, 255, 255),
                    outline=(180, 180, 175), width=2)
        # label strip
        d.rectangle([x + 2, y + 2, x + pw - 2, y + 38], fill=colour)
        d.text((x + 14, y + 20), label, font=label_f, fill=(255, 255, 255), anchor="lm")
        d.text((x + pw - 14, y + 20), f"{i + 1} / 6", font=label_f, fill=(255, 255, 255), anchor="rm")
        # headline
        d.text((x + 14, y + 50), headline, font=head_f, fill=(20, 20, 20))
        d.line([x + 14, y + 82, x + pw - 14, y + 82], fill=(210, 208, 200), width=2)
        # body text (left) + illustration (right)
        lines = wrap(d, body, body_f, 330)
        ty = y + 94
        for ln in lines[:7]:
            d.text((x + 14, ty), ln, font=body_f, fill=(40, 40, 40))
            ty += 20
        ILLUSTRATIONS[i](d, x + 356, y + 96, 110)

    # ---- Footer ----
    fy = top0 + 3 * ph + 2 * gap + 12  # 958
    d.rectangle([0, fy, W, H], fill=(18, 32, 54))
    foot_f = font(REG, 14)
    d.text((512, fy + 12), "Sources: verified news reports, 22 November 2026",
           font=foot_f, fill=(255, 255, 255), anchor="ma")
    d.text((512, fy + 32), "Drawn entirely in code with Python / Pillow \u2014 no AI-generated imagery",
           font=foot_f, fill=(200, 205, 215), anchor="ma")

    out = os.path.join(HERE, "news.png")
    img.save(out, "PNG", optimize=True)
    print(f"Wrote {out}: {img.size[0]}x{img.size[1]}, {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
