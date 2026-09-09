package hyper

import (
	"encoding/binary"
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
	"gopkg.in/yaml.v3"
)

func testMap(t *testing.T) *Map {
	t.Helper()
	_, file, _, _ := runtime.Caller(0)
	path := filepath.Join(filepath.Dir(file), "..", "..", "canmap.yaml")
	b, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	var root struct {
		Hyper Map `yaml:"hyper"`
	}
	if err := yaml.Unmarshal(b, &root); err != nil {
		t.Fatal(err)
	}
	if err := root.Hyper.Normalize(); err != nil {
		t.Fatal(err)
	}
	return &root.Hyper
}

func TestLoadAndDecodeTPDO190(t *testing.T) {
	d := NewDecoder(testMap(t))
	vs := &state.VehicleState{}

	data := make([]byte, 8)
	binary.LittleEndian.PutUint16(data[0:2], uint16(int16(1850)))
	data[2] = 35
	data[5] = 88
	data[6] = 82

	if !d.Apply(vs, canbus.Frame{ID: 0x190, Data: data}) {
		t.Fatal("expected apply")
	}
	snap := vs.Snapshot()
	if snap.Hyper.MotorRPM != 1850 {
		t.Errorf("rpm=%v", snap.Hyper.MotorRPM)
	}
	if snap.Hyper.InverterTempC != 48 {
		t.Errorf("invTemp=%v", snap.Hyper.InverterTempC)
	}
}

func TestDecodeTPDO191(t *testing.T) {
	d := NewDecoder(testMap(t))
	vs := &state.VehicleState{}
	data := make([]byte, 8)
	binary.LittleEndian.PutUint16(data[0:2], uint16(int16(1178)))
	binary.LittleEndian.PutUint16(data[2:4], uint16(int16(415)))
	binary.LittleEndian.PutUint16(data[4:6], 1<<9)

	if !d.Apply(vs, canbus.Frame{ID: 0x191, Data: data}) {
		t.Fatal("apply")
	}
	h := vs.Snapshot().Hyper
	if h.DCBusV < 117.7 || h.DCBusV > 117.9 {
		t.Errorf("V=%v", h.DCBusV)
	}
}

func TestUnknownID(t *testing.T) {
	d := NewDecoder(testMap(t))
	vs := &state.VehicleState{}
	if d.Apply(vs, canbus.Frame{ID: 0x999, Data: make([]byte, 8)}) {
		t.Fatal("should ignore unknown id")
	}
}
