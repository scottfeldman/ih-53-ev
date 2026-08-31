# Through-wall M8 power terminal from the shop drawing + part photo.
# Run inside FreeCAD. Units: mm.
# Z=0 is the panel front (back of the insulator flange). +Z is the outside face.
# No clamp nut — the flange is an elongated diamond with two mounting holes.

import math
import os

import FreeCAD as App
import Part

OUT_DIR = "/Users/sfeldma/work/ih-53-ev/thru wall terminals"
DOC_NAME = "ThruWallTerminal"

# Drawing dimensions (±0.1 mm)
FRONT_TO_PANEL = 13.6
BARREL_L = 18.7
FLANGE_T = 7.0
FRONT_LIP = 3.4  # flared cover-retention lip at the top of the front post
FLARE_OD = 34.0

FLANGE_W = 34.0
HOLE_PITCH = 44.0
HOLE_DIA = 4.5
END_R = 6.5
BARREL_OD = 25.4
COPPER_OD = 17.5

M8_MAJOR = 8.0
M8_PITCH = 1.25
THREAD_DEPTH = 15.7
# FDM holes print small and thread valleys fill in. Enlarge the nut form so a
# real M8x1.25 bolt (major ~8.0, minor ~6.47) starts by hand. Pitch stays 1.25.
PRINT_CLEARANCE = 0.25  # mm per side
M8_PRINT_MAJOR = M8_MAJOR + 2.0 * PRINT_CLEARANCE  # 8.5
M8_PRINT_MINOR = (M8_MAJOR - 2.0 * (5.0 * (M8_PITCH * math.sqrt(3.0) / 2.0) / 8.0)) + 2.0 * PRINT_CLEARANCE
GROOVE_WIDEN = 0.10  # extra half-width so a 0.4 mm nozzle does not close the V

COLOR_PA66 = (0.82, 0.12, 0.12)
COLOR_CU = (0.85, 0.45, 0.12)


def add_shape(doc, name, shape, color, transparency=0):
    obj = doc.addObject("Part::Feature", name)
    obj.Label = name
    obj.Shape = shape
    vo = getattr(obj, "ViewObject", None)
    if vo is not None:
        vo.ShapeColor = color
        if transparency:
            vo.Transparency = transparency
    return obj


def cylinder_z(od, z0, z1, x=0.0, y=0.0):
    h = z1 - z0
    return Part.makeCylinder(od / 2.0, h, App.Vector(x, y, z0), App.Vector(0, 0, 1))


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def flange_hull_pts(n=64):
    R = FLANGE_W / 2.0
    samples = []
    for i in range(n):
        a = 2.0 * math.pi * i / n
        samples.append((R * math.cos(a), R * math.sin(a)))
        samples.append((-HOLE_PITCH / 2.0 + END_R * math.cos(a), END_R * math.sin(a)))
        samples.append((HOLE_PITCH / 2.0 + END_R * math.cos(a), END_R * math.sin(a)))
    return _convex_hull(samples)


def m8_internal_cutter(z_low, height):
    """RH M8x1.25 internal cutter, oversized for FDM so a real bolt fits."""
    r_maj = M8_PRINT_MAJOR / 2.0
    r_min = M8_PRINT_MINOR / 2.0
    h = r_maj - r_min
    half = h * math.tan(math.radians(30.0)) + GROOVE_WIDEN
    pad = M8_PITCH * 0.5
    helix_h = height + M8_PITCH
    n_per_turn = 10
    n = int(round(n_per_turn * helix_h / M8_PITCH)) + 1
    wires = []
    for i in range(n):
        z = i * helix_h / (n - 1)
        rot = App.Rotation(App.Vector(0, 0, 1), 360.0 * z / M8_PITCH)
        q = []
        for x, zz in (
            (r_min - 0.25, -half),
            (r_maj + 0.10, -0.08),
            (r_maj + 0.10, 0.08),
            (r_min - 0.25, half),
        ):
            v = rot.multVec(App.Vector(x, 0, zz))
            v.z += z
            q.append(v)
        q.append(q[0])
        wires.append(Part.Wire(Part.makePolygon(q)))
    coil = Part.makeLoft(wires, True, False)
    core = Part.makeCylinder(
        r_min, helix_h + 0.4, App.Vector(0, 0, -0.2), App.Vector(0, 0, 1)
    )
    cutter = core.fuse(coil)
    cutter.translate(App.Vector(0, 0, z_low - pad))
    return cutter


