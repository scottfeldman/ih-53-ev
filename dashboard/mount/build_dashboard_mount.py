# Rear mount for Raspberry Pi Touch Display 2 10" + Pi 5 + PiCAN 3.
# Run inside FreeCAD. Units: mm. ASCII only.
#
# Display dims from Raspberry Pi product brief RP-010276-MM (10" Portrait):
#   glass 166.88 x 248.096, R=5; rear aluminum 143.36 x 228.73, sharp corners.
#   Glass overhang vs aluminum: 11.76 sides, 11.86 top, 7.51 bottom.
#   Four chassis bosses 121.8 x 160 (M2.5 through the plate into those
#   3 mm threaded standoffs). Four Pi standoffs
#   49 x 58, 5 mm tall, 90.06 mm from rear top to the upper pair.
# Side stack (drawing): glass 1.1 + aluminum 5.95 = 7.05 glass-front to
# aluminum-back. Plate sits on the 3 mm rear standoffs; the bevel wraps
# from those standoff tops to the glass front (7.05 + 3).
# Hood is fused to the plate (one print) over the Pi 5 + PiCAN 3,
# 31 mm inner height, with USB/Ethernet windows on the USB short edge and a
# USB-C cable hole on the long edge opposite GPIO (adjacent to Ethernet).
# Lid is a separate 4x M3 self-tap cover.
# Hinge barrels sit on the cabin face of the USB-C long edge (-X), raised
# so the pin is in the clear; a tunnel under the barrels lets the USB-C
# cable plug in. M6 threaded rod + printed round knobs set friction.
# Truck bracket fingers mesh between those barrels. 4x M2.5 through the
# plate into the display tabs (no counterbore).
# PiCAN 3 Rev C: 40-pin GPIO along one long edge; DB9 + 4-way screw terminal
# on the opposite long edge. Terminal silkscreen (user guide): 1 CAN_H,
# 2 CAN_L, 3 GND, 4 +12V. Four-wire gland is on the USB-C wall (-X).
# Wires: CAN-PI-H, CAN-PI-L, 12-PISW, 12-PIGND (schematic/wires.md).
#
# Z=0 is the outer face of the display rear aluminum (the 5.95 mm block).
# +Z is toward the cabin. Glass front is at Z=-7.05. Screw standoffs stick
# +3 mm from Z=0; the plate seats on those.
# Origin XY is the centre of the rear metal. +Y is portrait-screen up.
#
# Print PETG (supports OK: hinge and hood stand on the cabin face):
#   plate    -- wrap/glass rim on the bed. Hood walls and hinge print up.
#               Support the aluminum-pocket roof.
#   bracket  -- truck foot on the bed, knuckles up.
#   knob     -- stand-off boss on the bed (hinge side). Two of them.
#               Drop an M6 hex nut in the pocket on the opposite face.
#   lid      -- flat cover on the bed, M3 seats facing up.

import math
import os

import FreeCAD as App
import Part

try:
    import FreeCADGui as Gui
except ImportError:
    Gui = None

OUT_DIR = "/Users/sfeldma/work/ih-53-ev/dashboard/mount"
DOC_NAME = "DashboardMount"

# --- Touch Display 2 10" (product brief physical spec) ---
GLASS_W = 166.88
GLASS_H = 248.096
GLASS_R = 5.0
# Aluminum chassis corners are sharp (not the glass R5). Tiny break-edge for FDM.
AL_R = 0.8
REAR_W = 143.36
REAR_H = 228.73
GLASS_T = 1.1
FRONT_STACK = 7.05
REAR_T = FRONT_STACK - GLASS_T
OVERALL_T = FRONT_STACK
BOSS_H = 3.0
REAR_TOP_INSET = 11.86
GLASS_SIDE = (GLASS_W - REAR_W) / 2.0
Z_GLASS_FRONT = -OVERALL_T
# Wrap wall ~2.8 mm (was 0.8 at the aluminum root; PETG snapped).
AL_POCKET_CLR = 0.4
WRAP_WALL = 2.8
BACK_LIP = AL_POCKET_CLR + WRAP_WALL
WRAP_INSET = 0.25
FRONT_RIM = WRAP_WALL
BOSS_FROM_TOP = 34.56
BOSS_FROM_SIDE = 10.78
MOUNT_DX = 121.8
MOUNT_DY = 160.0
PI_HOLE_DX = 49.0
PI_HOLE_DY = 58.0
PI_HOLE_FROM_TOP = 90.06
PI_STAND_H = 5.0
PI_STAND_OD = 5.0
M25 = 2.5

# --- Pi 5 ---
PI_L = 85.0
PI_W = 56.0
PI_T = 1.6
PI_HOLE_EDGE = 3.5
USB_H = 16.0
ETH_H = 13.5
# RP-008347-DS: USB-C / dual micro-HDMI sit on the long edge opposite
# GPIO (drawing bottom). 11.2 is the USB-C centre from the left short
# edge. USB/Ethernet envelopes from STEP, same edge as datum (Y=0).
USBC_FROM_LEFT = 11.2
USBC_W = 8.94
HDMI0_FROM_LEFT = 25.8
HDMI1_FROM_LEFT = 39.2
ETH_FROM_USBC_EDGE = (2.25, 18.15)
USB_FROM_USBC_EDGE = (22.30, 54.66)

# --- PiCAN 3 HAT (HAT outline + DB9 / 4-way 5.08 mm terminal) ---
HAT_L = 65.0
HAT_W = 56.5
HAT_T = 1.6
HAT_GAP = 11.0
TERM_PITCH = 5.08
TERM_N = 4
TERM_H = 10.0
TERM_W = 8.2
DB9_L = 31.0
DB9_W = 12.6
DB9_H = 12.5
DB9_OVERHANG = 10.0
INDUCTOR_S = 12.0

