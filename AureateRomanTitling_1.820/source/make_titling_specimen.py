#!/usr/bin/env python3
"""Specimen sheet for Aureate Roman Titling 1.820. Text is shaped with HarfBuzz (kerning on)
and drawn glyph by glyph, so the spacing shown is the fonts' own."""
import os
import uharfbuzz as hb
from PIL import Image, ImageDraw, ImageFont
BASE = "/path/to/aureate"
T = os.path.join(BASE, "AureateRomanTitling_1.820/fonts/"); T0 = os.path.join(BASE, "AureateRomanTitling_1.800/fonts/"); C = os.path.join(BASE, "AureateCollection_1.701/fonts/")
R, B = T + "AureateRomanTitling-Regular.ttf", T + "AureateRomanTitling-Bold.ttf"
SC, SCB = T + "AureateRomanTitlingSC-Regular.ttf", T + "AureateRomanTitlingSC-Bold.ttf"
SANS, SANSC, TALL = C + "AureateSans-Regular.ttf", C + "AureateSansCondensed-Regular.ttf", C + "AureateRomanLivingTall-Regular.ttf"
PAPER, INK, INK2, GOLD = (246, 244, 238), (25, 23, 18), (93, 87, 74), (116, 89, 15)
W, H, M = 2400, 3600, 150
img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
_hb = {}
def advances(path, text):
    if path not in _hb:
        face = hb.Face(hb.Blob.from_file_path(path)); _hb[path] = (hb.Font(face), face.upem)
    font, upem = _hb[path]; buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False})
    return [p.x_advance / upem for p in buf.glyph_positions]
def width(path, text, size): return sum(advances(path, text)) * size
def run(x, y, text, path, size, fill=INK):
    f = ImageFont.truetype(path, size); adv = advances(path, text)
    for ch, a in zip(text, adv):
        d.text((x, y), ch, font=f, fill=fill, anchor="ls"); x += a * size
    return x
def fit(text, path, maxw, size):
    w = width(path, text, size); return size if w <= maxw else int(size * maxw / w)
def label(y, text): run(M, y, text.upper(), SANSC, 30, GOLD)
def rule(y): d.line([(M, y), (W - M, y)], fill=(25, 23, 18), width=2)

y = 190; label(y, "Aureate Roman Titling  ·  Version 1.820  ·  Regular and Bold, with small-capital families"); rule(y + 30)
s = fit("The Measured Whole", SC, W - 2 * M, 330); y += 60 + int(s * 0.74); run(M, y, "The Measured Whole", SC, s)
s2 = fit("Apollo and the Authority of Exact Particulars", SC, W - 2 * M, 120); y += int(s2 * 1.25); run(M, y, "Apollo and the Authority of Exact Particulars", SC, s2)
y += 120; rule(y)
y += 70; label(y, "Titling Regular  ·  capitals at 1453, the Tall stature")
s = fit("ABCDEFGHIJKLMNOPQRSTUVWXYZ", R, W - 2 * M, 150); y += int(s * 0.95); run(M, y, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", R, s)
y += 80; label(y, "Titling SC Regular  ·  drawn small capitals at 954 in the lowercase positions")
s = fit("abcdefghijklmnopqrstuvwxyz  0123456789", SC, W - 2 * M, 150); y += int(s * 0.95); run(M, y, "abcdefghijklmnopqrstuvwxyz  0123456789", SC, s)
y += 80; label(y, "Titling Bold and Titling SC Bold")
s = fit("MARY MOUNT RESEARCH  MMXXVI", B, W - 2 * M, 170); y += int(s * 0.95); run(M, y, "MARY MOUNT RESEARCH  MMXXVI", B, s)
s = fit("Form, Reason, Rhythm: The Collection in Proportion", SCB, W - 2 * M, 120); y += int(s * 1.3); run(M, y, "Form, Reason, Rhythm: The Collection in Proportion", SCB, s)
y += 80; label(y, "Titling Regular  ·  lowercase kept for mixed-case titles; smcp and c2sc still apply")
s = fit("Beauty requires a lucid whole, quietly measured.", R, W - 2 * M, 130); y += int(s * 1.0); run(M, y, "Beauty requires a lucid whole, quietly measured.", R, s)
y += 80; label(y, "Greek and Cyrillic capitals")
s = fit("ΑΠΟΛΛΩΝ ΚΑΙ ΤΟ ΜΕΤΡΟΝ   СОРАЗМЕРНОСТЬ", R, W - 2 * M, 120); y += int(s * 1.0); run(M, y, "ΑΠΟΛΛΩΝ ΚΑΙ ΤΟ ΜΕΤΡΟΝ   СОРАЗМЕРНОСТЬ", R, s)
y += 90; rule(y)
# proportion: lines and weights, then the table
y += 70; label(y, "Lines and weights  ·  1.800 (left, grey) and 1.820 (right), same size")
size = 430; yy = y + int(size * 0.84)
run(M, yy, "HAVE", T0 + "AureateRomanTitling-Regular.ttf", size, INK2); x1 = M + 1080; run(x1, yy, "HAVE", R, size)
u = size / 2048
for val, name in ((1503, "pointed  C + 50"), (1484, "round  C + 31"), (1453, "cap  C = 1453"), (0, "baseline"), (-50, "pointed  −50")):
    yl = yy - val * u; d.line([(x1 - 20, yl), (W - M, yl)], fill=GOLD, width=1)
y = yy + 150
rows = [("Capital : x-height", "1453 : 898", "φ  (1.61804)"),
        ("Small capital : x-height", "954 : 898", "φ to the 1/8"),
        ("Hairline : stem : bold stem", "72 : 116.5 : 188.5", "1 : φ : φ²"),
        ("Every other stroke", "H + (p − H) × k from the Roman's own thickness p", "one law for stems, diagonals, bowls"),
        ("Round overshoot", "31 above C, 31 below the baseline", "C × φ to the −8"),
        ("Pointed overshoot (A, V, W, N)", "50", "C × φ to the −7, the round overshoot × φ"),
        ("Lining figures", "flat at 0 and 1453, rounds at −31 and 1484", "the capital lines"),
        ("Envelope", "0.7862 of the Tall Roman", "φ to the −1/2"),
        ("Titling space · word space", "81 per glyph · 484", "X × φ to the −5 · em × φ to the −3")]
c1, c2 = M + 620, M + 1420
for a_, b_, c_ in rows:
    run(M, y, a_, SANS, 32, INK2); run(c1, y, b_, SANS, 32, INK); run(c2, y, c_, SANS, 32, GOLD); y += 50
y += 14; run(M, y, "Derived from Aureate Roman Living Tall, itself from Liberation Serif.  SIL Open Font License 1.1.  Aureate Type, 2026.", SANS, 30, INK2); y += 40
out = os.path.join(BASE, "AureateRomanTitling_1.820/specimen"); os.makedirs(out, exist_ok=True)
img = img.crop((0, 0, W, min(H, y + 110))); p = os.path.join(out, "Aureate_Roman_Titling_1.820_Specimen.png"); img.save(p); print(p, img.size)
