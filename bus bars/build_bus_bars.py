# Build HV copper bus bars TB1/TB2/TB3 on an SM40-M10 standoff.
# Run inside FreeCAD. Units: mm.
# Schematic: 2x 5/16-18 (2/0) + 2x #10-32 (10/18 AWG HV).
# SM40: H=40, face OD=40, waist=34, M10 inserts 11 mm both ends (BMC SM-40-M10).

import math
import os

import FreeCAD as App
import Part

OUT_DIR = "/Users/sfeldma/work/ih-53-ev/bus bars"
DOC_NAME = "BusBars"

# --- copper blank from one C110 1/4 x 4 x 12 plate ---
# 2.5" wide: 2/0 palms 16 mm from each long edge (31.5 mm c-c) so traction
# cables can come in at an angle. 85 mm long: SM40 sits toward the #10 end
# because 5/16 USS washers need more face clearance than #10 washers.
# #10 holes are 10 mm from the short edge (washer OD 12.7).
BAR_L = 85.0
BAR_W = 63.5
BAR_T = 6.35

# 5/16 (2/0) on the X1 end, #10-32 on the X2 end.
STUD_X1 = 16.0
STUD_X2 = 75.0
STUD_Y1 = 16.0
STUD_Y2 = BAR_W - 16.0

# SM40 offset toward the #10 end; M10 through-hole in copper
MOUNT_X = 48.0
MOUNT_Y = BAR_W / 2.0
HOLE_M10 = 11.0

DIA_516 = 7.938
DIA_10 = 4.826
HOLE_516 = 8.2
HOLE_10 = 5.0
STUD_H_516 = 22.0
STUD_H_10 = 16.0

NUT_AF_516 = 12.7
NUT_H_516 = 7.1
NUT_AF_10 = 9.53
NUT_H_10 = 3.18
HEAD_H_516 = 5.2
HEAD_H_10 = 3.2
WASH_OD_516 = 22.2
WASH_ID_516 = 8.4
WASH_T_516 = 2.0
WASH_OD_10 = 12.7
WASH_ID_10 = 5.0
WASH_T_10 = 1.2

# --- SM40 catalog ---
SM40_H = 40.0
SM40_OD = 40.0
SM40_WAIST = 34.0
SM40_INSERT_DEPTH = 11.0
SM40_INSERT_OD = 13.0
M10_DIA = 10.0
M10_HEAD_AF = 17.0
M10_HEAD_H = 6.4
M10_WASH_OD = 20.0
M10_WASH_T = 2.0

PITCH_Y = BAR_W + 50.0

COLOR_CU = (0.85, 0.45, 0.12)
COLOR_SS = (0.78, 0.78, 0.80)
COLOR_ZINC = (0.72, 0.74, 0.70)
COLOR_SM40 = (0.78, 0.16, 0.12)
COLOR_HEAD_BOT = (0.95, 0.72, 0.12)
COLOR_LUG = (0.25, 0.25, 0.28)


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


def washer(od, id_, t):
    return Part.makeCylinder(od / 2.0, t).cut(
        Part.makeCylinder(id_ / 2.0, t + 0.2, App.Vector(0, 0, -0.1))
    )


def place_xy(shape, x, y, z=0.0):
    s = shape.copy()
    s.translate(App.Vector(x, y, z))
    return s


def ring_lug(x, y, z, dir_x, tongue_w, tongue_back, barrel_r, barrel_l):
    """Keep-out: palm on the bar, barrel hanging off the end along X (dir_x +1 or -1)."""
    tip_x = 0.0 if dir_x < 0 else BAR_L
    if dir_x < 0:
        palm_x0 = min(tip_x, x + tongue_back)
        palm_x1 = max(tip_x, x + tongue_back)
    else:
        palm_x0 = min(tip_x, x - tongue_back)
        palm_x1 = max(tip_x, x - tongue_back)
    palm = Part.makeBox(
        palm_x1 - palm_x0,
        tongue_w,
        3.5,
        App.Vector(palm_x0, y - tongue_w / 2.0, z),
    )
    start = App.Vector(tip_x, y, z + barrel_r)
    barrel = Part.makeCylinder(barrel_r, barrel_l, start, App.Vector(dir_x, 0, 0))
    return palm.fuse(barrel)


def copper_bar():
    bar = Part.makeBox(BAR_L, BAR_W, BAR_T)
    holes = [
        (STUD_X1, STUD_Y1, HOLE_516),
        (STUD_X1, STUD_Y2, HOLE_516),
        (STUD_X2, STUD_Y1, HOLE_10),
        (STUD_X2, STUD_Y2, HOLE_10),
        (MOUNT_X, MOUNT_Y, HOLE_M10),
    ]
    for x, y, d in holes:
        bar = bar.cut(Part.makeCylinder(d / 2.0, BAR_T + 2.0, App.Vector(x, y, -1.0)))
    try:
        bar = bar.makeChamfer(0.8, [e for e in bar.Edges if e.Length > 40])
    except Exception:
        pass
    return bar


