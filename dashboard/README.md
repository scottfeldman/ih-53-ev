# IH-53 EV dashboard

Go + Fiber + HTMX + Gomponents instrument panel for the Raspberry Pi 5 + PiCAN 3.

Listens on `:10000`, talks **SocketCAN** `can0` at **250 kbps** (BMS-side CAN1 tap). Orion remains the TSM2500 charge master. The dash is **listen-only** for telemetry (Orion broadcasts + TSM2500 status + HyPer TPDOs). The only optional TX is **confirm-clear Orion DTCs** (OBD2 Mode `$04`).

## Hardware

- Pi 5 + [PiCAN 3](https://www.skpang.co.uk/collections/hats/products/pican3-can-bus-board-for-raspberry-pi-4-with-3a-smps-rtc)
- Tap **CAN-PI-H / CAN-PI-L** on Orion CAN1 (same net as CANdapter / TSM2500), **not** the HyPer side of the BB-CANOP isolator — see [`schematic/wires.md`](../schematic/wires.md) §8.5
- PiCAN **120 Ω jumper open** (Orion + HyPer already terminate)
- Bitrate **250000** — ignore `500000` in the [PiCAN Python examples](https://github.com/skpang/PiCAN-Python-examples)

SocketCAN bring-up is done by **systemd-networkd**, not by the process.

## Dev (Mac)

```bash
cd dashboard
GOWORK=off go run ./cmd/dashboard --demo --listen :10000
```

## Build for Pi 5

```bash
cd dashboard
GOWORK=off GOOS=linux GOARCH=arm64 go build -o ih53ev-dashboard ./cmd/dashboard
```

## Install on Pi

Fresh [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) plus the official [Touch Display 2 10″](https://www.raspberrypi.com/products/touch-display-2/) (1200×1920). Connection steps: [Touch Display 2 docs](https://www.raspberrypi.com/documentation/accessories/touch-display-2.html). Vehicle wiring (PiCAN 3 SMPS, SW5, CAN tap): [`schematic/wires.md`](../schematic/wires.md) §11.

**PiCAN 3:** the HAT covers the same 5 V/GND pins the display pigtail uses. Use a stacking header and pick 5 V/GND off the top, or tap 5 V/GND on the PiCAN to display J1. In the truck, power from the PiCAN **3 A SMPS** only — do **not** also plug USB-C into the Pi. Leave USB empty.

Flash [Raspberry Pi OS](https://www.raspberrypi.com/software/) (64-bit, **desktop** — not Lite). Enable SSH in Imager customisation.

```bash
git clone https://github.com/scottfeldman/ih-53-ev.git
cd ih-53-ev/dashboard
sudo ./install.sh
sudo reboot
```

`install.sh` builds the dash, enables it on boot (fullscreen Chromium), and sets the panel to landscape plus medium-screen desktop chrome. Reboot is required so the PiCAN overlay can create `can0`; until then the app exits and the browser has nothing to open. After reboot, Chromium should come up fullscreen on its own. If the image is sideways the wrong way, change `DISPLAY_TRANSFORM` in `install.sh` from `90` (Left) to `270` (Right) and re-run.

## Flags

| Flag | Default | Meaning |
|------|---------|---------|
| `--iface` | `can0` | SocketCAN interface |
| `--listen` | `:10000` | HTTP bind |
| `--demo` | off | Synthetic state, no CAN |
| `--canmap` | auto | Orion + HyPer layout YAML |
| `--log-can` | off | Log every RX frame |

## Orion broadcasts (CAN1)

Telemetry is **push**, not OBD2 poll — so the laptop Orion utility can stay on CAN1 without fighting the dash.

Program custom messages in the Orion utility (**CANBUS Settings → Edit CANBUS Messages**) to match [`canmap.yaml`](canmap.yaml). Standard 11-bit IDs, **big-endian**, CAN1:

| ID | Rate | Contents |
|----|------|----------|
| `0x350` | 100 ms | SOC % (u8), pack V (u16 ×0.1), pack A (i16 ×0.1) |
| `0x351` | 100 ms | CCL, DCL (u16 A), high/low/avg temp (°C i8) |
| `0x352` | 500 ms | cell min/max (u16 ×0.0001 V), pack cycles, fault count |

**Cell broadcast** (all 30 taps): Orion utility → CANBUS Settings → **Enable Battery Cell Broadcast** on CAN1, ID **`0x36`** (matches `canmap.yaml`). Each frame is one tap: ID, instant V, IR + shunt bit, open V, checksum. The Detail page shows a **5×6** grid (modules × taps).

For Pack SOC in the utility, set **Then Divide By = 2** so the bus carries whole percent (matches `scale: 1` in the YAML).

The dash does **not** continuously use `0x7E3` / `0x7EB`. Those stay free for the CANdapter utility.

## HyPer X1 TPDOs

Program in TAU SmartView (do not add Node ID). See `hyper:` in [`canmap.yaml`](canmap.yaml): `0x190` / `0x191` / `0x192`.

## TSM2500

Listen-only status `0x18EB2440`. Never transmits `0x18E54024`.

## Commands from the dash?

| Action | On bus? | Notes |
|--------|---------|--------|
| Read SOC / V / A / temps / cells summary | No TX | Orion broadcasts |
| Read charger / X1 | No TX | Status / TPDOs |
| Set charge V/A | **Never** | Orion owns TSM2500 |
| Drive / throttle | **Never** | Analog throttle |
| Clear Orion DTCs | Optional TX | Mode `$04` once; unplug utility first |

Normal operation is **read-only**. Clear-faults is the only command worth keeping on the dash.

## Safety

- Stale sources show **NO DATA**, not the last good value
- Fault clear is POST + browser confirm + `confirm=yes`
- CANdapter and Pi share CAN1; OBD2 conflict only if you clear faults while the utility is live
