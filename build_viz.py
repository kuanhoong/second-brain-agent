"""Generate a single, offline `viz.html` — a force-directed graph of the OKF vault,
color-coded by trust signal (status). Open it in any browser; no server needed.

    python build_viz.py            # writes viz.html next to this script
    VAULT_DIR=/path/to/vault python build_viz.py

Colors:  stable = green,  draft = amber,  deprecated = grey,  index = blue.
A red ring marks notes past their stale_after date.
This stands in for Google's OKF static visualizer so the repo is self-contained.
"""
from __future__ import annotations

import json
from pathlib import Path

from archivist import okf

HTML = """<!doctype html>
<html><head><meta charset="utf-8"><title>Second Brain — Knowledge Graph</title>
<style>
  html,body{margin:0;height:100%;overflow:hidden;background:#171029;color:#EAE7FB;
    font:14px/1.4 -apple-system,Segoe UI,Roboto,sans-serif}
  #hud{position:fixed;top:14px;left:16px;z-index:2;pointer-events:none}
  #hud h1{font-size:16px;margin:0 0 8px}
  .key{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:#CFC8F5}
  .key span{display:flex;align-items:center;gap:6px}
  .dot{width:11px;height:11px;border-radius:50%;display:inline-block}
  text{fill:#EAE7FB;font-size:11px;pointer-events:none}
  line.link{stroke:#6C4BF6;stroke-opacity:.45}
  circle{cursor:grab}
</style></head><body>
<div id="hud"><h1>Second Brain — Knowledge Graph</h1>
<div class="key">
  <span><i class="dot" style="background:#34A853"></i>stable</span>
  <span><i class="dot" style="background:#FBBC04"></i>draft</span>
  <span><i class="dot" style="background:#7A7690"></i>deprecated</span>
  <span><i class="dot" style="background:#4285F4"></i>index</span>
  <span><i class="dot" style="background:#171029;border:2px solid #EC4899"></i>stale</span>
</div></div>
<svg id="g"></svg>
<script>
// Fully self-contained force-directed graph (no external libraries) so viz.html
// works offline anywhere.
const DATA = __DATA__;
const W = innerWidth, H = innerHeight, SVGNS = "http://www.w3.org/2000/svg";
const color = d => d.type === "Index" ? "#4285F4"
  : d.status === "deprecated" ? "#7A7690"
  : d.status === "draft" ? "#FBBC04" : "#34A853";

const nodes = DATA.nodes.map((n, i) => Object.assign({}, n, {
  x: W/2 + Math.cos(i) * 180 + (Math.random()-.5)*60,
  y: H/2 + Math.sin(i) * 180 + (Math.random()-.5)*60, vx: 0, vy: 0 }));
const byId = Object.fromEntries(nodes.map(n => [n.id, n]));
const links = DATA.links.map(l => ({ s: byId[l.source], t: byId[l.target] })).filter(l => l.s && l.t);

const svg = document.getElementById("g");
svg.setAttribute("width", W); svg.setAttribute("height", H);
const gl = document.createElementNS(SVGNS, "g"), gn = document.createElementNS(SVGNS, "g");
svg.append(gl, gn);
const lineEls = links.map(() => { const e = document.createElementNS(SVGNS,"line"); e.setAttribute("class","link"); gl.append(e); return e; });
const nodeEls = nodes.map(d => {
  const g = document.createElementNS(SVGNS, "g");
  const c = document.createElementNS(SVGNS, "circle");
  c.setAttribute("r", d.type === "Index" ? 7 : 11);
  c.setAttribute("fill", color(d));
  c.setAttribute("stroke", d.stale ? "#EC4899" : "#171029");
  c.setAttribute("stroke-width", d.stale ? 3 : 1.5);
  const t = document.createElementNS(SVGNS, "text");
  t.textContent = d.title; t.setAttribute("x", 15); t.setAttribute("y", 4);
  g.append(c, t); gn.append(g);
  enableDrag(c, d);
  return g;
});

function tick() {
  // repulsion
  for (let i = 0; i < nodes.length; i++) for (let j = i+1; j < nodes.length; j++) {
    const a = nodes[i], b = nodes[j];
    let dx = a.x-b.x, dy = a.y-b.y, dist = Math.hypot(dx,dy)||.01;
    const f = 5200 / (dist*dist); dx/=dist; dy/=dist;
    a.vx += dx*f; a.vy += dy*f; b.vx -= dx*f; b.vy -= dy*f;
  }
  // link springs
  for (const l of links) {
    let dx = l.t.x-l.s.x, dy = l.t.y-l.s.y, dist = Math.hypot(dx,dy)||.01;
    const f = (dist-95)*0.02; dx/=dist; dy/=dist;
    l.s.vx += dx*f; l.s.vy += dy*f; l.t.vx -= dx*f; l.t.vy -= dy*f;
  }
  // centering + integrate
  for (const n of nodes) {
    if (n.fx != null) { n.x = n.fx; n.y = n.fy; n.vx = n.vy = 0; continue; }
    n.vx += (W/2-n.x)*0.002; n.vy += (H/2-n.y)*0.002;
    n.vx *= 0.86; n.vy *= 0.86;
    n.x += n.vx; n.y += n.vy;
  }
  links.forEach((l,i) => { lineEls[i].setAttribute("x1",l.s.x); lineEls[i].setAttribute("y1",l.s.y); lineEls[i].setAttribute("x2",l.t.x); lineEls[i].setAttribute("y2",l.t.y); });
  nodes.forEach((n,i) => nodeEls[i].setAttribute("transform", `translate(${n.x},${n.y})`));
  requestAnimationFrame(tick);
}
tick();

function enableDrag(circle, d) {
  circle.addEventListener("mousedown", e => {
    e.preventDefault(); d.fx = d.x; d.fy = d.y;
    const move = ev => { d.fx = ev.clientX; d.fy = ev.clientY; };
    const up = () => { d.fx = d.fy = null; window.removeEventListener("mousemove", move); window.removeEventListener("mouseup", up); };
    window.addEventListener("mousemove", move); window.addEventListener("mouseup", up);
  });
}
</script></body></html>
"""


def main() -> None:
    data = okf.graph()
    out = Path(__file__).resolve().parent / "viz.html"
    out.write_text(HTML.replace("__DATA__", json.dumps(data)), encoding="utf-8")
    print(f"Wrote {out}  ({len(data['nodes'])} nodes, {len(data['links'])} links)")


if __name__ == "__main__":
    main()