def stud_stack(x, y, dia, h_above, wash_od, wash_id, wash_t, nut_af, nut_h, head_h, bar_z):
    """Through-bolt: hex head + washer under the bar, washer + nut on top."""
    stud = Part.makeCylinder(
        dia / 2.0,
        BAR_T + h_above + wash_t + head_h,
        App.Vector(x, y, bar_z - wash_t - head_h),
    )
    w_top = place_xy(washer(wash_od, wash_id, wash_t), x, y, bar_z + BAR_T)
    n = hex_prism(nut_af, nut_h)
    n.translate(App.Vector(x, y, bar_z + BAR_T + wash_t))
    w_bot = place_xy(washer(wash_od, wash_id, wash_t), x, y, bar_z - wash_t)
    head = hex_prism(nut_af, head_h)
    head.translate(App.Vector(x, y, bar_z - wash_t - head_h))
    return stud, w_top, n, w_bot, head


def sm40_body():
    """BMC SM40 spool: 40 mm faces, 34 mm waist, mid rib, 40 mm tall."""
    r_od = SM40_OD / 2.0
    r_w = SM40_WAIST / 2.0
    h = SM40_H
    pts = [
        App.Vector(0, 0, 0),
        App.Vector(r_od, 0, 0),
        App.Vector(r_od, 0, 6.5),
        App.Vector(r_w, 0, 9.0),
        App.Vector(r_w, 0, 16.5),
        App.Vector(r_od, 0, 18.0),
        App.Vector(r_od, 0, 22.0),
        App.Vector(r_w, 0, 23.5),
        App.Vector(r_w, 0, 31.0),
        App.Vector(r_od, 0, 33.5),
        App.Vector(r_od, 0, h),
        App.Vector(0, 0, h),
        App.Vector(0, 0, 0),
    ]
    face = Part.Face(Part.makePolygon(pts))
    body = face.revolve(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 360)
    # M10 tapped pockets (inserts sit in these)
    r_pocket = SM40_INSERT_OD / 2.0 + 0.15
    body = body.cut(Part.makeCylinder(r_pocket, SM40_INSERT_DEPTH + 0.2, App.Vector(0, 0, -0.1)))
    body = body.cut(
        Part.makeCylinder(
            r_pocket,
            SM40_INSERT_DEPTH + 0.2,
            App.Vector(0, 0, h - SM40_INSERT_DEPTH),
        )
    )
    return body


def sm40_inserts():
    """M10 inserts, 11 mm deep, both faces."""
    r_o = SM40_INSERT_OD / 2.0
    r_i = 8.5 / 2.0  # M10x1.5 tap drill
    def insert_at(z):
        tube = Part.makeCylinder(r_o, SM40_INSERT_DEPTH, App.Vector(0, 0, z))
        return tube.cut(
            Part.makeCylinder(r_i, SM40_INSERT_DEPTH + 0.4, App.Vector(0, 0, z - 0.2))
        )

    return insert_at(0.0), insert_at(SM40_H - SM40_INSERT_DEPTH)


def m10_bolt(z_head_bottom, head_up=True):
    """Hex-head M10. Shaft points down if head_up else up from z_head_bottom."""
    head = hex_prism(M10_HEAD_AF, M10_HEAD_H)
    if head_up:
        head.translate(App.Vector(0, 0, z_head_bottom))
        shaft_len = BAR_T + M10_WASH_T + SM40_INSERT_DEPTH - 1.0
        shaft = Part.makeCylinder(
            M10_DIA / 2.0,
            shaft_len,
            App.Vector(0, 0, z_head_bottom - shaft_len + 0.2),
        )
    else:
        head.translate(App.Vector(0, 0, z_head_bottom - M10_HEAD_H))
        shaft_len = SM40_INSERT_DEPTH + 2.0
        shaft = Part.makeCylinder(M10_DIA / 2.0, shaft_len, App.Vector(0, 0, z_head_bottom - 0.2))
    return head.fuse(shaft)


def sm40_at(x, y, z=0.0):
    body = sm40_body()
    ins_bot, ins_top = sm40_inserts()
    for sh in (body, ins_bot, ins_top):
        sh.translate(App.Vector(x, y, z))
    return body, ins_bot, ins_top


