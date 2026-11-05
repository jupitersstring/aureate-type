# Aureate Destiny Serif 1.910: certificate

Every relation is measured in the finished fonts by `source/certificate_serif.py`. Lengths are in font units (2048 to the em). A stroke may differ from its target by one unit, because outlines sit on a whole-unit grid; a line or a height by half a unit; a ratio by what a three-quarter-unit reading error on each of its two lengths allows.

| Family | Relations | Passed |
| --- | --- | --- |
| solids | 20 | 20 |
| Aureate Destiny Serif | 133 | 133 |
| Aureate Destiny Serif Bold | 104 | 104 |
| Aureate Destiny Solar Serif | 135 | 135 |
| Aureate Destiny Solar Serif Bold | 106 | 106 |

## The five solids, measured from their vertex coordinates (edge = 1)

| Solid | V, E, F | r | ρ | R | ρ : r | R : ρ | R : r | Element | Kepler's place |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tetrahedron | 4, 6, 4 | 0.204124 | 0.353553 | 0.612372 | 1.732051 | 1.732051 | 3.000000 | fire | between Jupiter and Mars |
| cube | 8, 12, 6 | 0.500000 | 0.707107 | 0.866025 | 1.414214 | 1.224745 | 1.732051 | earth | between Saturn and Jupiter |
| octahedron | 6, 12, 8 | 0.408248 | 0.500000 | 0.707107 | 1.224745 | 1.414214 | 1.732051 | air | between Venus and Mercury |
| icosahedron | 12, 30, 20 | 0.755761 | 0.809017 | 0.951057 | 1.070466 | 1.175571 | 1.258409 | water | between Earth and Venus |
| dodecahedron | 20, 30, 12 | 1.113516 | 1.309017 | 1.401259 | 1.175571 | 1.070466 | 1.258409 | the heavens (aether) | between Mars and Earth |

## solids

| Group | Measure | Relation | Target | Measured | Tolerance | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| tetrahedron | r of the tetrahedron, edge 1 | measured from vertex coordinates against the closed form | 0.2041 | 0.2041 | ±1e-09 | pass |
| tetrahedron | ρ of the tetrahedron, edge 1 | measured from vertex coordinates against the closed form | 0.3536 | 0.3536 | ±1e-09 | pass |
| tetrahedron | R of the tetrahedron, edge 1 | measured from vertex coordinates against the closed form | 0.6124 | 0.6124 | ±1e-09 | pass |
| tetrahedron | vertices, edges, faces of the tetrahedron | counted from coordinates; V − E + F = 2 | 2 | 2 | ±0 | pass |
| cube | r of the cube, edge 1 | measured from vertex coordinates against the closed form | 0.5000 | 0.5000 | ±1e-09 | pass |
| cube | ρ of the cube, edge 1 | measured from vertex coordinates against the closed form | 0.7071 | 0.7071 | ±1e-09 | pass |
| cube | R of the cube, edge 1 | measured from vertex coordinates against the closed form | 0.8660 | 0.8660 | ±1e-09 | pass |
| cube | vertices, edges, faces of the cube | counted from coordinates; V − E + F = 2 | 2 | 2 | ±0 | pass |
| octahedron | r of the octahedron, edge 1 | measured from vertex coordinates against the closed form | 0.4082 | 0.4082 | ±1e-09 | pass |
| octahedron | ρ of the octahedron, edge 1 | measured from vertex coordinates against the closed form | 0.5000 | 0.5000 | ±1e-09 | pass |
| octahedron | R of the octahedron, edge 1 | measured from vertex coordinates against the closed form | 0.7071 | 0.7071 | ±1e-09 | pass |
| octahedron | vertices, edges, faces of the octahedron | counted from coordinates; V − E + F = 2 | 2 | 2 | ±0 | pass |
| icosahedron | r of the icosahedron, edge 1 | measured from vertex coordinates against the closed form | 0.7558 | 0.7558 | ±1e-09 | pass |
| icosahedron | ρ of the icosahedron, edge 1 | measured from vertex coordinates against the closed form | 0.8090 | 0.8090 | ±1e-09 | pass |
| icosahedron | R of the icosahedron, edge 1 | measured from vertex coordinates against the closed form | 0.9511 | 0.9511 | ±1e-09 | pass |
| icosahedron | vertices, edges, faces of the icosahedron | counted from coordinates; V − E + F = 2 | 2 | 2 | ±0 | pass |
| dodecahedron | r of the dodecahedron, edge 1 | measured from vertex coordinates against the closed form | 1.1135 | 1.1135 | ±1e-09 | pass |
| dodecahedron | ρ of the dodecahedron, edge 1 | measured from vertex coordinates against the closed form | 1.3090 | 1.3090 | ±1e-09 | pass |
| dodecahedron | R of the dodecahedron, edge 1 | measured from vertex coordinates against the closed form | 1.4013 | 1.4013 | ±1e-09 | pass |
| dodecahedron | vertices, edges, faces of the dodecahedron | counted from coordinates; V − E + F = 2 | 2 | 2 | ±0 | pass |

