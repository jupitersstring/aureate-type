#!/usr/bin/env python3
"""Aureate Roman Titling 1.820: a titling Roman in the Latin (wedge-serif) manner.

Source: Aureate Roman Living Tall 1.701, Regular and Bold (cap 1453, x 898, C/X = φ).
Construction, each step recorded in verification/titling_report.json:

  T1  Envelope: every horizontal measure × φ^-1/2 (0.78615): outlines, advances, kerning,
      mark anchors, ligature carets. Vertical measures are untouched, so the Tall stature
      and the 954-unit small capitals are exactly those of the Roman.
  T2  Wedge serifs: each flat serif end (a short vertical edge beside a flat base) becomes a
      point. The tip moves outward by the serif thickness × φ^-1 and the inner corner drops
      to thickness × φ^-4 above the base. Arm beaks (short horizontal edges beside a
      vertical) are pointed the same way, extended by their width × φ^-2.
  T2a (1.810) Lighter stems: every stroke edge moves into the ink by delta = stem·(1 − φ^-1/2)/2,
      scaled by the edge normal's horizontal component, so upright and steep strokes thin to
      stem × φ^-1/2. The local horizontal stroke thickness is measured by ray casting; strokes at or
      below 0.56 × stem (hairlines) are untouched and the effect ramps to full at 0.83 × stem.
  T2w (1.820, replaces T2a) One weight law. With H the Roman's hairline (its crossbar, 72 units in
      Regular) and S its stem, every stroke of perpendicular thickness p in the Roman becomes
      H + (p − H)·k here, k = (T − H)/(S − H), where the target stem T is 72·φ in Regular and
      72·φ² in Bold; p ≤ H is kept. So hairline : stem : bold stem = 1 : φ : φ², and verticals,
      diagonals, bowls and the S spine all follow the same law whatever the envelope did to them.
      Thickness is measured by rays along the inward normal in both the Roman and the narrowed
      outline; each edge is offset along its normal and corners are re-intersected, so bars and
      alignment lines do not move.
  T2l (1.820) Lining. Flat forms sit on 0 and C. Rounds overshoot by the Roman's own amount
      (31 for capitals = C·φ^-8, 24 for lowercase and small capitals). Pointed apexes and vertices
      overshoot by the round overshoot × φ (50 and 39). Lining figures are fitted to the capital
      lines: flat at 0 and C, rounds at −31 and C + 31.
  T2b (1.810) Pointed apexes: a flat apex or vertex between two long diagonals (A, V, W, M, Λ, Δ)
      closes to a point and overshoots by the stroke height × φ^-7.
      Serif tips in 1.810 reach thickness × φ^-1/2 (was φ^-1); inner corner thickness × φ^-5.
  T3  Titling space: every advancing glyph gains round(X·φ^-5) = 81 units, split evenly.
  T4  Two families: Aureate Roman Titling (capitals and lowercase, small capitals through
      smcp / c2sc) and Aureate Roman Titling SC (lowercase code points mapped to the drawn
      small capitals, for applications without OpenType feature controls).
"""
import os, sys, json, time, copy
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(time.mktime((2026, 11, 5, 12, 0, 0, 0, 0, 0)))))
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import BaseTable, ValueRecord
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.otlLib.builder import buildStatTable
import math
import numpy as np

PHI = (1 + 5 ** 0.5) / 2
BASE = "/path/to/aureate"
SRC = os.path.join(BASE, "AureateCollection_1.701/fonts")
OUT = os.path.join(BASE, "AureateRomanTitling_1.820")
K = PHI ** -0.5                      # envelope
TRACK = round(898 * PHI ** -5)       # 81
HALF = TRACK // 2                    # 40 left, 41 right
VERSION = "1.820"
SPIKE = PHI ** -0.5                 # serif tip reach, in serif thicknesses (1.800: φ^-1)
INNER = PHI ** -5                   # inner corner height (1.800: φ^-4)
THIN = PHI ** -0.5                  # stem factor
SKIP_RANGES = [(0x2190, 0x23FF), (0x2500, 0x27BF), (0x20D0, 0x20FF)]   # arrows, operators, boxes, shapes

report = {"version": VERSION, "envelope": K, "track": TRACK, "fonts": {}}

# ------------------------------------------------------------------ T1 envelope
def scale_layout(table, k):
    seen = set(); n = [0]
    def visit(o):
        if id(o) in seen: return
        if isinstance(o, ValueRecord):
            seen.add(id(o))
            for a in ("XPlacement", "XAdvance"):
                v = getattr(o, a, None)
                if v: setattr(o, a, round(v * k)); n[0] += 1
        elif isinstance(o, BaseTable):
            seen.add(id(o)); o.ensureDecompiled()
            if isinstance(o, otTables.Anchor):
                o.XCoordinate = round(o.XCoordinate * k); n[0] += 1
            elif isinstance(o, otTables.CaretValue) and getattr(o, "Format", 0) == 1:
                o.Coordinate = round(o.Coordinate * k); n[0] += 1
            for v in list(vars(o).values()): visit(v)
        elif isinstance(o, (list, tuple)):
            for v in o: visit(v)
    visit(table)
    return n[0]

def scale_x(font, k):
    glyf = font["glyf"]; hm = font["hmtx"].metrics
    for g in font.getGlyphOrder():
        gl = glyf[g]
        if gl.isComposite():
            for c in gl.components: c.x = round(c.x * k)
        elif gl.numberOfContours > 0:
            gl.coordinates = GlyphCoordinates([(round(x * k), y) for x, y in gl.coordinates])
        adv, lsb = hm[g]; hm[g] = (round(adv * k), round(lsb * k))
    n = 0
    for tag in ("GPOS", "GDEF"):
        if tag in font: n += scale_layout(font[tag].table, k)
    if "kern" in font:
        for sub in font["kern"].kernTables:
            if hasattr(sub, "kernTable"):
                for pair in list(sub.kernTable): sub.kernTable[pair] = round(sub.kernTable[pair] * k)
    os2 = font["OS/2"]
    for a in ("ySubscriptXSize", "ySubscriptXOffset", "ySuperscriptXSize", "ySuperscriptXOffset"):
        setattr(os2, a, round(getattr(os2, a) * k))
    return n

# ------------------------------------------------------------------ T2 wedge serifs
def contour_points(gl, i):
    s = 0 if i == 0 else gl.endPtsOfContours[i - 1] + 1; e = gl.endPtsOfContours[i]
    return [[gl.coordinates[j][0], gl.coordinates[j][1], bool(gl.flags[j] & 1)] for j in range(s, e + 1)]

