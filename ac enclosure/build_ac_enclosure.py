# AC enclosure: Cantex molded PVC junction boxes (Home Depot).
# Builds both R5133710 (6x6x4) and R5133705 (4x4x2) in one document.
# Dims from Cantex sell sheet (A-K, cover A-D). Holes we drill are
# parametric sketches. Re-running wipes manual edits.
# F7 is inline. T92 flange sits on the floor, QC on top.
# ASCII only (FreeCAD exec encoding).

import math
import os

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher

OUT_DIR = "/Users/sfeldma/work/ih-53-ev/ac enclosure"
DOC_NAME = "ACEnclosure"
IN = 25.4

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

RAC_PCB_L = 40.0
RAC_PCB_W = 30.0
RAC_PCB_T = 1.6
RAC_HOLE_DX = 32.0
RAC_HOLE_DY = 22.0
RAC_HOLE = 3.2
RAC_L = 33.70
RAC_W = 22.20
RAC_H = 17.75
PE_HOLE = 6.6

PG21 = 28.3
PG16 = 22.5
PG11 = 18.6
COVER_SCREW = 4.5
COVER_LIFT = 30.0
GASKET_T = 0.125 * IN

COLOR_PVC = (0.58, 0.60, 0.62)
COLOR_LID = (0.52, 0.54, 0.56)
COLOR_GASKET = (0.10, 0.10, 0.10)
COLOR_T92 = (0.12, 0.12, 0.14)
COLOR_RAC = (0.18, 0.22, 0.48)
COLOR_PCB = (0.12, 0.42, 0.18)
COLOR_GLAND = (0.18, 0.18, 0.20)
COLOR_SS = (0.78, 0.78, 0.80)


class Spec(object):
    pass


def cantex_box(
    tag,
    pn,
    trade,
    inner_l_in,
    inner_w_in,
    inner_h_in,
    outer_l_in,
    outer_w_in,
    mount_c_in,
    t_floor_in,
    ear_hole_r_in,
    cover_l_in,
    cover_w_in,
    cover_t_in,
    ear_along_in,
    cover_inset,
    ox,
    oy,
    cover_ox,
    t92_cy,
    rac_cx,
    rac_cy,
    pe_x,
    pe_y,
    in_z,
    out_dj_y,
    out_z,
    step_box,
    step_lid,
    step_asm,
    k_note,
):
    s = Spec()
    s.tag = tag
    s.pn = pn
    s.trade = trade
    s.ss = "Dim" + tag
    s.inner_l = inner_l_in * IN
    s.inner_w = inner_w_in * IN
    s.inner_h = inner_h_in * IN
    s.outer_l = outer_l_in * IN
    s.outer_w = outer_w_in * IN
    s.t = (s.outer_l - s.inner_l) / 2.0
    s.t_floor = t_floor_in * IN
    s.mount_c = mount_c_in * IN
    s.ear_proj = (s.mount_c - s.outer_l) / 2.0
    s.ear_along = ear_along_in * IN
    s.ear_hole_r = ear_hole_r_in * IN
    s.cover_l = cover_l_in * IN
    s.cover_w = cover_w_in * IN
    s.cover_t = cover_t_in * IN
    s.cover_inset = cover_inset
    s.cover_x0 = s.inner_l / 2.0 - s.cover_l / 2.0
    s.cover_y0 = s.inner_w / 2.0 - s.cover_w / 2.0
    s.ox = ox
    s.oy = oy
    s.cover_ox = cover_ox
    s.t92_cx = s.inner_l / 2.0
    s.t92_cy = t92_cy
    s.rac_cx = rac_cx
    s.rac_cy = rac_cy
    s.pe_x = pe_x
    s.pe_y = pe_y
    s.in_y = s.inner_w / 2.0
    s.in_z = in_z
    s.out_dj_y = out_dj_y
    s.out_sig_y = s.inner_w - out_dj_y
    s.out_z = out_z
    s.step_box = step_box
    s.step_lid = step_lid
    s.step_asm = step_asm
    s.k_note = k_note
    return s


def spec_664():
    # Cantex 5133710 / R5133710 6x6x4
    return cantex_box(
        tag="664",
        pn="R5133710",
        trade="6 x 6 x 4 in",
        inner_l_in=6.000,
        inner_w_in=6.000,
        inner_h_in=4.000,
        outer_l_in=6.438,
        outer_w_in=6.438,
        mount_c_in=7.375,
        t_floor_in=0.220,
        ear_hole_r_in=0.188,
        cover_l_in=6.750,
        cover_w_in=6.750,
        cover_t_in=0.180,
        ear_along_in=0.85,
        cover_inset=12.0,
        ox=0.0,
        oy=0.0,
        cover_ox=250.0,
        t92_cy=95.0,
        rac_cx=40.0,
        rac_cy=32.0,
        pe_x=16.0,
        pe_y=62.0,
        in_z=40.0,
        out_dj_y=40.0,
        out_z=40.0,
        step_box="ac_box.step",
        step_lid="ac_lid.step",
        step_asm="ac_enclosure_assembly.step",
        k_note="sheet K 0.220 in",
    )


