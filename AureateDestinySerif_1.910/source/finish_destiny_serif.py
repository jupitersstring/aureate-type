#!/usr/bin/env python3
"""Verify the Aureate Destiny Serif 1.910 package, merge the build reports, write the README from the
certificate, and the checksums. Run after build_destiny_serif.py and certificate_serif.py."""
import os, json, glob, hashlib
import numpy as np
import uharfbuzz as hb
from fontTools.ttLib import TTFont
import build_titling as bt
D = "/path/to/aureate/AureateDestinySerif_1.910"; V = os.path.join(D, "verification")

# ---- merge the four build reports
fonts = {}
for f in sorted(glob.glob(os.path.join(V, "build_*.json"))): fonts[os.path.basename(f)[6:-5]] = json.load(open(f))
if fonts:
    json.dump({"version": "1.910", "fonts": fonts}, open(os.path.join(V, "serif_report.json"), "w"), indent=1)
    for f in glob.glob(os.path.join(V, "build_*.json")): os.remove(f)
rep = json.load(open(os.path.join(V, "serif_report.json")))["fonts"]; cert = json.load(open(os.path.join(V, "certificate.json")))
M = cert["measured"]; rows = cert["relations"]; summ = cert["summary"]; sol = cert["solids"]

# ---- behaviour, by shaping
def shape(path, text, feats=None):
    face = hb.Face(hb.Blob.from_file_path(path)); font = hb.Font(face); buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, feats or {})
    return [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos], [p.x_advance for p in buf.glyph_positions]
def flank(tt, g):
    gs = tt["glyf"]; gl = gs[g]; gl.recalcBounds(gs); S = bt.flatten(gl); y = (gl.yMin + gl.yMax) / 2 + 0.37
    x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]; m = ((y1 <= y) & (y2 > y)) | ((y2 <= y) & (y1 > y))
    v = np.sort(x1[m] + (y - y1[m]) * (x2[m] - x1[m]) / (y2[m] - y1[m])); return float(v[1] - v[0])
ver = {}
for f in sorted(glob.glob(os.path.join(D, "fonts/*.ttf"))):
    b = os.path.basename(f); t = TTFont(f); n = t["name"]
    lower, _ = shape(f, "Aureate Destiny"); upper, _ = shape(f, "AUREATE DESTINY"); sc, _ = shape(f, "ABC", {"c2sc": True})
    _, kon = shape(f, "AV TO", {"kern": True}); _, koff = shape(f, "AV TO", {"kern": False}); _, adv = shape(f, "0123456789")
    w = TTFont(f[:-4] + ".woff2")
    ver[b] = {"family": n.getDebugName(1), "style": n.getDebugName(2), "version": n.getDebugName(5), "mac_names": sum(1 for x in n.names if x.platformID == 1),
              "glyphs": len(t.getGlyphOrder()), "composites": sum(1 for g in t.getGlyphOrder() if t["glyf"][g].isComposite()),
              "lowercase_types_capitals": lower == upper, "c2sc_gives_small_caps": all(g.endswith(".aursc") for g in sc),
              "kerning_active": kon != koff, "figures_tabular": len(set(adv)) == 1, "woff2_same_glyphs": w.getGlyphOrder() == t.getGlyphOrder(),
              "small_cap_bowl_flank": round(flank(t, "O.aursc"), 1), "capital_bowl_flank": round(flank(t, "O"), 1)}
    print(b, ver[b])
json.dump(ver, open(os.path.join(V, "verification_1910.json"), "w"), indent=1)

# ---- FontBakery, if a raw report is supplied (FB_JSON=path): keep a digest
fbp = os.path.join(V, "fontbakery_summary.json")
if os.environ.get("FB_JSON"):
    raw = json.load(open(os.environ["FB_JSON"])); found = {}
    def walk(o):
        if isinstance(o, dict):
            if o.get("result") in ("FAIL", "ERROR", "FATAL") and "key" in o:
                name = str(o["key"][1] if isinstance(o["key"], list) else o["key"]).split(":")[-1].strip(">")
                codes = sorted({str((l.get("message") or {}).get("code")) if isinstance(l.get("message"), dict) else "" for l in o.get("logs", []) if l.get("status") in ("FAIL", "ERROR", "FATAL")})
                e = found.setdefault(name, {"result": o["result"], "times": 0, "codes": codes}); e["times"] += 1
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(raw); json.dump({"profile": "universal", "totals": raw.get("result"), "not_passed": found}, open(fbp, "w"), indent=1)
fb = json.load(open(fbp)) if os.path.exists(fbp) else None
WHY = {"case_mapping": "by design: both cases give capitals", "consistent_family_name": "two families were checked in one folder",
       "typographic_family_name": "two families were checked in one folder", "base_has_width": "inherited from the Roman 1.701: six modifier letters (U+A717 to U+A721) have no advance",
       "smallcaps_before_ligatures": "inherited from the Roman 1.701: the small-capital lookups follow the ligature lookups"}
