# IH-53 EV wiring list

Physical wires taken from `IH53EV.kicad_sch`. Size/type is the schematic text on that run when present. Where a run is unlabeled, size is taken from the README manuals (noted in **Source**). Connector / termination types are from those same manuals plus the parts drawn on the schematic.

Inline disconnects (Anderson, Weather Pack, Deutsch, USB) are drawn as two-sided symbols. Each side is a separate cable termination; mating the housings is not a wire.

## Wire key (from schematic)

| Code | Meaning |
| --- | --- |
| AWG | conductor size |
| TXL | 12 V / 48 V primary (GXL OK, same AWG) |
| SGX | 12 V battery cable (4 AWG) |
| HV | 600–1000 V DC pack (silicone / EV) |
| AC | J1772 / T92 mains (600 V) |
| 300VAC | RAC02 tap only |
| DLO | traction / pack 2/0 |

## Connector reference

Verified from README manuals and the schematic parts.

| Device | Mating connector | Contacts / wire | Source |
| --- | --- | --- | --- |
| Orion BMS 2 Main I/O | TE 1376360-1 | 22 AWG + TE 1123343-1 (or 18 AWG + Sumitomo 8240-4892) | [Orion BMS 2 wiring manual](https://www.orionbms.com/manuals/pdf/orionbms2_wiring_manual.pdf) |
| Orion voltage taps (cell taps, not drawn as wires on this sheet) | TE 1318389-1 | 22 AWG + TE 1123343-2 (gold) | same |
| HyPer 9 X1 K1 | TE AMPSEAL 35-pin 776164-1, pins 770854-1 | typically 18–20 AWG | [HyPer System User Manual](https://www.go-ev.com/PDFs/HyPer_System_User_Manual_RevA_1.pdf) |
| HyPer 9 B+ / B− | inverter DC lugs | 2/0 DLO, ring terminal | schematic; HyPer HV terminals |
| TSM2500 AC input | DJ7031-4.8-11 / 4.8-21 | 2.5 mm² (~14 AWG) | [TSM2500 manual](https://www.thunderstruck-ev.com/images/companies/1/Chargers/ThunderStruck-TSM2500-ManualV1.09.pdf) |
| TSM2500 DC output | Anderson SB50 | 6 mm² (~10 AWG) | same |
| TSM2500 CAN | charger signal connector (DJ7043 / CAN pair) | 0.5 mm² signal | same |
| DCIS 600 W output | 2-pin DCIS output connector (factory pigtail) | 6.0 mm² (~10 AWG) red/black | [DCIS schematic](https://www.fastandquiet.com/downloadable/600w-dc-dc-converter-isolated-dcis-schematic.PDF) |
| DCIS 600 W input / enable | 3-pin DCIS input connector | 1.5 mm² input (~16 AWG); 0.5 mm² key | same |
| CANdapter CAN | DE-9 (DB9) | twisted pair to pins 7 (CAN_H) and 2 (CAN_L) | [CANdapter manual](https://www.ewertenergy.com/products/candapter/downloads/candapter_manual.pdf); Orion wiring manual |
| CANdapter USB | USB-B on adapter | USB cable | CANdapter manual |
| Blue Sea 5032 buses | #10-32 stud | ring terminal | [Blue Sea 5032](https://www.bluesea.com/products/5032/ST_Blade_Split_Bus_Fuse_Block) |
| Blue Sea 5032 circuits | #8-32 screw | ring or spade | same |
| J1772 inlet | SAE J1772 socket | AC pins + CP / PP signal pins | schematic |
| Anderson 350 A / 600 V | SB350 housing | 2/0 contacts | schematic |
| Anderson SB50 | SB50 housing | 6–10 AWG contacts | schematic + TSM2500 / DCIS |
| Delphi Weather Pack 4 | Weather Pack 4-way | typically 16–20 AWG, sealed | schematic |
| Deutsch DTM 3 | DTM 3-way | 16–22 AWG | schematic |
| BB CANOP isolator | device CAN / power plugs | 22 AWG TXL on this drawing | schematic |
| HV terminal blocks | 5/16″ and 1/4″ studs | 2/0 lugs on 5/16″; smaller HV on 1/4″ | schematic |
| Gigavac GV200QA-1 | M8 HV terminals; coil X1/X2 | 2/0 lugs; coil 18–22 AWG | schematic / datasheet |
| T92P11D22-12 | 0.250″ QC | 14 AWG AC; 22 AWG coil | TE T92 |
| T9AP1D52-12 | 0.250″ QC | 18–22 AWG | TE T9A |
| Cole Hersee 24213 | stud contacts; QC coil | 4 AWG SGX contacts; 18–22 AWG coil | schematic |
| MAXI 5006 | MAXI fuse holder lugs | 4 AWG SGX / 10 AWG TXL | schematic |
| A25X500-4 | bolted fuse | 2/0 DLO lugs | schematic |

---

## 1. Traction pack (2/0 DLO)

Tesla modules **BT2–BT6** in series. Inter-module runs are unlabeled next to the modules; 2/0 DLO labels sit on that pack string.

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| HV-01 | 2/0 DLO | BT2 − | module − lug | TerminalBlock2 5/16″ | 5/16″ stud, ring lug |
| HV-02 | 2/0 DLO | BT2 + | module + lug | BT3 − | module − lug |
| HV-03 | 2/0 DLO | BT3 + | module + lug | BT4 − | module − lug |
| HV-04 | 2/0 DLO | BT4 + | module + lug | BT5 − | module − lug |
| HV-05 | 2/0 DLO | BT5 + | module + lug | BT6 − | module − lug |
| HV-06 | 2/0 DLO | BT6 + | module + lug | F4 (A25X500-4) | bolted fuse pad |
| HV-07 | 2/0 DLO | F4 | bolted fuse pad | SW1 (Kill Switch HVBD6AXR) | switch HV terminal |
| HV-08 | 2/0 DLO | SW1 | switch HV terminal | TerminalBlock1 5/16″ | 5/16″ stud, ring lug |
| HV-09 | 2/0 DLO | TerminalBlock1 5/16″ | 5/16″ stud, ring lug | Anderson350A600V1 right + | SB350 contact (2/0) |
| HV-10 | 2/0 DLO | TerminalBlock2 5/16″ | 5/16″ stud, ring lug | Anderson350A600V1 right − | SB350 contact (2/0) |
| HV-11 | 2/0 DLO | Anderson350A600V1 left + | SB350 contact (2/0) | TerminalBlock3 5/16″ (pack + bus) | 5/16″ stud, ring lug |
| HV-12 | 2/0 DLO | Anderson350A600V1 left − | SB350 contact (2/0) | HyPer 9 **B+** | inverter B+ lug |
| HV-13 | 2/0 DLO | HyPer 9 **B−** | inverter B− lug | G1 (GV200QA-1) **A2−** | Gigavac M8 HV terminal |
| HV-14 | 2/0 DLO | G1 **A1+** | Gigavac M8 HV terminal | TerminalBlock3 5/16″ (pack + bus) | 5/16″ stud, ring lug |

SB350 left housing mates to right housing: pack + bus ↔ TB1, inverter B+ ↔ TB2−.

Cell taps on BT2–BT6 are **not** wired on this sheet. Orion tap harness is 22 AWG to TE 1318389-1; module end is a ring terminal on each tap (Orion wiring manual). Schematic notes **internally termination** at the modules.

---

## 2. Charger HV DC

TSM2500 DC pigtail is 6 mm² to SB50 in the charger manual. This sheet does not label those charger-to-breaker runs; pack-side cables on TB1/TB2 are 2/0 DLO.

| ID | Size / type | End A | A termination | End B | B termination | Source |
| --- | --- | --- | --- | --- | --- | --- |
| CH-DC+ | 6 mm² (~10 AWG) charger pigtail | TSM2500 **DC_Output_+** | Anderson SB50 (charger) | Circuit_Breaker3 | breaker HV terminal | TSM2500 manual; unlabeled on sheet |
| CH-DC+2 | HV (unlabeled) | Circuit_Breaker3 | breaker HV terminal | TerminalBlock1 1/4″ | 1/4″ stud, ring lug | schematic |
| CH-DC− | 6 mm² (~10 AWG) charger pigtail | TSM2500 **DC_Ouput_−** | Anderson SB50 (charger) | 2Pole_1000V_DC_32Amp1 | breaker HV terminal | TSM2500 manual; unlabeled on sheet |
| CH-DC−2 | HV (unlabeled) | 2Pole_1000V_DC_32Amp1 | breaker HV terminal | TerminalBlock2 1/4″ | 1/4″ stud, ring lug | schematic |

---

## 3. DC-DC converter (pack → 12 V)

DCIS factory leads: output 6.0 mm² (~10 AWG), input 1.5 mm² (~16 AWG), key 0.5 mm². 12 V output lands on Anderson **SB50** (same family as the charger DC plug).

| ID | Size / type | End A | A termination | End B | B termination | Source |
| --- | --- | --- | --- | --- | --- | --- |
| DC-IN+ | 1.5 mm² (~16 AWG) HV | DCIS **Input+** | DCIS 3-pin input | Circuit_Breaker4 *and* K4 pin 3 (splice) | breaker HV terminal; T9A QC | DCIS schematic; unlabeled on sheet |
| DC-IN+2 | HV (unlabeled) | Circuit_Breaker4 | breaker HV terminal | TerminalBlock1 1/4″ | 1/4″ stud | schematic |
| DC-IN− | 1.5 mm² (~16 AWG) HV | DCIS **Input−** | DCIS 3-pin input | 2Pole_1000V_DC_10Amp1 | breaker HV terminal | DCIS schematic; unlabeled on sheet |
| DC-IN−2 | HV (unlabeled) | 2Pole_1000V_DC_10Amp1 | breaker HV terminal | TerminalBlock2 1/4″ | 1/4″ stud | schematic |
| DC-KEY | 0.5 mm² (~20–22 AWG) | DCIS **Key_Switch_Control** | DCIS 3-pin input (green) | K4 pin 4 | T9A QC | DCIS schematic; unlabeled on sheet |
| DC-OUT+ | 10 AWG TXL | DCIS **Output+** | DCIS 2-pin output (red 6.0 mm²) | AndersonSB1 right + | SB50 contact | DCIS 6.0 mm²; 10 AWG TXL on 12 V SB50 path |
| DC-OUT− | 10 AWG TXL | DCIS **Output−** | DCIS 2-pin output (black 6.0 mm²) | AndersonSB1 right − | SB50 contact | same |

Precharge path from pack + into the inverter:

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| PC-01 | HV (unlabeled) | TerminalBlock3 1/4″ | 1/4″ stud | Circuit_Breaker2 | breaker HV terminal |
| PC-02 | HV (unlabeled) | Circuit_Breaker2 | breaker HV terminal | K2 (T9AP1D52-12) pin 4 | T9A QC |
| PC-03 | HV (unlabeled) | K2 pin 3 | T9A QC | HyPer 9 **Precharge/Key_Switch_In** (K1-24) | AMPSEAL 776164-1 pin 24 |

K1-24 is the only HyPer 9 K1 pin that sees pack voltage on a non-isolated X1 (HyPer manual).

---

## 4. J1772 / charger AC

14 AWG AC on the schematic. TSM2500 AC is 2.5 mm² (~14 AWG) into DJ7031-4.8. RAC02 tap is **18 AWG 300VAC**.

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| AC-L1 | 14 AWG AC | J1772 **L1** | J1772 inlet L1 | F7 (F5×20, 1 A max) *and* T92 pin 24 (splice) | fuse clip / 0.250″ QC |
| AC-L1-RAC | 14 AWG AC | F7 | fuse clip | RAC02 **VAC_IN(L)** | RAC02 AC pin |
| AC-L2 | 14 AWG AC | J1772 **L2/N** | J1772 inlet L2/N | T92 pin 14 *and* RAC02 **VAC_IN(N)** (splice) | 0.250″ QC / RAC02 AC pin |
| AC-L2-TAP | 18 AWG 300VAC | splice on AC-L2 | — | RAC02 **VAC_IN(N)** | RAC02 AC pin (300 V tap only) |
| AC-GND | 14 AWG AC | J1772 **Equipment Ground** | J1772 inlet PE | TSM2500 **AC_Input_Earth_Ground** *and* chassis GND | DJ7031 PE / chassis |
| AC-CHG-L | 14 AWG AC | T92 pin 23 | 0.250″ QC | TSM2500 **AC_Input_Line** | DJ7031 pin 1 (brown, 2.5 mm²) |
| AC-CHG-N | 14 AWG AC | T92 pin 13 | 0.250″ QC | TSM2500 **AC_Input_Neutral** | DJ7031 pin 2 (blue, 2.5 mm²) |

T92P11D22-12 (`Power_Relay1`) closes L1/L2 to the charger when the BMS charge coil is on.

---

## 5. 12 V vehicle battery and Blue Sea 5032

4 AWG SGX on battery cables. 10 AWG TXL on the SB50 / DC-DC 12 V path. Blue Sea buses are #10-32 studs; fused outputs are #8-32 screws (ring or spade).

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| 12-BAT+ | 4 AWG SGX | BT1 + (12 V vehicle battery) | battery + post | F5 (MAXI 80 A) *and* F6 (MAXI 50 A) (splice) | MAXI holder lug |
| 12-HOT | 4 AWG SGX | F5 | MAXI holder lug | Blue Sea **Always_Hot** bus *and* K3 (Cole Hersee 24213) pin 4 | #10-32 stud / solenoid stud |
| 12-SW | 4 AWG SGX | K3 pin 3 | solenoid stud | Blue Sea **Switched** bus | #10-32 stud |
| 12-SB50+ | 10 AWG TXL | F6 | MAXI holder lug | AndersonSB1 left + | SB50 contact |
| 12-BAT− | 4 AWG SGX | BT1 − | battery − post | Blue Sea **Battery−** *and* AndersonSB1 left − *and* chassis GND | #10-32 stud / SB50 / chassis |

SB50 left mates to right: 12 V battery +/− ↔ DCIS 12 V output +/−.

Ignition / inertia (coil side of K3):

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| 12-IGN1 | 18–22 AWG TXL (unlabeled) | SW3 (Ignition) A | switch terminal | K3 pin 2 | Cole Hersee coil QC |
| 12-IGN2 | 18–22 AWG TXL (unlabeled) | SW3 B | switch terminal | SW4 (Inertia Switch) A | switch terminal |
| 12-KEY | 18 AWG TXL | SW4 B | switch terminal | Blue Sea **Key_Switch** circuit | #8-32 screw, ring/spade |
| 12-K3GND | 18–22 AWG TXL (unlabeled) | K3 pin 1 | coil QC | chassis GND | ring to chassis |

K4 (DC-DC enable; value still `fix me` on the schematic):

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| 12-K4C | 18–22 AWG TXL (unlabeled) | K4 pin 1 | relay coil | chassis GND | ring to chassis |
| 12-K4S | 22 AWG TXL (Orion I/O) | K4 pin 2 | relay coil / contact (see net) | READY / isolator 12 V+ net (W-06) | Weather Pack / TE I/O — see §7 |

---

## 6. Charge-control 12 V (RAC02 + T92 coil)

RAC02-12SE_277 is a 12 V, 2 W supply off J1772 AC (18 AWG 300VAC tap). Coil wiring is **22 AWG TXL**.

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| CHG-12+ | 22 AWG TXL | RAC02 **+VOUT** | RAC02 DC pin | T92 **A1** *and* Orion **CHARGE_Power** pin 3 | 0.250″ QC / TE 1376360-1 pin 3 |
| CHG-12− | 22 AWG TXL (unlabeled) | RAC02 **−VOUT** | RAC02 DC pin | chassis GND | ring to chassis |
| CHG-SAFE | 22 AWG TXL | T92 **A2** | 0.250″ QC | Orion **Charger_Safety_(on/off)** pin 6 | TE 1376360-1 pin 6 |

---

## 7. Delphi Weather Pack 4 (12 V / BMS bulkhead)

4-way Weather Pack between the Blue Sea / K2 side and the Orion / CAN-isolator side. Schematic pin order is top → bottom.

**Left housing (fuse block / K2)**

| ID | Size / type | End A | A termination | Weather Pack pin | Source |
| --- | --- | --- | --- | --- | --- |
| WP-L1 | 22 AWG TXL | Blue Sea **GND** circuit | #8-32 screw | left pin 1 (top) | Orion I/O is 22 AWG; unlabeled on this run |
| WP-L2 | 22 AWG TXL | Blue Sea **Always_On** circuit | #8-32 screw | left pin 2 | same |
| WP-L3 | 22 AWG TXL | Blue Sea **Ready/Precharge** *and* K2 pin 1 | #8-32 / T9A QC | left pin 3 | same |
| WP-L4 | 22 AWG TXL | K2 pin 2 | T9A QC | left pin 4 (bottom) | same |

**Right housing (BMS / isolator)**

| ID | Size / type | Weather Pack pin | End B | B termination |
| --- | --- | --- | --- | --- |
| WP-R1 | 22 AWG TXL | right pin 1 (top) | BB CANOP **GND** *and* Orion **Ground** pin 12 | isolator power pin / TE 1376360-1 pin 12 |
| WP-R2 | 22 AWG TXL | right pin 2 | Orion **Always_On_Power** pin 1 | TE 1376360-1 pin 1 |
| WP-R3 | 22 AWG TXL | right pin 3 | Orion **READY_Power** pin 2 *and* BB CANOP **12V+** *and* K4 pin 2 | TE 1376360-1 pin 2 / isolator / T9A |
| WP-R4 | 22 AWG TXL | right pin 4 (bottom) | Orion **DISCHARGE_enable** pin 7 | TE 1376360-1 pin 7 |

Left mates to right, pin-for-pin.

---

## 8. CAN (22 AWG TXL, twisted pair)

Schematic: CAN1 250 kbps; **CAN shielding not terminated** on the inverter Deutsch. Orion CAN1 shield (pin 17) is landed on the isolator. Orion manual: shielded twisted pair; shield grounded at one end only (BMS pins provided for that).

### 8.1 HyPer 9 to Deutsch DTM 3

HyPer 9 K1 is AMPSEAL 776164-1. CAN_H = K1-13, CAN_L = K1-2.

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| CAN-INV-H | 22 AWG TXL | HyPer 9 **CAN_H** (K1-13) | AMPSEAL pin 13 | Deutsch DTM left pin 2 | DTM socket |
| CAN-INV-L | 22 AWG TXL | HyPer 9 **CAN_L** (K1-2) | AMPSEAL pin 2 | Deutsch DTM left pin 3 | DTM socket |
| CAN-INV-SH | not terminated | Deutsch DTM left pin 1 | DTM socket | — | schematic: shield not terminated |

HyPer 9 **CAN_H_RES** (K1-14) is jumpered to **CAN_L_RES** (K1-3) on the schematic with note **internally termination**. That is the inverter termination jumper, not a harness cable.

### 8.2 Deutsch DTM 3 to BB CANOP (inverter side of isolator)

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| CAN-ISO-1 | 22 AWG TXL | Deutsch DTM right pin 1 | DTM pin | BB CANOP pin 1 | isolator CAN plug |
| CAN-ISO-2 | 22 AWG TXL | Deutsch DTM right pin 2 | DTM pin | BB CANOP pin 2 | isolator CAN plug |
| CAN-ISO-3 | 22 AWG TXL | Deutsch DTM right pin 3 | DTM pin | BB CANOP pin 3 | isolator CAN plug |

### 8.3 BB CANOP (BMS side) to CAN1 bus

Multi-drop **CAN_H** / **CAN_L** (splice or short stubs):

| ID | Size / type | Ends | Terminations |
| --- | --- | --- | --- |
| CAN1-H | 22 AWG TXL (shielded pair w/ CAN1-L) | BB CANOP pin 6; Orion **CAN1_H** pin 18; CANdapter **CAN_H**; TSM2500 **CAN_H** | isolator CAN; TE 1376360-1 pin 18; CANdapter DB9 pin 7; charger CAN pair |
| CAN1-L | 22 AWG TXL (shielded pair w/ CAN1-H) | BB CANOP pin 7; Orion **CAN1_L** pin 19; CANdapter **CAN_L**; TSM2500 **CAN_L** | isolator CAN; TE 1376360-1 pin 19; CANdapter DB9 pin 2; charger CAN pair |
| CAN1-SH | 22 AWG drain / shield | BB CANOP pin 5 | Orion **CAN1_Sheild** pin 17 (TE 1376360-1 pin 17). Do not ground the shield elsewhere (Orion wiring manual). |

### 8.4 CANdapter USB

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| USB-1 | USB 2.0 cable | CANdapter **USB** | USB-B on adapter | USBConnector1 | USB connector (vehicle / laptop) |

USBConnector1 has a second pin with a short unterminated stub on the schematic (no far-end device).

---

## 9. J1772 pilot / proximity (Orion)

Orion I/O pins 13–14. Schematic **22 AWG TXL**. Orion manual: 22 AWG into TE 1376360-1.

| ID | Size / type | End A | A termination | End B | B termination |
| --- | --- | --- | --- | --- | --- |
| J1772-CP | 22 AWG TXL | Orion **J1772_Control_Pilot** pin 13 | TE 1376360-1 pin 13 | J1772 **Control Pilot** | J1772 CP pin |
| J1772-PP | 22 AWG TXL | Orion **J1772_Proximity_Detect** pin 14 | TE 1376360-1 pin 14 | J1772 **Proximity Detect** | J1772 PP pin |

---

## 10. Contactor coils (HyPer 9 K1)

| ID | Size / type | End A | A termination | End B | B termination | Source |
| --- | --- | --- | --- | --- | --- | --- |
| MC-X1 | 18–20 AWG | HyPer 9 **COIL_RETURN_+** (K1-25) | AMPSEAL 776164-1 pin 25 | G1 **X1** | Gigavac coil | HyPer K1 harness; unlabeled on sheet |
| MC-X2 | 18–20 AWG | HyPer 9 **DRIVER_OUT_1_−** (K1-26) | AMPSEAL 776164-1 pin 26 | G1 **X2** | Gigavac coil | same |

---

## Not wired on this sheet

| Item | Notes |
| --- | --- |
| Orion **Fan_Monitor_MPI3** pin 9, **Fan_Enable_MPO3** pin 10 | No-connect |
| Blue Sea 5032 fused circuits 1–4 and 6 | Unused (circuit 5 has a dangling stub only) |
| Tesla module cell taps | Separate Orion tap harness (22 AWG, TE 1318389-1) |
| HyPer 9 motor phase / encoder / thermistor | Not on this schematic |
| TSM2500 12 V aux, LED, drive-away, temp | Not on this schematic |

K4 still has schematic value `fix me`; treat coil/contact pinout as drawn until that part is chosen.
