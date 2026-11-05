#!/usr/bin/env python3
"""Aureate Collection 1.701: deterministic post-release repairs to the 1.700 binaries.

Reads  …/AureateCollection_1.700/fonts/*.ttf and the bundled upstream programs.
Writes …/AureateCollection_1.701/fonts/*.ttf and *.woff2, plus verification/repair_report.json.
The 1.700 package is never modified.

Repairs (see CHANGELOG.md in the output folder for the rationale):
  R1  Sidebearing floor for the Roman programs: no side may sit below the upstream
      Liberation Serif bearing scaled by the family's own bearing exponent.
  R2  Default (tabular) figures centred in their advance; figure-to-figure kerning removed
      from the default figures so ledgers align with kerning on.
  R3  Sans Geometric: the rebuilt glyphs (flat ~50/50 bearings) take the spacing of their
      Aureate Sans counterparts scaled by the retained-glyph factor.
  R4  Visible .notdef in the Roman programs.
  R5  Underline and strikeout unified across the collection: underline -212 / 81
      (X·φ^-3 and that ·φ^-2), strikeout at X/2 = 449, thickness 81.
  R6  gasp and prep (smart dropout control) for every program.
  R7  Degenerate contours removed (fewer than three points; repeated points).
  R8  Missing curve extrema inserted on static programs (variable programs untouched).
  R9  GDEF classes: sofpasuq is a base, U+034F is a mark.
  R10 Variable programs: default instance named after the style; Sans width programs
      gain Condensed / Calm / default named instances and a Calm STAT value.
  R11 Name table: version 1.701, Macintosh name records removed, xAvgCharWidth recalculated.
  R12 GSUB/GPOS feature and script records sorted by tag (OTS warning).
  R13 usWinAscent/usWinDescent equal across the four styles of each family.
"""
import os, sys, json, math, glob, shutil, time, copy, statistics
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(time.mktime((2026, 10, 28, 12, 0, 0, 0, 0, 0)))))
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.bezierTools import splitQuadraticAtT
from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib.tables._f_v_a_r import NamedInstance

PHI = (1 + 5 ** 0.5) / 2
BASE = "/path/to/aureate"
SRC = os.path.join(BASE, "AureateCollection_1.700")
OUT = os.path.join(BASE, "AureateCollection_1.701")
UP_ROMAN = os.path.join(SRC, "source/upstream/roman")
UP_SANS = os.path.join(SRC, "source/upstream")
X = 898
UNDERLINE_POS, UNDERLINE_THICK = -212, 81         # round(X·φ^-3), round(212·φ^-2)
STRIKE_POS, STRIKE_THICK = 449, 81                # X/2
FIGURES = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}

# family -> (group, bearing scale k, upstream file stem)
FAMILIES = {
    "Aureate Roman Living": ("roman", 1.0), "Aureate Roman Living Tall": ("roman", 1.0),
    "Aureate Roman Living Short": ("roman", 1.0), "Aureate Roman Living Variable": ("roman", 1.0),
    "Aureate Roman Living Condensed": ("roman", PHI ** (-1 / 8)),
    "Aureate Roman Living Olympian": ("roman", PHI ** (-3 / 16)),
    "Aureate Roman Monumental": ("roman", PHI ** (1 / 16)),
    "Aureate Sans": ("sans", 1.0), "Aureate Sans Tall": ("sans", 1.0), "Aureate Sans Short": ("sans", 1.0),
    "Aureate Sans Condensed": ("sans", 1.0), "Aureate Sans Variable": ("sans", 1.0),
    "Aureate Sans Geometric": ("geometric", 1.0),
}
UP_FILE = {("roman", "Regular"): "LiberationSerif-Regular.ttf", ("roman", "Italic"): "LiberationSerif-Italic.ttf",
           ("roman", "Bold"): "LiberationSerif-Bold.ttf", ("roman", "Bold Italic"): "LiberationSerif-BoldItalic.ttf"}
SANS_FILE = {"Regular": "AureateSans-Regular.ttf", "Italic": "AureateSans-Italic.ttf",
             "Bold": "AureateSans-Bold.ttf", "Bold Italic": "AureateSans-BoldItalic.ttf"}
