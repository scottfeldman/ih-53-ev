package charger

import (
	"encoding/binary"
	"fmt"
	"time"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

// StatusID is the default TSM2500 status extended ID (from charger → bus).
const StatusID = 0x18EB2440

// ControlID is the BMS→charger setpoint frame. Dashboard must NEVER transmit this.
const ControlID = 0x18E54024

// DecodeStatus parses a TSM2500 status frame into ChargerState fields.
// Protocol (EVWest / Thunderstruck):
//
//	BYTE1 bits: high-temp, input-voltage err, hardware, communication
//	BYTE2 bits: battery connect, start/charging
//	BYTE3-4: output voltage * 0.1 V (LE)
//	BYTE5-6: output current = raw*0.1 - 3200 A (LE)
//	BYTE7: temperature °C with -40 offset
func DecodeStatus(data []byte) (state.ChargerState, error) {
	if len(data) < 7 {
		return state.ChargerState{}, fmt.Errorf("tsm2500 status: need ≥7 bytes, got %d", len(data))
	}
	b1 := data[0]
	b2 := data[1]
	cs := state.ChargerState{
		HighTempProt:    (b1>>6)&0x03 == 0x01,
		InputVoltageErr: (b1>>4)&0x03 == 0x01,
		HardwareError:   (b1>>2)&0x03 == 0x01,
		CommError:       (b1)&0x03 == 0x01,
		BatteryConn:     (b2>>2)&0x03 == 0x00, // 00 = connected
		Charging:        (b2)&0x03 == 0x00,    // 00 = charging
		SeenAt:          time.Now(),
	}
	vRaw := binary.LittleEndian.Uint16(data[2:4])
	cs.OutputV = float64(vRaw) * 0.1
	iRaw := binary.LittleEndian.Uint16(data[4:6])
	cs.OutputA = float64(iRaw)*0.1 - 3200.0
	cs.TempC = float64(data[6]) - 40.0
	return cs, nil
}

// Apply updates VehicleState from a received frame if it is a TSM status ID.
func Apply(vs *state.VehicleState, f canbus.Frame) bool {
	if !f.Ext || f.ID != StatusID {
		return false
	}
	cs, err := DecodeStatus(f.Data)
	if err != nil {
		return false
	}
	vs.UpdateCharger(func(c *state.ChargerState) { *c = cs })
	return true
}