def spec_442():
    # Cantex 5133705 / R5133705 4x4x2. Packed layout; T92 and PG21 are tight.
    return cantex_box(
        tag="442",
        pn="R5133705",
        trade="4 x 4 x 2 in",
        inner_l_in=4.000,
        inner_w_in=4.000,
        inner_h_in=2.000,
        outer_l_in=4.400,
        outer_w_in=4.400,
        mount_c_in=5.375,
        t_floor_in=0.160,
        ear_hole_r_in=0.125,
        cover_l_in=4.375,
        cover_w_in=4.375,
        cover_t_in=0.240,
        ear_along_in=0.75,
        cover_inset=8.0,
        ox=0.0,
        oy=280.0,
        cover_ox=250.0,
        t92_cy=68.0,
        rac_cx=28.0,
        rac_cy=20.0,
        pe_x=88.0,
        pe_y=22.0,
        in_z=25.4,
        out_dj_y=32.0,
        out_z=25.4,
        step_box="ac_box_4x4x2.step",
        step_lid="ac_lid_4x4x2.step",
        step_asm="ac_enclosure_4x4x2_assembly.step",
        k_note="sheet K 0.160 in",
    )


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


def origin_plane(body, role):
    for feat in body.Origin.OriginFeatures:
        if feat.Role == role:
            return feat
    raise RuntimeError("no origin plane %s" % role)


def set_active_body(body):
    try:
        Gui.ActiveDocument.ActiveView.setActiveObject("pdbody", body)
    except Exception:
        pass


def ss_set(ss, row, name, value, note):
    ss.set("A" + str(row), name)
    ss.set("B" + str(row), value if isinstance(value, str) else str(value))
    ss.setAlias("B" + str(row), name)
    ss.set("C" + str(row), note)


def fill_spreadsheet(doc, spec):
    ss = doc.addObject("Spreadsheet::Sheet", spec.ss)
    ss.Label = spec.ss
    ss.set("A1", "name")
    ss.set("B1", "value")
    ss.set("C1", "note")
    r = 2
    rows = [
        ("BoxPN", spec.pn, "Cantex Home Depot"),
        ("Nema", "4X", "1/3/3S/4/4X/5/6/6P with gasket"),
        ("Material", "PVC", "molded rigid PVC"),
        ("Thickness", round(spec.t, 4), "wall (D-F)/2"),
        ("FloorT", round(spec.t_floor, 4), spec.k_note),
        ("InnerL", round(spec.inner_l, 4), "sheet F"),
        ("InnerW", round(spec.inner_w, 4), "sheet G"),
        ("InnerH", round(spec.inner_h, 4), "sheet A"),
        ("OuterL", round(spec.outer_l, 4), "sheet D"),
        ("OuterW", round(spec.outer_w, 4), "sheet E"),
        ("MountC", round(spec.mount_c, 4), "sheet C ears"),
        ("EarProj", round(spec.ear_proj, 4), "(C-D)/2"),
        ("EarAlong", round(spec.ear_along, 4), "ear along wall"),
        ("EarHoleR", round(spec.ear_hole_r, 4), "sheet J"),
        ("CoverL", round(spec.cover_l, 4), "cover C"),
        ("CoverW", round(spec.cover_w, 4), "cover D"),
        ("CoverT", round(spec.cover_t, 4), "cover A"),
        ("CoverX0", round(spec.cover_x0, 4), "cover min X"),
        ("CoverY0", round(spec.cover_y0, 4), "cover min Y"),
        ("GasketT", round(GASKET_T, 4), "neoprene 1/8 in"),
        ("T92Cx", round(spec.t92_cx, 4), "T92 center X"),
        ("T92Cy", spec.t92_cy, "T92 center Y"),
        ("T92Pitch", T92_PITCH, "flange hole c-c"),
        ("T92Hole", T92_HOLE, "T92 hole dia"),
        ("RacCx", spec.rac_cx, "RAC02 carrier center X"),
        ("RacCy", spec.rac_cy, "RAC02 carrier center Y"),
        ("RacHoleDx", RAC_HOLE_DX, "RAC02 hole spacing X"),
        ("RacHoleDy", RAC_HOLE_DY, "RAC02 hole spacing Y"),
        ("RacHole", RAC_HOLE, "RAC02 hole dia"),
        ("PeX", spec.pe_x, "PE stud X"),
        ("PeY", round(spec.pe_y, 4), "PE stud Y"),
        ("PeHole", PE_HOLE, "PE hole dia"),
        ("Pg21", PG21, "J1772 gland hole"),
        ("Pg16", PG16, "DJ7031 gland hole"),
        ("Pg11", PG11, "signal gland hole"),
        ("InY", round(spec.in_y, 4), "inlet gland Y"),
        ("InZ", round(spec.in_z, 4), "inlet gland Z"),
        ("OutDjY", spec.out_dj_y, "DJ7031 gland Y"),
        ("OutSigY", round(spec.out_sig_y, 4), "signal gland Y"),
        ("OutZ", round(spec.out_z, 4), "outlet gland Z"),
        ("CoverScrew", COVER_SCREW, "cover screw dia"),
        ("CoverInset", spec.cover_inset, "from cover edge"),
    ]
    for name, val, note in rows:
        ss_set(ss, r, name, val, note)
        r += 1
    derived = [
        ("T92X1", "=T92Cx - T92Pitch/2", "T92 hole A"),
        ("T92X2", "=T92Cx + T92Pitch/2", "T92 hole B"),
        ("RacX1", "=RacCx - RacHoleDx/2", ""),
        ("RacX2", "=RacCx + RacHoleDx/2", ""),
        ("RacY1", "=RacCy - RacHoleDy/2", ""),
        ("RacY2", "=RacCy + RacHoleDy/2", ""),
        ("EarHoleX1", "=-Thickness - EarProj/2", "SW/NW ear hole X"),
        ("EarHoleX2", "=InnerL + Thickness + EarProj/2", "SE/NE ear hole X"),
        ("EarHoleY1", "=-Thickness - EarProj/2", "SW/SE ear hole Y"),
        ("EarHoleY2", "=InnerW + Thickness + EarProj/2", "NW/NE ear hole Y"),
        ("CoverX2", "=CoverX0 + CoverL - CoverInset", ""),
        ("CoverY2", "=CoverY0 + CoverW - CoverInset", ""),
    ]
    for name, val, note in derived:
        ss_set(ss, r, name, val, note)
        r += 1
    doc.recompute()
    return ss


