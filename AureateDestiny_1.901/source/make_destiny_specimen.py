#!/usr/bin/env python3
"""Specimen sheet for Aureate Destiny 1.901: both lattices, with every relation and its built value.
Text is shaped with HarfBuzz (kerning on) and drawn glyph by glyph."""
import os, json
import uharfbuzz as hb
from PIL import Image, ImageDraw, ImageFont
BASE = "/path/to/aureate"
D = os.path.join(BASE, "AureateDestiny_1.901"); F = os.path.join(D, "fonts/"); C17 = os.path.join(BASE, "AureateCollection_1.701/fonts/")
G, GB = F + "AureateDestiny-Regular.ttf", F + "AureateDestiny-Bold.ttf"
SO, SOB = F + "AureateDestinySolar-Regular.ttf", F + "AureateDestinySolar-Bold.ttf"
SANS, SANSC = C17 + "AureateSans-Regular.ttf", C17 + "AureateSansCondensed-Regular.ttf"
rep = json.load(open(os.path.join(D, "verification/destiny_report.json")))["fonts"]
RG, RS, RGB, RSB = rep["AureateDestiny-Regular"], rep["AureateDestinySolar-Regular"], rep["AureateDestiny-Bold"], rep["AureateDestinySolar-Bold"]
PAPER, INK, INK2, GOLD = (246, 244, 238), (25, 23, 18), (93, 87, 74), (116, 89, 15)
W, H, M = 2400, 5200, 150
img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
_hb = {}
def advances(path, text):
    if path not in _hb:
        face = hb.Face(hb.Blob.from_file_path(path)); _hb[path] = (hb.Font(face), face.upem)
    font, upem = _hb[path]; buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False})
    return [p.x_advance / upem for p in buf.glyph_positions]
def run(x, y, text, path, size, fill=INK):
    f = ImageFont.truetype(path, size)
    for ch, a in zip(text, advances(path, text)):
        d.text((x, y), ch, font=f, fill=fill, anchor="ls"); x += a * size
    return x
def fit(text, path, maxw, size):
    w = sum(advances(path, text)) * size; return size if w <= maxw else int(size * maxw / w)
def label(y, text): run(M, y, text.upper(), SANSC, 30, GOLD)
def rule(y): d.line([(M, y), (W - M, y)], fill=INK, width=2)
def classes(r):
    out = {}
    for g, name in r["width_rungs"].items(): out.setdefault(name.replace(" (as O)", ""), []).append(g)
    return out
def table(y, rows, cols=(M, M + 470, M + 1230, M + 1820)):
    for a, b, c, e in rows:
        if b is None:                                   # an order heading
            y += 14; run(M, y, a, SANSC, 30, GOLD); y += 46; continue
        run(cols[0], y, a, SANS, 29, INK2); run(cols[1], y, b, SANS, 29, INK); run(cols[2], y, c, SANS, 29, GOLD); run(cols[3], y, e, SANS, 29, INK); y += 44
    return y