SUFFIXES = [".aursc", ".auronum.tnum", ".auronum.pnum", ".auronum", ".aurlnum.pnum", ".aurtnum", ".aurpnum",
            ".aursups", ".aursubs", ".aursinf", ".aurnumr", ".aurdnom", ".aurcase", ".aurcpsp", ".tnum", ".pnum"]

report = {"collection": "1.701", "fonts": {}}

def family_win_metrics():
    """R13: usWinAscent/usWinDescent equal across the four styles of a family (max ink of the family)."""
    fam_max = {}
    for f in glob.glob(os.path.join(SRC, "fonts", "*.ttf")):
        t = TTFont(f, lazy=True); fam = t["name"].getDebugName(16) or t["name"].getDebugName(1)
        a, d = fam_max.get(fam, (0, 0)); fam_max[fam] = (max(a, t["head"].yMax), max(d, -t["head"].yMin)); t.close()
    return fam_max
FAMILY_WIN = None

def bounds(gs, name):
    bp = BoundsPen(gs); gs[name].draw(bp); return bp.bounds

def bearings_of(font, name, gs=None):
    """(advance, lsb, rsb, bounds) from the integer glyf bounds, recalculated from the outline."""
    hm = font["hmtx"].metrics; glyf = font["glyf"]
    if name not in hm or name not in glyf: return None
    gl = glyf[name]
    if gl.numberOfContours == 0: return None
    gl.recalcBounds(glyf)
    if not hasattr(gl, "xMin"): return None
    adv = hm[name][0]
    return adv, gl.xMin, adv - gl.xMax, (gl.xMin, gl.yMin, gl.xMax, gl.yMax)

# --------------------------------------------------------------------------- outline helpers
def contour_points(glyph, i):
    start = 0 if i == 0 else glyph.endPtsOfContours[i - 1] + 1
    end = glyph.endPtsOfContours[i]
    return [(glyph.coordinates[j][0], glyph.coordinates[j][1], bool(glyph.flags[j] & 1)) for j in range(start, end + 1)]

def rebuild_glyph(glyph, contours):
    coords, flags, ends = [], [], []
    for c in contours:
        for x, y, on in c:
            coords.append((x, y)); flags.append(1 if on else 0)
        ends.append(len(coords) - 1)
    glyph.coordinates = GlyphCoordinates(coords); glyph.flags = bytearray(flags)
    glyph.endPtsOfContours = ends; glyph.numberOfContours = len(contours)

def clean_contours(glyph):
    """R7: drop contours with < 3 points and consecutive duplicate points. Returns count of fixes."""
    fixes = 0; out = []
    for i in range(glyph.numberOfContours):
        pts = contour_points(glyph, i)
        dedup = []
        for p in pts:
            if dedup and dedup[-1][0] == p[0] and dedup[-1][1] == p[1]:
                if p[2] and not dedup[-1][2]: dedup[-1] = p
                fixes += 1; continue
            dedup.append(p)
        if len(dedup) > 1 and dedup[0][0] == dedup[-1][0] and dedup[0][1] == dedup[-1][1]:
            dedup.pop(); fixes += 1
        if len(dedup) < 3: fixes += 1; continue
        out.append(dedup)
    if fixes: rebuild_glyph(glyph, out)
    return fixes

