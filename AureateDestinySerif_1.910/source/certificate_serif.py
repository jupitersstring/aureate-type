#!/usr/bin/env python3
"""Certificate for Aureate Destiny Serif 1.910.

Nothing here is taken from the builder. The five regular solids are constructed from their vertex
coordinates; their inradius r, midradius ρ and circumradius R are measured from those coordinates
(edge = 1) and checked against the closed forms. Every relation of the two lattices is then stated
as a number and measured in the finished fonts, with a tolerance and a verdict.

    python3 certificate_serif.py [package directory]
"""
import os, sys, json, math, itertools
import numpy as np
from fontTools.ttLib import TTFont
import build_titling as bt

PHI = (1 + 5 ** 0.5) / 2; R2, R3, R6 = 2 ** 0.5, 3 ** 0.5, 6 ** 0.5
BASE = "/path/to/aureate"
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "AureateDestinySerif_1.910")
SRC = os.path.join(BASE, "AureateCollection_1.701/fonts/AureateRomanLivingTall-Regular.ttf")
X, C = 898, 1453

from platonic import VERT, SOL, CLOSED, EULER, CORR
T, K, O, I, Dd = (SOL[k] for k in ("tetrahedron", "cube", "octahedron", "icosahedron", "dodecahedron"))

# ------------------------------------------------------------------ measuring a font
def runs(gs, g, y=None, x=None):
    S = bt.flatten(gs[g]); x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
    if y is not None:
        m = ((y1 <= y) & (y2 > y)) | ((y2 <= y) & (y1 > y)); v = np.sort(x1[m] + (y - y1[m]) * (x2[m] - x1[m]) / (y2[m] - y1[m]))
    else:
        m = ((x1 <= x) & (x2 > x)) | ((x2 <= x) & (x1 > x)); v = np.sort(y1[m] + (x - x1[m]) * (y2[m] - y1[m]) / (x2[m] - x1[m]))
    return [float(v[i + 1] - v[i]) for i in range(0, len(v) - 1, 2)]
def box(gs, g): gl = gs[g]; gl.recalcBounds(gs); return gl.xMin, gl.yMin, gl.xMax, gl.yMax
def serif_tip_old(gs, g="I"):
    b = box(gs, g); return runs(gs, g, x=b[0] + 12.37)[0]
def serif_tips(gs, g, top):
    """Heights of the serif tips: the short upright edges that end a foot on the baseline or a head on the top line."""
    gl = gs[g]; out = []; st = 0
    for e in gl.endPtsOfContours:
        idx = list(range(st, e + 1)); st = e + 1; n = len(idx)
        for k in range(n):
            i, j = idx[k], idx[(k + 1) % n]; (x1, y1), (x2, y2) = gl.coordinates[i], gl.coordinates[j]
            if not (gl.flags[i] & 1 and gl.flags[j] & 1) or x1 != x2: continue
            h = abs(y2 - y1); o, q = ((i, idx[(k - 1) % n]) if min(y1, y2) == y1 else (j, idx[(k + 2) % n])) if min(y1, y2) == 0 else ((i, idx[(k - 1) % n]) if max(y1, y2) == y1 else (j, idx[(k + 2) % n]))
            if (min(y1, y2) == 0 or max(y1, y2) == top) and 15 <= h <= 110 and gl.coordinates[q][1] == gl.coordinates[o][1] and abs(gl.coordinates[q][0] - x1) >= 30:
                inner = j if o == i else i; r_ = idx[(k + 2) % n] if inner == j else idx[(k - 1) % n]
                if abs(gl.coordinates[r_][1] - gl.coordinates[inner][1]) < 4 and (gl.flags[r_] & 1): continue      # the end of a plain bar
                out.append(float(h))
    return out
