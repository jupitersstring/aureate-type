# Aureate Destiny Serif 1.910

Light, wide-set titling capitals with serifs, in two proportional lattices, derived from Aureate Roman
Living Tall 1.701. Typing in either case gives capitals; small capitals come through `c2sc`. Four programs,
TTF and WOFF2, under `fonts/`:

| Family | Styles | Lattice | Solids |
| --- | --- | --- | --- |
| Aureate Destiny Serif | Regular, Bold | Golden: every measure a power of φ | icosahedron, dodecahedron |
| Aureate Destiny Solar Serif | Regular, Bold | Apollonian: whole numbers on the canon 6 : 8 : 9 : 12, with √2, √3 and √6 | tetrahedron, octahedron, cube |

The certificate measures 498 relations in the finished fonts; 498 hold within tolerance.
All hold. The full table is `verification/CERTIFICATE.md`, and
`specimen/` holds a type specimen and a geometry plate.

## The five solids

Each solid is built from its vertex coordinates and measured (edge = 1): inradius r, midradius ρ,
circumradius R. Nothing is taken from a formula sheet; the closed forms are only checked against.

| Solid | Element (Plato) | Place (Kepler) | r | ρ | R | ρ : r | R : ρ | R : r |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tetrahedron | fire | between Jupiter and Mars | 0.2041 | 0.3536 | 0.6124 | 1.7321 | 1.7321 | 3.0000 |
| Octahedron | air | between Venus and Mercury | 0.4082 | 0.5000 | 0.7071 | 1.2247 | 1.4142 | 1.7321 |
| Cube | earth | between Saturn and Jupiter | 0.5000 | 0.7071 | 0.8660 | 1.4142 | 1.2247 | 1.7321 |
| Icosahedron | water | between Earth and Venus | 0.7558 | 0.8090 | 0.9511 | 1.0705 | 1.1756 | 1.2584 |
| Dodecahedron | the heavens (aether) | between Mars and Earth | 1.1135 | 1.3090 | 1.4013 | 1.1756 | 1.0705 | 1.2584 |

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
| Stem | C ÷ 14; half the tetrahedron's edge | 103.79 | 104 | 155.68 | 156 |
| Hairline | ρ of the tetrahedron; serif·√3 | 73.39 | 74 | 89.88 | 90 |
| Serif (every tip) | r of the tetrahedron | 42.37 | 42 | 51.89 | 52 |
| Bowl | stem·9/8, the tone | 116.76 | 117.14 | 175.14 | 174.94 |
| Dot | stem·3/2, the fifth | 155.68 | 156 | 233.52 | 234 |
| Exclamation wedge | stem·4/3, the fourth | 138.38 | 138 | | |
| Round overshoot | C ÷ 48 | 30 | 30 above, 30 below | | |
| Apex of A; vertex of V, W | C ÷ 72; C ÷ 36 | 20; 40 | 20; 40 | | |
| Small capital height | C·2/3, the fifth | 969 | 969 | | |
| Titling space; word space | C ÷ 4; C ÷ 2, the octave | 363; 726 | 363; 726 | | |

Capital ink widths, in twelfths of the capital, with the cube's two roots. Bold widths are 16/15 of these.

| Letters | Rung | Target | Built | Bold target | Bold built |
| --- | --- | --- | --- | --- | --- |
| W | 16/12 C | 1937.33 | 1937 | 2066.49 | 2066 |
| M | 14/12 C | 1695.17 | 1695 | 1808.18 | 1808 |
| A H K N U V X Y | 12/12 C: the face of the cube of edge C | 1453 | 1453 | 1549.87 | 1550 |
| D G O Q R | √3/2 C: that cube's circumradius | 1258.33 | 1258 | 1342.22 | 1342 |
| B C L T Z | 10/12 C | 1210.83 | 1211 | 1291.56 | 1291 to 1292 |
| E | 9/12 C | 1089.75 | 1090 | 1162.4 | 1162 |
| F P | C ÷ √2: the edge of the cube whose face diagonal is C | 1027.43 | 1027 | 1095.92 | 1096 |
| S | 7/12 C | 847.58 | 847 | 904.09 | 904 |
| J | 6/12 C | 726.5 | 727 | 774.93 | 775 |

## Aureate Destiny Serif (x-height X = 898, cap height C = X·φ = 1453)

Two dual solids on one edge of two serifs give the stroke chain: the icosahedron's midsphere (water) is
the hairline and the dodecahedron's (the heavens) is the stem, so serif : hairline : stem = 1 : φ : φ².
The icosahedron of edge X spans three golden rectangles X by C, and the cube inscribed in the
dodecahedron of edge X has edge C: the cap height twice over. Half powers of φ are the Kepler triangle
1 : √φ : φ; quarter and eighth powers are its mean and the mean of that.

| Measure | Relation | Target | Built | Bold target | Bold built |
| --- | --- | --- | --- | --- | --- |
| Stem | X·φ^(−9/2); ρ of the dodecahedron | 103 | 103 | 166.66 (·φ) | 167 |
| Hairline | stem ÷ φ; ρ of the icosahedron | 63.66 | 64 | 80.97 (·φ^1/2) | 80 |
| Serif (every tip) | hairline ÷ φ; half the common edge | 39.34 | 39 | 44.37 (·φ^1/4) | 44 |
| Bowl | stem·φ^(1/4) | 116.17 | 116.17 | 187.96 | 187.95 |
| Dot | stem·φ^(3/4) | 147.77 | 148 | 239.09 | 240 |
| Exclamation wedge | stem·φ^(1/2) | 131.02 | 132 | | |
| Round overshoot | C·φ^(−8) | 31 | 31 above, 31 below | | |
| Apex of A; vertex of V, W | C·φ^(−9); C·φ^(−15/2) | 19; 39 | 19; 39 | | |
| Small capital height | X·φ^(1/8) | 954 | 954 | | |
| Titling space; word space | X·φ^(−2); X | 343; 898 | 343; 898 | | |