## Aureate Destiny Serif

| Group | Measure | Relation | Target | Measured | Tolerance | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| datum | cap height : x-height | the icosahedron of edge X spans three golden rectangles X by C (2ρ : edge) | 1.6180 | 1.6180 | ±0.0015 | pass |
| datum | cap height : x-height, by the dodecahedron | the cube inscribed in the dodecahedron of edge X has edge C (face diagonal : edge) | 1.6180 | 1.6180 | ±0.0015 | pass |
| stroke | stem | X·φ^(−9/2) | 103 | 103 | ±1 | pass |
| stroke | hairline | stem ÷ φ: midradius of the icosahedron whose edge is two serifs | 63.66 | 64 | ±1 | pass |
| stroke | serif (tip of I) | hairline ÷ φ | 39.34 | 39 | ±1 | pass |
| stroke | stem, by the dodecahedron | midradius of the dodecahedron whose edge is two serifs | 103 | 103 | ±1 | pass |
| stroke | hairline : serif | ρ of the icosahedron : half its edge = φ | 1.6180 | 1.6410 | ±0.0508 | pass |
| stroke | stem : hairline | face diagonal : edge of the dodecahedron = φ | 1.6180 | 1.6094 | ±0.0306 | pass |
| stroke | stem : serif | ρ of the dodecahedron : half its edge = φ² | 2.6180 | 2.6410 | ±0.0700 | pass |
| stroke | bowl | stem·φ^(1/4) | 116.17 | 116.17 | ±1 | pass |
| lining | overshoot above, O | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, C | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, G | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, S | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, 0 | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, 8 | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot below, O | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot below, C | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot below, G | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot below, S | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot below, 0 | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot below, 8 | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | apex of A above the cap line | C·φ^(−9) | 19 | 19 | ±0.5 | pass |
| lining | vertex of V below the baseline | C·φ^(−15/2) | 39 | 39 | ±0.5 | pass |
| lining | vertex of W below the baseline | C·φ^(−15/2) | 39 | 39 | ±0.5 | pass |
| lining | small capital height | X·φ^(1/8) | 954 | 954 | ±0.5 | pass |
| spacing | titling space added to H | X·φ^(−2) | 343 | 343 | ±1 | pass |
| spacing | titling space added to O | X·φ^(−2) | 343 | 343 | ±1 | pass |
| spacing | titling space added to A | X·φ^(−2) | 343 | 343 | ±1 | pass |
| spacing | titling space added to E | X·φ^(−2) | 343 | 343 | ±1 | pass |
| spacing | word space | X | 898 | 898 | ±0.5 | pass |
| stroke | dot | stem·φ^(3/4) | 147.77 | 148 | ±1 | pass |
| stroke | broad end of the exclamation wedge | stem·φ^(1/2) | 131.02 | 132 | ±1 | pass |
| width | ink width of W | C·φ^(0.5) | 1848.24 | 1848 | ±1 | pass |
| width | ink width of M | C·φ^(0.25) | 1638.75 | 1639 | ±1 | pass |
| width | ink width of A | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of H | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of K | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of N | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of U | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of V | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of X | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of Y | C·φ^(0) | 1453 | 1453 | ±1 | pass |
| width | ink width of D | C·φ^(-0.25) | 1288.31 | 1288 | ±1 | pass |
| width | ink width of G | C·φ^(-0.25) | 1288.31 | 1288 | ±1 | pass |
| width | ink width of O | C·φ^(-0.25) | 1288.31 | 1288 | ±1 | pass |
| width | ink width of Q | C·φ^(-0.25) | 1288.31 | 1288 | ±1 | pass |
| width | ink width of R | C·φ^(-0.25) | 1288.31 | 1288 | ±1 | pass |
| width | ink width of B | C·φ^(-0.5) | 1142.28 | 1142 | ±1 | pass |
| width | ink width of C | C·φ^(-0.5) | 1142.28 | 1142 | ±1 | pass |
| width | ink width of E | C·φ^(-0.5) | 1142.28 | 1142 | ±1 | pass |
| width | ink width of L | C·φ^(-0.5) | 1142.28 | 1142 | ±1 | pass |
| width | ink width of T | C·φ^(-0.5) | 1142.28 | 1142 | ±1 | pass |
| width | ink width of Z | C·φ^(-0.5) | 1142.28 | 1142 | ±1 | pass |
| width | ink width of F | C·φ^(-0.75) | 1012.8 | 1013 | ±1 | pass |
| width | ink width of P | C·φ^(-0.75) | 1012.8 | 1013 | ±1 | pass |
| width | ink width of S | C·φ^(-1) | 898 | 898 | ±1 | pass |
| width | ink width of J | C·φ^(-1.5) | 705.97 | 706 | ±1 | pass |
| width | ink width of I | C·φ^(-2) | 555 | 555 | ±1 | pass |
| uniformity | stem of B | every upright stem is the stem | 103 | 103 | ±1 | pass |
| uniformity | stem of D | every upright stem is the stem | 103 | 103 | ±1 | pass |
| uniformity | stem of E | every upright stem is the stem | 103 | 103 | ±1 | pass |
| uniformity | stem of F | every upright stem is the stem | 103 | 102 | ±1 | pass |
| uniformity | stem of H | every upright stem is the stem | 103 | 102 | ±1 | pass |
| uniformity | stem of I | every upright stem is the stem | 103 | 103 | ±1 | pass |
| uniformity | stem of K | every upright stem is the stem | 103 | 102 | ±1 | pass |
| uniformity | stem of L | every upright stem is the stem | 103 | 102 | ±1 | pass |
| uniformity | stem of P | every upright stem is the stem | 103 | 102 | ±1 | pass |
| uniformity | stem of R | every upright stem is the stem | 103 | 103 | ±1 | pass |
| uniformity | stem of T | every upright stem is the stem | 103 | 103 | ±1 | pass |
| uniformity | stem of H right | every upright stem is the stem | 103 | 103 | ±1 | pass |
| uniformity | stem of 1 | every upright stem is the stem | 103 | 102 | ±1 | pass |
| uniformity | stem of 4 | every upright stem is the stem | 103 | 102 | ±1 | pass |
| uniformity | hairline, H bar | every straight thin stroke is the hairline | 63.66 | 64 | ±1 | pass |
| uniformity | hairline, E foot arm | every straight thin stroke is the hairline | 63.66 | 64.03 | ±1 | pass |
| uniformity | hairline, E middle arm | every straight thin stroke is the hairline | 63.66 | 64 | ±1 | pass |
| uniformity | hairline, E top arm | every straight thin stroke is the hairline | 63.66 | 64.12 | ±1 | pass |
| uniformity | hairline, F middle arm | every straight thin stroke is the hairline | 63.66 | 63 | ±1 | pass |
| uniformity | hairline, F top arm | every straight thin stroke is the hairline | 63.66 | 64.02 | ±1 | pass |
| uniformity | hairline, L arm | every straight thin stroke is the hairline | 63.66 | 64.05 | ±1 | pass |
| uniformity | hairline, T bar, left | every straight thin stroke is the hairline | 63.66 | 64 | ±1 | pass |
| uniformity | hairline, T bar, right | every straight thin stroke is the hairline | 63.66 | 64 | ±1 | pass |
| uniformity | hairline, Z foot | every straight thin stroke is the hairline | 63.66 | 64.03 | ±1 | pass |
| uniformity | hairline, Z top | every straight thin stroke is the hairline | 63.66 | 64 | ±1 | pass |
| uniformity | hairline, A bar | every straight thin stroke is the hairline | 63.66 | 64 | ±1 | pass |
| uniformity | serif tips of A: thinnest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of A: thickest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of B: thinnest of 1 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of B: thickest of 1 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of D: thinnest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of D: thickest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of E: thinnest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of E: thickest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of F: thinnest of 3 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of F: thickest of 3 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of H: thinnest of 8 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of H: thickest of 8 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of I: thinnest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of I: thickest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of K: thinnest of 7 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of K: thickest of 7 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of L: thinnest of 3 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of L: thickest of 3 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of M: thinnest of 6 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of M: thickest of 6 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of N: thinnest of 5 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of N: thickest of 5 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of P: thinnest of 3 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of P: thickest of 3 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of R: thinnest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of R: thickest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of T: thinnest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of T: thickest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of U: thinnest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of U: thickest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of V: thinnest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of V: thickest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of W: thinnest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of W: thickest of 4 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of X: thinnest of 8 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of X: thickest of 8 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of Y: thinnest of 6 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of Y: thickest of 6 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of 1: thinnest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | serif tips of 1: thickest of 2 | every serif tip is the serif | 39.34 | 39 | ±1 | pass |
| uniformity | small capital stem (H) | small capitals take the capitals' strokes | 103 | 102 | ±1 | pass |
| uniformity | small capital stem (E) | small capitals take the capitals' strokes | 103 | 103 | ±1 | pass |
| uniformity | small capital hairline (H bar) | small capitals take the capitals' strokes | 63.66 | 64 | ±1 | pass |
| uniformity | small capital hairline (T bar) | small capitals take the capitals' strokes | 63.66 | 64 | ±1 | pass |
| uniformity | small capital serif tips of H: thinnest | small capitals take the capitals' strokes | 39.34 | 39 | ±1 | pass |
| uniformity | small capital serif tips of H: thickest | small capitals take the capitals' strokes | 39.34 | 39 | ±1 | pass |
| uniformity | small capital serif tips of T: thinnest | small capitals take the capitals' strokes | 39.34 | 39 | ±1 | pass |
| uniformity | small capital serif tips of T: thickest | small capitals take the capitals' strokes | 39.34 | 39 | ±1 | pass |

