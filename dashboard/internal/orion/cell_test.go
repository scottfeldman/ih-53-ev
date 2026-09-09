package orion

import (
	"testing"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

func TestEncodeDecodeCellBroadcast(t *testing.T) {
	const id = 0x36
	in := state.CellTap{
		ID: 22, VoltageV: 4.0500, OpenVoltageV: 4.0600,
		ResistancemOhm: 1.25, Shunting: true,
	}
	data := EncodeCellBroadcast(id, in)
	out, ok := DecodeCellBroadcast(id, data)
	if !ok {
		t.Fatal("decode failed")
	}
	if out.ID != 22 {
		t.Errorf("id=%d", out.ID)
	}
	if out.VoltageV < 4.049 || out.VoltageV > 4.051 {
		t.Errorf("V=%v", out.VoltageV)
	}
	if !out.Shunting {
		t.Error("expected shunt")
	}
	if out.ResistancemOhm < 1.2 || out.ResistancemOhm > 1.3 {
		t.Errorf("IR=%v", out.ResistancemOhm)
	}
}

func TestCellBroadcastBadChecksum(t *testing.T) {
	data := EncodeCellBroadcast(0x36, state.CellTap{ID: 1, VoltageV: 3.95})
	data[7] ^= 0xFF
	if _, ok := DecodeCellBroadcast(0x36, data); ok {
		t.Fatal("bad checksum should fail")
	}
}

func TestDecoderAppliesCellBroadcast(t *testing.T) {
	m := testBroadcastMap(t)
	d := NewDecoder(m)
	vs := &state.VehicleState{}
	for i := 0; i < 30; i++ {
		c := state.CellTap{ID: uint8(i), VoltageV: 3.90 + float64(i)*0.001, OpenVoltageV: 3.91}
		f := canbus.Frame{ID: 0x36, Data: EncodeCellBroadcast(0x36, c)}
		if !d.Apply(vs, f) {
			t.Fatalf("apply cell %d", i)
		}
	}
	snap := vs.Snapshot()
	if len(snap.Orion.Cells) != 30 {
		t.Fatalf("cells=%d", len(snap.Orion.Cells))
	}
	if snap.Orion.CellModules != 5 || snap.Orion.CellTaps != 6 {
		t.Errorf("layout %d×%d", snap.Orion.CellModules, snap.Orion.CellTaps)
	}
	if snap.Orion.CellMinV > snap.Orion.CellMaxV {
		t.Errorf("min/max inverted")
	}
	if snap.Orion.Cells[0].VoltageV < 3.89 {
		t.Errorf("cell0=%v", snap.Orion.Cells[0].VoltageV)
	}
}
