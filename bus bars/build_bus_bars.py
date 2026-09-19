# Build HV copper bus bars TB1/TB2/TB3 on an SM40-M10 standoff.
# Run inside FreeCAD. Units: mm.
# Schematic: 2x 5/16-18 (2/0) + 2x 1/4-20 (10/18 AWG HV).
# SM40: H=40, face OD=40, waist=34, M10 inserts 11 mm both ends (BMC SM-40-M10).

import math
import os

import FreeCAD as App
import Part

OUT_DIR = "/Users/sfeldma/work/ih-53-ev/bus bars"
DOC_NAME = "BusBars"

# --- copper blank from one C110 1/4 x 4 x 12 plate ---
# 2.5" wide: 2/0 palms 16 mm from each long edge (31.5 mm c-c) so traction
# cables can come in at an angle. 90 mm long: SM40 sits toward the 1/4-20 end
# because 5/16 USS washers need more face clearance than 1/4 USS washers.
# 1/4-20 holes are 12 mm from the short edge (USS washer OD 18.6).
BAR_L = 90.0
BAR_W = 63.5
BAR_T = 6.35

# 5/16 (2/0) on the X1 end, 1/4-20 on the X2 end.
STUD_X1 = 16.0
STUD_X2 = 78.0
STUD_Y1 = 16.0
STUD_Y2 = BAR_W - 16.0

# SM40 offset toward the 1/4-20 end; M10 through-hole in copper
MOUNT_X = 48.0
MOUNT_Y = BAR_W / 2.0
HOLE_M10 = 11.0

DIA_516 = 7.938
DIA_14 = 6.35
HOLE_516 = 8.2
HOLE_14 = 6.8
STUD_H_516 = 22.0
STUD_H_14 = 18.0

NUT_AF_516 = 12.7
NUT_H_516 = 7.1
NUT_AF_14 = 11.11
NUT_H_14 = 5.6
HEAD_H_516 = 5.2
HEAD_H_14 = 4.0
WASH_OD_516 = 22.2
WASH_ID_516 = 8.4
WASH_T_516 = 2.0
WASH_OD_14 = 18.6
WASH_ID_14 = 7.1
WASH_T_14 = 1.6

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
M10_NUT_H = 8.0

# Rincon HVBD series (HVBD6AXR) datasheet REV P
# https://downloads.rinconpower.com/hvbd-series-datasheet.pdf
HVBD_STUD_CC = 31.8
HVBD_BODY_OD = 68.6
HVBD_STUD_LEN = 19.1
HVBD_MOUNT_CC = 100.1
HVBD_MOUNT_HOLE = 8.33
HVBD_FLANGE_T = 5.8
HVBD_SIDE_R = 38.74
HVBD_EAR_R = 8.64
HVBD_FRONT = 29.4
HVBD_REAR = 40.7
HVBD_LOTO = 8.2
HVBD_COLLAR_OD = 64.0
HVBD_KNOB_OD = 54.0
HVBD_REAR_BOSS_OD = 62.0

# TB1-TB2: 165 mm SM40 centers so ~50 mm air remains if both bars
# yaw a full turn around the M10 (copper circumradius 57.5 mm).
# TB2-TB3 keep the original 50 mm aligned air gap.
PITCH_TB12 = 165.0
PITCH_TB23 = BAR_W + 50.0

# Anderson SB350 (DS-SB350): housing 107.9 x 69.9 x 33.3, mated 182.6, poles 34.9
SB350_L = 107.9
SB350_W = 69.9
SB350_H = 33.3
SB350_MATED = 182.6
SB350_POLE_CC = 34.9
SB350_CONTACT_L = 75.2
DLO_2_0_OD = 16.5
LUG_516_BARREL_L = 32.0
LUG_516_BARREL_R = 8.0

# Mersen 1SCM10 pair (drawing 701314) + A25X500-4 Form 101
# 1SCM8 is 400 A / M8; 500 A fuse uses 1SCM10 (800 A / M10).
SCM10_BASE_L = 53.8
SCM10_BASE_W = 25.4
SCM10_H = 97.0
SCM10_FOOT_H = 12.8
SCM10_BOSS_H = 61.3
SCM10_STUD_STACK = 35.7
SCM10_PAD_L = 42.9
SCM10_PAD_T = 5.2
A25X_L = 97.5
A25X_OD = 38.1
A25X_HOLE_CC = 73.9
A25X_HOLE = 10.4
A25X_BLADE_W = 25.4
A25X_BLADE_T = 6.4
A25X_BODY_L = 57.9
PLATE_T = 6.35
PLATE_MARGIN = 16.0
PLATE_HOLE_R = 3.5
F4_PLATE_T = PLATE_T
HOLE_M6 = 6.6
HOLE_M8 = 9.0
M8_DIA = 8.0
M8_HEAD_AF = 13.0
M8_HEAD_H = 5.3
M8_NUT_H = 6.5
SW1_POST_AF = 19.0
SW1_PAD_T = 6.35
SW1_CY_OFF = 50.0
COVER_WALL = 3.0
COVER_LID_T = 3.0
COVER_CLEAR = 32.0
COVER_INNER_H = 115.0
COVER_SCREW_INSET = 10.0
COVER_SW1_HOLE_R = HVBD_COLLAR_OD / 2.0 + 16.0
COVER_CB_MARGIN = 6.0

# CHTAIXI DZ47Z-63 2P 1000 V DC MCB (Amazon B0983ZHK69 32 A, B09BQQCV3P 10 A)
# Listing: 2.95 x 1.42 x 3.15 in. Follow marked +/- ; LINE toward pack.
AWG10_OD = 7.5
MCB_W = 36.0
MCB_D = 75.0
MCB_H = 80.0
MCB_MOD = 18.0
MCB_GAP = 10.0
DIN_W = 35.0
DIN_H = 7.5
LUG_14_BARREL_L = 20.0
LUG_14_BARREL_R = 4.5

COLOR_CU = (0.85, 0.45, 0.12)
COLOR_SS = (0.78, 0.78, 0.80)
COLOR_ZINC = (0.72, 0.74, 0.70)
COLOR_SM40 = (0.78, 0.16, 0.12)
COLOR_HEAD_BOT = (0.95, 0.72, 0.12)
COLOR_LUG = (0.25, 0.25, 0.28)
COLOR_HVBD = (0.18, 0.18, 0.20)
COLOR_HVBD_HANDLE = (0.78, 0.10, 0.10)
COLOR_SB350 = (0.88, 0.38, 0.08)
COLOR_DLO = (0.92, 0.42, 0.08)
COLOR_SB350_HANDLE = (0.22, 0.22, 0.24)
COLOR_SCM10 = (0.10, 0.10, 0.11)
COLOR_FUSE = (0.82, 0.74, 0.52)
COLOR_PLATE = (0.55, 0.56, 0.58)
COLOR_COVER = (0.42, 0.45, 0.48)
COLOR_MCB = (0.91, 0.91, 0.89)
COLOR_MCB_TOGGLE = (0.14, 0.14, 0.16)
COLOR_DIN = (0.62, 0.64, 0.66)
COLOR_HV_RED = (0.78, 0.12, 0.12)
COLOR_HV_BLK = (0.10, 0.10, 0.12)


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


def offbar_lug(x, y, z, dir_x, tongue_w, tongue_back, barrel_r, barrel_l):
    """Palm on a stud that is not on the bar; barrel along +/- X from the stud."""
    if dir_x < 0:
        palm = Part.makeBox(
            tongue_back, tongue_w, 3.5, App.Vector(x - tongue_back, y - tongue_w / 2.0, z)
        )
        start = App.Vector(x - tongue_back, y, z + barrel_r)
    else:
        palm = Part.makeBox(
            tongue_back, tongue_w, 3.5, App.Vector(x, y - tongue_w / 2.0, z)
        )
        start = App.Vector(x + tongue_back, y, z + barrel_r)
    barrel = Part.makeCylinder(barrel_r, barrel_l, start, App.Vector(dir_x, 0, 0))
    return palm.fuse(barrel)


