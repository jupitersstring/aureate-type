# Aureate Collection 1.701

Post-release repairs to the 1.700 binaries. The 1.700 package is unchanged; this folder is a
separate build made by `source/repair_1701.py` from the 1.700 TTFs and the bundled upstream
programs. Every change is deterministic and recorded in `verification/repair_report.json`;
`verification/verification_1701.json` compares each program with its 1.700 original.

## What was found

Audit of all 52 programs with FontBakery 1.1 (universal profile), fontTools 4.60, HarfBuzz
shaping tests and rendered proofs against the upstream Liberation Serif and Source Sans 3.

1. **Roman sidebearings below the upstream floor.** The 1.300 class budgets widened the
   straight-stemmed letters inside their unchanged advances. In Text Regular the n carries
   19 / 1 units (Liberation 47 / 31), m 22 / 7, r 15 / −15, u −3 / 5, j −148 / 159;
   capitals N 28 / −30, L 28 / 54 (Liberation 59 / 123), Z 67 / 9 (Liberation 98 / 112).
   Bold is tighter still: n 24 / −4, L 4 / −1, N 8 / −52, Z 67 / −13. Serif-to-serif gaps of
   20 units (0.01 em) merge at text sizes, and NI, NN, ZE, LL collide in capitals. The GPOS
   kerning was carried over from Liberation unchanged, so it presumes Liberation's bearings.
2. **Default figures kerned.** The default figures are tabular (1024 units) but the pair
   1–1 kerns by −76, so ledgers set with kerning on do not align unless `tnum` is requested.
   The narrowed figure 1 was also left off-centre in its tabular advance (211 / 280).
3. **Sans Geometric rebuilt glyphs unspaced.** The redrawn a b c d e h m n o p q and C G O Q
   all carry flat 50 / 50 bearings (Bold 53 / 53) while the retained letters keep the
   Source Sans spacing (l, k, r stems at 163). Words mixing both read unevenly.
4. **Empty .notdef** in all 28 Roman programs (inherited from Liberation; the Sans has one).
5. **Underline and strikeout inconsistent.** Roman underline −212 / 81 (X·φ⁻³ and that ·φ⁻²),
   Sans −50 / 31 (the Source Sans values were not rescaled). Strikeout: Roman Regular 420,
   Roman Bold 530, Sans 596 / 608. A mixed Roman–Sans line showed three different rules.
6. **No `prep` smart-dropout program; no `gasp` in the Sans.** Unhinted TrueType renders
   without dropout control and, in the Sans, without the grayscale flags on Windows.
7. **Degenerate contours** (two-point contours and repeated points) in the geometric
   shapes U+25D0–25D7 and a few others; **missing curve extrema**, mostly in the italics,
   where the oblique transform moved the extremes off the on-curve points
   (Olympian Italic 441 glyphs, Sans Tall Bold Italic 511).
8. **GDEF classes:** sofpasuq (U+05C3, a spacing Hebrew punctuation) classed as a mark in
   the Roman; U+034F not classed as a mark in the Sans.
9. **Variable programs:** the default instance is named “Roman”, not the style; the Sans
   width programs have no named instances at all; no Calm value in the Sans STAT.
10. **Name table** still carries Macintosh (platform 1) records; `xAvgCharWidth` stale;
    OTS warns that GSUB/GPOS feature and script records are not sorted by tag.
11. **Windows metrics differ between the styles of one family** (Roman Living Regular
    2024 / 686, Bold 2081 / 694), so legacy GDI line spacing changes when a word is bolded.

Noted, not changed (design or scope decisions for the author):

- The Roman italics measure 7.9° (Short), 8.4° (Text) and 9.4° (Tall) of stem slant while all
  declare 16.714°; the stature maps change the slope after slanting. Liberation Italic
  itself measures 9.8° against a declared 16.33°, so the declaration follows convention.
- Round letters sit off-centre in the Roman (o 87 / 69, e 97 / 54 against Liberation
  78 / 78 and 80 / 71). The floor restores the short side only; the asymmetry remains.
- Sans Italic small capitals are upright forms under the declared oblique, as documented.
- hhea ascent (1398) is below the tallest stacked accents (2024); USE_TYPO_METRICS is set
  and the Windows metrics cover the ink, so nothing clips, but macOS line spacing uses hhea.
- Full family name plus STAT name of the Roman Variable programs exceeds 31 characters
  (“Aureate Roman Living Variable Condensed”), which Word on Windows truncates.
- 131 unreachable glyphs inherited from Liberation (Eng.alt1, acute.alt1 …); exotic case
  pairs missing (U+A7DC etc.); soft hyphen drawn as a hyphen; fi / fl lack ligature carets.

## What 1.701 changes

- **R1 Bearing floor (Roman, 28 programs).** For every glyph that exists in the matching
  Liberation program, each side is raised to at least the Liberation bearing scaled by the
  family's own bearing exponent (Condensed φ⁻¹ᐟ⁸, Olympian φ⁻³ᐟ¹⁶, Monumental φ¹ᐟ¹⁶,
  others 1). Sides already wider are untouched; advances grow by the deficit; derived
  glyphs (small capitals, figure sets, superiors, case forms) follow their base in
  proportion to their advance. Text Regular: n → 47 / 31, m 43 / 32, u 27 / 35, N 59 / 47,
  L 59 / 123, Z 98 / 112, j −59 / 176. Measured with HarfBuzz on a 150-character pangram the
  Roman programs grow by 1.8 % to 3.2 % (Text Regular 2.02 %, Bold 2.25 %, Italic 2.07 %).
- **R2 Figures.** The figure 1 is centred on its foot serif, keeping the upstream optical
  offset (italics sit left of centre): Text Regular 211 / 280 → 274 / 217, Bold 195 / 271 →
  262 / 204. The 1–1 pair no longer kerns (−76 → 0), so 1,111 and 1,010 align. Kerning between default figures removed in GPOS and
  the legacy `kern` table; `pnum` figures keep their kerning.
- **R3 Sans Geometric.** Rebuilt glyphs take the bearings of their Aureate Sans
  counterparts scaled by the measured retained-glyph factor (0.972 Regular, 0.970 Bold):
  n 50 / 50 → 163 / 151, o → 91 / 91, a → 101 / 141. The pangram grows by 6.8 % (Regular) and
  4.1 % (Bold); the Italic programs contain no rebuilt glyphs and are unchanged.
- **R4** Visible .notdef box at cap height in the Roman programs.
- **R5** Underline −212 / 81 and strikeout 449 / 81 (X / 2) in all 52 programs.
- **R6** `gasp` {7: 10, 65535: 15} and a `prep` smart-dropout program in all 52.
- **R7** Degenerate contours removed; **R8** extrema inserted on the 44 static programs.
  The 8 variable programs keep their point structure so gvar stays valid; the four
  two-point contours in the Roman Variable Bold therefore remain.
- **R9** GDEF classes corrected. **R10** Variable instances Condensed / Calm / default named
  after the style; STAT carries the Calm value. Every program carries a STAT table
  with wght, wdth and ital axes for style linking; the variable programs keep their wdth
  values and gain the weight and italic values of their style.
- **R11** Version 1.701 in name and head; Macintosh name records removed; xAvgCharWidth
  recalculated. **R12** Layout feature and script records sorted by tag.
- **R13** usWinAscent / usWinDescent set to the family's maximum ink in all four styles.
  Typographic and hhea metrics are unchanged.

Kerning values, glyph outlines (other than extrema and degenerate points), feature logic,
character coverage and vertical metrics are unchanged. HarfBuzz shaping of the feature test
strings is identical to 1.700 for every program.
