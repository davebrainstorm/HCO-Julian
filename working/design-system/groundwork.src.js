/* Groundwork · HCO design system · behaviour v0.1 (no dependencies) */
(function () {
  "use strict";
  var GLYPHS = /*GLYPHS*/;
  var NS = "http://www.w3.org/2000/svg";
  /* Pixel numerals: one merged set of rects per string, 10 units tall, 1-unit tracking. */
  function pxSVG(str, opts) {
    opts = opts || {};
    var x = 0, rects = [], track = opts.track == null ? 1 : opts.track;
    String(str).split("").forEach(function (ch, i) {
      var g = GLYPHS[ch]; if (!g) return;
      if (i && x) x += track;
      for (var r = 0; r < 10; r++) {
        var row = g[r], c = 0;
        while (c < row.length) {
          if (row[c] === "#") { var s = c; while (c < row.length && row[c] === "#") c++; rects.push([x + s, r, c - s]); } else c++;
        }
      }
      x += g[0].length;
    });
    var merged = [];
    rects.forEach(function (q) {
      for (var k = 0; k < merged.length; k++) { var m = merged[k]; if (m[0] === q[0] && m[2] === q[2] && m[1] + m[3] === q[1]) { m[3]++; return; } }
      merged.push([q[0], q[1], q[2], 1]);
    });
    var d = merged.map(function (m) { return "M" + m[0] + " " + m[1] + "h" + m[2] + "v" + m[3] + "h-" + m[2] + "z"; }).join("");
    return '<svg xmlns="' + NS + '" viewBox="0 0 ' + x + ' 10" width="' + x + '" height="10" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>';
  }
  function renderPx(root) {
    (root || document).querySelectorAll("[data-px]").forEach(function (el) {
      var v = el.getAttribute("data-px") || el.textContent.trim();
      if (el.__px === v) return; el.__px = v;
      el.classList.add("gw-px"); el.setAttribute("role", "img"); el.setAttribute("aria-label", v);
      el.innerHTML = pxSVG(v);
    });
  }
  /* The trace: samples joined by 45° slopes (the Ridgeline as a line). */
  function traceSVG(heights, opts) {
    opts = opts || {}; var u = opts.unit || 10, n = heights.length, rows = opts.rows || (Math.max.apply(null, heights) + 1);
    function y(h) { return (rows - 1 - h) * u + u / 2; }
    var pts = [[0, y(heights[0])]];
    heights.forEach(function (h, i) { pts.push([i * u + u / 2, y(h)]); });
    pts.push([n * u, y(heights[n - 1])]);
    var d = pts.map(function (p, i) { return (i ? "L" : "M") + p[0] + " " + p[1]; }).join("");
    return '<svg xmlns="' + NS + '" viewBox="0 ' + (-u / 2) + " " + n * u + " " + (rows * u + u) + '" fill="none" stroke="currentColor" stroke-width="' + u + '" stroke-linejoin="miter" stroke-miterlimit="10" aria-hidden="true"><path d="' + d + '"/></svg>';
  }
  /* Ridgeline loader */
  function renderLoaders(root) {
    var H = [0, 1, 1, 2, 3, 4, 3, 2], C = ["var(--hco-e0)", "var(--hco-e1)", "var(--hco-e2)", "var(--hco-e3)", "var(--hco-e4)"];
    (root || document).querySelectorAll(".gw-loader:not(.is-ready)").forEach(function (el) {
      el.classList.add("is-ready"); el.setAttribute("role", "status"); if (!el.getAttribute("aria-label")) el.setAttribute("aria-label", "Loading");
      el.innerHTML = H.map(function (h, i) { return '<i style="--h:' + h + ';--i:' + i + ';--c:' + (el.dataset.mono ? "currentColor" : C[h]) + ';grid-column:' + (i + 1) + '"></i>'; }).join("");
    });
  }
  /* Toasts */
  function toast(msg, opts) {
    opts = opts || {};
    var region = document.querySelector(".gw-toast-region");
    if (!region) { region = document.createElement("div"); region.className = "gw-toast-region"; region.setAttribute("aria-live", "polite"); document.body.appendChild(region); }
    var t = document.createElement("div"), ms = opts.ms || 4200, icon = opts.icon || "success";
    t.className = "gw-toast"; t.setAttribute("role", "status");
    t.innerHTML = '<svg class="gw-icon" style="color:var(--hco-' + (opts.tone || "positive") + ')"><use href="' + GW.sprite + "#i-" + icon + '"/></svg><div><div style="font-weight:600;font-size:15px;line-height:24px">' + msg + "</div>" +
      (opts.body ? '<div style="font-size:14px;line-height:20px;color:var(--hco-text-muted)">' + opts.body + "</div>" : "") + '</div><button class="gw-toast__close" aria-label="Dismiss"><svg class="gw-icon"><use href="' + GW.sprite + '#i-close"/></svg></button>' +
      '<div class="gw-toast__timer">' + new Array(13).join("<i></i>") + "</div>";
    region.appendChild(t);
    var cells = t.querySelectorAll(".gw-toast__timer i");
    cells.forEach(function (c, i) { c.style.animationDuration = "1ms"; c.style.animationDelay = (ms * (cells.length - i) / cells.length) + "ms"; });
    var kill = function () { t.style.transition = "opacity 200ms"; t.style.opacity = "0"; setTimeout(function () { t.remove(); }, 220); };
    t.querySelector(".gw-toast__close").onclick = kill; setTimeout(kill, ms + 200);
  }
  function bind(root) {
    root = root || document;
    renderPx(root); renderLoaders(root);
    root.querySelectorAll('[role="tablist"]').forEach(function (list) {
      if (list.__b) return; list.__b = 1;
      var tabs = list.querySelectorAll('[role="tab"]');
      function sel(tab, focus) {
        tabs.forEach(function (t) { var on = t === tab; t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1; var p = document.getElementById(t.getAttribute("aria-controls")); if (p) p.hidden = !on; });
        if (focus) tab.focus(); list.dispatchEvent(new CustomEvent("gw:tab", { detail: tab }));
      }
      tabs.forEach(function (t, i) {
        t.addEventListener("click", function () { sel(t); });
        t.addEventListener("keydown", function (e) { var k = e.key, n = tabs.length; if (k === "ArrowRight" || k === "ArrowLeft") { e.preventDefault(); sel(tabs[(i + (k === "ArrowRight" ? 1 : n - 1)) % n], true); } });
      });
    });
    root.querySelectorAll(".gw-switch").forEach(function (s) { if (s.__b) return; s.__b = 1; s.addEventListener("click", function () { s.setAttribute("aria-checked", s.getAttribute("aria-checked") !== "true"); s.dispatchEvent(new Event("change", { bubbles: true })); }); });
    root.querySelectorAll(".gw-segmented, [data-single]").forEach(function (g) { if (g.__b) return; g.__b = 1; g.addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b || !g.contains(b)) return; g.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); g.dispatchEvent(new CustomEvent("gw:select", { detail: b.dataset.value || b.textContent.trim(), bubbles: true })); }); });
    root.querySelectorAll(".gw-chip[aria-pressed]").forEach(function (c) { if (c.__b || c.closest("[data-single]")) return; c.__b = 1; c.addEventListener("click", function () { c.setAttribute("aria-pressed", c.getAttribute("aria-pressed") !== "true"); }); });
    root.querySelectorAll(".gw-range").forEach(function (r) {
      if (r.__b) return; r.__b = 1;
      var out = r.id && document.querySelector('[for="' + r.id + '"] output, output[for="' + r.id + '"]');
      function upd() { var p = (r.value - r.min) / (r.max - r.min) * 100; r.style.setProperty("--v", p + "%"); if (out) out.textContent = r.dataset.fmt === "pct" ? Math.round(r.value) + "%" : (+r.value).toFixed(r.step && r.step.indexOf(".") > -1 ? r.step.split(".")[1].length : 0); }
      r.addEventListener("input", upd); upd();
    });
    root.querySelectorAll("[data-open]").forEach(function (b) {
      if (b.__b) return; b.__b = 1;
      b.addEventListener("click", function () { var m = document.getElementById(b.dataset.open); if (!m) return; m.classList.add("is-open"); var f = m.querySelector("button, [href], input"); if (f) f.focus(); m.__opener = b; });
    });
    root.querySelectorAll(".gw-scrim").forEach(function (m) {
      if (m.__b) return; m.__b = 1;
      function close() { m.classList.remove("is-open"); if (m.__opener) m.__opener.focus(); }
      m.addEventListener("click", function (e) { if (e.target === m || e.target.closest("[data-close]")) close(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape" && m.classList.contains("is-open")) close(); });
    });
    root.querySelectorAll("[data-toast]").forEach(function (b) { if (b.__b) return; b.__b = 1; b.addEventListener("click", function () { toast(b.dataset.toast, { body: b.dataset.toastBody, tone: b.dataset.tone, icon: b.dataset.icon }); }); });
    root.querySelectorAll("[data-busy]").forEach(function (b) { if (b.__b) return; b.__b = 1; b.addEventListener("click", function () { b.setAttribute("aria-busy", "true"); setTimeout(function () { b.removeAttribute("aria-busy"); toast(b.dataset.busy || "Done"); }, 1800); }); });
    root.querySelectorAll(".gw-dropzone").forEach(function (z) {
      if (z.__b) return; z.__b = 1;
      ["dragenter", "dragover"].forEach(function (ev) { z.addEventListener(ev, function (e) { e.preventDefault(); z.classList.add("is-over"); }); });
      ["dragleave", "drop"].forEach(function (ev) { z.addEventListener(ev, function (e) { e.preventDefault(); z.classList.remove("is-over"); if (ev === "drop") toast("Files received", { body: (e.dataTransfer.files.length || 0) + " file(s). Nothing is uploaded in this preview." }); }); });
    });
  }
  var script = document.currentScript;
  var GW = window.GW = { px: pxSVG, renderPx: renderPx, trace: traceSVG, toast: toast, bind: bind,
    sprite: (script && script.dataset.sprite) || "assets/icons/sprite.svg" };
  if (document.readyState !== "loading") bind(); else document.addEventListener("DOMContentLoaded", function () { bind(); });
})();