# --- mount (PETG) ---
PLATE_T = 6.0
WALL = 3.0
LID_T = 3.0
CAVITY_CLEAR = 7.0
HOOD_INNER_H = 31.0
# Pi 5 port envelopes plus plug clearance so a cable can seat with the
# hood on. USB-C hole is on the GPIO-opposite long wall, next to Ethernet.
PORT_CLR = 1.8
# Extra Z above the USB-A / RJ45 shells for bulky overmolds.
PORT_PLUG_CLR = 6.0
USBC_PLUG_H = 8.0
# M2.5 through the plate into the display's threaded tabs (not tapped in
# PETG). Straight 3.0 mm through; no head recess.
M25_THRU = 3.0
M3_CLR = 3.3
# M3x0.5 self-tap into PETG. Minor is ~2.39; 2.7 prints a bit small and bites.
M3_TAP = 2.7
M3_TAP_H = 10.0
M3_BOSS_OD = 9.5
M3_POST_IN = 3.4
M3_HEAD_D = 6.2
M3_HEAD_H = 1.6
VENT_W = 3.0
VENT_PITCH = 7.5
VENT_ROW_H = 9.0
VENT_MARGIN = 10.0
WIRE_HOLE = 4.6
HOOD_R = 4.0
# Tilt hinge on the USB-C long edge (-X). Barrels stand on the cabin
# face of the plate so the pin is in the open. Axis along +Y.
# M6 threaded rod; printed round knobs clamp the stack to hold tilt.
# HINGE_SIDE -1 = USB-C/-X, +1 = GPIO/+X.
HINGE_SIDE = -1.0
HINGE_PIN_D = 6.0
HINGE_PIN_CLR = 6.6
HINGE_OD = 18.0
HINGE_X = 18.0
HINGE_PED = 15.0
HINGE_KW = 14.0
HINGE_GAP = 0.8
HINGE_PLATE_N = 5
HINGE_BRKT_N = 4
HINGE_FOOT_T = 6.0
HINGE_FOOT_Y = 38.0
HINGE_PIN_OVERHANG = 16.0
# Knob OD cleared the hinge knuckles at 32; 28 turns freely.
# Stand-off boss is on the hinge side (opposite the nut pocket).
HINGE_KNOB_D = 28.0
HINGE_KNOB_T = 10.0
HINGE_KNOB_BOSS_D = 14.0
HINGE_KNOB_BOSS_H = 2.5
HINGE_KNOB_HEX = 10.6
HINGE_KNOB_HEX_T = 5.6
HINGE_KNOB_GAP = 0.8
M6_SLOT_W = 6.4
M6_SLOT_L = 14.0

COLOR_PETG = (0.14, 0.14, 0.16)
COLOR_LID = (0.20, 0.20, 0.22)
COLOR_BRACKET = (0.16, 0.16, 0.18)
COLOR_KNOB = (0.18, 0.18, 0.20)
COLOR_GLASS = (0.05, 0.05, 0.06)
COLOR_METAL = (0.72, 0.74, 0.76)
COLOR_PCB = (0.10, 0.42, 0.18)
COLOR_HAT = (0.08, 0.32, 0.16)
COLOR_SS = (0.78, 0.78, 0.80)
COLOR_USB = (0.55, 0.55, 0.58)
COLOR_TERM = (0.12, 0.12, 0.12)
COLOR_CAN_H = (0.85, 0.75, 0.10)
COLOR_CAN_L = (0.20, 0.55, 0.25)
COLOR_12V = (0.75, 0.08, 0.08)
COLOR_GND = (0.08, 0.08, 0.08)

WIRE_NAMES = ("CAN_H", "CAN_L", "GND", "p12V")
WIRE_COLORS = (COLOR_CAN_H, COLOR_CAN_L, COLOR_GND, COLOR_12V)


def rear_top_y():
    return REAR_H / 2.0


def mount_hole_xys():
    x = MOUNT_DX / 2.0
    y_top = rear_top_y() - BOSS_FROM_TOP
    y_bot = y_top - MOUNT_DY
    return ((-x, y_top), (x, y_top), (-x, y_bot), (x, y_bot))


def pi_hole_xys():
    x = PI_HOLE_DX / 2.0
    y_top = rear_top_y() - PI_HOLE_FROM_TOP
    y_bot = y_top - PI_HOLE_DY
    return ((-x, y_top), (x, y_top), (-x, y_bot), (x, y_bot))


def pi_hdmi_y():
    # Left short edge in RP-008347-DS (opposite USB/Ethernet). DSI / CAM
    # sit on this end; USB-C is NOT here -- it is on the long edge.
    return (rear_top_y() - PI_HOLE_FROM_TOP) + PI_HOLE_EDGE


def pi_usb_y():
    return pi_hdmi_y() - PI_L


def pi_center():
    return (0.0, 0.5 * (pi_hdmi_y() + pi_usb_y()))


def pi_pcb_z():
    return PI_STAND_H + PI_T


def pi_x_from_usbc_edge(d):
    # Drawing bottom (USB-C / HDMI long edge) maps to our -X.
    return -PI_W / 2.0 + d


def usb_window_xy():
    a, b = USB_FROM_USBC_EDGE
    return (pi_x_from_usbc_edge(a) - PORT_CLR, pi_x_from_usbc_edge(b) + PORT_CLR)


def eth_window_xy():
    a, b = ETH_FROM_USBC_EDGE
    return (pi_x_from_usbc_edge(a) - PORT_CLR, pi_x_from_usbc_edge(b) + PORT_CLR)


def usbc_y0():
    return pi_hdmi_y() - (USBC_FROM_LEFT + USBC_W / 2.0)


def usbc_y1():
    return pi_hdmi_y() - (USBC_FROM_LEFT - USBC_W / 2.0)


def usbc_window_y():
    return (usbc_y0() - PORT_CLR, usbc_y1() + PORT_CLR)


def hinge_r():
    return HINGE_OD / 2.0


def hinge_plate_edge():
    px0, _, px1, _ = rear_xy(BACK_LIP)
    if HINGE_SIDE < 0:
        return px0
    return px1


def hinge_x0x1():
    edge = hinge_plate_edge()
    inward = edge - HINGE_SIDE * HINGE_X
    return (min(edge, inward), max(edge, inward))


def hinge_axis_xz():
    # Flush with the plate edge, raised on a neck so knobs clear the plate
    # and a USB-C cable can pass under the barrels.
    edge = hinge_plate_edge()
    x = edge - HINGE_SIDE * hinge_r()
    z = plate_z1() + HINGE_PED + hinge_r()
    return x, z


def hinge_z_top():
    return plate_z1() + HINGE_PED + HINGE_OD


def hinge_span():
    n = HINGE_PLATE_N + HINGE_BRKT_N
    return n * HINGE_KW + (n - 1) * HINGE_GAP


def hinge_knuckle_ys(which):
    # P B P B ... along +Y, centred on the hinge edge.
    total = hinge_span()
    y = -total / 2.0
    spans = []
    plate = True
    for _i in range(HINGE_PLATE_N + HINGE_BRKT_N):
        if (plate and which == "plate") or ((not plate) and which == "bracket"):
            spans.append((y, y + HINGE_KW))
        y += HINGE_KW + HINGE_GAP
        plate = not plate
    return spans


