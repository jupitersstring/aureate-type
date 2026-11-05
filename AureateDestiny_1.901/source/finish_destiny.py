#!/usr/bin/env python3
"""Verify the Aureate Destiny 1.901 package, write its README from the measured report, and checksums."""
import os, json, glob, hashlib
import uharfbuzz as hb
from fontTools.ttLib import TTFont
D = "/path/to/aureate/AureateDestiny_1.901"
rep = json.load(open(os.path.join(D, "verification/destiny_report.json")))["fonts"]

def shape(path, text, feats=None):
    face = hb.Face(hb.Blob.from_file_path(path)); font = hb.Font(face); buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, feats or {})
    return [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos], [p.x_advance for p in buf.glyph_positions]

ver = {}
for f in sorted(glob.glob(os.path.join(D, "fonts/*.ttf"))):
    b = os.path.basename(f); t = TTFont(f); n = t["name"]
    lower, _ = shape(f, "Aureate Destiny"); upper, _ = shape(f, "AUREATE DESTINY")
    sc, _ = shape(f, "ABC", {"c2sc": True})
    _, kern_on = shape(f, "AV TO", {"kern": True}); _, kern_off = shape(f, "AV TO", {"kern": False})
    figs, adv = shape(f, "0123456789")
    ver[b] = {"family": n.getDebugName(1), "style": n.getDebugName(2), "version": n.getDebugName(5), "mac_names": sum(1 for x in n.names if x.platformID == 1),
              "glyphs": len(t.getGlyphOrder()), "lowercase_types_capitals": lower == upper, "c2sc_gives_small_caps": all(g.endswith(".s") for g in sc),
              "kerning_active": kern_on != kern_off, "figures_tabular": len(set(adv)) == 1}
    print(b, ver[b])
json.dump(ver, open(os.path.join(D, "verification/verification_1901.json"), "w"), indent=1)

def cls(r):
    out = {}
    for g, nm in r["width_rungs"].items(): out.setdefault(nm.replace(" (as O)", ""), []).append(g)
    return {k: " ".join(sorted(v)) for k, v in out.items()}
