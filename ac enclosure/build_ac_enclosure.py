# AC enclosure for RAC02 and T92P11D22-12. F7 is inline, not on the box.
# 5052-H32 sheet, SendCutSend laser + bend. Units: mm. ASCII only.
#
# Material: 0.063 in 5052-H32 (SCS bending calculator, 90 deg):
#   T=0.063 in, IR=0.035 in, K=0.42, BD=0.096 in, die=0.472 in
#   min formed flange=0.303 in, bend relief depth=0.118 in
#   hole keep-out from bend CL = 1/2 die = 0.236 in
#   2:1 rule: base >= 2 * flange; inner 180 x 130 base vs 58 mm walls
#
# Upload to SCS as two formed STEP files (Box, Lid), 90 deg bends, no custom radius.
# Optional: add engraved labels (J1772 IN / TSM2500 / CP-PP).

import math
import os

import FreeCAD as App
import Part

OUT_DIR = "/Users/sfeldma/work/ih-53-ev/ac enclosure"
DOC_NAME = "ACEnclosure"

IN = 25.4
T = 0.063 * IN
IR = 0.035 * IN
K_FACTOR = 0.42
BD = 0.096 * IN
DIE_W = 0.472 * IN
MIN_FLANGE = 0.303 * IN
RELIEF_SPEC = 0.118 * IN
HOLE_KEEP = 0.5 * DIE_W
RELIEF = 3.5

INNER_L = 180.0
INNER_W = 130.0
INNER_H = 58.0
LID_FLANGE = 18.0
LID_GAP = 0.5
LID_GAP_Z = 0.4
LID_LIFT = 28.0

T92_CX = 100.0
T92_CY = 82.0
T92_PITCH = 59.56
T92_HOLE = 4.5
T92_BODY_L = 52.4
T92_BODY_W = 34.54
T92_BODY_H = 26.42
T92_OVERALL_H = 37.97
T92_FLANGE_L = 68.58
T92_FLANGE_T = 2.5
T92_TAB_H = T92_OVERALL_H - T92_BODY_H
T92_TAB_W = 6.35
T92_TAB_T = 0.81

RAC_CX = 48.0
RAC_CY = 32.0
RAC_PCB_L = 40.0
RAC_PCB_W = 30.0
RAC_PCB_T = 1.6
RAC_HOLE_DX = 32.0
RAC_HOLE_DY = 22.0
RAC_HOLE = 3.2
RAC_L = 33.70
RAC_W = 22.20
RAC_H = 17.75

PE_X = 18.0
PE_Y = 108.0
PE_HOLE = 6.6

MOUNT_INSET = 12.0
MOUNT_HOLE = 6.5

PG21 = 28.3
PG16 = 22.5
PG11 = 18.6
IN_Y = INNER_W / 2.0
IN_Z = 30.0
OUT_DJ_Y = 40.0
OUT_SIG_Y = 98.0
OUT_Z = 30.0

LID_SCREW = 4.3
LID_SCREW_X = 22.0
LID_SCREW_DOWN = 10.0

COLOR_AL = (0.72, 0.74, 0.76)
COLOR_LID = (0.62, 0.66, 0.70)
COLOR_T92 = (0.12, 0.12, 0.14)
COLOR_RAC = (0.18, 0.22, 0.48)
COLOR_PCB = (0.12, 0.42, 0.18)
COLOR_GLAND = (0.18, 0.18, 0.20)
COLOR_SS = (0.78, 0.78, 0.80)


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


def hex_prism(af, h):
    r = af / math.sqrt(3.0)
    pts = []
    for i in range(6):
        a = math.radians(30.0 + 60.0 * i)
        pts.append(App.Vector(r * math.cos(a), r * math.sin(a), 0.0))
    pts.append(pts[0])
    face = Part.Face(Part.makePolygon(pts))
    return face.extrude(App.Vector(0, 0, h))


def cut_cyl(solid, r, x, y, z, dx, dy, dz, length):
    n = App.Vector(dx, dy, dz)
    n.normalize()
    cyl = Part.makeCylinder(r, length, App.Vector(x, y, z), n)
    return solid.cut(cyl)