def is_end_cap(nb_tip, T, N, nxt):
    """True when T-N is a flat end between two corners that turn the same way (a serif end or beak),
    not a step where the outline simply carries on past N."""
    import math
    a = (T[0] - nb_tip[0], T[1] - nb_tip[1]); b = (N[0] - T[0], N[1] - T[1]); c = (nxt[0] - N[0], nxt[1] - N[1])
    c1 = a[0] * b[1] - a[1] * b[0]; c2 = b[0] * c[1] - b[1] * c[0]
    if c1 * c2 <= 0: return False
    lb = math.hypot(*b); lc = math.hypot(*c)
    if not lb or not lc: return False
    return abs(c2) / (lb * lc) >= 0.42          # at least 25 degrees of turn at the inner corner

def sharpen_glyph(gl, vmin=24, vmax=120, hmin=18, hmax=130, cap_class=True):
    """Returns (serif_ends, beaks) sharpened."""
    out = []; ns = nb = 0
    for ci in range(gl.numberOfContours):
        pts = contour_points(gl, ci); n = len(pts)
        edits = {}
        for i in range(n):
            P = pts[i]; Q = pts[(i + 1) % n]
            if not (P[2] and Q[2]): continue
            A = pts[i - 1]; B = pts[(i + 2) % n]          # A precedes P, B follows Q
            dx = Q[0] - P[0]; dy = Q[1] - P[1]
            if abs(dx) <= 2 and vmin <= abs(dy) <= vmax:
                # vertical serif end: the tip is the endpoint whose on-curve neighbour runs flat
                def flat(pt, nb_):
                    if not nb_[2]: return None
                    ddx = abs(nb_[0] - pt[0]); ddy = abs(nb_[1] - pt[1])
                    return ddy / ddx if ddx >= 40 else None
                rp, rq = flat(P, A), flat(Q, B)
                cp = rp is not None and rp <= 0.1; cq = rq is not None and rq <= 0.1
                if cp and cq:                              # a bar end: the longer flat side is the base
                    la, lb = abs(A[0] - P[0]), abs(B[0] - Q[0])
                    if min(la, lb) < 1.5 * abs(dy): continue   # the outer edge of a beak, not a bar end
                    if la >= 1.3 * lb: cq = False
                    elif lb >= 1.3 * la: cp = False
                if cp == cq: continue                      # symmetric stroke end, or not a serif
                # the other side also runs flat for a short way: this is a beak's outer edge
                oth, onb = (Q, B) if cp else (P, A)
                if onb[2] and 12 <= abs(onb[0] - oth[0]) < 1.5 * abs(dy) and abs(onb[1] - oth[1]) <= 0.1 * abs(onb[0] - oth[0]): continue
                tip_i, inner_i, nb_pt = (i, (i + 1) % n, A) if cp else ((i + 1) % n, i, B)
                if tip_i in edits or inner_i in edits: continue
                T = pts[tip_i]; N = pts[inner_i]; t = abs(dy)
                if not is_end_cap(nb_pt, T, N, B if cp else A): continue
                d = 1 if T[0] > nb_pt[0] else -1
                s = 1 if N[1] > T[1] else -1
                edits[tip_i] = [T[0] + d * round(t * SPIKE), T[1], True]
                edits[inner_i] = [T[0], T[1] + s * max(3, round(t * INNER)), True]
                ns += 1
            elif abs(dy) <= 2 and hmin <= abs(dx) <= hmax:
                # arm beak: the tip is the endpoint whose on-curve neighbour runs vertical
                def upright(pt, nb_):
                    if not nb_[2]: return None
                    ddx = abs(nb_[0] - pt[0]); ddy = abs(nb_[1] - pt[1])
                    return ddx / ddy if ddy >= 60 else None
                rp, rq = upright(P, A), upright(Q, B)
                cp = rp is not None and rp <= 0.1; cq = rq is not None and rq <= 0.1
                if cp and cq:                              # both sides upright: the longer is the outer edge
                    la, lb = abs(A[1] - P[1]), abs(B[1] - Q[1])
                    if min(la, lb) < 1.5 * abs(dx): continue
                    if la >= 1.3 * lb: cq = False
                    elif lb >= 1.3 * la: cp = False
                if cp == cq: continue
                oth, onb = (Q, B) if cp else (P, A)
                if onb[2] and 12 <= abs(onb[1] - oth[1]) < 1.5 * abs(dx) and abs(onb[0] - oth[0]) <= 0.1 * abs(onb[1] - oth[1]): continue
                tip_i, inner_i, nb_pt = (i, (i + 1) % n, A) if cp else ((i + 1) % n, i, B)
                if tip_i in edits or inner_i in edits: continue
                T = pts[tip_i]; N = pts[inner_i]; w = abs(dx)
                if not is_end_cap(nb_pt, T, N, B if cp else A): continue
                d = 1 if T[1] > nb_pt[1] else -1
                s = 1 if N[0] > T[0] else -1
                line = min(LINES, key=lambda L: abs(L - T[1]))
                on_line = abs(line - T[1]) <= 3 and ((d < 0 and line == 0) or (d > 0 and line != 0))
                edits[tip_i] = [T[0], (line + d * pointed_overshoot(cap_class)) if on_line else T[1] + d * round(w * PHI ** -2), True]
                if not on_line: edits[inner_i] = [T[0] + s * max(3, round(w * INNER)), T[1], True]
                nb += 1
        for j, v in edits.items(): pts[j] = v
        out.append(pts)
    if ns or nb:
        gl.coordinates = GlyphCoordinates([(p[0], p[1]) for c in out for p in c])
    return ns, nb

# ------------------------------------------------------------------ T2a lighter stems
def flatten(gl):
    """Line segments of a simple glyph (quadratics in 8 steps). None if a contour has no on-curve point."""
    segs = []
    for ci in range(gl.numberOfContours):
        pts = contour_points(gl, ci)
        if not any(p[2] for p in pts): return None
        k = next(j for j, p in enumerate(pts) if p[2]); seq = pts[k:] + pts[:k] + [pts[k]]
        cur = seq[0]; j = 1
        while j < len(seq):
            if seq[j][2]:
                segs.append((cur[0], cur[1], seq[j][0], seq[j][1])); cur = seq[j]; j += 1
            else:
                c = seq[j]; nxt = seq[j + 1]
                end = nxt if nxt[2] else [(c[0] + nxt[0]) / 2, (c[1] + nxt[1]) / 2, True]
                px, py = cur[0], cur[1]
                for q in range(1, 9):
                    t = q / 8
                    x = (1 - t) ** 2 * cur[0] + 2 * (1 - t) * t * c[0] + t * t * end[0]
                    y = (1 - t) ** 2 * cur[1] + 2 * (1 - t) * t * c[1] + t * t * end[1]
                    segs.append((px, py, x, y)); px, py = x, y
                cur = end; j += 2 if nxt[2] else 1
    return np.array(segs, dtype=float) if segs else None

