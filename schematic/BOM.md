# IH-53 EV bill of materials

Purchase list for the wiring in [`wires.md`](wires.md) / `IH53EV.kicad_sch`. Lengths are **buy quantities** (spool / cut with slack), not measured harness lengths.

**How to use:** skip anything already on the truck. Factory pigtails and their housings ship with the device — do not rebuy those halves. Buy the vehicle-side mate, contacts, and bulk wire.

Tesla modules **BT2–BT6** in series are ~108–126 V. HV insulation on this sheet is 600–1000 V; interrupting ratings must still be **DC** at pack voltage.

---

## 1. Major assemblies (confirm on hand)

| Qty | Item | MPN / spec | Used for | Status |
| --- | --- | --- | --- | --- |
| 5 | Tesla Model S battery modules | BT2–BT6 | traction pack | on hand |
| 1 | 12 V vehicle battery | BT1 | Blue Sea / DCIS 12 V | on hand / buy if needed |
| 1 | NetGain HyPer 9 + K1 AMPSEAL harness | AMPSEAL 776164-1 | inverter | on hand |
| 1 | Orion BMS 2 + **CWHMIO 18 AWG** Main I/O | TE 1376360-1, Sumitomo 8240-4892 | BMS | on hand |
| 1 | Orion cell-tap harness | TE 1318389-1, 22 AWG | module taps (not on this sheet) | on hand / separate |
| 1 | Thunderstruck TSM2500 | includes DJ7031-4.8 + SB50 pigtails | charger | on hand |
| 1 | Fast and Quiet DCIS 600 W | includes dj70310-6.3-11 + DJ7021-8-21 | pack → 12 V | on hand |
| 1 | Ewert CANdapter | DE-9 CAN, USB-B | CAN config | on hand |

---

## 2. Buy — HV switching and protection

| Qty | Item | MPN / spec | Used for | Where |
| --- | --- | --- | --- | --- |
| 1 | Pack fuse 500 A, bolted semiconductor | Mersen **A25X500-4** (500 A, 250 V) | F4, pack + | DigiKey / Mersen |
| 1 | Fuse block / pads for A25X (1.5″ dia, bolt-in) | match A25X500-4 | F4 mounting | with fuse |
| 1 | Manual HV battery disconnect, 600 A, red handle, no aux | Rincon **HVBD6AXR** | SW1 kill switch | Rincon / EV distributors |
| 1 | HV contactor, 12 V coil, M8 power terminals | Gigavac / Sensata **GV200QA-1** | G1 pack + | Gigavac / EV distributors |
| 1 | Precharge / discharge relay, 12 V coil, SPST-NO, #250 QC | TE Potter & Brumfield **T9AP1D52-12** | K2 | DigiKey / Mouser |
| 1 | Charger AC relay, 12 V coil, DPDT, #250 QC | TE Potter & Brumfield **T92P11D22-12** | Power_Relay1 | DigiKey / Mouser |
| 1 | Pack-voltage key relay, 12 V coil, 400 V DC / 15 A, polarized contacts 3+ / 4− | Omron **G9EJ-1-E-UVD DC12** | K4 DCIS key | DigiKey / Mouser (not Amazon cube relays) |
| 1 | 12 V continuous-duty solenoid, 200 A, insulated coil | Cole Hersee / Littelfuse **24213** (aka 24213-BX) | K3 switched 12 V | Waytek / NAPA |
| 1 | 2-pole **1000 V DC** breaker, **32 A** | schematic `2Pole_1000V_DC_32Amp1` + `Circuit_Breaker3` (both poles of one breaker) | TSM2500 DC +/− | PV/EV DC MCB (e.g. Noark Ex9BP 4P 1000 V class — confirm pole count vs 1000 V) |
| 1 | 2-pole **1000 V DC** breaker, **10 A** | schematic `2Pole_1000V_DC_10Amp1` + `Circuit_Breaker4` | DCIS pack +/− | same family |
| 1 | 1-pole **1000 V DC** breaker, **10 A** | schematic `Circuit_Breaker2` / sheet text `1Pole_1000V_DC_10Amp` | precharge | same family |
| 1 | MAXI fuse holder | Littelfuse **5006** | F5 | Waytek / DigiKey |
| 1 | MAXI fuse **50 A** | MAXI 50 A | F5, 12 V Always_Hot | same |
| 1 | MAXI fuse holder | Littelfuse **5006** | F6 | same |
| 1 | MAXI fuse **50 A** | MAXI 50 A | F6, DCIS 12 V feed | same |
| 1 | 5×20 mm fuse holder (panel or inline) | F5×20 | F7 | DigiKey |
| 5 | 5×20 mm fuse **1 A**, slow-blow (Recom T1A class) | schematic `F5x20 (1A max)` | F7 RAC02 | DigiKey (spares) |

