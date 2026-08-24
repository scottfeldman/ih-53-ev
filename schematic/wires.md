# IH-53 EV wiring list

Physical wires taken from `IH53EV.kicad_sch`. Size/type is the schematic text on that run when present. **Color prefers the component wiring-harness pigtail** and is carried through splices; schematic stroke color is ignored when a harness color exists.

Inline disconnects (Anderson, DJ70xx, Weather Pack, Deutsch, USB) are drawn as two-sided symbols. Each side is a separate cable termination; mating the housings is not a wire.

**Orion BMS 2 Main I/O** on this vehicle is the **CWHMIO 18 AWG** harness (Sumitomo 8240-4892 crimps), not 22 AWG.

## Color rules

1. If a factory harness / pigtail has a color, that color is the color of the whole run, including splices and bulkhead connectors.
2. When two pigtails meet (for example TSM2500 CAN into Orion CAN1), **keep the Orion (or other “bus owner”) color on the trunk**; the other pigtail keeps its factory color only up to the splice.
3. Traction **2/0 DLO** is **orange** (EV HV jacket). Polarity is **red** (+) / **black** (−) adhesive heatshrink at each lug — not a red/black jacket.
4. 12 V **GXL** (schematic: GLX) battery and DC-DC 12 V feeds have no colored pigtail: **red = +**, **black = −**.
5. Vehicle **DCIS pack HV** (10 AWG / 18 AWG HV from the 3-way toward the pack) is **red = +**, **black = −**. Factory DCIS pigtail stays **yellow / gray** only up to `dj70310-6.3-1`.
6. Orion CWHMIO colors: pin 1 (Always_On) = **green**, pin 2 (READY) = solid **blue**, and pin 3 (CHARGE) = solid **red** (2 and 3 from [Orion’s CANdapter troubleshooting page](https://www.orionbms.com/troubleshooting/problems-connecting-bms-unit-pc-software/); pin 1 from this harness). Pins 6, 7, 13, 14 from this vehicle’s harness. Remaining pins still **verify on harness card**.

## Wire key (from schematic)

| Code | Meaning |
| --- | --- |
| AWG | conductor size |
| TXL | 12 V / 48 V primary (18 AWG on this sheet) |
| GXL | 12 V 10 AWG (schematic label **GLX**) |
| HV | 600–1000 V DC pack (silicone / EV) |
| AC | J1772 / T92 mains (600 V) |
| 300VAC | RAC02 tap only (schematic may say 18AWG AC — same run) |
| DLO | traction / pack 2/0 |

## Harness color map (factory pigtails)

| Device | Pin / lead | Color | Size | Source |
| --- | --- | --- | --- | --- |
| Orion CWHMIO | 1 Always_On_Power | **green** | 18 AWG | this harness |
| Orion CWHMIO | 2 READY_Power | **blue** | 18 AWG | [Orion troubleshooting](https://www.orionbms.com/troubleshooting/problems-connecting-bms-unit-pc-software/) |
| Orion CWHMIO | 3 CHARGE_Power | **red** | 18 AWG | same |
| Orion CWHMIO | 6 Charger_Safety | **red/white** | 18 AWG | this harness |
| Orion CWHMIO | 7 DISCHARGE_enable | **blue/white** | 18 AWG | this harness |
| Orion CWHMIO | 12 Ground | **black** (typical; verify) | 18 AWG | CWHMIO; ground convention |
| Orion CWHMIO | 13 J1772_Control_Pilot | **orange/white** | 18 AWG | this harness |
| Orion CWHMIO | 14 J1772_Proximity_Detect | **brown/white** | 18 AWG | this harness |
| Orion CWHMIO | 17 CAN1_Shield | drain / bare | shield | CWHMIO CAN1 STP |
| Orion CWHMIO | 18 CAN1_H | CAN1 pair (gray jacket STP; inner *verify*) | 18 AWG pair, 12 ft | [purchasing guide](https://www.orionbms.com/manuals/pdf/orionbms2_purchasing_guide.pdf) |
| Orion CWHMIO | 19 CAN1_L | CAN1 pair (with pin 18) | 18 AWG pair, 12 ft | same |
| TSM2500 AC | L / N / PE | **brown** / **blue** / **green-yellow** | 2.5 mm² (~14 AWG) | [TSM2500 manual](https://www.thunderstruck-ev.com/images/companies/1/Chargers/ThunderStruck-TSM2500-ManualV1.09.pdf) |
| TSM2500 DC | + / − | **red** / **black** | 6 mm² (~10 AWG **HV**, not TXL) | same (SB50); pack voltage |
| TSM2500 CAN | H / L | **green/white** / **blue/white** | 0.5 mm² | same; [Orion TSM2500 note](https://www.orionbms.com/charger-integration/interfacing-tsm2500-chargers/) (splice onto Orion CAN1 colors) |
| DCIS output | + / − | **red** / **black** | 6.0 mm² (~10 AWG) | [DCIS schematic](https://www.fastandquiet.com/downloadable/600w-dc-dc-converter-isolated-dcis-schematic.PDF) |
| DCIS input | + / − | factory **yellow** / **gray**; vehicle **red** / **black** | 10 AWG **HV** (factory pigtail 1.5 mm²) | factory pigtail to 3-way; vehicle HV is red/black |
| DCIS key | Key_Switch_Control | **green** | 0.5 mm² | same |
| HyPer 9 encoder (not on this sheet) | K1-35 / 21 / 33 / 9 | red / yellow / green / black | 18 / 20 AWG | [HyPer manual](https://www.go-ev.com/PDFs/HyPer_System_User_Manual_RevA_1.pdf) |
| HyPer 9 K1 CAN, K1-24, K1-25, K1-26 | — | *verify on K1 print* (colors vary by kit) | 18–20 AWG | HyPer manual: identify by pin number |
| HyPer 9 B+ / B− | DC lugs | **orange** jacket; red / black HS | 2/0 DLO | EV orange; polarity by heatshrink |
| CANdapter USB | cable | black jacket (USB 2.0) | USB | CANdapter |

## Connector reference

| Device | Mating connector | Contacts / wire | Source |
| --- | --- | --- | --- |
| Orion BMS 2 Main I/O | TE 1376360-1 | **18 AWG** + Sumitomo 8240-4892 (this harness) | user; [Orion wiring manual](https://www.orionbms.com/manuals/pdf/orionbms2_wiring_manual.pdf) |
| Orion voltage taps (cell taps, not drawn as wires on this sheet) | TE 1318389-1 | 22 AWG + TE 1123343-2 (gold); group colors orange / red / yellow, grounds black | same |
| HyPer 9 X1 K1 | TE AMPSEAL 35-pin 776164-1, pins 770854-1 | typically 18–20 AWG | [HyPer System User Manual](https://www.go-ev.com/PDFs/HyPer_System_User_Manual_RevA_1.pdf) |
| HyPer 9 B+ / B− | inverter DC lugs | 2/0 DLO, ring terminal | schematic |
| TSM2500 AC input | DJ7031-4.8 (`DJ7031-4.8`; 4.8-11 / 4.8-21) | 2.5 mm² (~14 AWG) brown / blue / green-yellow | TSM2500 manual; schematic |
| TSM2500 DC output | Anderson SB50 (`AndersonSB50`) | 6 mm² (~10 AWG **HV**) red / black | same |
| TSM2500 CAN | charger CAN pair | 0.5 mm² green/white + blue/white | same |
| DCIS 600 W output | DJ7021-8-21 (`DJ7021-8-1`) | 6.0 mm² factory; vehicle **10 AWG GXL** red / black | DCIS schematic; schematic |
| DCIS 600 W input / enable | dj70310-6.3-11 (`dj70310-6.3-1`) | 10 AWG **HV** vehicle red / black (factory 1.5 mm² yellow / gray); 18 AWG **HV** / 0.5 mm² green key | this vehicle / DCIS schematic |
| CANdapter CAN | DE-9 (DB9) | twisted pair to pins 7 (CAN_H) and 2 (CAN_L) | [CANdapter manual](https://www.ewertenergy.com/products/candapter/downloads/candapter_manual.pdf) |
| CANdapter USB | USB-B on adapter | USB cable | CANdapter manual |
| Blue Sea 5032 buses | #10-32 stud | ring terminal | [Blue Sea 5032](https://www.bluesea.com/products/5032/ST_Blade_Split_Bus_Fuse_Block) |
| Blue Sea 5032 circuits | #8-32 screw | ring or spade | same |
| J1772 inlet | SAE J1772 socket | AC pins + CP / PP | schematic |
| Anderson 350 A / 600 V | SB350 housing | 2/0 contacts | schematic |
| Anderson SB50 | SB50 housing | 6–10 AWG contacts | TSM2500 DC only |
| DJ7021-8-21 | 2-way, 8.0 mm | DCIS 12 V output | schematic (included with DCIS) |
| dj70310-6.3-11 | 3-way, 6.3 mm | DCIS pack input / key | schematic (included with DCIS) |
| DJ7031-4.8 | 3-way, 4.8 mm | TSM2500 AC | schematic (included with TSM2500) |
| Delphi Weather Pack 4 | Weather Pack 4-way | 18 AWG (Orion colors carried through) | schematic |
| Deutsch DTM 3 | DTM 3-way | 16–22 AWG | schematic |
| BB CANOP isolator | terminal-block CAN / power | no factory pigtail color | Advantech BB-CANOP |
| HV terminal blocks | 5/16″ and 1/4″ studs | 2/0 lugs on 5/16″; smaller HV on 1/4″ | schematic |
| Gigavac GV200QA-1 | M8 HV terminals; coil X1/X2 | 2/0 lugs; coil from K1 harness | schematic |
| T92P11D22-12 | 0.250″ QC | 14 AWG AC; 18 AWG coil from Orion | TE T92 |
| T9AP1D52-12 | 0.250″ QC | 18 AWG where tied to Orion | TE T9A |
| G9EJ-1-E-UVD DC12 | 0.250″ QC | 18 AWG HV contacts (polarized 3+/4−); 18 AWG TXL coil | Omron G9EJ |
| Cole Hersee 24213 | stud contacts; QC coil | 10 AWG GXL contacts | schematic |
| MAXI 5006 | MAXI fuse holder lugs | 10 AWG GXL | schematic |
| A25X500-4 | bolted fuse | 2/0 DLO lugs | schematic |

---

## 1. Traction pack (2/0 DLO)

Tesla modules **BT2–BT6** in series. Inter-module runs are unlabeled next to the modules; 2/0 DLO labels sit on that pack string. Jacket is **orange** (EV HV). Mark every lug with **red** (+) or **black** (−) adhesive heatshrink.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| HV-01 | 2/0 DLO | orange, black HS | BT2 − | module − lug | TerminalBlock2 5/16″ | 5/16″ stud, ring lug |
| HV-02 | 2/0 DLO | orange, red HS | BT2 + | module + lug | BT3 − | module − lug |
| HV-03 | 2/0 DLO | orange, red HS | BT3 + | module + lug | BT4 − | module − lug |
| HV-04 | 2/0 DLO | orange, red HS | BT4 + | module + lug | BT5 − | module − lug |
| HV-05 | 2/0 DLO | orange, red HS | BT5 + | module + lug | BT6 − | module − lug |
| HV-06 | 2/0 DLO | orange, red HS | BT6 + | module + lug | F4 (A25X500-4) | bolted fuse pad |
| HV-07 | 2/0 DLO | orange, red HS | F4 | bolted fuse pad | SW1 (Kill Switch HVBD6AXR) | switch HV terminal |
| HV-08 | 2/0 DLO | orange, red HS | SW1 | switch HV terminal | TerminalBlock1 5/16″ | 5/16″ stud, ring lug |
| HV-09 | 2/0 DLO | orange, red HS | TerminalBlock1 5/16″ | 5/16″ stud, ring lug | Anderson350A600V1 right + | SB350 contact (2/0) |
| HV-10 | 2/0 DLO | orange, black HS | TerminalBlock2 5/16″ | 5/16″ stud, ring lug | Anderson350A600V1 right − | SB350 contact (2/0) |
| HV-11 | 2/0 DLO | orange, red HS | Anderson350A600V1 left + | SB350 contact (2/0) | TerminalBlock3 5/16″ (pack + bus) | 5/16″ stud, ring lug |
| HV-12 | 2/0 DLO | orange, red HS | Anderson350A600V1 left − | SB350 contact (2/0) | HyPer 9 **B+** | inverter B+ lug |
| HV-13 | 2/0 DLO | orange, black HS | HyPer 9 **B−** | inverter B− lug | G1 (GV200QA-1) **A2−** | Gigavac M8 HV terminal |
| HV-14 | 2/0 DLO | orange, red HS | G1 **A1+** | Gigavac M8 HV terminal | TerminalBlock3 5/16″ (pack + bus) | 5/16″ stud, ring lug |

SB350 left housing mates to right housing: pack + bus ↔ TB1, inverter B+ ↔ TB2−.

Cell taps on BT2–BT6 are **not** wired on this sheet. Orion tap harness is 22 AWG to TE 1318389-1 (orange / red / yellow groups, black grounds). Schematic notes **internally termination** at the modules.

---

## 2. Charger HV DC

TSM2500 DC is the included **Anderson SB50** (`AndersonSB50`). Mating is not a wire: left housing is the charger pigtail, right housing is the vehicle. Pigtail colors **red / black** carry through. Vehicle runs are **10 AWG HV** (labeled). Factory pigtail is 6 mm² (~10 AWG) unlabeled on the charger side of the SB50.

SB50 mates top-to-top: charger **+** (left top) → vehicle right top → 32 A 2-pole → TerminalBlock1 1/4″ (pack +). Charger **−** (left bottom) → vehicle right bottom → Circuit_Breaker3 → TerminalBlock2 1/4″ (pack −).

| ID | Size / type | Color | End A | A termination | End B | B termination | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CH-DC+ | 6 mm² charger pigtail | red | TSM2500 **DC_Output_+** | charger DC + | AndersonSB50 left top | SB50 contact | TSM2500 pigtail |
| CH-DC− | 6 mm² charger pigtail | black | TSM2500 **DC_Ouput_−** | charger DC − | AndersonSB50 left bottom | SB50 contact | TSM2500 pigtail |
| CH-DC+V | 10 AWG HV | red | AndersonSB50 right top | SB50 contact | 2Pole_1000V_DC_32Amp1 B | breaker HV terminal | carry TSM2500 red |
| CH-DC+2 | 10 AWG HV | red | 2Pole_1000V_DC_32Amp1 A | breaker HV terminal | TerminalBlock1 1/4″ | 1/4″ stud, ring lug | carry TSM2500 red |
| CH-DC−V | 10 AWG HV | black | AndersonSB50 right bottom | SB50 contact | Circuit_Breaker3 B | breaker HV terminal | carry TSM2500 black |
| CH-DC−2 | 10 AWG HV | black | Circuit_Breaker3 A | breaker HV terminal | TerminalBlock2 1/4″ | 1/4″ stud, ring lug | carry TSM2500 black |

---

## 3. DC-DC converter (pack → 12 V)

DCIS factory connectors are drawn: **dj70310-6.3-11** (`dj70310-6.3-1`) 3-way input/key, **DJ7021-8-21** (`DJ7021-8-1`) 2-way 12 V output. Mating is not a wire. Factory pigtail stays **yellow / gray / green** only to the 3-way. Vehicle pack HV from that connector is **red / black**. Key stays **green**. 12 V output is **red / black**.

Pack input vehicle runs are **10 AWG HV** (same cable as charger DC). Factory pigtail to the 3-way is 1.5 mm². Key is pack voltage (DCIS: “key switch control voltage is consistent with the input voltage”), so the vehicle key run and the K4 tap are **18 AWG HV**, not TXL. 12 V output vehicle runs are **10 AWG GXL** (labeled GLX). If 10 AWG HV will not enter the 6.3 mm contacts, splice a short 14–16 AWG tail into the housing.

dj70310 pin order top → bottom: Input+ / Input− / Key. DJ7021 pin order top → bottom: Output+ / Output−. Left = DCIS pigtail, right = vehicle on the 3-way; **right = DCIS pigtail, left = vehicle** on the 2-way (as drawn).

| ID | Size / type | Color | End A | A termination | End B | B termination | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DC-IN0+ | 1.5 mm² factory pigtail | yellow | DCIS **Input+** | DCIS 3-pin | dj70310-6.3-1 left top | 6.3 mm contact | DCIS yellow |
| DC-IN0− | 1.5 mm² factory pigtail | gray | DCIS **Input−** | DCIS 3-pin | dj70310-6.3-1 left mid | 6.3 mm contact | DCIS gray |
| DC-KEY0 | 0.5 mm² factory pigtail | green | DCIS **Key_Switch_Control** | DCIS 3-pin | dj70310-6.3-1 left bottom | 6.3 mm contact | DCIS green |
| DC-IN+ | 10 AWG HV | red | dj70310-6.3-1 right top | 6.3 mm contact | Circuit_Breaker4 A | breaker HV terminal | vehicle HV+ |
| DC-K4TAP | 18 AWG HV | red | splice on DC-IN+ | — | K4 pin 3 (+) | G9EJ #250 QC | pack + to key relay |
| DC-IN+2 | 10 AWG HV | red | Circuit_Breaker4 B | breaker HV terminal | TerminalBlock1 1/4″ | 1/4″ stud | vehicle HV+ |
| DC-IN− | 10 AWG HV | black | dj70310-6.3-1 right mid | 6.3 mm contact | 2Pole_1000V_DC_10Amp1 A | breaker HV terminal | vehicle HV− |
| DC-IN−2 | 10 AWG HV | black | 2Pole_1000V_DC_10Amp1 B | breaker HV terminal | TerminalBlock2 1/4″ | 1/4″ stud | vehicle HV− |
| DC-KEY | 18 AWG HV | green | dj70310-6.3-1 right bottom | 6.3 mm contact | K4 pin 4 (−) | G9EJ #250 QC | carry DCIS green |
| DC-OUT+ | 6.0 mm² factory pigtail | red | DCIS **Output+** | DCIS 2-pin | DJ7021-8-1 right top | 8.0 mm contact | DCIS red |
| DC-OUT− | 6.0 mm² factory pigtail | black | DCIS **Output−** | DCIS 2-pin | DJ7021-8-1 right bottom | 8.0 mm contact | DCIS black |

Precharge path from pack + into the inverter (no pigtail). Schematic unlabeled; **18 AWG HV** (T9A QC), **red**. Circuit_Breaker2 is **1-pole 1000 V DC 10 A**.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| PC-01 | 18 AWG HV (unlabeled) | red | TerminalBlock3 1/4″ | 1/4″ stud | Circuit_Breaker2 | breaker HV terminal |
| PC-02 | 18 AWG HV (unlabeled) | red | Circuit_Breaker2 | breaker HV terminal | K2 (T9AP1D52-12) pin 4 | T9A QC |
| PC-03 | 18 AWG HV (unlabeled) | red | K2 pin 3 | T9A QC | HyPer 9 **Precharge/Key_Switch_In** (K1-24) | AMPSEAL 776164-1 pin 24 |

K1-24 is the only HyPer 9 K1 pin that sees pack voltage on a non-isolated X1 (HyPer manual). If the K1 pigtail for pin 24 is a different color, use that K1 color instead of red from the splice to the AMPSEAL.

---

## 4. J1772 / charger AC

TSM2500 AC is the included **DJ7031-4.8** (`DJ7031-4.8`). Right housing is the charger pigtail (**brown / blue / green-yellow**); left is vehicle **14 AWG AC**. Those colors carry through the T92 to the J1772 inlet.

RAC02-12SE/277 is 2 W (≈47 mA at 115 VAC). Do **not** run 14 AWG AC to F7 / RAC02. Tap **18 AWG 300VAC** off the L1/L2 mains and fuse it at F7 (F5×20, 1 A / Recom T1A slow-blow).

DJ7031 pin order top → bottom: L / N / PE.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| AC-L1 | 14 AWG AC | brown | J1772 **L1** | J1772 inlet L1 | T92 pin 24 | 0.250″ QC |
| AC-L1-F7 | 18 AWG 300VAC | brown | splice on AC-L1 | — | F7 (F5×20, 1 A max) | fuse clip |
| AC-L1-RAC | 18 AWG 300VAC | brown | F7 | fuse clip | RAC02 **VAC_IN(L)** | RAC02 AC pin |
| AC-L2 | 14 AWG AC | blue | J1772 **L2/N** | J1772 inlet L2/N | T92 pin 14 | 0.250″ QC |
| AC-L2-TAP | 18 AWG 300VAC | blue | splice on AC-L2 | — | RAC02 **VAC_IN(N)** | RAC02 AC pin |
| AC-GND | 14 AWG AC | green-yellow | J1772 **Equipment Ground** | J1772 inlet PE | DJ7031-4.8 left bottom *and* chassis GND | 4.8 mm contact / chassis |
| AC-CHG-L | 14 AWG AC | brown | T92 pin 23 | 0.250″ QC | DJ7031-4.8 left top | 4.8 mm contact |
| AC-CHG-N | 14 AWG AC | blue | T92 pin 13 | 0.250″ QC | DJ7031-4.8 left mid | 4.8 mm contact |
| AC-CHG-L0 | 2.5 mm² charger pigtail | brown | DJ7031-4.8 right top | 4.8 mm contact | TSM2500 **AC_Input_Line** | charger AC pin 1 |
| AC-CHG-N0 | 2.5 mm² charger pigtail | blue | DJ7031-4.8 right mid | 4.8 mm contact | TSM2500 **AC_Input_Neutral** | charger AC pin 2 |
| AC-CHG-PE0 | 2.5 mm² charger pigtail | green-yellow | DJ7031-4.8 right bottom | 4.8 mm contact | TSM2500 **AC_Input_Earth_Ground** | charger AC pin 3 |

T92P11D22-12 (`Power_Relay1`) closes L1/L2 to the charger when the BMS charge coil is on.

---

## 5. 12 V vehicle battery and Blue Sea 5032

Battery / 12 V bus has no pigtail: **red = +**, **black = −**. F5 and F6 are both **MAXI 5006 50 A**. All 10 AWG 12 V runs are **GXL** (schematic **GLX**). 12 V feed from F6 is **red** to match DCIS output + through the mated DJ7021-8-21.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| 12-BAT+ | 10 AWG GXL | red | BT1 + (12 V vehicle battery) | battery + post | F5 (MAXI 50 A) *and* F6 (MAXI 50 A) (splice) | MAXI holder lug |
| 12-HOT | 10 AWG GXL | red | F5 | MAXI holder lug | Blue Sea **Always_Hot** bus *and* K3 (Cole Hersee 24213) pin 4 | #10-32 stud / solenoid stud |
| 12-SW | 10 AWG GXL | red | K3 pin 3 | solenoid stud | Blue Sea **Switched** bus | #10-32 stud |
| 12-DJ+ | 10 AWG GXL | red | F6 | MAXI holder lug | DJ7021-8-1 left top | 8.0 mm contact |
| 12-BAT− | 10 AWG GXL | black | BT1 − | battery − post | Blue Sea **Battery−** *and* DJ7021-8-1 left bottom *and* chassis GND | #10-32 stud / 8.0 mm / chassis |

DJ7021-8-1 left mates to right: 12 V battery +/− ↔ DCIS 12 V output +/− (red / black).

Ignition / inertia (coil side of K3). No factory harness; **red** = switched 12 V, **black** = ground.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| 12-IGN1 | 18 AWG TXL (unlabeled) | red | SW3 (Ignition) A | switch terminal | K3 pin 2 | Cole Hersee coil QC |
| 12-IGN2 | 18 AWG TXL (unlabeled) | red | SW3 B | switch terminal | SW4 (Inertia Switch) A | switch terminal |
| 12-KEY | 18 AWG TXL | red | SW4 B | switch terminal | Blue Sea **Key_Switch** circuit | #8-32 screw, ring/spade |
| 12-K3GND | 18 AWG TXL (unlabeled) | black | K3 pin 1 | coil QC | chassis GND | ring to chassis |

K4 is **Omron G9EJ-1-E-UVD DC12** (schematic value). Coil is 12 V continuous on the READY rail (TXL), 100 mA / 1.2 W. Contacts close pack + onto the DCIS key (HV, signal current). Polarized contacts: pack + on terminal **3 (+)**, key on terminal **4 (−)**. Coil has no polarity. 0.250″ QC.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| 12-K4C | 18 AWG TXL (unlabeled) | black | K4 pin 1 | G9EJ coil QC | chassis GND | ring to chassis |
| 12-K4S | 18 AWG CWHMIO | **blue** (READY, pin 2) | K4 pin 2 | G9EJ coil QC | READY net (WP-R3) | see §7 |

---

## 6. Charge-control 12 V (RAC02 + T92 coil)

RAC02 has no colored pigtail. **Orion CWHMIO 18 AWG colors carry** onto the T92 coil.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| CHG-12+ | 18 AWG CWHMIO | **red** (CHARGE, pin 3) | RAC02 **+VOUT** | RAC02 DC pin | T92 **A1** *and* Orion **CHARGE_Power** pin 3 | 0.250″ QC / TE 1376360-1 pin 3 |
| CHG-12− | 18 AWG (unlabeled) | black | RAC02 **−VOUT** | RAC02 DC pin | chassis GND | ring to chassis |
| CHG-SAFE | 18 AWG CWHMIO | **red/white** (Charger_Safety, pin 6) | T92 **A2** | 0.250″ QC | Orion **Charger_Safety_(on/off)** pin 6 | TE 1376360-1 pin 6 |

---

## 7. Delphi Weather Pack 4 (12 V / BMS bulkhead)

4-way Weather Pack between the Blue Sea / K2 side and the Orion / CAN-isolator side. **Orion 18 AWG CWHMIO colors carry through both housings.** Schematic pin order is top → bottom.

**Right housing (BMS / isolator) — Orion pigtail side**

| ID | Size / type | Color | Weather Pack pin | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| WP-R1 | 18 AWG CWHMIO | **black** (Ground, pin 12; verify) | right pin 1 (top) | BB CANOP **GND** *and* Orion **Ground** pin 12 | isolator / TE 1376360-1 pin 12 |
| WP-R2 | 18 AWG CWHMIO | **green** (Always_On, pin 1) | right pin 2 | Orion **Always_On_Power** pin 1 | TE 1376360-1 pin 1 |
| WP-R3 | 18 AWG CWHMIO | **blue** (READY, pin 2) | right pin 3 | Orion **READY_Power** pin 2 *and* BB CANOP **12V+** *and* K4 pin 2 | TE 1376360-1 pin 2 / isolator / G9EJ coil |
| WP-R4 | 18 AWG CWHMIO | **blue/white** (DISCHARGE_enable, pin 7) | right pin 4 (bottom) | Orion **DISCHARGE_enable** pin 7 | TE 1376360-1 pin 7 |

**Left housing (fuse block / K2) — same colors through the mate**

| ID | Size / type | Color | End A | A termination | Weather Pack pin |
| --- | --- | --- | --- | --- | --- |
| WP-L1 | 18 AWG | **black** (from pin 12) | Blue Sea **GND** circuit | #8-32 screw | left pin 1 (top) |
| WP-L2 | 18 AWG | **green** (Always_On) | Blue Sea **Always_On** circuit | #8-32 screw | left pin 2 |
| WP-L3 | 18 AWG | **blue** (READY) | Blue Sea **Ready/Precharge** *and* K2 pin 1 | #8-32 / T9A QC | left pin 3 |
| WP-L4 | 18 AWG | **blue/white** (DISCHARGE_enable) | K2 pin 2 | T9A QC | left pin 4 (bottom) |

Left mates to right, pin-for-pin.

---

## 8. CAN

Schematic: CAN1 250 kbps; **CAN shielding not terminated** on the inverter Deutsch. Orion CAN1 is a **12 ft shielded twisted pair** on the CWHMIO. Orion shield (pin 17) lands on the isolator. Shield grounded at one end only (Orion wiring manual).

**Trunk color = Orion CAN1 pair.** TSM2500 **green/white** (H) and **blue/white** (L) and CANdapter pigtails splice onto that pair and keep factory color only up to the splice.

### 8.1 HyPer 9 to Deutsch DTM 3

HyPer 9 K1 is AMPSEAL 776164-1. CAN_H = K1-13, CAN_L = K1-2. Standard K1 kits often leave K1-13 unpopulated — identify by **pin number**; colors vary.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| CAN-INV-H | 18–20 AWG K1 | *K1-13 harness — verify* | HyPer 9 **CAN_H** (K1-13) | AMPSEAL pin 13 | Deutsch DTM left pin 2 | DTM socket |
| CAN-INV-L | 18–20 AWG K1 | *K1-2 harness — verify* | HyPer 9 **CAN_L** (K1-2) | AMPSEAL pin 2 | Deutsch DTM left pin 3 | DTM socket |
| CAN-INV-SH | not terminated | — | Deutsch DTM left pin 1 | DTM socket | — | schematic: shield not terminated |

HyPer 9 **CAN_H_RES** (K1-14) is jumpered to **CAN_L_RES** (K1-3) on the schematic with note **internally termination**. That is the inverter termination jumper, not a harness cable.

### 8.2 Deutsch DTM 3 to BB CANOP (inverter side of isolator)

Carry the same K1 CAN colors through the DTM.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| CAN-ISO-1 | same as CAN-INV-* | *carry K1 CAN colors* | Deutsch DTM right pin 1 | DTM pin | BB CANOP pin 1 | isolator CAN TB |
| CAN-ISO-2 | same as CAN-INV-H | *carry K1-13* | Deutsch DTM right pin 2 | DTM pin | BB CANOP pin 2 | isolator CAN TB |
| CAN-ISO-3 | same as CAN-INV-L | *carry K1-2* | Deutsch DTM right pin 3 | DTM pin | BB CANOP pin 3 | isolator CAN TB |

### 8.3 BB CANOP (BMS side) to CAN1 bus

| ID | Size / type | Color | Ends | Terminations |
| --- | --- | --- | --- | --- |
| CAN1-H | 18 AWG CWHMIO CAN1 pair | Orion CAN1_H (pin 18; *verify inner*) | BB CANOP pin 6; Orion **CAN1_H** pin 18; CANdapter **CAN_H**; TSM2500 **CAN_H** (green/white pigtail to splice only) | isolator; TE 1376360-1 pin 18; CANdapter DB9 pin 7; charger CAN |
| CAN1-L | 18 AWG CWHMIO CAN1 pair | Orion CAN1_L (pin 19; *verify inner*) | BB CANOP pin 7; Orion **CAN1_L** pin 19; CANdapter **CAN_L**; TSM2500 **CAN_L** (blue/white pigtail to splice only) | isolator; TE 1376360-1 pin 19; CANdapter DB9 pin 2; charger CAN |
| CAN1-SH | shield drain | drain / bare | BB CANOP pin 5 | Orion **CAN1_Sheild** pin 17. Do not ground the shield elsewhere. |

### 8.4 CANdapter USB

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| USB-1 | USB 2.0 cable | black jacket | CANdapter **USB** | USB-B on adapter | USBConnector1 | USB connector (vehicle / laptop) |

USBConnector1 has a second pin with a short unterminated stub on the schematic (no far-end device).

---

## 9. J1772 pilot / proximity (Orion)

CWHMIO **18 AWG** colors carry from the I/O connector to the inlet.

| ID | Size / type | Color | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- | --- |
| J1772-CP | 18 AWG CWHMIO | **orange/white** (Control_Pilot, pin 13) | Orion **J1772_Control_Pilot** pin 13 | TE 1376360-1 pin 13 | J1772 **Control Pilot** | J1772 CP pin |
| J1772-PP | 18 AWG CWHMIO | **brown/white** (Proximity_Detect, pin 14) | Orion **J1772_Proximity_Detect** pin 14 | TE 1376360-1 pin 14 | J1772 **Proximity Detect** | J1772 PP pin |

---

## 10. Contactor coils (HyPer 9 K1)

Use the **K1 harness color printed for that pin** (kits vary). No published color for K1-25 / K1-26 in the HyPer text manual.

| ID | Size / type | Color | End A | A termination | End B | B termination | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MC-X1 | 18–20 AWG K1 | *K1-25 harness — verify* | HyPer 9 **COIL_RETURN_+** (K1-25) | AMPSEAL 776164-1 pin 25 | G1 **X1** | Gigavac coil | HyPer K1 |
| MC-X2 | 18–20 AWG K1 | *K1-26 harness — verify* | HyPer 9 **DRIVER_OUT_1_−** (K1-26) | AMPSEAL 776164-1 pin 26 | G1 **X2** | Gigavac coil | HyPer K1 |

---

## Not wired on this sheet

| Item | Notes |
| --- | --- |
| Orion **Fan_Monitor_MPI3** pin 9, **Fan_Enable_MPO3** pin 10 | No-connect (leave CWHMIO tails capped) |
| Blue Sea 5032 fused circuits 1–4 and 6 | Unused (circuit 5 is Key_Switch / 12-KEY) |
| Tesla module cell taps | Separate Orion tap harness (22 AWG, orange / red / yellow, black grounds) |
| HyPer 9 motor phase / encoder / thermistor | Encoder: red / yellow / green / black as in HyPer manual |
| TSM2500 12 V aux, LED, drive-away, temp | Not on this schematic |

K4 is Omron **G9EJ-1-E-UVD DC12** (see §5).

### CWHMIO pins still to read off the card

| Pin | Function | Color (from card) |
| --- | --- | --- |
| 12 | Ground (expect black) | |
| 18 / 19 | CAN1_H / CAN1_L inner | |

---

## Schematic check (2026-08-23)

Parsed `IH53EV.kicad_sch` after 10 AWG GXL (label GLX) update. Gaps left as documented:

- Traction 2/0 is **orange** with red/black heatshrink (vehicle convention; schematic stroke may still show +/−).
- Vehicle DCIS pack HV is **red / black** from the 3-way; factory pigtail stays yellow / gray.
- F5 and F6 are both **MAXI 5006 50 A**; all 10 AWG 12 V is **GXL** (sheet says GLX). Sheet wire key may still mention SGX.
- Precharge PC-01/02/03 has no size label; assigned **18 AWG HV** (T9A QC). Circuit_Breaker2 sheet text is **1Pole_1000V_DC_10Amp**.
- RAC02 / F7 taps: schematic has both **18AWG AC** and **18AWG 300VAC**; same runs as the wire key.
- DC-IN+ is one net with the K4 tap: **10 AWG HV** on breaker → stud, **18 AWG HV** at the tap (DC-K4TAP).
- Circuit_Breaker3 / Circuit_Breaker4 / 2-pole breakers have empty Value fields; ratings are from the reference / nearby text (32 A charger, 10 A DCIS).
- J1772 inlet instance reference is `J1773`.
- Unused: Blue Sea circuits 1–4 and 6, Orion fan pins 9/10, Tesla cell-tap pins, one TerminalBlock3 1/4″ stud, USBConnector1 stub.