RG, RGB = rep["AureateDestiny-Regular"], rep["AureateDestiny-Bold"]; RS, RSB = rep["AureateDestinySolar-Regular"], rep["AureateDestinySolar-Bold"]
mg, ms, cg, cs = RG["measured"], RS["measured"], cls(RG), cls(RS)
def w(m, *ks): return ", ".join(str(m["widths"][k]) for k in ks)
readme = f"""# Aureate Destiny 1.901

A light, wide-set titling sans in two proportional lattices, derived from Aureate Sans Geometric 1.701.
Typing in either case gives capitals; small capitals are available through `c2sc`. Four programs in TTF
and WOFF2 under `fonts/`:

| Family | Styles | Lattice |
| --- | --- | --- |
| Aureate Destiny | Regular, Bold | Golden: every measure a power of φ |
| Aureate Destiny Solar | Regular, Bold | Apollonian: whole numbers on the Sun's six and the lyre canon 6 : 8 : 9 : 12 |

"Solar" is used in the traditional sense: six as the number of the Sun, the canon 6 : 8 : 9 : 12 built on
it (the fixed strings of the lyre), and Apollo's seven. It is a modern typographic interpretation in the
manner of the Apollonian Harmonic page edition, not astronomy.

## The golden lattice (x-height X = 898)

The orders are nested roots: a half power is the geometric mean of a whole step, a quarter power the mean
of that mean, an eighth power the mean again.

| Order | Measure | Relation | Target | Built |
| --- | --- | --- | --- | --- |
| 1 whole powers | Cap height | X·φ | 1453 | 1453 |
| 1 | Titling space | X·φ^-2 | {RG['targets']['track']} | {RG['targets']['track']} per glyph |
| 1 | Word space | X | 898 | {mg['space']} |
| 1 | Round overshoot | C·φ^-9 | {RG['targets']['overshoot']} | {mg['O'][1]-1453} above, {-mg['O'][0]} below; figures {mg['zero'][1]-1453} / {-mg['zero'][0]} |
| 1 | Bold stem | stem·φ | {RGB['targets']['stem']} | {RGB['measured']['stem_I']} |
| 2 half powers | Stem | X·φ^(-9/2) | {RG['targets']['stem']} | {mg['stem_I']} |
| 2 | Width of W | C | 1453 | {w(mg,'W')} |
| 2 | Width of {cg.get('C·φ^-1/2','')} | C·φ^(-1/2) | 1142 | {w(mg,'O','C','G')} |
| 2 | Width of {cg.get('C·φ^-1 = X','')} | C·φ^-1 = X | 898 | {w(mg,'H','N','D','T','B','R','S')} |
| 2 | Width of {cg.get('C·φ^-3/2','')} | C·φ^(-3/2) | 706 | {w(mg,'E','F','L')} |
| 3 quarter powers | Width of {cg.get('C·φ^-3/4','')} | C·φ^(-3/4) | 1013 | {w(mg,'A','M','V')} |
| 3 | Width of {cg.get('C·φ^-5/4','')} | C·φ^(-5/4) | 796 | {w(mg,'P')} |
| 3 | Dot | stem·φ^(3/4) | {RG['targets']['dot']} | {mg['dot']} |
| 4 eighth powers | Bar | stem·φ^(-1/8) | {RG['targets']['bar']} | {mg['bar_E']} (arm of E), {mg['bar_H']} (crossbar of H) |
| 4 | Small capital height | X·φ^(1/8) | 954 | {mg['H_sc_top']} |
| 4 | Bold widths | rung·φ^(1/8) | H 954 | H {RGB['measured']['widths']['H']} |

## The Apollonian solar lattice (cap height C = 1453)

The orders are ratios of ratios: the tone is a fifth less a fourth, and the sevenths divide what the
canon leaves between its terms.

| Order | Measure | Relation | Target | Built |
| --- | --- | --- | --- | --- |
| 1 octave 2:1 | Word space : titling space | C/2 : C/4 | 726 : 363 | {ms['space']} : {RS['targets']['track']} |
| 1 | Cap height : width of {cs.get('6/12 C','')} | 12 : 6 | 726 | {w(ms,'E','F','L')} |
| 2 fifth 3:2, fourth 4:3 | Bold stem : stem | 3 : 2 | {RSB['targets']['stem']} : {RS['targets']['stem']} | {RSB['measured']['stem_I']} : {ms['stem_I']} |
| 2 | Dot : stem | 3 : 2 | {RS['targets']['dot']} | {ms['dot']} |
| 2 | Width of {cs.get('9/12 C','')} : narrow | 9 : 6 | 1090 | {w(ms,'O','C','G','M')} |
| 2 | Width of W : round | 12 : 9 | 1453 | {w(ms,'W')} |
| 2 | Small capital : capital | 2 : 3 | 969 | {ms['H_sc_top']} |
| 3 tone 9:8 | Stem : bar | 9 : 8 | {RS['targets']['stem']} : {RS['targets']['bar']} | {ms['stem_I']} : {ms['bar_E']} |
| 3 | Round : width of {cs.get('8/12 C','')} | 9 : 8 | 969 | {w(ms,'H','N','A','V','D','T')} |
| 4 sevenths | Width of {cs.get('7/12 C','')} | 8 : 7 under the mean class, 7 : 6 over the narrow | 848 | {w(ms,'B','R','S','P')} |
| 4 | Cap height : stem | 14 : 1 (twice seven) | {RS['targets']['stem']} | {ms['stem_I']} |
| 4 | Round overshoot | C/72 (six twelves) | {RS['targets']['overshoot']} | {ms['O'][1]-1453} above, {-ms['O'][0]} below |
| 4 | Bold widths | 16 : 15 | H {round(969*16/15)} | H {RSB['measured']['widths']['H']} |

## How it is made

1. **Lining.** Flats sit on 0 and C; every round overshoots by the lattice's amount; figures take the
   capital lines; small capitals take the lattice's height.
2. **Widths.** Each capital's ink width is set on a rung. A dry run first measures how much the letter
   narrows when its strokes thin, so the finished width lands on the rung. In the solar lattice, letters
   that belong together share a rung (H N U; A V; B P R S).
3. **Weight.** One law: every stroke side moves in by the same amount for its orientation, so stems land
   on the stem target and bars on the bar target. Flat edges on alignment lines are pinned and the inside
   of the stroke takes the whole correction; the outsides of bowls hold at their extremes.
4. **Dots and short bars** are scaled to the lattice's dot : stem ratio or thinned as bars.
5. **Spacing.** Titling space is added to every advancing glyph; kerning is kept.

## Limits

- Glyphs whose outline tangled under the correction keep the source weight: {RG['left_at_source_weight']} in Destiny Regular,
  {RGB['left_at_source_weight']} in Bold, {RS['left_at_source_weight']} in Solar Regular, {RSB['left_at_source_weight']} in Solar Bold (of about 2,400). In Regular these are mostly
  symbols and rare letters; the reachable ones are listed in `verification/destiny_report.json`.
- {RG['kept_with_small_overlap']} to {RSB['kept_with_small_overlap']} glyphs per program keep a small overlap where a tail or cedilla joins; it fills solid.
- Stems are whole font units, so 103.0 is built as {mg['stem_I']} and 103.8 as {ms['stem_I']}.
- The crossbar of H is a unit or two thicker than the arms of E, because a bar with space on both sides
  is corrected from both sides.
- Lowercase is not reachable by typing (both cases give capitals). No italic.
- The letterforms are Aureate's own; this is in the manner of light, wide-set game-title lettering, not a
  copy of any.

## Changes in 1.901

1.900 took a cedilla, ogonek, comma accent or tail for the bottom of the letter and pressed the whole glyph
between the baseline and the cap line: Ç, Ş, Ţ, Ą, Ę, Ģ, Ķ, Ļ, Ņ, Ŗ, Q and the other descending capitals
(about a hundred glyphs with their small capitals) came out short, with the mark squeezed above the
baseline. In 1.901 the body is lined on its own (baseline or overshoot to cap line) and the mark is carried
below it at its drawn depth. A mark that hangs below the baseline is also weighed separately from its
letter. Every lattice measure in the tables above is unchanged from 1.900.

## Rebuild

    python3 source/build_destiny.py            # about 15 minutes; fonts/ and verification/destiny_report.json
    python3 source/make_destiny_specimen.py
    python3 source/finish_destiny.py           # verification, this README, checksums

Requires Python 3.10+, fontTools, numpy, brotli, uharfbuzz and Pillow, and `build_titling.py` beside the
scripts (the weight engine). SIL Open Font License 1.1; derived from Source Sans 3 through Aureate Sans
Geometric. Aureate Type, 2026.
"""
open(os.path.join(D, "README.md"), "w").write(readme)
with open(os.path.join(D, "verification/SHA256SUMS.txt"), "w") as fh:
    for f in sorted(glob.glob(os.path.join(D, "fonts/*"))):
        fh.write(hashlib.sha256(open(f, "rb").read()).hexdigest() + "  fonts/" + os.path.basename(f) + "\n")
print("README and checksums written")