def hinge_pin_len():
    return hinge_span() + 2.0 * HINGE_PIN_OVERHANG


def hinge_pin_cutter():
    x_ax, z_ax = hinge_axis_xz()
    total = hinge_pin_len()
    extra = 4.0
    return cyl(
        HINGE_PIN_CLR,
        total + 2.0 * extra,
        x_ax,
        -total / 2.0 - extra,
        z_ax,
        (0, 1, 0),
    )


def hinge_barrel_blank():
    x0, x1 = hinge_x0x1()
    x_ax, z_ax = hinge_axis_xz()
    hy0 = -hinge_span() / 2.0
    hy1 = hinge_span() / 2.0
    barrel = cyl(HINGE_OD, hy1 - hy0, x_ax, hy0, z_ax, (0, 1, 0))
    neck = box(
        x0,
        hy0,
        plate_z1() - 0.4,
        x1,
        hy1,
        plate_z1() + HINGE_PED + hinge_r(),
    )
    return fuse_all([barrel, neck])


def hinge_slot_cutters():
    x0, x1 = hinge_x0x1()
    g = HINGE_GAP / 2.0
    cuts = []
    for y0, y1 in hinge_knuckle_ys("bracket"):
        cuts.append(
            box(
                x0 - 1.0,
                y0 - g,
                plate_z1() - 0.3,
                x1 + 1.0,
                y1 + g,
                hinge_z_top() + 1.0,
            )
        )
    return cuts


def hex_prism(af, h, x, y, z):
    r = af / math.sqrt(3.0)
    verts = []
    for i in range(6):
        a = math.radians(60.0 * i + 30.0)
        verts.append(App.Vector(x + r * math.cos(a), y + r * math.sin(a), z))
    verts.append(verts[0])
    return Part.Face(Part.makePolygon(verts)).extrude(App.Vector(0, 0, h))


def build_knob():
    # Stand-off boss on the bed (z <= 0) faces the hinge. Hex nut pocket
    # on the outer face (z = T). Through-hole along +Z.
    t = HINGE_KNOB_T
    bh = HINGE_KNOB_BOSS_H
    knob = cyl(HINGE_KNOB_D, t, 0.0, 0.0, 0.0)
    boss = cyl(HINGE_KNOB_BOSS_D, bh, 0.0, 0.0, -bh)
    knob = fuse_all([knob, boss])
    n = 8
    rd = HINGE_KNOB_D / 2.0 + 1.2
    for i in range(n):
        a = i * 2.0 * math.pi / n
        knob = knob.cut(
            cyl(9.0, t + 2.0, rd * math.cos(a), rd * math.sin(a), -1.0)
        )
    knob = knob.cut(
        cyl(HINGE_PIN_CLR, t + bh + 2.0, 0.0, 0.0, -bh - 1.0)
    )
    knob = knob.cut(
        hex_prism(HINGE_KNOB_HEX, HINGE_KNOB_HEX_T + 0.2, 0.0, 0.0, t - HINGE_KNOB_HEX_T)
    )
    return knob.removeSplitter()


def placed_knob(toward_plus_y):
    x_ax, z_ax = hinge_axis_xz()
    half = hinge_span() / 2.0
    # Offset from hinge end to the knob body face; boss tip sits at GAP.
    offset = HINGE_KNOB_GAP + HINGE_KNOB_BOSS_H
    k = build_knob()
    if toward_plus_y:
        k.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -90.0)
        k.translate(App.Vector(x_ax, half + offset, z_ax))
    else:
        k.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 90.0)
        k.translate(App.Vector(x_ax, -(half + offset), z_ax))
    return k


def dummy_hinge_rod():
    x_ax, z_ax = hinge_axis_xz()
    h = hinge_pin_len()
    return cyl(HINGE_PIN_D, h, x_ax, -h / 2.0, z_ax, (0, 1, 0))


def cavity_xy():
    # Drop-over envelope for Pi 5 + PiCAN 3. GPIO is +X; DB9 and the 4-way
    # terminal hang off -X. USB/Ethernet (-Y) keeps CAVITY_CLEAR.
    # Opening is NOT centered on the Pi. Left/right and the DSI end are
    # set so the remaining plate (opening to cabin-face outer edge) matches
    # the USB-end remaining plate.
    px0, py0, px1, py1 = rear_xy(BACK_LIP)
    y0 = pi_usb_y() - CAVITY_CLEAR
    edge = y0 - py0
    y1 = py1 - edge
    x0 = -PI_W / 2.0 - CAVITY_CLEAR - DB9_OVERHANG
    x1 = px1 - (x0 - px0)
    return (x0, y0, x1, y1)


def pican_term_pin_ys():
    # Pin 1 CAN_H toward USB (-Y), pin 4 +12V toward HDMI (+Y).
    y_p12v = pi_hdmi_y() - 8.0
    y_canh = y_p12v - (TERM_N - 1) * TERM_PITCH
    return [y_canh + i * TERM_PITCH for i in range(TERM_N)]


def hood_z1():
    return plate_z1() + HOOD_INNER_H


def plate_z0():
    return BOSS_H


def plate_z1():
    return BOSS_H + PLATE_T


def wrap_h():
    return plate_z0() - Z_GLASS_FRONT


def wrap_z_front():
    return Z_GLASS_FRONT


def hood_outer_m():
    return WALL


def cavity_expand(m):
    x0, y0, x1, y1 = cavity_xy()
    return (x0 - m, y0 - m, x1 + m, y1 + m)


def cavity_rr(m, z0, z1, r=None):
    if r is None:
        r = HOOD_R + max(m, 0.0)
    return rounded_rect(*(cavity_expand(m) + (z0, z1, r)))


def rear_xy(margin=0.0):
    return (
        -REAR_W / 2.0 - margin,
        -REAR_H / 2.0 - margin,
        REAR_W / 2.0 + margin,
        REAR_H / 2.0 + margin,
    )


def glass_xy(inset=0.0):
    # Glass is not centered on the aluminum: 11.86 top, 7.51 bottom, 11.76 sides.
    top = rear_top_y() + REAR_TOP_INSET - inset
    bot = rear_top_y() + REAR_TOP_INSET - GLASS_H + inset
    left = -GLASS_W / 2.0 + inset
    right = GLASS_W / 2.0 - inset
    return (left, bot, right, top)