def open_tray(inner_l, inner_w, inner_h, relief):
    cavity = Part.makeBox(inner_l, inner_w, inner_h)
    bottom = [e for e in cavity.Edges if abs(e.CenterOfMass.z) < 1e-4]
    if len(bottom) != 4:
        raise RuntimeError("expected 4 bottom edges, got %s" % len(bottom))
    cavity = cavity.makeFillet(IR, bottom)
    top_faces = [f for f in cavity.Faces if f.CenterOfMass.z > inner_h - 0.8]
    if len(top_faces) != 1:
        raise RuntimeError("expected 1 top face, got %s" % len(top_faces))
    solid = cavity.makeThickness(top_faces, T, 1e-3)
    corners = ((0.0, 0.0), (inner_l, 0.0), (0.0, inner_w), (inner_l, inner_w))
    for cx, cy in corners:
        sx = (-T - 1.0) if cx == 0.0 else (cx - relief)
        sy = (-T - 1.0) if cy == 0.0 else (cy - relief)
        dx = T + 1.0 + relief
        dy = T + 1.0 + relief
        cutter = Part.makeBox(dx, dy, inner_h + T + 2.0, App.Vector(sx, sy, -T - 1.0))
        solid = solid.cut(cutter)
    return solid


def lid_inner_size():
    return INNER_L + 2.0 * T + 2.0 * LID_GAP, INNER_W + 2.0 * T + 2.0 * LID_GAP


def _lid_placement(lift=0.0):
    ll, lw = lid_inner_size()
    tx = -T - LID_GAP
    ty = lw - T - LID_GAP
    tz = INNER_H + LID_GAP_Z + lift
    return tx, ty, tz


def place_lid_over_box(lid_tray, lift=0.0):
    lid = lid_tray.copy()
    lid.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 180.0)
    tx, ty, tz = _lid_placement(lift)
    lid.translate(App.Vector(tx, ty, tz))
    return lid


def unplace_lid(lid_placed, lift=0.0):
    lid = lid_placed.copy()
    tx, ty, tz = _lid_placement(lift)
    lid.translate(App.Vector(-tx, -ty, -tz))
    lid.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -180.0)
    return lid


def cut_box_holes(box):
    z_floor = -T - 1.0
    depth = T + 2.0
    floor_holes = [
        (T92_CX - T92_PITCH / 2.0, T92_CY, T92_HOLE),
        (T92_CX + T92_PITCH / 2.0, T92_CY, T92_HOLE),
        (RAC_CX - RAC_HOLE_DX / 2.0, RAC_CY - RAC_HOLE_DY / 2.0, RAC_HOLE),
        (RAC_CX + RAC_HOLE_DX / 2.0, RAC_CY - RAC_HOLE_DY / 2.0, RAC_HOLE),
        (RAC_CX - RAC_HOLE_DX / 2.0, RAC_CY + RAC_HOLE_DY / 2.0, RAC_HOLE),
        (RAC_CX + RAC_HOLE_DX / 2.0, RAC_CY + RAC_HOLE_DY / 2.0, RAC_HOLE),
        (PE_X, PE_Y, PE_HOLE),
        (MOUNT_INSET, MOUNT_INSET, MOUNT_HOLE),
        (INNER_L - MOUNT_INSET, MOUNT_INSET, MOUNT_HOLE),
        (MOUNT_INSET, INNER_W - MOUNT_INSET, MOUNT_HOLE),
        (INNER_L - MOUNT_INSET, INNER_W - MOUNT_INSET, MOUNT_HOLE),
    ]
    for x, y, d in floor_holes:
        box = cut_cyl(box, d / 2.0, x, y, z_floor, 0, 0, 1, depth)

    wall_len = T + 8.0
    box = cut_cyl(box, PG21 / 2.0, -4.0, IN_Y, IN_Z, 1, 0, 0, wall_len)
    box = cut_cyl(box, PG16 / 2.0, INNER_L - 4.0, OUT_DJ_Y, OUT_Z, 1, 0, 0, wall_len)
    box = cut_cyl(box, PG11 / 2.0, INNER_L - 4.0, OUT_SIG_Y, OUT_Z, 1, 0, 0, wall_len)

    zs = INNER_H - LID_SCREW_DOWN
    r = LID_SCREW / 2.0
    for x in (LID_SCREW_X, INNER_L - LID_SCREW_X):
        box = cut_cyl(box, r, x, -6.0, zs, 0, 1, 0, 12.0)
        box = cut_cyl(box, r, x, INNER_W - 6.0, zs, 0, 1, 0, 12.0)
    return box


