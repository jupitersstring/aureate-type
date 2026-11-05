#!/usr/bin/env python3
"""Measure perpendicular stroke thickness on a font's outlines by casting rays along inward normals."""
import sys, math, numpy as np
from fontTools.ttLib import TTFont
import build_titling as bt

def perp_rays(S, pts, nrm):
    """pts (k×2) start points, nrm (k×2) unit directions; returns distance to the nearest segment hit."""
    x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
    ex, ey = x2 - x1, y2 - y1
    out = np.full(len(pts), np.inf)
    for i, ((px, py), (dx, dy)) in enumerate(zip(pts, nrm)):
        den = dx * ey - dy * ex
        ok = np.abs(den) > 1e-9
        t = ((x1 - px) * ey - (y1 - py) * ex)[ok] / den[ok]
        u = ((x1 - px) * dy - (y1 - py) * dx)[ok] / den[ok]
        hit = t[(t > 0.5) & (u >= 0) & (u <= 1)]
        if hit.size: out[i] = hit.min()
    return out

def glyph_thickness(gl):
    """Samples: (x, y, nx, ny, thickness, straight?) at the midpoint of every flattened segment."""
    S = bt.flatten(gl)
    if S is None: return None
    mid = np.column_stack(((S[:, 0] + S[:, 2]) / 2, (S[:, 1] + S[:, 3]) / 2))
    ex, ey = S[:, 2] - S[:, 0], S[:, 3] - S[:, 1]; ln = np.hypot(ex, ey); keep = ln > 2
    S2, mid, ex, ey, ln = S[keep], mid[keep], ex[keep], ey[keep], ln[keep]
    left = np.column_stack((-ey / ln, ex / ln))
    # ink side per sample
    ins = np.array([bt.inside(S, m[0] + l[0] * 1.2, m[1] + l[1] * 1.2 + 0.013) for m, l in zip(mid, left)])
    inward = np.where(ins[:, None], left, -left)
    th = perp_rays(S, mid + inward * 0.6, inward)
    return mid, inward, th, ln

if __name__ == "__main__":
    path = sys.argv[1]; names = sys.argv[2:]
    f = TTFont(path); glyf = f["glyf"]; stem = bt.stem_width(f)
    print("stem(I at mid cap) =", round(stem, 1))
    for g in names:
        r = glyph_thickness(glyf[g])
        if r is None: continue
        mid, inward, th, ln = r
        fin = np.isfinite(th)
        thick = th[fin & (th > 0.7 * stem) & (th < 2.0 * stem)]; wt = ln[fin & (th > 0.7 * stem) & (th < 2.0 * stem)]
        thin = th[fin & (th > 25) & (th <= 0.7 * stem)]
        def wq(v, w, q):
            if not v.size: return float("nan")
            o = np.argsort(v); c = np.cumsum(w[o]); return float(v[o][np.searchsorted(c, q * c[-1])])
        print(f"{g:10s} thick: median {wq(thick, wt, 0.5):6.1f}  p90 {wq(thick, wt, 0.9):6.1f}  max {thick.max() if thick.size else float('nan'):6.1f} | thin: median {np.median(thin) if thin.size else float('nan'):6.1f}  min {thin.min() if thin.size else float('nan'):6.1f} | yMax {glyf[g].yMax} yMin {glyf[g].yMin}")
