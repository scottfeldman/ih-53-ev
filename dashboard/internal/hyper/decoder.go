package hyper

import (
	"encoding/binary"
	"fmt"
	"time"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

// Field describes one value packed into a TPDO payload.
type Field struct {
	Name  string  `yaml:"name"`
	Byte  int     `yaml:"byte"`
	Type  string  `yaml:"type"` // u8, i16, u16
	Scale float64 `yaml:"scale"`
	Add   float64 `yaml:"add"`
	Unit  string  `yaml:"unit"`
}

// TPDO is one configurable transmit PDO.
type TPDO struct {
	ID     uint32  `yaml:"id"`
	RateMS int     `yaml:"rate_ms"`
	Fields []Field `yaml:"fields"`
}

// Map is the hyper: section of canmap.yaml.
type Map struct {
	TPDOs          []TPDO `yaml:"tpdos"`
	StaleTimeoutMS int    `yaml:"stale_timeout_ms"`
}

func (m *Map) Normalize() error {
	if m.StaleTimeoutMS == 0 {
		m.StaleTimeoutMS = 1000
	}
	for i := range m.TPDOs {
		if m.TPDOs[i].ID == 0 {
			return fmt.Errorf("tpdo %d: missing id", i)
		}
		for j := range m.TPDOs[i].Fields {
			f := &m.TPDOs[i].Fields[j]
			if f.Scale == 0 {
				f.Scale = 1
			}
		}
	}
	return nil
}

// Decoder applies HyPer TPDO layouts to VehicleState.
type Decoder struct {
	byID map[uint32]TPDO
}

func NewDecoder(m *Map) *Decoder {
	d := &Decoder{byID: make(map[uint32]TPDO, len(m.TPDOs))}
	for _, t := range m.TPDOs {
		d.byID[t.ID] = t
	}
	return d
}

func (d *Decoder) Apply(vs *state.VehicleState, f canbus.Frame) bool {
	tpdo, ok := d.byID[f.ID]
	if !ok {
		return false
	}
	vals := make(map[string]float64, len(tpdo.Fields))
	for _, field := range tpdo.Fields {
		v, err := readField(f.Data, field)
		if err != nil {
			return false
		}
		vals[field.Name] = v
	}
	now := time.Now()
	vs.UpdateHyper(func(h *state.HyperState) {
		if v, ok := vals["motor_rpm"]; ok {
			h.MotorRPM = v
		}
		if v, ok := vals["throttle_pct"]; ok {
			h.ThrottlePct = v
		}
		if v, ok := vals["fault_code"]; ok {
			h.FaultCode = uint8(v)
		}
		if v, ok := vals["fault_level"]; ok {
			h.FaultLevel = uint8(v)
		}
		if v, ok := vals["inverter_temp_c"]; ok {
			h.InverterTempC = v
		}
		if v, ok := vals["motor_temp_c"]; ok {
			h.MotorTempC = v
		}
		if v, ok := vals["dc_bus_v"]; ok {
			h.DCBusV = v
		}
		if v, ok := vals["dc_bus_a"]; ok {
			h.DCBusA = v
		}
		if v, ok := vals["system_flags"]; ok {
			h.SystemFlags = uint16(v)
		}
		if v, ok := vals["vehicle_speed_mph"]; ok {
			h.SpeedMPH = v
		}
		if v, ok := vals["key_switch_v"]; ok {
			h.KeySwitchV = v
		}
		h.SeenAt = now
	})
	return true
}

func readField(data []byte, f Field) (float64, error) {
	switch f.Type {
	case "u8":
		if f.Byte >= len(data) {
			return 0, fmt.Errorf("%s: short frame", f.Name)
		}
		return float64(data[f.Byte])*f.Scale + f.Add, nil
	case "i16":
		if f.Byte+1 >= len(data) {
			return 0, fmt.Errorf("%s: short frame", f.Name)
		}
		raw := int16(binary.LittleEndian.Uint16(data[f.Byte : f.Byte+2]))
		return float64(raw)*f.Scale + f.Add, nil
	case "u16":
		if f.Byte+1 >= len(data) {
			return 0, fmt.Errorf("%s: short frame", f.Name)
		}
		raw := binary.LittleEndian.Uint16(data[f.Byte : f.Byte+2])
		return float64(raw)*f.Scale + f.Add, nil
	default:
		return 0, fmt.Errorf("%s: unknown type %q", f.Name, f.Type)
	}
}
