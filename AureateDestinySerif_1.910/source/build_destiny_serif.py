#!/usr/bin/env python3
"""Aureate Destiny Serif 1.910: light, wide-set titling capitals with serifs, in two lattices.

Source: Aureate Roman Living Tall 1.701 Regular, for both weights. Both cases type capitals.

  Aureate Destiny Serif        golden (the double square, root five): stem : hairline : serif = φ² : φ : 1,
                               capital widths on C·φ^(n/4), n from +2 (W) to −8 (I).
  Aureate Destiny Solar Serif  Apollonian solar (the square and the vesica): serif : hairline : stem
                               = 1 : √3 : √6 with the capital 14 stems tall; capital widths in twelfths
                               of the cap height: 6, 7, 6√2, 9, 10, 6√3, 12, 14, 16.

Every relation is declared in LATTICES with its order, parent and tolerance; certificate_serif.py
measures each one in the finished fonts.
"""
import os, sys, json, math, time, copy, array, unicodedata
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(time.mktime((2026, 11, 6, 12, 0, 0, 0, 0, 0)))))
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.otlLib.builder import buildStatTable
import build_titling as bt
import build_destiny as bd

PHI = bt.PHI; R2, R3, R6 = math.sqrt(2), math.sqrt(3), math.sqrt(6)
BASE = "/path/to/aureate"
SRC = os.path.join(BASE, "AureateCollection_1.701/fonts/AureateRomanLivingTall-Regular.ttf")
OUT = os.path.join(BASE, "AureateDestinySerif_1.910")
VERSION = "1.910"
ONLY = set(os.environ.get("DS_ONLY", "").split())            # quick trial on a few glyphs: DS_ONLY="A Q Ccedilla" DS_OUT=/tmp/x
if os.environ.get("DS_OUT"): OUT = os.environ["DS_OUT"]
X, C, SC0 = 898, 1453, 954
SRC_SERIF, SRC_HAIR, SRC_STEM, SRC_ROUND = 42.0, 72.0, 192.0, 220.9      # measured on the Roman
FIG = bd.FIG
SC_SERIF, SC_HAIR, SC_STEM = 37.0, 64.0, 161.0                           # the Roman's small capitals, measured on H.aursc

def unify_tips(gl, want, lo, hi):
    """The Roman's serif tips are 42 units on H, I and E, 57 on most letters and up to 71 on T. Give every
    tip one height, so one law gives every serif one thickness. A tip is a short upright edge between the
    flat of a foot or head and the slope of its bracket."""
    co = list(gl.coordinates); fl = gl.flags; st = 0; n_ = 0
    for e in gl.endPtsOfContours:
        idx = list(range(st, e + 1)); st = e + 1; m = len(idx)
        for k in range(m):
            i, j = idx[k], idx[(k + 1) % m]; h_, l_ = idx[(k - 1) % m], idx[(k + 2) % m]
            if not (fl[i] & 1 and fl[j] & 1): continue
            (x1, y1), (x2, y2) = co[i], co[j]
            if x1 != x2 or not (lo <= abs(y2 - y1) <= hi) or abs(abs(y2 - y1) - want) < 1: continue
            for outer, inner, q_o, q_i in ((i, j, h_, l_), (j, i, l_, h_)):
                xo, yo = co[outer]; xq, yq = co[q_o]; xi, yi = co[inner]; xr, yr = co[q_i]
                if not (fl[q_o] & 1) or yq != yo or abs(xq - xo) < 30: continue          # the flat of the foot or head
                if (xr - xi) * (xq - xo) <= 0: continue                                 # the bracket runs the same way as the flat
                if abs(yr - yi) < 4 and (fl[q_i] & 1): continue                         # the end of a plain bar, not a serif
                co[inner] = (xi, yo + (want if yi > yo else -want)); n_ += 1; break
    gl.coordinates = GlyphCoordinates(co); return n_