def add_extrema(glyph):
    """R8: insert on-curve points at quadratic extrema that lie more than 2 units beyond both ends."""
    inserted = 0; out = []
    for i in range(glyph.numberOfContours):
        pts = contour_points(glyph, i)
        if not any(p[2] for p in pts): out.append(pts); continue
        k = next(j for j, p in enumerate(pts) if p[2]); pts = pts[k:] + pts[:k]
        # explicit quadratics
        segs = []; j = 0; n = len(pts)
        while j < n:
            p0 = pts[j]; offs = []; m = j + 1
            while m < n and not pts[m % n][2]: offs.append(pts[m]); m += 1
            p2 = pts[m % n]
            if not offs: segs.append(("line", p0, p2))
            else:
                cur = p0
                for q, c in enumerate(offs):
                    if q < len(offs) - 1:
                        nxt = offs[q + 1]; mid = ((c[0] + nxt[0]) / 2, (c[1] + nxt[1]) / 2, True)
                    else: mid = p2
                    segs.append(("quad", cur, c, mid)); cur = mid
            j = m
        new = []
        for s in segs:
            if s[0] == "line": new.append(s); continue
            stack = [(s[1], s[2], s[3])]
            while stack:
                p0, c, p2 = stack.pop(0)
                split_t = None
                for ax in (0, 1):
                    den = p0[ax] - 2 * c[ax] + p2[ax]
                    if den == 0: continue
                    t = (p0[ax] - c[ax]) / den
                    if 0.03 < t < 0.97:
                        e = (1 - t) ** 2 * p0[ax] + 2 * (1 - t) * t * c[ax] + t * t * p2[ax]
                        if min(abs(e - p0[ax]), abs(e - p2[ax])) > 2 and (e > max(p0[ax], p2[ax]) or e < min(p0[ax], p2[ax])):
                            split_t = t; break
                if split_t is None: new.append(("quad", p0, c, p2)); continue
                a, b = splitQuadraticAtT((p0[0], p0[1]), (c[0], c[1]), (p2[0], p2[1]), split_t)
                m = (round(a[2][0]), round(a[2][1]), True)
                inserted += 1
                stack.insert(0, (m, (round(b[1][0]), round(b[1][1]), False), p2))
                stack.insert(0, (p0, (round(a[1][0]), round(a[1][1]), False), m))
        # back to point list, re-implying midpoints where exact
        pl = []
        for s in new:
            if s[0] == "line":
                if not pl or pl[-1][:2] != s[1][:2]: pl.append((s[1][0], s[1][1], True))
            else:
                _, p0, c, p2 = s
                if not pl or pl[-1][:2] != p0[:2]: pl.append((p0[0], p0[1], True))
                pl.append((c[0], c[1], False))
                pl.append((p2[0], p2[1], True))
        if pl and pl[0][:2] == pl[-1][:2] and len(pl) > 1: pl.pop()
        # remove on-curve points that are exact midpoints of neighbouring off-curves
        compact = []
        for idx, p in enumerate(pl):
            prv = pl[idx - 1]; nxt = pl[(idx + 1) % len(pl)]
            if p[2] and not prv[2] and not nxt[2] and (prv[0] + nxt[0]) == 2 * p[0] and (prv[1] + nxt[1]) == 2 * p[1]:
                continue
            compact.append((int(round(p[0])), int(round(p[1])), p[2]))
        out.append(compact)
    if inserted: rebuild_glyph(glyph, out)
    return inserted

def shift_simple(glyph, dx):
    if dx: glyph.coordinates.translate((dx, 0))

# --------------------------------------------------------------------------- notdef
def draw_notdef(font, cap):
    glyf = font["glyf"]; adv = 1229
    w = round(cap * 0.75); s = round(cap / 13); x0 = (adv - w) // 2
    outer = [(x0, 0), (x0, cap), (x0 + w, cap), (x0 + w, 0)]
    inner = [(x0 + s, s), (x0 + w - s, s), (x0 + w - s, cap - s), (x0 + s, cap - s)]
    g = Glyph(); g.numberOfContours = 2
    g.coordinates = GlyphCoordinates(outer + inner); g.flags = bytearray([1] * 8); g.endPtsOfContours = [3, 7]
    from fontTools.ttLib.tables.ttProgram import Program
    g.program = Program()
    glyf[".notdef"] = g; font["hmtx"].metrics[".notdef"] = (adv, x0)
    if "gvar" in font: font["gvar"].variations.pop(".notdef", None)

