#!/usr/bin/env python3
"""Draw the 20 November 2026 front page: one image, six stories.

Pure Pillow shapes and text, no photos, no network. Renders entry.png
at 1024x1024 in the same directory as this script.

Stories (all verified against reputable reporting of 20 Nov 2026):
  01 Trump pushes the Iran war decision to 2027 (Reuters / TOI)
  02 Cyclone Akvan makes landfall on India's east coast (The Hindu / ANI)
  03 Ex-judge Varma: resignation is no admission of guilt (NDTV)
  04 GTA VI tops $1.84bn on launch day (Sensor Tower via Reuters / Forbes)
  05 Anthropic soars in its record Wall Street debut (The Hindu BusinessLine / CNN)
  06 Glenn Phillips' century lifts New Zealand in Wellington (ICC / ANI)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (250, 244, 228)
CARD = (255, 250, 236)
NAVY = (13, 38, 64)
NAVY_DARK = (9, 28, 48)
GOLD = (214, 158, 24)
GOLD_SOFT = (240, 196, 84)
INK = (24, 24, 22)
BODY = (70, 70, 64)
MUTED = (118, 110, 94)
WHITE = (255, 255, 255)
CRIMSON = (178, 34, 34)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning lines that fit max_width."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, fnt, color, max_width, leading):
    """Draw wrapped text; return the y just below the last line."""
    for ln in wrap(draw, text, fnt, max_width):
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title = font(SANS_BOLD, 52)
    d.text((34, 26), "THE WORLD IN ONE PAGE", font=title, fill=WHITE)
    sub = font(SANS_BOLD, 22)
    d.text((34, 84), "FRIDAY 20 NOVEMBER 2026  |  SIX STORIES, ONE DAY",
           font=sub, fill=GOLD_SOFT)
    issue = font(SANS, 22)
    d.text((W - 34 - d.textlength("No. 324", font=issue), 84),
           "No. 324", font=issue, fill=WHITE)
    d.rectangle([0, 118, W, 124], fill=GOLD)

    # ---- Lead story -----------------------------------------------------
    d.rectangle([24, 138, 1000, 404], fill=NAVY)
    d.rectangle([24, 138, 1000, 144], fill=GOLD)
    kick = font(SANS_BOLD, 24)
    d.text((52, 156), "USA  /  IRAN", font=kick, fill=GOLD_SOFT)
    num = font(SANS_BOLD, 34)
    d.text((1000 - 52 - d.textlength("01", font=num), 150), "01",
           font=num, fill=GOLD_SOFT)
    d.rectangle([52, 190, 98, 195], fill=GOLD)
    head = font(SANS_BOLD, 44)
    y = draw_wrapped(d, 52, 204,
                     "Trump pushes Iran war decision to 2027",
                     head, WHITE, 920, 50)
    d.rectangle([52, y + 8, 98, y + 13], fill=GOLD)
    deck = font(SANS, 25)
    draw_wrapped(d, 52, y + 24,
                 "\u201cWe\u2019ll see what happens after January 1,\u201d he "
                 "says aboard Air Force One; no new strikes this year "
                 "despite Israeli pressure.",
                 deck, WHITE, 920, 31)

    # ---- Story grid -----------------------------------------------------
    stories = [
        ("WEATHER  /  INDIA", CRIMSON,
         "Cyclone Akvan hits India's east coast",
         "Landfall near Gopalpur at noon; about 300,000 people "
         "evacuated to shelters, 423 rescue teams deployed.",
         "02"),
        ("INDIA  /  LAW", NAVY,
         "Judge: resignation is no admission of guilt",
         "Ex-judge Yashwant Varma tells Parliament his resignation "
         "ends the removal proceedings against him.",
         "03"),
        ("CULTURE  /  GAMING", NAVY,
         "GTA VI tops $1.84bn on launch day",
         "Sensor Tower's estimate passes The Odyssey's $1.805bn "
         "lifetime box office in a single day.",
         "04"),
        ("BUSINESS  /  AI", CRIMSON,
         "Anthropic soars in record Wall Street debut",
         "Shares close 17% up at $97.17 after a record $81.3bn IPO; "
         "the AI lab is valued near $1.8 trillion.",
         "05"),
    ]
    card_w, card_h = 476, 216
    xs = [24, 524]
    ys = [418, 648]
    kick_f = font(SANS_BOLD, 21)
    head_f = font(SANS_BOLD, 27)
    body_f = font(SANS, 19)
    num_f = font(SANS_BOLD, 28)
    for i, (kicker, accent, headline, body, number) in enumerate(stories):
        x, y = xs[i % 2], ys[i // 2]
        d.rectangle([x, y, x + card_w, y + card_h], fill=CARD,
                    outline=NAVY, width=2)
        d.rectangle([x, y, x + 8, y + card_h], fill=accent)
        tx = x + 26
        d.text((tx, y + 14), kicker, font=kick_f, fill=accent)
        d.rectangle([tx, y + 42, tx + 46, y + 47], fill=accent)
        hy = draw_wrapped(d, tx, y + 54, headline, head_f, INK, 424, 35)
        # Narrow body column so the corner number never collides with text.
        draw_wrapped(d, tx, hy + 8, body, body_f, BODY, 360, 24)
        d.text((x + card_w - 26 - d.textlength(number, font=num_f),
                y + card_h - 38), number, font=num_f, fill=NAVY)

    # ---- Bottom strip: cricket ------------------------------------------
    d.rectangle([24, 878, 1000, 984], fill=GOLD)
    d.text((52, 890), "SPORT  /  CRICKET", font=kick_f, fill=NAVY_DARK)
    storm = font(SANS_BOLD, 28)
    d.text((52, 912), "Phillips' 118 lifts New Zealand past 300",
           font=storm, fill=INK)
    storm_body = font(SANS, 19)
    d.text((52, 948),
           "Day two in Wellington: first hundreds in all three formats "
           "vs India in one year.",
           font=storm_body, fill=(58, 44, 8))
    d.ellipse([892, 896, 968, 972], outline=NAVY_DARK, width=4)
    circ = font(SANS_BOLD, 34)
    label = "06"
    d.text((930 - d.textlength(label, font=circ) / 2, 914), label,
           font=circ, fill=NAVY_DARK)

    # ---- Footer ---------------------------------------------------------
    foot = font(SANS, 19)
    d.text((24, 994), "Compiled from verified reports  |  One image, six stories",
           font=foot, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
