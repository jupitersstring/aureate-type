#!/usr/bin/env python3
"""Aureate Destiny 1.900: a light, wide-set titling sans in two proportional lattices.

Source: Aureate Sans Geometric 1.701 Regular, for both weights. Both cases type capitals.

  Aureate Destiny        the golden lattice. Every measure is a power of φ; the orders are nested
                         roots: whole powers, half powers (the mean of a step), quarter powers
                         (the mean of the mean), eighth powers.
  Aureate Destiny Solar  the Apollonian lattice. Whole numbers on the Sun's six and the lyre canon
                         6 : 8 : 9 : 12 with Apollo's seven; the orders are ratios of ratios:
                         octave 2:1, fifth 3:2 and fourth 4:3, tone 9:8 (fifth ÷ fourth), then the
                         sevenths 8:7 and 7:6 and the semitone 16:15.

Steps, identical for both lattices, with the lattice supplying the numbers:
  D1  Capital and small-capital ink widths are set on the lattice's width rungs (fractions of the
      cap height); bearings are kept.
  D2  Lining: flats on 0 and C, rounds overshoot by the lattice's amount, figures take the capital
      lines, small capitals take the lattice's height.
  D3  One weight law: every stroke of the source becomes source × (stem target / source stem), with
      horizontal strokes further set to the lattice's bar : stem ratio. Flat edges on alignment
      lines are pinned and the inside takes the whole correction.
  D4  Dots, commas and accents are scaled to the lattice's dot : stem ratio; hyphens and dashes
      are thinned as bars.
  D5  Titling space and word space from the lattice. Lowercase code points map to capitals.
"""
import os, sys, json, math, time, unicodedata
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(time.mktime((2026, 11, 5, 12, 0, 0, 0, 0, 0)))))
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.otlLib.builder import buildStatTable
import build_titling as bt

PHI = bt.PHI
BASE = "/path/to/aureate"
SRC = os.path.join(BASE, "AureateCollection_1.701/fonts")
OUT = os.path.join(BASE, "AureateDestiny_1.900")
VERSION = "1.900"
X, C, SC0 = 898, 1453, 954

LATTICES = {
    "golden": dict(
        family="Aureate Destiny",
        rungs={"C": C, "C·φ^-1/4": C * PHI ** -0.25, "C·φ^-1/2": C * PHI ** -0.5, "C·φ^-3/4": C * PHI ** -0.75,
               "C·φ^-1 = X": C * PHI ** -1, "C·φ^-5/4": C * PHI ** -1.25, "C·φ^-3/2": C * PHI ** -1.5},
        stem=X * PHI ** -4.5, stem_rel="X·φ^-9/2", bold_stem_factor=PHI, bold_rel="stem·φ",
        bar_ratio=PHI ** -0.125, bar_rel="stem·φ^-1/8", overshoot=C * PHI ** -9, over_rel="C·φ^-9",
        track=X * PHI ** -2, track_rel="X·φ^-2", space=float(X), space_rel="X",
        dot_ratio=PHI ** 0.75, dot_rel="stem·φ^3/4", bold_width=PHI ** 0.125, boldw_rel="rung·φ^1/8",
        sc=float(SC0), sc_rel="X·φ^1/8"),
    "solar": dict(
        family="Aureate Destiny Solar",
        rungs={"12/12 C": C, "9/12 C": C * 9 / 12, "8/12 C": C * 8 / 12, "7/12 C": C * 7 / 12, "6/12 C": C * 6 / 12},
        stem=C / 14, stem_rel="C/14 (twice seven stems to the capital)", bold_stem_factor=1.5, bold_rel="stem·3/2",
        bar_ratio=8 / 9, bar_rel="stem·8/9", overshoot=C / 72, over_rel="C/72 (six twelves)",
        track=C / 4, track_rel="C/4", space=C / 2, space_rel="C/2 (twice the titling space)",
        dot_ratio=1.5, dot_rel="stem·3/2", bold_width=16 / 15, boldw_rel="rung·16/15",
        sc=C * 2 / 3, sc_rel="C·2/3",
        # letters that belong together share a rung (H N U; A V; B P R S), whichever rung is nearest to each alone
        classes={"W": "12/12 C", "C": "9/12 C", "G": "9/12 C", "O": "9/12 C", "M": "9/12 C",
                 "A": "8/12 C", "D": "8/12 C", "H": "8/12 C", "K": "8/12 C", "N": "8/12 C", "T": "8/12 C", "U": "8/12 C", "V": "8/12 C", "X": "8/12 C", "Y": "8/12 C",
                 "B": "7/12 C", "P": "7/12 C", "R": "7/12 C", "S": "7/12 C", "Z": "7/12 C",
                 "E": "6/12 C", "F": "6/12 C", "J": "6/12 C", "L": "6/12 C"}),
}
FIG = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
report = {"version": VERSION, "fonts": {}}

