package canmap

import (
	"fmt"
	"os"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/hyper"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/orion"
	"gopkg.in/yaml.v3"
)

// File is the on-disk canmap.yaml (Orion broadcasts + HyPer TPDOs).
type File struct {
	Orion orion.BroadcastMap `yaml:"orion"`
	Hyper hyper.Map          `yaml:"hyper"`
}

func Load(path string) (*File, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var f File
	if err := yaml.Unmarshal(b, &f); err != nil {
		return nil, err
	}
	if err := f.Orion.Normalize(); err != nil {
		return nil, fmt.Errorf("orion: %w", err)
	}
	if err := f.Hyper.Normalize(); err != nil {
		return nil, fmt.Errorf("hyper: %w", err)
	}
	return &f, nil
}
