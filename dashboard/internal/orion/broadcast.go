package orion

import (
	"encoding/binary"
	"fmt"
	"time"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

const (
	DefaultCellBroadcastID = 0x36
	DefaultCellCount       = 30 // 5 Tesla modules × 6 taps
)

// Field is one value in a custom Orion broadcast frame.
type Field struct {
	Name  string  `yaml:"name"`
	Byte  int     `yaml:"byte"`
	Type  string  `yaml:"type"` // u8, i8, u16, i16
	Scale float64 `yaml:"scale"`
	Add   float64 `yaml:"add"`
	Unit  string  `yaml:"unit"`
}

// Message is one programmable Orion CAN broadcast.
type Message struct {
	ID     uint32  `yaml:"id"`
	RateMS int     `yaml:"rate_ms"`
	Endian string  `yaml:"endian"` // be (default) or le
	Fields []Field `yaml:"fields"`
}

// CellBroadcast is Orion's sequential Battery Cell Broadcast Message.
// Enable in Orion utility → CANBUS Settings → Enable Battery Cell Broadcast.
type CellBroadcast struct {
	ID        uint32 `yaml:"id"`
	CellCount int    `yaml:"cell_count"`
	Modules   int    `yaml:"modules"`
	Taps      int    `yaml:"taps_per_module"`
}

// BroadcastMap is the orion: section of canmap.yaml.
type BroadcastMap struct {
	Messages       []Message     `yaml:"messages"`
	CellBroadcast  CellBroadcast `yaml:"cell_broadcast"`
	StaleTimeoutMS int           `yaml:"stale_timeout_ms"`
}

func (m *BroadcastMap) Normalize() error {
	if m.StaleTimeoutMS == 0 {
		m.StaleTimeoutMS = 2000
	}
	if m.CellBroadcast.ID == 0 {
		m.CellBroadcast.ID = DefaultCellBroadcastID
	}
	if m.CellBroadcast.Modules == 0 {
		m.CellBroadcast.Modules = 5
	}
	if m.CellBroadcast.Taps == 0 {
		m.CellBroadcast.Taps = 6
	}
	if m.CellBroadcast.CellCount == 0 {
		m.CellBroadcast.CellCount = m.CellBroadcast.Modules * m.CellBroadcast.Taps
	}
	for i := range m.Messages {
		msg := &m.Messages[i]
		if msg.ID == 0 {
			return fmt.Errorf("message %d: missing id", i)
		}
		if msg.Endian == "" {
			msg.Endian = "be"
		}
		if msg.Endian != "be" && msg.Endian != "le" {
			return fmt.Errorf("message 0x%X: endian must be be or le", msg.ID)
		}
		for j := range msg.Fields {
			f := &msg.Fields[j]
			if f.Scale == 0 {
				f.Scale = 1
			}
		}
	}
	return nil
}

// Decoder applies Orion custom broadcasts and cell broadcast frames.
type Decoder struct {
	byID     map[uint32]Message
	cellID   uint32
	cellN    int
	modules  int
	taps     int
}

func NewDecoder(m *BroadcastMap) *Decoder {
	d := &Decoder{
		byID:    make(map[uint32]Message, len(m.Messages)),
		cellID:  m.CellBroadcast.ID,
		cellN:   m.CellBroadcast.CellCount,
		modules: m.CellBroadcast.Modules,
		taps:    m.CellBroadcast.Taps,
	}
	for _, msg := range m.Messages {
		d.byID[msg.ID] = msg
	}
	return d
}

func (d *Decoder) Apply(vs *state.VehicleState, f canbus.Frame) bool {
	if f.Ext {
		return false
	}
	if f.ID == d.cellID {
		return d.applyCellBroadcast(vs, f)
	}
	msg, ok := d.byID[f.ID]
	if !ok {
		return false
	}
	vals := make(map[string]float64, len(msg.Fields))
	for _, field := range msg.Fields {
		v, err := readField(f.Data, field, msg.Endian)
		if err != nil {
			return false
		}
		vals[field.Name] = v
	}
	now := time.Now()
	vs.UpdateOrion(func(o *state.OrionState) {
		if v, ok := vals["soc_pct"]; ok {
			o.SOCPct = v
		}
		if v, ok := vals["pack_v"]; ok {
			o.PackV = v
		}
		if v, ok := vals["pack_a"]; ok {
			o.PackA = v
		}
		if v, ok := vals["ccl"]; ok {
			o.CCL = v
		}
		if v, ok := vals["dcl"]; ok {
			o.DCL = v
		}
		if v, ok := vals["high_temp_c"]; ok {
			o.HighTempC = v
		}
		if v, ok := vals["low_temp_c"]; ok {
			o.LowTempC = v
		}
		if v, ok := vals["avg_temp_c"]; ok {
			o.AvgTempC = v
		}
		if v, ok := vals["cell_min_v"]; ok {
			o.CellMinV = v
		}
		if v, ok := vals["cell_max_v"]; ok {
			o.CellMaxV = v
			o.CellDeltaV = o.CellMaxV - o.CellMinV
		}
		if v, ok := vals["pack_cycles"]; ok {
			o.PackCycles = v
		}
		if v, ok := vals["fault_count"]; ok {
			o.FaultCount = int(v)
		}
		o.SeenAt = now
	})
	return true
}

func (d *Decoder) applyCellBroadcast(vs *state.VehicleState, f canbus.Frame) bool {
	cell, ok := DecodeCellBroadcast(d.cellID, f.Data)
	if !ok {
		return false
	}
	if int(cell.ID) >= d.cellN {
		return false
	}
	now := time.Now()
	vs.UpdateOrion(func(o *state.OrionState) {
		ensureCells(o, d.cellN, d.modules, d.taps)
		idx := int(cell.ID)
		o.Cells[idx] = cell
		o.Cells[idx].SeenAt = now
		o.CellsSeenAt = now
		recomputeCellSummary(o)
		// Cell traffic also proves BMS is alive even if custom msgs lag.
		if o.SeenAt.IsZero() || now.After(o.SeenAt) {
			o.SeenAt = now
		}
	})
	return true
}

func ensureCells(o *state.OrionState, n, modules, taps int) {
	if len(o.Cells) != n {
		o.Cells = make([]state.CellTap, n)
		for i := range o.Cells {
			o.Cells[i].ID = uint8(i)
		}
	}
	o.CellModules = modules
	o.CellTaps = taps
}

func recomputeCellSummary(o *state.OrionState) {
	var minV, maxV float64
	have := false
	for _, c := range o.Cells {
		if c.SeenAt.IsZero() || c.VoltageV < 0.5 {
			continue
		}
		if !have {
			minV, maxV = c.VoltageV, c.VoltageV
			have = true
			continue
		}
		if c.VoltageV < minV {
			minV = c.VoltageV
		}
		if c.VoltageV > maxV {
			maxV = c.VoltageV
		}
	}
	if !have {
		return
	}
	o.CellMinV = minV
	o.CellMaxV = maxV
	o.CellDeltaV = maxV - minV
}

// DecodeCellBroadcast parses one Orion Battery Cell Broadcast frame.
// Format (big-endian words): cell ID, instant V (0.1 mV), IR (0.01 mΩ) with
// MSB of byte3 = shunting, open V (0.1 mV), checksum.
// Checksum = (canID + 8 + sum(bytes[0:7])) & 0xFF
func DecodeCellBroadcast(canID uint32, data []byte) (state.CellTap, bool) {
	if len(data) < 8 {
		return state.CellTap{}, false
	}
	sum := int(canID) + 8
	for i := 0; i < 7; i++ {
		sum += int(data[i])
	}
	if byte(sum&0xFF) != data[7] {
		return state.CellTap{}, false
	}
	id := data[0]
	inst := binary.BigEndian.Uint16(data[1:3])
	irWord := binary.BigEndian.Uint16(data[3:5])
	shunting := data[3]&0x80 != 0
	irRaw := irWord & 0x7FFF
	openV := binary.BigEndian.Uint16(data[5:7])
	return state.CellTap{
		ID:             id,
		VoltageV:       float64(inst) * 0.0001, // 0.1 mV
		OpenVoltageV:   float64(openV) * 0.0001,
		ResistancemOhm: float64(irRaw) * 0.01,
		Shunting:       shunting,
	}, true
}

// EncodeCellBroadcast builds a frame for tests (valid checksum).
func EncodeCellBroadcast(canID uint32, cell state.CellTap) []byte {
	data := make([]byte, 8)
	data[0] = cell.ID
	binary.BigEndian.PutUint16(data[1:3], uint16(cell.VoltageV/0.0001+0.5))
	ir := uint16(cell.ResistancemOhm/0.01 + 0.5)
	if ir > 0x7FFF {
		ir = 0x7FFF
	}
	if cell.Shunting {
		ir |= 0x8000
	}
	binary.BigEndian.PutUint16(data[3:5], ir)
	binary.BigEndian.PutUint16(data[5:7], uint16(cell.OpenVoltageV/0.0001+0.5))
	sum := int(canID) + 8
	for i := 0; i < 7; i++ {
		sum += int(data[i])
	}
	data[7] = byte(sum & 0xFF)
	return data
}

func readField(data []byte, f Field, endian string) (float64, error) {
	be := endian != "le"
	switch f.Type {
	case "u8":
		if f.Byte >= len(data) {
			return 0, fmt.Errorf("%s: short", f.Name)
		}
		return float64(data[f.Byte])*f.Scale + f.Add, nil
	case "i8":
		if f.Byte >= len(data) {
			return 0, fmt.Errorf("%s: short", f.Name)
		}
		return float64(int8(data[f.Byte]))*f.Scale + f.Add, nil
	case "u16":
		if f.Byte+1 >= len(data) {
			return 0, fmt.Errorf("%s: short", f.Name)
		}
		var raw uint16
		if be {
			raw = binary.BigEndian.Uint16(data[f.Byte : f.Byte+2])
		} else {
			raw = binary.LittleEndian.Uint16(data[f.Byte : f.Byte+2])
		}
		return float64(raw)*f.Scale + f.Add, nil
	case "i16":
		if f.Byte+1 >= len(data) {
			return 0, fmt.Errorf("%s: short", f.Name)
		}
		var raw uint16
		if be {
			raw = binary.BigEndian.Uint16(data[f.Byte : f.Byte+2])
		} else {
			raw = binary.LittleEndian.Uint16(data[f.Byte : f.Byte+2])
		}
		return float64(int16(raw))*f.Scale + f.Add, nil
	default:
		return 0, fmt.Errorf("%s: unknown type %q", f.Name, f.Type)
	}
}
