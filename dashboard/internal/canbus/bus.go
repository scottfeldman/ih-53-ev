package canbus

import (
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"sync"
)

// Frame is a SocketCAN-compatible CAN frame.
type Frame struct {
	ID   uint32
	Data []byte
	Ext  bool // 29-bit extended ID
}

const (
	canEFFFlag = 0x80000000 // extended frame format
	canRTRFlag = 0x40000000
	canERRFlag = 0x20000000
	canEFFMask = 0x1FFFFFFF
	canSFFMask = 0x000007FF
)

// Bus is the SocketCAN (or demo stub) interface.
type Bus interface {
	Receive() (Frame, error)
	Send(Frame) error
	Close() error
}

// StubBus is an in-memory bus for --demo / tests.
type StubBus struct {
	mu   sync.Mutex
	rx   chan Frame
	done chan struct{}
}

func NewStubBus() *StubBus {
	return &StubBus{
		rx:   make(chan Frame, 64),
		done: make(chan struct{}),
	}
}

func (b *StubBus) Receive() (Frame, error) {
	select {
	case f := <-b.rx:
		return f, nil
	case <-b.done:
		return Frame{}, io.EOF
	}
}

func (b *StubBus) Send(f Frame) error {
	select {
	case <-b.done:
		return io.EOF
	default:
		// OBD2 replies are not simulated on stub; demo mode skips CAN.
		return nil
	}
}

func (b *StubBus) Inject(f Frame) {
	select {
	case b.rx <- f:
	default:
	}
}

func (b *StubBus) Close() error {
	select {
	case <-b.done:
	default:
		close(b.done)
	}
	return nil
}

// EncodeCANID packs ID + extended flag into SocketCAN can_id.
func EncodeCANID(id uint32, ext bool) uint32 {
	if ext {
		return (id & canEFFMask) | canEFFFlag
	}
	return id & canSFFMask
}

// DecodeCANID unpacks SocketCAN can_id.
func DecodeCANID(canID uint32) (id uint32, ext bool) {
	ext = canID&canEFFFlag != 0
	if ext {
		return canID & canEFFMask, true
	}
	return canID & canSFFMask, false
}

// FrameFromRaw builds a Frame from SocketCAN wire fields.
func FrameFromRaw(canID uint32, data []byte) Frame {
	id, ext := DecodeCANID(canID)
	d := make([]byte, len(data))
	copy(d, data)
	return Frame{ID: id, Data: d, Ext: ext}
}

// PackData pads/truncates to at most 8 bytes.
func PackData(b []byte) [8]byte {
	var out [8]byte
	n := len(b)
	if n > 8 {
		n = 8
	}
	copy(out[:], b[:n])
	return out
}

var ErrNotSocketCAN = errors.New("socketcan only available on linux")

// Open opens a SocketCAN interface (linux) or returns ErrNotSocketCAN.
func Open(iface string) (Bus, error) {
	return openSocketCAN(iface)
}

// MustEncode helpers for tests.
func U16BE(v uint16) []byte {
	b := make([]byte, 2)
	binary.BigEndian.PutUint16(b, v)
	return b
}

func I16LE(v int16) []byte {
	b := make([]byte, 2)
	binary.LittleEndian.PutUint16(b, uint16(v))
	return b
}

func FormatFrame(f Frame) string {
	kind := "S"
	if f.Ext {
		kind = "E"
	}
	return fmt.Sprintf("%s %03X [%d] %X", kind, f.ID, len(f.Data), f.Data)
}