def golden():
    stem = X * PHI ** -4.5; hair = stem / PHI; serif = hair / PHI
    return dict(
        family="Aureate Destiny Serif", key="golden",
        stem=stem, hair=hair, serif=serif, round=stem * PHI ** 0.25,
        bold=dict(stem=stem * PHI, hair=hair * PHI ** 0.5, serif=serif * PHI ** 0.25, round=stem * PHI * PHI ** 0.25, width=PHI ** 0.125),
        over=C * PHI ** -8, point_top=C * PHI ** -9, point_bottom=C * PHI ** -7.5, sc=float(SC0),
        track=X * PHI ** -2, space=float(X), dot_ratio=PHI ** 0.75, wedge_ratio=PHI ** 0.25,
        rungs={"C·φ^1/2": C * PHI ** 0.5, "C·φ^1/4": C * PHI ** 0.25, "C": float(C), "C·φ^-1/4": C * PHI ** -0.25, "C·φ^-1/2": C * PHI ** -0.5,
               "C·φ^-3/4": C * PHI ** -0.75, "C·φ^-1 = X": C / PHI, "C·φ^-3/2": C * PHI ** -1.5, "C·φ^-2": C * PHI ** -2},
        classes={"W": "C·φ^1/2", "M": "C·φ^1/4", **{k: "C" for k in "AHKNUVXY"}, **{k: "C·φ^-1/4" for k in "DGOQR"},
                 **{k: "C·φ^-1/2" for k in "BCELTZ"}, "F": "C·φ^-3/4", "P": "C·φ^-3/4", "S": "C·φ^-1 = X", "J": "C·φ^-3/2", "I": "C·φ^-2"})

def solar():
    stem = C / 14; serif = stem / R6; hair = serif * R3
    return dict(
        family="Aureate Destiny Solar Serif", key="solar",
        stem=stem, hair=hair, serif=serif, round=stem * 9 / 8,
        bold=dict(stem=stem * 1.5, hair=hair * math.sqrt(1.5), serif=serif * math.sqrt(1.5), round=stem * 1.5 * 9 / 8, width=16 / 15),
        over=C / 48, point_top=C / 72, point_bottom=C / 36, sc=C * 2 / 3,
        track=C / 4, space=C / 2, dot_ratio=1.5, wedge_ratio=9 / 8,
        rungs={"16/12 C": C * 16 / 12, "14/12 C": C * 14 / 12, "12/12 C": float(C), "6√3/12 C": C * R3 / 2, "10/12 C": C * 10 / 12, "9/12 C": C * 9 / 12,
               "6√2/12 C": C / R2, "7/12 C": C * 7 / 12, "6/12 C": C / 2, "14 stems·... ": 0.0},
        classes={"W": "16/12 C", "M": "14/12 C", **{k: "12/12 C" for k in "AHKNUVXY"}, **{k: "6√3/12 C" for k in "DGOQR"},
                 **{k: "10/12 C" for k in "BCLTZ"}, "E": "9/12 C", "F": "6√2/12 C", "P": "6√2/12 C", "S": "7/12 C", "J": "6/12 C"})

LATTICES = {"golden": golden(), "solar": solar()}
LATTICES["solar"]["rungs"].pop("14 stems·... ")
report = {"version": VERSION, "fonts": {}}