def profile_wire(x0, y0, x1, y1, z, r):
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    r = min(r, (x1 - x0) / 2.0 - 0.05, (y1 - y0) / 2.0 - 0.05)
    # Quarter-circle midpoints (not the square corners -- those make
    # bulbous semicircles that overshoot the outline).
    k = r * (1.0 - math.sqrt(2.0) / 2.0)
    p = [
        App.Vector(x0 + r, y0, z),
        App.Vector(x1 - r, y0, z),
        App.Vector(x1, y0 + r, z),
        App.Vector(x1, y1 - r, z),
        App.Vector(x1 - r, y1, z),
        App.Vector(x0 + r, y1, z),
        App.Vector(x0, y1 - r, z),
        App.Vector(x0, y0 + r, z),
    ]
    segs = [
        Part.LineSegment(p[0], p[1]),
        Part.Arc(p[1], App.Vector(x1 - k, y0 + k, z), p[2]),
        Part.LineSegment(p[2], p[3]),
        Part.Arc(p[3], App.Vector(x1 - k, y1 - k, z), p[4]),
        Part.LineSegment(p[4], p[5]),
        Part.Arc(p[5], App.Vector(x0 + k, y1 - k, z), p[6]),
        Part.LineSegment(p[6], p[7]),
        Part.Arc(p[7], App.Vector(x0 + k, y0 + k, z), p[0]),
    ]
    return Part.Wire([s.toShape() for s in segs])


def rounded_rect(x0, y0, x1, y1, z0, z1, r):
    if z0 > z1:
        z0, z1 = z1, z0
    if r < 0.2:
        return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, App.Vector(min(x0, x1), min(y0, y1), z0))
    wire = profile_wire(x0, y0, x1, y1, z0, r)
    return Part.Face(wire).extrude(App.Vector(0, 0, z1 - z0))


def _ordered_edges(wire):
    if hasattr(wire, "OrderedEdges"):
        return list(wire.OrderedEdges)
    return list(wire.Edges)


def ruled_solid(w_back, w_front):
    # Pair edges 1:1 (line-to-line, arc-to-arc). A whole-wire loft maps by
    # perimeter fraction, so sharp aluminum corners do not stay matched to
    # glass R5 and the bevel balloons past the front panel.
    e0 = _ordered_edges(w_back)
    e1 = _ordered_edges(w_front)
    if len(e0) != len(e1):
        raise RuntimeError("wrap edge count %d vs %d" % (len(e0), len(e1)))
    faces = [Part.Face(w_back), Part.Face(w_front)]
    for a, b in zip(e0, e1):
        faces.append(Part.makeRuledSurface(a, b))
    shell = Part.Shell(faces)
    if not shell.isValid():
        shell.fix(1e-5, 1e-5, 1e-5)
    solid = Part.Solid(shell)
    if solid.Volume < 0.0:
        solid = Part.Solid(shell.reversed())
    if not solid.isValid() or solid.Volume <= 0.0:
        raise RuntimeError("wrap solid invalid vol=%s" % solid.Volume)
    return solid


def wrap_shell():
    # From boss tops (plate seat) to the glass front. Inner loft leaves a
    # ~FRONT_RIM lip on the glass. Glass is offset (more overhang at top).
    z_back = plate_z0()
    z_front = wrap_z_front()
    inner_r = max(GLASS_R - FRONT_RIM, 0.8)
    outer_back = profile_wire(*(rear_xy(BACK_LIP) + (z_back, AL_R)))
    outer_front = profile_wire(*(glass_xy(WRAP_INSET) + (z_front, GLASS_R)))
    inner_back = profile_wire(*(rear_xy(AL_POCKET_CLR) + (z_back, AL_R)))
    inner_front = profile_wire(
        *(glass_xy(WRAP_INSET + FRONT_RIM) + (z_front, inner_r))
    )
    return ruled_solid(outer_back, outer_front).cut(
        ruled_solid(inner_back, inner_front)
    )


def cyl(d, h, x, y, z, axis=(0, 0, 1)):
    return Part.makeCylinder(
        d / 2.0, h, App.Vector(x, y, z), App.Vector(*axis)
    )


def box(x0, y0, z0, x1, y1, z1):
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    if z0 > z1:
        z0, z1 = z1, z0
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, App.Vector(x0, y0, z0))


def fuse_all(shapes):
    shapes = [s for s in shapes if s is not None]
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out.removeSplitter()


def cut_all(base, tools):
    for t in tools:
        if t is not None:
            base = base.cut(t)
    return base.removeSplitter()


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


def add_label(doc, name, text, pos):
    a = doc.addObject("App::Annotation", name)
    a.LabelText = text
    a.Position = App.Vector(*pos)
    vo = getattr(a, "ViewObject", None)
    if vo:
        vo.FontSize = 12
        vo.TextColor = (1.0, 1.0, 1.0)
    return a


def wire_ys():
    return pican_term_pin_ys()


def _overlaps(a0, a1, b0, b1):
    return a0 < b1 and b0 < a1


def _slot_starts(a0, a1, width, pitch):
    span = a1 - a0
    if span < width:
        return []
    n = int((span - width) / pitch) + 1
    used = (n - 1) * pitch + width
    start = a0 + 0.5 * (span - used)
    return [start + i * pitch for i in range(n)]


def _skip_hit(p0, p1, skips):
    for s0, s1 in skips:
        if _overlaps(p0, p1, s0, s1):
            return True
    return False


def wall_vents_along_y(x_a, x_b, y0, y1, z0, z1, skips):
    cuts = []
    for y in _slot_starts(y0, y1, VENT_W, VENT_PITCH):
        if not _skip_hit(y, y + VENT_W, skips):
            cuts.append(box(x_a, y, z0, x_b, y + VENT_W, z1))
    return cuts


def wall_vents_along_x(x0, x1, y_a, y_b, z0, z1, skips):
    cuts = []
    for x in _slot_starts(x0, x1, VENT_W, VENT_PITCH):
        if not _skip_hit(x, x + VENT_W, skips):
            cuts.append(box(x, y_a, z0, x + VENT_W, y_b, z1))
    return cuts


