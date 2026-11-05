#!/usr/bin/env python3
"""Two plates for Aureate Destiny Serif 1.910.

  Specimen   the four programs set as titling, with small capitals
  Geometry   the five solids drawn from their coordinates, the stroke chains, the width rungs and the certificate's count

Destiny text is shaped with HarfBuzz (kerning on) and drawn from the outlines, so features such as c2sc show.
In a specimen string a lower-case letter means a small capital.
"""
import os, sys, json, math
import numpy as np
import uharfbuzz as hb
from PIL import Image, ImageDraw, ImageFont, ImageChops
from fontTools.ttLib import TTFont
from platonic import VERT, SOL, CORR, PHI

BASE = "/path/to/aureate"
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "AureateDestinySerif_1.910"); F = os.path.join(D, "fonts/"); C17 = os.path.join(BASE, "AureateCollection_1.701/fonts/")
G, GB = F + "AureateDestinySerif-Regular.ttf", F + "AureateDestinySerif-Bold.ttf"
SO, SOB = F + "AureateDestinySolarSerif-Regular.ttf", F + "AureateDestinySolarSerif-Bold.ttf"
SANS, SANSC = C17 + "AureateSans-Regular.ttf", C17 + "AureateSansCondensed-Regular.ttf"
cert = json.load(open(os.path.join(D, "verification/certificate.json"))); M = cert["measured"]
GR, GBm, SR, SBm = (M[k] for k in ("AureateDestinySerif-Regular", "AureateDestinySerif-Bold", "AureateDestinySolarSerif-Regular", "AureateDestinySolarSerif-Bold"))
PAPER, INK, INK2, GOLD, FAINT = (246, 244, 238), (25, 23, 18), (93, 87, 74), (116, 89, 15), (198, 192, 178)
W, MG = 2400, 150
X, C = 898, 1453

class Plate:
    def __init__(self, h): self.img = Image.new("RGB", (W, h), PAPER); self.d = ImageDraw.Draw(self.img); self._hb = {}; self._tt = {}
    def _font(self, path):
        if path not in self._hb:
            face = hb.Face(hb.Blob.from_file_path(path)); self._hb[path] = (hb.Font(face), face.upem); tt = TTFont(path); self._tt[path] = (tt, tt.getGlyphOrder())
        return self._hb[path] + self._tt[path]
    def shape(self, path, text, feats=None):
        font, upem, tt, order = self._font(path)
        if not text: return []
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(font, buf, {"kern": True, "liga": False, **(feats or {})})
        return [(order[i.codepoint], p.x_advance / upem) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]
    def glyphs(self, path, text):
        """Lower-case letters are small capitals: runs are shaped with c2sc on."""
        out = []; run = ""; low = False
        for ch in text:
            cls = ch.islower() if ch.isalpha() else low
            if run and cls != low: out += self.shape(path, run.upper(), {"c2sc": True} if low else None); run = ""
            low = cls; run += ch
        if run: out += self.shape(path, run.upper(), {"c2sc": True} if low else None)
        return out
    def width(self, path, text): return sum(a for _, a in self.glyphs(path, text))
    def polys(self, path, name):
        tt = self._font(path)[2]; gl = tt["glyf"][name]; out = []
        if gl.numberOfContours <= 0: return out
        st = 0
        for e in gl.endPtsOfContours:
            pts = [(gl.coordinates[i][0], gl.coordinates[i][1], gl.flags[i] & 1) for i in range(st, e + 1)]; st = e + 1; full = []
            for i, p in enumerate(pts):
                q = pts[(i + 1) % len(pts)]; full.append(p)
                if not p[2] and not q[2]: full.append(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 1))
            k0 = next(i for i, p in enumerate(full) if p[2]); full = full[k0:] + full[:k0] + [full[k0]]; poly = [full[0][:2]]; i = 1
            while i < len(full):
                if full[i][2]: poly.append(full[i][:2]); i += 1
                else:
                    a, c, b = poly[-1], full[i], full[i + 1]
                    for t in (0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0): poly.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]))
                    i += 2
            out.append(poly)
        return out
    def text(self, x, y, text, path, size, fill=INK):
        """Draw Destiny text on the baseline y from its outlines, three times oversampled."""
        upem = self._font(path)[1]; ss = 3
        for name, adv in self.glyphs(path, text):
            ps = self.polys(path, name)
            if ps:
                xs = [p[0] for poly in ps for p in poly]; ys = [p[1] for poly in ps for p in poly]; k = size / upem
                x0, x1 = math.floor(x + min(xs) * k) - 1, math.ceil(x + max(xs) * k) + 1; y0, y1 = math.floor(y - max(ys) * k) - 1, math.ceil(y - min(ys) * k) + 1
                acc = Image.new("1", ((x1 - x0) * ss, (y1 - y0) * ss), 0)
                for poly in ps:
                    one = Image.new("1", acc.size, 0); ImageDraw.Draw(one).polygon([((x + px * k - x0) * ss, (y - py * k - y0) * ss) for px, py in poly], fill=1)
                    acc = ImageChops.logical_xor(acc, one)
                self.img.paste(fill, (x0, y0), acc.convert("L").resize((x1 - x0, y1 - y0), Image.LANCZOS))
            x += adv * size
        return x
    def fit(self, text, path, maxw, size): w = self.width(path, text) * size; return size if w <= maxw else size * maxw / w
    def label(self, x, y, text, size=29, fill=INK2, path=SANS, anchor="ls"):
        f = ImageFont.truetype(path, size)
        if anchor != "ls": self.d.text((x, y), text, font=f, fill=fill, anchor=anchor); return x
        for ch, (_, a) in zip(text, self.shape(path, text)): self.d.text((x, y), ch, font=f, fill=fill, anchor="ls"); x += a * size
        return x
    def head(self, y, text): self.label(MG, y, "".join(c if c in "φρ" else c.upper() for c in text), 30, GOLD, SANSC)
    def rule(self, y, fill=INK, width=2): self.d.line([(MG, y), (W - MG, y)], fill=fill, width=width)
    def save(self, name, h):
        os.makedirs(os.path.join(D, "specimen"), exist_ok=True); p = os.path.join(D, "specimen", name); self.img.crop((0, 0, W, h)).save(p); print(p, (W, h)); return p