def crossings(S, y0):
    y1 = S[:, 1]; y2 = S[:, 3]
    m = ((y1 <= y0) & (y2 > y0)) | ((y2 <= y0) & (y1 > y0))
    if not m.any(): return np.empty(0)
    return S[m, 0] + (y0 - S[m, 1]) * (S[m, 2] - S[m, 0]) / (S[m, 3] - S[m, 1])

def ray(S, x0, y0, d):
    xs = crossings(S, y0)
    if not xs.size: return math.inf
    dist = (xs - x0) * d; dist = dist[dist > 0.5]
    return float(dist.min()) if dist.size else math.inf

def inside(S, x, y):
    xs = crossings(S, y)
    return int((xs > x).sum()) % 2 == 1

def bar_thickness(font, glyph="H"):
    """Thickness of the crossbar, measured on a vertical through the middle of the glyph."""
    gl = font["glyf"][glyph]; gl.recalcBounds(font["glyf"]); S = flatten(gl); xm = (gl.xMin + gl.xMax) / 2 + 0.37
    x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
    m = ((x1 <= xm) & (x2 > xm)) | ((x2 <= xm) & (x1 > xm))
    ys = np.sort(y1[m] + (xm - x1[m]) * (y2[m] - y1[m]) / (x2[m] - x1[m]))
    mid = (gl.yMin + gl.yMax) / 2; i = int(np.argmin(np.abs((ys[:-1] + ys[1:]) / 2 - mid)))
    return float(ys[i + 1] - ys[i])

def stem_width(font, glyph="I"):
    gl = font["glyf"][glyph]; S = flatten(gl)
    xs = np.sort(crossings(S, font["OS/2"].sCapHeight / 2 + 0.37))
    return float(xs[1] - xs[0])