y = 190; label(y, "Aureate Destiny  ·  Version 1.901  ·  one face in two proportional lattices"); rule(y + 30)
s = fit("AUREATE DESTINY", G, W - 2 * M, 300); y += 70 + int(s * 0.72); run(M, y, "AUREATE DESTINY", G, s)
y += 60; label(y, "Aureate Destiny  ·  the golden lattice  ·  Regular and Bold")
s = fit("ABCDEFGHIJKLMNOPQRSTUVWXYZ", G, W - 2 * M, 150); y += int(s * 0.95); run(M, y, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", G, s)
s2 = fit("0123456789  THE MEASURED WHOLE", GB, W - 2 * M, 150); y += int(s2 * 1.35); run(M, y, "0123456789  THE MEASURED WHOLE", GB, s2)
y += 110; rule(y)
s = fit("AUREATE DESTINY", SO, W - 2 * M, 300); y += 60 + int(s * 0.72); run(M, y, "AUREATE DESTINY", SO, s)
y += 60; label(y, "Aureate Destiny Solar  ·  the Apollonian lattice on the Sun's six and the lyre canon 6 : 8 : 9 : 12  ·  Regular and Bold")
s = fit("ABCDEFGHIJKLMNOPQRSTUVWXYZ", SO, W - 2 * M, 150); y += int(s * 0.95); run(M, y, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", SO, s)
s2 = fit("0123456789  THE MEASURED WHOLE", SOB, W - 2 * M, 150); y += int(s2 * 1.35); run(M, y, "0123456789  THE MEASURED WHOLE", SOB, s2)
y += 110; rule(y)

# ---- the golden lattice
mg = RG["measured"]; cg = classes(RG); wg = mg["widths"]
def letters(c, key): return " ".join(sorted(c.get(key, []))) or "none"
y += 70; label(y, "The golden lattice  ·  measure, relation, target, built (font units; x-height X = 898)")
y += 20
rows = [("First order: whole powers of φ", None, None, None),
        ("Cap height", "X · φ", "1453", str(1453)),
        ("Titling space", "X · φ⁻²", str(RG["targets"]["track"]), str(mg["adv_H"] - wg["H"] - 2 * 179 - (166 - mg["stem_I"])) + " added"),
        ("Word space", "X", "898", str(mg["space"])),
        ("Round overshoot", "C · φ⁻⁹", str(RG["targets"]["overshoot"]), f"{mg['O'][1] - 1453} above, {-mg['O'][0]} below"),
        ("Bold stem", "stem · φ", str(RGB["targets"]["stem"]), str(RGB["measured"]["stem_I"])),
        ("Second order: half powers, the mean of a step", None, None, None),
        ("Stem", "X · φ^(−9/2)", str(RG["targets"]["stem"]), str(mg["stem_I"])),
        ("Width of W", "C", "1453", str(wg["W"])),
        ("Width of " + letters(cg, "C·φ^-1/2"), "C · φ^(−1/2)", "1142", f"{wg['O']}, {wg['C']}, {wg['G']}"),
        ("Width of " + letters(cg, "C·φ^-1 = X")[:38], "C · φ⁻¹ = X", "898", f"{wg['H']}, {wg['N']}, {wg['T']}, {wg['S']}"),
        ("Width of " + letters(cg, "C·φ^-3/2"), "C · φ^(−3/2)", "706", f"{wg['E']}, {wg['F']}, {wg['L']}"),
        ("Third order: quarter powers, the mean of the mean", None, None, None),
        ("Width of " + letters(cg, "C·φ^-3/4"), "C · φ^(−3/4)", "1013", f"{wg['A']}, {wg['M']}, {wg['V']}"),
        ("Width of " + letters(cg, "C·φ^-5/4"), "C · φ^(−5/4)", "796", str(wg["P"])),
        ("Dot", "stem · φ^(3/4)", str(RG["targets"]["dot"]), str(mg["dot"])),
        ("Fourth order: eighth powers", None, None, None),
        ("Bar", "stem · φ^(−1/8)", str(RG["targets"]["bar"]), str(mg["bar_E"])),
        ("Small capital height", "X · φ^(1/8)", "954", str(mg["H_sc_top"])),
        ("Bold widths", "rung · φ^(1/8)", "H: 954", "H: " + str(RGB["measured"]["widths"]["H"]))]
y = table(y + 30, rows)

# ---- the solar lattice
ms = RS["measured"]; cs = classes(RS); ws = ms["widths"]
y += 50; rule(y); y += 70; label(y, "The Apollonian solar lattice  ·  whole numbers; the orders are ratios of ratios (cap height C = 1453)")
y += 20
rows = [("First order: the octave, 2 : 1", None, None, None),
        ("Word space : titling space", "C/2 : C/4", "726 : 363", f"{ms['space']} : {RS['targets']['track']}"),
        ("Cap height : width of " + letters(cs, "6/12 C"), "12 : 6", "726", f"{ws['E']}, {ws['F']}, {ws['L']}"),
        ("Second order: the fifth 3 : 2 and the fourth 4 : 3", None, None, None),
        ("Bold stem : stem", "3 : 2", f"{RSB['targets']['stem']} : {RS['targets']['stem']}", f"{RSB['measured']['stem_I']} : {ms['stem_I']}"),
        ("Dot : stem", "3 : 2", str(RS["targets"]["dot"]), str(ms["dot"])),
        ("Width of " + letters(cs, "9/12 C") + " : narrow", "9 : 6", "1090", f"{ws['O']}, {ws['C']}, {ws['G']}"),
        ("Width of W : round", "12 : 9", "1453", str(ws["W"])),
        ("Small capital : capital", "2 : 3", "969", str(ms["H_sc_top"])),
        ("Third order: the tone 9 : 8, a fifth less a fourth", None, None, None),
        ("Stem : bar", "9 : 8", f"{RS['targets']['stem']} : {RS['targets']['bar']}", f"{ms['stem_I']} : {ms['bar_E']}"),
        ("Round : width of " + letters(cs, "8/12 C")[:30], "9 : 8", "969", f"{ws['H']}, {ws['N']}, {ws['A']}, {ws['T']}"),
        ("Fourth order: the sevenths and the remainder", None, None, None),
        ("Width of " + letters(cs, "7/12 C"), "8 : 7 below the mean class, 7 : 6 above the narrow", "848", f"{ws['B']}, {ws['R']}, {ws['S']}, {ws['P']}"),
        ("Cap height : stem", "14 : 1, twice seven", str(RS["targets"]["stem"]), str(ms["stem_I"])),
        ("Round overshoot", "C / 72, six twelves", str(RS["targets"]["overshoot"]), f"{ms['O'][1] - 1453} above, {-ms['O'][0]} below"),
        ("Bold widths", "16 : 15", "H: " + str(round(969 * 16 / 15)), "H: " + str(RSB["measured"]["widths"]["H"]))]
y = table(y + 30, rows)
y += 40; run(M, y, "Both families derive from Aureate Sans Geometric, itself from Source Sans 3.  SIL Open Font License 1.1.  Aureate Type, 2026.", SANS, 28, INK2)
y += 34; run(M, y, "Solar is used in the traditional sense: the Sun's number six and the canon built on it. It is a typographic interpretation, not astronomy.", SANS, 28, INK2)
os.makedirs(os.path.join(D, "specimen"), exist_ok=True)
img = img.crop((0, 0, W, min(H, y + 110))); p = os.path.join(D, "specimen", "Aureate_Destiny_1.901_Specimen.png"); img.save(p); print(p, img.size)