def n(v, d=2): return f"{v:.{d}f}".rstrip("0").rstrip(".")

# =============================================================================== plate one: the specimen
def specimen():
    P = Plate(6400); y = 190
    P.head(y, "Aureate Destiny Serif  ·  Version 1.910  ·  light titling capitals with serifs, in two lattices"); P.rule(y + 30)
    def family(y, reg, bold, title, caption, lines):
        s = P.fit(title, reg, W - 2 * MG, 300); y += 70 + int(s * 0.72); P.text(MG, y, title, reg, s)
        y += 62; P.head(y, caption)
        for text, path, size in lines:
            s = P.fit(text, path, W - 2 * MG, size); y += int(s * 1.02) + 36; P.text(MG, y, text, path, s)
        return y + 96
    y = family(y, G, GB, "AUREATE DESTINY", "Aureate Destiny Serif  ·  the golden lattice, on the icosahedron and the dodecahedron  ·  Regular and Bold",
               [("ABCDEFGHIJKLM", G, 180), ("NOPQRSTUVWXYZ", G, 180), ("0123456789  &?!", G, 180), ("THE MEASURED WHOLE", GB, 180),
                ("Water and the Heavens", G, 150), ("Ars Sine Scientia Nihil Est", GB, 120), ("FRANÇAIS  ŚWIĘTO  ÆTHER  ØRSTED", G, 110)])
    P.rule(y); y += 10
    y = family(y, SO, SOB, "AUREATE DESTINY", "Aureate Destiny Solar Serif  ·  the Apollonian lattice, on the tetrahedron, the octahedron and the cube  ·  Regular and Bold",
               [("ABCDEFGHIJKLM", SO, 180), ("NOPQRSTUVWXYZ", SO, 180), ("0123456789  &?!", SO, 180), ("THE MEASURED WHOLE", SOB, 180),
                ("Fire  Air  Earth", SO, 150), ("The Harmony of the Spheres", SOB, 120), ("FRANÇAIS  ŚWIĘTO  ÆTHER  ØRSTED", SO, 110)])
    P.rule(y); y += 60
    P.label(MG, y, "Both cases type capitals. Small capitals come through the c2sc feature; above they stand for the lower case of the titles.", 28)
    y += 38; P.label(MG, y, "Derived from Aureate Roman Living Tall 1.701, itself from Liberation Serif.  SIL Open Font License 1.1.  Aureate Type, 2026.", 28)
    return P.save("Aureate_Destiny_Serif_1.910_Specimen.png", y + 110)