def thin_glyph(gl, delta, stem, law=None):
    """Move stem edges into the ink by delta × (horizontal part of the normal).
    An edge is a stem edge when the horizontal ink thickness at its midpoint lies between a
    hairline (0.56 × stem, no effect) and a stem (0.83 × stem, full effect) and is not a run along
    a bar or through several strokes (fades out between 1.4 and 1.8 × stem). A point moves with the
    stronger of its two edges, so stem sides stay straight while bar ends, beaks and serif ends stay."""
    S = flatten(gl)
    if S is None: return 0
    tmin, tref, tmax0, tmax1 = 0.56 * stem, 0.83 * stem, 1.4 * stem, 1.8 * stem
    out = []; moved = 0
    for ci in range(gl.numberOfContours):
        pts = contour_points(gl, ci); n = len(pts)
        # ink side: probe beside the longest straight on-curve edge, else beside a short chord of a curve
        best = None
        for i in range(n):
            a = pts[i]; b = pts[(i + 1) % n]
            if a[2] and b[2]:
                ln = math.hypot(b[0] - a[0], b[1] - a[1])
                if ln >= 12 and (best is None or ln > best[0]): best = (ln, a, b)
        if best is None and any(q[2] for q in pts):
            k = next(j for j, q in enumerate(pts) if q[2]); a = pts[k]; c = pts[(k + 1) % n]; e = pts[(k + 2) % n]
            end = e if e[2] else [(c[0] + e[0]) / 2, (c[1] + e[1]) / 2, True]
            def at(t): return [(1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * end[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * end[1]]
            q1, q2 = at(0.48), at(0.52); ln = math.hypot(q2[0] - q1[0], q2[1] - q1[1])
            if ln > 1e-6: best = (ln, q1, q2)
        if best is None: out.append(pts); continue
        ln, a, b = best; ex, ey = b[0] - a[0], b[1] - a[1]
        sign = -1 if inside(S, (a[0] + b[0]) / 2 - ey / ln * 2.5, (a[1] + b[1]) / 2 + ex / ln * 2.5 + 0.013) else 1
        # per-edge outward normal and stem factor
        normals = []; fac = []; straight = []
        for i in range(n):
            a = pts[i]; b = pts[(i + 1) % n]; ex, ey = b[0] - a[0], b[1] - a[1]; ln = math.hypot(ex, ey)
            straight.append(bool(a[2] and b[2] and ln >= 60 and abs(ex) <= 0.6 * abs(ey)))
            if ln < 1e-6: normals.append(None); fac.append(0.0); continue
            nx, ny = sign * -ey / ln, sign * ex / ln; normals.append((nx, ny))
            if abs(nx) < 0.5: fac.append(0.0); continue      # only edges within 60 degrees of upright bound a stem
            d = -1 if nx > 0 else 1
            x0 = (a[0] + b[0]) / 2 + d * 1.0; y0 = (a[1] + b[1]) / 2 + 0.37
            xs = crossings(S, y0)
            dist = np.sort((xs - x0) * d); dist = dist[dist > 0.5]
            if not dist.size: fac.append(0.0); continue
            if int((xs > x0).sum()) % 2 == 1: t = float(dist[0])              # start is in the ink
            elif dist.size >= 2 and dist[0] < 0.35 * stem: t = float(dist[1] - dist[0])   # control edge just outside
            else: fac.append(0.0); continue
            if a[2] and b[2] and abs(ex) <= 2 and ln <= 130 and t > 1.2 * stem:
                fac.append(0.0); continue                    # the end of a serif or flag, not a stem side
            if law is not None:                              # same law as the main pass, on horizontal thickness
                Hh, kk = law; src_t = t / K
                want = t if src_t <= Hh else min(t, Hh + (src_t - Hh) * kk)
                down = max(0.0, min(1.0, (tmax1 - t) / (tmax1 - tmax0)))
                fac.append(max(0.0, (t - want) / 2) * down / max(delta, 1e-6)); continue
            up = max(0.0, min(1.0, (t - tmin) / (tref - tmin)))
            down = max(0.0, min(1.0, (tmax1 - t) / (tmax1 - tmax0)))
            fac.append(min(up, down))
        new = [list(q) for q in pts]
        for i in range(n):
            # a point on a straight stem side moves with that side, so the side stays straight
            sp, sn = straight[i - 1], straight[i]
            if sp and not sn: f = fac[i - 1]
            elif sn and not sp: f = fac[i]
            else: f = max(fac[i - 1], fac[i])
            if f <= 0: continue
            n1 = normals[i - 1] or normals[i]; n2 = normals[i] or normals[i - 1]
            if n1 is None: continue
            dot = n1[0] * n2[0] + n1[1] * n2[1]
            m = (n1[0] + n2[0]) / 2 if 1 + dot < 0.25 else (n1[0] + n2[0]) / (1 + dot)
            mx = max(-1.5, min(1.5, m))
            if abs(mx) < 0.15: continue
            new[i][0] = round(pts[i][0] - delta * f * mx); moved += 1
        out.append(new)
    if moved:
        gl.coordinates = GlyphCoordinates([(q[0], q[1]) for c in out for q in c])
    return moved

# ------------------------------------------------------------------ T2w one weight law
def flatten_tagged(gl):
    """Line segments of a simple glyph with, for each, the (contour, control-polygon edge) it belongs to.
    Edge i of a contour runs from point i to point i+1."""
    segs = []; tags = []
    for ci in range(gl.numberOfContours):
        pts = contour_points(gl, ci); n = len(pts)
        if not any(q[2] for q in pts): return None, None
        k = next(j for j, q in enumerate(pts) if q[2])
        cur = pts[k]; j = 1
        while j <= n:
            i = (k + j) % n; q = pts[i]
            if q[2]:
                segs.append((cur[0], cur[1], q[0], q[1])); tags.append((ci, (i - 1) % n)); cur = q; j += 1
            else:
                nxt = pts[(i + 1) % n]
                end = nxt if nxt[2] else [(q[0] + nxt[0]) / 2, (q[1] + nxt[1]) / 2, True]
                px, py = cur[0], cur[1]
                for step in range(1, 9):
                    t = step / 8
                    x = (1 - t) ** 2 * cur[0] + 2 * (1 - t) * t * q[0] + t * t * end[0]
                    y = (1 - t) ** 2 * cur[1] + 2 * (1 - t) * t * q[1] + t * t * end[1]
                    segs.append((px, py, x, y)); tags.append((ci, (i - 1) % n if step <= 4 else i)); px, py = x, y
                cur = end; j += 2 if nxt[2] else 1
    return (np.array(segs, dtype=float), tags) if segs else (None, None)

def ray_hits(S, px, py, dx, dy):
    """Sorted distances along the ray to every segment crossed, and the indices of those segments."""
    x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
    ex, ey = x2 - x1, y2 - y1
    den = dx * ey - dy * ex
    ok = np.nonzero(np.abs(den) > 1e-9)[0]
    t = ((x1 - px) * ey - (y1 - py) * ex)[ok] / den[ok]
    u = ((x1 - px) * dy - (y1 - py) * dx)[ok] / den[ok]
    m = (t > 1e-6) & (u >= 0) & (u < 1)
    t = t[m]; idx = ok[m]; o = np.argsort(t)
    return t[o], idx[o]

def ink_sign(S, pts):
    """+1 when the ink lies to the right of the direction of travel (outward = left normal)."""
    n = len(pts); best = None
    for i in range(n):
        a = pts[i]; b = pts[(i + 1) % n]
        if a[2] and b[2]:
            ln = math.hypot(b[0] - a[0], b[1] - a[1])
            if ln >= 12 and (best is None or ln > best[0]): best = (ln, a, b)
    if best is None and any(q[2] for q in pts):
        k = next(j for j, q in enumerate(pts) if q[2]); a = pts[k]; c = pts[(k + 1) % n]; e = pts[(k + 2) % n]
        end = e if e[2] else [(c[0] + e[0]) / 2, (c[1] + e[1]) / 2, True]
        def at(t): return [(1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * end[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * end[1]]
        q1, q2 = at(0.48), at(0.52); ln = math.hypot(q2[0] - q1[0], q2[1] - q1[1])
        if ln > 1e-6: best = (ln, q1, q2)
    if best is None: return None
    ln, a, b = best; ex, ey = b[0] - a[0], b[1] - a[1]
    return -1 if inside(S, (a[0] + b[0]) / 2 - ey / ln * 2.5, (a[1] + b[1]) / 2 + ex / ln * 2.5 + 0.013) else 1

def edge_data(S, tags, pts, sign, sref, sample="max"):
    """Per edge: outward unit normal, perpendicular ink thickness, the edge on the far side of the
    stroke, and whether the edge faces open space (nothing of the glyph beyond it)."""
    n = len(pts); normals = []; thick = []; partner = []; outer = []
    for i in range(n):
        a = pts[i]; b = pts[(i + 1) % n]; ex, ey = b[0] - a[0], b[1] - a[1]; ln = math.hypot(ex, ey)
        if ln < 1e-6: normals.append(None); thick.append(None); partner.append(None); outer.append(False); continue
        nx, ny = sign * -ey / ln, sign * ex / ln; normals.append((nx, ny))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        best_t = None; best_p = None
        for f_ in ((0.2, 0.5, 0.8) if sample == "min" else ((0.5,) if (a[2] and b[2]) else (0.2, 0.5, 0.8))):
            sx, sy = a[0] + ex * f_, a[1] + ey * f_
            h, idx = ray_hits(S, sx - nx * 0.5, sy - ny * 0.5, -nx, -ny)
            if not h.size: continue
            if h.size % 2 == 1: t_, p_ = float(h[0]) + 0.5, tags[idx[0]]
            elif h[0] < 0.35 * sref: t_, p_ = float(h[1] - h[0]), tags[idx[1]]                     # control edge just outside
            else: continue
            if t_ <= 1.6 * sref and (best_t is None or (t_ < best_t if sample == "min" else t_ > best_t)): best_t, best_p = t_, p_
        thick.append(best_t); partner.append(best_p)
        ho, _ = ray_hits(S, mx + nx * 0.5, my + ny * 0.5, nx, ny)
        outer.append(ho.size == 0 or (ho.size == 1 and ho[0] < 0.35 * sref))
    return normals, thick, partner, outer

def reweight_glyph(gl, sgl, s_src, H, k, target_fn=None, lines=None, glyph_box=False, term_len=0.7, dmax=(0.25, 0.4), const_full=None, sample="max", smooth=2, small_h=0.4 * 898, miter=1.7):
    """Offset edges so each stroke has thickness H + (p_src − H)·φ^-2.
    Pinned: flat edges, stroke ends, and up- or down-facing edges with open space beyond them
    (the outside of a bowl or arch at its extreme). The far side of a pinned edge takes the whole
    correction, so alignment lines and overshoots are those of the Roman."""
    if gl.numberOfContours != sgl.numberOfContours or len(gl.coordinates) != len(sgl.coordinates): return 0
    S1, T1 = flatten_tagged(gl); S0, T0 = flatten_tagged(sgl)
    if S1 is None or S0 is None: return 0
    cont = []
    for ci in range(gl.numberOfContours):
        pts = contour_points(gl, ci); spts = contour_points(sgl, ci); n = len(pts)
        sg1 = ink_sign(S1, pts); sg0 = ink_sign(S0, spts)
        ys = [q[1] for q in pts]
        if sg1 is None or sg0 is None or n < 3 or max(ys) - min(ys) < small_h: cont.append(None); continue
        normals, p_now, partner, outer = edge_data(S1, T1, pts, sg1, s_src, sample)
        _, p_src, _, _ = edge_data(S0, T0, spts, sg0, s_src, sample)
        pinned = [False] * n; weight = [0.0] * n            # weight: how firmly the edge keeps its place
        for i in range(n):
            if normals[i] is None: pinned[i] = True; weight[i] = 1.0; continue
            ny = abs(normals[i][1])
            a = pts[i]; b = pts[(i + 1) % n]
            if ny >= 0.985:
                if lines is None: pinned[i] = True; weight[i] = 1.0; continue
                # monoline mode: a flat edge is pinned only where it lies on an alignment line with open space beyond
                if outer[i] and any(abs((a[1] + b[1]) / 2 - L) <= 3 for L in lines): pinned[i] = True; weight[i] = 1.0; continue
            if outer[i] and (lines is None or not (a[2] and b[2])):
                weight[i] = max(0.0, min(1.0, (ny - 0.45) / 0.4))               # eases in from 27 to 58 degrees off upright
            if not (a[2] and b[2]): continue
            e = (b[0] - a[0], b[1] - a[1]); ln = math.hypot(*e)
            if ln > term_len * s_src: continue
            pa = pts[i - 1]; nb = pts[(i + 2) % n]
            e0 = (a[0] - pa[0], a[1] - pa[1]); e2 = (nb[0] - b[0], nb[1] - b[1]); l0 = math.hypot(*e0); l2 = math.hypot(*e2)
            if l0 < 1e-6 or l2 < 1e-6: continue
            c1 = (e0[0] * e[1] - e0[1] * e[0]) / (l0 * ln); c2 = (e[0] * e2[1] - e[1] * e2[0]) / (ln * l2)
            if c1 * c2 > 0 and abs(c1) >= 0.76 and abs(c2) >= 0.76: pinned[i] = True; weight[i] = 1.0     # a stroke end
        for _ in range(3):
            sw = list(weight)
            for i in range(n):
                if pinned[i] or (pts[i][2] and pts[(i + 1) % n][2]): continue
                if outer[i] and abs(normals[i][1]) >= 0.9: continue          # the very extreme of a bowl keeps its full hold
                a_, b_ = (i - 1) % n, (i + 1) % n
                if pinned[a_] or pinned[b_] or normals[a_] is None or normals[b_] is None: continue
                sw[i] = (weight[a_] + 2 * weight[i] + weight[b_]) / 4
            weight = sw
        cont.append(dict(pts=pts, n=n, normals=normals, p_now=p_now, p_src=p_src, partner=partner, pinned=pinned, weight=weight))
    out = []; moved = 0
    for ci, c in enumerate(cont):
        if c is None: out.append(contour_points(gl, ci)); continue
        pts, n, normals = c["pts"], c["n"], c["normals"]
        delta = [None] * n
        for i in range(n):
            if c["pinned"][i]: delta[i] = 0.0; continue
            a, b = c["p_now"][i], c["p_src"][i]
            if a is None or b is None or b > 1.6 * s_src or a > 1.6 * s_src: continue
            target = target_fn(b, normals[i]) if target_fn is not None else (b if b <= H else H + (b - H) * k)
            if const_full is not None:                       # a stroke already thinner than the stem thins in proportion
                full = const_full(normals[i]) * min(1.0, b / (0.9 * s_src))
            else: full = a - target
            pr = c["partner"][i]; wp = cont[pr[0]]["weight"][pr[1]] if pr is not None and cont[pr[0]] is not None else 0.0
            share = (1 - c["weight"][i]) * 0.5 * (1 + wp)        # the two sides always add up to the whole correction
            delta[i] = max(-dmax[0] * s_src, min(dmax[1] * s_src, full * share))
        for i in range(n):                                   # unknown edges take a like-facing neighbour's offset
            if delta[i] is not None: continue
            vals = []
            for j in ((i - 1) % n, (i + 1) % n):
                if delta[j] is not None and not c["pinned"][j] and normals[j] is not None:
                    if normals[i][0] * normals[j][0] + normals[i][1] * normals[j][1] > 0.85: vals.append(delta[j])
            delta[i] = sum(vals) / len(vals) if vals else 0.0
        follow = {}
        for i in range(n):
            if c["pinned"][i] or normals[i] is None or (pts[i][2] and pts[(i + 1) % n][2]): continue
            for j in ((i - 1) % n, (i + 1) % n):
                a_, b_ = pts[j], pts[(j + 1) % n]
                if normals[j] is None or c["pinned"][j] or not (a_[2] and b_[2]): continue
                if math.hypot(b_[0] - a_[0], b_[1] - a_[1]) >= 0.5 * s_src and normals[i][0] * normals[j][0] + normals[i][1] * normals[j][1] > 0.94:
                    follow[i] = delta[j]
        for i, v in follow.items(): delta[i] = v
        for _ in range(smooth):                              # even out the offset along smooth runs of a curve
            sm = list(delta)
            for i in range(n):
                if c["pinned"][i] or normals[i] is None: continue
                if (pts[i][2] and pts[(i + 1) % n][2]) or i in follow: continue      # straight sides and their brackets keep their offset
                a_, b_ = (i - 1) % n, (i + 1) % n
                if normals[a_] is None or normals[b_] is None or c["pinned"][a_] or c["pinned"][b_]: continue
                if normals[i][0] * normals[a_][0] + normals[i][1] * normals[a_][1] > 0.9 and normals[i][0] * normals[b_][0] + normals[i][1] * normals[b_][1] > 0.9:
                    sm[i] = (delta[a_] + 2 * delta[i] + delta[b_]) / 4
            delta = sm
        new = [list(q) for q in pts]
        xs_ = [q[0] for q in pts]; ys_ = [q[1] for q in pts]
        if glyph_box:                                       # counters may grow; nothing may leave the glyph's own box
            xs_ = [q[0] for cc in cont if cc for q in cc["pts"]]; ys_ = [q[1] for cc in cont if cc for q in cc["pts"]]
        x_lo, x_hi, y_lo, y_hi = min(xs_) - 0.08 * s_src, max(xs_) + 0.08 * s_src, min(ys_), max(ys_)
        for i in range(n):
            n1 = normals[i - 1] or normals[i]; n2 = normals[i] or normals[i - 1]
            if n1 is None: continue
            d1 = delta[i - 1] if normals[i - 1] is not None else delta[i]; d2 = delta[i] if normals[i] is not None else delta[i - 1]
            if abs(d1) < 0.25 and abs(d2) < 0.25: continue
            cr = n1[0] * n2[1] - n1[1] * n2[0]
            if abs(cr) < 0.08:
                mx, my = n1[0] + n2[0], n1[1] + n2[1]; ml = math.hypot(mx, my)
                if ml < 1e-6: mx, my, ml = n1[0], n1[1], 1.0
                dx, dy = -(d1 + d2) / 2 * mx / ml, -(d1 + d2) / 2 * my / ml
            else:
                dx = (-d1 * n2[1] + n1[1] * d2) / cr; dy = (-n1[0] * d2 + n2[0] * d1) / cr
            lim = miter * max(abs(d1), abs(d2)) + 1; ln = math.hypot(dx, dy)
            if ln > lim: dx, dy = dx * lim / ln, dy * lim / ln
            # never leave the contour's own vertical extent: lines and overshoots are the Roman's
            new[i][0] = min(x_hi, max(x_lo, pts[i][0] + dx)); new[i][1] = min(y_hi, max(y_lo, pts[i][1] + dy)); moved += 1
        # ---- keep every joint that was smooth in the outline smooth
        def ang(u, v):
            lu, lv = math.hypot(*u), math.hypot(*v)
            if lu < 1e-6 or lv < 1e-6: return 180.0
            return math.degrees(math.acos(max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / (lu * lv)))))
        for i in range(n):
            if not pts[i][2]: continue
            a_, b_ = (i - 1) % n, (i + 1) % n; pa, pb, pp = pts[a_], pts[b_], pts[i]
            if ang((pp[0] - pa[0], pp[1] - pa[1]), (pb[0] - pp[0], pb[1] - pp[1])) > 4.0: continue
            if not pa[2] and not pb[2]:                      # curve to curve: the point stays on the line of its handles
                la = math.hypot(pp[0] - pa[0], pp[1] - pa[1]); lb = math.hypot(pb[0] - pp[0], pb[1] - pp[1])
                t = la / (la + lb) if la + lb > 1e-6 else 0.5
                new[i][0] = new[a_][0] + t * (new[b_][0] - new[a_][0]); new[i][1] = new[a_][1] + t * (new[b_][1] - new[a_][1])
            elif pa[2] != pb[2]:                             # straight to curve: the handle stays on the line
                ln_i, off_i = (a_, b_) if pa[2] else (b_, a_)
                ux, uy = new[i][0] - new[ln_i][0], new[i][1] - new[ln_i][1]; lu = math.hypot(ux, uy)
                if lu > 1e-6:
                    dist = math.hypot(pts[off_i][0] - pp[0], pts[off_i][1] - pp[1])
                    new[off_i][0] = new[i][0] + ux / lu * dist; new[off_i][1] = new[i][1] + uy / lu * dist
                    # the whole bracket travels with its stem, so its shape is the Roman's; the serif end stays
                    step = 1 if off_i == b_ else -1; shift = new[i][0] - pp[0]
                    for k_ in (2, 3):
                        j = (i + step * k_) % n
                        beyond = j if step == 1 else (j - 1) % n          # the edge leaving j, away from the stem
                        if c["pinned"][beyond] and pts[j][2]: break       # reached the serif end
                        if math.hypot(pts[j][0] - pp[0], pts[j][1] - pp[1]) > 1.2 * s_src: break
                        new[j][0] = pts[j][0] + shift; new[j][1] = pts[j][1]
        for q in new: q[0] = round(min(x_hi, max(x_lo, q[0]))); q[1] = round(min(y_hi, max(y_lo, q[1])))
        out.append(new)
    if moved:
        gl.coordinates = GlyphCoordinates([(q[0], q[1]) for c in out for q in c])
    return moved

def crossings_count(gl):
    """Number of proper crossings between non-adjacent outline segments."""
    S = flatten(gl)
    if S is None or len(S) < 4: return 0
    x1, y1, x2, y2 = S[:, 0][:, None], S[:, 1][:, None], S[:, 2][:, None], S[:, 3][:, None]
    X1, Y1, X2, Y2 = S[:, 0][None, :], S[:, 1][None, :], S[:, 2][None, :], S[:, 3][None, :]
    def orient(ax, ay, bx, by, cx, cy): return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    d1 = orient(x1, y1, x2, y2, X1, Y1); d2 = orient(x1, y1, x2, y2, X2, Y2)
    d3 = orient(X1, Y1, X2, Y2, x1, y1); d4 = orient(X1, Y1, X2, Y2, x2, y2)
    eps = 1e-6
    hit = (d1 * d2 < -eps) & (d3 * d4 < -eps)
    return int(np.triu(hit, 2).sum())

def turning_angles(gl):
    """Signed turning angle at every point of the control polygon (degrees); None where an edge is too short."""
    out = []
    for ci in range(gl.numberOfContours):
        pts = contour_points(gl, ci); n = len(pts)
        for i in range(n):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
            u = (b[0] - a[0], b[1] - a[1]); v = (c[0] - b[0], c[1] - b[1]); lu, lv = math.hypot(*u), math.hypot(*v)
            if lu < 10 or lv < 10: out.append(None); continue
            out.append(math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])))
    return out