# ------------------------------------------------------------------ helpers
def ink(glyf, g):
    gl = glyf[g]; gl.recalcBounds(glyf)
    return (gl.xMin, gl.yMin, gl.xMax, gl.yMax) if gl.numberOfContours > 0 else None

def anchors_by_glyph(font):
    out = {}
    if "GPOS" not in font: return out
    for lk in font["GPOS"].table.LookupList.Lookup:
        for st in lk.SubTable:
            if lk.LookupType == 9: st = st.ExtSubTable
            if st.LookupType == 4:
                for g, br in zip(st.BaseCoverage.glyphs, st.BaseArray.BaseRecord):
                    out.setdefault(g, []).extend(a for a in br.BaseAnchor if a is not None)
            elif st.LookupType == 5:
                for g, la in zip(st.LigatureCoverage.glyphs, st.LigatureArray.LigatureAttach):
                    for cr in la.ComponentRecord: out.setdefault(g, []).extend(a for a in cr.LigatureAnchor if a is not None)
            elif st.LookupType == 6:
                for g, mr in zip(st.Mark2Coverage.glyphs, st.Mark2Array.Mark2Record):
                    out.setdefault(g, []).extend(a for a in mr.Mark2Anchor if a is not None)
    return out

def arm_thickness(font, glyph="E"):
    """Thickness of the top arm, on a vertical at 70 % of the glyph's width."""
    gl = font["glyf"][glyph]; gl.recalcBounds(font["glyf"]); S = bt.flatten(gl); xm = gl.xMin + 0.7 * (gl.xMax - gl.xMin) + 0.37
    x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
    m = ((x1 <= xm) & (x2 > xm)) | ((x2 <= xm) & (x1 > xm))
    ys = np.sort(y1[m] + (xm - x1[m]) * (y2[m] - y1[m]) / (x2[m] - x1[m]))
    return float(ys[-1] - ys[-2])

def scale_x_about_left(font, anchors, g, s):
    glyf = font["glyf"]; hm = font["hmtx"].metrics; gl = glyf[g]; b = ink(glyf, g); x0 = b[0]; w = b[2] - b[0]
    gl.coordinates = GlyphCoordinates([(round(x0 + (x - x0) * s), y) for x, y in gl.coordinates])
    adv, lsb = hm[g]; hm[g] = (adv + round(w * s) - w, lsb)
    for a in anchors.get(g, []): a.XCoordinate = round(x0 + (a.XCoordinate - x0) * s)

def fit_y(font, g, t_lo, t_hi):
    glyf = font["glyf"]; gl = glyf[g]; b = ink(glyf, g); lo, hi = b[1], b[3]
    if hi == lo or (lo, hi) == (t_lo, t_hi): return False
    a = (t_hi - t_lo) / (hi - lo); c = t_lo - a * lo
    gl.coordinates = GlyphCoordinates([(x, round(a * y + c)) for x, y in gl.coordinates]); return True

def scale_small_contours(gl, dot_f, bar_f, small_h):
    """Dots, commas and accents scale about their own centre (their foot if they stand on the baseline);
    short bars are thinned only."""
    out = []; n_ = 0
    for ci in range(gl.numberOfContours):
        pts = bt.contour_points(gl, ci); xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        if h >= small_h or w >= max(0.9 * X, 2.2 * small_h) or h == 0 or w == 0: out.append(pts); continue
        cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2
        if w > 2.2 * h:                                     # a bar: hyphen, dash, macron
            new = [[q[0], round(cy + (q[1] - cy) * bar_f), q[2]] for q in pts]
        else:
            ay = min(ys) if -60 <= min(ys) <= 20 else cy
            new = [[round(cx + (q[0] - cx) * dot_f), round(ay + (q[1] - ay) * dot_f), q[2]] for q in pts]
        out.append(new); n_ += 1
    if n_: gl.coordinates = GlyphCoordinates([(q[0], q[1]) for c in out for q in c])
    return n_

def nearest_rung(w, rungs):
    name = min(rungs, key=lambda k: abs(math.log(rungs[k] / w))); return name, rungs[name]

