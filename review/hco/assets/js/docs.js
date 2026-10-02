/* Groundwork documentation behaviour: theme, navigation, contents, search, specimens, copy. */
(function () {
  "use strict";
  var root = document.documentElement, KEY = root.getAttribute("data-theme-key") || "gw-theme";
  try { var saved = localStorage.getItem(KEY); if (saved) root.setAttribute("data-theme", saved); } catch (e) {}
  if (!root.getAttribute("data-theme")) root.setAttribute("data-theme", "dark");
  function ready(fn) { if (document.readyState !== "loading") fn(); else document.addEventListener("DOMContentLoaded", fn); }
  ready(function () {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
      b.addEventListener("click", function () { var t = root.getAttribute("data-theme") === "dark" ? "light" : "dark"; root.setAttribute("data-theme", t); try { localStorage.setItem(KEY, t); } catch (e) {}
        document.dispatchEvent(new CustomEvent("gw:theme", { detail: t })); });
    });
    var side = document.querySelector(".ds-side"), menu = document.querySelector(".ds-menu");
    if (menu && side) { menu.addEventListener("click", function () { var o = side.classList.toggle("is-open"); menu.setAttribute("aria-expanded", o); });
      document.addEventListener("click", function (e) { if (side.classList.contains("is-open") && !side.contains(e.target) && !menu.contains(e.target)) { side.classList.remove("is-open"); menu.setAttribute("aria-expanded", false); } }); }
    // contents
    var toc = document.querySelector(".ds-toc nav"), heads = Array.prototype.slice.call(document.querySelectorAll(".ds-content > .ds-sec > h2[id]"));
    if (toc && heads.length) {
      toc.innerHTML = heads.map(function (h) { return '<a href="#' + h.id + '">' + h.firstChild.textContent.trim() + "</a>"; }).join("");
      var links = toc.querySelectorAll("a");
      var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { links.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id); }); } }); }, { rootMargin: "-80px 0px -70% 0px" });
      heads.forEach(function (h) { io.observe(h); });
    }
    // specimens
    document.querySelectorAll(".ds-spec").forEach(function (sp) {
      var g = sp.querySelector("[data-spec-grid]"), th = sp.querySelector("[data-spec-theme]"), cd = sp.querySelector("[data-spec-code]"), stage = sp.querySelector(".ds-spec__stage"), code = sp.querySelector(".ds-code");
      if (g) g.addEventListener("click", function () { var on = sp.getAttribute("data-grid") !== "on"; sp.setAttribute("data-grid", on ? "on" : "off"); g.setAttribute("aria-pressed", on); });
      if (th) th.addEventListener("click", function () { var cur = stage.getAttribute("data-theme") || root.getAttribute("data-theme"); var nx = cur === "dark" ? "light" : "dark"; stage.setAttribute("data-theme", nx); sp.querySelector(".ds-spec__bar").setAttribute("data-theme", nx); th.setAttribute("aria-pressed", true); });
      if (cd && code) cd.addEventListener("click", function () { code.hidden = !code.hidden; cd.setAttribute("aria-pressed", !code.hidden); });
    });
    // copy
    document.addEventListener("click", function (e) {
      var b = e.target.closest("[data-copy]"); if (!b) return;
      var txt = b.getAttribute("data-copy"); if (!txt) { var pre = b.parentElement.querySelector("pre, code"); txt = pre ? pre.innerText : ""; }
      var ok = function () { if (window.GW && GW.toast) GW.toast("Copied", { body: txt.length > 64 ? txt.slice(0, 64) + "…" : txt, icon: "copy" }); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(ok, ok); else ok();
    });
    // search
    var find = document.querySelector(".ds-find"), input = find && find.querySelector("input"), list = find && find.querySelector(".ds-find__list"), idx = window.GW_INDEX || [], sel = 0, hits = [];
    function open() { if (!find) return; find.classList.add("is-open"); input.value = ""; render(""); setTimeout(function () { input.focus(); }, 10); }
    function close() { if (find) find.classList.remove("is-open"); }
    function render(q) {
      q = q.trim().toLowerCase(); hits = idx.filter(function (r) { return !q || (r.t + " " + r.s + " " + (r.k || "")).toLowerCase().indexOf(q) > -1; }).slice(0, 12); sel = 0;
      list.innerHTML = hits.length ? hits.map(function (r, i) { return '<li><a href="' + r.u + '"' + (i === 0 ? ' class="is-sel"' : "") + ">" + r.t + "<span>" + r.s + "</span></a></li>"; }).join("") : '<li class="ds-find__empty">Nothing matches. Try “colour”, “button” or “map”.</li>';
    }
    if (find) {
      document.querySelectorAll("[data-search]").forEach(function (b) { b.addEventListener("click", open); });
      input.addEventListener("input", function () { render(input.value); });
      input.addEventListener("keydown", function (e) {
        var as = list.querySelectorAll("a"); if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); sel = (sel + (e.key === "ArrowDown" ? 1 : as.length - 1)) % Math.max(1, as.length); as.forEach(function (a, i) { a.classList.toggle("is-sel", i === sel); }); }
        if (e.key === "Enter" && as[sel]) { location.href = as[sel].getAttribute("href"); close(); }
      });
      find.addEventListener("click", function (e) { if (e.target === find) close(); });
      document.addEventListener("keydown", function (e) { if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); open(); } else if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); open(); } else if (e.key === "Escape") close(); });
    }
  });
})();