Breaker Values are empty on the schematic; ratings above are from the reference designators and the `1Pole_1000V_DC_10Amp` note. Buy **DC-rated** PV/EV breakers, not AC-only DIN breakers.

---

## 3. Buy — 12 V, charge, CAN, inlet

| Qty | Item | MPN / spec | Used for | Where |
| --- | --- | --- | --- | --- |
| 1 | ST Blade split-bus fuse block | Blue Sea **5032** | Always_Hot / Switched / fused circuits | Blue Sea / West Marine |
| 1 | ATO/ATC fuse assortment 5–15 A | — | Blue Sea circuits actually used (Always_On, Ready/Precharge, Key_Switch). Circuits 1–4 and 6 unused. | any |
| 1 | PCB AC/DC 2 W, 12 V out, 85–305 VAC | Recom **RAC02-12SE/277** (schematic `RAC02-12SE_277`). If NRND, successor in RAC02-E/277 or RAC02-SK 12 V 2 W | charge 12 V for T92 / Orion CHARGE | DigiKey / Mouser |
| 1 | CAN isolator | Advantech **BB-CANOP** | HyPer CAN ↔ Orion CAN1 | Advantech / DigiKey |
| 1 | SAE J1772 inlet (16–32 A) | any listed J1772 socket | AC + CP + PP (`J1773` on the sheet) | EVSE suppliers |
| 1 | Ignition / key SPST | schematic SW3 | K3 coil | automotive |
| 1 | Inertia / crash switch, SPST, NC or as wired | schematic SW4 | series with ignition | automotive (GM-style inertia) |
| 1 | USB bulkhead or USB-A/B extension | USBConnector1 | CANdapter USB | any |

---

## 4. Buy — connectors (vehicle side)

Included pigtails: TSM2500 DJ7031 + SB50, DCIS dj70310 + DJ7021, Orion CWHMIO, HyPer K1. Buy mates / extra contacts only if you are building the vehicle half instead of splicing onto the pigtail.

| Qty | Item | MPN / spec | Used for |
| --- | --- | --- | --- |
| 1 pair | Anderson **SB350** housings, 350 A / 600 V | Anderson SB350 | pack / inverter disconnect |
| 4 | SB350 contacts for **2/0** | Anderson 2/0 contacts (e.g. 905-series) | HV-09…HV-12 |
| 1 | Anderson **SB50** housing + 2× contacts for **6–10 AWG / 6 mm²** | mate to TSM2500 DC pigtail | CH-DC+V / CH-DC−V |
| 1 | Weather Pack **4-way** kit (both housings, TPA, cable seals) | Aptiv 4-way line **12015797** (tower) + **12010974** (shroud), or 4-way square **12015798** + **12015024**; terminals **18 AWG** (socket 12089188 / pin 12089040 class) | DelphiWeather4Pack1 |
| 1 | Deutsch **DTM 3** kit | **DTM06-3S** + **DTM04-3P**, wedges WM-3S / WM-3P, pins 1060-16-0122, sockets 1062-16-0122 | inverter CAN bulkhead |
| 1 | DJ7031-4.8 vehicle half + 3× 4.8 mm contacts for **14 AWG** | mate to TSM2500 AC | AC-CHG-L/N/PE |
| 1 | dj70310-6.3-11 vehicle half + contacts: 2× **10 AWG HV** (or 14–16 AWG tails if 6.3 mm will not take 10 AWG), 1× **18 AWG HV** | mate to DCIS input/key | DC-IN+ (red), DC-IN− (black), DC-KEY (green) |
| 1 | DJ7021-8-21 vehicle half + 2× 8.0 mm contacts for **10 AWG** | mate to DCIS 12 V | 12-DJ+, 12-BAT− |
| — | Sumitomo **8240-4892** | only if extending/re-pinning CWHMIO | Orion Main I/O |

---

## 5. Buy — wire

Colors follow [`wires.md`](wires.md). **HV is 600–1000 V silicone / EV**, not TXL. Traction 2/0 is **orange**; polarity is heatshrink, not jacket color.

