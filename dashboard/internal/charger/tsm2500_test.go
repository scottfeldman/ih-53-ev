package charger

import (
	"encoding/binary"
	"testing"
)

func TestDecodeStatusCharging(t *testing.T) {
	data := make([]byte, 8)
	// no errors in byte1
	data[0] = 0x00
	// battery connected (bits 3-2 = 00), charging (bits 1-0 = 00)
	data[1] = 0x00
	binary.LittleEndian.PutUint16(data[2:4], 1180) // 118.0 V
	binary.LittleEndian.PutUint16(data[4:6], 32015) // 32015*0.1 - 3200 = 1.5 A
	data[6] = 80 // 40 °C

	cs, err := DecodeStatus(data)
	if err != nil {
		t.Fatal(err)
	}
	if !cs.Charging {
		t.Error("expected charging")
	}
	if !cs.BatteryConn {
		t.Error("expected battery connected")
	}
	if cs.OutputV < 117.9 || cs.OutputV > 118.1 {
		t.Errorf("OutputV=%v", cs.OutputV)
	}
	if cs.OutputA < 1.4 || cs.OutputA > 1.6 {
		t.Errorf("OutputA=%v", cs.OutputA)
	}
	if cs.TempC != 40 {
		t.Errorf("TempC=%v", cs.TempC)
	}
}

func TestDecodeStatusErrors(t *testing.T) {
	data := make([]byte, 8)
	// high temp protect (bits 7-6 = 01), hardware err (bits 3-2 = 01)
	data[0] = 0x44 // 01 00 01 00
	// no battery (bits 3-2 = 01), not charging (bits 1-0 = 01)
	data[1] = 0x05
	binary.LittleEndian.PutUint16(data[2:4], 0)
	binary.LittleEndian.PutUint16(data[4:6], 32000) // 0 A
	data[6] = 40 // 0 °C

	cs, err := DecodeStatus(data)
	if err != nil {
		t.Fatal(err)
	}
	if !cs.HighTempProt {
		t.Error("expected high temp protect")
	}
	if !cs.HardwareError {
		t.Error("expected hardware error")
	}
	if cs.Charging {
		t.Error("expected not charging")
	}
	if cs.BatteryConn {
		t.Error("expected no battery")
	}
}

func TestDecodeShort(t *testing.T) {
	_, err := DecodeStatus([]byte{1, 2, 3})
	if err == nil {
		t.Fatal("expected error")
	}
}