def shape_changed(before_angles, gl, limit=24.0):
    after = turning_angles(gl)
    if len(after) != len(before_angles): return True
    for a, b in zip(before_angles, after):
        if a is None or b is None: continue
        d = abs(a - b); d = min(d, 360 - d)
        if d > limit: return True
    return False

# ------------------------------------------------------------------ T2b pointed apexes
LINES = (0, 898, 954, 1453)
def pointed_overshoot(cap_class): return round((31 if cap_class else 24) * PHI)     # 50 or 39

def point_apexes(gl, cap_class=True):
    out = []; count = 0; S = None
    for ci in range(gl.numberOfContours):
        pts = contour_points(gl, ci); n = len(pts)
        if n < 5: out.append(pts); continue
        for i in range(n):
            P = pts[i]; Q = pts[(i + 1) % n]; A = pts[i - 1]; B = pts[(i + 2) % n]
            if not (P[2] and Q[2] and A[2] and B[2]): continue
            if abs(Q[1] - P[1]) > 2 or not (8 <= abs(Q[0] - P[0]) <= 210): continue
            dya = A[1] - P[1]; dyb = B[1] - Q[1]
            if dya * dyb <= 0 or min(abs(dya), abs(dyb)) < 300: continue
            ra = abs(A[0] - P[0]) / abs(dya); rb = abs(B[0] - Q[0]) / abs(dyb)
            if not (0.12 <= ra <= 1.3 and 0.12 <= rb <= 1.3): continue
            if (A[0] - P[0]) * (P[0] - Q[0]) <= 0 or (B[0] - Q[0]) * (Q[0] - P[0]) <= 0: continue
            up = 1 if dya < 0 else -1
            line = min(LINES, key=lambda L: abs(L - P[1]))
            if abs(line - P[1]) <= 90: y = line + up * pointed_overshoot(cap_class)      # on a line: exact overshoot
            else: y = P[1] + up * round(max(abs(dya), abs(dyb)) * PHI ** -8)            # inner apex (W, M): a small point
            # which stroke is the thick one: horizontal ink thickness beside each outer edge
            if S is None: S = flatten(gl)
            def hthick(a, b):
                mx_, my_ = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.37
                d = 1 if (P[0] + Q[0]) / 2 > mx_ else -1
                return ray(S, mx_ + d * 1.0, my_, d) if S is not None else 0.0
            ta, tb = hthick(A, P), hthick(Q, B)
            sp = 1 if P[0] > Q[0] else -1
            if ta >= tb:      # the stroke through A–P is thick: its outer edge runs on to the point;
                x = P[0] + (P[0] - A[0]) / (P[1] - A[1]) * (y - P[1])        # the thin side keeps its place (an oblique cut)
                pts[i] = [round(x), y, True]
            else:
                x = Q[0] + (Q[0] - B[0]) / (Q[1] - B[1]) * (y - Q[1])
                pts[(i + 1) % n] = [round(x), y, True]
            count += 1
        out.append(pts)
    if count:
        gl.coordinates = GlyphCoordinates([(p[0], p[1]) for c in out for p in c])
    return count