def dummy_display():
    gx0, gy0, gx1, gy1 = glass_xy(0.0)
    z_glass0 = Z_GLASS_FRONT
    z_glass1 = z_glass0 + GLASS_T
    z_al0 = -REAR_T
    glass = rounded_rect(gx0, gy0, gx1, gy1, z_glass0, z_glass1, GLASS_R)
    rx0, ry0, rx1, ry1 = rear_xy(0.0)
    metal = rounded_rect(rx0, ry0, rx1, ry1, z_al0, 0.0, AL_R)
    bosses = []
    stands = []
    for x, y in mount_hole_xys():
        b = cyl(6.5, BOSS_H, x, y, 0.0)
        bosses.append(b.cut(cyl(M25, BOSS_H + 0.4, x, y, -0.2)))
    metal = metal.cut(fuse_all([cyl(M25, REAR_T + 1.0, x, y, -REAR_T - 0.5) for x, y in mount_hole_xys()]))
    for x, y in pi_hole_xys():
        s = cyl(PI_STAND_OD, PI_STAND_H, x, y, 0.0)
        stands.append(s.cut(cyl(M25, PI_STAND_H + 0.4, x, y, -0.2)))
    # display DSI / J1 between the Pi standoffs
    dsi = box(-8.0, pi_hole_xys()[2][1] + 8.0, 0.0, 8.0, pi_hole_xys()[0][1] - 8.0, 3.5)
    return glass, metal, fuse_all(bosses), fuse_all(stands), dsi


def dummy_pi():
    y1 = pi_hdmi_y()
    y0 = pi_usb_y()
    x0 = -PI_W / 2.0
    x1 = PI_W / 2.0
    z0 = PI_STAND_H
    pcb = box(x0, y0, z0, x1, y1, z0 + PI_T)
    for x, y in pi_hole_xys():
        pcb = pcb.cut(cyl(2.8, PI_T + 0.4, x, y, z0 - 0.2))
    usb_z = z0 + PI_T
    ux0, ux1 = usb_window_xy()
    ex0, ex1 = eth_window_xy()
    uy0, uy1 = usbc_window_y()
    usb = box(ux0 + PORT_CLR, y0 - 3.9, usb_z, ux1 - PORT_CLR, y0 + 8.0, usb_z + USB_H)
    eth = box(ex0 + PORT_CLR, y0 - 3.0, usb_z, ex1 - PORT_CLR, y0 + 14.0, usb_z + ETH_H)
    usbc = box(x0 - 1.2, uy0 + PORT_CLR, usb_z, x0 + 1.2, uy1 - PORT_CLR, usb_z + 3.2)
    hdmi = box(
        x0 - 1.0,
        pi_hdmi_y() - HDMI1_FROM_LEFT - 3.3,
        usb_z,
        x0 + 1.0,
        pi_hdmi_y() - HDMI0_FROM_LEFT + 3.3,
        usb_z + 3.0,
    )
    gpio = box(x1 - 5.2, y0 + 24.5, usb_z, x1 - 0.2, y0 + 24.5 + 51.0, usb_z + 8.5)
    return pcb, fuse_all([usb, eth, usbc, hdmi]), gpio


def dummy_pican():
    y1 = pi_hdmi_y()
    y0 = y1 - HAT_L
    x0 = -HAT_W / 2.0
    x1 = HAT_W / 2.0
    z0 = PI_STAND_H + PI_T + HAT_GAP
    pcb = box(x0, y0, z0, x1, y1, z0 + HAT_T)
    for x, y in pi_hole_xys():
        if y0 - 1.0 < y < y1 + 1.0:
            pcb = pcb.cut(cyl(2.8, HAT_T + 0.4, x, y, z0 - 0.2))
    # DB9 + 4-way terminal on the long edge opposite the 40-pin GPIO (-X).
    wys = pican_term_pin_ys()
    tx1 = -PI_W / 2.0 + 1.5
    tx0 = tx1 - TERM_W
    ty0 = wys[0] - TERM_PITCH / 2.0
    ty1 = wys[-1] + TERM_PITCH / 2.0
    term = box(tx0, ty0, z0 + HAT_T, tx1, ty1, z0 + HAT_T + TERM_H)
    db9_y1 = ty0 - 2.0
    db9_y0 = db9_y1 - DB9_L
    db9 = box(
        -PI_W / 2.0 - DB9_OVERHANG,
        db9_y0,
        z0 + HAT_T,
        -PI_W / 2.0 + 2.0,
        db9_y1,
        z0 + HAT_T + DB9_H,
    )
    ind = box(x0 + 2.0, y0 + 14.0, z0 + HAT_T, x0 + 2.0 + INDUCTOR_S, y0 + 14.0 + INDUCTOR_S, z0 + HAT_T + 10.0)
    header = box(x1 - 5.2, y0 + 4.5, z0 + HAT_T, x1 - 0.2, y0 + 4.5 + 51.0, z0 + HAT_T + 8.5)
    term_x = 0.5 * (tx0 + tx1)
    return pcb, db9, term, fuse_all([ind, header]), term_x, wys, z0 + HAT_T + TERM_H


def dummy_wires(term_x, term_ys, term_z, gland_x, gland_z):
    wires = []
    for y in term_ys:
        a = cyl(2.3, 8.0, term_x, y, term_z)
        dx = gland_x - term_x
        if abs(dx) > 1.0:
            bar = cyl(2.3, abs(dx), term_x, y, term_z + 6.0, (-1 if dx < 0 else 1, 0, 0))
        else:
            bar = None
        through = cyl(2.3, 16.0, gland_x, y, gland_z, (1 if gland_x > 0 else -1, 0, 0))
        wires.append(fuse_all([s for s in (a, bar, through) if s is not None]))
    return wires


def lid_post_xys():
    x0, y0, x1, y1 = cavity_xy()
    return (
        (x0 + M3_POST_IN, y0 + M3_POST_IN),
        (x1 - M3_POST_IN, y0 + M3_POST_IN),
        (x0 + M3_POST_IN, y1 - M3_POST_IN),
        (x1 - M3_POST_IN, y1 - M3_POST_IN),
    )


def wire_gland_x():
    return cavity_xy()[0] - hood_outer_m()


def opening_cutter():
    # Through the plate only. Hood interior is already hollow; cutting
    # through the hood height would eat the lid-screw posts.
    return cavity_rr(0.0, plate_z0() - 2.0, plate_z1() + 0.05, HOOD_R)


def hood_body():
    x0, y0, x1, y1 = cavity_xy()
    z0 = plate_z1()
    z1 = hood_z1()
    om = hood_outer_m()
    outer = cavity_rr(om, z0 - 0.4, z1, HOOD_R + 1.2)
    hood = outer.cut(cavity_rr(0.0, z0 - 1.0, z1 + 1.0, HOOD_R))
    posts = [cyl(M3_BOSS_OD, z1 - z0 + 0.3, x, y, z0) for x, y in lid_post_xys()]
    return fuse_all([hood] + posts)