## Aureate Destiny Serif Bold

| Group | Measure | Relation | Target | Measured | Tolerance | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| stroke | bold stem | stem·φ | 166.66 | 167 | ±1 | pass |
| stroke | bold hairline | hairline·φ^(1/2) | 80.97 | 80 | ±1 | pass |
| stroke | bold serif | serif·φ^(1/4) | 44.37 | 44 | ±1 | pass |
| stroke | bold bowl | bold stem·φ^(1/4) | 187.96 | 187.95 | ±1 | pass |
| stroke | bold stem : stem | one whole step, φ | 1.6180 | 1.6214 | ±0.0191 | pass |
| stroke | bold dot | bold stem·φ^(3/4) | 239.09 | 240 | ±1 | pass |
| width | ink width of W | rung·φ^(1/8) | 1962.83 | 1963 | ±1 | pass |
| width | ink width of M | rung·φ^(1/8) | 1740.35 | 1740 | ±1 | pass |
| width | ink width of A | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of H | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of K | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of N | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of U | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of V | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of X | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of Y | rung·φ^(1/8) | 1543.08 | 1543 | ±1 | pass |
| width | ink width of D | rung·φ^(1/8) | 1368.18 | 1368 | ±1 | pass |
| width | ink width of G | rung·φ^(1/8) | 1368.18 | 1368 | ±1 | pass |
| width | ink width of O | rung·φ^(1/8) | 1368.18 | 1368 | ±1 | pass |
| width | ink width of Q | rung·φ^(1/8) | 1368.18 | 1368 | ±1 | pass |
| width | ink width of R | rung·φ^(1/8) | 1368.18 | 1368 | ±1 | pass |
| width | ink width of B | rung·φ^(1/8) | 1213.1 | 1213 | ±1 | pass |
| width | ink width of C | rung·φ^(1/8) | 1213.1 | 1213 | ±1 | pass |
| width | ink width of E | rung·φ^(1/8) | 1213.1 | 1213 | ±1 | pass |
| width | ink width of L | rung·φ^(1/8) | 1213.1 | 1213 | ±1 | pass |
| width | ink width of T | rung·φ^(1/8) | 1213.1 | 1213 | ±1 | pass |
| width | ink width of Z | rung·φ^(1/8) | 1213.1 | 1213 | ±1 | pass |
| width | ink width of F | rung·φ^(1/8) | 1075.59 | 1076 | ±1 | pass |
| width | ink width of P | rung·φ^(1/8) | 1075.59 | 1076 | ±1 | pass |
| width | ink width of S | rung·φ^(1/8) | 953.68 | 954 | ±1 | pass |
| width | ink width of J | rung·φ^(1/8) | 749.73 | 750 | ±1 | pass |
| width | ink width of I | rung·φ^(1/8) | 589.4 | 589 | ±1 | pass |
| uniformity | stem of B | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of D | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of E | every upright stem is the bold stem | 166.66 | 167 | ±1 | pass |
| uniformity | stem of F | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of H | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of I | every upright stem is the bold stem | 166.66 | 167 | ±1 | pass |
| uniformity | stem of K | every upright stem is the bold stem | 166.66 | 167 | ±1 | pass |
| uniformity | stem of L | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of P | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of R | every upright stem is the bold stem | 166.66 | 167 | ±1 | pass |
| uniformity | stem of T | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of H right | every upright stem is the bold stem | 166.66 | 167 | ±1 | pass |
| uniformity | stem of 1 | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | stem of 4 | every upright stem is the bold stem | 166.66 | 166 | ±1 | pass |
| uniformity | serif tips of A: thinnest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of A: thickest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of B: thinnest of 1 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of B: thickest of 1 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of D: thinnest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of D: thickest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of E: thinnest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of E: thickest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of F: thinnest of 3 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of F: thickest of 3 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of H: thinnest of 8 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of H: thickest of 8 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of I: thinnest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of I: thickest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of K: thinnest of 7 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of K: thickest of 7 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of L: thinnest of 3 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of L: thickest of 3 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of M: thinnest of 6 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of M: thickest of 6 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of N: thinnest of 5 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of N: thickest of 5 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of P: thinnest of 3 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of P: thickest of 3 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of R: thinnest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of R: thickest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of T: thinnest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of T: thickest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of U: thinnest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of U: thickest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of V: thinnest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of V: thickest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of W: thinnest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of W: thickest of 4 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of X: thinnest of 8 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of X: thickest of 8 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of Y: thinnest of 6 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of Y: thickest of 6 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of 1: thinnest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | serif tips of 1: thickest of 2 | every serif tip is the bold serif | 44.37 | 44 | ±1 | pass |
| uniformity | hairline, H bar | every straight thin stroke is the bold hairline | 80.97 | 80 | ±1 | pass |
| uniformity | hairline, E foot arm | every straight thin stroke is the bold hairline | 80.97 | 81.06 | ±1 | pass |
| uniformity | hairline, E middle arm | every straight thin stroke is the bold hairline | 80.97 | 80 | ±1 | pass |
| uniformity | hairline, E top arm | every straight thin stroke is the bold hairline | 80.97 | 81.3 | ±1 | pass |
| uniformity | hairline, F middle arm | every straight thin stroke is the bold hairline | 80.97 | 81 | ±1 | pass |
| uniformity | hairline, F top arm | every straight thin stroke is the bold hairline | 80.97 | 81.06 | ±1 | pass |
| uniformity | hairline, L arm | every straight thin stroke is the bold hairline | 80.97 | 81.13 | ±1 | pass |
| uniformity | hairline, T bar, left | every straight thin stroke is the bold hairline | 80.97 | 81 | ±1 | pass |
| uniformity | hairline, T bar, right | every straight thin stroke is the bold hairline | 80.97 | 81 | ±1 | pass |
| uniformity | hairline, Z foot | every straight thin stroke is the bold hairline | 80.97 | 81.07 | ±1 | pass |
| uniformity | hairline, Z top | every straight thin stroke is the bold hairline | 80.97 | 81 | ±1 | pass |
| uniformity | hairline, A bar | every straight thin stroke is the bold hairline | 80.97 | 80 | ±1 | pass |
| lining | overshoot above, O | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, C | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, G | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, S | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, 0 | C·φ^(−8) | 31 | 31 | ±0.5 | pass |
| lining | overshoot above, 8 | C·φ^(−8) | 31 | 31 | ±0.5 | pass |