# ------------------------------------------------------------------ T2l lining figures
FIG = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
def line_figures(font, cap=1453, over=31):
    """Full-height figures take the capital lines: rounds at −over and cap + over, flats at 0 and cap."""
    glyf = font["glyf"]; done = {}
    for g in font.getGlyphOrder():
        base = g.split(".")[0]
        if base not in FIG or base == "one" or any(t in g for t in ("auronum", "sups", "subs", "numr", "dnom", "sinf", ".alt", "aursc")): continue
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0: continue
        gl.recalcBounds(glyf)
        if gl.yMax < 0.9 * cap: continue
        lo, hi = gl.yMin, gl.yMax
        t_hi = cap + over if hi >= cap + 20 else cap            # round top, or flat / pointed top
        t_lo = -over if lo <= -15 else 0
        if (lo, hi) == (t_lo, t_hi) or hi == lo: continue
        a = (t_hi - t_lo) / (hi - lo); b = t_lo - a * lo
        gl.coordinates = GlyphCoordinates([(x, round(a * y + b)) for x, y in gl.coordinates])
        done[g] = [[lo, hi], [t_lo, t_hi]]
    return done

# ------------------------------------------------------------------ T3 titling space
def track(font, t, half):
    glyf = font["glyf"]; hm = font["hmtx"].metrics; moved = set()
    for g in font.getGlyphOrder():
        adv, lsb = hm[g]
        if adv <= 0: continue
        gl = glyf[g]
        if gl.isComposite():
            for c in gl.components: c.x += half
        elif gl.numberOfContours > 0:
            gl.coordinates.translate((half, 0))
        hm[g] = (adv + t, lsb + half); moved.add(g)
    # anchors on advancing bases and ligatures follow their glyph
    if "GPOS" in font:
        for lk in font["GPOS"].table.LookupList.Lookup:
            for st in lk.SubTable:
                if lk.LookupType == 9: st = st.ExtSubTable
                if st.LookupType == 4:
                    for g, br in zip(st.BaseCoverage.glyphs, st.BaseArray.BaseRecord):
                        if g in moved:
                            for a in br.BaseAnchor:
                                if a is not None: a.XCoordinate += half
                elif st.LookupType == 5:
                    for g, la in zip(st.LigatureCoverage.glyphs, st.LigatureArray.LigatureAttach):
                        if g in moved:
                            for cr in la.ComponentRecord:
                                for a in cr.LigatureAnchor:
                                    if a is not None: a.XCoordinate += half
                elif st.LookupType == 6:
                    for g, mr in zip(st.Mark2Coverage.glyphs, st.Mark2Array.Mark2Record):
                        if g in moved:
                            for a in mr.Mark2Anchor:
                                if a is not None: a.XCoordinate += half
                    for g, mr in zip(st.Mark1Coverage.glyphs, st.Mark1Array.MarkRecord):
                        if g in moved: mr.MarkAnchor.XCoordinate += half
                if st.LookupType in (4, 5):
                    cov = st.MarkCoverage.glyphs
                    for g, mr in zip(cov, st.MarkArray.MarkRecord):
                        if g in moved: mr.MarkAnchor.XCoordinate += half
    if "GDEF" in font and getattr(font["GDEF"].table, "LigCaretList", None):
        lcl = font["GDEF"].table.LigCaretList
        for g, lg in zip(lcl.Coverage.glyphs, lcl.LigGlyph):
            if g in moved:
                for cv in lg.CaretValue:
                    if cv.Format == 1: cv.Coordinate += half