def offbar_lug_y(x, y, z, dir_y, tongue_w, tongue_back, barrel_r, barrel_l):
    """Palm on a stud; barrel along +/- Y."""
    if dir_y < 0:
        palm = Part.makeBox(
            tongue_w, tongue_back, 3.5, App.Vector(x - tongue_w / 2.0, y - tongue_back, z)
        )
        start = App.Vector(x, y - tongue_back, z + barrel_r)
    else:
        palm = Part.makeBox(
            tongue_w, tongue_back, 3.5, App.Vector(x - tongue_w / 2.0, y, z)
        )
        start = App.Vector(x, y + tongue_back, z + barrel_r)
    barrel = Part.makeCylinder(barrel_r, barrel_l, start, App.Vector(0, dir_y, 0))
    return palm.fuse(barrel)


def ring_lug(x, y, z, dir_x, tongue_w, tongue_back, barrel_r, barrel_l, ox=0.0):
    """Keep-out: palm on the bar, barrel hanging off the end along X (dir_x +1 or -1)."""
    tip_x = ox if dir_x < 0 else ox + BAR_L
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


def copper_bar(sw1=False):
    bar = Part.makeBox(BAR_L, BAR_W, BAR_T)
    holes = [
        (STUD_X1, STUD_Y1, HOLE_M10 if sw1 else HOLE_516),
        (STUD_X1, STUD_Y2, HOLE_516),
        (STUD_X2, STUD_Y1, HOLE_14),
        (STUD_X2, STUD_Y2, HOLE_14),
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


def m10_bolt(z_head_bottom, head_up=True, shaft_extra=0.0):
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
        shaft_len = SM40_INSERT_DEPTH + 2.0 + shaft_extra
        shaft = Part.makeCylinder(M10_DIA / 2.0, shaft_len, App.Vector(0, 0, z_head_bottom - 0.2))
    return head.fuse(shaft)


def sm40_at(x, y, z=0.0):
    body = sm40_body()
    ins_bot, ins_top = sm40_inserts()
    for sh in (body, ins_bot, ins_top):
        sh.translate(App.Vector(x, y, z))
    return body, ins_bot, ins_top


def _hull_xy(pts):
    pts = sorted(set((round(p[0], 5), round(p[1], 5)) for p in pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _circle_pts(cx, cy, r, n):
    return [
        (cx + r * math.cos(2.0 * math.pi * i / n), cy + r * math.sin(2.0 * math.pi * i / n))
        for i in range(n)
    ]


def _fuse_many(shapes):
    shapes = [s for s in shapes if s is not None]
    if len(shapes) == 1:
        return shapes[0]
    try:
        out = shapes[0].multiFuse(shapes[1:])
    except Exception:
        out = shapes[0]
        for s in shapes[1:]:
            out = out.fuse(s)
    try:
        out = out.removeSplitter()
    except Exception:
        pass
    return out


def hvbd_flange():
    """Diamond flange: R38.74 sides, R8.64 ears on 100.1 mm mount C:C (gasket RP2127)."""
    m = HVBD_MOUNT_CC / 2.0
    pts = (
        _circle_pts(0.0, 0.0, HVBD_SIDE_R, 72)
        + _circle_pts(m, 0.0, HVBD_EAR_R, 28)
        + _circle_pts(-m, 0.0, HVBD_EAR_R, 28)
    )
    hull = _hull_xy(pts)
    vecs = [App.Vector(x, y, 0.0) for x, y in hull]
    vecs.append(vecs[0])
    face = Part.Face(Part.makePolygon(vecs))
    flange = face.extrude(App.Vector(0, 0, HVBD_FLANGE_T))
    for x in (m, -m):
        flange = flange.cut(
            Part.makeCylinder(
                HVBD_MOUNT_HOLE / 2.0,
                HVBD_FLANGE_T + 2.0,
                App.Vector(x, 0.0, -1.0),
            )
        )
        # triangular lightening pocket in each ear (datasheet rear view)
        x_in = 0.78 * x
        x_out = 0.92 * x
        y = 9.5
        poly = [
            App.Vector(x_in, 0.0, -0.1),
            App.Vector(x_out, y, -0.1),
            App.Vector(x_out, -y, -0.1),
            App.Vector(x_in, 0.0, -0.1),
        ]
        pocket = Part.Face(Part.makePolygon(poly)).extrude(App.Vector(0, 0, 2.0))
        flange = flange.cut(pocket)
    return flange


def hvbd_switch(x_out, y_out, z_bar_top):
    """HVBD6AXR from the datasheet. Studs along Y, mount holes along X, handle +Z."""
    z_rear = M10_NUT_H
    z_flange_back = HVBD_REAR
    z_flange_front = HVBD_REAR + HVBD_FLANGE_T
    z_knob = z_flange_front + HVBD_FRONT
    y_out_l = HVBD_STUD_CC / 2.0
    y_in_l = -HVBD_STUD_CC / 2.0
    r_body = HVBD_BODY_OD / 2.0

    flange = hvbd_flange()
    flange.translate(App.Vector(0, 0, z_flange_back))

    body = Part.makeCylinder(r_body, z_flange_back - z_rear, App.Vector(0, 0, z_rear))
    boss = Part.makeCylinder(HVBD_REAR_BOSS_OD / 2.0, z_rear + 6.0, App.Vector(0, 0, 0))
    collar = Part.makeCylinder(
        HVBD_COLLAR_OD / 2.0,
        12.0,
        App.Vector(0, 0, z_flange_front - 0.5),
    )

    rib_h = M10_NUT_H + 3.0
    rib = Part.makeBox(HVBD_BODY_OD - 10.0, 3.6, rib_h, App.Vector(-(HVBD_BODY_OD - 10.0) / 2.0, -1.8, 0))
    rib_cap = Part.makeCylinder(1.8, rib_h, App.Vector(-(HVBD_BODY_OD - 10.0) / 2.0, 0, 0))
    rib = rib.fuse(rib_cap).common(
        Part.makeCylinder(r_body - 0.8, rib_h + 1.0, App.Vector(0, 0, -0.5))
    )

    # LOTO hasp on the front collar (datasheet side view, shackle DIA 9/32 ~ 8.2)
    hasp = Part.makeBox(
        7.0,
        14.0,
        12.0,
        App.Vector(-HVBD_COLLAR_OD / 2.0 - 5.0, -7.0, z_flange_front),
    )
    hasp = hasp.cut(
        Part.makeCylinder(
            HVBD_LOTO / 2.0,
            16.0,
            App.Vector(-HVBD_COLLAR_OD / 2.0 - 1.5, -8.0, z_flange_front + 6.5),
            App.Vector(0, 1, 0),
        )
    )

    housing = _fuse_many([flange, body, boss, collar, rib, hasp])

    knob = Part.makeCylinder(
        HVBD_KNOB_OD / 2.0,
        HVBD_FRONT - 10.0,
        App.Vector(0, 0, z_flange_front + 10.0),
    )
    # Raised paddle on the knob face; LOTO end just past the knob OD (front view)
    paddle_z = z_knob - 5.0
    paddle_h = 5.5
    paddle_r = 6.5
    paddle_box = Part.makeBox(
        36.0,
        paddle_r * 2.0,
        paddle_h,
        App.Vector(-24.0, -paddle_r, paddle_z),
    )
    paddle_hi = Part.makeCylinder(paddle_r, paddle_h, App.Vector(12.0, 0, paddle_z))
    paddle_lo = Part.makeCylinder(paddle_r + 1.0, paddle_h, App.Vector(-24.0, 0, paddle_z))
    loto = Part.makeCylinder(3.2, paddle_h + 2.0, App.Vector(-24.0, 0, paddle_z - 1.0))
    screw = Part.makeCylinder(2.2, 2.5, App.Vector(0, 0, z_knob - 0.5))
    handle = _fuse_many([knob, paddle_box, paddle_hi, paddle_lo, screw]).cut(loto)

    terminals = []
    for y in (y_out_l, y_in_l):
        stud = Part.makeCylinder(
            M10_DIA / 2.0,
            HVBD_STUD_LEN + 3.0,
            App.Vector(0, y, 3.0),
            App.Vector(0, 0, -1),
        )
        nut = hex_prism(M10_HEAD_AF, M10_NUT_H)
        nut.translate(App.Vector(0, y, 0))
        terminals.append(stud.fuse(nut))
    terminals = _fuse_many(terminals)

    bushings = []
    m = HVBD_MOUNT_CC / 2.0
    for x in (m, -m):
        tube = Part.makeCylinder(4.75, HVBD_FLANGE_T, App.Vector(x, 0, z_flange_back))
        bushings.append(
            tube.cut(
                Part.makeCylinder(
                    HVBD_MOUNT_HOLE / 2.0,
                    HVBD_FLANGE_T + 0.4,
                    App.Vector(x, 0, z_flange_back - 0.2),
                )
            )
        )
    bushings = _fuse_many(bushings)

    dx, dy, dz = x_out, y_out - y_out_l, z_bar_top
    for sh in (housing, handle, terminals, bushings):
        sh.translate(App.Vector(dx, dy, dz))
    return housing, handle, terminals, bushings


def sweep_tube(points, radius):
    """2/0 jacket as a capsule chain (no spline overshoot)."""
    vecs = [p if isinstance(p, App.Vector) else App.Vector(*p) for p in points]
    chunks = [Part.makeSphere(radius, vecs[0])]
    for a, b in zip(vecs, vecs[1:]):
        d = b - a
        if d.Length < 1e-6:
            continue
        chunks.append(Part.makeCylinder(radius, d.Length, a, d))
        chunks.append(Part.makeSphere(radius, b))
    return _fuse_many(chunks)


def sb350_half(cable_x, cy, cable_dir):
    """One SB350 housing. cable_dir +1: cables enter from +X (pack half)."""
    if cable_dir > 0:
        x0 = cable_x - SB350_L
    else:
        x0 = cable_x
    body = Part.makeBox(SB350_L, SB350_W, SB350_H, App.Vector(x0, cy - SB350_W / 2.0, 0.0))
    try:
        body = body.makeChamfer(4.0, [e for e in body.Edges if e.Length > 50])
    except Exception:
        pass
    pole_ys = (cy - SB350_POLE_CC / 2.0, cy + SB350_POLE_CC / 2.0)
    z_c = SB350_H / 2.0
    r_entry = DLO_2_0_OD / 2.0 + 2.0
    for y in pole_ys:
        body = body.cut(
            Part.makeCylinder(
                r_entry,
                22.0,
                App.Vector(cable_x - cable_dir * 1.0, y, z_c),
                App.Vector(cable_dir, 0, 0),
            )
        )
    contacts = []
    for y in pole_ys:
        contacts.append(
            Part.makeCylinder(
                6.2,
                SB350_CONTACT_L,
                App.Vector(cable_x + cable_dir * 8.0, y, z_c),
                App.Vector(-cable_dir, 0, 0),
            )
        )
    return body, _fuse_many(contacts), pole_ys, z_c


def yaw_about_bar(shapes, origin, yaw_deg):
    if abs(float(yaw_deg)) < 1e-9:
        return
    ox, oy, oz = origin
    center = App.Vector(ox + BAR_L / 2.0, oy + BAR_W / 2.0, oz)
    axis = App.Vector(0, 0, 1)
    for sh in shapes:
        sh.rotate(center, axis, yaw_deg)


def sm40_xy(origin, yaw_deg=0.0):
    ox, oy, _oz = origin
    mx, my = ox + MOUNT_X, oy + MOUNT_Y
    if abs(float(yaw_deg)) < 1e-9:
        return mx, my
    cx, cy = ox + BAR_L / 2.0, oy + BAR_W / 2.0
    ang = math.radians(yaw_deg)
    dx, dy = mx - cx, my - cy
    return cx + dx * math.cos(ang) - dy * math.sin(ang), cy + dx * math.sin(ang) + dy * math.cos(ang)


def f4_layout(tb1_origin):
    ox, oy, _oz = tb1_origin
    y_fuse = oy - 130.0
    x_pack = ox + 2.0
    x_sw1 = x_pack + A25X_HOLE_CC
    return x_pack, x_sw1, y_fuse


def sw1_pose(tb1_origin):
    """HVBD6AXR on the pack plate, south of TB1. Output jumper to TB1 Y1."""
    ox, oy, oz = tb1_origin
    x_out = ox + STUD_X1
    cy = oy - SW1_CY_OFF
    y_out = cy + HVBD_STUD_CC / 2.0
    z_term = oz + SM40_H + BAR_T
    return {
        "x_out": x_out,
        "y_out": y_out,
        "y_in": cy - HVBD_STUD_CC / 2.0,
        "cy": cy,
        "z_term": z_term,
        "z_flange": z_term + HVBD_REAR,
        "z_handle": z_term + HVBD_REAR + HVBD_FLANGE_T + HVBD_FRONT,
    }


def sw1_mount_layout(tb1_origin):
    """M8 posts under the HVBD flange ears, straight down to the pack plate."""
    sw = sw1_pose(tb1_origin)
    m = HVBD_MOUNT_CC / 2.0
    ears = ((sw["x_out"] - m, sw["cy"]), (sw["x_out"] + m, sw["cy"]))
    return {
        "posts": ears,
        "ears": ears,
        "z_pad": sw["z_flange"] - SW1_PAD_T,
        "z_flange": sw["z_flange"],
    }


def cb_layout(tb1_origin, tb2_origin):
    """CHTAIXI 2P pair on the 1/4-20 end. + pole toward TB1, LINE toward pack."""
    ox1, oy1, oz1 = tb1_origin
    _ox2, oy2, _oz2 = tb2_origin
    x_front = ox1 + BAR_L + LUG_14_BARREL_L + 18.0
    y_mid = (oy1 + MOUNT_Y + oy2 + MOUNT_Y) / 2.0
    cy3 = y_mid - (MCB_W + MCB_GAP) / 2.0
    cy4 = y_mid + (MCB_W + MCB_GAP) / 2.0
    z_base = PLATE_T
    return {
        "x_front": x_front,
        "x_back": x_front + MCB_D,
        "cy3": cy3,
        "cy4": cy4,
        "z_base": z_base,
        "z_line": z_base + MCB_H - 12.0,
        "z_load": z_base + 16.0,
        "y_plus": MCB_MOD / 2.0,
        "y_minus": MCB_MOD / 2.0,
        "lug_z": oz1 + SM40_H + BAR_T + LUG_14_BARREL_R,
        "barrel_x": ox1 + BAR_L + LUG_14_BARREL_L,
        "tb1_y1": oy1 + STUD_Y1,
        "tb1_y2": oy1 + STUD_Y2,
        "tb2_y1": oy2 + STUD_Y1,
        "tb2_y2": oy2 + STUD_Y2,
    }


def plate_box(x0, y0, x1, y1, holes, z=0.0):
    plate = Part.makeBox(x1 - x0, y1 - y0, PLATE_T, App.Vector(x0, y0, z))
    for hx, hy, r in holes:
        plate = plate.cut(Part.makeCylinder(r, PLATE_T + 2.0, App.Vector(hx, hy, z - 1.0)))
    return plate


def _corner_holes(x0, y0, x1, y1, inset=8.0, r=PLATE_HOLE_R):
    return (
        (x0 + inset, y0 + inset, r),
        (x1 - inset, y0 + inset, r),
        (x0 + inset, y1 - inset, r),
        (x1 - inset, y1 - inset, r),
    )


def pack_plate_layout(tb1_origin, tb2_origin):
    """Outer plate / cover envelope, mounting holes, and SW1 plate location."""
    ox, oy, _oz = tb1_origin
    x_pack, x_fuse_sw, y_fuse = f4_layout(tb1_origin)
    cb = cb_layout(tb1_origin, tb2_origin)
    sw = sw1_pose(tb1_origin)
    mt = sw1_mount_layout(tb1_origin)
    sm1 = sm40_xy(tb1_origin)
    sm2 = sm40_xy(tb2_origin)
    south = cb["cy3"] - MCB_W / 2.0 - 26.0
    north = cb["cy4"] + MCB_W / 2.0 + 26.0
    x_dev = cb["x_front"] + MCB_D + 35.0
    f4_x0 = x_pack - SCM10_BASE_L / 2.0
    f4_x1 = x_fuse_sw + SCM10_BASE_L / 2.0
    f4_y0 = y_fuse - SCM10_BASE_W / 2.0
    sw_x = sw["x_out"]
    sw_y_out = sw["y_out"]
    sw_cy = sw["cy"]
    parts_x0 = min(f4_x0, 0.0, cb["x_front"], sw_x - HVBD_MOUNT_CC / 2.0 - 12.0)
    parts_x1 = max(f4_x1, BAR_L, x_dev, sw_x + HVBD_MOUNT_CC / 2.0 + 12.0)
    parts_y0 = min(f4_y0, 0.0, south, sw_cy - HVBD_BODY_OD / 2.0 - 8.0, mt["posts"][0][1] - 16.0)
    parts_y1 = max(y_fuse + SCM10_BASE_W / 2.0, PITCH_TB12 + BAR_W, north)
    inner_x0 = parts_x0 - COVER_CLEAR
    inner_x1 = parts_x1 + COVER_CLEAR
    inner_y0 = parts_y0 - COVER_CLEAR
    inner_y1 = parts_y1 + COVER_CLEAR
    px0 = inner_x0 - COVER_WALL
    px1 = inner_x1 + COVER_WALL
    py0 = inner_y0 - COVER_WALL
    py1 = inner_y1 + COVER_WALL
    z_lid = PLATE_T + COVER_INNER_H
    holes = [
        (sm1[0], sm1[1], HOLE_M10 / 2.0),
        (sm2[0], sm2[1], HOLE_M10 / 2.0),
    ]
    for x in (x_pack, x_fuse_sw):
        for dx in (-18.0, 18.0):
            holes.append((x + dx, y_fuse, HOLE_M6 / 2.0))
    din_x = cb["x_front"] + MCB_D - 18.0
    din_y0 = cb["cy3"] - MCB_W / 2.0 - 8.0
    din_y1 = cb["cy4"] + MCB_W / 2.0 + 8.0
    holes.append((din_x, din_y0 + 12.0, HOLE_M6 / 2.0))
    holes.append((din_x, din_y1 - 12.0, HOLE_M6 / 2.0))
    for px, py in mt["posts"]:
        holes.append((px, py, HOLE_M8 / 2.0))
    xs = (px0 + COVER_SCREW_INSET, (px0 + px1) / 2.0, px1 - COVER_SCREW_INSET)
    ys = (py0 + COVER_SCREW_INSET, (py0 + py1) / 2.0, py1 - COVER_SCREW_INSET)
    for hx in xs:
        for hy in ys:
            if hx in (xs[0], xs[2]) or hy in (ys[0], ys[2]):
                holes.append((hx, hy, HOLE_M6 / 2.0))
    return {
        "px0": px0,
        "px1": px1,
        "py0": py0,
        "py1": py1,
        "inner_x0": inner_x0,
        "inner_x1": inner_x1,
        "inner_y0": inner_y0,
        "inner_y1": inner_y1,
        "holes": holes,
        "z_lid": z_lid,
        "sw_x": sw_x,
        "sw_y_out": sw_y_out,
        "sw_cy": sw_cy,
        "z_sw1_term": sw["z_term"],
        "cb": cb,
        "x_pack": x_pack,
        "x_fuse_sw": x_fuse_sw,
        "y_fuse": y_fuse,
    }


def add_mount_plates(doc, tb1_origin, tb2_origin, tb3_origin):
    """1/4 in plates with holes for SM40, 1SCM10, DIN rail, SW1 posts, and cover screws."""
    lay = pack_plate_layout(tb1_origin, tb2_origin)
    pack = plate_box(lay["px0"], lay["py0"], lay["px1"], lay["py1"], lay["holes"])
    sm3 = sm40_xy(tb3_origin, 180.0)
    pad = SM40_OD / 2.0 + PLATE_MARGIN
    t3x0, t3y0 = sm3[0] - pad, sm3[1] - pad
    t3x1, t3y1 = sm3[0] + pad, sm3[1] + pad
    tb3_holes = list(_corner_holes(t3x0, t3y0, t3x1, t3y1))
    tb3_holes.append((sm3[0], sm3[1], HOLE_M10 / 2.0))
    tb3_plate = plate_box(t3x0, t3y0, t3x1, t3y1, tb3_holes)

    grp = doc.addObject("App::DocumentObjectGroup", "MountPlates")
    grp.Label = "MountPlates"
    objs = [
        add_shape(doc, "Plate_Pack", pack, COLOR_PLATE),
        add_shape(doc, "Plate_TB3", tb3_plate, COLOR_PLATE),
    ]
    for o in objs:
        grp.addObject(o)
    return grp, lay


def add_sw1(doc, tb1_origin):
    """HVBD6AXR on the pack plate. Flange M8s on posts; 2/0 jumper to TB1 Y1."""
    ox, oy, oz = tb1_origin
    sw = sw1_pose(tb1_origin)
    mt = sw1_mount_layout(tb1_origin)
    housing, handle, terminals, bushings = hvbd_switch(sw["x_out"], sw["y_out"], sw["z_term"])
    z_lug = sw["z_term"]
    lug_in = offbar_lug_y(sw["x_out"], sw["y_in"], z_lug, -1, 22.0, 10.0, 8.0, 32.0)
    lug_out = offbar_lug_y(sw["x_out"], sw["y_out"], z_lug, 1, 22.0, 10.0, 8.0, 32.0)
    z_j = z_lug + LUG_516_BARREL_R
    jumper = sweep_tube(
        (
            App.Vector(sw["x_out"], sw["y_out"], z_j),
            App.Vector(ox + STUD_X1, oy + STUD_Y1, z_j),
        ),
        DLO_2_0_OD / 2.0,
    )

    z0 = PLATE_T
    z_pad = mt["z_pad"]
    z_fl = mt["z_flange"]
    mounts = []
    hw = []
    for fx, fy in mt["ears"]:
        foot = Part.makeBox(28.0, 28.0, 6.35, App.Vector(fx - 14.0, fy - 14.0, z0))
        foot = foot.cut(Part.makeCylinder(HOLE_M8 / 2.0, 8.0, App.Vector(fx, fy, z0 - 1.0)))
        post = hex_prism(SW1_POST_AF, z_pad - z0 - 6.35)
        post.translate(App.Vector(fx, fy, z0 + 6.35))
        pad = Part.makeBox(22.0, 22.0, SW1_PAD_T, App.Vector(fx - 11.0, fy - 11.0, z_pad))
        pad = pad.cut(Part.makeCylinder(HOLE_M8 / 2.0, SW1_PAD_T + 2.0, App.Vector(fx, fy, z_pad - 1.0)))
        mounts.append(_fuse_many([foot, post, pad]))
        z_fl_top = z_fl + HVBD_FLANGE_T
        shaft = Part.makeCylinder(
            M8_DIA / 2.0,
            HVBD_FLANGE_T + SW1_PAD_T + 14.0,
            App.Vector(fx, fy, z_pad - 14.0),
        )
        wash = place_xy(washer(16.0, HOLE_M8, 1.6), fx, fy, z_fl_top)
        head = hex_prism(M8_HEAD_AF, M8_HEAD_H)
        head.translate(App.Vector(fx, fy, z_fl_top + 1.6))
        hw.extend((shaft, head, wash))
        bot_head = hex_prism(M8_HEAD_AF, M8_HEAD_H)
        bot_head.translate(App.Vector(fx, fy, z0 - PLATE_T - M8_HEAD_H))
        bot_shaft = Part.makeCylinder(
            M8_DIA / 2.0,
            PLATE_T + 6.35 + M8_NUT_H,
            App.Vector(fx, fy, z0 - PLATE_T),
        )
        bot_nut = hex_prism(M8_HEAD_AF, M8_NUT_H)
        bot_nut.translate(App.Vector(fx, fy, z0 + 6.35))
        hw.extend((bot_head, bot_shaft, bot_nut))

    grp = doc.addObject("App::DocumentObjectGroup", "SW1")
    grp.Label = "SW1"
    objs = [
        add_shape(doc, "SW1_Body", housing, COLOR_HVBD),
        add_shape(doc, "SW1_Handle", handle, COLOR_HVBD_HANDLE),
        add_shape(doc, "SW1_Studs", terminals, COLOR_SS),
        add_shape(doc, "SW1_Bushings", bushings, COLOR_HEAD_BOT),
        add_shape(doc, "SW1_Mounts", _fuse_many(mounts), COLOR_ZINC),
        add_shape(doc, "SW1_MountHW", _fuse_many(hw), COLOR_SS),
        add_shape(doc, "SW1_Jumper", jumper, COLOR_DLO),
        add_shape(doc, "SW1_InputLug", lug_in.fuse(lug_out), COLOR_LUG, transparency=50),
    ]
    for o in objs:
        grp.addObject(o)
    add_label(doc, "Label_SW1", ["SW1  HVBD6AXR"], (sw["x_out"], sw["cy"] - 45.0, sw["z_handle"] + 8.0))
    return grp


def add_cover(doc, tb1_origin, tb2_origin):
    """Cover slips over plate-mounted SW1. Lid windows over CB3 / CB4."""
    lay = pack_plate_layout(tb1_origin, tb2_origin)
    x0, x1 = lay["inner_x0"], lay["inner_x1"]
    y0, y1 = lay["inner_y0"], lay["inner_y1"]
    z0 = PLATE_T
    zh = COVER_INNER_H
    w = COVER_WALL
    walls = [
        Part.makeBox(x1 - x0 + 2.0 * w, w, zh, App.Vector(x0 - w, y0 - w, z0)),
        Part.makeBox(x1 - x0 + 2.0 * w, w, zh, App.Vector(x0 - w, y1, z0)),
        Part.makeBox(w, y1 - y0, zh, App.Vector(x0 - w, y0, z0)),
        Part.makeBox(w, y1 - y0, zh, App.Vector(x1, y0, z0)),
    ]
    wall = _fuse_many(walls)
    lid = Part.makeBox(x1 - x0 + 2.0 * w, y1 - y0 + 2.0 * w, COVER_LID_T, App.Vector(x0 - w, y0 - w, lay["z_lid"]))
    lid = lid.cut(
        Part.makeCylinder(
            COVER_SW1_HOLE_R,
            COVER_LID_T + 2.0,
            App.Vector(lay["sw_x"], lay["sw_cy"], lay["z_lid"] - 1.0),
        )
    )
    cb = lay["cb"]
    mgn = COVER_CB_MARGIN
    for cy in (cb["cy3"], cb["cy4"]):
        lid = lid.cut(
            Part.makeBox(
                MCB_D + 2.0 * mgn,
                MCB_W + 2.0 * mgn,
                COVER_LID_T + 2.0,
                App.Vector(cb["x_front"] - mgn, cy - MCB_W / 2.0 - mgn, lay["z_lid"] - 1.0),
            )
        )
    grp = doc.addObject("App::DocumentObjectGroup", "PackCover")
    grp.Label = "PackCover"
    objs = [
        add_shape(doc, "Cover_Walls", wall, COLOR_COVER, transparency=50),
        add_shape(doc, "Cover_Lid", lid, COLOR_COVER, transparency=30),
    ]
    for o in objs:
        grp.addObject(o)
    return grp


def sb350_layout(tb1_origin, tb2_origin):
    ox1, oy1, oz1 = tb1_origin
    _ox2, oy2, _oz2 = tb2_origin
    y_plus = oy1 + STUD_Y2
    y_minus = oy2 + STUD_Y1
    cy = (y_plus + y_minus) / 2.0
    barrel_x = ox1 - LUG_516_BARREL_L
    cable_x = barrel_x - 90.0
    inv_x = cable_x - SB350_MATED
    return barrel_x, cable_x, inv_x, cy, y_plus, y_minus, oz1


def tb3_at_inverter(tb1_origin, tb2_origin):
    """TB3 origin (pre-180 yaw) so the 5/16 end faces the SB350 inverter half."""
    _bx, _cx, inv_x, cy, _yp, _ym, oz = sb350_layout(tb1_origin, tb2_origin)
    tx = inv_x - 122.0 - BAR_L
    ty = cy - BAR_W / 2.0
    return (tx, ty, oz)


def add_sb350(doc, tb1_origin, tb2_origin, tb3_origin=None):
    """Mated SB350 off the 5/16 end; HV-09 / HV-10 2/0 from the inner studs."""
    ox1, oy1, oz1 = tb1_origin
    barrel_x, cable_x, inv_x, cy, y_plus, y_minus, oz1 = sb350_layout(tb1_origin, tb2_origin)
    lug_z = oz1 + SM40_H + BAR_T
    z_lug = lug_z + LUG_516_BARREL_R
    pack, pack_ct, pack_ys, z_c = sb350_half(cable_x, cy, 1)
    inv, inv_ct, _, _ = sb350_half(inv_x, cy, -1)
    housing = pack.fuse(inv)

    hx = cable_x - SB350_L * 0.35
    grip = Part.makeBox(
        22.0,
        SB350_W - 16.0,
        10.0,
        App.Vector(hx - 11.0, cy - (SB350_W - 16.0) / 2.0, SB350_H + 32.0),
    )
    leg1 = Part.makeBox(10.0, 8.0, 38.0, App.Vector(hx - 5.0, cy - SB350_W / 2.0 + 4.0, SB350_H - 4.0))
    leg2 = Part.makeBox(10.0, 8.0, 38.0, App.Vector(hx - 5.0, cy + SB350_W / 2.0 - 12.0, SB350_H - 4.0))
    handle = _fuse_many([grip, leg1, leg2])

    cables = []
    for y_lug, y_ent in ((y_plus, pack_ys[0]), (y_minus, pack_ys[1])):
        p0 = App.Vector(barrel_x, y_lug, z_lug)
        p3 = App.Vector(cable_x + 6.0, y_ent, z_c)
        pts = []
        for t in (0.0, 0.22, 0.5, 0.78, 1.0):
            s = t * t * (3.0 - 2.0 * t)
            pts.append(
                App.Vector(
                    p0.x + (p3.x - p0.x) * t,
                    p0.y + (p3.y - p0.y) * s,
                    p0.z + (p3.z - p0.z) * s,
                )
            )
        cables.append(sweep_tube(pts, DLO_2_0_OD / 2.0))
    if tb3_origin is not None:
        tx, ty, _ = tb3_origin
        y_tb3_plus = ty + BAR_W - STUD_Y2
        barrel_tb3 = tx + BAR_L + LUG_516_BARREL_L
        p0 = App.Vector(inv_x - 2.0, pack_ys[0], z_c)
        p3 = App.Vector(barrel_tb3, y_tb3_plus, z_lug)
        pts = []
        for t in (0.0, 0.22, 0.5, 0.78, 1.0):
            s = t * t * (3.0 - 2.0 * t)
            pts.append(
                App.Vector(
                    p0.x + (p3.x - p0.x) * t,
                    p0.y + (p3.y - p0.y) * s,
                    p0.z + (p3.z - p0.z) * s,
                )
            )
        cables.append(sweep_tube(pts, DLO_2_0_OD / 2.0))
        cables.append(
            sweep_tube(
                (
                    App.Vector(inv_x - 2.0, pack_ys[1], z_c),
                    App.Vector(inv_x - 80.0, pack_ys[1] + 50.0, z_c),
                ),
                DLO_2_0_OD / 2.0,
            )
        )
    else:
        for y_ent in pack_ys:
            p0 = App.Vector(inv_x - 2.0, y_ent, z_c)
            p1 = App.Vector(inv_x - 70.0, y_ent, z_c)
            cables.append(sweep_tube((p0, p1), DLO_2_0_OD / 2.0))

    grp = doc.addObject("App::DocumentObjectGroup", "SB350_PackDisconnect")
    grp.Label = "SB350_PackDisconnect"
    objs = [
        add_shape(doc, "SB350_Housing", housing, COLOR_SB350),
        add_shape(doc, "SB350_Handle", handle, COLOR_SB350_HANDLE),
        add_shape(doc, "SB350_Contacts", pack_ct.fuse(inv_ct), COLOR_SS),
        add_shape(doc, "SB350_DLO", Part.makeCompound(cables), COLOR_DLO),
    ]
    for o in objs:
        grp.addObject(o)
    add_label(doc, "Label_SB350", ["SB350  pack / inverter"], (cable_x, cy - SB350_W / 2.0 - 18.0, SB350_H + 40.0))
    return grp


def scm10_mount():
    """One 1SCM10 pedestal, stud on +Z at origin in XY, base on z=0."""
    pts = [
        App.Vector(-SCM10_BASE_L / 2.0, 0, 0),
        App.Vector(SCM10_BASE_L / 2.0, 0, 0),
        App.Vector(SCM10_BASE_L / 2.0, 0, SCM10_FOOT_H),
        App.Vector(12.0, 0, 50.0),
        App.Vector(12.0, 0, SCM10_BOSS_H - SCM10_PAD_T),
        App.Vector(-12.0, 0, SCM10_BOSS_H - SCM10_PAD_T),
        App.Vector(-12.0, 0, 50.0),
        App.Vector(-SCM10_BASE_L / 2.0, 0, SCM10_FOOT_H),
        App.Vector(-SCM10_BASE_L / 2.0, 0, 0),
    ]
    ins = Part.Face(Part.makePolygon(pts)).extrude(App.Vector(0, SCM10_BASE_W, 0))
    ins.translate(App.Vector(0, -SCM10_BASE_W / 2.0, 0))
    pad = Part.makeBox(
        SCM10_PAD_L,
        SCM10_BASE_W,
        SCM10_PAD_T,
        App.Vector(-SCM10_PAD_L / 2.0, -SCM10_BASE_W / 2.0, SCM10_BOSS_H - SCM10_PAD_T),
    )
    stud = Part.makeCylinder(M10_DIA / 2.0, SCM10_STUD_STACK + 4.0, App.Vector(0, 0, SCM10_BOSS_H - 4.0))
    wash = place_xy(washer(M10_WASH_OD, HOLE_M10, M10_WASH_T), 0, 0, SCM10_BOSS_H + A25X_BLADE_T + 3.5)
    nut = hex_prism(M10_HEAD_AF, M10_NUT_H)
    nut.translate(App.Vector(0, 0, SCM10_BOSS_H + A25X_BLADE_T + 3.5 + M10_WASH_T))
    metal = _fuse_many([pad, stud, wash, nut])
    return ins, metal


def a25x_fuse():
    """A25X500-4: 1.5 in body, 0.406 in holes at 2.91 in C:C, blades 1 x 0.25 in."""
    overhang = (A25X_L - A25X_HOLE_CC) / 2.0
    blade = Part.makeBox(
        A25X_L,
        A25X_BLADE_W,
        A25X_BLADE_T,
        App.Vector(-overhang, -A25X_BLADE_W / 2.0, 0),
    )
    for x in (0.0, A25X_HOLE_CC):
        blade = blade.cut(
            Part.makeCylinder(A25X_HOLE / 2.0, A25X_BLADE_T + 2.0, App.Vector(x, 0, -1.0))
        )
    x_body = (A25X_HOLE_CC - A25X_BODY_L) / 2.0
    body = Part.makeCylinder(
        A25X_OD / 2.0,
        A25X_BODY_L,
        App.Vector(x_body, 0, A25X_BLADE_T + A25X_OD / 2.0),
        App.Vector(1, 0, 0),
    )
    return body, blade


def add_f4(doc, tb1_origin):
    """F4 A25X500-4 on a 1SCM10 pair. Mounts sit on the 1/4 in pack plate."""
    ox, oy, oz = tb1_origin
    x_pack, x_sw1, y_fuse = f4_layout(tb1_origin)
    z0 = PLATE_T
    z_blade = z0 + SCM10_BOSS_H

    insulators = []
    metals = []
    for x in (x_pack, x_sw1):
        ins, metal = scm10_mount()
        for sh in (ins, metal):
            sh.translate(App.Vector(x, y_fuse, z0))
        insulators.append(ins)
        metals.append(metal)

    body, blade = a25x_fuse()
    for sh in (body, blade):
        sh.translate(App.Vector(x_pack, y_fuse, z_blade))

    sw = sw1_pose(tb1_origin)
    z_f = z_blade + A25X_BLADE_T + LUG_516_BARREL_R
    z_sw1 = sw["z_term"] + LUG_516_BARREL_R
    p0 = App.Vector(x_sw1, y_fuse, z_f)
    p1 = App.Vector(sw["x_out"], sw["y_in"], z_f)
    p2 = App.Vector(sw["x_out"], sw["y_in"], z_sw1)
    hv07 = sweep_tube((p0, p1, p2), DLO_2_0_OD / 2.0)
    hv06 = sweep_tube(
        (
            App.Vector(x_pack, y_fuse, z_f),
            App.Vector(x_pack - 80.0, y_fuse, z_f),
        ),
        DLO_2_0_OD / 2.0,
    )

    grp = doc.addObject("App::DocumentObjectGroup", "F4_PackFuse")
    grp.Label = "F4_PackFuse"
    objs = [
        add_shape(doc, "F4_Mounts", _fuse_many(insulators), COLOR_SCM10),
        add_shape(doc, "F4_Hardware", _fuse_many(metals), COLOR_ZINC),
        add_shape(doc, "F4_Body", body, COLOR_FUSE),
        add_shape(doc, "F4_Blades", blade, COLOR_CU),
        add_shape(doc, "F4_DLO", Part.makeCompound((hv07, hv06)), COLOR_DLO),
    ]
    for o in objs:
        grp.addObject(o)
    add_label(doc, "Label_F4", ["F4  A25X500-4  1SCM10"], (x_sw1, y_fuse - 28.0, z0 + SCM10_H + 10.0))
    return grp


def mcb_2p(cy, x_front, z_base):
    """CHTAIXI DZ47Z-63 2P. Front/LINE face at x_front toward the bars. + pole at -Y."""
    body = Part.makeBox(MCB_D, MCB_W, MCB_H, App.Vector(x_front, cy - MCB_W / 2.0, z_base))
    try:
        body = body.makeChamfer(1.2, [e for e in body.Edges if e.Length > 70])
    except Exception:
        pass
    toggle = Part.makeBox(
        12.0,
        22.0,
        18.0,
        App.Vector(x_front + 8.0, cy - 11.0, z_base + MCB_H - 28.0),
    )
    yp = cy - MCB_MOD / 2.0
    ym = cy + MCB_MOD / 2.0
    plus = Part.makeCylinder(3.2, 2.0, App.Vector(x_front - 0.5, yp, z_base + MCB_H / 2.0), App.Vector(-1, 0, 0))
    minus = Part.makeCylinder(3.2, 2.0, App.Vector(x_front - 0.5, ym, z_base + MCB_H / 2.0), App.Vector(-1, 0, 0))
    return body, toggle, plus, minus, yp, ym


def add_breakers(doc, tb1_origin, tb2_origin):
    """CB3 32 A charger and CB4 10 A DCIS. Pack on LINE, device on LOAD, + to TB1."""
    cb = cb_layout(tb1_origin, tb2_origin)
    xf = cb["x_front"]
    z0 = cb["z_base"]
    z_line = cb["z_line"]
    z_load = cb["z_load"]
    r = AWG10_OD / 2.0

    bodies = []
    toggles = []
    pluses = []
    minuses = []
    terms = {}
    for key, cy in (("cb3", cb["cy3"]), ("cb4", cb["cy4"])):
        body, toggle, plus, minus, yp, ym = mcb_2p(cy, xf, z0)
        bodies.append(body)
        toggles.append(toggle)
        pluses.append(plus)
        minuses.append(minus)
        terms[key] = {"plus": yp, "minus": ym}

    din_y0 = cb["cy3"] - MCB_W / 2.0 - 8.0
    din_y1 = cb["cy4"] + MCB_W / 2.0 + 8.0
    din_x = xf + MCB_D - 18.0 - DIN_W / 2.0
    din = Part.makeBox(DIN_W, din_y1 - din_y0, DIN_H, App.Vector(din_x - DIN_W / 2.0, din_y0, z0))
    lip = Part.makeBox(DIN_W + 6.0, din_y1 - din_y0, 1.2, App.Vector(din_x - DIN_W / 2.0 - 3.0, din_y0, z0 + DIN_H))
    din = din.fuse(lip)

    bx = cb["barrel_x"]
    lz = cb["lug_z"]
    x_dev = xf + MCB_D + 35.0
    x_face = xf - 8.0
    south = cb["cy3"] - MCB_W / 2.0 - 14.0
    north = cb["cy4"] + MCB_W / 2.0 + 14.0

    def fan(y_lug, y_term, z_term):
        return sweep_tube(
            (
                App.Vector(bx, y_lug, lz),
                App.Vector(bx + (xf - bx) * 0.4, y_lug + (y_term - y_lug) * 0.2, lz + (z_term - lz) * 0.5),
                App.Vector(xf, y_term, z_term),
            ),
            r,
        )

    def load_around(y_term, outer_y):
        return sweep_tube(
            (
                App.Vector(xf, y_term, z_load),
                App.Vector(x_face, y_term, z_load),
                App.Vector(x_face, outer_y, z_load),
                App.Vector(x_dev, outer_y, z_load),
            ),
            r,
        )

    reds = []
    blks = []
    t3 = terms["cb3"]
    t4 = terms["cb4"]
    reds.append(fan(cb["tb1_y1"], t3["plus"], z_line))
    blks.append(fan(cb["tb2_y1"], t3["minus"], z_line))
    reds.append(load_around(t3["plus"], south))
    blks.append(load_around(t3["minus"], south - 12.0))
    reds.append(fan(cb["tb1_y2"], t4["plus"], z_line))
    blks.append(fan(cb["tb2_y2"], t4["minus"], z_line))
    reds.append(load_around(t4["plus"], north + 12.0))
    blks.append(load_around(t4["minus"], north))

    grp = doc.addObject("App::DocumentObjectGroup", "CB3_CB4")
    grp.Label = "CB3_CB4"
    objs = [
        add_shape(doc, "CB_Bodies", _fuse_many(bodies), COLOR_MCB),
        add_shape(doc, "CB_Toggles", _fuse_many(toggles), COLOR_MCB_TOGGLE),
        add_shape(doc, "CB_PlusMark", _fuse_many(pluses), COLOR_HV_RED),
        add_shape(doc, "CB_MinusMark", _fuse_many(minuses), COLOR_HV_BLK),
        add_shape(doc, "CB_DIN", din, COLOR_DIN),
        add_shape(doc, "CB_DLO_Pos", _fuse_many(reds), COLOR_HV_RED),
        add_shape(doc, "CB_DLO_Neg", _fuse_many(blks), COLOR_HV_BLK),
    ]
    for o in objs:
        grp.addObject(o)
    add_label(doc, "Label_CB3", ["CB3  32 A  charger"], (xf, cb["cy3"] - 28.0, z0 + MCB_H + 8.0))
    add_label(doc, "Label_CB4", ["CB4  10 A  DCIS"], (xf, cb["cy4"] + 18.0, z0 + MCB_H + 8.0))
    return grp


def build_one(doc, prefix, origin, sw1=False, yaw=0.0, y1_south=False):
    ox, oy, oz = origin
    bar_z = SM40_H
    mx, my = ox + MOUNT_X, oy + MOUNT_Y

    bar = copper_bar(sw1=sw1)
    bar.translate(App.Vector(ox, oy, oz + bar_z))

    hardware = []
    underside = []
    stacks = []
    if not sw1:
        stacks.append(
            (STUD_X1, STUD_Y1, DIA_516, STUD_H_516, WASH_OD_516, WASH_ID_516, WASH_T_516, NUT_AF_516, NUT_H_516, HEAD_H_516)
        )
    stacks.extend(
        (
            (STUD_X1, STUD_Y2, DIA_516, STUD_H_516, WASH_OD_516, WASH_ID_516, WASH_T_516, NUT_AF_516, NUT_H_516, HEAD_H_516),
            (STUD_X2, STUD_Y1, DIA_14, STUD_H_14, WASH_OD_14, WASH_ID_14, WASH_T_14, NUT_AF_14, NUT_H_14, HEAD_H_14),
            (STUD_X2, STUD_Y2, DIA_14, STUD_H_14, WASH_OD_14, WASH_ID_14, WASH_T_14, NUT_AF_14, NUT_H_14, HEAD_H_14),
        )
    )
    for x, y, dia, h, wod, wid, wt, af, nh, hh in stacks:
        st, w, n, w_bot, head = stud_stack(x, y, dia, h, wod, wid, wt, af, nh, hh, bar_z)
        for sh in (st, w, n, w_bot, head):
            sh.translate(App.Vector(ox, oy, oz))
        hardware.extend((st, w, n))
        underside.extend((w_bot, head))

    body, ins_bot, ins_top = sm40_at(mx, my, oz)

    wash = place_xy(washer(M10_WASH_OD, HOLE_M10, M10_WASH_T), mx, my, oz + bar_z + BAR_T)
    top_bolt = m10_bolt(oz + bar_z + BAR_T + M10_WASH_T, head_up=True)
    top_bolt.translate(App.Vector(mx, my, 0))
    bot_bolt = m10_bolt(oz - PLATE_T, head_up=False, shaft_extra=PLATE_T)
    bot_bolt.translate(App.Vector(mx, my, 0))
    hardware.extend((wash, top_bolt, bot_bolt))

    lug_z = oz + bar_z + BAR_T
    lugs = [
        ring_lug(ox + STUD_X1, oy + STUD_Y2, lug_z, -1, 22.0, 10.0, 8.0, 32.0, ox),
        ring_lug(ox + STUD_X2, oy + STUD_Y1, lug_z, 1, 12.0, 8.0, 4.5, 20.0, ox),
        ring_lug(ox + STUD_X2, oy + STUD_Y2, lug_z, 1, 12.0, 8.0, 4.5, 20.0, ox),
    ]
    if not sw1:
        if y1_south:
            lugs.insert(0, offbar_lug_y(ox + STUD_X1, oy + STUD_Y1, lug_z, -1, 22.0, 10.0, 8.0, 32.0))
        else:
            lugs.insert(0, ring_lug(ox + STUD_X1, oy + STUD_Y1, lug_z, -1, 22.0, 10.0, 8.0, 32.0, ox))

    yaw_about_bar(
        [bar, body, ins_bot, ins_top] + hardware + underside + lugs,
        origin,
        yaw,
    )

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
        ("bar_L", BAR_L, "3.54 in, SM40 offset to 1/4-20 end"),
        ("bar_W", BAR_W, "2.5 in for angled 2/0"),
        ("bar_T", BAR_T, "1/4 in plate"),
        ("stud_x1", STUD_X1, "2/0 column"),
        ("stud_x2", STUD_X2, "1/4-20, 12 mm from end"),
        ("stud_y1", STUD_Y1, "row A, 16 mm from edge"),
        ("stud_y2", STUD_Y2, "row B, 16 mm from edge"),
        ("mount_x", MOUNT_X, "SM40 / M10, toward 1/4-20"),
        ("mount_y", MOUNT_Y, "SM40 / M10 hole center"),
        ("hole_M10", HOLE_M10, "SM40 clamp"),
        ("HVBD_stud_cc", HVBD_STUD_CC, "SW1 M10 studs"),
        ("HVBD_body_OD", HVBD_BODY_OD, "SW1 rear housing"),
        ("HVBD_stud_len", HVBD_STUD_LEN, "thread outboard of terminal nut"),
        ("HVBD_mount_cc", HVBD_MOUNT_CC, "M8 flange holes"),
        ("HVBD_flange_t", HVBD_FLANGE_T, "diamond flange"),
        ("HVBD_front", HVBD_FRONT, "handle/collar in front of flange"),
        ("HVBD_rear", HVBD_REAR, "flange to terminal nut"),
        ("SM40_H", SM40_H, "catalog height"),
        ("SM40_OD", SM40_OD, "face diameter"),
        ("SM40_waist", SM40_WAIST, "socket / waist"),
        ("SM40_insert", "M10 x 11", "both ends"),
        ("creepage_air_gap_tb23", PITCH_TB23 - BAR_W, "TB2-TB3 aligned copper"),
        ("pitch_tb12", PITCH_TB12, "TB1-TB2 SM40 centers, spin-safe"),
        ("pitch_tb23", PITCH_TB23, "TB2-TB3 SM40 centers"),
        ("air_tb12_aligned", PITCH_TB12 - BAR_W, "TB1-TB2 air when aligned"),
        ("SB350_L", SB350_L, "single housing length"),
        ("SB350_W", SB350_W, "housing width"),
        ("SB350_mated", SB350_MATED, "mated pair length"),
        ("DLO_2_0_OD", DLO_2_0_OD, "2/0 jacket keep-out"),
        ("A25X_L", A25X_L, "F4 overall length"),
        ("A25X_OD", A25X_OD, "F4 body diameter"),
        ("A25X_hole_cc", A25X_HOLE_CC, "F4 blade holes / 1SCM10 C:C"),
        ("SCM10_H", SCM10_H, "1SCM10 overall height"),
        ("F4_plate_T", PLATE_T, "1/4 in plate under SM40s and 1SCM10s"),
        ("cover_inner_H", COVER_INNER_H, "pack cover inside height"),
        ("cover_wall", COVER_WALL, "cover wall thickness"),
        ("MCB_W", MCB_W, "CHTAIXI DZ47Z-63 2P width"),
        ("MCB_D", MCB_D, "CHTAIXI 2.95 in depth"),
        ("MCB_H", MCB_H, "CHTAIXI 3.15 in height"),
        ("section_mm2", round(BAR_W * BAR_T, 1), "copper cross section"),
    ]
    for i, (a, b, c) in enumerate(rows, start=1):
        ss.set("A" + str(i), str(a))
        ss.set("B" + str(i), str(b))
        ss.set("C" + str(i), str(c))
    return ss


def export_steps(bar_shape, sm40_shape, assembly_shape, tb1_shape=None):
    os.makedirs(OUT_DIR, exist_ok=True)
    bar_shape.exportStep(os.path.join(OUT_DIR, "copper_bar.step"))
    if tb1_shape is not None:
        tb1_shape.exportStep(os.path.join(OUT_DIR, "copper_bar_tb1.step"))
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
    master_tb1 = add_shape(doc, "Master_CopperBar_TB1", copper_bar(), COLOR_CU)
    master_sm40 = add_shape(doc, "Master_SM40", sm40_body(), COLOR_SM40)
    masters = doc.addObject("App::DocumentObjectGroup", "Masters")
    for o in (master_bar, master_tb1, master_sm40):
        masters.addObject(o)
        if o.ViewObject:
            o.ViewObject.Visibility = False

    tb1 = (0.0, 0.0, PLATE_T)
    tb2 = (0.0, PITCH_TB12, PLATE_T)
    tb3 = tb3_at_inverter(tb1, tb2)
    add_mount_plates(doc, tb1, tb2, tb3)
    build_one(doc, "TB1_PackPlus_Rear", tb1, y1_south=True)
    build_one(doc, "TB2_PackMinus", tb2)
    build_one(doc, "TB3_PackPlus_Inverter", tb3, yaw=180.0)
    add_sb350(doc, tb1, tb2, tb3)
    add_f4(doc, tb1)
    add_breakers(doc, tb1, tb2)
    add_sw1(doc, tb1)
    add_cover(doc, tb1, tb2)

    add_label(doc, "Label_TB1", ["TB1  pack +  rear"], (tb1[0], tb1[1] - 28, 70))
    add_label(doc, "Label_TB2", ["TB2  pack -"], (tb2[0], tb2[1] - 28, 70))
    add_label(doc, "Label_TB3", ["TB3  pack +  inverter"], (tb3[0], tb3[1] - 28, 70))

    doc.recompute()

    parts = [
        o.Shape
        for o in doc.Objects
        if o.TypeId == "Part::Feature"
        and not o.Name.startswith("Master")
        and "LugKeepout" not in o.Name
        and "_SW1_" not in o.Name
        and "SB350_DLO" not in o.Name
        and "F4_DLO" not in o.Name
        and "CB_DLO" not in o.Name
        and "SW1_InputLug" not in o.Name
        and "SW1_Jumper" not in o.Name
        and hasattr(o, "Shape")
        and not o.Shape.isNull()
        and o.ViewObject is not None
        and o.ViewObject.Visibility
    ]
    assembly = Part.makeCompound(parts) if parts else master_bar.Shape
    export_steps(master_bar.Shape, master_sm40.Shape, assembly, tb1_shape=master_tb1.Shape)

    path = os.path.join(OUT_DIR, "bus bars.FCStd")
    doc.saveAs(path)
    print("Saved", path)
    dx516 = abs(STUD_X1 - MOUNT_X)
    dx10 = abs(STUD_X2 - MOUNT_X)
    dy = abs(STUD_Y1 - MOUNT_Y)
    print("Bar", BAR_L, "x", BAR_W, "x", BAR_T, "mm; SM40 at", MOUNT_X, MOUNT_Y)
    print("5/16 c-c (rows)", round(abs(STUD_Y2 - STUD_Y1), 1), "  5/16 to 1/4 (ends)", abs(STUD_X2 - STUD_X1))
    print("5/16 to M10", round((dx516**2 + dy**2) ** 0.5, 1), "  1/4 to M10", round((dx10**2 + dy**2) ** 0.5, 1))
    print("SW1 on plate south of TB1; 2/0 jumper to TB1 Y1")
    print("TB1-TB2 SM40 c-c", PITCH_TB12, "  aligned air", PITCH_TB12 - BAR_W)
    print("TB3 at inverter end of SB350", [round(v, 1) for v in tb3], "yaw 180")
    return doc


doc = main()