# =============================================================================== plate two: the geometry
def rot(P_, ax, ay, az=0.0):
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]); Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return P_ @ (Rx @ Ry @ Rz).T
VIEW = {"tetrahedron": (0.35, 0.5, 0.2), "cube": (0.42, 0.55, 0.0), "octahedron": (0.3, 0.42, 0.0), "icosahedron": (0.24, 0.2, 0.0), "dodecahedron": (0.2, 0.33, 0.0)}
def draw_solid(P, cx, cy, rad, name):
    s = SOL[name]; V = rot(VERT[name] / (s["R"] * s["edge"]), *VIEW[name]) * rad
    for rr, col, wd in ((1.0, FAINT, 2), (s["rho"] / s["R"], GOLD, 2), (s["r"] / s["R"], GOLD, 2)):
        P.d.ellipse([cx - rad * rr, cy - rad * rr, cx + rad * rr, cy + rad * rr], outline=col, width=wd)
    U = rot(VERT[name], *VIEW[name]); N = rot(np.array([p_[0] for p_ in s["face_planes"]]), *VIEW[name]); H = [p_[1] for p_ in s["face_planes"]]
    def seen(i, j):                                          # an edge shows when one of its two faces looks toward the viewer
        return any(N[f][2] > 1e-9 and abs(N[f] @ U[i] - H[f]) < 1e-6 and abs(N[f] @ U[j] - H[f]) < 1e-6 for f in range(len(H)))
    edges = sorted(s["edge_list"], key=lambda e: seen(*e))
    for i, j in edges:
        back = not seen(i, j)
        P.d.line([(cx + V[i][0], cy - V[i][1]), (cx + V[j][0], cy - V[j][1])], fill=FAINT if back else INK, width=3 if back else 5)

