package orion

import (
	"fmt"
	"sync"
	"time"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

const (
	DefaultECUID  = 0x7E3
	DefaultRespID = 0x7EB
)

// Clearer sends a one-shot OBD2 Mode $04 clear-DTC when requested.
// Telemetry is broadcast-only; this is the only dash TX on CAN1.
// Do not use while the Orion utility is connected (shared OBD2 ECU).
type Clearer struct {
	bus    canbus.Bus
	ecuID  uint32
	respID uint32
	vs     *state.VehicleState

	mu      sync.Mutex
	pending chan []byte
	clearReq chan struct{}
	stop    chan struct{}
	wg      sync.WaitGroup
}

func NewClearer(bus canbus.Bus, vs *state.VehicleState) *Clearer {
	return &Clearer{
		bus:      bus,
		ecuID:    DefaultECUID,
		respID:   DefaultRespID,
		vs:       vs,
		pending:  make(chan []byte, 1),
		clearReq: make(chan struct{}, 1),
		stop:     make(chan struct{}),
	}
}

// HandleFrame accepts OBD2 replies for an in-flight clear.
func (c *Clearer) HandleFrame(f canbus.Frame) bool {
	if f.Ext || f.ID != c.respID || len(f.Data) < 1 {
		return false
	}
	c.mu.Lock()
	defer c.mu.Unlock()
	select {
	case c.pending <- append([]byte(nil), f.Data...):
	default:
	}
	return true
}

func (c *Clearer) RequestClearFaults() {
	select {
	case c.clearReq <- struct{}{}:
	default:
	}
}

func (c *Clearer) Start() {
	c.wg.Add(1)
	go func() {
		defer c.wg.Done()
		for {
			select {
			case <-c.stop:
				return
			case <-c.clearReq:
				_ = c.clearFaults()
			}
		}
	}()
}

func (c *Clearer) Stop() {
	close(c.stop)
	c.wg.Wait()
}

func (c *Clearer) clearFaults() error {
	select {
	case <-c.pending:
	default:
	}
	req := []byte{0x01, 0x04, 0, 0, 0, 0, 0, 0}
	if err := c.bus.Send(canbus.Frame{ID: c.ecuID, Data: req, Ext: false}); err != nil {
		return err
	}
	deadline := time.After(500 * time.Millisecond)
	for {
		select {
		case <-c.stop:
			return fmt.Errorf("stopped")
		case <-deadline:
			return fmt.Errorf("orion clear-faults timeout")
		case data := <-c.pending:
			if len(data) < 2 {
				continue
			}
			// Single-frame: [len][44…]
			if data[0]>>4 == 0 && len(data) > 1 && data[1] == 0x44 {
				c.vs.UpdateOrion(func(o *state.OrionState) {
					o.DTCs = nil
					o.FaultCount = 0
					o.FaultsSeenAt = time.Now()
				})
				return nil
			}
		}
	}
}
