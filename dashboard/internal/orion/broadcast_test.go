package orion

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

func testBroadcastMap(t *testing.T) *BroadcastMap {
	t.Helper()
	_, file, _, _ := runtime.Caller(0)
	path := filepath.Join(filepath.Dir(file), "..", "..", "canmap.yaml")
	b, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	var root struct {
		Orion BroadcastMap `yaml:"orion"`
	}
	if err := yaml.Unmarshal(b, &root); err != nil {
		t.Fatal(err)
	}
	if err := root.Orion.Normalize(); err != nil {
		t.Fatal(err)
	}
	return &root.Orion
}

func TestBroadcastDrive(t *testing.T) {
	d := NewDecoder(testBroadcastMap(t))
	vs := &state.VehicleState{}
	data := make([]byte, 8)
	data[0] = 73
	binary.BigEndian.PutUint16(data[1:3], 1184)
	binary.BigEndian.PutUint16(data[3:5], uint16(int16(420)))

	if !d.Apply(vs, canbus.Frame{ID: 0x350, Data: data}) {
		t.Fatal("apply")
	}
	o := vs.Snapshot().Orion
	if o.SOCPct != 73 {
		t.Errorf("SOC=%v", o.SOCPct)
	}
	if o.PackV < 118.3 || o.PackV > 118.5 {
		t.Errorf("V=%v", o.PackV)
	}
	if o.PackA != 42 {
		t.Errorf("A=%v", o.PackA)
	}
}

func TestBroadcastLimitsAndFaults(t *testing.T) {
	d := NewDecoder(testBroadcastMap(t))
	vs := &state.VehicleState{}

	lim := make([]byte, 8)
	binary.BigEndian.PutUint16(lim[0:2], 20)
	binary.BigEndian.PutUint16(lim[2:4], 400)
	lim[4], lim[5], lim[6] = 28, 24, 26
	if !d.Apply(vs, canbus.Frame{ID: 0x351, Data: lim}) {
		t.Fatal("351")
	}

	sum := make([]byte, 8)
	binary.BigEndian.PutUint16(sum[0:2], 39200)
	binary.BigEndian.PutUint16(sum[2:4], 40100)
	binary.BigEndian.PutUint16(sum[4:6], 12)
	sum[6] = 2
	if !d.Apply(vs, canbus.Frame{ID: 0x352, Data: sum}) {
		t.Fatal("352")
	}

	o := vs.Snapshot().Orion
	if o.CCL != 20 || o.DCL != 400 {
		t.Errorf("limits CCL=%v DCL=%v", o.CCL, o.DCL)
	}
	if o.FaultCount != 2 {
		t.Errorf("faults=%d", o.FaultCount)
	}
	if !vs.Snapshot().AnyFault() {
		t.Error("expected AnyFault")
	}
}

func TestUnknownID(t *testing.T) {
	d := NewDecoder(testBroadcastMap(t))
	vs := &state.VehicleState{}
	if d.Apply(vs, canbus.Frame{ID: 0x7E3, Data: make([]byte, 8)}) {
		t.Fatal("must ignore OBD2 IDs")
	}
}