def flange_plate(z0, z1):
    pts = [App.Vector(x, y, z0) for x, y in flange_hull_pts()]
    pts.append(pts[0])
    solid = Part.Face(Part.makePolygon(pts)).extrude(App.Vector(0, 0, z1 - z0))
    solid = solid.cut(cylinder_z(COPPER_OD, z0 - 0.1, z1 + 0.1))
    for x in (-HOLE_PITCH / 2.0, HOLE_PITCH / 2.0):
        solid = solid.cut(cylinder_z(HOLE_DIA, z0 - 0.1, z1 + 0.1, x=x))
    return solid


def build():
    if DOC_NAME in App.listDocuments():
        App.closeDocument(DOC_NAME)
    doc = App.newDocument(DOC_NAME)

    z_front = FRONT_TO_PANEL
    z_panel = 0.0
    z_rear = -BARREL_L
    z_flange_front = FLANGE_T
    z_flare = z_front - FRONT_LIP

    copper = cylinder_z(COPPER_OD, z_rear, z_front)
    copper = copper.cut(m8_internal_cutter(z_front - THREAD_DEPTH, THREAD_DEPTH))
    copper = copper.cut(m8_internal_cutter(z_rear, THREAD_DEPTH))
    chamfer = 1.0
    for z_face, sign in ((z_front, -1.0), (z_rear, 1.0)):
        cone = Part.makeCone(
            M8_PRINT_MAJOR / 2.0 + 0.5,
            M8_PRINT_MINOR / 2.0,
            chamfer,
            App.Vector(0, 0, z_face + (0.05 if sign < 0 else -chamfer - 0.05)),
            App.Vector(0, 0, sign),
        )
        copper = copper.cut(cone)

    # Neck Ø25.4 with a rounded Ø34 bead (no sharp rim) so a boot slips over.
    r_cu = COPPER_OD / 2.0
    r_neck = BARREL_OD / 2.0
    r_fl = FLARE_OD / 2.0
    bead_r = FRONT_LIP / 2.0
    cx, cz = r_fl - bead_r, z_front - bead_r
    p1 = App.Vector(r_cu, 0, z_front)
    p2 = App.Vector(cx, 0, z_front)
    p3 = App.Vector(r_fl, 0, cz)
    p4 = App.Vector(cx, 0, z_flare)
    p5 = App.Vector(r_neck, 0, z_flare)
    p6 = App.Vector(r_neck, 0, z_flange_front)
    p7 = App.Vector(r_cu, 0, z_flange_front)
    front_wire = Part.Wire(
        [
            Part.makeLine(p1, p2),
            Part.Arc(p2, p3, p4).toShape(),
            Part.makeLine(p4, p5),
            Part.makeLine(p5, p6),
            Part.makeLine(p6, p7),
            Part.makeLine(p7, p1),
        ]
    )
    front_post = Part.Face(front_wire).revolve(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 360)

    flange = flange_plate(z_panel, z_flange_front)
    # Barrel meets the flat back of the flange — no extra ring.
    barrel = cylinder_z(BARREL_OD, z_rear, z_panel).cut(
        cylinder_z(COPPER_OD, z_rear - 0.1, z_panel + 0.1)
    )

    insulator = flange.fuse(front_post).fuse(barrel).removeSplitter()

    add_shape(doc, "Insulator_PA66", insulator, COLOR_PA66)
    add_shape(doc, "Conductor_Copper", copper, COLOR_CU)

    assembly = insulator.fuse(copper).removeSplitter()
    add_shape(doc, "ThruWall_M8_Assembly", assembly, COLOR_CU)
    doc.getObject("ThruWall_M8_Assembly").Visibility = False

    doc.recompute()

    os.makedirs(OUT_DIR, exist_ok=True)
    fcstd = os.path.join(OUT_DIR, "thru wall terminals.FCStd")
    step = os.path.join(OUT_DIR, "ThruWall_M8.step")
    doc.saveAs(fcstd)
    assembly.exportStep(step)

    bb_i = insulator.BoundBox
    bb_c = copper.BoundBox
    stl = os.path.join(OUT_DIR, "ThruWall_M8.stl")
    assembly.exportStl(stl)
    print("Saved", fcstd)
    print("Saved", step)
    print("Saved", stl)
    print(
        "print M8 minor {:.2f} major {:.2f} pitch {:.2f}".format(
            M8_PRINT_MINOR, M8_PRINT_MAJOR, M8_PITCH
        )
    )
    print(
        "insulator X {:.2f}:{:.2f} Y {:.2f}:{:.2f} Z {:.2f}:{:.2f}".format(
            bb_i.XMin, bb_i.XMax, bb_i.YMin, bb_i.YMax, bb_i.ZMin, bb_i.ZMax
        )
    )
    print(
        "copper X {:.2f}:{:.2f} Z {:.2f}:{:.2f}".format(
            bb_c.XMin, bb_c.XMax, bb_c.ZMin, bb_c.ZMax
        )
    )
    return doc


if __name__ == "__main__":
    build()