def law(knots):
    """Monotone piecewise-linear map of stroke thickness: source thickness -> target thickness."""
    xs = [0.0] + [k[0] for k in knots]; ys = [0.0] + [k[1] for k in knots]
    def f(p, n=None):
        for i in range(1, len(xs)):
            if p <= xs[i]: return ys[i - 1] + (p - xs[i - 1]) * (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1])
        return ys[-1] + (p - xs[-1]) * (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
    return f

def serif_thickness(font, glyph="I"):
    """Thickness of the foot serif near its tip, on a vertical 12 units inside the glyph's left edge."""
    gl = font["glyf"][glyph]; gl.recalcBounds(font["glyf"]); S = bt.flatten(gl); xm = gl.xMin + 12.37
    x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
    m = ((x1 <= xm) & (x2 > xm)) | ((x2 <= xm) & (x1 > xm))
    ys = np.sort(y1[m] + (xm - x1[m]) * (y2[m] - y1[m]) / (x2[m] - x1[m]))
    return float(ys[1] - ys[0])

def bowl_thickest(font, glyph="O"):
    import measure_strokes as ms
    mid, inw, th, ln = ms.glyph_thickness(font["glyf"][glyph]); v = th[np.isfinite(th) & (th < 400)]
    return float(np.percentile(v, 97))

CAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "serif_regulation.json")
def build(lattice, style, cal=None):
    if cal is None:
        cal = (json.load(open(CAL_FILE)) if os.path.exists(CAL_FILE) else {}).get(f"{lattice}-{style}", {})
    L = LATTICES[lattice]; bold = style == "Bold"; T = L["bold"] if bold else L
    font = TTFont(SRC); source = TTFont(SRC); glyf, sglyf = font["glyf"], source["glyf"]; hm = font["hmtx"].metrics; cmap = font.getBestCmap()
    order = font.getGlyphOrder(); anchors = bd.anchors_by_glyph(font)
    rec = {"lattice": lattice, "family": L["family"], "style": style}
    over, sc_t, track = round(L["over"]), round(L["sc"]), round(L["track"]); half = track // 2
    p_top, p_bot = round(L["point_top"]), round(L["point_bottom"])
    K = {k: T[k] + cal.get(k, 0.0) for k in ("serif", "hair", "stem", "round")}          # regulated knots
    def make_target(src_stem, src_serif=SRC_SERIF, src_hair=SRC_HAIR):
        f = law([(src_serif, K["serif"]), (src_hair, K["hair"]), (src_stem, K["stem"]), (src_stem * SRC_ROUND / SRC_STEM, K["round"])])
        r_ = src_stem / SRC_STEM                              # straight strokes take three levels only: serif, hairline, stem
        fs = law([(src_serif, K["serif"]), (src_hair, K["hair"]), (max(src_hair + 1, 130 * r_), K["hair"]), (max(src_hair + 2, 165 * r_), K["stem"]), (4000.0, K["stem"])])
        def t(p, n=None, straight=False):
            return fs(p) if straight else f(p)                  # only a curve is modulated, and only a curve may swell past the stem
        t.edge_aware = True
        return t
    target = make_target(SRC_STEM); FIG_STEM = {"one": make_target(128.0), "four": make_target(172.0)}
    sc_target = make_target(SC_STEM, SC_SERIF, SC_HAIR)       # small capitals take the capitals' stem, hairline and serif
    def target_for(g):
        if g in smalls: return sc_target
        b_ = g.split(".")[0]
        return FIG_STEM[b_] if b_ in FIG_STEM and not any(q in g for q in ("sups", "subs", "numr", "dnom")) else target
    rec["regulation"] = {k: round(v, 2) for k, v in cal.items()}
    rec["targets"] = {"stem": round(T["stem"], 2), "hairline": round(T["hair"], 2), "serif": round(T["serif"], 2), "bowl": round(T["round"], 2),
                      "overshoot": over, "point_top": p_top, "point_bottom": p_bot, "small_cap": sc_t, "track": track, "space": round(L["space"]),
                      "dot": round(T["stem"] * L["dot_ratio"], 1), "wedge": round(T["stem"] * L["dot_ratio"] / L["wedge_ratio"], 1)}
    caps = {g for cp, g in cmap.items() if unicodedata.category(chr(cp)) == "Lu"}
    smalls = {g for g in order if g.endswith(".aursc") and g[:-6] in caps}
    figs = {g for g in order if g.split(".")[0] in FIG and (g in FIG or "aurlnum" in g)}
    rev = {}
    for cp, gg in cmap.items(): rev.setdefault(gg, cp)
    base_letter = {}
    for gg, cp in rev.items():
        b0 = unicodedata.normalize("NFD", chr(cp))[0]
        if "A" <= b0 <= "Z": base_letter[gg] = b0

    # ---- the T family: the Roman's crossbar is 30 units, under half a hairline; give it the hairline before anything is measured
    def top_runs(gs_, g, frac):
        gl_ = gs_[g]; gl_.recalcBounds(gs_); S_ = bt.flatten(gl_); xq = gl_.xMin + frac * (gl_.xMax - gl_.xMin) + 0.37
        x1, y1, x2, y2 = S_[:, 0], S_[:, 1], S_[:, 2], S_[:, 3]
        m_ = ((x1 <= xq) & (x2 > xq)) | ((x2 <= xq) & (x1 > xq)); v_ = np.sort(y1[m_] + (xq - x1[m_]) * (y2[m_] - y1[m_]) / (x2[m_] - x1[m_]))
        return (float(v_[-2]), float(v_[-1])) if len(v_) >= 2 else (0.0, 0.0)
    sc_hair = (lambda r_: r_[1] - r_[0])(top_runs(sglyf, "E.aursc", 0.6)); bars = 0; t_family = []
    for g in sorted(caps | smalls):
        if sglyf[g].numberOfContours <= 0: continue
        top = SC0 if g in smalls else C; want = sc_hair if g in smalls else SRC_HAIR
        a_, b_ = top_runs(sglyf, g, 0.22), top_runs(sglyf, g, 0.78)
        if not all(abs(r_[1] - top) <= 1 and 24 <= r_[1] - r_[0] <= 34 for r_ in (a_, b_)): continue
        for gs_, w_ in ((glyf, T["hair"]), (sglyf, want + 8)):    # the drawing takes the target outright; the reference reads as a hairline
            gs_[g].coordinates = GlyphCoordinates([(x, top - round(w_)) if top - 37 <= y <= top - 22 else (x, y) for x, y in gs_[g].coordinates])
        bars += 1; t_family.append(g)
    rec["crossbars_given_the_hairline"] = bars
    tips = 0
    for g in sorted(caps | smalls | figs):
        if sglyf[g].numberOfContours <= 0: continue
        want, lo_, hi_ = (SC_SERIF, 30, 75) if g in smalls else (SRC_SERIF, 36, 95)
        n_ = unify_tips(sglyf[g], want, lo_, hi_); unify_tips(glyf[g], want, lo_, hi_); tips += n_
    rec["serif_tips_unified"] = tips

    # ---- lining
    lined = 0
    for g in sorted(caps | figs | smalls):
        if glyf[g].isComposite() or glyf[g].numberOfContours <= 0: continue
        if g in smalls and abs(sc_t / SC0 - 1) > 1e-6:
            glyf[g].coordinates = GlyphCoordinates([(x, round(y * sc_t / SC0)) for x, y in glyf[g].coordinates])
        b = bd.ink(glyf, g); top = sc_t if g in smalls else C; k_ = top / C
        if b[3] > top + 60: continue                                    # accented: leave
        d_top = b[3] - top
        t_hi = top + round(over * k_) if d_top >= 25 * k_ else (top + round(p_top * k_) if d_top >= 9 * k_ else top if abs(d_top) <= 3 else b[3])
        if b[1] < -60 * k_:                                             # a tail, cedilla or ogonek: line the body, carry the rest
            small_ = g in smalls; letter = base_letter.get(g[:-6] if small_ else g); ref = "O" if letter == "Q" else letter
            ref = (ref + ".aursc") if (ref and small_) else ref; y_ob = 0
            if ref and ref in sglyf and sglyf[ref].numberOfContours > 0:
                rb = bd.ink(sglyf, ref)
                if rb[1] >= -60: y_ob = round(rb[1] * (sc_t / SC0 if small_ else 1))
            t_ob = -round(p_bot * k_) if y_ob <= -36 * k_ else (-round(over * k_) if y_ob <= -20 * k_ else y_ob)
            a_ = (t_hi - t_ob) / (b[3] - y_ob)
            glyf[g].coordinates = GlyphCoordinates([(x, round(t_ob + (y - y_ob) * a_) if y >= y_ob else y + (t_ob - y_ob)) for x, y in glyf[g].coordinates])
            lined += 1; continue
        t_lo = -round(p_bot * k_) if b[1] <= -36 * k_ else (-round(over * k_) if b[1] <= -20 * k_ else b[1])
        lined += bd.fit_y(font, g, t_lo, t_hi)
    rec["glyphs_lined"] = lined

    # ---- one weight law, measured against the Roman
    lines = [0, X, sc_t, C]
    kw = dict(lines=lines, glyph_box=True, term_len=0.7, dmax=(0.3, 0.55), sample="mixed", smooth=6, miter=3.2)
    def weigh_part(gl, sgl, target, record, g):
        before = (GlyphCoordinates(list(gl.coordinates)), bt.crossings_count(gl), bt.turning_angles(gl))
        m_ = bt.reweight_glyph(gl, sgl, SRC_STEM, 0.0, 1.0, target_fn=target, **kw)
        if m_:                                              # a second pass removes what the first left (bowls especially)
            once = GlyphCoordinates(list(gl.coordinates)); c1 = bt.crossings_count(gl)
            bt.reweight_glyph(gl, sgl, SRC_STEM, 0.0, 1.0, target_fn=target, **kw)
            if bt.crossings_count(gl) > c1: gl.coordinates = once
        bad = bt.crossings_count(gl) - before[1]
        if m_ and (bad > 0 or bt.shape_changed(before[2], gl, 120.0)):
            first = GlyphCoordinates(list(gl.coordinates))
            gl.coordinates = GlyphCoordinates(list(before[0]))
            if record is not None: record[0].append(g)
            m_ = bt.reweight_glyph(gl, sgl, SRC_STEM, 0.0, 1.0, target_fn=target, **{**kw, "smooth": 2, "miter": 1.7})
            bad2 = bt.crossings_count(gl) - before[1]
            if m_ and (bad2 > 0 or bt.shape_changed(before[2], gl, 120.0)):
                if 0 < bad <= 4 and not bt.shape_changed(before[2], gl, 120.0):
                    gl.coordinates = first
                    if record is not None: record[2].append(g)
                else:                                   # third attempt: the thinnest reading everywhere, one pass
                    gl.coordinates = GlyphCoordinates(list(before[0]))
                    m_ = bt.reweight_glyph(gl, sgl, SRC_STEM, 0.0, 1.0, target_fn=target, **{**kw, "sample": "min", "smooth": 2, "miter": 1.7})
                    bad3 = bt.crossings_count(gl) - before[1]
                    if os.environ.get("DS_DEBUG"): print("   third", g, "crossings", bad, bad2, bad3, "shape", bt.shape_changed(before[2], gl, 120.0))
                    if m_ and (bad3 > 0 or bt.shape_changed(before[2], gl, 120.0)):
                        gl.coordinates = GlyphCoordinates(list(before[0])); m_ = 0
                        if record is not None: record[1].append(g)
        return m_

    def part(gl, idxs):
        """A copy of the glyph holding only the listed contours, and where their points sit in the whole."""
        ends = list(gl.endPtsOfContours); starts = [0] + [e + 1 for e in ends[:-1]]
        where = [i for ci in idxs for i in range(starts[ci], ends[ci] + 1)]
        q = copy.deepcopy(gl); q.coordinates = GlyphCoordinates([gl.coordinates[i] for i in where])
        q.flags = array.array("B", [gl.flags[i] for i in where]); e_ = []; n_ = 0
        for ci in idxs: n_ += ends[ci] - starts[ci] + 1; e_.append(n_ - 1)
        q.endPtsOfContours = e_; q.numberOfContours = len(idxs)
        return q, where

    def weigh(g, record=None):
        """A cedilla, ogonek or other mark hanging below the baseline is weighed on its own, so the letter and
        the mark do not confuse each other's stroke measurements."""
        gl = glyf[g]; sgl = sglyf[g]; target = target_for(g)
        ends = list(gl.endPtsOfContours); starts = [0] + [e + 1 for e in ends[:-1]]; marks = []
        if len(ends) > 1:
            for ci, (a_, b_) in enumerate(zip(starts, ends)):
                ys_ = [gl.coordinates[i][1] for i in range(a_, b_ + 1)]
                if max(ys_) <= 40 and min(ys_) < -60: marks.append(ci)
        if not marks or len(marks) == len(ends): return weigh_part(gl, sgl, target, record, g)
        body = [ci for ci in range(len(ends)) if ci not in marks]; total = 0; co = list(gl.coordinates)
        for idxs, rec_ in ((body, record), (marks, None if record is None else (record[0], record[3], record[2]))):
            q, where = part(gl, idxs); sq, _ = part(sgl, idxs)
            total += weigh_part(q, sq, target, rec_, g)
            for i, xy in zip(where, q.coordinates): co[i] = xy
        gl.coordinates = GlyphCoordinates(co)
        return total

    # ---- widths on the rungs (a dry run measures the narrowing, so the finished width lands on the rung)
    snapped = {}; exact = {}
    for g in sorted(caps | smalls):
        if glyf[g].isComposite() or glyf[g].numberOfContours <= 0 or (ONLY and g not in ONLY): continue
        b = bd.ink(glyf, g); sb = bd.ink(sglyf, g)
        if b is None or sb is None: continue
        w_r = sb[2] - sb[0]; small = g in smalls
        rungs = {k: v * (sc_t if small else C) / C for k, v in L["rungs"].items()}
        name, tgt = bd.nearest_rung(w_r * (sc_t / SC0 if small else 1), rungs)
        letter = base_letter.get(g)
        if not small and letter and letter in L["classes"]: name = L["classes"][letter]; tgt = rungs[name]
        if not small and letter == "I" and "I" not in L["classes"]: continue
        if w_r < 0.3 * (SC0 if small else C) and not (letter == "I" and "I" in L["classes"]): continue
        if bold: tgt *= T["width"]
        keep = GlyphCoordinates(list(glyf[g].coordinates)); w0 = b[2] - b[0]
        weigh(g); w1 = bd.ink(glyf, g)[2] - bd.ink(glyf, g)[0]; glyf[g].coordinates = keep
        s = (tgt + (w0 - w1)) / w0
        if abs(math.log(s)) > 0.2: continue
        x0_ = b[0]                                          # a second dry run at the scaled size refines the estimate
        glyf[g].coordinates = GlyphCoordinates([(round(x0_ + (x - x0_) * s), y) for x, y in keep]); bs_ = bd.ink(glyf, g)
        weigh(g); b2_ = bd.ink(glyf, g); glyf[g].coordinates = keep
        s = (tgt + ((bs_[2] - bs_[0]) - (b2_[2] - b2_[0]))) / w0
        bd.scale_x_about_left(font, anchors, g, s); snapped[g] = (name, round(tgt), round(s, 4)); exact[g] = tgt
    rec["widths_set"] = len(snapped); rec["width_rungs"] = {g: snapped[g][0] for g in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if g in snapped}

    moved = 0; retry = []; failed = []; overlap = []; marks_left = []
    for g in order:
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0 or g == ".notdef" or hm[g][0] == 0 or (ONLY and g not in ONLY): continue
        if g in ("exclam", "exclamdown"):                    # the wedge: its broad end is the dot less one bowl step
            wedge = T["stem"] * L["dot_ratio"] / L["wedge_ratio"]; co = list(gl.coordinates); st = 0
            for e_ in gl.endPtsOfContours:
                seg = co[st:e_ + 1]; xs_ = [q[0] for q in seg]; ys_ = [q[1] for q in seg]
                if max(ys_) - min(ys_) > 0.4 * X:
                    cx_ = (min(xs_) + max(xs_)) / 2; f_ = wedge / (max(xs_) - min(xs_))
                    for i_ in range(st, e_ + 1): co[i_] = (round(cx_ + (co[i_][0] - cx_) * f_), co[i_][1])
                st = e_ + 1
            gl.coordinates = GlyphCoordinates(co); continue
        moved += weigh(g, (retry, failed, overlap, marks_left))
    tips_trued = 0                                          # a serif's wedge takes one offset along its length: set each tip to the serif outright
    for g in sorted(caps | smalls | figs):
        if glyf[g].numberOfContours > 0 and not (ONLY and g not in ONLY): tips_trued += unify_tips(glyf[g], round(T["serif"]), 20, 2.2 * T["serif"])
    rec["serif_tips_trued"] = tips_trued
    for g in t_family:                                      # and the T family's crossbar to the hairline outright
        if ONLY and g not in ONLY: continue
        top = sc_t if g in smalls else C; u_ = top - round(T["hair"])
        glyf[g].coordinates = GlyphCoordinates([(x, u_) if abs(y - u_) <= 12 and y != u_ else (x, y) for x, y in glyf[g].coordinates])
    trued = 0                                               # true each width: the dry run is an estimate, the rung is exact
    for g, tgt in exact.items():
        b = bd.ink(glyf, g); w_ = b[2] - b[0]
        if abs(w_ - tgt) >= 0.75 and abs(tgt / w_ - 1) < 0.004:      # at most 0.4 %: a stem moves by under half a unit
            bd.scale_x_about_left(font, anchors, g, tgt / w_); trued += 1
    rec["widths_trued"] = trued
    tab_adv = sorted(shm_[0] for shm_ in [source["hmtx"].metrics[q] for q in ("one", "two", "three", "four", "five")])[2]
    shm = source["hmtx"].metrics; restored = 0              # side bearings as drawn: thinning must not move the ink away from its neighbours
    for g in order:
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0 or g == ".notdef" or hm[g][0] == 0 or (ONLY and g not in ONLY): continue
        b = bd.ink(glyf, g); sb_ = bd.ink(sglyf, g)
        if b is None or sb_ is None: continue
        dx = sb_[0] - b[0]; adv_ = sb_[0] + (b[2] - b[0]) + (shm[g][0] - sb_[2])
        if g.split(".")[0] in FIG and abs(shm[g][0] - tab_adv) <= 1:      # a tabular figure keeps the common advance and its centre
            adv_ = tab_adv; dx = round((sb_[0] + sb_[2]) / 2 - (b[0] + b[2]) / 2)
        if dx == 0 and adv_ == hm[g][0]: continue
        if dx:
            gl.coordinates = GlyphCoordinates([(x + dx, y) for x, y in gl.coordinates])
            for a in anchors.get(g, []): a.XCoordinate += dx
        hm[g] = (adv_, hm[g][1]); restored += 1
    rec["side_bearings_restored"] = restored
    reach = set(cmap.values()) | smalls
    rec["points_reweighted"] = moved; rec["second_attempt"] = len(retry); rec["left_at_source_weight"] = len(failed); rec["kept_with_small_overlap"] = len(overlap)
    rec["marks_left_at_source_weight"] = sorted(set(marks_left))
    rec["failed_reachable"] = [g for g in failed if g in reach and not (g in rev and chr(rev[g]).islower())]

    # ---- dots and short bars
    dot_src = bd.ink(sglyf, "period")[2] - bd.ink(sglyf, "period")[0]
    dot_f = T["stem"] * L["dot_ratio"] / dot_src; bar_f = T["stem"] / SRC_STEM; small_h = 0.4 * X
    small = 0
    for g in order:
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0 or g == ".notdef": continue
        small += bd.scale_small_contours(gl, dot_f, bar_f, small_h)
    rec["small_contours_scaled"] = small

    # ---- spacing and encoding
    pre = {g: hm[g][0] for g in ("H", "O")}
    bt.track(font, track, half)
    for sp in ("space", cmap.get(0xA0)):
        if sp in hm: hm[sp] = (round(L["space"]), hm[sp][1])
    for sub in font["cmap"].tables:
        if not sub.isUnicode(): continue
        for cp in list(sub.cmap):
            ch = chr(cp)
            if ch.islower() and len(ch.upper()) == 1 and ord(ch.upper()) in sub.cmap: sub.cmap[cp] = sub.cmap[ord(ch.upper())]

    # ---- names, tables, save
    fam = L["family"]; ps = fam.replace(" ", "") + "-" + style
    name = font["name"]; name.names = [n for n in name.names if n.nameID not in (21, 22, 25)]
    desc = ("Light titling capitals with serifs, derived from Aureate Roman Living Tall (from Liberation Serif) under SIL OFL 1.1. "
            + ("Golden lattice: stem : hairline : serif = phi^2 : phi : 1, stem X*phi^-9/2, widths on C*phi^(n/4)."
               if lattice == "golden" else
               "Apollonian solar lattice: serif : hairline : stem = 1 : sqrt3 : sqrt6, capital = 14 stems, widths in twelfths of the capital."))
    for nid, val in {1: fam, 2: style, 3: f"{VERSION};AURT;{ps}", 4: fam if style == "Regular" else f"{fam} {style}", 5: f"Version {VERSION}",
                     6: ps, 16: fam, 17: style, 9: "Aureate deterministic type system", 10: desc}.items():
        name.setName(val, nid, 3, 1, 0x409)
    font["head"].fontRevision = float(VERSION); os2 = font["OS/2"]
    if bold: os2.usWeightClass = 700; os2.fsSelection = (os2.fsSelection | 0x20) & ~0x40; font["head"].macStyle |= 1
    else: os2.usWeightClass = 400; os2.fsSelection = (os2.fsSelection | 0x40) & ~0x20; font["head"].macStyle &= ~1
    for g in order:
        gl = glyf[g]
        if gl.numberOfContours != 0:
            gl.recalcBounds(glyf)
            if hasattr(gl, "xMin"): hm[g] = (hm[g][0], gl.xMin)
    if "STAT" in font: del font["STAT"]
    buildStatTable(font, [
        {"tag": "wght", "name": "Weight", "values": [{"value": os2.usWeightClass, "name": "Bold" if bold else "Regular", "flags": 0 if bold else 0x2}]},
        {"tag": "ital", "name": "Italic", "values": [{"value": 0, "name": "Roman", "flags": 0x2}]}], elidedFallbackName="Regular")
    name.names = [n for n in name.names if n.platformID != 1]
    if "kern" in font:
        enc = set(font.getBestCmap().values())
        for sub in font["kern"].kernTables:
            if hasattr(sub, "kernTable"):
                for pair in [q for q in sub.kernTable if q[0] not in enc or q[1] not in enc]: del sub.kernTable[pair]
    os2.recalcAvgCharWidth(font)
    out = os.path.join(OUT, "fonts", ps + ".ttf"); font.save(out)
    w = TTFont(out); w.flavor = "woff2"; w.save(out[:-4] + ".woff2")

    # ---- measured
    f2 = TTFont(out); g2 = f2["glyf"]; h2 = f2["hmtx"].metrics
    def iw(n): b = bd.ink(g2, n); return b[2] - b[0]
    def yy(n): b = bd.ink(g2, n); return [b[1], b[3]]
    rec["measured"] = {"stem": bt.stem_width(f2), "hairline": round(bt.bar_thickness(f2), 1), "arm": round(bd.arm_thickness(f2), 1), "serif": round(serif_thickness(f2), 1),
                       "bowl": round(bowl_thickest(f2), 1), "O": yy("O"), "A": yy("A"), "V": yy("V"), "H": yy("H"), "zero": yy("zero"), "seven": yy("seven"),
                       "widths": {n: iw(n) for n in "WMAHKNUVXYDGOQRBCELTZFPSJI"}, "dot": iw("period"), "space": h2["space"][0],
                       "track_added": h2["H"][0] - pre["H"], "H_sc_top": bd.ink(g2, "H.aursc")[3]}
    report["fonts"][ps] = rec
    rec["residual"] = {"serif": T["serif"] - serif_thickness(f2), "hair": T["hair"] - bt.bar_thickness(f2), "stem": T["stem"] - bt.stem_width(f2), "round": T["round"] - bowl_thickest(f2)}
    m = rec["measured"]
    print(ps, json.dumps({"targets": rec["targets"], "second": len(retry), "overlap": len(overlap), "failed": len(failed), "stem": m["stem"], "hairline": m["hairline"], "arm": m["arm"],
                          "serif": m["serif"], "bowl": m["bowl"], "O": m["O"], "A": m["A"], "V": m["V"], "zero": m["zero"], "dot": m["dot"], "widths": m["widths"]}))
    print("   failed reachable:", rec["failed_reachable"][:40])

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True); os.makedirs(os.path.join(OUT, "verification"), exist_ok=True)
    todo = [(l, s) for l in ("golden", "solar") for s in ("Regular", "Bold")]
    if len(sys.argv) > 1: todo = [t for t in todo if any(a in f"{t[0]}-{t[1]}" for a in sys.argv[1:])]
    if os.environ.get("DS_REGULATE"):                 # regulate on I H E O: each round adds the residual to the knot; keep each knot's best round
        allc = {}
        for l, s in todo:
            cal = {}; best = {}
            for it in range(4):
                build(l, s, dict(cal)); r_ = list(report["fonts"].values())[-1]["residual"]
                print("   round", it + 1, {k: round(v, 2) for k, v in r_.items()}, {k: round(v, 2) for k, v in cal.items()})
                for k, v in r_.items():
                    if k not in best or abs(v) < abs(best[k][0]) - 1e-9: best[k] = (v, cal.get(k, 0.0))
                    if abs(v) > 0.5: cal[k] = cal.get(k, 0.0) + max(-3.0, min(3.0, 0.7 * v))
            allc[f"{l}-{s}"] = {k: round(c_, 2) for k, (v, c_) in best.items() if abs(c_) > 1e-9}
            print("  ", f"{l}-{s}", "kept", allc[f"{l}-{s}"], "residuals", {k: round(v, 2) for k, (v, c_) in best.items()})
        json.dump(allc, open(CAL_FILE, "w"), indent=1); sys.exit(0)
    for l, s in todo: build(l, s)
    for ps_, rec_ in report["fonts"].items():
        json.dump(rec_, open(os.path.join(OUT, "verification", f"build_{ps_}.json"), "w"), indent=1, default=str)