def e(spec, name):
    return spec.ss + "." + name


def add_rect(sk, x0, y0, x1, y1, prefix, x0e=None, y0e=None, xe=None, ye=None):
    v = [
        App.Vector(x0, y0, 0),
        App.Vector(x1, y0, 0),
        App.Vector(x1, y1, 0),
        App.Vector(x0, y1, 0),
    ]
    g0 = len(sk.Geometry)
    for i in range(4):
        sk.addGeometry(Part.LineSegment(v[i], v[(i + 1) % 4]), False)
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint("Coincident", g0 + i, 2, g0 + (i + 1) % 4, 1))
    sk.addConstraint(Sketcher.Constraint("Horizontal", g0))
    sk.addConstraint(Sketcher.Constraint("Horizontal", g0 + 2))
    sk.addConstraint(Sketcher.Constraint("Vertical", g0 + 1))
    sk.addConstraint(Sketcher.Constraint("Vertical", g0 + 3))
    cx = sk.addConstraint(Sketcher.Constraint("DistanceX", g0, 1, g0, 2, x1 - x0))
    cy = sk.addConstraint(Sketcher.Constraint("DistanceY", g0 + 1, 1, g0 + 1, 2, y1 - y0))
    sk.renameConstraint(cx, prefix + "L")
    sk.renameConstraint(cy, prefix + "W")
    if xe:
        sk.setExpression("Constraints.%sL" % prefix, xe)
    if ye:
        sk.setExpression("Constraints.%sW" % prefix, ye)
    ox = sk.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, g0, 1, x0))
    oy = sk.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, g0, 1, y0))
    sk.renameConstraint(ox, prefix + "X")
    sk.renameConstraint(oy, prefix + "Y")
    if x0e:
        sk.setExpression("Constraints.%sX" % prefix, x0e)
    if y0e:
        sk.setExpression("Constraints.%sY" % prefix, y0e)
    return g0


def add_circle(sk, x, y, r, name, x_expr=None, y_expr=None, r_expr=None):
    g = sk.addGeometry(Part.Circle(App.Vector(x, y, 0), App.Vector(0, 0, 1), r), False)
    cr = sk.addConstraint(Sketcher.Constraint("Radius", g, r))
    sk.renameConstraint(cr, name + "_R")
    cx = sk.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, g, 3, x))
    sk.renameConstraint(cx, name + "_X")
    cy = sk.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, g, 3, y))
    sk.renameConstraint(cy, name + "_Y")
    if r_expr:
        sk.setExpression("Constraints.%s_R" % name, r_expr)
    if x_expr:
        sk.setExpression("Constraints.%s_X" % name, x_expr)
    if y_expr:
        sk.setExpression("Constraints.%s_Y" % name, y_expr)
    return g


def add_sketch_on(body, name, support):
    sk = body.newObject("Sketcher::SketchObject", name)
    sk.AttachmentSupport = [(support, "")]
    sk.MapMode = "FlatFace"
    return sk


def add_pocket(body, name, sketch, length, reversed_):
    pkt = body.newObject("PartDesign::Pocket", name)
    pkt.Profile = sketch
    pkt.Type = 0
    pkt.Length = length
    pkt.Reversed = reversed_
    if sketch.ViewObject:
        sketch.ViewObject.Visibility = False
    return pkt


