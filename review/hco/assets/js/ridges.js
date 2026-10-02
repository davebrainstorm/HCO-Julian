/* Groundwork · pixel ridgelines (hero canvas). Uses window.GW_RIDGES. Same pen as the wordmark: 2-cell stroke, 1-cell stairs. */
(function () {
  "use strict";
  var AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
  function dec(s) { var a = []; for (var i = 0; i < s.length; i++) a.push(AL.indexOf(s[i]) / 63); return a; }
  function tok(n) { return getComputedStyle(document.documentElement).getPropertyValue("--hco-" + n).trim(); }
  function rgb(h) { h = h.replace("#", ""); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function mix(a, b, f) { return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]; }
  function Ridges(cv, opts) {
    opts = opts || {}; var R = window.GW_RIDGES, ctx = cv.getContext("2d"), lines = R.h.map(dec), tones = R.t.map(dec), n = R.n, m = R.m;
    var bg = rgb(opts.bg || tok("stone-900")), basalt = rgb(tok("basalt")), moss = rgb(tok("moss")), E = [0, 1, 2, 3, 4].map(function (i) { return rgb(tok("e" + i)); });
    var stops = [[0, basalt], [.42, mix(basalt, moss, .35)], [.72, moss], [.88, E[0]], [.945, E[1]], [.972, E[2]], [.988, E[3]], [.997, E[4]]];
    function tone(t) { for (var k = 1; k < stops.length; k++) if (t <= stops[k][0]) { var a = stops[k - 1], b = stops[k]; return mix(a[1], b[1], (t - a[0]) / (b[0] - a[0])); } return E[4]; }
    var cell = 6, cols = m, rows = 100, prog = 0;
    function size() { var r = cv.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1); cell = Math.max(4, Math.round(r.width / m)); cols = Math.ceil(r.width / cell); rows = Math.ceil(r.height / cell);
      cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function frame(p) {
      ctx.fillStyle = "rgb(" + bg.join(",") + ")"; ctx.fillRect(0, 0, cols * cell, rows * cell);
      var b0 = opts.b0 || .38, b1 = opts.b1 || 1.06, amp = opts.amp || .42, fade = .55;
      for (var k = 0; k < n; k++) {
        var local = Math.max(0, Math.min(1, p * (n + 6) / 7 - k / 7)); if (local <= 0) continue;
        var e = 1 - Math.pow(1 - local, 3), base = rows * (b0 + (b1 - b0) * k / (n - 1)), depth = k / (n - 1), L = lines[k], T = tones[k], top = [];
        for (var x = 0; x < cols; x++) { var s = Math.min(m - 1, Math.floor(x / cols * m)); top.push(Math.round(base - L[s] * rows * amp * e)); }
        for (x = 0; x < cols; x++) {
          ctx.fillStyle = "rgb(" + bg.join(",") + ")"; ctx.fillRect(x * cell, (top[x] + 2) * cell, cell, rows * cell);
          var a = top[x], lo = a + 1;
          if (x > 0 && top[x - 1] > lo) lo = top[x - 1]; if (x < cols - 1 && top[x + 1] > lo) lo = top[x + 1];
          var s2 = Math.min(m - 1, Math.floor(x / cols * m)), c = tone(T[s2]); c = mix(bg, c, (fade + (1 - fade) * depth) * Math.min(1, local * 1.4));
          ctx.fillStyle = "rgb(" + (c[0] | 0) + "," + (c[1] | 0) + "," + (c[2] | 0) + ")";
          for (var y = a; y <= lo; y++) ctx.fillRect(x * cell, y * cell, cell - (opts.gap ? 1 : 0), cell - (opts.gap ? 1 : 0));
        }
      }
    }
    function run() {
      size(); var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce || opts.static) { frame(1); return; }
      var t0 = performance.now(), dur = opts.dur || 2600;
      (function step(now) { prog = Math.min(1, (now - t0) / dur); frame(prog); if (prog < 1) requestAnimationFrame(step); })(t0);
    }
    run(); var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { size(); frame(1); }, 150); });
  }
  window.GW = window.GW || {}; window.GW.Ridges = Ridges;
  document.addEventListener("DOMContentLoaded", function () { document.querySelectorAll("canvas[data-ridges]").forEach(function (c) { new Ridges(c, { b0: +c.dataset.b0 || undefined, amp: +c.dataset.amp || undefined, gap: c.dataset.gap === "on", static: c.dataset.static === "on" }); }); });
})();
