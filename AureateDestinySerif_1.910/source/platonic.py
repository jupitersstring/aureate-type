#!/usr/bin/env python3
"""The five regular solids, constructed from vertex coordinates and measured (edge = 1): inradius r,
midradius ρ, circumradius R. Used by the certificate and by the geometry plate."""
import math, itertools
import numpy as np
PHI = (1 + 5 ** 0.5) / 2; R2, R3, R6 = 2 ** 0.5, 3 ** 0.5, 6 ** 0.5

def cyc(v): return [v, (v[2], v[0], v[1]), (v[1], v[2], v[0])]
def signs(v): return {tuple(s * c for s, c in zip(sg, v)) for sg in itertools.product((1, -1), repeat=3)}
def solid_vertices():
    V = {}
    V["tetrahedron"] = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    V["cube"] = sorted(signs((1, 1, 1)))
    V["octahedron"] = sorted(set().union(*[signs(p) for p in cyc((1, 0, 0))]))
    V["icosahedron"] = sorted(set().union(*[signs(p) for p in cyc((0, 1, PHI))]))
    V["dodecahedron"] = sorted(signs((1, 1, 1)) | set().union(*[signs(p) for p in cyc((0, 1 / PHI, PHI))]))
    return {k: np.array(v, float) for k, v in V.items()}

def measure_solid(P):
    n = len(P); d = np.linalg.norm(P[:, None] - P[None], axis=2); e = d[d > 1e-9].min()
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if abs(d[i, j] - e) < 1e-9]
    R = float(np.linalg.norm(P, axis=1).max()); rho = float(min(np.linalg.norm((P[i] + P[j]) / 2) for i, j in edges))
    planes = {}
    for i, j, k in itertools.combinations(range(n), 3):                # a face plane has every vertex on one side
        nrm = np.cross(P[j] - P[i], P[k] - P[i]); ln = np.linalg.norm(nrm)
        if ln < 1e-9: continue
        nrm /= ln; h = float(nrm @ P[i])
        if h < 0: nrm, h = -nrm, -h
        if (P @ nrm <= h + 1e-9).all(): planes[tuple(np.round(nrm, 6))] = h
    r = min(planes.values()); dist = sorted({round(float(x), 9) for x in d[d > 1e-9]})
    return dict(vertices=n, edges=len(edges), faces=len(planes), edge=float(e), r=r / e, rho=rho / e, R=R / e, face_planes=[(nrm_, h_) for nrm_, h_ in planes.items()],
                second_distance=dist[1] / e if len(dist) > 1 else None, edge_list=edges)

VERT = solid_vertices(); SOL = {k: measure_solid(v) for k, v in VERT.items()}
CLOSED = {"tetrahedron": (R6 / 12, R2 / 4, R6 / 4), "cube": (0.5, R2 / 2, R3 / 2), "octahedron": (R6 / 6, 0.5, R2 / 2),
          "icosahedron": (PHI ** 2 / (2 * R3), PHI / 2, math.sqrt(PHI * 5 ** 0.5) / 2),
          "dodecahedron": (PHI ** 2 / (2 * math.sqrt(3 - PHI)), PHI ** 2 / 2, R3 * PHI / 2)}
EULER = {"tetrahedron": (4, 6, 4), "cube": (8, 12, 6), "octahedron": (6, 12, 8), "icosahedron": (12, 30, 20), "dodecahedron": (20, 30, 12)}
CORR = {  # traditional correspondences: Plato, Timaeus 53c-56c; Kepler, Mysterium Cosmographicum (1596)
    "tetrahedron": ("fire", "between Jupiter and Mars"), "cube": ("earth", "between Saturn and Jupiter"),
    "octahedron": ("air", "between Venus and Mercury"), "icosahedron": ("water", "between Earth and Venus"),
    "dodecahedron": ("the heavens (aether)", "between Mars and Earth")}