def hood_cutters():
    x0, y0, x1, y1 = cavity_xy()
    z0 = plate_z1()
    z1 = hood_z1()
    om = hood_outer_m()
    cuts = []
    for x, y in lid_post_xys():
        cuts.append(cyl(M3_TAP, M3_TAP_H + 1.5, x, y, z1 - M3_TAP_H))

    wys = wire_ys()
    gx_out = x0 - om
    for y in wys:
        cuts.append(cyl(WIRE_HOLE, om + 8.0, x0 + 1.0, y, z1, (-1, 0, 0)))
    cuts.append(
        box(
            gx_out - 0.6,
            wys[0] - WIRE_HOLE,
            z1 - WIRE_HOLE / 2.0,
            x0 + 0.2,
            wys[-1] + WIRE_HOLE,
            z1 + 1.0,
        )
    )

    pcb_z = pi_pcb_z()
    ux0, ux1 = usb_window_xy()
    ex0, ex1 = eth_window_xy()
    uy0, uy1 = usbc_window_y()
    usb_top = pcb_z + USB_H + PORT_PLUG_CLR
    eth_top = pcb_z + USB_H + PORT_PLUG_CLR
    cuts.append(box(ux0, y0 - om - 1.5, z0 - 0.5, ux1, y0 + 8.0, usb_top))
    cuts.append(box(ex0, y0 - om - 1.5, z0 - 0.5, ex1, y0 + 8.0, eth_top))
    usbc_y = 0.5 * (uy0 + uy1)
    usbc_z = pcb_z + 0.5 * USBC_PLUG_H
    usbc_d = max(uy1 - uy0, USBC_PLUG_H + 3.0)
    cuts.append(cyl(usbc_d, om + 3.0, x0 + 1.2, usbc_y, usbc_z, (-1, 0, 0)))

    vz_lo0 = z0 + 7.0
    vz_lo1 = vz_lo0 + VENT_ROW_H
    vz_hi0 = z1 - 4.0 - VENT_ROW_H
    vz_hi1 = z1 - 4.0
    ym0 = y0 + VENT_MARGIN
    ym1 = y1 - VENT_MARGIN
    xm0 = x0 + VENT_MARGIN
    xm1 = x1 - VENT_MARGIN
    gland_skip = [(wys[0] - WIRE_HOLE - 2.0, wys[-1] + WIRE_HOLE + 2.0)]
    usbc_skip = [(uy0 - 3.0, uy1 + 3.0)]

    # +X GPIO wall.
    cuts.extend(wall_vents_along_y(x1 - 0.8, x1 + om + 0.5, ym0, ym1, vz_lo0, vz_lo1, []))
    cuts.extend(wall_vents_along_y(x1 - 0.8, x1 + om + 0.5, ym0, ym1, vz_hi0, vz_hi1, []))
    # -X USB-C wall: skip the power-cable hole on the lower row and the
    # 4-wire comb on the upper row.
    cuts.extend(wall_vents_along_y(x0 - om - 0.5, x0 + 0.8, ym0, ym1, vz_lo0, vz_lo1, usbc_skip))
    cuts.extend(wall_vents_along_y(x0 - om - 0.5, x0 + 0.8, ym0, ym1, vz_hi0, vz_hi1, gland_skip))
    # +Y HDMI wall.
    cuts.extend(wall_vents_along_x(xm0, xm1, y1 - 0.8, y1 + om + 0.5, vz_lo0, vz_lo1, []))
    cuts.extend(wall_vents_along_x(xm0, xm1, y1 - 0.8, y1 + om + 0.5, vz_hi0, vz_hi1, []))
    # -Y USB/Ethernet wall: upper row, outside the taller port bays.
    port_skip = [(ex0 - 1.5, ex1 + 1.5), (ux0 - 1.5, ux1 + 1.5)]
    cuts.extend(wall_vents_along_x(xm0, xm1, y0 - om - 0.5, y0 + 0.8, vz_hi0, vz_hi1, port_skip))

    return cuts


def build_plate():
    px0, py0, px1, py1 = rear_xy(BACK_LIP)
    z0 = plate_z0()
    plate = rounded_rect(px0, py0, px1, py1, z0, plate_z1(), AL_R)
    plate = fuse_all([plate, wrap_shell(), hinge_barrel_blank(), hood_body()])
    cuts = [opening_cutter(), hinge_pin_cutter()] + hinge_slot_cutters() + hood_cutters()
    for x, y in mount_hole_xys():
        cuts.append(cyl(M25_THRU, PLATE_T + 8.0, x, y, z0 - 2.0))
    plate = cut_all(plate, cuts)
    if len(plate.Solids) > 1:
        plate = fuse_all(list(plate.Solids))
    return plate


def build_bracket():
    edge = hinge_plate_edge()
    x_ax, z_ax = hinge_axis_xz()
    hy0 = -hinge_span() / 2.0
    hy1 = hinge_span() / 2.0
    z_web = plate_z1() + HINGE_PED
    x_out = edge + HINGE_SIDE * 10.0
    fingers = []
    for y0, y1 in hinge_knuckle_ys("bracket"):
        barrel = cyl(HINGE_OD, y1 - y0, x_ax, y0, z_ax, (0, 1, 0))
        lug = box(x_ax, y0, z_web, x_out, y1, hinge_z_top())
        fingers.append(fuse_all([barrel, lug]))
    web = box(edge, hy0, z_web, x_out, hy1, hinge_z_top())
    foot_a = edge + HINGE_SIDE * 6.0
    foot_b = foot_a + HINGE_SIDE * HINGE_FOOT_Y
    foot = box(
        foot_a,
        hy0 - 8.0,
        z_web,
        foot_b,
        hy1 + 8.0,
        z_web + HINGE_FOOT_T,
    )
    br = fuse_all(fingers + [web, foot])
    cuts = [hinge_pin_cutter()]
    slot_x0 = 0.5 * (foot_a + foot_b) - M6_SLOT_L / 2.0
    for sy in (-hinge_span() / 4.0, hinge_span() / 4.0):
        cuts.append(
            box(
                slot_x0,
                sy - M6_SLOT_W / 2.0,
                z_web - 1.0,
                slot_x0 + M6_SLOT_L,
                sy + M6_SLOT_W / 2.0,
                z_web + HINGE_FOOT_T + 1.0,
            )
        )
    br = cut_all(br, cuts)
    if len(br.Solids) > 1:
        br = fuse_all(list(br.Solids))
    return br