Capital ink widths on quarter powers of φ. Bold widths are these times φ^(1/8).

| Letters | Rung | Target | Built | Bold target | Bold built |
| --- | --- | --- | --- | --- | --- |
| W | C·φ^(1/2) | 1848.24 | 1848 | 1962.83 | 1963 |
| M | C·φ^(1/4) | 1638.75 | 1639 | 1740.35 | 1740 |
| A H K N U V X Y | C | 1453 | 1453 | 1543.08 | 1543 |
| D G O Q R | C·φ^(−1/4) | 1288.31 | 1288 | 1368.18 | 1368 |
| B C E L T Z | C·φ^(−1/2) | 1142.28 | 1142 | 1213.1 | 1213 |
| F P | C·φ^(−3/4) | 1012.8 | 1013 | 1075.59 | 1076 |
| S | C·φ^(−1) = X | 898 | 898 | 953.68 | 954 |
| J | C·φ^(−3/2) | 705.97 | 706 | 749.73 | 750 |
| I | C·φ^(−2) | 555 | 555 | 589.4 | 589 |

## How it is made

1. **The Roman is trued first.** Its serif tips come in several heights (42 units on H, I and E, 57 on most
   letters, up to 71 on T), its T has a crossbar of 30 units, and its small capitals are lighter than its
   capitals. Every tip is set to one height, the T family takes the hairline, and small capitals are read
   on their own scale, so one law can give one result. 3582 tips and 19 crossbars.
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

- Glyphs whose outline tangled under the correction keep the Roman's weight: 62 in Destiny Serif
  Regular, 0 in Bold, 55 in Solar Serif Regular, 30 in Bold (of 3397). No Latin capital, figure or
  small capital of A to Z is among them. Those that can be typed, in Regular: alef, yod, tsadi, shin, vavyod, yodyod, integraltp, integralbt, male, uni2669, musicalnote, uniFB1D, yodyod_patah, alefwide, shinshindot, shinsindot, shindageshshindot, shindageshsindot, alefmapiq, yoddagesh, tsadidagesh, shindagesh, aleflamed, uni01B7.aursc, uni01B8.aursc, uni01EE.aursc, uni04E0.aursc. In Solar
  Regular: yod, tsadi, shin, yodyod, integraltp, integralbt, uni2669, musicalnote, yodyod_patah, shinshindot, shinsindot, shindageshshindot, shindageshsindot, yoddagesh, tsadidagesh, shindagesh, aleflamed, uni01B7.aursc, uni01B8.aursc, uni01EE.aursc, uni04E0.aursc.
- 163 and 126 glyphs in the Regulars keep a small overlap where two strokes meet; it fills solid.
- Outlines sit on whole units, so a stroke may stand up to one unit from its target: the golden Bold hairline
  is 80 against 80.97, and the next step the grid allows is two units on.
- Small capitals take the capitals' stem, hairline and serif, but their bowls are close to the stem weight
  (104.7 against 118.4 in the capitals of Solar Regular), because the Roman's small capitals have no swell.
- Figures keep the Roman's modulation. Their upright stems are the stem and the zero's bowl is the
  capitals', but their thin strokes are curves and are not all the hairline: 58 to 86 units in Destiny
  Serif Regular (hairline 64) and 65 to 94 in Solar Serif Regular (hairline 73).
- Kerning is the Roman's. It was not refitted to the new widths.
- Lowercase is not reachable by typing (both cases give capitals). No italic.
- The relations between the solids and the strokes are exact identities, stated with numbers and checked.
  The elements and planets attached to the solids are tradition, quoted as tradition.
- The letterforms are Aureate's own, in the manner of light, wide-set titling. They copy no logo.

## Checks

- Certificate: 498 of 498 relations hold (`verification/CERTIFICATE.md`).
- Behaviour, by HarfBuzz shaping, in all four fonts: lower case types capitals, `c2sc` gives small capitals,
  kerning is active, default figures share one advance, WOFF2 holds the same glyphs
  (`verification/verification_1910.json`).
- FontBakery, universal profile, four fonts: 271 passed, 37 warnings, 14 failed, 0 errors. The failures:

- `opentype/family/consistent_family_name` (1 times): two families were checked in one folder.
- `base_has_width` (4 times): inherited from the Roman 1.701: six modifier letters (U+A717 to U+A721) have no advance.
- `case_mapping` (4 times): by design: both cases give capitals.
- `smallcaps_before_ligatures` (4 times): inherited from the Roman 1.701: the small-capital lookups follow the ligature lookups.
- `typographic_family_name` (1 times): two families were checked in one folder.

## Rebuild

    python3 source/build_destiny_serif.py              # four fonts; about 25 minutes run one after another
    python3 source/certificate_serif.py                # verification/certificate.json and CERTIFICATE.md
    python3 source/make_destiny_serif_specimen.py      # the two plates
    python3 source/finish_destiny_serif.py             # behaviour checks, this README, checksums

`DS_REGULATE=1 DS_ONLY="I H E O" DS_OUT=/tmp/trial python3 source/build_destiny_serif.py` repeats the regulation.
Requires Python 3.10+, fontTools, numpy, brotli, uharfbuzz and Pillow. `build_titling.py` (the weight
engine), `build_destiny.py`, `measure_strokes.py` and `platonic.py` sit beside the scripts.
SIL Open Font License 1.1; derived from Liberation Serif through Aureate Roman Living Tall. Aureate Type, 2026.