def flip_if_no_hole(doc, body, pocket, point):
    doc.recompute()
    p = App.Vector(*point)
    if not body.Shape.isInside(p, 0.15, True):
        return
    pocket.Reversed = not pocket.Reversed
    doc.recompute()
    still = body.Shape.isInside(p, 0.15, True)
    print(
        pocket.Name,
        "reversed",
        pocket.Reversed,
        "HOLE" if not still else "STILL SOLID",
        "at",
        [round(c, 2) for c in point],
    )


def dummy_t92(spec):
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
    for x in (-T92_PITCH / 2.0, T92_PITCH / 2.0):
        flange = flange.cut(
            Part.makeCylinder(T92_HOLE / 2.0, T92_FLANGE_T + 2.0, App.Vector(x, 0, -1), App.Vector(0, 0, 1))
        )
    cover = body.fuse(flange)
    tabs = []
    for x in (-18.0, -6.0, 6.0, 18.0):
        for y in (-12.7, 12.7):
            tabs.append(
                Part.makeBox(
                    T92_TAB_W,
                    T92_TAB_T,
                    T92_TAB_H,
                    App.Vector(x - T92_TAB_W / 2.0, y - T92_TAB_T / 2.0, T92_BODY_H),
                )
            )
    qc = tabs[0]
    for t in tabs[1:]:
        qc = qc.fuse(t)
    cover.translate(App.Vector(spec.ox + spec.t92_cx, spec.oy + spec.t92_cy, 0.0))
    qc.translate(App.Vector(spec.ox + spec.t92_cx, spec.oy + spec.t92_cy, 0.0))
    return cover, qc


def dummy_rac02(spec):
    pcb = Part.makeBox(
        RAC_PCB_L,
        RAC_PCB_W,
        RAC_PCB_T,
        App.Vector(spec.ox + spec.rac_cx - RAC_PCB_L / 2.0, spec.oy + spec.rac_cy - RAC_PCB_W / 2.0, 0.0),
    )
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            pcb = pcb.cut(
                Part.makeCylinder(
                    RAC_HOLE / 2.0,
                    RAC_PCB_T + 2.0,
                    App.Vector(
                        spec.ox + spec.rac_cx + sx * RAC_HOLE_DX / 2.0,
                        spec.oy + spec.rac_cy + sy * RAC_HOLE_DY / 2.0,
                        -1.0,
                    ),
                    App.Vector(0, 0, 1),
                )
            )
    body = Part.makeBox(
        RAC_L,
        RAC_W,
        RAC_H,
        App.Vector(spec.ox + spec.rac_cx - RAC_L / 2.0, spec.oy + spec.rac_cy - RAC_W / 2.0, RAC_PCB_T),
    )
    return pcb, body


def dummy_gland(spec, hole_d, y, z, x_face, inward):
    hex_af = hole_d + 6.0
    thread_l = spec.t + 6.0
    hex_h = 6.0
    y = spec.oy + y
    x_face = spec.ox + x_face
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


def dummy_pe_stud(spec):
    x = spec.ox + spec.pe_x
    y = spec.oy + spec.pe_y
    stud = Part.makeCylinder(3.0, 16.0, App.Vector(x, y, -2.0))
    wash = Part.makeCylinder(8.0, 1.2, App.Vector(x, y, 0.0))
    nut = hex_prism(10.0, 5.0)
    nut.translate(App.Vector(x, y, 1.2))
    return stud.fuse(wash).fuse(nut)


def dummy_gasket(spec):
    outer = Part.makeBox(
        spec.cover_l,
        spec.cover_w,
        GASKET_T,
        App.Vector(spec.ox + spec.cover_x0, spec.oy + spec.cover_y0, spec.inner_h),
    )
    inner = Part.makeBox(
        spec.inner_l - 2.0,
        spec.inner_w - 2.0,
        GASKET_T + 2.0,
        App.Vector(spec.ox + 1.0, spec.oy + 1.0, spec.inner_h - 1.0),
    )
    return outer.cut(inner)


def add_label(doc, name, text, pos):
    a = doc.addObject("App::Annotation", name)
    a.LabelText = text
    a.Position = App.Vector(*pos)
    vo = a.ViewObject
    if vo:
        vo.FontSize = 12
        vo.TextColor = (1.0, 1.0, 1.0)
    return a


def gp(spec, x, y, z):
    return (spec.ox + x, spec.oy + y, z)