# ------------------------------------------------------------------ names
def rename(font, family, style):
    name = font["name"]; ps = family.replace(" ", "") + "-" + style.replace(" ", "")
    full = family if style == "Regular" else f"{family} {style}"
    name.names = [n for n in name.names if n.nameID not in (21, 22, 25) and n.nameID < 256]
    values = {1: family, 2: style, 3: f"{VERSION};AURT;{ps}", 4: full, 5: f"Version {VERSION}", 6: ps, 16: family, 17: style,
              9: "Aureate Roman deterministic type system",
              10: ("A titling Roman in the Latin manner derived from Aureate Roman Living Tall under SIL OFL 1.1. "
                   "Envelope phi^-1/2; every stroke H + (p - H)*phi^-2 with H = S*phi^-2, so stems are S/phi; wedge serifs; "
                   "pointed apexes; titling space X*phi^-5; "
                   "capitals at C = X + round(X*phi^-1) = 1453 with drawn small capitals at 954.")}
    for nid, val in values.items():
        name.setName(val, nid, 3, 1, 0x409)
    font["head"].fontRevision = float(VERSION)
    font["OS/2"].usWidthClass = 3

def smcp_map(font):
    m = {}
    gsub = font["GSUB"].table
    idx = set()
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag == "smcp": idx.update(fr.Feature.LookupListIndex)
    for i in sorted(idx):
        lk = gsub.LookupList.Lookup[i]
        for st in lk.SubTable:
            if lk.LookupType == 7: st = st.ExtSubTable
            if st.LookupType == 1:
                for a, b in st.mapping.items(): m.setdefault(a, b)
            elif st.LookupType == 2:
                for a, seq in st.mapping.items():
                    if len(seq) == 1: m.setdefault(a, seq[0])
    return m

