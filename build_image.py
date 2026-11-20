#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page as entry.png.

Pure Pillow: flat shapes and text only, no photos, no network.
Canvas 1024x1024, deep teal-navy / amber / cream newspaper design:
masthead, full-width lead panel, two-column story grid, bottom strip.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

CREAM = (247, 241, 222)
NAVY = (27, 42, 68)
AMBER = (232, 169, 44)
RED = (178, 34, 34)
INK = (27, 42, 68)
GREY = (112, 102, 86)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def reg(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    """Section label with a short underline bar; returns y below the bar."""
    draw.text((x, y), text, font=bold(24), fill=color)
    draw.rectangle([x, y + 36, x + 42, y + 41], fill=color)
    return y + 52


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.text((32, 16), "THE WORLD IN ONE PAGE", font=bold(62), fill=WHITE)
    d.text((32, 84), "FRIDAY 20 NOVEMBER 2026  |  SIX STORIES, ONE DAY",
           font=bold(25), fill=AMBER)
    d.text((992, 84), "No. 324", font=bold(25), fill=WHITE, anchor="ra")
    d.rectangle([0, 116, W, 122], fill=AMBER)

    # ---- Lead story: Trump / Iran ---------------------------------------
    lx, ly, lw, lh = 24, 140, 976, 260
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=NAVY)
    d.rectangle([lx, ly, lx + lw, ly + 6], fill=AMBER)
    d.text((lx + 24, ly + 18), "USA  /  IRAN", font=bold(28), fill=AMBER)
    d.text((lx + lw - 24, ly + 14), "01", font=bold(44), fill=AMBER, anchor="ra")
    d.rectangle([lx + 24, ly + 58, lx + 72, ly + 63], fill=AMBER)
    head = wrap(d, "Trump pushes Iran war decision to 2027",
                bold(46), lw - 48)
    y = draw_lines(d, head, lx + 24, ly + 68, bold(46), WHITE, 52)
    d.rectangle([lx + 24, y + 6, lx + 72, y + 11], fill=AMBER)
    body = wrap(
        d,
        "\u201cWe\u2019ll see what happens after January 1,\u201d he says "
        "aboard Air Force One; no new strikes this year despite "
        "Israeli pressure.",
        reg(25), lw - 48)
    draw_lines(d, body, lx + 24, y + 20, reg(25), WHITE, 31)

    # ---- Middle grid: four stories --------------------------------------
    stories = [
        ("WEATHER  /  INDIA", RED,
         "Cyclone Akvan hits India's east coast",
         "Landfall near Gopalpur at noon; about 300,000 evacuated, "
         "423 rescue teams deployed.", "02"),
        ("INDIA  /  LAW", NAVY,
         "Judge: resignation is no admission of guilt",
         "Ex-judge Yashwant Varma says his resignation ends the "
         "removal proceedings against him.", "03"),
        ("CULTURE  /  GAMING", NAVY,
         "GTA VI tops $1.84bn on launch day",
         "Sensor Tower's estimate passes The Odyssey's $1.805bn "
         "lifetime box office in a single day.", "04"),
        ("BUSINESS  /  AI", RED,
         "Anthropic soars in record Wall Street debut",
         "Shares close 17% up at $97.17 after a record $81.3bn IPO; "
         "the lab is valued near $1.8tn.", "05"),
    ]
    cw, ch, gap = 476, 236, 24
    for i, (kick, kcolor, headline, text, num) in enumerate(stories):
        cx = 24 + (i % 2) * (cw + gap)
        cy = 412 + (i // 2) * (ch + 8)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CREAM,
                    outline=NAVY, width=3)
        d.rectangle([cx, cy, cx + 8, cy + ch], fill=kcolor)
        ix = cx + 26
        y = kicker(d, ix, cy + 12, kick, kcolor)
        hlines = wrap(d, headline, bold(30), cw - 52)
        y = draw_lines(d, hlines, ix, y, bold(30), INK, 37)
        blines = wrap(d, text, reg(22), cw - 110)
        draw_lines(d, blines, ix, y + 8, reg(22), INK, 27)
        d.text((cx + cw - 18, cy + ch - 40), num, font=bold(30),
               fill=NAVY, anchor="ra")

    # ---- Bottom strip: cricket ------------------------------------------
    bx, by, bw, bh = 24, 904, 976, 76
    d.rectangle([bx, by, bx + bw, by + bh], fill=AMBER)
    d.text((bx + 24, by + 6), "SPORT  /  CRICKET", font=bold(20), fill=NAVY)
    d.text((bx + 24, by + 28), "Phillips' 118 lifts New Zealand past 300",
           font=bold(29), fill=NAVY)
    d.text((bx + 24, by + 56),
           "Day two in Wellington: first hundreds in all three formats "
           "vs India in one year.",
           font=reg(17), fill=NAVY)
    cx0, cy0, r = bx + bw - 62, by + bh // 2, 30
    d.ellipse([cx0 - r, cy0 - r, cx0 + r, cy0 + r], outline=NAVY, width=4)
    d.text((cx0, cy0), "06", font=bold(32), fill=NAVY, anchor="mm")

    # ---- Footer ----------------------------------------------------------
    d.text((24, 990), "Compiled from verified reports  |  "
           "One image, six stories", font=reg(20), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
