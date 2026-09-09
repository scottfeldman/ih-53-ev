package main

import (
	"context"
	"flag"
	"log"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/canbus"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/canmap"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/hyper"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/orion"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/pipeline"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/web"
)

func main() {
	iface := flag.String("iface", "can0", "SocketCAN interface (use vcan0 for testing)")
	listen := flag.String("listen", ":10000", "HTTP listen address")
	demo := flag.Bool("demo", false, "Synthetic telemetry; no CAN (Mac/dev UI)")
	canmapPath := flag.String("canmap", "", "Path to canmap.yaml (default: beside binary or ./canmap.yaml)")
	logAll := flag.Bool("log-can", false, "Log every received CAN frame")
	flag.Parse()

	vs := &state.VehicleState{}
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()

	var clearer *orion.Clearer
	mapPath := *canmapPath
	if mapPath == "" {
		mapPath = findCanmap()
	}

	if *demo {
		log.Printf("demo mode: synthetic state, no CAN")
		vs.Demo()
		go func() {
			t := time.NewTicker(500 * time.Millisecond)
			defer t.Stop()
			for {
				select {
				case <-ctx.Done():
					return
				case <-t.C:
					vs.Demo()
				}
			}
		}()
	} else {
		bus, err := canbus.Open(*iface)
		if err != nil {
			log.Fatalf("open %s: %v (use --demo on non-Linux)", *iface, err)
		}
		defer bus.Close()

		cm, err := canmap.Load(mapPath)
		if err != nil {
			log.Fatalf("canmap %s: %v", mapPath, err)
		}
		od := orion.NewDecoder(&cm.Orion)
		hd := hyper.NewDecoder(&cm.Hyper)
		clearer = orion.NewClearer(bus, vs)
		clearer.Start()
		defer clearer.Stop()

		demux := &pipeline.Demux{
			Bus:    bus,
			State:  vs,
			Orion:  od,
			Clear:  clearer,
			Hyper:  hd,
			LogAll: *logAll,
		}
		go demux.Run(ctx)
		log.Printf("can %s @ 250 kbps: Orion+HyPer listen-only; clear-DTC is sole TX", *iface)
	}

	srv := web.New(vs, clearer)
	go func() {
		<-ctx.Done()
		_ = srv.Shutdown()
	}()

	log.Printf("IH-53 dashboard http://0.0.0.0%s", *listen)
	if err := srv.Listen(*listen); err != nil {
		log.Printf("server stopped: %v", err)
	}
}

func findCanmap() string {
	candidates := []string{
		"canmap.yaml",
		filepath.Join("dashboard", "canmap.yaml"),
	}
	if exe, err := os.Executable(); err == nil {
		candidates = append([]string{filepath.Join(filepath.Dir(exe), "canmap.yaml")}, candidates...)
	}
	for _, c := range candidates {
		if _, err := os.Stat(c); err == nil {
			return c
		}
	}
	return "canmap.yaml"
}