def geometry():
    P = Plate(9000); y = 190
    P.head(y, "Aureate Destiny Serif 1.910  ·  the geometry  ·  every number below is measured, in the solids and in the fonts"); P.rule(y + 30)
    # ---- the five solids
    y += 100; P.head(y, "The five regular solids, drawn from their vertex coordinates. Gold rings: insphere and midsphere. Grey ring: circumsphere. Edge = 1.")
    cols = [MG + 210 + i * 420 for i in range(5)]; cy = y + 300; rad = 185
    gives = {"tetrahedron": ["Solar: serif = r, hairline = ρ", "of the tetrahedron on two stems;", "Bold stem = R, enlarged"],
             "octahedron": ["Solar: the Bold step", "ρ : r = √(3/2);", "stem : hairline = R : ρ = √2"],
             "cube": ["Solar: hairline : serif = R : r = √3;", "widths C, C·√3/2 and C ÷ √2", "(face, circumradius, edge)"],
             "icosahedron": ["Golden: hairline = ρ on an edge", "of two serifs; three golden", "rectangles X by C"],
             "dodecahedron": ["Golden: stem = ρ on an edge of", "two serifs; inscribed cube", "of edge C on edge X"]}
    for cx, name in zip(cols, ("tetrahedron", "octahedron", "cube", "icosahedron", "dodecahedron")):
        draw_solid(P, cx, cy, rad, name); s = SOL[name]; ty = cy + rad + 62
        P.label(cx, ty, name.capitalize(), 36, INK, SANS, "ms"); ty += 42
        P.label(cx, ty, f"{CORR[name][0]}  ·  {s['vertices']} V, {s['edges']} E, {s['faces']} F", 26, GOLD, SANS, "ms"); ty += 38
        P.label(cx, ty, f"r {s['r']:.4f}   ρ {s['rho']:.4f}   R {s['R']:.4f}", 26, INK2, SANS, "ms"); ty += 34
        P.label(cx, ty, f"ρ:r {s['rho'] / s['r']:.4f}   R:ρ {s['R'] / s['rho']:.4f}   R:r {s['R'] / s['r']:.4f}", 26, INK2, SANS, "ms"); ty += 44
        for line in gives[name]: P.label(cx, ty, line, 25, INK, SANS, "ms"); ty += 32
    y = ty + 20
    P.label(MG, y, "Elements after Plato's Timaeus. Kepler set the cube between Saturn and Jupiter, the tetrahedron between Jupiter and Mars, the dodecahedron between Mars and Earth,", 26); y += 34
    P.label(MG, y, "the icosahedron between Earth and Venus, the octahedron between Venus and Mercury. These are traditional correspondences, not astronomy.", 26)
    y += 60; P.rule(y)

    # ---- the stroke chains
    def chain(y, title, reg, bold, rows, note):
        y += 70; P.head(y, title); k = 1.5; x = MG; base = y + 330
        for name, relation, target, built, tb, bb in rows:
            wpx = target * k; P.d.rectangle([x, base - 250, x + wpx, base], fill=INK)
            P.label(x, base + 46, name, 30, INK); P.label(x, base + 84, relation, 25, GOLD)
            P.label(x, base + 120, f"target {n(target)}  built {n(built)}", 25, INK2); P.label(x, base + 154, f"Bold {n(tb)}  built {n(bb)}", 25, INK2)
            x += 520
        y = base + 200; P.label(MG, y, note, 26); return y + 50
    gs, gh, gst = X * PHI ** -6.5, X * PHI ** -5.5, X * PHI ** -4.5
    y = chain(y, "Aureate Destiny Serif  ·  the stroke chain  ·  serif : hairline : stem = 1 : φ : φ², the midspheres of the icosahedron and the dodecahedron on one edge", GR, GBm,
              [("Serif", "half the common edge", gs, GR["serif"], gs * PHI ** 0.25, GBm["serif"]), ("Hairline", "ρ of the icosahedron, serif·φ", gh, GR["hair"], gh * PHI ** 0.5, GBm["hair"]),
               ("Stem", "ρ of the dodecahedron, X·φ^(−9/2)", gst, GR["stem"], gst * PHI, GBm["stem"]), ("Bowl", "stem·φ^(1/4)", gst * PHI ** 0.25, GR["bowl"], gst * PHI ** 1.25, GBm["bowl"])],
              "Bold steps by a whole power for the stem, a half power for the hairline and a quarter power for the serif: first, second and third order.")
    P.rule(y, FAINT)
    ss = C / 14; se = ss / 6 ** 0.5; sh = se * 3 ** 0.5; q = 1.5 ** 0.5
    y = chain(y, "Aureate Destiny Solar Serif  ·  the stroke chain  ·  serif : hairline : stem = 1 : √3 : √6, one tetrahedron whose edge is two stems; the capital is 14 stems", SR, SBm,
              [("Serif", "r of the tetrahedron", se, SR["serif"], se * q, SBm["serif"]), ("Hairline", "ρ of the tetrahedron, serif·√3", sh, SR["hair"], sh * q, SBm["hair"]),
               ("Stem", "half the edge, C ÷ 14", ss, SR["stem"], ss * 1.5, SBm["stem"]), ("Bowl", "stem·9/8, the tone", ss * 9 / 8, SR["bowl"], ss * 1.5 * 9 / 8, SBm["bowl"])],
              "Bold is the same tetrahedron enlarged by the octahedron's ρ : r = √(3/2); its circumsphere is the Bold stem, so Bold stem : stem = 3 : 2 and Bold serif : hairline : stem = 1 : √3 : 3.")
    P.rule(y)

    # ---- the width rungs
    def ladder(y, title, path, m, rungs):
        y += 70; P.head(y, title); y += 30; k = 0.5; x_bar = MG + 1050
        for name, value, letters in rungs:
            y += 118; P.text(MG, y, " ".join(letters), path, P.fit(" ".join(letters), path, 980, 96))
            P.d.rectangle([x_bar, y - 40, x_bar + value * k, y - 28], fill=GOLD)
            ws = [m["widths"][g] for g in letters]; built = str(ws[0]) if len(set(ws)) == 1 else f"{min(ws)} to {max(ws)}"
            P.label(x_bar, y - 56, f"{name}  =  {n(value)}", 27, INK); P.label(x_bar, y + 6, f"built {built}", 25, INK2)
        return y + 70
    y = ladder(y, "Aureate Destiny Serif  ·  capital ink widths on quarter powers of φ (the Kepler triangle 1 : √φ : φ, and its mean)", G, GR,
               [("C·φ^(1/2)", C * PHI ** 0.5, "W"), ("C·φ^(1/4)", C * PHI ** 0.25, "M"), ("C", C, "AHKNUVXY"), ("C·φ^(−1/4)", C * PHI ** -0.25, "DGOQR"), ("C·φ^(−1/2)", C * PHI ** -0.5, "BCELTZ"),
                ("C·φ^(−3/4)", C * PHI ** -0.75, "FP"), ("C·φ^(−1) = X", C / PHI, "S"), ("C·φ^(−3/2)", C * PHI ** -1.5, "J"), ("C·φ^(−2)", C * PHI ** -2, "I")])
    P.rule(y, FAINT)
    y = ladder(y, "Aureate Destiny Solar Serif  ·  capital ink widths in twelfths of the capital, with the cube's two roots", SO, SR,
               [("16/12 C", C * 16 / 12, "W"), ("14/12 C", C * 14 / 12, "M"), ("12/12 C, the cube's face", C, "AHKNUVXY"), ("√3/2 C, the cube's circumradius", C * 3 ** 0.5 / 2, "DGOQR"), ("10/12 C", C * 10 / 12, "BCLTZ"),
                ("9/12 C", C * 9 / 12, "E"), ("C ÷ √2, edge from face diagonal", C / 2 ** 0.5, "FP"), ("7/12 C", C * 7 / 12, "S"), ("6/12 C", C / 2, "J")])
    P.rule(y)

    # ---- lining, spacing and the count
    y += 70; P.head(y, "Lining and spacing  ·  measure, relation, target, built")
    rows = [("", "Aureate Destiny Serif", "", "Aureate Destiny Solar Serif", ""),
            ("Round overshoot", "C·φ^(−8)", f"{round(C * PHI ** -8)}, built {n(GR['over_top']['O'])} and {n(GR['over_bottom']['O'])}", "C ÷ 48", f"{round(C / 48)}, built {n(SR['over_top']['O'])} and {n(SR['over_bottom']['O'])}"),
            ("Apex of A", "C·φ^(−9)", f"{round(C * PHI ** -9)}, built {n(GR['apex'])}", "C ÷ 72", f"{round(C / 72)}, built {n(SR['apex'])}"),
            ("Vertex of V", "C·φ^(−15/2)", f"{round(C * PHI ** -7.5)}, built {n(GR['vertex']['V'])}", "C ÷ 36", f"{round(C / 36)}, built {n(SR['vertex']['V'])}"),
            ("Small capital", "X·φ^(1/8)", f"{round(X * PHI ** 0.125)}, built {n(GR['sc'])}", "C·2/3", f"{round(C * 2 / 3)}, built {n(SR['sc'])}"),
            ("Titling space", "X·φ^(−2)", f"{round(X * PHI ** -2)}, built {n(GR['track']['H'])}", "C ÷ 4", f"{round(C / 4)}, built {n(SR['track']['H'])}"),
            ("Word space", "X", f"{X}, built {n(GR['space'])}", "C ÷ 2", f"{round(C / 2)}, built {n(SR['space'])}"),
            ("Dot", "stem·φ^(3/4)", f"{n(X * PHI ** -3.75, 1)}, built {n(GR['dot'])}", "stem·3/2", f"{n(C / 14 * 1.5, 1)}, built {n(SR['dot'])}"),
            ("Exclamation wedge", "stem·φ^(1/2)", f"{n(X * PHI ** -4, 1)}, built {n(GR['wedge'])}", "stem·4/3", f"{n(C / 14 * 4 / 3, 1)}, built {n(SR['wedge'])}")]
    cx = (MG, MG + 400, MG + 700, MG + 1250, MG + 1550); y += 20
    for r in rows:
        y += 46
        for xx, t, col in zip(cx, r, (INK2, GOLD, INK, GOLD, INK)): P.label(xx, y, t, 28, col if r[0] else GOLD)
    y += 70; P.rule(y); y += 70; P.head(y, "The certificate  ·  relations measured in the finished fonts, and how many hold within tolerance")
    for fam, s_ in cert["summary"].items():
        y += 46; P.label(MG, y, "The five solids against their closed forms" if fam == "solids" else fam, 28, INK2); P.label(MG + 900, y, f"{s_['passed']} of {s_['relations']}", 28, INK)
    y += 60; P.label(MG, y, "Tolerance: one unit on a stroke or a width (outlines sit on whole units, 2048 to the em), half a unit on a line or a height. Full table in verification/CERTIFICATE.md.", 26)
    return P.save("Aureate_Destiny_Serif_1.910_Geometry.png", y + 110)

if __name__ == "__main__":
    specimen(); geometry()
