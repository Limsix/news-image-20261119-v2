#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a one-page newspaper front page
summing up Thursday 19 November 2026. 1024x1024 PNG, PIL only, no network,
deterministic output."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (178, 28, 28)
BLUE = (30, 58, 95)
GRAY = (96, 96, 96)
LIGHT = (232, 226, 214)
WHITE = (255, 255, 255)

DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def centered(x0, x1, y, text, fnt, fill=INK):
    w = fnt.getlength(text)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)

def rule(x0, x1, y, fill=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)

M = 36  # margin
X1 = W - M

# ---------- masthead ----------
f_title = font(DJSB, 62)
centered(M, X1, 26, "THE WORLD TODAY", f_title)
f_date = font(DJB, 27)
centered(M, X1, 104, "THURSDAY, 19 NOVEMBER 2026", f_date, fill=RED)
rule(M, X1, 146, width=4)
rule(M, X1, 153, width=1)

# ---------- lead story: Shenzhen summit ----------
LY = 170
f_kick = font(DJB, 20)
d.text((M, LY), "SHENZHEN  ·  APEC SUMMIT", font=f_kick, fill=RED)
f_head = font(DJB, 41)
head_lines = wrap("Trump, Xi and Putin hold first three-way summit", f_head, 640)
text_block(M, LY + 30, head_lines, f_head, leading=48)
f_body = font(DJ, 23)
body = wrap("The three leaders meet in Shenzhen and declare dialogue on nuclear "
            "risks and stable energy flows.",
            f_body, 640)
text_block(M, LY + 30 + 48 * len(head_lines) + 8, body, f_body, leading=29)

# three circles: US / CN / RU
cx, cy, r = 800, 268, 52
for i, (label, col) in enumerate([("US", (30, 58, 95)), ("CN", (178, 28, 28)), ("RU", (60, 90, 60))]):
    x = cx + (i - 1) * 118
    d.ellipse([x - r, cy - r, x + r, cy + r], fill=col)
    f_lab = font(DJB, 30)
    tw = f_lab.getlength(label)
    d.text((x - tw / 2, cy - 20), label, font=f_lab, fill=WHITE)
f_cap = font(DJ, 17)
centered(700, 952, 340, "Trump  ·  Xi Jinping  ·  Putin", f_cap, fill=GRAY)

rule(M, X1, 392, width=2)

# ---------- grid: four stories, 2 x 2 ----------
f_pk = font(DJB, 18)
f_h2 = font(DJB, 27)
f_b2 = font(DJ, 21)

def panel(x, y, w, hgt, kicker, headline, body, kcol):
    d.rectangle([x, y, x + w, y + hgt], outline=(200, 192, 176), width=1)
    d.text((x + 14, y + 10), kicker, font=f_pk, fill=kcol)
    hl = wrap(headline, f_h2, w - 28)
    by = text_block(x + 14, y + 38, hl, f_h2, leading=32)
    bl = wrap(body, f_b2, w - 28)
    text_block(x + 14, by + 6, bl, f_b2, leading=26)

GW = 466
GH = 196
GY = 408
GX2 = M + GW + 20

panel(M, GY, GW, GH, "THE HAGUE  ·  ICJ",
      "Myanmar guilty of genocide against the Rohingya",
      "UN top court rules on the 2017 crackdown: about 10,000 killed, "
      "more than 700,000 fled to Bangladesh.", RED)
panel(GX2, GY, GW, GH, "UKRAINE  ·  WAR",
      "Ukraine hits Crimean Bridge for the third time",
      "Kerch Bridge severely damaged in a missile and drone strike; "
      "Russia hits Kyiv power infrastructure.", BLUE)
panel(M, GY + GH + 16, GW, GH, "MIDDLE EAST",
      "Gaza ground operation; Riyadh tower struck",
      "Israel launches an operation in central Gaza; a Houthi missile "
      "damages the PIF Tower in the Saudi capital.", RED)
panel(GX2, GY + GH + 16, GW, GH, "GULF  ·  IRAN",
      "US strikes Iran's Qeshm island",
      "Reported Iranian retaliation against Kuwait and Bahrain follows "
      "the strike in the Strait of Hormuz.", BLUE)

# ---------- briefly strip ----------
BY = GY + 2 * GH + 32
rule(M, X1, BY, width=2)
f_br = font(DJB, 19)
d.text((M, BY + 12), "ALSO TODAY", font=f_br, fill=RED)
f_b3 = font(DJ, 20)
briefs = [
    ("CYCLONE AKVAN", "Severe storm nears India's east coast; landfall Friday."),
    ("ANTHROPIC IPO", "AI firm debuts above $2 trillion on Nasdaq."),
    ("COP31 / ARCTIC", "Climate talks split on fossil fuels; Denmark OKs Greenland deal."),
]
col_w = 304
for i, (k, t) in enumerate(briefs):
    x = M + i * (col_w + 16)
    d.text((x, BY + 42), k, font=font(DJB, 17), fill=BLUE)
    bl = wrap(t, f_b3, col_w)
    text_block(x, BY + 66, bl, f_b3, leading=24)

# ---------- footer ----------
rule(M, X1, 972, width=1)
f_ft = font(DJ, 16)
centered(M, X1, 982, "make.fun  ·  one day's news in one image  ·  19 November 2026",
         f_ft, fill=GRAY)

img.save("/home/hatch/workspace/makefun/news-image-20261119-entry-v2/entry.png")
print("saved entry.png", img.size)