def finish(font, family, style, wght):
    rename(font, family, style)
    glyf = font["glyf"]; hm = font["hmtx"].metrics
    for g in font.getGlyphOrder():
        gl = glyf[g]
        if gl.numberOfContours != 0:
            gl.recalcBounds(glyf)
            if hasattr(gl, "xMin"): hm[g] = (hm[g][0], gl.xMin)
    axes = [
        {"tag": "wght", "name": "Weight", "values": [{"value": wght, "name": "Bold" if wght == 700 else "Regular", "flags": 0x2 if wght == 400 else 0}]},
        {"tag": "wdth", "name": "Width", "values": [{"value": round(K * 100, 3), "name": "Titling"}]},
        {"tag": "ital", "name": "Italic", "values": [{"value": 0, "name": "Roman", "flags": 0x2}]},
    ]
    if "STAT" in font: del font["STAT"]
    buildStatTable(font, axes, elidedFallbackName="Regular")
    font["name"].names = [n for n in font["name"].names if n.platformID != 1]   # no Macintosh records
    if "kern" in font:                                   # legacy kern table: encoded glyphs only
        enc = set(font.getBestCmap().values())
        for sub in font["kern"].kernTables:
            if hasattr(sub, "kernTable"):
                for pair in [q for q in sub.kernTable if q[0] not in enc or q[1] not in enc]: del sub.kernTable[pair]
    font["OS/2"].recalcAvgCharWidth(font)
    out = os.path.join(OUT, "fonts", family.replace(" ", "") + "-" + style.replace(" ", "") + ".ttf")
    font.save(out)
    w = TTFont(out); w.flavor = "woff2"; w.save(out[:-4] + ".woff2")
    return out

def build(style):
    src = os.path.join(SRC, f"AureateRomanLivingTall-{style}.ttf")
    font = TTFont(src); glyf = font["glyf"]; cmap = font.getBestCmap()
    rec = {"source": os.path.basename(src)}
    rec["layout_values_scaled"] = scale_x(font, K)
    import unicodedata
    allowed = {g for cp, g in cmap.items() if (unicodedata.category(chr(cp))[0] in "LN" or cp == 0x26)
               and not any(a <= cp <= b for a, b in SKIP_RANGES)}
    for g in font.getGlyphOrder():                     # unencoded variants follow their base letter
        if g not in allowed and (g.split(".")[0] in allowed or g.startswith("aureate_")): allowed.add(g)
    rec["glyphs_eligible"] = len(allowed)
    source = TTFont(src); sglyf = source["glyf"]            # the untouched Roman, for stroke measurement
    s_src = stem_width(source); rec["stem_roman"] = round(s_src, 1); rec["hairline_law"] = round(s_src * PHI ** -2, 2)
    capclass = {g: (sglyf[g].numberOfContours > 0 and getattr(sglyf[g], "yMax", 0) > 1200) for g in font.getGlyphOrder()}
    moved = apexes = 0; off_line = []; fallback = []; s_scaled = stem_width(font)
    # the weight law: hairline H_w is this weight's own bar; the capital stem lands on 72·φ (Regular) or 72·φ² (Bold)
    H_w = bar_thickness(source); H_ref = 72.0
    stem_target = H_ref * PHI if font["OS/2"].usWeightClass < 600 else H_ref * PHI ** 2
    k_w = (stem_target - H_w) / (s_src - H_w)
    rec["hairline"] = H_w; rec["stem_target"] = round(stem_target, 2); rec["law_k"] = round(k_w, 4)
    for g in font.getGlyphOrder():
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0 or g not in allowed: continue
        before = (GlyphCoordinates(list(gl.coordinates)), crossings_count(gl), turning_angles(gl))
        m_ = reweight_glyph(gl, sglyf[g], s_src, H_w, k_w)
        if m_ and (crossings_count(gl) > before[1] or shape_changed(before[2], gl)):   # tangled or bent: thin stem sides only
            gl.coordinates = before[0]; fallback.append(g)
            m_ = thin_glyph(gl, 1.0, s_scaled, law=(H_w, k_w))
        moved += m_
        gl.recalcBounds(glyf); sglyf[g].recalcBounds(sglyf)
        if abs(gl.yMax - sglyf[g].yMax) > 1 or abs(gl.yMin - sglyf[g].yMin) > 1: off_line.append((g, gl.yMax - sglyf[g].yMax, gl.yMin - sglyf[g].yMin))
        apexes += point_apexes(gl, capclass[g])
    rec["glyphs_off_their_lines_after_reweighting"] = len(off_line); rec["off_line_sample"] = off_line[:12]
    rec["fallback_glyphs"] = len(fallback); rec["fallback_sample"] = fallback[:40]
    rec["figure_extents"] = {g: [glyf[g].yMin, glyf[g].yMax] for g in ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")}
    rec["points_reweighted"] = moved; rec["apexes_pointed"] = apexes; rec["stem_after"] = round(stem_width(font), 1)
    ns = nb = ng = 0
    for g in font.getGlyphOrder():
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0 or g not in allowed: continue
        a, b = sharpen_glyph(gl, cap_class=capclass[g])
        if a or b: ng += 1
        ns += a; nb += b
    rec["serif_ends_pointed"] = ns; rec["beaks_pointed"] = nb; rec["glyphs_changed"] = ng
    rec["figures_lined"] = line_figures(font)
    track(font, TRACK, HALF)
    wght = font["OS/2"].usWeightClass
    out = finish(font, "Aureate Roman Titling", style, wght)
    # small-capitals family: lowercase code points take the drawn small capitals
    sc = TTFont(out); m = smcp_map(sc); remapped = 0
    for sub in sc["cmap"].tables:
        if not sub.isUnicode(): continue
        for cp, g in list(sub.cmap.items()):
            if g in m: sub.cmap[cp] = m[g]; remapped += 1
    rec["sc_codepoints_remapped"] = len({cp for sub in sc["cmap"].tables if sub.isUnicode() for cp, g in sub.cmap.items() if g.endswith(".aursc")})
    finish(sc, "Aureate Roman Titling SC", style, wght)
    hm = font["hmtx"].metrics
    rec["sample"] = {g: [hm[g][0], glyf[g].xMin, hm[g][0] - glyf[g].xMax] for g in ["H", "O", "A", "I", "E", "n", "H.aursc"] if g in hm}
    report["fonts"][style] = rec
    print(style, rec)

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True); os.makedirs(os.path.join(OUT, "verification"), exist_ok=True)
    for style in ("Regular", "Bold"): build(style)
    json.dump(report, open(os.path.join(OUT, "verification", "titling_report.json"), "w"), indent=1)