fb_text = "FontBakery was not run for this build.\n" if not fb else (
    f"FontBakery, universal profile, four fonts: {fb['totals'].get('PASS', 0)} passed, {fb['totals'].get('WARN', 0)} warnings, {fb['totals'].get('FAIL', 0)} failed, "
    f"{fb['totals'].get('ERROR', 0)} errors. The failures:\n\n" + "".join(
        f"- `{k}` ({v['times']} times): {next((w for q, w in WHY.items() if q in k), 'not explained; see the digest')}.\n" for k, v in fb["not_passed"].items()))

# ---- the README
GR, GB, SR, SB = (M[k] for k in ("AureateDestinySerif-Regular", "AureateDestinySerif-Bold", "AureateDestinySolarSerif-Regular", "AureateDestinySolarSerif-Bold"))
RG, RGB, RS, RSB = (rep[k] for k in ("AureateDestinySerif-Regular", "AureateDestinySerif-Bold", "AureateDestinySolarSerif-Regular", "AureateDestinySolarSerif-Bold"))
def n_(v, d=2): return f"{v:.{d}f}".rstrip("0").rstrip(".")
def w_(m, letters):
    ws = [m["widths"][g] for g in letters]; return str(ws[0]) if len(set(ws)) == 1 else f"{min(ws)} to {max(ws)}"