# ------------------------------------------------------------------ build
def build(lattice, style):
    L = LATTICES[lattice]; bold = style == "Bold"
    # both weights are drawn from the Geometric Regular: its own stem (166) is the golden Bold target (stem·φ = 167),
    # so the Bold needs almost no thinning and every glyph takes the law cleanly
    path = os.path.join(SRC, "AureateSansGeometric-Regular.ttf")
    font = TTFont(path); source = TTFont(path); regular = TTFont(os.path.join(SRC, "AureateSansGeometric-Regular.ttf"))
    glyf, sglyf, rglyf = font["glyf"], source["glyf"], regular["glyf"]; hm = font["hmtx"].metrics; cmap = font.getBestCmap()
    order = font.getGlyphOrder(); anchors = anchors_by_glyph(font)
    rec = {"lattice": lattice, "family": L["family"], "style": style}
    s_src = bt.stem_width(source); bar_src = arm_thickness(source); dot_src = ink(sglyf, "period")[2] - ink(sglyf, "period")[0]
    stem_t = L["stem"] * (L["bold_stem_factor"] if bold else 1.0)
    over = round(L["overshoot"]); sc_t = round(L["sc"]); track = round(L["track"]); half = track // 2
    rec["source"] = {"stem": s_src, "bar": bar_src, "dot": dot_src}
    rec["targets"] = {"stem": round(stem_t, 2), "bar": round(stem_t * L["bar_ratio"], 2), "overshoot": over, "small_cap": sc_t,
                      "track": track, "space": round(L["space"]), "dot": round(stem_t * L["dot_ratio"], 1)}

    caps = {g for cp, g in cmap.items() if unicodedata.category(chr(cp)) == "Lu"}
    smalls = {g for g in order if g.endswith(".s") and g[:-2] in caps}
    figs = {g for g in order if g.split(".")[0] in FIG and not any(t in g for t in (".o", ".s", ".u", ".n", ".d", "superior", "inferior")) }

    # ---- D2 lining (vertical only; done first so the weight pass sees the final lines)
    lined = 0
    for g in sorted(caps | figs | smalls):
        if glyf[g].isComposite() or glyf[g].numberOfContours <= 0: continue
        b = ink(glyf, g)
        if g in smalls:
            f = sc_t / SC0
            if abs(f - 1) > 1e-6:
                glyf[g].coordinates = GlyphCoordinates([(x, round(y * f)) for x, y in glyf[g].coordinates]); b = ink(glyf, g)
            top, o_ = sc_t, max(1, round(over * sc_t / C))
        elif g in figs:
            flat_top = min(ink(sglyf, q)[3] for q in ("one", "four", "seven"))
            t_hi = C + over if b[3] > flat_top + 8 else C
            t_lo = -over if b[1] < -8 else 0
            lined += fit_y(font, g, t_lo, t_hi); continue
        else:
            top, o_ = C, over
        if b[3] > top + 3 * o_ + 20: continue                           # accented: leave
        t_hi = top + o_ if b[3] > top + 6 else b[3]
        t_lo = -o_ if b[1] < -6 else b[1]
        lined += fit_y(font, g, t_lo, t_hi)
    rec["glyphs_lined"] = lined

    # ---- D3 one weight law (monoline: the same law on every stroke side)
    r = stem_t / s_src; c_h = L["bar_ratio"] / (bar_src / s_src)
    def s_of(n): return s_src + (bar_src - s_src) * n[1] * n[1]                 # source stroke by orientation
    def const_full(n): return s_of(n) * (1 - r * (1 + (c_h - 1) * n[1] * n[1]))
    def target_fn(p, n): return p * r * (1 + (c_h - 1) * n[1] * n[1])
    lines = [0, X, sc_t, C]
    small_h = max(0.4 * X, 1.8 * s_src)
    kw = dict(lines=lines, glyph_box=True, term_len=1.3, dmax=(0.3, 0.55), sample="min", smooth=6, small_h=small_h, miter=3.2)
    def weigh(g, record=None):
        gl = glyf[g]
        before = (GlyphCoordinates(list(gl.coordinates)), bt.crossings_count(gl), bt.turning_angles(gl))
        m_ = bt.reweight_glyph(gl, sglyf[g], s_src, 0.0, r, const_full=const_full, **kw)
        if m_ and (bt.crossings_count(gl) > before[1] or bt.shape_changed(before[2], gl, 120.0)):
            uniform = GlyphCoordinates(list(gl.coordinates)); extra = bt.crossings_count(gl) - before[1]
            gl.coordinates = GlyphCoordinates(list(before[0]))
            if record is not None: record[0].append(g)
            m_ = bt.reweight_glyph(gl, sglyf[g], s_src, 0.0, r, target_fn=target_fn, **kw)
            if m_ and (bt.crossings_count(gl) > before[1] or bt.shape_changed(before[2], gl, 120.0)):
                if 0 < extra <= 4:                       # a small overlap where a tail or cedilla joins: fills solid, keep it
                    gl.coordinates = uniform
                    if record is not None: record[2].append(g)
                else:
                    gl.coordinates = GlyphCoordinates(list(before[0])); m_ = 0
                    if record is not None: record[1].append(g)
        return m_

    # ---- D1 widths on the rungs: a dry run measures how much each letter narrows when its strokes thin,
    #      so that the finished ink width, not the source's, lands on the rung
    snapped = {}
    rev = {}
    for cp, gg in cmap.items(): rev.setdefault(gg, cp)
    base_letter = {}                                     # glyph -> its plain Latin capital, through Unicode decomposition
    for gg, cp in rev.items():
        b0 = unicodedata.normalize("NFD", chr(cp))[0]
        if "A" <= b0 <= "Z": base_letter[gg] = b0
    for g in sorted(caps | smalls):
        if glyf[g].isComposite() or glyf[g].numberOfContours <= 0 or g not in rglyf: continue
        rb = ink(rglyf, g); b = ink(glyf, g)
        if rb is None or b is None: continue
        ref = C if g in caps else SC0
        w_r = rb[2] - rb[0]
        if w_r < 0.33 * ref: continue                                   # I and the like: a stem, not a width
        base = g[:-2] if g in smalls else g
        rungs = {k: v * (C if g in caps else sc_t) / C for k, v in L["rungs"].items()}
        if base == "Q":                                                 # Q is O with a tail: it takes O's rung factor
            ob = ink(rglyf, "O" if g in caps else "O.s"); name, t_ = nearest_rung((ob[2] - ob[0]) * (1 if g in caps else sc_t / SC0), rungs)
            target = w_r * t_ / (ob[2] - ob[0]); name += " (as O)"
        else:
            name, target = nearest_rung(w_r * (1 if g in caps else sc_t / SC0), rungs)
            letter = base_letter.get(base)
            if letter and letter in L.get("classes", {}): name = L["classes"][letter]; target = rungs[name]
        if bold: target *= L["bold_width"]
        keep = GlyphCoordinates(list(glyf[g].coordinates)); w0 = b[2] - b[0]
        weigh(g); w1 = ink(glyf, g)[2] - ink(glyf, g)[0]; glyf[g].coordinates = keep      # dry run, then restore
        s = (target + (w0 - w1)) / w0
        if abs(math.log(s)) > 0.18: continue
        scale_x_about_left(font, anchors, g, s); snapped[g] = (name, round(target), round(s, 4))
    rec["widths_set"] = len(snapped)
    rec["width_rungs"] = {g: snapped[g][0] for g in "ABCDEFGHJKLMNOPQRSTUVWXYZ" if g in snapped}

    moved = 0; retry = []; failed = []; overlap = []
    for g in order:
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0 or g == ".notdef" or hm[g][0] == 0: continue
        moved += weigh(g, (retry, failed, overlap))
    reach = set(cmap.values()) | smalls
    rec["points_reweighted"] = moved; rec["second_attempt"] = len(retry); rec["left_at_source_weight"] = len(failed); rec["kept_with_small_overlap"] = len(overlap)
    rec["failed_reachable"] = [g for g in failed if g in reach and not (g in cmap.values() and all(chr(cp).islower() for cp, gg in cmap.items() if gg == g))]

    # ---- D4 dots and short bars
    dot_f = stem_t * L["dot_ratio"] / dot_src; bar_f = stem_t * L["bar_ratio"] / bar_src
    small = 0
    for g in order:
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0 or g == ".notdef": continue
        small += scale_small_contours(gl, dot_f, bar_f, small_h)
    rec["small_contours_scaled"] = small

    # ---- D5 spacing and encoding
    bt.track(font, track, half)
    for sp in ("space", cmap.get(0xA0)):
        if sp in hm: hm[sp] = (round(L["space"]), hm[sp][1])
    remap = 0
    for sub in font["cmap"].tables:
        if not sub.isUnicode(): continue
        for cp in list(sub.cmap):
            ch = chr(cp)
            if ch.islower() and len(ch.upper()) == 1 and ord(ch.upper()) in sub.cmap:
                sub.cmap[cp] = sub.cmap[ord(ch.upper())]; remap += 1
    rec["lowercase_mapped_to_capitals"] = remap

    # ---- names, tables, save
    fam = L["family"]; ps = fam.replace(" ", "") + "-" + style
    name = font["name"]; name.names = [n for n in name.names if n.nameID not in (21, 22, 25)]   # keep the feature-name records (stylistic sets)
    desc = ("A light titling sans derived from Aureate Sans Geometric (from Source Sans 3) under SIL OFL 1.1. "
            + ("Golden lattice: stem X*phi^-9/2, widths on C*phi^-n/4, bars stem*phi^-1/8, overshoot C*phi^-9, space X*phi^-2."
               if lattice == "golden" else
               "Apollonian solar lattice: cap = 14 stems, widths 6:7:8:9:12 twelfths of the cap, stem:bar 9:8, overshoot C/72, space C/4."))
    for nid, val in {1: fam, 2: style, 3: f"{VERSION};AURT;{ps}", 4: fam if style == "Regular" else f"{fam} {style}", 5: f"Version {VERSION}",
                     6: ps, 16: fam, 17: style, 9: "Aureate deterministic type system", 10: desc}.items():
        name.setName(val, nid, 3, 1, 0x409)
    font["head"].fontRevision = float(VERSION)
    os2 = font["OS/2"]
    if bold: os2.usWeightClass = 700; os2.fsSelection = (os2.fsSelection | 0x20) & ~0x40; font["head"].macStyle |= 1
    else: os2.usWeightClass = 400; os2.fsSelection = (os2.fsSelection | 0x40) & ~0x20; font["head"].macStyle &= ~1
    for g in order:
        gl = glyf[g]
        if gl.numberOfContours != 0:
            gl.recalcBounds(glyf)
            if hasattr(gl, "xMin"): hm[g] = (hm[g][0], gl.xMin)
    wght = font["OS/2"].usWeightClass
    if "STAT" in font: del font["STAT"]
    buildStatTable(font, [
        {"tag": "wght", "name": "Weight", "values": [{"value": wght, "name": "Bold" if wght >= 600 else "Regular", "flags": 0x2 if wght < 600 else 0}]},
        {"tag": "ital", "name": "Italic", "values": [{"value": 0, "name": "Roman", "flags": 0x2}]}], elidedFallbackName="Regular")
    name.names = [n for n in name.names if n.platformID != 1]
    if "kern" in font:
        enc = set(font.getBestCmap().values())
        for sub in font["kern"].kernTables:
            if hasattr(sub, "kernTable"):
                for pair in [q for q in sub.kernTable if q[0] not in enc or q[1] not in enc]: del sub.kernTable[pair]
    font["OS/2"].recalcAvgCharWidth(font)
    out = os.path.join(OUT, "fonts", ps + ".ttf"); font.save(out)
    w = TTFont(out); w.flavor = "woff2"; w.save(out[:-4] + ".woff2")

    # ---- measured
    f2 = TTFont(out); g2 = f2["glyf"]; h2 = f2["hmtx"].metrics
    def iw(n): b = ink(g2, n); return b[2] - b[0]
    rec["measured"] = {"stem_I": bt.stem_width(f2), "bar_E": round(arm_thickness(f2), 1), "bar_H": round(bt.bar_thickness(f2), 1),
                       "O": [ink(g2, "O")[1], ink(g2, "O")[3]], "S": [ink(g2, "S")[1], ink(g2, "S")[3]], "zero": [ink(g2, "zero")[1], ink(g2, "zero")[3]], "seven_top": ink(g2, "seven")[3],
                       "widths": {n: iw(n) for n in ("W", "O", "C", "G", "A", "M", "V", "H", "N", "D", "T", "B", "R", "S", "P", "E", "F", "L")},
                       "dot": iw("period"), "space": h2["space"][0], "adv_H": h2["H"][0], "lsb_H": ink(g2, "H")[0], "H_sc_top": ink(g2, "H.s")[3] if "H.s" in g2 else None}
    report["fonts"][ps] = rec
    print(ps, json.dumps({k: rec[k] for k in ("targets", "widths_set", "width_rungs", "glyphs_lined", "points_reweighted", "second_attempt", "left_at_source_weight", "kept_with_small_overlap", "small_contours_scaled", "measured")}))
    print("   failed reachable:", rec["failed_reachable"][:60])

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True); os.makedirs(os.path.join(OUT, "verification"), exist_ok=True)
    todo = [(l, s) for l in ("golden", "solar") for s in ("Regular", "Bold")]
    if len(sys.argv) > 1: todo = [t for t in todo if any(a in f"{t[0]}-{t[1]}" for a in sys.argv[1:])]
    for l, s in todo: build(l, s)
    p = os.path.join(OUT, "verification", "destiny_report.json")
    old = json.load(open(p)) if os.path.exists(p) else {"version": VERSION, "fonts": {}}
    old["fonts"].update(report["fonts"]); json.dump(old, open(p, "w"), indent=1, default=str)