def build_box(doc, spec):
    body = doc.addObject("PartDesign::Body", "Body_Box_" + spec.tag)
    body.Label = "Cantex_" + spec.tag
    body.Placement = App.Placement(App.Vector(spec.ox, spec.oy, 0), App.Rotation())
    set_active_body(body)
    xy = origin_plane(body, "XY_Plane")
    ss = spec.ss

    sko = add_sketch_on(body, "Sketch_Outer_" + spec.tag, xy)
    add_rect(
        sko,
        -spec.t,
        -spec.t,
        spec.inner_l + spec.t,
        spec.inner_w + spec.t,
        "Out",
        "-" + e(spec, "Thickness"),
        "-" + e(spec, "Thickness"),
        e(spec, "OuterL"),
        e(spec, "OuterW"),
    )
    pad_w = body.newObject("PartDesign::Pad", "Pad_Walls_" + spec.tag)
    pad_w.Profile = sko
    pad_w.Length = spec.inner_h
    pad_w.setExpression("Length", e(spec, "InnerH"))
    if sko.ViewObject:
        sko.ViewObject.Visibility = False
    doc.recompute()

    skf = add_sketch_on(body, "Sketch_Floor_" + spec.tag, xy)
    add_rect(
        skf,
        -spec.t,
        -spec.t,
        spec.inner_l + spec.t,
        spec.inner_w + spec.t,
        "Fl",
        "-" + e(spec, "Thickness"),
        "-" + e(spec, "Thickness"),
        e(spec, "OuterL"),
        e(spec, "OuterW"),
    )
    pad_f = body.newObject("PartDesign::Pad", "Pad_Floor_" + spec.tag)
    pad_f.Profile = skf
    pad_f.Length = spec.t_floor
    pad_f.Reversed = True
    pad_f.setExpression("Length", e(spec, "FloorT"))
    if skf.ViewObject:
        skf.ViewObject.Visibility = False
    doc.recompute()

    ske = add_sketch_on(body, "Sketch_Ears_" + spec.tag, xy)
    along = spec.ear_proj + spec.ear_along
    add_rect(
        ske,
        -spec.t - spec.ear_proj,
        -spec.t - spec.ear_proj,
        -spec.t - spec.ear_proj + along,
        -spec.t - spec.ear_proj + along,
        "SW",
        "-" + e(spec, "Thickness") + " - " + e(spec, "EarProj"),
        "-" + e(spec, "Thickness") + " - " + e(spec, "EarProj"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
    )
    add_rect(
        ske,
        spec.inner_l + spec.t - spec.ear_along,
        -spec.t - spec.ear_proj,
        spec.inner_l + spec.t + spec.ear_proj,
        -spec.t - spec.ear_proj + along,
        "SE",
        e(spec, "InnerL") + " + " + e(spec, "Thickness") + " - " + e(spec, "EarAlong"),
        "-" + e(spec, "Thickness") + " - " + e(spec, "EarProj"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
    )
    add_rect(
        ske,
        -spec.t - spec.ear_proj,
        spec.inner_w + spec.t - spec.ear_along,
        -spec.t - spec.ear_proj + along,
        spec.inner_w + spec.t + spec.ear_proj,
        "NW",
        "-" + e(spec, "Thickness") + " - " + e(spec, "EarProj"),
        e(spec, "InnerW") + " + " + e(spec, "Thickness") + " - " + e(spec, "EarAlong"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
    )
    add_rect(
        ske,
        spec.inner_l + spec.t - spec.ear_along,
        spec.inner_w + spec.t - spec.ear_along,
        spec.inner_l + spec.t + spec.ear_proj,
        spec.inner_w + spec.t + spec.ear_proj,
        "NE",
        e(spec, "InnerL") + " + " + e(spec, "Thickness") + " - " + e(spec, "EarAlong"),
        e(spec, "InnerW") + " + " + e(spec, "Thickness") + " - " + e(spec, "EarAlong"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
        e(spec, "EarProj") + " + " + e(spec, "EarAlong"),
    )
    pad_e = body.newObject("PartDesign::Pad", "Pad_Ears_" + spec.tag)
    pad_e.Profile = ske
    pad_e.Length = spec.t_floor
    pad_e.Reversed = True
    pad_e.setExpression("Length", e(spec, "FloorT"))
    if ske.ViewObject:
        ske.ViewObject.Visibility = False
    doc.recompute()

    skc = add_sketch_on(body, "Sketch_Cavity_" + spec.tag, xy)
    add_rect(skc, 0, 0, spec.inner_l, spec.inner_w, "Cv", "0", "0", e(spec, "InnerL"), e(spec, "InnerW"))
    pkt_c = add_pocket(body, "Pocket_Cavity_" + spec.tag, skc, spec.inner_h, False)
    pkt_c.setExpression("Length", e(spec, "InnerH"))
    doc.recompute()
    cavity_pt = gp(spec, spec.inner_l / 2.0, spec.inner_w / 2.0, spec.inner_h / 2.0)
    if body.Shape.isInside(App.Vector(*cavity_pt), 0.15, True):
        pkt_c.Reversed = not pkt_c.Reversed
        doc.recompute()
    print(
        spec.tag,
        "cavity open",
        not body.Shape.isInside(App.Vector(*cavity_pt), 0.15, True),
        "floor solid",
        body.Shape.isInside(App.Vector(*gp(spec, spec.inner_l / 2.0, spec.inner_w / 2.0, -spec.t_floor / 2.0)), 0.15, True),
        "wall solid",
        body.Shape.isInside(App.Vector(*gp(spec, -spec.t / 2.0, spec.inner_w / 2.0, spec.inner_h / 2.0)), 0.15, True),
    )

    skh = add_sketch_on(body, "Sketch_FloorHoles_" + spec.tag, xy)
    holes = [
        ("T92A", spec.t92_cx - T92_PITCH / 2.0, spec.t92_cy, T92_HOLE / 2.0, e(spec, "T92X1"), e(spec, "T92Cy"), e(spec, "T92Hole") + "/2"),
        ("T92B", spec.t92_cx + T92_PITCH / 2.0, spec.t92_cy, T92_HOLE / 2.0, e(spec, "T92X2"), e(spec, "T92Cy"), e(spec, "T92Hole") + "/2"),
        ("Rac11", spec.rac_cx - RAC_HOLE_DX / 2.0, spec.rac_cy - RAC_HOLE_DY / 2.0, RAC_HOLE / 2.0, e(spec, "RacX1"), e(spec, "RacY1"), e(spec, "RacHole") + "/2"),
        ("Rac21", spec.rac_cx + RAC_HOLE_DX / 2.0, spec.rac_cy - RAC_HOLE_DY / 2.0, RAC_HOLE / 2.0, e(spec, "RacX2"), e(spec, "RacY1"), e(spec, "RacHole") + "/2"),
        ("Rac12", spec.rac_cx - RAC_HOLE_DX / 2.0, spec.rac_cy + RAC_HOLE_DY / 2.0, RAC_HOLE / 2.0, e(spec, "RacX1"), e(spec, "RacY2"), e(spec, "RacHole") + "/2"),
        ("Rac22", spec.rac_cx + RAC_HOLE_DX / 2.0, spec.rac_cy + RAC_HOLE_DY / 2.0, RAC_HOLE / 2.0, e(spec, "RacX2"), e(spec, "RacY2"), e(spec, "RacHole") + "/2"),
        ("PE", spec.pe_x, spec.pe_y, PE_HOLE / 2.0, e(spec, "PeX"), e(spec, "PeY"), e(spec, "PeHole") + "/2"),
    ]
    for name, x, y, r, xe, ye, re in holes:
        add_circle(skh, x, y, r, name, xe, ye, re)
    pkt_f = add_pocket(body, "Pocket_FloorHoles_" + spec.tag, skh, 8.0, False)
    flip_if_no_hole(doc, body, pkt_f, gp(spec, spec.t92_cx - T92_PITCH / 2.0, spec.t92_cy, -spec.t_floor / 2.0))

    hx1 = -spec.t - spec.ear_proj / 2.0
    hy1 = -spec.t - spec.ear_proj / 2.0
    hx2 = spec.inner_l + spec.t + spec.ear_proj / 2.0
    hy2 = spec.inner_w + spec.t + spec.ear_proj / 2.0
    skeh = add_sketch_on(body, "Sketch_EarHoles_" + spec.tag, xy)
    add_circle(skeh, hx1, hy1, spec.ear_hole_r, "E11", e(spec, "EarHoleX1"), e(spec, "EarHoleY1"), e(spec, "EarHoleR"))
    add_circle(skeh, hx2, hy1, spec.ear_hole_r, "E21", e(spec, "EarHoleX2"), e(spec, "EarHoleY1"), e(spec, "EarHoleR"))
    add_circle(skeh, hx1, hy2, spec.ear_hole_r, "E12", e(spec, "EarHoleX1"), e(spec, "EarHoleY2"), e(spec, "EarHoleR"))
    add_circle(skeh, hx2, hy2, spec.ear_hole_r, "E22", e(spec, "EarHoleX2"), e(spec, "EarHoleY2"), e(spec, "EarHoleR"))
    pkt_e = add_pocket(body, "Pocket_EarHoles_" + spec.tag, skeh, 8.0, False)
    flip_if_no_hole(doc, body, pkt_e, gp(spec, hx1, hy1, -spec.t_floor / 2.0))

    ski = add_sketch_on(body, "Sketch_Inlet_" + spec.tag, origin_plane(body, "YZ_Plane"))
    ski.AttachmentOffset = App.Placement(App.Vector(0, 0, -spec.t), App.Rotation())
    ski.setExpression("AttachmentOffset.Base.z", "-" + e(spec, "Thickness"))
    add_circle(ski, spec.in_y, spec.in_z, PG21 / 2.0, "PG21", e(spec, "InY"), e(spec, "InZ"), e(spec, "Pg21") + "/2")
    pkt_i = add_pocket(body, "Pocket_Inlet_" + spec.tag, ski, 12.0, False)
    flip_if_no_hole(doc, body, pkt_i, gp(spec, -spec.t / 2.0, spec.in_y, spec.in_z))

    skout = add_sketch_on(body, "Sketch_Outlet_" + spec.tag, origin_plane(body, "YZ_Plane"))
    skout.AttachmentOffset = App.Placement(App.Vector(0, 0, spec.inner_l + spec.t), App.Rotation())
    skout.setExpression("AttachmentOffset.Base.z", e(spec, "InnerL") + " + " + e(spec, "Thickness"))
    add_circle(skout, spec.out_dj_y, spec.out_z, PG16 / 2.0, "PG16", e(spec, "OutDjY"), e(spec, "OutZ"), e(spec, "Pg16") + "/2")
    add_circle(skout, spec.out_sig_y, spec.out_z, PG11 / 2.0, "PG11", e(spec, "OutSigY"), e(spec, "OutZ"), e(spec, "Pg11") + "/2")
    pkt_o = add_pocket(body, "Pocket_Outlet_" + spec.tag, skout, 12.0, True)
    flip_if_no_hole(doc, body, pkt_o, gp(spec, spec.inner_l + spec.t / 2.0, spec.out_dj_y, spec.out_z))

    if body.ViewObject:
        body.ViewObject.ShapeColor = COLOR_PVC
    return body


def build_cover(doc, spec):
    body = doc.addObject("PartDesign::Body", "Body_Cover_" + spec.tag)
    body.Label = "Cantex_Cover_" + spec.tag
    body.Placement = App.Placement(App.Vector(spec.cover_ox, spec.oy, 0), App.Rotation())
    set_active_body(body)
    xy = origin_plane(body, "XY_Plane")
    sk = add_sketch_on(body, "Sketch_Cover_" + spec.tag, xy)
    add_rect(
        sk,
        spec.cover_x0,
        spec.cover_y0,
        spec.cover_x0 + spec.cover_l,
        spec.cover_y0 + spec.cover_w,
        "Cv",
        e(spec, "CoverX0"),
        e(spec, "CoverY0"),
        e(spec, "CoverL"),
        e(spec, "CoverW"),
    )
    pad = body.newObject("PartDesign::Pad", "Pad_Cover_" + spec.tag)
    pad.Profile = sk
    pad.Length = spec.cover_t
    pad.setExpression("Length", e(spec, "CoverT"))
    if sk.ViewObject:
        sk.ViewObject.Visibility = False
    doc.recompute()

    sks = add_sketch_on(body, "Sketch_CoverScrews_" + spec.tag, xy)
    inset = spec.cover_inset
    r = COVER_SCREW / 2.0
    add_circle(
        sks,
        spec.cover_x0 + inset,
        spec.cover_y0 + inset,
        r,
        "C11",
        e(spec, "CoverX0") + " + " + e(spec, "CoverInset"),
        e(spec, "CoverY0") + " + " + e(spec, "CoverInset"),
        e(spec, "CoverScrew") + "/2",
    )
    add_circle(
        sks,
        spec.cover_x0 + spec.cover_l - inset,
        spec.cover_y0 + inset,
        r,
        "C21",
        e(spec, "CoverX2"),
        e(spec, "CoverY0") + " + " + e(spec, "CoverInset"),
        e(spec, "CoverScrew") + "/2",
    )
    add_circle(
        sks,
        spec.cover_x0 + inset,
        spec.cover_y0 + spec.cover_w - inset,
        r,
        "C12",
        e(spec, "CoverX0") + " + " + e(spec, "CoverInset"),
        e(spec, "CoverY2"),
        e(spec, "CoverScrew") + "/2",
    )
    add_circle(
        sks,
        spec.cover_x0 + spec.cover_l - inset,
        spec.cover_y0 + spec.cover_w - inset,
        r,
        "C22",
        e(spec, "CoverX2"),
        e(spec, "CoverY2"),
        e(spec, "CoverScrew") + "/2",
    )
    pkt = add_pocket(body, "Pocket_CoverScrews_" + spec.tag, sks, 8.0, False)
    flip_if_no_hole(
        doc,
        body,
        pkt,
        (spec.cover_ox + spec.cover_x0 + inset, spec.oy + spec.cover_y0 + inset, spec.cover_t / 2.0),
    )

    if body.ViewObject:
        body.ViewObject.ShapeColor = COLOR_LID
    return body


def export_steps(spec, box, cover, assembly):
    os.makedirs(OUT_DIR, exist_ok=True)
    box.exportStep(os.path.join(OUT_DIR, spec.step_box))
    cover.exportStep(os.path.join(OUT_DIR, spec.step_lid))
    assembly.exportStep(os.path.join(OUT_DIR, spec.step_asm))


def print_fit(spec):
    qc_clear = spec.inner_h - T92_OVERALL_H
    pg21_edge = spec.in_z - PG21 / 2.0
    print(
        spec.tag,
        "inner mm",
        round(spec.inner_l, 2),
        round(spec.inner_w, 2),
        round(spec.inner_h, 2),
        "T92 QC clearance mm",
        round(qc_clear, 2),
        "PG21 floor clearance mm",
        round(pg21_edge, 2),
    )


def build_one(doc, spec):
    print_fit(spec)
    box = build_box(doc, spec)
    cover = build_cover(doc, spec)
    t92, t92_qc = dummy_t92(spec)
    rac_pcb, rac_body = dummy_rac02(spec)
    g_in = dummy_gland(spec, PG21, spec.in_y, spec.in_z, 0.0, 1)
    g_dj = dummy_gland(spec, PG16, spec.out_dj_y, spec.out_z, spec.inner_l, -1)
    g_sig = dummy_gland(spec, PG11, spec.out_sig_y, spec.out_z, spec.inner_l, -1)
    pe = dummy_pe_stud(spec)
    gasket = dummy_gasket(spec)

    grp = doc.addObject("App::DocumentObjectGroup", "Ref_" + spec.tag)
    grp.Label = "ReferenceParts_" + spec.tag
    objs = [
        add_shape(doc, "T92_" + spec.tag, t92, COLOR_T92),
        add_shape(doc, "T92_QC_" + spec.tag, t92_qc, COLOR_SS),
        add_shape(doc, "RAC02_PCB_" + spec.tag, rac_pcb, COLOR_PCB),
        add_shape(doc, "RAC02_" + spec.tag, rac_body, COLOR_RAC),
        add_shape(doc, "Gland_J1772_" + spec.tag, g_in, COLOR_GLAND),
        add_shape(doc, "Gland_DJ7031_" + spec.tag, g_dj, COLOR_GLAND),
        add_shape(doc, "Gland_Signal_" + spec.tag, g_sig, COLOR_GLAND),
        add_shape(doc, "PE_Stud_" + spec.tag, pe, COLOR_SS),
        add_shape(doc, "Gasket_" + spec.tag, gasket, COLOR_GASKET, 40),
    ]
    for o in objs:
        grp.addObject(o)

    add_label(
        doc,
        "Label_Box_" + spec.tag,
        ["Cantex " + spec.pn, spec.trade + " PVC NEMA 4X"],
        (spec.ox, spec.oy - 40, spec.inner_h + 10),
    )
    add_label(doc, "Label_IN_" + spec.tag, ["J1772 IN  PG21"], (spec.ox - 50, spec.oy + spec.in_y - 8, spec.in_z + 16))
    add_label(doc, "Label_DJ_" + spec.tag, ["DJ7031 to TSM2500"], (spec.ox + spec.inner_l + 10, spec.oy + spec.out_dj_y - 8, spec.out_z + 14))
    add_label(doc, "Label_SIG_" + spec.tag, ["CP/PP + CHARGE"], (spec.ox + spec.inner_l + 10, spec.oy + spec.out_sig_y - 8, spec.out_z + 14))
    add_label(doc, "Label_T92_" + spec.tag, ["T92P11D22-12"], (spec.ox + spec.t92_cx - 30, spec.oy + spec.t92_cy + 22, T92_OVERALL_H + 6))
    add_label(doc, "Label_RAC_" + spec.tag, ["RAC02-12SE/277"], (spec.ox + spec.rac_cx - 16, spec.oy + spec.rac_cy - 22, 20))

    doc.recompute()
    cover_placed = cover.Shape.copy()
    cover_placed.translate(
        App.Vector(spec.ox - spec.cover_ox, 0, spec.inner_h + GASKET_T + COVER_LIFT)
    )
    assembly = Part.makeCompound(
        [box.Shape, cover_placed, gasket, t92, t92_qc, rac_pcb, rac_body, g_in, g_dj, g_sig, pe]
    )
    export_steps(spec, box.Shape, cover.Shape, assembly)
    bb = box.Shape.BoundBox
    print(
        spec.tag,
        "BB",
        round(bb.XMin, 2),
        round(bb.XMax, 2),
        round(bb.YMin, 2),
        round(bb.YMax, 2),
        round(bb.ZMin, 2),
        round(bb.ZMax, 2),
    )
    print(
        spec.tag,
        "holes",
        "T92",
        not box.Shape.isInside(App.Vector(*gp(spec, spec.t92_cx - T92_PITCH / 2.0, spec.t92_cy, -spec.t_floor / 2.0)), 0.1, True),
        "PG21",
        not box.Shape.isInside(App.Vector(*gp(spec, -spec.t / 2.0, spec.in_y, spec.in_z)), 0.1, True),
        "PG16",
        not box.Shape.isInside(App.Vector(*gp(spec, spec.inner_l + spec.t / 2.0, spec.out_dj_y, spec.out_z)), 0.1, True),
        "PG11",
        not box.Shape.isInside(App.Vector(*gp(spec, spec.inner_l + spec.t / 2.0, spec.out_sig_y, spec.out_z)), 0.1, True),
    )
    return box


def main():
    for d in list(App.listDocuments().keys()):
        if d == DOC_NAME or d.startswith("SMTest") or App.getDocument(d).Label == DOC_NAME:
            App.closeDocument(d)

    doc = App.newDocument(DOC_NAME)
    Gui.setActiveDocument(doc.Name)
    boxes = (spec_664(), spec_442())
    for spec in boxes:
        fill_spreadsheet(doc, spec)
    last = None
    for spec in boxes:
        last = build_one(doc, spec)
    path = os.path.join(OUT_DIR, "ac enclosure.FCStd")
    doc.saveAs(path)
    print("Saved", path)
    if last is not None:
        set_active_body(last)
    return doc


doc = main()