## Aureate Destiny Solar Serif

| Group | Measure | Relation | Target | Measured | Tolerance | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| stroke | stem | C ÷ 14 (twice seven) | 103.79 | 104 | ±1 | pass |
| stroke | serif | inradius of the tetrahedron whose edge is two stems | 42.37 | 42 | ±1 | pass |
| stroke | hairline | midradius of the same tetrahedron | 73.39 | 74 | ±1 | pass |
| stroke | hairline : serif | ρ : r of the tetrahedron = R : r of the cube = R : r of the octahedron = √3 | 1.7321 | 1.7619 | ±0.0493 | pass |
| stroke | √3 three ways | tetrahedron ρ : r against cube R : r | 1.7321 | 1.7321 | ±1e-09 | pass |
| stroke | √3 three ways | tetrahedron ρ : r against octahedron R : r | 1.7321 | 1.7321 | ±1e-09 | pass |
| stroke | stem : hairline | ρ : r of the cube = R : ρ of the octahedron = √2 | 1.4142 | 1.4054 | ±0.0244 | pass |
| stroke | √2 two ways | cube ρ : r against octahedron R : ρ | 1.4142 | 1.4142 | ±1e-09 | pass |
| stroke | stem : serif | half-edge : inradius of the tetrahedron = √6 | 2.4495 | 2.4762 | ±0.0621 | pass |
| datum | cap height : stem | 14 : 1 | 14.0000 | 13.9712 | ±0.0720 | pass |
| stroke | bowl | stem·9/8, the tone | 116.76 | 117.14 | ±1 | pass |
| lining | overshoot above, O | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, C | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, G | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, S | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, 0 | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, 8 | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot below, O | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot below, C | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot below, G | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot below, S | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot below, 0 | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot below, 8 | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | apex of A above the cap line | C ÷ 72 | 20 | 20 | ±0.5 | pass |
| lining | vertex of V below the baseline | C ÷ 36 | 40 | 40 | ±0.5 | pass |
| lining | vertex of W below the baseline | C ÷ 36 | 40 | 40 | ±0.5 | pass |
| lining | small capital height | C·2/3, the fifth | 969 | 969 | ±0.5 | pass |
| spacing | titling space added to H | C ÷ 4 | 363 | 363 | ±1 | pass |
| spacing | titling space added to O | C ÷ 4 | 363 | 363 | ±1 | pass |
| spacing | titling space added to A | C ÷ 4 | 363 | 363 | ±1 | pass |
| spacing | titling space added to E | C ÷ 4 | 363 | 363 | ±1 | pass |
| spacing | word space | C ÷ 2, the octave over the titling space | 726 | 726 | ±0.5 | pass |
| stroke | dot | stem·3/2, the fifth | 155.68 | 156 | ±1 | pass |
| stroke | broad end of the exclamation wedge | stem·4/3, the fourth; dot : wedge = 9 : 8 | 138.38 | 138 | ±1 | pass |
| width | √3/2 from the cube | circumradius of the cube of edge 1 | 0.8660 | 0.8660 | ±1e-09 | pass |
| width | 1/√2 from the cube | edge : face diagonal, r : ρ of the cube | 0.7071 | 0.7071 | ±1e-09 | pass |
| width | ink width of W | 16/12 C | 1937.33 | 1937 | ±1 | pass |
| width | ink width of M | 14/12 C | 1695.17 | 1695 | ±1 | pass |
| width | ink width of A | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of H | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of K | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of N | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of U | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of V | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of X | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of Y | 12/12 C, the face of the cube of edge C | 1453 | 1453 | ±1 | pass |
| width | ink width of D | √3/2 C, the circumradius of the cube of edge C | 1258.33 | 1258 | ±1 | pass |
| width | ink width of G | √3/2 C, the circumradius of the cube of edge C | 1258.33 | 1258 | ±1 | pass |
| width | ink width of O | √3/2 C, the circumradius of the cube of edge C | 1258.33 | 1258 | ±1 | pass |
| width | ink width of Q | √3/2 C, the circumradius of the cube of edge C | 1258.33 | 1258 | ±1 | pass |
| width | ink width of R | √3/2 C, the circumradius of the cube of edge C | 1258.33 | 1258 | ±1 | pass |
| width | ink width of B | 10/12 C | 1210.83 | 1211 | ±1 | pass |
| width | ink width of C | 10/12 C | 1210.83 | 1211 | ±1 | pass |
| width | ink width of L | 10/12 C | 1210.83 | 1211 | ±1 | pass |
| width | ink width of T | 10/12 C | 1210.83 | 1211 | ±1 | pass |
| width | ink width of Z | 10/12 C | 1210.83 | 1211 | ±1 | pass |
| width | ink width of E | 9/12 C | 1089.75 | 1090 | ±1 | pass |
| width | ink width of F | C ÷ √2, the edge of the cube whose face diagonal is C | 1027.43 | 1027 | ±1 | pass |
| width | ink width of P | C ÷ √2, the edge of the cube whose face diagonal is C | 1027.43 | 1027 | ±1 | pass |
| width | ink width of S | 7/12 C | 847.58 | 847 | ±1 | pass |
| width | ink width of J | 6/12 C | 726.5 | 727 | ±1 | pass |
| uniformity | stem of B | every upright stem is the stem | 103.79 | 103 | ±1 | pass |
| uniformity | stem of D | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of E | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of F | every upright stem is the stem | 103.79 | 103 | ±1 | pass |
| uniformity | stem of H | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of I | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of K | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of L | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of P | every upright stem is the stem | 103.79 | 103 | ±1 | pass |
| uniformity | stem of R | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of T | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of H right | every upright stem is the stem | 103.79 | 103 | ±1 | pass |
| uniformity | stem of 1 | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | stem of 4 | every upright stem is the stem | 103.79 | 104 | ±1 | pass |
| uniformity | hairline, H bar | every straight thin stroke is the hairline | 73.39 | 74 | ±1 | pass |
| uniformity | hairline, E foot arm | every straight thin stroke is the hairline | 73.39 | 73.02 | ±1 | pass |
| uniformity | hairline, E middle arm | every straight thin stroke is the hairline | 73.39 | 74 | ±1 | pass |
| uniformity | hairline, E top arm | every straight thin stroke is the hairline | 73.39 | 73.13 | ±1 | pass |
| uniformity | hairline, F middle arm | every straight thin stroke is the hairline | 73.39 | 73 | ±1 | pass |
| uniformity | hairline, F top arm | every straight thin stroke is the hairline | 73.39 | 73.02 | ±1 | pass |
| uniformity | hairline, L arm | every straight thin stroke is the hairline | 73.39 | 73.06 | ±1 | pass |
| uniformity | hairline, T bar, left | every straight thin stroke is the hairline | 73.39 | 73 | ±1 | pass |
| uniformity | hairline, T bar, right | every straight thin stroke is the hairline | 73.39 | 73 | ±1 | pass |
| uniformity | hairline, Z foot | every straight thin stroke is the hairline | 73.39 | 73.03 | ±1 | pass |
| uniformity | hairline, Z top | every straight thin stroke is the hairline | 73.39 | 73 | ±1 | pass |
| uniformity | hairline, A bar | every straight thin stroke is the hairline | 73.39 | 74 | ±1 | pass |
| uniformity | serif tips of A: thinnest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of A: thickest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of B: thinnest of 1 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of B: thickest of 1 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of D: thinnest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of D: thickest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of E: thinnest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of E: thickest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of F: thinnest of 3 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of F: thickest of 3 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of H: thinnest of 8 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of H: thickest of 8 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of I: thinnest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of I: thickest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of K: thinnest of 7 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of K: thickest of 7 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of L: thinnest of 3 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of L: thickest of 3 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of M: thinnest of 6 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of M: thickest of 6 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of N: thinnest of 5 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of N: thickest of 5 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of P: thinnest of 3 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of P: thickest of 3 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of R: thinnest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of R: thickest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of T: thinnest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of T: thickest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of U: thinnest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of U: thickest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of V: thinnest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of V: thickest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of W: thinnest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of W: thickest of 4 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of X: thinnest of 8 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of X: thickest of 8 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of Y: thinnest of 6 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of Y: thickest of 6 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of 1: thinnest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | serif tips of 1: thickest of 2 | every serif tip is the serif | 42.37 | 42 | ±1 | pass |
| uniformity | small capital stem (H) | small capitals take the capitals' strokes | 103.79 | 104 | ±1 | pass |
| uniformity | small capital stem (E) | small capitals take the capitals' strokes | 103.79 | 103 | ±1 | pass |
| uniformity | small capital hairline (H bar) | small capitals take the capitals' strokes | 73.39 | 73 | ±1 | pass |
| uniformity | small capital hairline (T bar) | small capitals take the capitals' strokes | 73.39 | 73 | ±1 | pass |
| uniformity | small capital serif tips of H: thinnest | small capitals take the capitals' strokes | 42.37 | 42 | ±1 | pass |
| uniformity | small capital serif tips of H: thickest | small capitals take the capitals' strokes | 42.37 | 42 | ±1 | pass |
| uniformity | small capital serif tips of T: thinnest | small capitals take the capitals' strokes | 42.37 | 42 | ±1 | pass |
| uniformity | small capital serif tips of T: thickest | small capitals take the capitals' strokes | 42.37 | 42 | ±1 | pass |