def build_lid(lid_pts, wys, gland_x, gland_z):
    # Flat cover only — no inner ridge (clears the M3 screw bosses) and
    # no wire grooves (hood slot is enough to pass the four wires).
    x0, y0, x1, y1 = cavity_xy()
    om = hood_outer_m()
    lid = cavity_rr(om, gland_z, gland_z + LID_T, HOOD_R + 1.6)

    cuts = []
    for x, y in lid_pts:
        cuts.append(cyl(M3_CLR, LID_T + 4.0, x, y, gland_z - 2.0))

    # lid vents, inset from screws and the rim, through the full lid
    inset = 12.0
    for y in _slot_starts(y0 + inset, y1 - inset, 22.0, 28.0):
        for x in _slot_starts(x0 + inset, x1 - inset, VENT_W, VENT_PITCH):
            cuts.append(
                box(x, y, gland_z - 2.0, x + VENT_W, y + 22.0, gland_z + LID_T + 1.0)
            )

    return cut_all(lid, cuts)


def dummy_screws(lid_pts, gland_z):
    sh = []
    for x, y in mount_hole_xys():
        sh.append(cyl(4.5, 1.4, x, y, plate_z1()))
        sh.append(cyl(2.45, PLATE_T + BOSS_H + 4.0, x, y, -BOSS_H - 3.0))
    for x, y in lid_pts:
        sh.append(cyl(5.5, M3_HEAD_H, x, y, gland_z + LID_T - M3_HEAD_H))
        sh.append(cyl(2.9, M3_HEAD_H + M3_TAP_H + 1.0, x, y, gland_z - M3_TAP_H))
    return fuse_all(sh)


def fill_spreadsheet(doc):
    ss = doc.addObject("Spreadsheet::Sheet", "Dimensions")
    rows = [
        ("param", "mm", "note"),
        ("glass_W", GLASS_W, "TD2 10in front, RP-010276-MM"),
        ("glass_H", GLASS_H, "portrait"),
        ("rear_W", REAR_W, "rear metal"),
        ("rear_H", REAR_H, "rear metal"),
        ("mount_DX", MOUNT_DX, "4x M2.5 chassis bosses"),
        ("mount_DY", MOUNT_DY, "4x M2.5 chassis bosses"),
        ("al_R", AL_R, "aluminum corner, sharp"),
        ("glass_R", GLASS_R, "front panel corner"),
        ("glass_side", GLASS_SIDE, "glass overhang each side"),
        ("rear_top_inset", REAR_TOP_INSET, "glass overhang top"),
        ("back_lip", BACK_LIP, "plate over aluminum edge"),
        ("front_rim", FRONT_RIM, "inner wall at wrap front"),
        ("wrap_wall", WRAP_WALL, "flare wall, aluminum root to glass lip"),
        ("boss_H", BOSS_H, "aluminum M2.5 standoffs, plate datum"),
        ("pi_hole_DX", PI_HOLE_DX, "Pi standoffs"),
        ("pi_hole_DY", PI_HOLE_DY, "Pi standoffs"),
        ("pi_hole_from_top", PI_HOLE_FROM_TOP, "rear top to upper Pi holes"),
        ("pi_stand_H", PI_STAND_H, "Pi standoff height"),
        ("plate_T", PLATE_T, "PETG back plate"),
        ("overall_T", OVERALL_T, "glass front to aluminum back"),
        ("rear_T", REAR_T, "aluminum = 7.05 - 1.1 glass"),
        ("front_stack", FRONT_STACK, "drawing: glass + aluminum"),
        ("glass_T", GLASS_T, "front glass"),
        ("cavity_clear", CAVITY_CLEAR, "USB/Ethernet end, opening to Pi"),
        ("wall", WALL, "hood wall, fused to plate"),
        ("hood_inner_H", HOOD_INNER_H, "clearance over PiCAN + wires"),
        ("wire_hole", WIRE_HOLE, "4x at 5.08 pitch"),
        ("term_pitch", TERM_PITCH, "PiCAN 3 terminal"),
        ("m25_thru", M25_THRU, "3.0 through plate into M2.5 display tabs"),
        ("hinge_pin", HINGE_PIN_D, "M6 threaded rod"),
        ("hinge_od", HINGE_OD, "raised cabin-face barrels"),
        ("hinge_knob", HINGE_KNOB_D, "printed round knob OD"),
        ("hinge_knob_boss", HINGE_KNOB_BOSS_D, "stand-off collar OD, hinge side"),
        ("hinge_knob_boss_H", HINGE_KNOB_BOSS_H, "stand-off height"),
        ("m3_tap", M3_TAP, "M3 self-tap into corner posts"),
        ("m3_tap_h", M3_TAP_H, "blind hole depth"),
        ("m3_boss_od", M3_BOSS_OD, "corner post OD"),
    ]
    for i, row in enumerate(rows, start=1):
        ss.set("A" + str(i), str(row[0]))
        ss.set("B" + str(i), str(row[1]))
        ss.set("C" + str(i), str(row[2]))
    return ss


def export_steps(plate, lid, bracket, knob, assembly):
    os.makedirs(OUT_DIR, exist_ok=True)
    plate.exportStep(os.path.join(OUT_DIR, "mount_plate.step"))
    lid.exportStep(os.path.join(OUT_DIR, "mount_lid.step"))
    bracket.exportStep(os.path.join(OUT_DIR, "mount_bracket.step"))
    knob.exportStep(os.path.join(OUT_DIR, "mount_knob.step"))
    assembly.exportStep(os.path.join(OUT_DIR, "mount_assembly.step"))
    plate.exportStl(os.path.join(OUT_DIR, "mount_plate.stl"))
    lid.exportStl(os.path.join(OUT_DIR, "mount_lid.stl"))
    bracket.exportStl(os.path.join(OUT_DIR, "mount_bracket.stl"))
    knob.exportStl(os.path.join(OUT_DIR, "mount_knob.stl"))


