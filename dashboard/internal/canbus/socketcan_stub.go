//go:build !linux

package canbus

import "fmt"

func openSocketCAN(iface string) (Bus, error) {
	return nil, fmt.Errorf("%w (iface=%s); use --demo on non-Linux hosts", ErrNotSocketCAN, iface)
}