# --------------------------------------------------------------------------- layout sorting
def sort_layout(table):
    t = table.table
    fl = t.FeatureList; recs = fl.FeatureRecord
    order = sorted(range(len(recs)), key=lambda i: (recs[i].FeatureTag, i))
    remap = {old: new for new, old in enumerate(order)}
    fl.FeatureRecord = [recs[i] for i in order]
    def fix_langsys(ls):
        if ls is None: return
        if ls.ReqFeatureIndex != 0xFFFF: ls.ReqFeatureIndex = remap[ls.ReqFeatureIndex]
        ls.FeatureIndex = sorted(remap[i] for i in ls.FeatureIndex)
    sl = t.ScriptList; sl.ScriptRecord.sort(key=lambda r: r.ScriptTag)
    for sr in sl.ScriptRecord:
        fix_langsys(sr.Script.DefaultLangSys)
        sr.Script.LangSysRecord.sort(key=lambda r: r.LangSysTag)
        for lr in sr.Script.LangSysRecord: fix_langsys(lr.LangSys)
    fv = getattr(t, "FeatureVariations", None)
    if fv:
        for rec in fv.FeatureVariationRecord:
            for sub in rec.FeatureTableSubstitution.SubstitutionRecord:
                sub.FeatureIndex = remap[sub.FeatureIndex]
    return len(recs)

# --------------------------------------------------------------------------- kerning
def pairpos_subtables(gpos):
    for lk in gpos.table.LookupList.Lookup:
        for st in lk.SubTable:
            if lk.LookupType == 9: st = st.ExtSubTable
            if st.LookupType == 2: yield st

def zero_figure_kerning(font, figs):
    """R2b: remove XAdvance kerning where both glyphs are default figures."""
    removed = 0
    if "GPOS" in font:
        for st in pairpos_subtables(font["GPOS"]):
            if st.Format == 1:
                for g1, ps in zip(st.Coverage.glyphs, st.PairSet):
                    if g1 not in figs: continue
                    keep = []
                    for pvr in ps.PairValueRecord:
                        if pvr.SecondGlyph in figs and pvr.Value1 and getattr(pvr.Value1, "XAdvance", 0): removed += 1; continue
                        keep.append(pvr)
                    ps.PairValueRecord = keep; ps.PairValueCount = len(keep)
            else:
                c1 = st.ClassDef1.classDefs; c2 = st.ClassDef2.classDefs
                members1 = {}; members2 = {}
                for g, c in c1.items(): members1.setdefault(c, set()).add(g)
                for g, c in c2.items(): members2.setdefault(c, set()).add(g)
                for i, r1 in enumerate(st.Class1Record):
                    m1 = members1.get(i, set())
                    if not m1 or not m1 <= figs: continue
                    for j, r2 in enumerate(r1.Class2Record):
                        m2 = members2.get(j, set())
                        if m2 and m2 <= figs and r2.Value1 and getattr(r2.Value1, "XAdvance", 0):
                            r2.Value1.XAdvance = 0; removed += 1
    if "kern" in font:
        for sub in font["kern"].kernTables:
            if hasattr(sub, "kernTable"):
                for pair in [p for p in sub.kernTable if p[0] in figs and p[1] in figs]:
                    del sub.kernTable[pair]; removed += 1
    return removed