def build_one(doc, prefix, origin):
    ox, oy, oz = origin
    bar_z = SM40_H
    mx, my = ox + MOUNT_X, oy + MOUNT_Y

    bar = copper_bar()
    bar.translate(App.Vector(ox, oy, oz + bar_z))

    hardware = []
    underside = []
    for x, y, dia, h, wod, wid, wt, af, nh, hh in (
        (STUD_X1, STUD_Y1, DIA_516, STUD_H_516, WASH_OD_516, WASH_ID_516, WASH_T_516, NUT_AF_516, NUT_H_516, HEAD_H_516),
        (STUD_X1, STUD_Y2, DIA_516, STUD_H_516, WASH_OD_516, WASH_ID_516, WASH_T_516, NUT_AF_516, NUT_H_516, HEAD_H_516),
        (STUD_X2, STUD_Y1, DIA_10, STUD_H_10, WASH_OD_10, WASH_ID_10, WASH_T_10, NUT_AF_10, NUT_H_10, HEAD_H_10),
        (STUD_X2, STUD_Y2, DIA_10, STUD_H_10, WASH_OD_10, WASH_ID_10, WASH_T_10, NUT_AF_10, NUT_H_10, HEAD_H_10),
    ):
        st, w, n, w_bot, head = stud_stack(x, y, dia, h, wod, wid, wt, af, nh, hh, bar_z)
        for sh in (st, w, n, w_bot, head):
            sh.translate(App.Vector(ox, oy, oz))
        hardware.extend((st, w, n))
        underside.extend((w_bot, head))

    body, ins_bot, ins_top = sm40_at(mx, my, oz)

    wash = place_xy(washer(M10_WASH_OD, HOLE_M10, M10_WASH_T), mx, my, oz + bar_z + BAR_T)
    top_bolt = m10_bolt(oz + bar_z + BAR_T + M10_WASH_T, head_up=True)
    top_bolt.translate(App.Vector(mx, my, 0))
    bot_bolt = m10_bolt(oz, head_up=False)
    bot_bolt.translate(App.Vector(mx, my, 0))
    hardware.extend((wash, top_bolt, bot_bolt))

    lug_z = oz + bar_z + BAR_T
    lugs = [
        ring_lug(ox + STUD_X1, oy + STUD_Y1, lug_z, -1, 22.0, 10.0, 8.0, 32.0),
        ring_lug(ox + STUD_X1, oy + STUD_Y2, lug_z, -1, 22.0, 10.0, 8.0, 32.0),
        ring_lug(ox + STUD_X2, oy + STUD_Y1, lug_z, 1, 11.0, 7.0, 4.5, 20.0),
        ring_lug(ox + STUD_X2, oy + STUD_Y2, lug_z, 1, 11.0, 7.0, 4.5, 20.0),
    ]

    grp = doc.addObject("App::DocumentObjectGroup", prefix)
    grp.Label = prefix
    objs = [
        add_shape(doc, prefix + "_Copper", bar, COLOR_CU),
        add_shape(doc, prefix + "_Hardware", Part.makeCompound(hardware), COLOR_SS),
        add_shape(doc, prefix + "_StudHeadsBottom", Part.makeCompound(underside), COLOR_HEAD_BOT),
        add_shape(doc, prefix + "_SM40", body, COLOR_SM40),
        add_shape(doc, prefix + "_Inserts", ins_bot.fuse(ins_top), COLOR_ZINC),
        add_shape(doc, prefix + "_LugKeepout", Part.makeCompound(lugs), COLOR_LUG, transparency=50),
    ]
    for o in objs:
        grp.addObject(o)
    return grp


def add_label(doc, name, text, pos):
    a = doc.addObject("App::Annotation", name)
    a.LabelText = text
    a.Position = App.Vector(*pos)
    vo = a.ViewObject
    if vo:
        vo.FontSize = 14
        vo.TextColor = (1.0, 1.0, 1.0)
    return a


def fill_spreadsheet(doc):
    ss = doc.addObject("Spreadsheet::Sheet", "Dimensions")
    rows = [
        ("param", "mm", "note"),
        ("bar_L", BAR_L, "3.35 in, SM40 offset to #10 end"),
        ("bar_W", BAR_W, "2.5 in for angled 2/0"),
        ("bar_T", BAR_T, "1/4 in plate"),
        ("stud_x1", STUD_X1, "5/16 2/0 column"),
        ("stud_x2", STUD_X2, "#10-32, 10 mm from end"),
        ("stud_y1", STUD_Y1, "row A, 16 mm from edge"),
        ("stud_y2", STUD_Y2, "row B, 16 mm from edge"),
        ("mount_x", MOUNT_X, "SM40 / M10, toward #10"),
        ("mount_y", MOUNT_Y, "SM40 / M10 hole center"),
        ("hole_M10", HOLE_M10, "clearance through bar into SM40"),
        ("SM40_H", SM40_H, "catalog height"),
        ("SM40_OD", SM40_OD, "face diameter"),
        ("SM40_waist", SM40_WAIST, "socket / waist"),
        ("SM40_insert", "M10 x 11", "both ends"),
        ("creepage_air_gap", 50.0, "between adjacent bars"),
        ("section_mm2", round(BAR_W * BAR_T, 1), "copper cross section"),
    ]
    for i, (a, b, c) in enumerate(rows, start=1):
        ss.set("A" + str(i), str(a))
        ss.set("B" + str(i), str(b))
        ss.set("C" + str(i), str(c))
    return ss


