# FreeCAD macro: add a cast-iron bump crust to the outer cylinder walls
# of `lower_base_flanged`, then write an STL for printing.
#
# Run after the hung remesh is cancelled/restarted:
#   Macro → Macros... → Execute, or paste into the Python console.
#
# Only the outer vault/cylinder faces are displaced. Flanges, holes, and
# inner walls stay smooth. Displacement fades out over 7 mm at the flanges
# so the mesh stays connected.

import math
import os
import sys
import FreeCAD as App
import Mesh
import MeshPart
import Part
from FreeCAD import Vector

DOC_NAME = "bottom_1x"
SRC_NAME = "lower_base_flanged"
OUT_MESH = "lower_base_cast"
STL_PATH = os.path.join(
    os.path.dirname(App.ActiveDocument.FileName)
    if App.ActiveDocument and App.ActiveDocument.FileName
    else os.path.expanduser("~/work/ih-53-ev/futuristic power"),
    "lower_base_cast.stl",
)

MAX_LEN = 1.2          # mm triangle size on outer walls
AMP = 0.55             # mm bump amplitude
BASE_OFFSET = 0.15     # mm always-outward so slicer sees the bumps
CRUST = 0.45           # mm inward overlap into the solid
FADE = 7.0
Z_BOTTOM = 9.75
Z_TOP = 106.35
MID_X, MID_Y, Z_AXIS = 423.8625, 181.76875, 4.7498
R_FB_O, R_LR_O = 163.769, 405.863
R_FB_I, R_LR_I = 159.019, 401.113


def fade_z(z):
    d = min(z - Z_BOTTOM, Z_TOP - z)
    if d >= FADE:
        return 1.0
    if d <= 0.0:
        return 0.0
    t = d / FADE
    return t * t * (3.0 - 2.0 * t)


def noise(x, y, z):
    n = (
        math.sin(0.52 * x + 0.18 * y)
        + math.sin(0.48 * y + 0.20 * z + 0.7)
        + math.sin(0.50 * z + 0.22 * x + 1.4)
        + 0.5 * math.sin(1.15 * x + 0.92 * y + 0.4)
        + 0.5 * math.sin(1.08 * y + 0.88 * z + 1.9)
        + 0.5 * math.sin(0.98 * z + 1.12 * x + 2.6)
        + 0.25 * math.sin(2.4 * x + 1.7 * z + 0.9)
        + 0.25 * math.sin(2.2 * y + 2.3 * x + 1.5)
    )
    return n / 4.5


def outward_normal(x, y, z):
    rfb = math.hypot(y - MID_Y, z - Z_AXIS)
    rlr = math.hypot(x - MID_X, z - Z_AXIS)
    if abs(rfb - R_FB_O) <= abs(rlr - R_LR_O):
        nx, ny, nz = 0.0, y - MID_Y, z - Z_AXIS
    else:
        nx, ny, nz = x - MID_X, 0.0, z - Z_AXIS
    ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return nx / ln, ny / ln, nz / ln


def is_outer_face(face):
    s = face.Surface
    if hasattr(s, "Radius"):
        r = s.Radius
        return abs(r - R_FB_O) < 2.0 or abs(r - R_LR_O) < 2.0
    # groin-vault patches
    try:
        u0, u1, v0, v1 = face.ParameterRange[:4]
        p = face.valueAt((u0 + u1) / 2.0, (v0 + v1) / 2.0)
    except Exception:
        p = face.BoundBox.Center
    rfb = math.hypot(p.y - MID_Y, p.z - Z_AXIS)
    rlr = math.hypot(p.x - MID_X, p.z - Z_AXIS)
    return abs(rfb - R_FB_O) < 3.0 or abs(rlr - R_LR_O) < 3.0


def main():
    doc = App.getDocument(DOC_NAME) if DOC_NAME in [d.Name for d in App.listDocuments().values()] else App.ActiveDocument
    src = doc.getObject(SRC_NAME)
    if src is None:
        raise RuntimeError("Missing %s" % SRC_NAME)

    outer_faces = [f for f in src.Shape.Faces if is_outer_face(f)]
    print("outer faces", len(outer_faces))
    compound = Part.Compound(outer_faces)

    print("meshing outer walls MaxLength=%s ..." % MAX_LEN)
    raw = MeshPart.meshFromShape(Shape=compound, MaxLength=MAX_LEN)
    print("outer mesh", raw.CountPoints, "pts", raw.CountFacets, "tris")

    outer_pts = []
    inner_pts = []
    for p in raw.Points:
        x, y, z = p.x, p.y, p.z
        nx, ny, nz = outward_normal(x, y, z)
        fz = fade_z(z)
        disp = (BASE_OFFSET + AMP * 0.5 * (noise(x, y, z) + 1.0)) * fz
        outer_pts.append(Vector(x + nx * disp, y + ny * disp, z + nz * disp))
        inner_pts.append(Vector(x - nx * CRUST, y - ny * CRUST, z - nz * CRUST))

    tris = []
    for fac in raw.Facets:
        i, j, k = fac.PointIndices
        tris.append((outer_pts[i], outer_pts[j], outer_pts[k]))
        tris.append((inner_pts[i], inner_pts[k], inner_pts[j]))  # flipped

    # side walls on open edges
    from collections import Counter
    edge_count = Counter()
    for fac in raw.Facets:
        i, j, k = fac.PointIndices
        for e in (tuple(sorted((i, j))), tuple(sorted((j, k))), tuple(sorted((k, i)))):
            edge_count[e] += 1
    for (a, b), n in edge_count.items():
        if n != 1:
            continue
        tris.append((outer_pts[a], outer_pts[b], inner_pts[b]))
        tris.append((outer_pts[a], inner_pts[b], inner_pts[a]))

    crust = Mesh.Mesh(tris)
    print("crust", crust.CountPoints, "pts", crust.CountFacets, "tris")

    print("meshing body (coarse)...")
    body = MeshPart.meshFromShape(Shape=src.Shape, LinearDeflection=0.9, AngularDeflection=0.35, Relative=False)
    body.addMesh(crust)
    print("combined", body.CountPoints, "pts", body.CountFacets, "tris")

    if doc.getObject(OUT_MESH):
        doc.removeObject(OUT_MESH)
    obj = doc.addObject("Mesh::Feature", OUT_MESH)
    obj.Label = "lower base (cast texture)"
    obj.Mesh = body
    if obj.ViewObject:
        obj.ViewObject.ShapeColor = (0.32, 0.32, 0.34)
    if src.ViewObject:
        src.ViewObject.Visibility = False

    body.write(STL_PATH)
    print("wrote", STL_PATH)
    doc.recompute()


if __name__ == "__main__" or __name__ == "__builtin__":
    main()
