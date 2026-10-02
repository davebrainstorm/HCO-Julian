/* Groundwork · field map renderer (canvas). Uses window.GW_FIELD and colour tokens from tokens.css. */
(function () {
  "use strict";
  var AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
  function dec(s) { var a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = AL.indexOf(s[i]); return a; }
  function tok(n) { return getComputedStyle(document.documentElement).getPropertyValue("--hco-" + n).trim(); }
  function rgb(h) { h = h.replace("#", ""); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function ramp(stops, t) { t = Math.max(0, Math.min(1, t)) * (stops.length - 1); var i = Math.floor(t), j = Math.min(i + 1, stops.length - 1), f = t - i, a = stops[i], b = stops[j]; return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]; }
  function mixc(a, b, f) { return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]; }
  var LAYERS = {
    vigour: { name: "Vegetation index", short: "Vigour", src: "ndvi", dom: [0.15, 0.9], ramp: "vigour", fmt: function (v) { return v.toFixed(2); }, ticks: ["0.15", "0.50", "0.90"], note: "NDVI-style index from red and near-infrared bands" },
    redge: { name: "Red-edge index", short: "Red edge", src: "ndre", dom: [0.05, 0.55], ramp: "vigour", fmt: function (v) { return v.toFixed(2); }, ticks: ["0.05", "0.30", "0.55"], note: "NDRE-style index from red-edge and near-infrared bands" },
    elevation: { name: "Relative elevation", short: "Elevation", src: "elev", dom: [0, 1], ramp: "terrain", fmt: function (v, d) { return Math.round(v * d.elev_range_m) + " m"; }, ticks: ["0 m", "19 m", "38 m"], note: "Relative to the lowest point on the property" },
    land: { name: "Land use", short: "Land", src: null, note: "Paddocks, tracks, water and structures" }
  };
  function FieldMap(root, opts) {
    opts = opts || {};
    var D = window.GW_FIELD, W = D.w, H = D.h, self = this;
    var vals = { ndvi: dec(D.ndvi), ndre: dec(D.ndre), elev: dec(D.elev) };
    function real(src, i) { var r = src === "ndvi" ? D.ndvi_range : src === "ndre" ? D.ndre_range : [0, 1]; return r[0] + vals[src][i] / 63 * (r[1] - r[0]); }
    var wrap = document.createElement("div"); wrap.style.position = "relative";
    var cv = document.createElement("canvas"), ctx = cv.getContext("2d");
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.style.cssText = "position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible";
    var tip = document.createElement("div"); tip.className = "gw-map__tip";
    wrap.appendChild(cv); wrap.appendChild(svg); root.appendChild(wrap); root.appendChild(tip);
    this.layer = opts.layer || "vigour"; this.threshold = null; this.active = null; this.root = root;
    var cell = 8, colours = {}, prev = null;
    function readColours() {
      colours.vigour = []; colours.terrain = [];
      for (var i = 0; i < 9; i++) { colours.vigour.push(rgb(tok("vigour-" + i))); colours.terrain.push(rgb(tok("terrain-" + i))); }
      colours.water = rgb(tok("map-water")); colours.waterEdge = rgb(tok("map-water-edge")); colours.bg = rgb(tok("stone-975"));
      colours.track = rgb(tok("stone-600")); colours.structure = rgb(tok("stone-300")); colours.field = rgb(tok("stone-800")); colours.pasture = rgb(tok("stone-850")); colours.lichen = rgb(tok("lichen"));
    }
    function cellColour(i, layer) {
      var c = D.cls[i];
      if (c === "w") return colours.water; if (c === "b") return colours.structure;
      if (layer === "land") return c === "t" ? colours.track : c === "f" ? colours.field : colours.pasture;
      var L = LAYERS[layer], v = real(L.src, i), t = (v - L.dom[0]) / (L.dom[1] - L.dom[0]);
      var col = ramp(colours[L.ramp], t);
      if (self.threshold != null && L.src !== "elev") { if (v >= self.threshold) col = mixc(col, colours.bg, 0.72); }
      return col;
    }
    function size() {
      var w = root.clientWidth || 800; cell = Math.max(3, Math.floor(w / W)); var dpr = Math.min(2, window.devicePixelRatio || 1);
      cv.width = W * cell * dpr; cv.height = H * cell * dpr; cv.style.width = "100%"; cv.style.height = "auto"; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function paint(layer, x0, x1) {
      var seam = cell >= 6;
      for (var y = 0; y < H; y++) for (var x = x0; x < x1; x++) {
        var i = y * W + x, c = cellColour(i, layer);
        if (seam) { ctx.fillStyle = "rgb(" + (c[0] * .84 | 0) + "," + (c[1] * .84 | 0) + "," + (c[2] * .84 | 0) + ")"; ctx.fillRect(x * cell, y * cell, cell, cell); }
        ctx.fillStyle = "rgb(" + (c[0] | 0) + "," + (c[1] | 0) + "," + (c[2] | 0) + ")"; ctx.fillRect(x * cell, y * cell, cell - (seam ? 1 : 0), cell - (seam ? 1 : 0));
      }
    }
    function draw(animate) {
      var bg = colours.bg; ctx.fillStyle = "rgb(" + bg.join(",") + ")"; ctx.fillRect(0, 0, W * cell, H * cell);
      var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!animate || reduce || prev == null) { paint(self.layer, 0, W); return; }
      paint(prev, 0, W);
      var t0 = performance.now(), dur = 720, done = 0;
      (function step(now) {
        var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3), to = Math.round(e * W);
        if (to > done) { paint(self.layer, done, to); done = to; }
        if (p < 1) { var lc = colours.lichen; ctx.fillStyle = "rgba(" + lc.join(",") + ",.9)"; ctx.fillRect(to * cell, 0, 2, H * cell); requestAnimationFrame(step); }
        else paint(self.layer, Math.max(0, W - 2), W);
      })(t0);
    }
    function overlays() {
      var s = "", C = "rgba(244,245,239,.55)";
      D.blocks.forEach(function (b) {
        var x0 = b.x0, y0 = b.y0, x1 = b.x1 + 1, y1 = b.y1 + 1;
        if (b.id === "B") s += '<path d="M' + x0 + " " + y0 + "H" + x1 + "V19.2M" + x1 + " 22V" + y1 + "H" + x0 + "V" + y0 + '" fill="none" stroke="' + C + '" stroke-width=".22" stroke-dasharray=".6 .6" vector-effect="none"/>';
        else s += '<rect x="' + x0 + '" y="' + y0 + '" width="' + (x1 - x0) + '" height="' + (y1 - y0) + '" fill="none" stroke="' + C + '" stroke-width=".22" stroke-dasharray=".6 .6"/>';
        s += '<text x="' + (x0 + 1.2) + '" y="' + (y0 + 2.6) + '" fill="#F4F5EF" font-size="1.7" font-family="Instrument Sans, sans-serif" font-weight="600" letter-spacing=".08" style="text-transform:uppercase;font-stretch:75%">' + b.id + " · " + b.name + "</text>";
      });
      var p = D.pivot; s += '<circle cx="' + p.cx + '" cy="' + p.cy + '" r="' + (p.r + 0.6) + '" fill="none" stroke="' + C + '" stroke-width=".22" stroke-dasharray=".6 .6"/>';
      s += '<text x="' + (p.cx - p.r) + '" y="' + (p.cy - p.r - 1.2) + '" fill="#F4F5EF" font-size="1.7" font-family="Instrument Sans, sans-serif" font-weight="600" style="text-transform:uppercase;font-stretch:75%">D · ' + p.name + "</text>";
      svg.innerHTML = s;
      wrap.querySelectorAll(".gw-map__pin").forEach(function (n) { n.remove(); });
      if (opts.pins === false) return;
      D.observations.forEach(function (o) {
        var b = document.createElement("button"); b.className = "gw-marker gw-map__pin" + (o.x > W - 8 ? " gw-marker--flip is-flip" : ""); b.type = "button";
        b.style.left = (o.x / W * 100) + "%"; b.style.top = ((o.y + 1) / H * 100) + "%"; b.setAttribute("aria-label", "Observation " + o.n + ": " + o.title);
        b.innerHTML = '<span data-px="' + o.n + '"></span>'; b.dataset.n = o.n;
        b.addEventListener("click", function (e) { e.stopPropagation(); self.select(o.n); root.dispatchEvent(new CustomEvent("gw:obs", { detail: o, bubbles: true })); });
        wrap.appendChild(b);
      });
      if (window.GW) GW.renderPx(wrap);
    }
    function blockAt(x, y) {
      for (var k = 0; k < D.blocks.length; k++) { var b = D.blocks[k]; if (x >= b.x0 && x <= b.x1 && y >= b.y0 && y <= b.y1) return b.id + " · " + b.name; }
      var p = D.pivot; if (Math.hypot(x - p.cx, y - p.cy) <= p.r) return "D · " + p.name; return null;
    }
    var CL = { f: "Crop", p: "Pasture", t: "Track", w: "Water", b: "Structure" };
    cv.addEventListener("mousemove", function (e) {
      var r = cv.getBoundingClientRect(), x = Math.floor((e.clientX - r.left) / r.width * W), y = Math.floor((e.clientY - r.top) / r.height * H);
      if (x < 0 || y < 0 || x >= W || y >= H) return; var i = y * W + x, L = LAYERS[self.layer], c = D.cls[i];
      var val = L.src && c !== "w" && c !== "b" ? "<b>" + L.fmt(real(L.src, i), D) + "</b> " + L.short.toLowerCase() : "<b>" + CL[c] + "</b>";
      tip.innerHTML = val + '<br><span style="color:#959F9A">' + (blockAt(x, y) || CL[c]) + " · cell " + x + ", " + y + "</span>";
      var rr = root.getBoundingClientRect(); tip.style.display = "block";
      var tx = e.clientX - rr.left + 14, ty = e.clientY - rr.top + 14; if (tx > rr.width - 200) tx -= 220; tip.style.left = tx + "px"; tip.style.top = ty + "px";
    });
    cv.addEventListener("mouseleave", function () { tip.style.display = "none"; });
    this.setLayer = function (l) { if (l === self.layer) return; prev = self.layer; self.layer = l; draw(true); self.legend(); root.dispatchEvent(new CustomEvent("gw:layer", { detail: l, bubbles: true })); };
    this.setThreshold = function (v) { self.threshold = v; prev = null; draw(false); self.legend(); };
    this.select = function (n) { self.active = n; wrap.querySelectorAll(".gw-map__pin").forEach(function (p) { p.classList.toggle("is-active", p.dataset.n === n); }); };
    this.below = function (thr) { var L = LAYERS[self.layer]; if (!L.src || L.src === "elev") return null; var n = 0, tot = 0; for (var i = 0; i < W * H; i++) if (D.cls[i] === "f") { tot++; if (real(L.src, i) < thr) n++; } return n / tot; };
    this.legend = function () {
      var el = opts.legend; if (!el) return; var L = LAYERS[self.layer];
      if (!L.src) { el.innerHTML = '<div class="gw-label">' + L.name + '</div><div style="display:grid;grid-template-columns:repeat(2,auto);gap:6px 16px;justify-content:start;font-size:12px">' +
        [["field", "Crop"], ["pasture", "Pasture"], ["track", "Track"], ["water", "Water"], ["structure", "Structure"]].map(function (k) { var c = colours[k[0]]; return '<span style="display:flex;gap:8px;align-items:center"><i class="gw-swatch-dot" style="background:rgb(' + c.join(",") + ')"></i>' + k[1] + "</span>"; }).join("") + "</div>"; return; }
      var cells = ""; for (var i = 0; i < 9; i++) { var c = colours[L.ramp][i]; cells += '<i style="background:rgb(' + c.join(",") + ')"></i>'; }
      el.innerHTML = '<div class="gw-label">' + L.name + '</div><div class="gw-legend__ramp">' + cells + '</div><div class="gw-legend__ticks">' + L.ticks.map(function (t) { return "<span>" + t + "</span>"; }).join("") + '</div><div style="font-size:12px;color:var(--hco-text-subtle)">' + L.note + "</div>";
    };
    readColours(); size(); draw(false); overlays(); this.legend();
    var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { size(); prev = null; draw(false); }, 120); });
    root.__map = this;
  }
  window.GW = window.GW || {}; window.GW.FieldMap = FieldMap; window.GW.LAYERS = LAYERS;
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-fieldmap]").forEach(function (el) {
      var leg = el.dataset.legend ? document.querySelector(el.dataset.legend) : null;
      new FieldMap(el, { layer: el.dataset.layer || "vigour", legend: leg, pins: el.dataset.pins !== "off" });
    });
  });
})();
