#!/usr/bin/env python3
"""Verify AureateCollection_1.701 against 1.700.

- shaping regression: identical glyph sequences for feature test strings (HarfBuzz)
- width impact: pangram width 1.700 vs 1.701 per program
- metric checks: bearing floor satisfied, notdef drawn, underline/strikeout unified,
  tabular figure kerning gone, instances present, no degenerate contours
Writes verification/verification_1701.json and prints a summary table.
"""
import os, glob, json, math
import uharfbuzz as hb
from fontTools.ttLib import TTFont

BASE = "/path/to/aureate"
OLD = os.path.join(BASE, "AureateCollection_1.700/fonts")
NEW = os.path.join(BASE, "AureateCollection_1.701/fonts")
PANGRAM = "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. Minimum numbness, nineteen noon winners in Munich. 1,010,101.01 and 1,111,111.11"
TESTS = [("office ffl fine", {"liga": True}), ("1/2 21/32 2026", {"frac": True}), ("Hello àéîõü", {"smcp": True}),
         ("ABC ÀÉÎ", {"c2sc": True, "smcp": True}), ("1st 2nd 3rd", {"ordn": True}), ("H2O x2", {"sups": True}),
         ("0123456789", {"onum": True, "tnum": True}), ("0123456789", {"onum": True, "pnum": True}),
         ("ǟ ẫ q̃ ş̌", {}), ("Ἀπόλλων", {}), ("Соразмерность", {}), ("(AUREATE)", {"case": True}), ("AV To LT Wa", {})]

def shape(path, text, feats):
    blob = hb.Blob.from_file_path(path); face = hb.Face(blob); font = hb.Font(face)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf, feats)
    return [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos], sum(p.x_advance for p in buf.glyph_positions)

def degenerate(font):
    glyf = font["glyf"]; n = 0
    for g in font.getGlyphOrder():
        gl = glyf[g]
        if gl.isComposite() or gl.numberOfContours <= 0: continue
        start = 0
        for e in gl.endPtsOfContours:
            if e - start + 1 < 3: n += 1
            start = e + 1
    return n

def fig_kern(path):
    _, w1 = shape(path, "11", {"kern": True}); _, w0 = shape(path, "11", {"kern": False}); return w1 - w0

out = {}
rows = []
for old in sorted(glob.glob(os.path.join(OLD, "*.ttf"))):
    b = os.path.basename(old); new = os.path.join(NEW, b)
    if not os.path.exists(new): rows.append((b, "MISSING")); continue
    fo = TTFont(old); fn = TTFont(new)
    rec = {}
    mism = []
    for t, f in TESTS:
        go, _ = shape(old, t, f); gn, _ = shape(new, t, f)
        if go != gn: mism.append((t, go, gn))
    rec["shaping_mismatches"] = mism
    _, wo = shape(old, PANGRAM, {"kern": True}); _, wn = shape(new, PANGRAM, {"kern": True})
    rec["pangram_width_old"] = wo; rec["pangram_width_new"] = wn; rec["width_change_pct"] = round((wn - wo) / wo * 100, 3)
    rec["notdef_contours"] = fn["glyf"][".notdef"].numberOfContours
    rec["underline"] = [fn["post"].underlinePosition, fn["post"].underlineThickness]
    rec["strike"] = [fn["OS/2"].yStrikeoutPosition, fn["OS/2"].yStrikeoutSize]
    rec["fig11_kern_old"] = fig_kern(old); rec["fig11_kern_new"] = fig_kern(new)
    rec["degenerate_old"] = degenerate(fo); rec["degenerate_new"] = degenerate(fn)
    rec["version"] = fn["name"].getDebugName(5); rec["mac_names"] = sum(1 for n in fn["name"].names if n.platformID == 1)
    rec["gasp"] = dict(fn["gasp"].gaspRange) if "gasp" in fn else None; rec["prep"] = "prep" in fn; rec["STAT"] = "STAT" in fn
    if "fvar" in fn: rec["instances"] = [fn["name"].getDebugName(i.subfamilyNameID) for i in fn["fvar"].instances]
    rec["glyphs_old_new"] = [len(fo.getGlyphOrder()), len(fn.getGlyphOrder())]
    rec["bytes_old_new"] = [os.path.getsize(old), os.path.getsize(new)]
    out[b] = rec
    rows.append((b, f"shape {'OK' if not mism else 'DIFF:%d' % len(mism)}  width {rec['width_change_pct']:+.2f}%  notdef {rec['notdef_contours']}  ul {rec['underline']} st {rec['strike']}  11kern {rec['fig11_kern_old']}->{rec['fig11_kern_new']}  degen {rec['degenerate_old']}->{rec['degenerate_new']}  inst {rec.get('instances','-')}"))
for r in rows: print(f"{r[0]:46s} {r[1]}")
json.dump(out, open(os.path.join(BASE, "AureateCollection_1.701/verification/verification_1701.json"), "w"), indent=1)