def cut_lid_holes(lid_placed):
    zs = INNER_H - LID_SCREW_DOWN
    r = LID_SCREW / 2.0
    for x in (LID_SCREW_X, INNER_L - LID_SCREW_X):
        lid_placed = cut_cyl(lid_placed, r, x, -12.0, zs, 0, 1, 0, 16.0)
        lid_placed = cut_cyl(lid_placed, r, x, INNER_W - 4.0, zs, 0, 1, 0, 16.0)
    return lid_placed


def dummy_t92():
    """Flange sits on the floor. Cover stands up. #250 QC terminals on the top face."""
    body = Part.makeBox(
        T92_BODY_L,
        T92_BODY_W,
        T92_BODY_H,
        App.Vector(-T92_BODY_L / 2.0, -T92_BODY_W / 2.0, 0.0),
    )
    flange = Part.makeBox(
        T92_FLANGE_L,
        T92_BODY_W,
        T92_FLANGE_T,
        App.Vector(-T92_FLANGE_L / 2.0, -T92_BODY_W / 2.0, 0.0),
    )
    flange = cut_cyl(
        flange, T92_HOLE / 2.0, -T92_PITCH / 2.0, 0.0, -1.0, 0, 0, 1, T92_FLANGE_T + 2.0
    )
    flange = cut_cyl(
        flange, T92_HOLE / 2.0, T92_PITCH / 2.0, 0.0, -1.0, 0, 0, 1, T92_FLANGE_T + 2.0
    )
    cover = body.fuse(flange)
    tabs = []
    # DPDT + coil: two rows of four .250 QC on the top of the cover.
    for x in (-18.0, -6.0, 6.0, 18.0):
        for y in (-12.7, 12.7):
            tab = Part.makeBox(
                T92_TAB_W,
                T92_TAB_T,
                T92_TAB_H,
                App.Vector(x - T92_TAB_W / 2.0, y - T92_TAB_T / 2.0, T92_BODY_H),
            )
            tabs.append(tab)
    qc = tabs[0]
    for t in tabs[1:]:
        qc = qc.fuse(t)
    cover.translate(App.Vector(T92_CX, T92_CY, 0.0))
    qc.translate(App.Vector(T92_CX, T92_CY, 0.0))
    return cover, qc


def dummy_rac02():
    pcb = Part.makeBox(
        RAC_PCB_L,
        RAC_PCB_W,
        RAC_PCB_T,
        App.Vector(RAC_CX - RAC_PCB_L / 2.0, RAC_CY - RAC_PCB_W / 2.0, 0.0),
    )
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            pcb = cut_cyl(
                pcb,
                RAC_HOLE / 2.0,
                RAC_CX + sx * RAC_HOLE_DX / 2.0,
                RAC_CY + sy * RAC_HOLE_DY / 2.0,
                -1.0,
                0,
                0,
                1,
                RAC_PCB_T + 2.0,
            )
    body = Part.makeBox(
        RAC_L,
        RAC_W,
        RAC_H,
        App.Vector(RAC_CX - RAC_L / 2.0, RAC_CY - RAC_W / 2.0, RAC_PCB_T),
    )
    return pcb, body


def dummy_gland(hole_d, y, z, x_face, inward):
    hex_af = hole_d + 6.0
    thread_l = T + 6.0
    hex_h = 6.0
    if inward > 0:
        origin_thread = App.Vector(x_face - 2.0, y, z)
        direction = App.Vector(1, 0, 0)
        hex_pos = App.Vector(x_face - 2.0 - hex_h, y, z)
    else:
        origin_thread = App.Vector(x_face + 2.0, y, z)
        direction = App.Vector(-1, 0, 0)
        hex_pos = App.Vector(x_face + 2.0 + hex_h, y, z)
    thread = Part.makeCylinder(hole_d / 2.0 - 0.2, thread_l, origin_thread, direction)
    nut = hex_prism(hex_af, hex_h)
    if inward > 0:
        nut.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90.0)
        nut.translate(hex_pos)
    else:
        nut.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), -90.0)
        nut.translate(App.Vector(x_face + 2.0, y, z))
    return thread.fuse(nut)