def serif_tip(gs, g="I", top=1453):
    t = serif_tips(gs, g, top); return max(t, key=lambda v: abs(v - sorted(t)[len(t) // 2])) if t else None    # the tip farthest from the median: the worst one
def bowl(font, g="O"):
    import measure_strokes as ms
    mid, inw, th, ln = ms.glyph_thickness(font["glyf"][g]); v = th[np.isfinite(th) & (th < 400)]
    return float(np.percentile(v, 97))
def measure(path):
    f = TTFont(path); gs = f["glyf"]; hm = f["hmtx"].metrics; s = TTFont(SRC); sg = s["glyf"]; shm = s["hmtx"].metrics; m = {}
    yq = 0.3 * C + 0.37
    m["stems"] = {g: runs(gs, g, y=yq)[0] for g in "BDEFHIKLPRT"}; m["stems"]["H right"] = runs(gs, "H", y=yq)[1]
    m["stems"]["1"] = runs(gs, "one", y=yq)[0]; m["stems"]["4"] = runs(gs, "four", y=0.6 * C + 0.37)[-1]
    def vx(g, frac=0.5): b = box(gs, g); return runs(gs, g, x=b[0] + frac * (b[2] - b[0]) + 0.37)
    e = vx("E", 0.6); fz = vx("F", 0.6); z = vx("Z"); a = vx("A"); l = vx("L", 0.6); t = vx("T", 0.25)
    m["hairlines"] = {"H bar": vx("H")[0], "E foot arm": e[0], "E middle arm": e[1], "E top arm": e[-1], "F middle arm": fz[-2], "F top arm": fz[-1],
                      "L arm": l[0], "T bar, left": t[-1], "T bar, right": vx("T", 0.75)[-1], "Z foot": z[0], "Z top": z[-1], "A bar": a[0]}
    m["stem"] = m["stems"]["I"]; m["hair"] = m["hairlines"]["H bar"]; m["serif"] = serif_tips(gs, "I", C)[0]; m["bowl"] = bowl(f)
    m["serifs"] = {g: serif_tips(gs, g, C) for g in "ABDEFHIKLMNPRTUVWXY"}; m["serifs"]["1"] = serif_tips(gs, "one", C)
    for g, k in (("O", "O"), ("C", "C"), ("G", "G"), ("S", "S"), ("zero", "0"), ("eight", "8")):
        b = box(gs, g); m.setdefault("over_top", {})[k] = b[3] - C; m.setdefault("over_bottom", {})[k] = -b[1]
    m["apex"] = box(gs, "A")[3] - C; m["vertex"] = {g: -box(gs, g)[1] for g in "VW"}; m["cap"] = box(gs, "H")[3]; m["base"] = box(gs, "H")[1]
    m["sc"] = box(gs, "H.aursc")[3]; m["sc_stem"] = runs(gs, "H.aursc", y=0.3 * m["sc"] + 0.37)[0]
    m["sc_hair"] = vx("H.aursc")[0]; m["sc_serif"] = serif_tips(gs, "H.aursc", m["sc"]); m["sc_serif_T"] = serif_tips(gs, "T.aursc", m["sc"]); m["sc_T_bar"] = vx("T.aursc", 0.25)[-1]; m["sc_E_stem"] = runs(gs, "E.aursc", y=0.3 * m["sc"] + 0.37)[0]
    def sb(g_, font_gs, font_hm): b = box(font_gs, g_); return b[0] + font_hm[g_][0] - b[2]
    m["track"] = {g: sb(g, gs, hm) - sb(g, sg, shm) for g in "HOAE"}; m["space"] = hm["space"][0]
    b = box(gs, "period"); m["dot"] = b[2] - b[0]
    gl = gs["exclam"]; st = 0; m["wedge"] = None
    for e_ in gl.endPtsOfContours:
        seg = gl.coordinates[st:e_ + 1]; ys = [q[1] for q in seg]; xs = [q[0] for q in seg]; st = e_ + 1
        if max(ys) - min(ys) > 0.4 * X: m["wedge"] = max(xs) - min(xs)
    m["widths"] = {g: box(gs, g)[2] - box(gs, g)[0] for g in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    m["os2"] = {"xHeight": f["OS/2"].sxHeight, "capHeight": f["OS/2"].sCapHeight, "upm": f["head"].unitsPerEm}
    m["Q_body_bottom"] = None
    return m

# ------------------------------------------------------------------ the relations
rows = []
def rel(family, group, name, statement, expected, measured, tol, kind="length"):
    ok = measured is not None and abs(measured - expected) <= tol + 1e-9
    rows.append(dict(family=family, group=group, name=name, statement=statement, expected=expected, measured=measured, tolerance=tol, kind=kind, verdict="pass" if ok else "FAIL"))
def ratio(family, group, name, statement, expected, a, b, q=0.75):
    """A ratio of two measured lengths; the tolerance is what a ±q unit reading error on each length allows."""
    rel(family, group, name, statement, expected, a / b, (a / b) * (q / a + q / b), "ratio")

def P(n): return os.path.join(D, "fonts", n + ".ttf")
GR, GB = measure(P("AureateDestinySerif-Regular")), measure(P("AureateDestinySerif-Bold"))
SR, SB = measure(P("AureateDestinySolarSerif-Regular")), measure(P("AureateDestinySolarSerif-Bold"))

# ---- solids against their closed forms
for k, s in SOL.items():
    for nm, got, want in zip(("r", "ρ", "R"), (s["r"], s["rho"], s["R"]), CLOSED[k]):
        rel("solids", k, f"{nm} of the {k}, edge 1", "measured from vertex coordinates against the closed form", want, got, 1e-9, "number")
    rel("solids", k, f"vertices, edges, faces of the {k}", "counted from coordinates; V − E + F = 2", 2, s["vertices"] - s["edges"] + s["faces"], 0, "count")

# ---- Aureate Destiny Serif: the golden lattice on the icosahedron and the dodecahedron
F = "Aureate Destiny Serif"
stem = X * PHI ** -4.5; hair = stem / PHI; serif = hair / PHI
ratio(F, "datum", "cap height : x-height", "the icosahedron of edge X spans three golden rectangles X by C (2ρ : edge)", 2 * I["rho"], GR["cap"], GR["os2"]["xHeight"], 0.5)
ratio(F, "datum", "cap height : x-height, by the dodecahedron", "the cube inscribed in the dodecahedron of edge X has edge C (face diagonal : edge)", Dd["second_distance"], GR["cap"], GR["os2"]["xHeight"], 0.5)
rel(F, "stroke", "stem", "X·φ^(−9/2)", stem, GR["stem"], 1.0)
rel(F, "stroke", "hairline", "stem ÷ φ: midradius of the icosahedron whose edge is two serifs", 2 * serif * I["rho"], GR["hair"], 1.0)
rel(F, "stroke", "serif (tip of I)", "hairline ÷ φ", serif, GR["serif"], 1.0)
rel(F, "stroke", "stem, by the dodecahedron", "midradius of the dodecahedron whose edge is two serifs", 2 * serif * Dd["rho"], GR["stem"], 1.0)
ratio(F, "stroke", "hairline : serif", "ρ of the icosahedron : half its edge = φ", I["rho"] / 0.5, GR["hair"], GR["serif"])
ratio(F, "stroke", "stem : hairline", "face diagonal : edge of the dodecahedron = φ", Dd["second_distance"], GR["stem"], GR["hair"])
ratio(F, "stroke", "stem : serif", "ρ of the dodecahedron : half its edge = φ²", Dd["rho"] / 0.5, GR["stem"], GR["serif"])
rel(F, "stroke", "bowl", "stem·φ^(1/4)", stem * PHI ** 0.25, GR["bowl"], 1.0)
for k_, v_ in GR["over_top"].items(): rel(F, "lining", f"overshoot above, {k_}", "C·φ^(−8)", round(C * PHI ** -8), v_, 0.5)
for k_, v_ in GR["over_bottom"].items(): rel(F, "lining", f"overshoot below, {k_}", "C·φ^(−8)", round(C * PHI ** -8), v_, 0.5)
rel(F, "lining", "apex of A above the cap line", "C·φ^(−9)", round(C * PHI ** -9), GR["apex"], 0.5)
for g_, v_ in GR["vertex"].items(): rel(F, "lining", f"vertex of {g_} below the baseline", "C·φ^(−15/2)", round(C * PHI ** -7.5), v_, 0.5)
rel(F, "lining", "small capital height", "X·φ^(1/8)", round(X * PHI ** 0.125), GR["sc"], 0.5)
for g_, v_ in GR["track"].items(): rel(F, "spacing", f"titling space added to {g_}", "X·φ^(−2)", round(X * PHI ** -2), v_, 1.0)
rel(F, "spacing", "word space", "X", X, GR["space"], 0.5)
rel(F, "stroke", "dot", "stem·φ^(3/4)", stem * PHI ** 0.75, GR["dot"], 1.0)
rel(F, "stroke", "broad end of the exclamation wedge", "stem·φ^(1/2)", stem * PHI ** 0.5, GR["wedge"], 1.0)
GW = {"W": 0.5, "M": 0.25, **{k: 0 for k in "AHKNUVXY"}, **{k: -0.25 for k in "DGOQR"}, **{k: -0.5 for k in "BCELTZ"}, "F": -0.75, "P": -0.75, "S": -1, "J": -1.5, "I": -2}
for g_ in sorted(GW, key=lambda q: (-GW[q], q)):
    rel(F, "width", f"ink width of {g_}", f"C·φ^({GW[g_]:+g})".replace("+0", "0"), C * PHI ** GW[g_], GR["widths"][g_], 1.0)
for g_, v_ in GR["stems"].items(): rel(F, "uniformity", f"stem of {g_}", "every upright stem is the stem", stem, v_, 1.0)
for g_, v_ in GR["hairlines"].items(): rel(F, "uniformity", f"hairline, {g_}", "every straight thin stroke is the hairline", hair, v_, 1.0)
for g_, v_ in GR["serifs"].items():
    rel(F, "uniformity", f"serif tips of {g_}: thinnest of {len(v_)}", "every serif tip is the serif", serif, min(v_), 1.0)
    rel(F, "uniformity", f"serif tips of {g_}: thickest of {len(v_)}", "every serif tip is the serif", serif, max(v_), 1.0)
for nm_, key_, tg_ in (("small capital stem (H)", "sc_stem", stem), ("small capital stem (E)", "sc_E_stem", stem), ("small capital hairline (H bar)", "sc_hair", hair),
                       ("small capital hairline (T bar)", "sc_T_bar", hair)):
    rel(F, "uniformity", nm_, "small capitals take the capitals' strokes", tg_, GR[key_], 1.0)
for nm_, v_ in (("H", GR["sc_serif"]), ("T", GR["sc_serif_T"])):
    rel(F, "uniformity", f"small capital serif tips of {nm_}: thinnest", "small capitals take the capitals' strokes", serif, min(v_), 1.0)
    rel(F, "uniformity", f"small capital serif tips of {nm_}: thickest", "small capitals take the capitals' strokes", serif, max(v_), 1.0)
FB = F + " Bold"
rel(FB, "stroke", "bold stem", "stem·φ", stem * PHI, GB["stem"], 1.0)
rel(FB, "stroke", "bold hairline", "hairline·φ^(1/2)", hair * PHI ** 0.5, GB["hair"], 1.0)
rel(FB, "stroke", "bold serif", "serif·φ^(1/4)", serif * PHI ** 0.25, GB["serif"], 1.0)
rel(FB, "stroke", "bold bowl", "bold stem·φ^(1/4)", stem * PHI ** 1.25, GB["bowl"], 1.0)
ratio(FB, "stroke", "bold stem : stem", "one whole step, φ", PHI, GB["stem"], GR["stem"])
rel(FB, "stroke", "bold dot", "bold stem·φ^(3/4)", stem * PHI ** 1.75, GB["dot"], 1.0)
for g_ in sorted(GW, key=lambda q: (-GW[q], q)):
    rel(FB, "width", f"ink width of {g_}", f"rung·φ^(1/8)", C * PHI ** GW[g_] * PHI ** 0.125, GB["widths"][g_], 1.0)
for g_, v_ in GB["stems"].items(): rel(FB, "uniformity", f"stem of {g_}", "every upright stem is the bold stem", stem * PHI, v_, 1.0)
for g_, v_ in GB["serifs"].items():
    rel(FB, "uniformity", f"serif tips of {g_}: thinnest of {len(v_)}", "every serif tip is the bold serif", serif * PHI ** 0.25, min(v_), 1.0)
    rel(FB, "uniformity", f"serif tips of {g_}: thickest of {len(v_)}", "every serif tip is the bold serif", serif * PHI ** 0.25, max(v_), 1.0)
for g_, v_ in GB["hairlines"].items(): rel(FB, "uniformity", f"hairline, {g_}", "every straight thin stroke is the bold hairline", hair * PHI ** 0.5, v_, 1.0)
for k_, v_ in GB["over_top"].items(): rel(FB, "lining", f"overshoot above, {k_}", "C·φ^(−8)", round(C * PHI ** -8), v_, 0.5)

# ---- Aureate Destiny Solar Serif: whole numbers and roots on the tetrahedron, the cube and the octahedron
F = "Aureate Destiny Solar Serif"
stem = C / 14; serif = stem / R6; hair = serif * R3; edge = 2 * stem
rel(F, "stroke", "stem", "C ÷ 14 (twice seven)", stem, SR["stem"], 1.0)
rel(F, "stroke", "serif", "inradius of the tetrahedron whose edge is two stems", edge * T["r"], SR["serif"], 1.0)
rel(F, "stroke", "hairline", "midradius of the same tetrahedron", edge * T["rho"], SR["hair"], 1.0)
ratio(F, "stroke", "hairline : serif", "ρ : r of the tetrahedron = R : r of the cube = R : r of the octahedron = √3", T["rho"] / T["r"], SR["hair"], SR["serif"])
rel(F, "stroke", "√3 three ways", "tetrahedron ρ : r against cube R : r", K["R"] / K["r"], T["rho"] / T["r"], 1e-9, "number")
rel(F, "stroke", "√3 three ways", "tetrahedron ρ : r against octahedron R : r", O["R"] / O["r"], T["rho"] / T["r"], 1e-9, "number")
ratio(F, "stroke", "stem : hairline", "ρ : r of the cube = R : ρ of the octahedron = √2", K["rho"] / K["r"], SR["stem"], SR["hair"])
rel(F, "stroke", "√2 two ways", "cube ρ : r against octahedron R : ρ", O["R"] / O["rho"], K["rho"] / K["r"], 1e-9, "number")
ratio(F, "stroke", "stem : serif", "half-edge : inradius of the tetrahedron = √6", 0.5 / T["r"], SR["stem"], SR["serif"])
ratio(F, "datum", "cap height : stem", "14 : 1", 14, SR["cap"], SR["stem"], 0.5)
rel(F, "stroke", "bowl", "stem·9/8, the tone", stem * 9 / 8, SR["bowl"], 1.0)
for k_, v_ in SR["over_top"].items(): rel(F, "lining", f"overshoot above, {k_}", "C ÷ 48", round(C / 48), v_, 0.5)
for k_, v_ in SR["over_bottom"].items(): rel(F, "lining", f"overshoot below, {k_}", "C ÷ 48", round(C / 48), v_, 0.5)
rel(F, "lining", "apex of A above the cap line", "C ÷ 72", round(C / 72), SR["apex"], 0.5)
for g_, v_ in SR["vertex"].items(): rel(F, "lining", f"vertex of {g_} below the baseline", "C ÷ 36", round(C / 36), v_, 0.5)
rel(F, "lining", "small capital height", "C·2/3, the fifth", round(C * 2 / 3), SR["sc"], 0.5)
for g_, v_ in SR["track"].items(): rel(F, "spacing", f"titling space added to {g_}", "C ÷ 4", round(C / 4), v_, 1.0)
rel(F, "spacing", "word space", "C ÷ 2, the octave over the titling space", round(C / 2), SR["space"], 0.5)
rel(F, "stroke", "dot", "stem·3/2, the fifth", stem * 1.5, SR["dot"], 1.0)
rel(F, "stroke", "broad end of the exclamation wedge", "stem·4/3, the fourth; dot : wedge = 9 : 8", stem * 4 / 3, SR["wedge"], 1.0)
SW = {"W": (16 / 12, "16/12 C"), "M": (14 / 12, "14/12 C"), **{k: (1.0, "12/12 C, the face of the cube of edge C") for k in "AHKNUVXY"},
      **{k: (R3 / 2, "√3/2 C, the circumradius of the cube of edge C") for k in "DGOQR"}, **{k: (10 / 12, "10/12 C") for k in "BCLTZ"}, "E": (9 / 12, "9/12 C"),
      "F": (1 / R2, "C ÷ √2, the edge of the cube whose face diagonal is C"), "P": (1 / R2, "C ÷ √2, the edge of the cube whose face diagonal is C"), "S": (7 / 12, "7/12 C"), "J": (6 / 12, "6/12 C")}
rel(F, "width", "√3/2 from the cube", "circumradius of the cube of edge 1", R3 / 2, K["R"], 1e-9, "number")
rel(F, "width", "1/√2 from the cube", "edge : face diagonal, r : ρ of the cube", 1 / R2, K["r"] / K["rho"], 1e-9, "number")
for g_ in sorted(SW, key=lambda q: (-SW[q][0], q)): rel(F, "width", f"ink width of {g_}", SW[g_][1], C * SW[g_][0], SR["widths"][g_], 1.0)
for g_, v_ in SR["stems"].items(): rel(F, "uniformity", f"stem of {g_}", "every upright stem is the stem", stem, v_, 1.0)
for g_, v_ in SR["hairlines"].items(): rel(F, "uniformity", f"hairline, {g_}", "every straight thin stroke is the hairline", hair, v_, 1.0)
for g_, v_ in SR["serifs"].items():
    rel(F, "uniformity", f"serif tips of {g_}: thinnest of {len(v_)}", "every serif tip is the serif", serif, min(v_), 1.0)
    rel(F, "uniformity", f"serif tips of {g_}: thickest of {len(v_)}", "every serif tip is the serif", serif, max(v_), 1.0)
for nm_, key_, tg_ in (("small capital stem (H)", "sc_stem", stem), ("small capital stem (E)", "sc_E_stem", stem), ("small capital hairline (H bar)", "sc_hair", hair),
                       ("small capital hairline (T bar)", "sc_T_bar", hair)):
    rel(F, "uniformity", nm_, "small capitals take the capitals' strokes", tg_, SR[key_], 1.0)
for nm_, v_ in (("H", SR["sc_serif"]), ("T", SR["sc_serif_T"])):
    rel(F, "uniformity", f"small capital serif tips of {nm_}: thinnest", "small capitals take the capitals' strokes", serif, min(v_), 1.0)
    rel(F, "uniformity", f"small capital serif tips of {nm_}: thickest", "small capitals take the capitals' strokes", serif, max(v_), 1.0)
FB = F + " Bold"; step = O["rho"] / O["r"]; bedge = edge * step
rel(FB, "stroke", "the bold step", "ρ : r of the octahedron = √(3/2)", math.sqrt(1.5), step, 1e-9, "number")
rel(FB, "stroke", "bold serif", "inradius of the tetrahedron enlarged by the octahedron's step", bedge * T["r"], SB["serif"], 1.0)
rel(FB, "stroke", "bold hairline", "midradius of the enlarged tetrahedron", bedge * T["rho"], SB["hair"], 1.0)
rel(FB, "stroke", "bold stem", "circumradius of the enlarged tetrahedron", bedge * T["R"], SB["stem"], 1.0)
ratio(FB, "stroke", "bold stem : stem", "two octahedral steps = 3 : 2, the fifth", 1.5, SB["stem"], SR["stem"])
ratio(FB, "stroke", "bold stem : bold hairline", "R : ρ of the tetrahedron = √3", T["R"] / T["rho"], SB["stem"], SB["hair"])
ratio(FB, "stroke", "bold stem : bold serif", "R : r of the tetrahedron = 3", T["R"] / T["r"], SB["stem"], SB["serif"])
rel(FB, "stroke", "bold bowl", "bold stem·9/8", stem * 1.5 * 9 / 8, SB["bowl"], 1.0)
rel(FB, "stroke", "bold dot", "bold stem·3/2", stem * 2.25, SB["dot"], 1.0)
for g_ in sorted(SW, key=lambda q: (-SW[q][0], q)): rel(FB, "width", f"ink width of {g_}", "rung·16/15", C * SW[g_][0] * 16 / 15, SB["widths"][g_], 1.0)
for g_, v_ in SB["stems"].items(): rel(FB, "uniformity", f"stem of {g_}", "every upright stem is the bold stem", stem * 1.5, v_, 1.0)
for g_, v_ in SB["serifs"].items():
    rel(FB, "uniformity", f"serif tips of {g_}: thinnest of {len(v_)}", "every serif tip is the bold serif", bedge * T["r"], min(v_), 1.0)
    rel(FB, "uniformity", f"serif tips of {g_}: thickest of {len(v_)}", "every serif tip is the bold serif", bedge * T["r"], max(v_), 1.0)
for g_, v_ in SB["hairlines"].items(): rel(FB, "uniformity", f"hairline, {g_}", "every straight thin stroke is the bold hairline", bedge * T["rho"], v_, 1.0)
for k_, v_ in SB["over_top"].items(): rel(FB, "lining", f"overshoot above, {k_}", "C ÷ 48", round(C / 48), v_, 0.5)

# ------------------------------------------------------------------ output
os.makedirs(os.path.join(D, "verification"), exist_ok=True)
fails = [r for r in rows if r["verdict"] != "pass"]
summary = {}
for r in rows: s_ = summary.setdefault(r["family"], [0, 0]); s_[0] += 1; s_[1] += r["verdict"] == "pass"
solids_out = {k: {q: s[q] for q in ("vertices", "edges", "faces", "r", "rho", "R")} | {"R_over_r": s["R"] / s["r"], "rho_over_r": s["rho"] / s["r"], "R_over_rho": s["R"] / s["rho"],
              "element": CORR[k][0], "kepler": CORR[k][1]} for k, s in SOL.items()}
json.dump({"version": "1.910", "solids": solids_out, "summary": {k: {"relations": v[0], "passed": v[1]} for k, v in summary.items()},
           "measured": {"AureateDestinySerif-Regular": GR, "AureateDestinySerif-Bold": GB, "AureateDestinySolarSerif-Regular": SR, "AureateDestinySolarSerif-Bold": SB},
           "relations": rows}, open(os.path.join(D, "verification", "certificate.json"), "w"), indent=1, default=str)
def fmt(v, kind): return "—" if v is None else (f"{v:.4f}" if kind in ("ratio", "number") else (f"{v:.0f}" if kind == "count" else f"{v:.2f}".rstrip("0").rstrip(".")))
with open(os.path.join(D, "verification", "CERTIFICATE.md"), "w") as fh:
    fh.write("# Aureate Destiny Serif 1.910: certificate\n\nEvery relation is measured in the finished fonts by `source/certificate_serif.py`. Lengths are in font units "
             "(2048 to the em). A stroke may differ from its target by one unit, because outlines sit on a whole-unit grid; a line or a height by half a unit; "
             "a ratio by what a three-quarter-unit reading error on each of its two lengths allows.\n\n")
    fh.write("| Family | Relations | Passed |\n| --- | --- | --- |\n" + "".join(f"| {k} | {v[0]} | {v[1]} |\n" for k, v in summary.items()) + "\n")
    fh.write("## The five solids, measured from their vertex coordinates (edge = 1)\n\n| Solid | V, E, F | r | ρ | R | ρ : r | R : ρ | R : r | Element | Kepler's place |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for k, s in solids_out.items():
        fh.write(f"| {k} | {s['vertices']}, {s['edges']}, {s['faces']} | {s['r']:.6f} | {s['rho']:.6f} | {s['R']:.6f} | {s['rho_over_r']:.6f} | {s['R_over_rho']:.6f} | {s['R_over_r']:.6f} | {s['element']} | {s['kepler']} |\n")
    for fam in summary:
        fh.write(f"\n## {fam}\n\n| Group | Measure | Relation | Target | Measured | Tolerance | Verdict |\n| --- | --- | --- | --- | --- | --- | --- |\n")
        for r in rows:
            if r["family"] == fam:
                tol = f"{r['tolerance']:.4f}" if r["kind"] == "ratio" else (f"{r['tolerance']:.0e}" if r["kind"] == "number" else fmt(r["tolerance"], "length"))
                fh.write(f"| {r['group']} | {r['name']} | {r['statement']} | {fmt(r['expected'], r['kind'])} | {fmt(r['measured'], r['kind'])} | ±{tol} | {r['verdict']} |\n")
print(json.dumps({k: f"{v[1]}/{v[0]}" for k, v in summary.items()}))
for r in fails: print("  FAIL", r["family"], "|", r["name"], "| target", fmt(r["expected"], r["kind"]), "measured", fmt(r["measured"], r["kind"]), "tol", r["tolerance"])
