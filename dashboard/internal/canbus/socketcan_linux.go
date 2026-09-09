//go:build linux

package canbus

import (
	"encoding/binary"
	"fmt"
	"net"
	"os"
	"syscall"
	"unsafe"
)

const (
	afCAN       = 29
	pfCAN       = 29
	sockRaw     = 3
	canRaw      = 1
	canMTU      = 16
	solCANRaw   = 101
	canRawFilter = 1
)

type sockaddrCAN struct {
	Family  uint16
	IfIndex int32
	_       [8]byte
}

type socketBus struct {
	fd   int
	name string
}

func openSocketCAN(iface string) (Bus, error) {
	ifi, err := net.InterfaceByName(iface)
	if err != nil {
		return nil, fmt.Errorf("can interface %q: %w", iface, err)
	}
	fd, err := syscall.Socket(afCAN, sockRaw, canRaw)
	if err != nil {
		return nil, fmt.Errorf("socket can: %w", err)
	}
	addr := sockaddrCAN{
		Family:  afCAN,
		IfIndex: int32(ifi.Index),
	}
	_, _, errno := syscall.Syscall(
		syscall.SYS_BIND,
		uintptr(fd),
		uintptr(unsafe.Pointer(&addr)),
		unsafe.Sizeof(addr),
	)
	if errno != 0 {
		syscall.Close(fd)
		return nil, fmt.Errorf("bind %s: %w", iface, errno)
	}
	return &socketBus{fd: fd, name: iface}, nil
}

func (b *socketBus) Receive() (Frame, error) {
	buf := make([]byte, canMTU)
	n, err := syscall.Read(b.fd, buf)
	if err != nil {
		return Frame{}, err
	}
	if n < 8 {
		return Frame{}, fmt.Errorf("short can frame: %d", n)
	}
	canID := binary.LittleEndian.Uint32(buf[0:4])
	dlc := int(buf[4] & 0x0F)
	if dlc > 8 {
		dlc = 8
	}
	if n < 8+dlc {
		dlc = n - 8
	}
	data := make([]byte, dlc)
	copy(data, buf[8:8+dlc])
	return FrameFromRaw(canID, data), nil
}

func (b *socketBus) Send(f Frame) error {
	buf := make([]byte, canMTU)
	binary.LittleEndian.PutUint32(buf[0:4], EncodeCANID(f.ID, f.Ext))
	dlc := len(f.Data)
	if dlc > 8 {
		dlc = 8
	}
	buf[4] = byte(dlc)
	copy(buf[8:], f.Data[:dlc])
	_, err := syscall.Write(b.fd, buf)
	return err
}

func (b *socketBus) Close() error {
	return syscall.Close(b.fd)
}

// Ensure we can open /dev for diagnostics if needed.
var _ = os.Open