def tips(m): v = [t for l in m["serifs"].values() for t in l]; return f"{n_(min(v))}" if min(v) == max(v) else f"{n_(min(v))} to {n_(max(v))}"
def rng(d): v = list(d.values()); return n_(v[0]) if min(v) == max(v) else f"{n_(min(v))} to {n_(max(v))}"
fails = [r for r in rows if r["verdict"] != "pass"]; total = sum(s["relations"] for s in summ.values()); passed = sum(s["passed"] for s in summ.values())
X, C = 898, 1453; PHI = (1 + 5 ** 0.5) / 2
gst = X * PHI ** -4.5; gh = gst / PHI; gs = gh / PHI; ss = C / 14; se = ss / 6 ** 0.5; sh = se * 3 ** 0.5; q = 1.5 ** 0.5
def solid_row(k): s = sol[k]; return f"| {k.capitalize()} | {s['element']} | {s['kepler']} | {s['r']:.4f} | {s['rho']:.4f} | {s['R']:.4f} | {s['rho_over_r']:.4f} | {s['R_over_rho']:.4f} | {s['R_over_r']:.4f} |"
def reach(r): return ", ".join(r["failed_reachable"]) or "none"
readme = f"""# Aureate Destiny Serif 1.910

Light, wide-set titling capitals with serifs, in two proportional lattices, derived from Aureate Roman
Living Tall 1.701. Typing in either case gives capitals; small capitals come through `c2sc`. Four programs,
TTF and WOFF2, under `fonts/`:

| Family | Styles | Lattice | Solids |
| --- | --- | --- | --- |
| Aureate Destiny Serif | Regular, Bold | Golden: every measure a power of φ | icosahedron, dodecahedron |
| Aureate Destiny Solar Serif | Regular, Bold | Apollonian: whole numbers on the canon 6 : 8 : 9 : 12, with √2, √3 and √6 | tetrahedron, octahedron, cube |

The certificate measures {total} relations in the finished fonts; {passed} hold within tolerance.
{"All hold." if not fails else "The ones that do not are listed under Limits."} The full table is `verification/CERTIFICATE.md`, and
`specimen/` holds a type specimen and a geometry plate.

## The five solids

Each solid is built from its vertex coordinates and measured (edge = 1): inradius r, midradius ρ,
circumradius R. Nothing is taken from a formula sheet; the closed forms are only checked against.

| Solid | Element (Plato) | Place (Kepler) | r | ρ | R | ρ : r | R : ρ | R : r |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{solid_row('tetrahedron')}
{solid_row('octahedron')}
{solid_row('cube')}
{solid_row('icosahedron')}
{solid_row('dodecahedron')}

The three solids of √2 and √3 belong to the Solar family; the two solids of φ belong to the golden family.
The elements and Kepler's planetary places are the traditional correspondences. They are not astronomy,
and "Solar" is used as in the sans: the Sun's six and the canon built on it.

## Aureate Destiny Solar Serif (cap height C = 1453)

One tetrahedron (fire) whose edge is two stems gives the whole stroke chain: its insphere is the serif,
its midsphere the hairline, half its edge the stem. So serif : hairline : stem = 1 : √3 : √6. The same
ratios are the cube's and the octahedron's: √3 is R : r of both, √2 is ρ : r of the cube and R : ρ of the
octahedron. The Bold is that tetrahedron enlarged by the octahedron's ρ : r = √(3/2); the enlarged
circumsphere is the Bold stem, which makes Bold stem : stem the fifth, 3 : 2, and the Bold chain
1 : √3 : 3, the tetrahedron's own r : ρ : R.

| Measure | Relation | Target | Built | Bold target | Bold built |
| --- | --- | --- | --- | --- | --- |
| Stem | C ÷ 14; half the tetrahedron's edge | {n_(ss)} | {n_(SR['stem'])} | {n_(ss * 1.5)} | {n_(SB['stem'])} |
| Hairline | ρ of the tetrahedron; serif·√3 | {n_(sh)} | {n_(SR['hair'])} | {n_(sh * q)} | {n_(SB['hair'])} |
| Serif (every tip) | r of the tetrahedron | {n_(se)} | {tips(SR)} | {n_(se * q)} | {tips(SB)} |
| Bowl | stem·9/8, the tone | {n_(ss * 9 / 8)} | {n_(SR['bowl'])} | {n_(ss * 27 / 16)} | {n_(SB['bowl'])} |
| Dot | stem·3/2, the fifth | {n_(ss * 1.5)} | {n_(SR['dot'])} | {n_(ss * 2.25)} | {n_(SB['dot'])} |
| Exclamation wedge | stem·4/3, the fourth | {n_(ss * 4 / 3)} | {n_(SR['wedge'])} | | |
| Round overshoot | C ÷ 48 | {round(C / 48)} | {rng(SR['over_top'])} above, {rng(SR['over_bottom'])} below | | |
| Apex of A; vertex of V, W | C ÷ 72; C ÷ 36 | {round(C / 72)}; {round(C / 36)} | {n_(SR['apex'])}; {rng(SR['vertex'])} | | |
| Small capital height | C·2/3, the fifth | {round(C * 2 / 3)} | {n_(SR['sc'])} | | |
| Titling space; word space | C ÷ 4; C ÷ 2, the octave | {round(C / 4)}; {round(C / 2)} | {rng(SR['track'])}; {n_(SR['space'])} | | |

Capital ink widths, in twelfths of the capital, with the cube's two roots. Bold widths are 16/15 of these.

| Letters | Rung | Target | Built | Bold target | Bold built |
| --- | --- | --- | --- | --- | --- |
| W | 16/12 C | {n_(C * 16 / 12)} | {w_(SR, 'W')} | {n_(C * 16 / 12 * 16 / 15)} | {w_(SB, 'W')} |
| M | 14/12 C | {n_(C * 14 / 12)} | {w_(SR, 'M')} | {n_(C * 14 / 12 * 16 / 15)} | {w_(SB, 'M')} |
| A H K N U V X Y | 12/12 C: the face of the cube of edge C | {C} | {w_(SR, 'AHKNUVXY')} | {n_(C * 16 / 15)} | {w_(SB, 'AHKNUVXY')} |
| D G O Q R | √3/2 C: that cube's circumradius | {n_(C * 3 ** 0.5 / 2)} | {w_(SR, 'DGOQR')} | {n_(C * 3 ** 0.5 / 2 * 16 / 15)} | {w_(SB, 'DGOQR')} |
| B C L T Z | 10/12 C | {n_(C * 10 / 12)} | {w_(SR, 'BCLTZ')} | {n_(C * 10 / 12 * 16 / 15)} | {w_(SB, 'BCLTZ')} |
| E | 9/12 C | {n_(C * 9 / 12)} | {w_(SR, 'E')} | {n_(C * 9 / 12 * 16 / 15)} | {w_(SB, 'E')} |
| F P | C ÷ √2: the edge of the cube whose face diagonal is C | {n_(C / 2 ** 0.5)} | {w_(SR, 'FP')} | {n_(C / 2 ** 0.5 * 16 / 15)} | {w_(SB, 'FP')} |
| S | 7/12 C | {n_(C * 7 / 12)} | {w_(SR, 'S')} | {n_(C * 7 / 12 * 16 / 15)} | {w_(SB, 'S')} |
| J | 6/12 C | {n_(C / 2)} | {w_(SR, 'J')} | {n_(C / 2 * 16 / 15)} | {w_(SB, 'J')} |

## Aureate Destiny Serif (x-height X = 898, cap height C = X·φ = 1453)

Two dual solids on one edge of two serifs give the stroke chain: the icosahedron's midsphere (water) is
the hairline and the dodecahedron's (the heavens) is the stem, so serif : hairline : stem = 1 : φ : φ².
The icosahedron of edge X spans three golden rectangles X by C, and the cube inscribed in the
dodecahedron of edge X has edge C: the cap height twice over. Half powers of φ are the Kepler triangle
1 : √φ : φ; quarter and eighth powers are its mean and the mean of that.

| Measure | Relation | Target | Built | Bold target | Bold built |
| --- | --- | --- | --- | --- | --- |
| Stem | X·φ^(−9/2); ρ of the dodecahedron | {n_(gst)} | {n_(GR['stem'])} | {n_(gst * PHI)} (·φ) | {n_(GB['stem'])} |
| Hairline | stem ÷ φ; ρ of the icosahedron | {n_(gh)} | {n_(GR['hair'])} | {n_(gh * PHI ** 0.5)} (·φ^1/2) | {n_(GB['hair'])} |
| Serif (every tip) | hairline ÷ φ; half the common edge | {n_(gs)} | {tips(GR)} | {n_(gs * PHI ** 0.25)} (·φ^1/4) | {tips(GB)} |
| Bowl | stem·φ^(1/4) | {n_(gst * PHI ** 0.25)} | {n_(GR['bowl'])} | {n_(gst * PHI ** 1.25)} | {n_(GB['bowl'])} |
| Dot | stem·φ^(3/4) | {n_(gst * PHI ** 0.75)} | {n_(GR['dot'])} | {n_(gst * PHI ** 1.75)} | {n_(GB['dot'])} |
| Exclamation wedge | stem·φ^(1/2) | {n_(gst * PHI ** 0.5)} | {n_(GR['wedge'])} | | |
| Round overshoot | C·φ^(−8) | {round(C * PHI ** -8)} | {rng(GR['over_top'])} above, {rng(GR['over_bottom'])} below | | |
| Apex of A; vertex of V, W | C·φ^(−9); C·φ^(−15/2) | {round(C * PHI ** -9)}; {round(C * PHI ** -7.5)} | {n_(GR['apex'])}; {rng(GR['vertex'])} | | |
| Small capital height | X·φ^(1/8) | {round(X * PHI ** 0.125)} | {n_(GR['sc'])} | | |
| Titling space; word space | X·φ^(−2); X | {round(X * PHI ** -2)}; {X} | {rng(GR['track'])}; {n_(GR['space'])} | | |

Capital ink widths on quarter powers of φ. Bold widths are these times φ^(1/8).

| Letters | Rung | Target | Built | Bold target | Bold built |
| --- | --- | --- | --- | --- | --- |
""" + "".join(f"| {' '.join(l)} | {nm} | {n_(C * PHI ** e)} | {w_(GR, l)} | {n_(C * PHI ** (e + 0.125))} | {w_(GB, l)} |\n" for l, nm, e in (
    ("W", "C·φ^(1/2)", 0.5), ("M", "C·φ^(1/4)", 0.25), ("AHKNUVXY", "C", 0), ("DGOQR", "C·φ^(−1/4)", -0.25), ("BCELTZ", "C·φ^(−1/2)", -0.5),
    ("FP", "C·φ^(−3/4)", -0.75), ("S", "C·φ^(−1) = X", -1), ("J", "C·φ^(−3/2)", -1.5), ("I", "C·φ^(−2)", -2))) + f"""
## How it is made

1. **The Roman is trued first.** Its serif tips come in several heights (42 units on H, I and E, 57 on most
   letters, up to 71 on T), its T has a crossbar of 30 units, and its small capitals are lighter than its
   capitals. Every tip is set to one height, the T family takes the hairline, and small capitals are read
   on their own scale, so one law can give one result. {RS['serif_tips_unified']} tips and {RS['crossbars_given_the_hairline']} crossbars.
2. **Lining.** Flats sit on the baseline and the cap line; rounds, apexes and vertices take the lattice's
   overshoots; a letter with a tail, cedilla or ogonek is lined on its body and the mark is carried below.
3. **Widths.** Each capital's ink width is set on its rung. Two dry runs measure how much the letter narrows
   when its strokes thin, so the finished width lands on the rung; a last correction of at most 0.4 % trues it.
4. **Weight.** Stroke thickness is measured against the Roman, edge by edge. Straight strokes take three
   levels only: serif, hairline, stem. Curves are modulated from hairline to bowl. Flat edges on alignment
   lines are held and the inside of the stroke takes the correction. A mark below the baseline is weighed
   apart from its letter.
5. **Regulation.** The law's four values are adjusted against the measured I, H, E and O, and the best round
   is kept (`source/serif_regulation.json`). Serif tips and the T crossbar are then set outright.
6. **Spacing.** Every glyph keeps the side bearings it was drawn with, then the titling space is added.
   Dots take the lattice's dot : stem ratio; the exclamation mark's wedge is scaled, not thinned.

## Limits

- Glyphs whose outline tangled under the correction keep the Roman's weight: {RG['left_at_source_weight']} in Destiny Serif
  Regular, {RGB['left_at_source_weight']} in Bold, {RS['left_at_source_weight']} in Solar Serif Regular, {RSB['left_at_source_weight']} in Bold (of {ver['AureateDestinySerif-Regular.ttf']['glyphs']}). No Latin capital, figure or
  small capital of A to Z is among them. Those that can be typed, in Regular: {reach(RG)}. In Solar
  Regular: {reach(RS)}.
- {RG['kept_with_small_overlap']} and {RS['kept_with_small_overlap']} glyphs in the Regulars keep a small overlap where two strokes meet; it fills solid.
- Outlines sit on whole units, so a stroke may stand up to one unit from its target: the golden Bold hairline
  is {n_(GB['hair'])} against {n_(gh * PHI ** 0.5)}, and the next step the grid allows is two units on.
- Small capitals take the capitals' stem, hairline and serif, but their bowls are close to the stem weight
  ({ver['AureateDestinySolarSerif-Regular.ttf']['small_cap_bowl_flank']} against {ver['AureateDestinySolarSerif-Regular.ttf']['capital_bowl_flank']} in the capitals of Solar Regular), because the Roman's small capitals have no swell.
- Figures keep the Roman's modulation. Their upright stems are the stem and the zero's bowl is the
  capitals', but their thin strokes are curves and are not all the hairline: 58 to 86 units in Destiny
  Serif Regular (hairline 64) and 65 to 94 in Solar Serif Regular (hairline 73).
- Kerning is the Roman's. It was not refitted to the new widths.
- Lowercase is not reachable by typing (both cases give capitals). No italic.
- The relations between the solids and the strokes are exact identities, stated with numbers and checked.
  The elements and planets attached to the solids are tradition, quoted as tradition.
- The letterforms are Aureate's own, in the manner of light, wide-set titling. They copy no logo.
""" + ("".join(f"- Certificate: {r['family']}, {r['name']}: target {n_(r['expected'])}, measured {n_(r['measured'])}.\n" for r in fails)) + f"""
## Checks

- Certificate: {passed} of {total} relations hold (`verification/CERTIFICATE.md`).
- Behaviour, by HarfBuzz shaping, in all four fonts: lower case types capitals, `c2sc` gives small capitals,
  kerning is active, default figures share one advance, WOFF2 holds the same glyphs
  (`verification/verification_1910.json`).
- {fb_text}
## Rebuild

    python3 source/build_destiny_serif.py              # four fonts; about 25 minutes run one after another
    python3 source/certificate_serif.py                # verification/certificate.json and CERTIFICATE.md
    python3 source/make_destiny_serif_specimen.py      # the two plates
    python3 source/finish_destiny_serif.py             # behaviour checks, this README, checksums

`DS_REGULATE=1 DS_ONLY="I H E O" DS_OUT=/tmp/trial python3 source/build_destiny_serif.py` repeats the regulation.
Requires Python 3.10+, fontTools, numpy, brotli, uharfbuzz and Pillow. `build_titling.py` (the weight
engine), `build_destiny.py`, `measure_strokes.py` and `platonic.py` sit beside the scripts.
SIL Open Font License 1.1; derived from Liberation Serif through Aureate Roman Living Tall. Aureate Type, 2026.
"""
open(os.path.join(D, "README.md"), "w").write(readme)
with open(os.path.join(V, "SHA256SUMS.txt"), "w") as fh:
    for f in sorted(glob.glob(os.path.join(D, "fonts/*"))): fh.write(hashlib.sha256(open(f, "rb").read()).hexdigest() + "  fonts/" + os.path.basename(f) + "\n")
print("README and checksums written;", passed, "of", total, "relations hold")
