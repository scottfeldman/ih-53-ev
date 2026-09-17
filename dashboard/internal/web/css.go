package web

const css = `
:root {
  --bg: #000000;
  --card: #151b24;
  --text: #e8eef7;
  --muted: #8b9bb0;
  --accent: #3ddc97;
  --warn: #f0c14a;
  --fault: #ff5c5c;
  --charge: #4da3ff;
  --bar: #243041;
}
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  background: var(--bg); color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
  min-height: 100%;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}
.top {
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
  gap: 12px; padding: 16px 20px; border-bottom: 1px solid #1f2a38;
  position: sticky; top: 0; background: #000; z-index: 10;
}
.top h1 { margin: 0; font-size: 1.4rem; letter-spacing: 0.04em; }
nav { display: flex; gap: 8px; }
.nav {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 48px; min-width: 88px; padding: 10px 18px;
  border-radius: 12px; text-decoration: none; color: var(--text);
  background: var(--card); font-weight: 600; font-size: 1.05rem;
}
.nav.active { background: #243246; outline: 2px solid var(--accent); }
.content { padding: 16px 20px 32px; max-width: 900px; margin: 0 auto; }
.banners { display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; }
.banner {
  padding: 14px 16px; border-radius: 14px; font-weight: 700;
  font-size: 1.15rem; letter-spacing: 0.03em; text-align: center;
}
.banner.ok { background: #123528; color: var(--accent); }
.banner.warn { background: #3a2e10; color: var(--warn); }
.banner.fault { background: #3a1212; color: var(--fault); }
.banner.charge { background: #10253a; color: var(--charge); }
.gauges { display: flex; flex-direction: column; gap: 14px; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.card {
  background: var(--card); border-radius: 18px; padding: 16px 18px;
  min-height: 110px;
}
.card.wide { width: 100%; }
.card.soc .big { font-size: 4rem; line-height: 1; margin: 8px 0 14px; }
.big { font-size: 2.4rem; font-weight: 700; }
.biggish { font-size: 1.35rem; font-weight: 600; }
.nodata { color: var(--fault); }
.label { color: var(--muted); font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.06em; }
.line { font-size: 1.25rem; margin-top: 8px; font-weight: 600; }
.sub { color: var(--muted); margin-top: 8px; font-size: 1.05rem; }
.bar { height: 22px; background: var(--bar); border-radius: 999px; overflow: hidden; }
.fill { height: 100%; background: linear-gradient(90deg, #2bb673, var(--accent)); }
.health-row { display: flex; flex-wrap: wrap; gap: 16px; padding: 8px 4px; color: var(--muted); }
.health { display: inline-flex; align-items: center; gap: 6px; font-size: 0.95rem; }
.dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.dot.ok { background: var(--accent); }
.dot.bad { background: var(--fault); }
.dtc { font-size: 1.2rem; margin: 10px 0; padding-left: 1.2em; }
.btn {
  min-height: 52px; min-width: 160px; padding: 12px 20px; border: 0; border-radius: 14px;
  font-size: 1.1rem; font-weight: 700; cursor: pointer;
}
.btn.danger { background: var(--fault); color: #1a0505; }
.clear-form { margin-top: 12px; }
.note { color: var(--muted); font-size: 0.95rem; margin-top: 8px; }
.cell-empty { margin-top: 12px; color: var(--warn); font-size: 1.05rem; }
.cell-grid { display: flex; flex-direction: column; gap: 8px; margin-top: 14px; }
.cell-row {
  display: grid;
  grid-template-columns: 40px repeat(6, minmax(0, 1fr)) 48px;
  gap: 6px; align-items: stretch;
}
.cell-mod {
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; color: var(--muted); font-size: 0.9rem;
}
.cell {
  position: relative;
  min-height: 48px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.95rem; font-weight: 700; font-variant-numeric: tabular-nums;
  background: #1c2533;
}
.cell.mid { background: #1a3a2c; }
.cell.cool { background: #1a2a3a; color: #9ec5ff; }
.cell.warm { background: #3a2e14; color: #ffd27a; }
.cell.lo { outline: 2px solid var(--charge); }
.cell.hi { outline: 2px solid var(--warn); }
.cell.stale { color: #5a6a7a; background: #121820; font-weight: 500; }
.cell.shunt::after {
  content: ""; position: absolute; top: 6px; right: 6px;
  width: 8px; height: 8px; border-radius: 50%; background: var(--accent);
}
.cell-delta {
  display: flex; align-items: center; justify-content: flex-end;
  font-size: 0.85rem; color: var(--muted); font-variant-numeric: tabular-nums;
}
@media (max-width: 600px) {
  .row { grid-template-columns: 1fr; }
  .card.soc .big { font-size: 3.2rem; }
  .cell { font-size: 0.8rem; min-height: 42px; }
  .cell-row { grid-template-columns: 28px repeat(6, minmax(0, 1fr)) 36px; gap: 4px; }
}
`
