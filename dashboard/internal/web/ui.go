package web

import (
	"fmt"
	"time"

	. "github.com/maragudk/gomponents"
	. "github.com/maragudk/gomponents/html"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

func Banner(s state.Snapshot) Node {
	var parts []Node
	if s.AnyFault() {
		parts = append(parts, Div(Class("banner fault"), Text("FAULT — check Detail")))
	}
	if s.IsCharging() {
		parts = append(parts, Div(Class("banner charge"), Text("CHARGING")))
	}
	if s.Orion.Stale() {
		parts = append(parts, Div(Class("banner warn"), Text("BMS NO DATA")))
	}
	if s.Hyper.Stale() {
		parts = append(parts, Div(Class("banner warn"), Text("X1 NO DATA")))
	}
	if !s.Orion.Stale() && !s.AnyFault() && !s.IsCharging() {
		parts = append(parts, Div(Class("banner ok"), Text("READY")))
	}
	if len(parts) == 0 {
		parts = append(parts, Div(Class("banner ok"), Text("OK")))
	}
	return Div(Class("banners"), Group(parts))
}

func DriveGauges(s state.Snapshot) Node {
	return Div(Class("gauges"),
		socCard(s),
		Div(Class("row"),
			metric("Pack", fmtPower(s), fmtVolt(s.Orion.PackV, s.Orion.Stale()), fmtAmp(s.Orion.PackA, s.Orion.Stale())),
			metric("Limits",
				fmtVal("DCL", s.Orion.DCL, "A", s.Orion.Stale()),
				fmtVal("CCL", s.Orion.CCL, "A", s.Orion.Stale()),
				fmtTempRange(s),
			),
		),
		Div(Class("row"),
			metric("Motor",
				fmtRPM(s),
				fmtVal("Thr", s.Hyper.ThrottlePct, "%", s.Hyper.Stale()),
				fmtSpeed(s),
			),
			metric("Temps",
				fmtVal("Inv", s.Hyper.InverterTempC, "°C", s.Hyper.Stale()),
				fmtVal("Mot", s.Hyper.MotorTempC, "°C", s.Hyper.Stale()),
				fmtVal("Pack", s.Orion.AvgTempC, "°C", s.Orion.Stale()),
			),
		),
		busHealth(s),
	)
}

func ChargePanel(s state.Snapshot) Node {
	ch := s.Charger
	stale := ch.Stale()
	status := "OFFLINE"
	if !stale {
		if ch.Charging {
			status = "CHARGING"
		} else {
			status = "IDLE"
		}
	}
	flags := []string{}
	if !stale {
		if ch.CommError {
			flags = append(flags, "COMM ERR")
		}
		if ch.HardwareError {
			flags = append(flags, "HW ERR")
		}
		if ch.InputVoltageErr {
			flags = append(flags, "AC ERR")
		}
		if ch.HighTempProt {
			flags = append(flags, "HOT")
		}
		if !ch.BatteryConn {
			flags = append(flags, "NO BATT")
		}
	}
	flagText := "—"
	if len(flags) > 0 {
		flagText = ""
		for i, f := range flags {
			if i > 0 {
				flagText += " · "
			}
			flagText += f
		}
	}

	return Div(Class("gauges"),
		Div(Class("card wide"),
			Div(Class("label"), Text("Charger status")),
			Div(Class("big"), Text(status)),
			Div(Class("sub"), Text(flagText)),
		),
		Div(Class("row"),
			metric("Output",
				fmtVal("V", ch.OutputV, "V", stale),
				fmtVal("A", ch.OutputA, "A", stale),
				fmtVal("Temp", ch.TempC, "°C", stale),
			),
			metric("BMS",
				fmtVal("SOC", s.Orion.SOCPct, "%", s.Orion.Stale()),
				fmtVal("CCL", s.Orion.CCL, "A", s.Orion.Stale()),
				fmtVal("Pack", s.Orion.PackV, "V", s.Orion.Stale()),
			),
		),
		P(Class("note"), Text("Orion is charge master. Dashboard does not set charger voltage/current.")),
	)
}

func DetailPanel(s state.Snapshot) Node {
	faultLine := "NO DATA"
	if !s.Orion.Stale() {
		if s.Orion.FaultCount == 0 && len(s.Orion.DTCs) == 0 {
			faultLine = "No active faults (broadcast count = 0)"
		} else if s.Orion.FaultCount > 0 {
			faultLine = fmt.Sprintf("Active fault count: %d (see Orion utility for codes)", s.Orion.FaultCount)
		} else {
			faultLine = "Faults cleared"
		}
	}

	summary := "NO DATA"
	if !s.Orion.Stale() && (s.Orion.CellMinV > 0 || s.Orion.CellMaxV > 0 || len(s.Orion.Cells) > 0) {
		summary = fmt.Sprintf("min %.3f V · max %.3f V · Δ %.0f mV",
			s.Orion.CellMinV, s.Orion.CellMaxV, s.Orion.CellDeltaV*1000)
	}

	x1Fault := "none"
	if !s.Hyper.Stale() && s.Hyper.HasFault() {
		x1Fault = fmt.Sprintf("code %d level %d", s.Hyper.FaultCode, s.Hyper.FaultLevel)
	} else if s.Hyper.Stale() {
		x1Fault = "NO DATA"
	}

	return Div(Class("gauges"),
		Div(Class("card wide"),
			Div(Class("label"), Text("Cell taps (5 × 6)")),
			Div(Class("sub biggish"), Text(summary)),
			cellGrid(s),
			P(Class("note"), Text("Orion cell IDs 0–29 in tap order. Highlight = pack min/max. Dot = balancing (shunt).")),
		),
		Div(Class("card wide"),
			Div(Class("label"), Text("Orion faults")),
			Div(Class("sub biggish"), Text(faultLine)),
			P(Class("note"), Text("Dash is listen-only for telemetry. Clear uses a one-shot OBD2 Mode $04 — unplug the Orion utility first.")),
			Form(Method("post"), Action("/api/clear-faults"), Class("clear-form"),
				Input(Type("hidden"), Name("confirm"), Value("yes")),
				Button(Type("submit"), Class("btn danger"),
					Attr("onclick", "return confirm('Clear Orion fault codes? Unplug CANdapter utility first.');"),
					Text("Clear faults"),
				),
			),
		),
		Div(Class("row"),
			metric("Charger bits",
				Text(chargerBits(s)),
			),
			metric("X1",
				Text("Fault: "+x1Fault),
				Br(),
				Text(fmt.Sprintf("Flags: 0x%04X", s.Hyper.SystemFlags)),
			),
		),
	)
}

func cellGrid(s state.Snapshot) Node {
	modules := s.Orion.CellModules
	taps := s.Orion.CellTaps
	if modules == 0 {
		modules = 5
	}
	if taps == 0 {
		taps = 6
	}
	cells := s.Orion.Cells
	if len(cells) == 0 {
		return Div(Class("cell-empty"), Text("Waiting for Orion cell broadcast (enable ID 0x36 on CAN1)…"))
	}

	packMin, packMax := s.Orion.CellMinV, s.Orion.CellMaxV
	rows := make([]Node, 0, modules)
	for m := 0; m < modules; m++ {
		tapsNodes := make([]Node, 0, taps+2)
		tapsNodes = append(tapsNodes, Div(Class("cell-mod"), Text(fmt.Sprintf("M%d", m+1))))
		modMin, modMax := 0.0, 0.0
		modHave := false
		for t := 0; t < taps; t++ {
			idx := m*taps + t
			cls := "cell"
			label := "—"
			title := fmt.Sprintf("cell %d", idx)
			if idx < len(cells) {
				c := cells[idx]
				if c.Fresh(3*time.Second) && c.VoltageV >= 0.5 {
					label = fmt.Sprintf("%.3f", c.VoltageV)
					title = fmt.Sprintf("#%d  %.3f V  OCV %.3f V  %.2f mΩ",
						c.ID, c.VoltageV, c.OpenVoltageV, c.ResistancemOhm)
					if c.Shunting {
						cls += " shunt"
						title += "  SHUNT"
					}
					if packMin > 0 && c.VoltageV <= packMin+0.0005 {
						cls += " lo"
					}
					if packMax > 0 && c.VoltageV >= packMax-0.0005 {
						cls += " hi"
					}
					mid := (packMin + packMax) / 2
					span := packMax - packMin
					if span < 0.01 {
						span = 0.01
					}
					switch {
					case c.VoltageV < mid-span*0.15:
						cls += " cool"
					case c.VoltageV > mid+span*0.15:
						cls += " warm"
					default:
						cls += " mid"
					}
					if !modHave || c.VoltageV < modMin {
						modMin = c.VoltageV
					}
					if !modHave || c.VoltageV > modMax {
						modMax = c.VoltageV
					}
					modHave = true
				} else {
					cls += " stale"
				}
			} else {
				cls += " stale"
			}
			tapsNodes = append(tapsNodes, Div(Class(cls), Title(title), Text(label)))
		}
		if modHave {
			tapsNodes = append(tapsNodes, Div(Class("cell-delta"),
				Text(fmt.Sprintf("Δ%.0f", (modMax-modMin)*1000))))
		} else {
			tapsNodes = append(tapsNodes, Div(Class("cell-delta"), Text("")))
		}
		rows = append(rows, Div(Class("cell-row"), Group(tapsNodes)))
	}
	return Div(Class("cell-grid"), Group(rows))
}

func socCard(s state.Snapshot) Node {
	if s.Orion.Stale() {
		return Div(Class("card soc"),
			Div(Class("label"), Text("State of charge")),
			Div(Class("big nodata"), Text("NO DATA")),
		)
	}
	pct := s.Orion.SOCPct
	if pct < 0 {
		pct = 0
	}
	if pct > 100 {
		pct = 100
	}
	return Div(Class("card soc"),
		Div(Class("label"), Text("State of charge")),
		Div(Class("big"), Text(fmt.Sprintf("%.0f%%", pct))),
		Div(Class("bar"),
			Div(Class("fill"), Style(fmt.Sprintf("width:%.1f%%", pct))),
		),
	)
}

func metric(title string, lines ...Node) Node {
	kids := []Node{Div(Class("label"), Text(title))}
	for _, n := range lines {
		kids = append(kids, Div(Class("line"), n))
	}
	return Div(Class("card"), Group(kids))
}

func busHealth(s state.Snapshot) Node {
	dot := func(name string, stale bool) Node {
		cls := "dot ok"
		label := "live"
		if stale {
			cls = "dot bad"
			label = "stale"
		}
		return Span(Class("health"),
			Span(Class(cls)),
			Text(" "+name+" "+label),
		)
	}
	return Div(Class("health-row"),
		dot("BMS", s.Orion.Stale()),
		dot("CHG", s.Charger.Stale()),
		dot("X1", s.Hyper.Stale()),
	)
}

func fmtPower(s state.Snapshot) Node {
	if s.Orion.Stale() {
		return Text("NO DATA")
	}
	return Text(fmt.Sprintf("%.1f kW", s.Orion.PackKW()))
}

func fmtVolt(v float64, stale bool) Node {
	if stale {
		return Text("— V")
	}
	return Text(fmt.Sprintf("%.1f V", v))
}

func fmtAmp(a float64, stale bool) Node {
	if stale {
		return Text("— A")
	}
	return Text(fmt.Sprintf("%.1f A", a))
}

func fmtVal(label string, v float64, unit string, stale bool) Node {
	if stale {
		return Text(label + ": NO DATA")
	}
	return Text(fmt.Sprintf("%s: %.1f %s", label, v, unit))
}

func fmtTempRange(s state.Snapshot) Node {
	if s.Orion.Stale() {
		return Text("Temp: NO DATA")
	}
	return Text(fmt.Sprintf("T: %.0f…%.0f °C", s.Orion.LowTempC, s.Orion.HighTempC))
}

func fmtRPM(s state.Snapshot) Node {
	if s.Hyper.Stale() {
		return Text("RPM: NO DATA")
	}
	return Text(fmt.Sprintf("%.0f RPM", s.Hyper.MotorRPM))
}

func fmtSpeed(s state.Snapshot) Node {
	if s.Hyper.Stale() {
		return Text("SPD: NO DATA")
	}
	return Text(fmt.Sprintf("%.1f mph", s.Hyper.SpeedMPH))
}

func chargerBits(s state.Snapshot) string {
	if s.Charger.Stale() {
		return "NO DATA"
	}
	c := s.Charger
	return fmt.Sprintf("chg=%v batt=%v comm=%v hw=%v hot=%v",
		c.Charging, c.BatteryConn, c.CommError, c.HardwareError, c.HighTempProt)
}
