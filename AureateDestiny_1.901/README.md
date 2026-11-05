# Aureate Destiny 1.901

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
| 1 | Titling space | X·φ^-2 | 343 | 343 per glyph |
| 1 | Word space | X | 898 | 898 |
| 1 | Round overshoot | C·φ^-9 | 19 | 19 above, 19 below; figures 19 / 19 |
| 1 | Bold stem | stem·φ | 166.66 | 166.0 |
| 2 half powers | Stem | X·φ^(-9/2) | 103.0 | 102.0 |
| 2 | Width of W | C | 1453 | 1453 |
| 2 | Width of C G O Q | C·φ^(-1/2) | 1142 | 1142, 1142, 1142 |
| 2 | Width of B D H K N R S T U X Y Z | C·φ^-1 = X | 898 | 898, 898, 899, 898, 899, 898, 901 |
| 2 | Width of E F J L | C·φ^(-3/2) | 706 | 706, 706, 706 |
| 3 quarter powers | Width of A M V | C·φ^(-3/4) | 1013 | 1013, 1013, 1013 |
| 3 | Width of P | C·φ^(-5/4) | 796 | 796 |
| 3 | Dot | stem·φ^(3/4) | 147.8 | 148 |
| 4 eighth powers | Bar | stem·φ^(-1/8) | 96.99 | 97.0 (arm of E), 102.0 (crossbar of H) |
| 4 | Small capital height | X·φ^(1/8) | 954 | 954 |
| 4 | Bold widths | rung·φ^(1/8) | H 954 | H 954 |

## The Apollonian solar lattice (cap height C = 1453)

The orders are ratios of ratios: the tone is a fifth less a fourth, and the sevenths divide what the
canon leaves between its terms.

| Order | Measure | Relation | Target | Built |
| --- | --- | --- | --- | --- |
| 1 octave 2:1 | Word space : titling space | C/2 : C/4 | 726 : 363 | 726 : 363 |
| 1 | Cap height : width of E F J L | 12 : 6 | 726 | 726, 727, 726 |
| 2 fifth 3:2, fourth 4:3 | Bold stem : stem | 3 : 2 | 155.68 : 103.79 | 156.0 : 104.0 |
| 2 | Dot : stem | 3 : 2 | 155.7 | 156 |
| 2 | Width of C G M O Q : narrow | 9 : 6 | 1090 | 1090, 1090, 1090, 1090 |
| 2 | Width of W : round | 12 : 9 | 1453 | 1452 |
| 2 | Small capital : capital | 2 : 3 | 969 | 969 |
| 3 tone 9:8 | Stem : bar | 9 : 8 | 103.79 : 92.25 | 104.0 : 92.0 |
| 3 | Round : width of A D H K N T U V X Y | 9 : 8 | 969 | 969, 969, 969, 969, 971, 969 |
| 4 sevenths | Width of B P R S Z | 8 : 7 under the mean class, 7 : 6 over the narrow | 848 | 849, 848, 849, 849 |
| 4 | Cap height : stem | 14 : 1 (twice seven) | 103.79 | 104.0 |
| 4 | Round overshoot | C/72 (six twelves) | 20 | 20 above, 20 below |
| 4 | Bold widths | 16 : 15 | H 1034 | H 1033 |

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

- Glyphs whose outline tangled under the correction keep the source weight: 33 in Destiny Regular,
  0 in Bold, 30 in Solar Regular, 18 in Solar Bold (of about 2,400). In Regular these are mostly
  symbols and rare letters; the reachable ones are listed in `verification/destiny_report.json`.
- 69 to 31 glyphs per program keep a small overlap where a tail or cedilla joins; it fills solid.
- Stems are whole font units, so 103.0 is built as 102.0 and 103.8 as 104.0.
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
