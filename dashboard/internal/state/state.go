package state

import (
	"sync"
	"time"
)

const (
	OrionStale   = 2 * time.Second
	ChargerStale = 2 * time.Second
	HyperStale   = 1 * time.Second
)

// VehicleState holds the latest decoded telemetry from the CAN bus.
type VehicleState struct {
	mu sync.RWMutex

	orion   OrionState
	charger ChargerState
	hyper   HyperState
	updated time.Time
}

// Snapshot is a mutex-free copy for UI / readers.
type Snapshot struct {
	Orion     OrionState
	Charger   ChargerState
	Hyper     HyperState
	UpdatedAt time.Time
}

type OrionState struct {
	SOCPct       float64
	PackV        float64
	PackA        float64
	CCL          float64
	DCL          float64
	HighTempC    float64
	LowTempC     float64
	AvgTempC     float64
	PackCycles   float64
	CellMinV     float64
	CellMaxV     float64
	CellDeltaV   float64
	Cells        []CellTap // per-tap from Orion cell broadcast (30 = 5×6)
	CellModules  int
	CellTaps     int
	CellsSeenAt  time.Time
	FaultCount   int
	DTCs         []string
	SeenAt       time.Time
	FaultsSeenAt time.Time
}

// CellTap is one Orion voltage-sense group (Tesla module tap).
type CellTap struct {
	ID             uint8
	VoltageV       float64
	OpenVoltageV   float64
	ResistancemOhm float64
	Shunting       bool
	SeenAt         time.Time
}

func (c CellTap) Fresh(maxAge time.Duration) bool {
	return !c.SeenAt.IsZero() && time.Since(c.SeenAt) <= maxAge
}

func (o OrionState) Stale() bool {
	return o.SeenAt.IsZero() || time.Since(o.SeenAt) > OrionStale
}

func (o OrionState) PackKW() float64 {
	return o.PackV * o.PackA / 1000.0
}

type ChargerState struct {
	OutputV         float64
	OutputA         float64
	TempC           float64
	Charging        bool
	BatteryConn     bool
	CommError       bool
	HardwareError   bool
	InputVoltageErr bool
	HighTempProt    bool
	SeenAt          time.Time
}

func (c ChargerState) Stale() bool {
	return c.SeenAt.IsZero() || time.Since(c.SeenAt) > ChargerStale
}

type HyperState struct {
	MotorRPM      float64
	ThrottlePct   float64
	FaultCode     uint8
	FaultLevel    uint8
	InverterTempC float64
	MotorTempC    float64
	DCBusV        float64
	DCBusA        float64
	SystemFlags   uint16
	SpeedMPH      float64
	KeySwitchV    float64
	SeenAt        time.Time
}

func (h HyperState) Stale() bool {
	return h.SeenAt.IsZero() || time.Since(h.SeenAt) > HyperStale
}

func (h HyperState) HasFault() bool {
	return h.FaultCode != 0
}

func (s *VehicleState) Snapshot() Snapshot {
	s.mu.RLock()
	defer s.mu.RUnlock()
	out := Snapshot{
		Orion:     s.orion,
		Charger:   s.charger,
		Hyper:     s.hyper,
		UpdatedAt: s.updated,
	}
	if s.orion.Cells != nil {
		out.Orion.Cells = append([]CellTap(nil), s.orion.Cells...)
	}
	if s.orion.DTCs != nil {
		out.Orion.DTCs = append([]string(nil), s.orion.DTCs...)
	}
	return out
}

func (s *VehicleState) UpdateOrion(fn func(*OrionState)) {
	s.mu.Lock()
	defer s.mu.Unlock()
	fn(&s.orion)
	s.updated = time.Now()
}

func (s *VehicleState) UpdateCharger(fn func(*ChargerState)) {
	s.mu.Lock()
	defer s.mu.Unlock()
	fn(&s.charger)
	s.updated = time.Now()
}

func (s *VehicleState) UpdateHyper(fn func(*HyperState)) {
	s.mu.Lock()
	defer s.mu.Unlock()
	fn(&s.hyper)
	s.updated = time.Now()
}

func (s Snapshot) AnyFault() bool {
	if !s.Orion.Stale() && (s.Orion.FaultCount > 0 || len(s.Orion.DTCs) > 0) {
		return true
	}
	if !s.Charger.Stale() && (s.Charger.CommError || s.Charger.HardwareError || s.Charger.HighTempProt) {
		return true
	}
	if !s.Hyper.Stale() && s.Hyper.HasFault() {
		return true
	}
	return false
}

func (s Snapshot) IsCharging() bool {
	if !s.Charger.Stale() && s.Charger.Charging {
		return true
	}
	if !s.Orion.Stale() && s.Orion.PackA < -1.0 {
		return true
	}
	return false
}

// Demo fills synthetic live data for Mac UI development (--demo).
func (s *VehicleState) Demo() {
	now := time.Now()
	s.mu.Lock()
	defer s.mu.Unlock()
	cells := make([]CellTap, 30)
	var minV, maxV float64
	for i := range cells {
		v := 3.95 + float64(i%6)*0.01 - float64(i/6)*0.005
		if i == 3 {
			v = 3.90 // pack low
		}
		if i == 22 {
			v = 4.05 // pack high
		}
		cells[i] = CellTap{
			ID: uint8(i), VoltageV: v, OpenVoltageV: v + 0.01,
			ResistancemOhm: 0.8 + float64(i%5)*0.05, SeenAt: now,
		}
		if i == 22 {
			cells[i].Shunting = true
		}
		if i == 0 || v < minV {
			minV = v
		}
		if i == 0 || v > maxV {
			maxV = v
		}
	}
	s.orion = OrionState{
		SOCPct:       72.5,
		PackV:        118.4,
		PackA:        42.0,
		CCL:          20.0,
		DCL:          400.0,
		HighTempC:    28,
		LowTempC:     24,
		AvgTempC:     26,
		PackCycles:   12,
		CellMinV:     minV,
		CellMaxV:     maxV,
		CellDeltaV:   maxV - minV,
		Cells:        cells,
		CellModules:  5,
		CellTaps:     6,
		CellsSeenAt:  now,
		DTCs:         nil,
		SeenAt:       now,
		FaultsSeenAt: now,
	}
	s.charger = ChargerState{
		OutputV: 0, OutputA: 0, TempC: 35,
		Charging: false, BatteryConn: true,
		SeenAt: now.Add(-3 * time.Second),
	}
	s.hyper = HyperState{
		MotorRPM: 1850, ThrottlePct: 35, FaultCode: 0, FaultLevel: 0,
		InverterTempC: 48, MotorTempC: 42,
		DCBusV: 117.8, DCBusA: 41.5, SystemFlags: 1 << 9,
		SpeedMPH: 28.4, KeySwitchV: 12.6,
		SeenAt: now,
	}
	s.updated = now
}