| Qty | Size / type | Color | Used for (wire IDs) |
| --- | --- | --- | --- |
| 45 ft | 2/0 DLO | **orange** | HV-01…HV-14 (all traction) |
| 18 ft | 10 AWG **GXL** (schematic GLX) | red | 12-BAT+, 12-HOT, 12-SW, 12-DJ+ |
| 8 ft | 10 AWG GXL | black | 12-BAT− |
| 20 ft | 10 AWG HV | red | CH-DC+V, CH-DC+2, DC-IN+, DC-IN+2 |
| 20 ft | 10 AWG HV | black | CH-DC−V, CH-DC−2, DC-IN−, DC-IN−2 |
| 8 ft | 18 AWG HV | red | DC-K4TAP, PC-01, PC-02, PC-03 |
| 8 ft | 18 AWG HV | green | DC-KEY |
| 15 ft | 14 AWG 600 V AC (THHN/MTW/SXL as preferred) | brown | AC-L1, AC-CHG-L |
| 15 ft | 14 AWG 600 V AC | blue | AC-L2, AC-CHG-N |
| 15 ft | 14 AWG 600 V AC | green-yellow | AC-GND |
| 5 ft | 18 AWG **300 VAC** (or 18 AWG AC as labeled) | brown | AC-L1-F7, AC-L1-RAC |
| 5 ft | 18 AWG 300 VAC | blue | AC-L2-TAP |
| 25 ft | 18 AWG TXL | red | 12-IGN1, 12-IGN2, 12-KEY, leftover 12 V |
| 15 ft | 18 AWG TXL | black | 12-K3GND, 12-K4C, CHG-12− |
| 1 pack | 2/0 adhesive heatshrink | **red** | + ends of orange 2/0 |
| 1 pack | 2/0 adhesive heatshrink | **black** | − ends of orange 2/0 |

Do **not** buy TXL for charger DC, DCIS pack input, DCIS key, or precharge. Vehicle DCIS pack HV is the same **10 AWG HV** as charger DC (red / black). Factory pigtail stays yellow / gray.

Orion CWHMIO already supplies Always_On (green), READY (blue), CHARGE (red), Charger_Safety (red/white), DISCHARGE_enable (blue/white), CP (orange/white), PP (brown/white), CAN1 pair, and typically ground. Extend those tails rather than replacing them.

HyPer K1 already supplies CAN (K1-13 / K1-2), precharge/key (K1-24), and coil (K1-25 / K1-26) — splice or pin those colors; do not guess.

---

## 6. Buy — lugs and terminals

| Qty (min) | Item | Wire | Lands on |
| --- | --- | --- | --- |
| 12 | 2/0 ring, **5/16″** | 2/0 DLO | TB1/2/3 5/16″, module lugs, F4, SW1, SB350 |
| 4 | 2/0 ring, **M8** | 2/0 DLO | Gigavac A1+ / A2−, HyPer B+ / B− if M8 |
| 6 | 10 AWG HV ring, **#10-32** | 10 AWG HV | TB1 / TB2 #10 studs (4 used + spares) |
| 2 | 18 AWG HV ring, **#10-32** | 18 AWG HV | TB3 #10 precharge (+ spare) |
| 12 | 10 AWG HV ring, **1/4″ or M6** | 10 AWG HV | charger DC and DCIS breaker terminals (match breaker) |
| 4 | 18 AWG HV ring, **1/4″ or M6** | 18 AWG HV | Circuit_Breaker2 terminals (match breaker) |
| 8 | 10 AWG ring, **5/16″–24** | 10 AWG GXL | K3 studs, MAXI 5006, battery posts |
| 4 | 10 AWG ring, **#10-32** | 10 AWG GXL | Blue Sea Always_Hot / Switched / Battery− |
| 8 | 18 AWG ring or spade, **#8-32** | 18 AWG | Blue Sea circuits |
| 6 | 18 AWG ring, **#10** chassis | 18 AWG TXL / HV | chassis GND |
| 20 | 0.250″ QC (insulated), 14 AWG | 14 AWG AC | T92 pins 13/14/23/24 |
| 20 | 0.250″ QC (insulated), 18 AWG | 18 AWG | T92 A1/A2, T9A, G9EJ, Cole Hersee coil |
| 10 | 18 AWG HV 0.250″ QC | 18 AWG HV | G9EJ contacts 3/4, T9A pins 3/4 |
| 1 pack | heat-shrink, adhesive lined, 10 AWG through 18 AWG | — | every small lug |
| — | HV bus bars TB1/TB2/TB3 | 5/16″-18 + #10-32 | make — §6b |