## Aureate Destiny Solar Serif Bold

| Group | Measure | Relation | Target | Measured | Tolerance | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| stroke | the bold step | ρ : r of the octahedron = √(3/2) | 1.2247 | 1.2247 | ±1e-09 | pass |
| stroke | bold serif | inradius of the tetrahedron enlarged by the octahedron's step | 51.89 | 52 | ±1 | pass |
| stroke | bold hairline | midradius of the enlarged tetrahedron | 89.88 | 90 | ±1 | pass |
| stroke | bold stem | circumradius of the enlarged tetrahedron | 155.68 | 156 | ±1 | pass |
| stroke | bold stem : stem | two octahedral steps = 3 : 2, the fifth | 1.5000 | 1.5000 | ±0.0180 | pass |
| stroke | bold stem : bold hairline | R : ρ of the tetrahedron = √3 | 1.7321 | 1.7333 | ±0.0228 | pass |
| stroke | bold stem : bold serif | R : r of the tetrahedron = 3 | 3.0000 | 3.0000 | ±0.0577 | pass |
| stroke | bold bowl | bold stem·9/8 | 175.14 | 174.94 | ±1 | pass |
| stroke | bold dot | bold stem·3/2 | 233.52 | 234 | ±1 | pass |
| width | ink width of W | rung·16/15 | 2066.49 | 2066 | ±1 | pass |
| width | ink width of M | rung·16/15 | 1808.18 | 1808 | ±1 | pass |
| width | ink width of A | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of H | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of K | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of N | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of U | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of V | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of X | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of Y | rung·16/15 | 1549.87 | 1550 | ±1 | pass |
| width | ink width of D | rung·16/15 | 1342.22 | 1342 | ±1 | pass |
| width | ink width of G | rung·16/15 | 1342.22 | 1342 | ±1 | pass |
| width | ink width of O | rung·16/15 | 1342.22 | 1342 | ±1 | pass |
| width | ink width of Q | rung·16/15 | 1342.22 | 1342 | ±1 | pass |
| width | ink width of R | rung·16/15 | 1342.22 | 1342 | ±1 | pass |
| width | ink width of B | rung·16/15 | 1291.56 | 1292 | ±1 | pass |
| width | ink width of C | rung·16/15 | 1291.56 | 1291 | ±1 | pass |
| width | ink width of L | rung·16/15 | 1291.56 | 1292 | ±1 | pass |
| width | ink width of T | rung·16/15 | 1291.56 | 1292 | ±1 | pass |
| width | ink width of Z | rung·16/15 | 1291.56 | 1291 | ±1 | pass |
| width | ink width of E | rung·16/15 | 1162.4 | 1162 | ±1 | pass |
| width | ink width of F | rung·16/15 | 1095.92 | 1096 | ±1 | pass |
| width | ink width of P | rung·16/15 | 1095.92 | 1096 | ±1 | pass |
| width | ink width of S | rung·16/15 | 904.09 | 904 | ±1 | pass |
| width | ink width of J | rung·16/15 | 774.93 | 775 | ±1 | pass |
| uniformity | stem of B | every upright stem is the bold stem | 155.68 | 155 | ±1 | pass |
| uniformity | stem of D | every upright stem is the bold stem | 155.68 | 155 | ±1 | pass |
| uniformity | stem of E | every upright stem is the bold stem | 155.68 | 155 | ±1 | pass |
| uniformity | stem of F | every upright stem is the bold stem | 155.68 | 155 | ±1 | pass |
| uniformity | stem of H | every upright stem is the bold stem | 155.68 | 155 | ±1 | pass |
| uniformity | stem of I | every upright stem is the bold stem | 155.68 | 156 | ±1 | pass |
| uniformity | stem of K | every upright stem is the bold stem | 155.68 | 155 | ±1 | pass |
| uniformity | stem of L | every upright stem is the bold stem | 155.68 | 156 | ±1 | pass |
| uniformity | stem of P | every upright stem is the bold stem | 155.68 | 156 | ±1 | pass |
| uniformity | stem of R | every upright stem is the bold stem | 155.68 | 155 | ±1 | pass |
| uniformity | stem of T | every upright stem is the bold stem | 155.68 | 156 | ±1 | pass |
| uniformity | stem of H right | every upright stem is the bold stem | 155.68 | 156 | ±1 | pass |
| uniformity | stem of 1 | every upright stem is the bold stem | 155.68 | 156 | ±1 | pass |
| uniformity | stem of 4 | every upright stem is the bold stem | 155.68 | 156 | ±1 | pass |
| uniformity | serif tips of A: thinnest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of A: thickest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of B: thinnest of 1 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of B: thickest of 1 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of D: thinnest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of D: thickest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of E: thinnest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of E: thickest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of F: thinnest of 3 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of F: thickest of 3 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of H: thinnest of 8 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of H: thickest of 8 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of I: thinnest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of I: thickest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of K: thinnest of 7 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of K: thickest of 7 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of L: thinnest of 3 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of L: thickest of 3 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of M: thinnest of 6 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of M: thickest of 6 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of N: thinnest of 5 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of N: thickest of 5 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of P: thinnest of 3 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of P: thickest of 3 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of R: thinnest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of R: thickest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of T: thinnest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of T: thickest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of U: thinnest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of U: thickest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of V: thinnest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of V: thickest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of W: thinnest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of W: thickest of 4 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of X: thinnest of 8 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of X: thickest of 8 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of Y: thinnest of 6 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of Y: thickest of 6 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of 1: thinnest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | serif tips of 1: thickest of 2 | every serif tip is the bold serif | 51.89 | 52 | ±1 | pass |
| uniformity | hairline, H bar | every straight thin stroke is the bold hairline | 89.88 | 90 | ±1 | pass |
| uniformity | hairline, E foot arm | every straight thin stroke is the bold hairline | 89.88 | 90.06 | ±1 | pass |
| uniformity | hairline, E middle arm | every straight thin stroke is the bold hairline | 89.88 | 90 | ±1 | pass |
| uniformity | hairline, E top arm | every straight thin stroke is the bold hairline | 89.88 | 90.26 | ±1 | pass |
| uniformity | hairline, F middle arm | every straight thin stroke is the bold hairline | 89.88 | 89 | ±1 | pass |
| uniformity | hairline, F top arm | every straight thin stroke is the bold hairline | 89.88 | 90.05 | ±1 | pass |
| uniformity | hairline, L arm | every straight thin stroke is the bold hairline | 89.88 | 90.13 | ±1 | pass |
| uniformity | hairline, T bar, left | every straight thin stroke is the bold hairline | 89.88 | 90 | ±1 | pass |
| uniformity | hairline, T bar, right | every straight thin stroke is the bold hairline | 89.88 | 90 | ±1 | pass |
| uniformity | hairline, Z foot | every straight thin stroke is the bold hairline | 89.88 | 90.07 | ±1 | pass |
| uniformity | hairline, Z top | every straight thin stroke is the bold hairline | 89.88 | 90 | ±1 | pass |
| uniformity | hairline, A bar | every straight thin stroke is the bold hairline | 89.88 | 90 | ±1 | pass |
| lining | overshoot above, O | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, C | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, G | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, S | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, 0 | C ÷ 48 | 30 | 30 | ±0.5 | pass |
| lining | overshoot above, 8 | C ÷ 48 | 30 | 30 | ±0.5 | pass |