def dummy_pe_stud():
    stud = Part.makeCylinder(3.0, 16.0, App.Vector(PE_X, PE_Y, -2.0))
    wash = Part.makeCylinder(8.0, 1.2, App.Vector(PE_X, PE_Y, 0.0))
    nut = hex_prism(10.0, 5.0)
    nut.translate(App.Vector(PE_X, PE_Y, 1.2))
    return stud.fuse(wash).fuse(nut)


def add_label(doc, name, text, pos):
    a = doc.addObject("App::Annotation", name)
    a.LabelText = text
    a.Position = App.Vector(*pos)
    vo = a.ViewObject
    if vo:
        vo.FontSize = 12
        vo.TextColor = (1.0, 1.0, 1.0)
    return a


def fill_spreadsheet(doc):
    ss = doc.addObject("Spreadsheet::Sheet", "Dimensions")
    ll, lw = lid_inner_size()
    rows = [
        ("param", "value", "note"),
        ("material", "5052-H32", "SendCutSend"),
        ("thickness_in", 0.063, "SCS stock"),
        ("T_mm", round(T, 4), "0.063 in"),
        ("IR_mm", round(IR, 4), "SCS calculator 0.035 in"),
        ("K_factor", K_FACTOR, "SCS calculator"),
        ("BD_mm", round(BD, 4), "0.096 in at 90 deg"),
        ("die_mm", round(DIE_W, 4), "0.472 in"),
        ("hole_keep_mm", round(HOLE_KEEP, 3), "1/2 die from bend CL"),
        ("min_flange_mm", round(MIN_FLANGE, 3), "0.303 in formed"),
        ("relief_mm", RELIEF, "corner cut, spec depth 0.118 in"),
        ("inner_L", INNER_L, "cavity X"),
        ("inner_W", INNER_W, "cavity Y"),
        ("inner_H", INNER_H, "cavity Z, 2:1 vs 130 mm base"),
        ("outer_L", round(INNER_L + 2.0 * T, 3), "formed box"),
        ("outer_W", round(INNER_W + 2.0 * T, 3), "formed box"),
        ("outer_H", round(INNER_H + T, 3), "formed box"),
        ("lid_inner_L", round(ll, 3), "wraps outside box"),
        ("lid_inner_W", round(lw, 3), "wraps outside box"),
        ("lid_flange", LID_FLANGE, "min 7.7 mm"),
        ("T92_cx", T92_CX, "flange flat on floor"),
        ("T92_cy", T92_CY, "flange holes 59.56 mm c-c"),
        ("RAC_cx", RAC_CX, "carrier PCB 40 x 30"),
        ("RAC_cy", RAC_CY, "4x M3"),
        ("PE", "%s, %s" % (PE_X, PE_Y), "M6 chassis bond"),
        ("PG21_in", "%s, z=%s" % (IN_Y, IN_Z), "J1772 L/N/PE/PP/CP"),
        ("F7", "inline", "not on enclosure"),
        ("PG16_out", "%s, z=%s" % (OUT_DJ_Y, OUT_Z), "DJ7031-4.8 pigtail"),
        ("PG11_sig", "%s, z=%s" % (OUT_SIG_Y, OUT_Z), "CP/PP + coil to Orion"),
        ("lid_screws", "M4 x4", "long walls, 10 mm from rim"),
    ]
    for i, (a, b, c) in enumerate(rows, start=1):
        ss.set("A" + str(i), str(a))
        ss.set("B" + str(i), str(b))
        ss.set("C" + str(i), str(c))
    return ss


def export_steps(box, lid_tray, assembly):
    os.makedirs(OUT_DIR, exist_ok=True)
    box.exportStep(os.path.join(OUT_DIR, "ac_box.step"))
    lid_tray.exportStep(os.path.join(OUT_DIR, "ac_lid.step"))
    assembly.exportStep(os.path.join(OUT_DIR, "ac_enclosure_assembly.step"))


