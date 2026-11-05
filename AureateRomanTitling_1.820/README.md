# Aureate Roman Titling 1.820

A light titling Roman with wedge serifs, derived from Aureate Roman Living Tall 1.701. Four programs
in TTF and WOFF2 under `fonts/`: **Aureate Roman Titling** (Regular, Bold: capitals and lowercase,
small capitals through `smcp` / `c2sc`) and **Aureate Roman Titling SC** (Regular, Bold: the lowercase
keys give the drawn small capitals, so "The Measured Whole" typed as written sets as capitals and small
capitals in any application).

1.800 was the first build, 1.810 added lighter stems and pointed apexes, 1.820 puts the weights and the
alignment on one stated system. Earlier folders are kept unchanged.

## The system

| Measure | Value | Relation |
| --- | --- | --- |
| Capital : x-height | 1453 : 898 | φ (1.61804), the Roman's Tall stature |
| Small capital : x-height | 954 : 898 | φ^(1/8) |
| Hairline : stem : bold stem | 72 : 116.5 : 188.5 | 1 : φ : φ² |
| Every other stroke | H + (p − H)·k | p is that stroke's thickness in the Roman; one law for stems, diagonals, bowls |
| Round overshoot | 31 above C and below the baseline | C·φ^-8 |
| Pointed overshoot (A, V, W, N) | 50 | C·φ^-7, the round overshoot × φ |
| Lowercase and small-capital overshoots | 24 round, 39 pointed | the Roman's own, × φ for points |
| Lining figures | flat at 0 and 1453, rounds at −31 and 1484 | the capital lines |
| Envelope | 0.78615 of the Tall Roman | φ^(-1/2) |
| Titling space | 81 units per glyph | X·φ^-5 |
| Word space | 484 units | em·φ^-3 |

**Weight law.** H is the Roman's hairline, measured on the crossbar of H (72 units in Regular, 86 in
Bold); S is its capital stem (192, 315). A stroke of perpendicular thickness p in the Roman becomes
H + (p − H)·k, with k = (T − H)/(S − H) and target stem T = 72·φ in Regular and 72·φ² in Bold. Strokes
at or below H are kept. Thickness is measured by rays along the inward normal in both the Roman and the
narrowed outline; each edge is offset along its normal and corners are re-intersected. Flat edges,
stroke ends and the outside of bowls at their extremes are pinned, and the far side takes the whole
correction, so no alignment line or overshoot moves. Measured results are in
`verification/proportions_measured.json`: capital stems 117 (Regular, the integer nearest 116.5) and
188 (Bold), lowercase stems 107 to 110, small-capital stems 104, thick diagonals 117 to 125, bowls
125 to 138 at their thickest. Measured stem : hairline is 1.625 and bold : regular stem 1.607 against
φ = 1.618; the difference is rounding to whole font units.

**Serifs and points.** Flat serif ends and arm beaks are drawn to points (tip at the serif thickness
× φ^(-1/2)). A flat apex or vertex between two long diagonals is cut obliquely: the thick stroke's
outer edge runs straight on to the overshoot line, so neither stroke tapers.

## Limits

- Bowls at their thickest are 1.18 × the stem, against 1.15 in the Roman: slightly heavier than the
  law predicts, because curves are corrected edge by edge.
- About a quarter of the glyphs (726 of 2,577 eligible in Regular, 812 in Bold) could not take the full
  correction without tangling or bending their outline and use a simpler pass that thins upright
  stem sides only, by the same law. Their shallow diagonals and bowl shoulders keep the Roman's
  narrowed weight.
- A few Bold letters (B, h, a) show a slight irregularity in a counter or shoulder at very large sizes.
- Lowercase a has a faintly faceted bowl in Regular.
- No italic. The letterforms are Aureate's own; this is in the manner of that kind of logo lettering,
  not a copy of any.

## Rebuild

    python3 source/build_titling.py            # fonts/ and verification/titling_report.json  (about 6 minutes)
    python3 source/make_titling_specimen.py    # specimen/…Specimen.png, shaped with HarfBuzz
    python3 source/measure_strokes.py fonts/AureateRomanTitling-Regular.ttf I H O S A V n

Requires Python 3.10+, fontTools, numpy, brotli, uharfbuzz and Pillow. SIL Open Font License 1.1;
derived from Liberation Serif through Aureate Roman Living. Aureate Type, 2026.
