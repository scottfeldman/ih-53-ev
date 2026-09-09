package web

import (
	"bufio"
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	. "github.com/maragudk/gomponents"
	. "github.com/maragudk/gomponents/html"

	"github.com/sfeldma/ih-53-ev/dashboard/internal/orion"
	"github.com/sfeldma/ih-53-ev/dashboard/internal/state"
)

type Server struct {
	State *state.VehicleState
	Orion *orion.Clearer
	app   *fiber.App
}

func New(vs *state.VehicleState, oc *orion.Clearer) *Server {
	s := &Server{State: vs, Orion: oc}
	app := fiber.New(fiber.Config{
		DisableStartupMessage: false,
		AppName:               "IH-53 EV Dashboard",
	})
	app.Use(logger.New(logger.Config{
		Format: "${time} ${status} ${method} ${path} ${latency}\n",
	}))
	app.Get("/", s.handleDrive)
	app.Get("/charge", s.handleCharge)
	app.Get("/detail", s.handleDetail)
	app.Get("/partials/banner", s.handleBanner)
	app.Get("/partials/gauges", s.handleGauges)
	app.Get("/partials/charge", s.handleChargePartial)
	app.Get("/partials/detail", s.handleDetailPartial)
	app.Get("/events", s.handleSSE)
	app.Post("/api/clear-faults", s.handleClearFaults)
	app.Get("/static/htmx.min.js", s.handleHTMX)
	s.app = app
	return s
}

func (s *Server) Listen(addr string) error {
	return s.app.Listen(addr)
}

func (s *Server) Shutdown() error {
	return s.app.Shutdown()
}

func render(c *fiber.Ctx, n Node) error {
	c.Set("Content-Type", "text/html; charset=utf-8")
	var b []byte
	w := &byteWriter{}
	if err := n.Render(w); err != nil {
		return err
	}
	b = w.b
	return c.Send(b)
}

type byteWriter struct{ b []byte }

func (w *byteWriter) Write(p []byte) (int, error) {
	w.b = append(w.b, p...)
	return len(p), nil
}

func (s *Server) handleDrive(c *fiber.Ctx) error {
	return render(c, pageShell("Drive", "drive",
		Div(ID("banner"), Attr("hx-get", "/partials/banner"), Attr("hx-trigger", "load, every 400ms, sse:tick from:#sse"),
			Banner(s.State.Snapshot()),
		),
		Div(ID("gauges"), Attr("hx-get", "/partials/gauges"), Attr("hx-trigger", "load, every 400ms, sse:tick from:#sse"),
			DriveGauges(s.State.Snapshot()),
		),
	))
}

func (s *Server) handleCharge(c *fiber.Ctx) error {
	return render(c, pageShell("Charge", "charge",
		Div(ID("banner"), Attr("hx-get", "/partials/banner"), Attr("hx-trigger", "load, every 400ms"),
			Banner(s.State.Snapshot()),
		),
		Div(ID("gauges"), Attr("hx-get", "/partials/charge"), Attr("hx-trigger", "load, every 400ms"),
			ChargePanel(s.State.Snapshot()),
		),
	))
}

func (s *Server) handleDetail(c *fiber.Ctx) error {
	return render(c, pageShell("Detail", "detail",
		Div(ID("banner"), Attr("hx-get", "/partials/banner"), Attr("hx-trigger", "load, every 400ms"),
			Banner(s.State.Snapshot()),
		),
		Div(ID("gauges"), Attr("hx-get", "/partials/detail"), Attr("hx-trigger", "load, every 500ms"),
			DetailPanel(s.State.Snapshot()),
		),
	))
}

func (s *Server) handleBanner(c *fiber.Ctx) error {
	return render(c, Banner(s.State.Snapshot()))
}
func (s *Server) handleGauges(c *fiber.Ctx) error {
	return render(c, DriveGauges(s.State.Snapshot()))
}
func (s *Server) handleChargePartial(c *fiber.Ctx) error {
	return render(c, ChargePanel(s.State.Snapshot()))
}
func (s *Server) handleDetailPartial(c *fiber.Ctx) error {
	return render(c, DetailPanel(s.State.Snapshot()))
}

func (s *Server) handleClearFaults(c *fiber.Ctx) error {
	confirm := c.FormValue("confirm")
	if confirm != "yes" {
		return c.Status(http.StatusBadRequest).SendString("confirm=yes required")
	}
	if s.Orion != nil {
		s.Orion.RequestClearFaults()
	}
	return c.Redirect("/detail", http.StatusSeeOther)
}

var sseClientsMu sync.Mutex
var sseClients = map[chan struct{}]struct{}{}

func (s *Server) handleSSE(c *fiber.Ctx) error {
	c.Set("Content-Type", "text/event-stream")
	c.Set("Cache-Control", "no-cache")
	c.Set("Connection", "keep-alive")

	ch := make(chan struct{}, 1)
	sseClientsMu.Lock()
	sseClients[ch] = struct{}{}
	sseClientsMu.Unlock()
	defer func() {
		sseClientsMu.Lock()
		delete(sseClients, ch)
		sseClientsMu.Unlock()
	}()

	c.Context().SetBodyStreamWriter(func(w *bufio.Writer) {
		ticker := time.NewTicker(400 * time.Millisecond)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				_, _ = fmt.Fprintf(w, "event: tick\ndata: 1\n\n")
				if err := w.Flush(); err != nil {
					return
				}
			case <-ch:
				return
			}
		}
	})
	return nil
}

func (s *Server) handleHTMX(c *fiber.Ctx) error {
	c.Set("Content-Type", "application/javascript")
	return c.SendString(htmxMinJS)
}

func pageShell(title, active string, body ...Node) Node {
	nav := func(href, label, key string) Node {
		cls := "nav"
		if key == active {
			cls = "nav active"
		}
		return A(Href(href), Class(cls), Text(label))
	}
	return HTML(
		Lang("en"),
		Head(
			Meta(Charset("utf-8")),
			Meta(Name("viewport"), Content("width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no")),
			TitleEl(Text("IH-53 · "+title)),
			StyleEl(Type("text/css"), Raw(css)),
			Script(Src("/static/htmx.min.js"), Defer()),
		),
		Body(
			Div(ID("sse"), Attr("hx-ext", "sse"), Attr("sse-connect", "/events"), Style("display:none")),
			Header(
				Class("top"),
				H1(Text("IH-53 EV")),
				Nav(
					nav("/", "Drive", "drive"),
					nav("/charge", "Charge", "charge"),
					nav("/detail", "Detail", "detail"),
				),
			),
			Main(Class("content"), Group(body)),
		),
	)
}