def export_steps(bar_shape, sm40_shape, assembly_shape):
    os.makedirs(OUT_DIR, exist_ok=True)
    bar_shape.exportStep(os.path.join(OUT_DIR, "copper_bar.step"))
    sm40_shape.exportStep(os.path.join(OUT_DIR, "sm40.step"))
    assembly_shape.exportStep(os.path.join(OUT_DIR, "bus_bars_assembly.step"))
    stale = (
        "insulator_saddle.step",
        "insulator_saddle.stl",
        "insulator_cap.step",
        "insulator_cap.stl",
    )
    for name in stale:
        path = os.path.join(OUT_DIR, name)
        if os.path.exists(path):
            os.remove(path)
    try:
        import MeshPart

        mesh = MeshPart.meshFromShape(Shape=sm40_shape, LinearDeflection=0.12, AngularDeflection=0.3)
        mesh.write(os.path.join(OUT_DIR, "sm40.stl"))
    except Exception as exc:
        print("STL export skipped:", exc)


def main():
    target_path = os.path.abspath(os.path.join(OUT_DIR, "bus bars.FCStd"))
    for d in list(App.listDocuments().keys()):
        existing = App.getDocument(d)
        existing_path = os.path.abspath(existing.FileName) if existing.FileName else ""
        if d == DOC_NAME or existing.Label in (DOC_NAME, "bus bars") or existing_path == target_path:
            App.closeDocument(d)

    doc = App.newDocument(DOC_NAME)
    fill_spreadsheet(doc)

    master_bar = add_shape(doc, "Master_CopperBar", copper_bar(), COLOR_CU)
    master_sm40 = add_shape(doc, "Master_SM40", sm40_body(), COLOR_SM40)
    masters = doc.addObject("App::DocumentObjectGroup", "Masters")
    for o in (master_bar, master_sm40):
        masters.addObject(o)
        if o.ViewObject:
            o.ViewObject.Visibility = False

    build_one(doc, "TB1_PackPlus_Rear", (0.0, 0.0, 0.0))
    build_one(doc, "TB2_PackMinus", (0.0, PITCH_Y, 0.0))
    build_one(doc, "TB3_PackPlus_Inverter", (0.0, 2.0 * PITCH_Y, 0.0))

    add_label(doc, "Label_TB1", ["TB1  pack +  rear"], (0, -28, 70))
    add_label(doc, "Label_TB2", ["TB2  pack -"], (0, PITCH_Y - 28, 70))
    add_label(doc, "Label_TB3", ["TB3  pack +  inverter"], (0, 2.0 * PITCH_Y - 28, 70))

    doc.recompute()

    parts = [
        o.Shape
        for o in doc.Objects
        if o.TypeId == "Part::Feature"
        and not o.Name.startswith("Master")
        and "LugKeepout" not in o.Name
        and hasattr(o, "Shape")
        and not o.Shape.isNull()
        and o.ViewObject is not None
        and o.ViewObject.Visibility
    ]
    assembly = Part.makeCompound(parts) if parts else master_bar.Shape
    export_steps(master_bar.Shape, master_sm40.Shape, assembly)

    path = os.path.join(OUT_DIR, "bus bars.FCStd")
    doc.saveAs(path)
    print("Saved", path)
    dx516 = abs(STUD_X1 - MOUNT_X)
    dx10 = abs(STUD_X2 - MOUNT_X)
    dy = abs(STUD_Y1 - MOUNT_Y)
    print("Bar", BAR_L, "x", BAR_W, "x", BAR_T, "mm; SM40 at", MOUNT_X, MOUNT_Y)
    print("5/16 c-c (rows)", round(abs(STUD_Y2 - STUD_Y1), 1), "  5/16 to #10 (ends)", abs(STUD_X2 - STUD_X1))
    print("5/16 to M10", round((dx516**2 + dy**2) ** 0.5, 1), "  #10 to M10", round((dx10**2 + dy**2) ** 0.5, 1))
    print("From 4x12 plate: 2.5 x 3.35 in blanks; 2/0 palm gap", round(abs(STUD_Y2 - STUD_Y1) - 22.0, 1), "mm")
    return doc


doc = main()
