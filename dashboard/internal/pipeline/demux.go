package pipeline

import (
	"context"
	"log"
	"time"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/charger"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/hyper"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/orion"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

// Demux runs the receive loop and routes frames to decoders.
type Demux struct {
	Bus    canbus.Bus
	State  *state.VehicleState
	Orion  *orion.Decoder
	Clear  *orion.Clearer
	Hyper  *hyper.Decoder
	LogAll bool
}

func (d *Demux) Run(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
		}
		f, err := d.Bus.Receive()
		if err != nil {
			select {
			case <-ctx.Done():
				return
			default:
			}
			log.Printf("can rx: %v", err)
			time.Sleep(100 * time.Millisecond)
			continue
		}
		if d.LogAll {
			log.Printf("can %s", canbus.FormatFrame(f))
		}
		if d.Clear != nil && d.Clear.HandleFrame(f) {
			continue
		}
		if d.Orion != nil && d.Orion.Apply(d.State, f) {
			continue
		}
		if charger.Apply(d.State, f) {
			continue
		}
		if d.Hyper != nil {
			_ = d.Hyper.Apply(d.State, f)
		}
	}
}