def main():
    for name in list(App.listDocuments().keys()):
        d = App.getDocument(name)
        if name == DOC_NAME or d.Label == DOC_NAME:
            App.closeDocument(name)

    doc = App.newDocument(DOC_NAME)
    if Gui is not None:
        Gui.setActiveDocument(doc.Name)

    fill_spreadsheet(doc)

    plate = build_plate()
    bracket = build_bracket()
    lid_pts = lid_post_xys()
    wys = wire_ys()
    gland_x = wire_gland_x()
    gland_z = hood_z1()
    lid = build_lid(lid_pts, wys, gland_x, gland_z)
    glass, metal, bosses, stands, dsi = dummy_display()
    pi_pcb, pi_io, gpio = dummy_pi()
    hat, db9, term, hat_top, term_x, term_ys, term_z = dummy_pican()
    wires = dummy_wires(term_x, term_ys, term_z, gland_x, gland_z)
    screws = dummy_screws(lid_pts, gland_z)
    rod = dummy_hinge_rod()
    knob = build_knob()
    knob_a = placed_knob(True)
    knob_b = placed_knob(False)

    add_shape(doc, "Mount_Plate", plate, COLOR_PETG)
    add_shape(doc, "Mount_Bracket", bracket, COLOR_BRACKET)
    add_shape(doc, "Mount_Lid", lid, COLOR_LID)
    grp = doc.addObject("App::DocumentObjectGroup", "Reference")
    grp.Label = "Reference_TD2_Pi5_PiCAN3"
    refs = [
        add_shape(doc, "TD2_Glass", glass, COLOR_GLASS, 50),
        add_shape(doc, "TD2_RearMetal", metal, COLOR_METAL),
        add_shape(doc, "TD2_MountBosses", bosses, COLOR_SS),
        add_shape(doc, "TD2_PiStandoffs", stands, COLOR_SS),
        add_shape(doc, "TD2_DSI", dsi, COLOR_TERM),
        add_shape(doc, "Pi5_PCB", pi_pcb, COLOR_PCB),
        add_shape(doc, "Pi5_IO", pi_io, COLOR_USB),
        add_shape(doc, "Pi5_GPIO", gpio, COLOR_TERM),
        add_shape(doc, "PiCAN3_PCB", hat, COLOR_HAT),
        add_shape(doc, "PiCAN3_DB9", db9, COLOR_SS),
        add_shape(doc, "PiCAN3_Terminal", term, COLOR_TERM),
        add_shape(doc, "PiCAN3_Parts", hat_top, COLOR_USB),
        add_shape(doc, "M25_Screws", screws, COLOR_SS),
        add_shape(doc, "Hinge_Rod", rod, COLOR_SS),
        add_shape(doc, "Hinge_Knob_A", knob_a, COLOR_KNOB),
        add_shape(doc, "Hinge_Knob_B", knob_b, COLOR_KNOB),
    ]
    for i, w in enumerate(wires):
        refs.append(add_shape(doc, "Wire_" + WIRE_NAMES[i], w, WIRE_COLORS[i]))
    for o in refs:
        grp.addObject(o)

    add_label(
        doc,
        "Label_Mount",
        ["IH-53 EV dash mount", "TD2 10in  4x M2.5 thru  hinge M6 rod"],
        (-REAR_W / 2.0, REAR_H / 2.0 + 12.0, hood_z1() + 8.0),
    )
    add_label(
        doc,
        "Label_Wires",
        ["gland -X  USB-C  5.08 pitch", "1 CAN_H  2 CAN_L  3 GND  4 +12V"],
        (gland_x - 8.0, wys[0] - 8.0, gland_z + 10.0),
    )
    add_label(
        doc,
        "Label_Hood",
        ["integral hood  31mm inner  USB/ETH/USB-C", "lid 4x M3 self-tap"],
        (cavity_xy()[2] + 10.0, pi_center()[1], hood_z1() + 6.0),
    )

    doc.recompute()
    assembly = Part.makeCompound(
        [plate, bracket, lid, knob_a, knob_b, rod, glass, metal, bosses, stands, dsi, pi_pcb, pi_io, gpio, hat, db9, term, hat_top, screws]
        + wires
    )
    export_steps(plate, lid, bracket, knob, assembly)
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "mount.FCStd")
    doc.saveAs(path)
    bb = plate.BoundBox
    print(
        "plate",
        round(bb.XLength, 2),
        "x",
        round(bb.YLength, 2),
        "x",
        round(bb.ZLength, 2),
    )
    print("hood_z", round(hood_z1(), 2), "inner", HOOD_INNER_H, "cavity", [round(v, 2) for v in cavity_xy()])
    x_ax, z_ax = hinge_axis_xz()
    print(
        "hinge USB-C-edge axis x",
        round(x_ax, 2),
        "z",
        round(z_ax, 2),
        "pin M6 rod",
        HINGE_PIN_D,
        "len",
        round(hinge_pin_len(), 1),
        "M2.5 thru",
        M25_THRU,
        "plate_T",
        PLATE_T,
    )
    print(
        "ports USB",
        [round(v, 2) for v in usb_window_xy()],
        "ETH",
        [round(v, 2) for v in eth_window_xy()],
        "USBC y",
        [round(v, 2) for v in usbc_window_y()],
    )
    cx0, cy0, cx1, cy1 = cavity_xy()
    px0, py0, px1, py1 = rear_xy(BACK_LIP)
    print(
        "opening to plate edge  L",
        round(cx0 - px0, 2),
        "R",
        round(px1 - cx1, 2),
        "USB",
        round(cy0 - py0, 2),
        "DSI",
        round(py1 - cy1, 2),
    )
    gx0, gy0, gx1, gy1 = glass_xy(WRAP_INSET)
    rx0, ry0, rx1, ry1 = rear_xy(BACK_LIP)
    flare = math.degrees(math.atan(((gx1 - gx0) - (rx1 - rx0)) / 2.0 / wrap_h()))
    print(
        "wrap flare",
        round(flare, 1),
        "deg  wrap_h",
        round(wrap_h(), 2),
        "wall",
        round(BACK_LIP - AL_POCKET_CLR, 2),
        "..",
        FRONT_RIM,
        "z",
        round(wrap_z_front(), 2),
        "..",
        round(plate_z1(), 2),
        "stack glass",
        GLASS_T,
        "al",
        REAR_T,
        "boss",
        BOSS_H,
    )
    print("mount holes", [(round(x, 2), round(y, 2)) for x, y in mount_hole_xys()])
    print("pi holes", [(round(x, 2), round(y, 2)) for x, y in pi_hole_xys()])
    print("wire Y", [round(y, 2) for y in wys], "gland_x", round(gland_x, 2))
    print("Saved", path)
    return doc


doc = main()