def main():
    for d in list(App.listDocuments().keys()):
        if d == DOC_NAME or App.getDocument(d).Label == DOC_NAME:
            App.closeDocument(d)

    doc = App.newDocument(DOC_NAME)
    fill_spreadsheet(doc)

    box = cut_box_holes(open_tray(INNER_L, INNER_W, INNER_H, RELIEF))
    ll, lw = lid_inner_size()
    lid_blank = open_tray(ll, lw, LID_FLANGE, RELIEF)
    lid_closed = cut_lid_holes(place_lid_over_box(lid_blank, lift=0.0))
    lid_open = lid_closed.copy()
    lid_open.translate(App.Vector(0.0, 0.0, LID_LIFT))
    lid_tray = unplace_lid(lid_closed, lift=0.0)

    t92, t92_qc = dummy_t92()
    rac_pcb, rac_body = dummy_rac02()
    g_in = dummy_gland(PG21, IN_Y, IN_Z, 0.0, 1)
    g_dj = dummy_gland(PG16, OUT_DJ_Y, OUT_Z, INNER_L, -1)
    g_sig = dummy_gland(PG11, OUT_SIG_Y, OUT_Z, INNER_L, -1)
    pe = dummy_pe_stud()

    add_shape(doc, "Box_5052", box, COLOR_AL)
    add_shape(doc, "Lid_5052", lid_open, COLOR_LID)
    add_shape(doc, "T92", t92, COLOR_T92)
    add_shape(doc, "T92_QC", t92_qc, COLOR_SS)
    add_shape(doc, "RAC02_PCB", rac_pcb, COLOR_PCB)
    add_shape(doc, "RAC02", rac_body, COLOR_RAC)
    add_shape(doc, "Gland_J1772", g_in, COLOR_GLAND)
    add_shape(doc, "Gland_DJ7031", g_dj, COLOR_GLAND)
    add_shape(doc, "Gland_Signal", g_sig, COLOR_GLAND)
    add_shape(doc, "PE_Stud", pe, COLOR_SS)

    add_label(doc, "Label_IN", ["J1772 IN  PG21", "L/N/PE/PP/CP"], (-45, IN_Y - 10, IN_Z + 20))
    add_label(doc, "Label_DJ", ["DJ7031 to TSM2500"], (INNER_L + 10, OUT_DJ_Y - 8, OUT_Z + 18))
    add_label(doc, "Label_SIG", ["CP/PP + CHARGE", "Charger_Safety"], (INNER_L + 10, OUT_SIG_Y - 8, OUT_Z + 18))
    add_label(doc, "Label_T92", ["T92P11D22-12"], (T92_CX - 30, T92_CY + 28, T92_OVERALL_H + 8))
    add_label(doc, "Label_RAC", ["RAC02-12SE/277"], (RAC_CX - 20, RAC_CY - 28, 25))

    doc.recompute()

    assembly = Part.makeCompound(
        [box, lid_open, t92, t92_qc, rac_pcb, rac_body, g_in, g_dj, g_sig, pe]
    )
    export_steps(box, lid_tray, assembly)

    path = os.path.join(OUT_DIR, "ac enclosure.FCStd")
    doc.saveAs(path)
    print("Saved", path)
    print("T_mm", round(T, 4), "IR_mm", round(IR, 4), "relief", RELIEF)
    print("Box inner", INNER_L, INNER_W, INNER_H)
    print("Box outer", round(INNER_L + 2 * T, 3), round(INNER_W + 2 * T, 3), round(INNER_H + T, 3))
    print("2:1 flange", INNER_H, "base min", 2 * INNER_H, "bases", INNER_L, INNER_W)
    print("hole keep", round(HOLE_KEEP, 2), "mount inset", MOUNT_INSET)
    print("lid inner", round(ll, 3), round(lw, 3), LID_FLANGE)
    bb = box.BoundBox
    print("box BB", round(bb.XMin, 2), round(bb.XMax, 2), round(bb.YMin, 2), round(bb.YMax, 2), round(bb.ZMin, 2), round(bb.ZMax, 2))
    return doc


doc = main()