---

## 6b. Buy / make — HV copper bus bars

Three identical C110 bars. TB1 and TB3 are pack **+**; TB2 is pack **−**. 500 A pack fuse (A25X500-4) sets the section: 1/4″ × 2″ is ~323 mm², enough for a short open 500 A run. Split **8″** sticks in half (**4.00″ / 101.6 mm**); two sticks make three bars plus a spare. Through-bolt 5/16″ heads under the bar clear the SM40 (~36 mm c-c).

| Qty | Item | MPN / spec | Used for |
| --- | --- | --- | --- |
| 3 | Copper bar blank | C110, **1/4″ × 2″**, cut **101.6 mm** (8″ stick split in half; buy 2 sticks) | TB1, TB2, TB3 |
| 6 | 5/16″-18 bus stud, SS or silicon bronze, ~1.25″ above bar | brazed, press-in, or through-bolt + jam nut | 2/0 landings |
| 6 | #10-32 bus stud, SS or silicon bronze, ~1.0″ above bar | same | 10/18 AWG HV landings |
| 12 | 5/16″-18 hex nut + SAE flat washer + Belleville | SS | 2/0 clamp (2 nuts/stud if through-bolt) |
| 12 | #10-32 hex nut + #10 washer + Belleville | SS | small HV clamp |
| 3 | **SM40** busbar standoff | BMC, 40 mm tall, 40 mm face / 34 mm waist, **M8** inserts 11 mm both ends, 1000 VAC / 1500 VDC | 1 per bar, under the center; **not** battery-box mounts |
| 6 | M8 × 20 mm hex bolt + M8 flat washer | SS or zinc | 1 through bar into SM40 top; 1 from chassis into SM40 bottom |

Do **not** substitute 1/4″ lugs on the small studs — #10-32 is 0.190″, not 0.250″.

Do **not** land a cable on the center M8 — that bolt only clamps the bar to the SM40. Torque the M8 to the insulator rating (~13 N·m), not lug torque.

---

## 7. Optional / tooling

| Qty | Item | Why |
| --- | --- | --- |
| 1 | 2/0 lug crimper (dies for 2/0 DLO) | traction cable |
| 1 | Weather Pack crimper + cavity tool | 4-way bulkhead |
| 1 | Deutsch DTM (size 16) crimper | inverter CAN |
| 1 | 14 / 18 AWG insulated-terminal crimper | QC and rings |
| — | HV cable loom, orange tape, warning labels | pack / charger DC / DCIS HV |

---

## 8. Do not buy (included or unused)

| Item | Why |
| --- | --- |
| TSM2500 AC DJ7031 pigtail, DC SB50 pigtail, CAN pair | ships with charger |
| DCIS dj70310 / DJ7021 pigtails | ships with DCIS |
| Orion CWHMIO 18 AWG Main I/O | ships with this BMS |
| HyPer 9 K1 AMPSEAL harness | ships with inverter |
| CANdapter USB-B cable | ships with adapter (add bulkhead only if you want a dash port) |
| Blue Sea circuits 1–4, 6 | unused on this sheet |
| Orion fan pins 9 and 10 | no-connect |
| Tesla cell taps on this schematic | separate Orion tap harness |

---

## 9. Schematic vs this list

- Kill switch: **Rincon HVBD6AXR** (600 A, no aux, red).
- K4: **Omron G9EJ-1-E-UVD DC12** only — polarized HV contacts, 12 V coil.
- F5 and F6 are both **MAXI 50 A**; all 10 AWG 12 V is **GXL** (schematic GLX).
- Traction 2/0 is **orange** with red/black heatshrink at the lugs.
- Vehicle DCIS pack HV is **red / black** 10 AWG HV, same cable as charger DC (factory pigtail stays yellow / gray).
- Precharge wire is unlabeled on the sheet; buy **18 AWG HV** red.
- RAC02 taps: buy **18 AWG 300 VAC** (schematic also says 18AWG AC).
- J1772 symbol reference is `J1773`.
- Circuit_Breaker3 is the second pole of the **32 A** charger DC breaker; Circuit_Breaker4 is the second pole of the **10 A** DCIS breaker.
- TB1/TB3 (`Terminal_Block+`) and TB2 (`Terminal_Block−`): small studs are **#10-32**, not 1/4″. 2/0 still lands on **5/16″**.