# --------------------------------------------------------------------------- per-font repair
def repair(path):
    font = TTFont(path); name = font["name"]
    fam = name.getDebugName(16) or name.getDebugName(1); sty = name.getDebugName(17) or name.getDebugName(2)
    group, k = FAMILIES[fam]
    r = {"family": fam, "style": sty, "group": group}
    glyf = font["glyf"]; hmtx = font["hmtx"].metrics; gs = font.getGlyphSet(); cmap = font.getBestCmap()
    os2 = font["OS/2"]; is_vf = "gvar" in font
    if is_vf:  # materialise every lazy gvar record against the original outlines
        gv = font["gvar"]; gv.variations = {g: gv.variations[g] for g in list(gv.variations.keys())}
    cap = os2.sCapHeight
    order = font.getGlyphOrder()

    # ---- R7 / R8 outline cleanup
    cleaned = 0; extrema = 0
    for g in order:
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0: continue
        if is_vf: continue   # point counts are bound to gvar; variable programs keep their outlines
        cleaned += clean_contours(gl)
        extrema += add_extrema(gl)
    r["contours_cleaned"] = cleaned; r["extrema_inserted"] = extrema

    # ---- R1 / R3 spacing
    deltas = {}   # glyph -> (dx, dadv)
    ref = None
    if group == "roman":
        ref = TTFont(os.path.join(UP_ROMAN, UP_FILE[("roman", sty)]))
    elif group == "geometric":
        ref = TTFont(os.path.join(SRC, "fonts", SANS_FILE[sty]))
    if ref is not None:
        rgs = ref.getGlyphSet(); rhm = ref["hmtx"].metrics
        scale = 1.0
        if group == "geometric":
            ratios = []
            for g in order:
                if g in rhm and hmtx[g][0] and rhm[g][0]:
                    a = bearings_of(font, g, gs); b = bearings_of(ref, g, rgs)
                    if a and b and b[1] > 60 and a[1] > 0 and not (abs(a[1] - a[2]) <= 3 and 40 <= a[1] <= 62): ratios.append(a[1] / b[1])
            scale = statistics.median(ratios); r["geometric_retained_scale"] = round(scale, 4)
        for g in order:
            gl = glyf[g]
            if gl.isComposite() or gl.numberOfContours <= 0 or g == ".notdef": continue
            if g not in rhm or hmtx[g][0] == 0: continue
            a = bearings_of(font, g, gs); b = bearings_of(ref, g, rgs)
            if not a or not b: continue
            adv, lsb, rsb, _ = a; _, ulsb, ursb, _ = b
            if group == "roman":
                tl, tr = round(ulsb * k), round(ursb * k)
                dx = max(0, tl - lsb); dr = max(0, tr - rsb)
            else:
                # rebuilt geometric glyph: flat 40..62 bearings that are not the Sans's own
                if not (abs(lsb - rsb) <= 3 and 40 <= lsb <= 62 and not (abs(ulsb - lsb) <= 3 and abs(ursb - rsb) <= 3)): continue
                tl, tr = round(ulsb * scale), round(ursb * scale)
                dx = tl - lsb; dr = tr - rsb
            if dx or dr:
                deltas[g] = (dx, dr)
        # derived glyphs follow their base, scaled by advance ratio
        for g in order:
            if g in deltas or glyf[g].isComposite(): continue
            base = None
            for suf in SUFFIXES:
                if g.endswith(suf) and g[: -len(suf)] in deltas: base = g[: -len(suf)]; break
            if base is None: continue
            badv = hmtx[base][0]; adv = hmtx[g][0]
            if not badv or not adv: continue
            s = min(1.2, max(0.5, adv / badv))
            dx, dr = deltas[base]; dx, dr = round(dx * s), round(dr * s)
            if dx or dr: deltas[g] = (dx, dr)
        for g, (dx, dr) in deltas.items():
            shift_simple(glyf[g], dx); hmtx[g] = (hmtx[g][0] + dx + dr, hmtx[g][1] + dx)
        # composites: follow the first component that moved; other components shift with it
        comp_follow = 0
        for g in order:
            gl = glyf[g]
            if not gl.isComposite(): continue
            base = gl.components[0].glyphName
            if base in deltas:
                dx, dr = deltas[base]
                for c in gl.components[1:]:
                    c.x += dx
                hmtx[g] = (hmtx[g][0] + dx + dr, hmtx[g][1] + dx); comp_follow += 1
        r["spacing_glyphs_shifted"] = len(deltas); r["composites_following"] = comp_follow
        r["spacing_sample"] = {g: deltas[g] for g in ["n", "m", "o", "u", "r", "a", "e", "H", "N", "L", "Z", "j"] if g in deltas}

    # ---- R2 figures: centre the Roman figure 1 on its foot, remove figure-figure kerning
    centred = {}
    figs = set()
    for g in order:
        base = g.split(".")[0]
        if base in FIGURES and (g == base or ".tnum" in g or g.endswith(".tab") or g.endswith(".t")): figs.add(g)
    if group == "roman" and "one" in glyf and not glyf["one"].isComposite() and glyf["one"].numberOfContours > 0:
        gl = glyf["one"]; adv = hmtx["one"][0]
        def foot_centre(glyph):
            xs = [glyph.coordinates[i][0] for i in range(len(glyph.coordinates)) if glyph.coordinates[i][1] <= 40]
            return (min(xs) + max(xs)) / 2 if xs else None
        centre = foot_centre(gl)
        # keep the upstream foot offset from the advance centre (italics sit left of centre by design)
        offset = 0
        if ref is not None and "one" in ref["glyf"]:
            rc = foot_centre(ref["glyf"]["one"])
            if rc is not None: offset = rc - ref["hmtx"].metrics["one"][0] / 2
        if centre is not None:
            dx = round(adv / 2 + offset - centre)
            if abs(dx) >= 6:
                shift_simple(gl, dx); hmtx["one"] = (adv, hmtx["one"][1] + dx); centred["one"] = dx
    r["figures_centred"] = centred
    r["figure_kern_pairs_removed"] = zero_figure_kerning(font, figs)

    # ---- R4 notdef
    if glyf[".notdef"].numberOfContours == 0:
        draw_notdef(font, cap); r["notdef_drawn"] = True

    # ---- recompute bounds and lsb for every glyph
    for g in order:
        gl = glyf[g]
        if gl.isComposite():
            gl.recalcBounds(glyf)
        elif gl.numberOfContours > 0:
            gl.recalcBounds(glyf)
        else:
            continue
        adv = hmtx[g][0]; hmtx[g] = (adv, gl.xMin)

    # ---- R13 family-wide Windows metrics
    global FAMILY_WIN
    if FAMILY_WIN is None: FAMILY_WIN = family_win_metrics()
    wa, wd = FAMILY_WIN[fam]
    if (os2.usWinAscent, os2.usWinDescent) != (wa, wd):
        r["win_metrics"] = [[os2.usWinAscent, os2.usWinDescent], [wa, wd]]; os2.usWinAscent, os2.usWinDescent = wa, wd

    # ---- R5 underline / strikeout
    post = font["post"]; post.underlinePosition = UNDERLINE_POS; post.underlineThickness = UNDERLINE_THICK
    os2.yStrikeoutPosition = STRIKE_POS; os2.yStrikeoutSize = STRIKE_THICK

    # ---- R6 gasp / prep
    gasp = newTable("gasp"); gasp.version = 1; gasp.gaspRange = {7: 10, 0xFFFF: 15}; font["gasp"] = gasp
    if "prep" not in font:
        prep = newTable("prep"); prep.program = None
        from fontTools.ttLib.tables.ttProgram import Program
        p = Program(); p.fromBytecode(b"\xb8\x01\xff\x85\xb0\x04\x8d"); prep.program = p; font["prep"] = prep
        mx = font["maxp"]; mx.maxStackElements = max(getattr(mx, "maxStackElements", 0), 2)
        mx.maxSizeOfInstructions = max(getattr(mx, "maxSizeOfInstructions", 0), 7)
        mx.maxFunctionDefs = max(getattr(mx, "maxFunctionDefs", 0), 0)
        r["prep_added"] = True

    # ---- R9 GDEF classes
    if "GDEF" in font and font["GDEF"].table.GlyphClassDef:
        cd = font["GDEF"].table.GlyphClassDef.classDefs
        if "sofpasuq" in cd and cd["sofpasuq"] == 3: cd["sofpasuq"] = 1; r["gdef_sofpasuq_base"] = True
        if "uni034F" in cmap.values() and cd.get("uni034F") != 3: cd["uni034F"] = 3; r["gdef_cgj_mark"] = True

    # ---- R10 variable instances
    if "fvar" in font:
        fvar = font["fvar"]
        style_id = 17 if name.getDebugName(17) else 2
        def nid(text):
            return name.addMultilingualName({"en": text}, font, minNameID=256)
        default_nid = nid(sty)
        want = [("Condensed", 88.66517639160156), ("Calm", PHI ** (-1 / 8) * 100), (sty, 100.0)]
        fvar.instances = []
        for label, val in want:
            inst = NamedInstance(); inst.coordinates = {"wdth": val}
            inst.subfamilyNameID = default_nid if label == sty else nid(label); inst.postscriptNameID = 0xFFFF
            fvar.instances.append(inst)
        # STAT: ensure Condensed / Calm / default(elided) values
        wght = os2.usWeightClass; ital = 1 if "Italic" in sty else 0
        axes = [
            {"tag": "wght", "name": "Weight", "values": [{"value": wght, "name": "Bold" if wght == 700 else "Regular", "flags": 0x2 if wght == 400 else 0}]},
            {"tag": "wdth", "name": "Width", "values": [
                {"value": 88.66517639160156, "name": "Condensed"},
                {"value": PHI ** (-1 / 8) * 100, "name": "Calm"},
                {"value": 100.0, "name": "Text" if group != "roman" else "Roman", "flags": 0x2},
            ]},
            {"tag": "ital", "name": "Italic", "values": [{"value": 1, "name": "Italic"} if ital else {"value": 0, "name": "Roman", "flags": 0x2, "linkedValue": 1}]},
        ]
        buildStatTable(font, axes, elidedFallbackName="Regular")
        r["vf_instances"] = [l for l, _ in want]
    elif "STAT" not in font:
        wdth = {"Aureate Roman Living Condensed": 88.665, "Aureate Sans Condensed": 88.665,
                "Aureate Roman Living Olympian": 83.489, "Aureate Roman Monumental": 106.2}.get(fam, 100.0)
        wght = os2.usWeightClass; ital = 1 if "Italic" in sty else 0
        axes = [
            {"tag": "wght", "name": "Weight", "values": [{"value": wght, "name": "Bold" if wght == 700 else "Regular", "flags": 0x2 if wght == 400 else 0}]},
            {"tag": "wdth", "name": "Width", "values": [{"value": wdth, "name": {100.0: "Normal", 88.665: "Condensed", 83.489: "Olympian", 106.2: "Monumental"}[wdth], "flags": 0x2 if wdth == 100.0 else 0}]},
            {"tag": "ital", "name": "Italic", "values": [{"value": 1, "name": "Italic"} if ital else {"value": 0, "name": "Roman", "flags": 0x2, "linkedValue": 1}]},
        ]
        buildStatTable(font, axes, elidedFallbackName="Regular")
        r["stat_added"] = True

    # ---- R11 names, version, xAvgCharWidth
    name.names = [n for n in name.names if n.platformID != 1]
    for n in name.names:
        if n.nameID == 5: n.string = "Version 1.701"
        if n.nameID == 3:
            s = n.toUnicode(); n.string = s.replace("1.600;", "1.701;").replace("1.700;", "1.701;")
    font["head"].fontRevision = 1.701
    os2.recalcAvgCharWidth(font)

    # ---- R12 sort layout tags
    for tag in ("GSUB", "GPOS"):
        if tag in font: sort_layout(font[tag])

    # ---- write
    out_ttf = os.path.join(OUT, "fonts", os.path.basename(path))
    font.save(out_ttf)
    w = TTFont(out_ttf); w.flavor = "woff2"; w.save(out_ttf[:-4] + ".woff2")
    r["bytes_ttf"] = os.path.getsize(out_ttf); r["bytes_woff2"] = os.path.getsize(out_ttf[:-4] + ".woff2")
    return r

def main():
    only = sys.argv[1:]
    os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True); os.makedirs(os.path.join(OUT, "verification"), exist_ok=True)
    files = sorted(glob.glob(os.path.join(SRC, "fonts", "*.ttf")))
    if only: files = [f for f in files if any(o in f for o in only)]
    for f in files:
        print("repairing", os.path.basename(f), flush=True)
        rep = repair(f); report["fonts"][os.path.basename(f)] = rep
        print(os.path.basename(f), {k: v for k, v in rep.items() if k not in ("spacing_sample",)}, rep.get("spacing_sample"))
    json.dump(report, open(os.path.join(OUT, "verification", "repair_report.json"), "w"), indent=1, default=str)

if __name__ == "__main__":
    main()
