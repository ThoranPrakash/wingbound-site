/* WingBound — site scripts. Every page works without JS; this adds interaction and polish. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  // Footer year
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // ---------- Reveal on scroll + blueprint draw-on ----------
  var revealEls = $$("[data-reveal]");
  var drawEls = $$("[data-draw]");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add(e.target.hasAttribute("data-draw") ? "is-drawn" : "is-in");
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealEls.forEach(function (el, i) {
      // small stagger for siblings in the same row
      var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      el.style.transitionDelay = Math.min(sib, 5) * 70 + "ms";
      io.observe(el);
    });
    drawEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
    drawEls.forEach(function (el) { el.classList.add("is-drawn"); });
  }

  // ---------- Scroll progress plane in the header ----------
  var trail = $(".fp-trail");
  var fpPlane = $(".fp-plane");
  if (trail && fpPlane) {
    var ticking = false;
    var update = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, window.scrollY / max) : 0;
      trail.style.transform = "scaleX(" + p + ")";
      fpPlane.style.transform = "translateX(" + (p * (window.innerWidth - 24)) + "px)";
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // ---------- Pause SVG animations when off-screen ----------
  var animated = $$("svg.sky, .flightfield svg, .sta-loop svg");
  animated.forEach(function (svg) { if (reduceMotion && svg.pauseAnimations) svg.pauseAnimations(); });
  if (!reduceMotion && "IntersectionObserver" in window) {
    var skyIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.target.pauseAnimations) return;
        if (e.isIntersecting) e.target.unpauseAnimations(); else e.target.pauseAnimations();
      });
    });
    animated.forEach(function (svg) { skyIO.observe(svg); });
  }

  // ---------- Mobile navigation ----------
  var toggle = $(".nav-toggle");
  var nav = $("#site-nav");
  if (toggle && nav) {
    var mq = window.matchMedia("(min-width: 1080px)");
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      if (open) { var first = $("a", nav); if (first) first.focus(); }
    };
    toggle.addEventListener("click", function () { setOpen(toggle.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { setOpen(false); toggle.focus(); }
    });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { if (!mq.matches) setOpen(false); }); });
    mq.addEventListener("change", function (m) { if (m.matches) setOpen(false); });
    // keep keyboard focus inside the open menu
    nav.addEventListener("keydown", function (e) {
      if (e.key !== "Tab" || mq.matches || !nav.classList.contains("is-open")) return;
      var items = $$("a", nav).concat([toggle]);
      var i = items.indexOf(document.activeElement);
      if (e.shiftKey && i === 0) { e.preventDefault(); toggle.focus(); }
    });
    toggle.addEventListener("keydown", function (e) {
      if (e.key === "Tab" && !e.shiftKey && !mq.matches && nav.classList.contains("is-open")) {
        e.preventDefault(); var first = $("a", nav); if (first) first.focus();
      }
    });
  }

  // ---------- Tabs (audience switcher) ----------
  $$("[data-tabs]").forEach(function (wrap) {
    var tabs = $$('[role="tab"]', wrap);
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tab.focus();
      tab.scrollIntoView({ block: "nearest", inline: "nearest", behavior: reduceMotion ? "auto" : "smooth" });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t, false); });
      t.addEventListener("keydown", function (e) {
        var n = null;
        if (e.key === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") n = tabs[0];
        if (e.key === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  });

  // ---------- Forces of flight ----------
  $$("[data-forces]").forEach(function (box) {
    var btns = $$(".force-btn", box);
    var texts = $$(".force-text [data-force]", box);
    var show = function (force) {
      box.setAttribute("data-active", force);
      btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.force === force)); });
      texts.forEach(function (p) { p.hidden = p.dataset.force !== force; });
    };
    btns.forEach(function (b) { b.addEventListener("click", function () { show(b.dataset.force); }); });
    show("lift");
  });

  // ---------- Electronics wiring ----------
  $$("[data-wiring]").forEach(function (box) {
    var art = $(".wiring-art", box);
    var btns = $$(".part-btn", box);
    var set = function (part) {
      art.setAttribute("data-active", part || "");
      btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.part === part)); });
    };
    btns.forEach(function (b) {
      b.addEventListener("click", function () { set(b.getAttribute("aria-pressed") === "true" ? "" : b.dataset.part); });
      b.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) art.setAttribute("data-active", b.dataset.part); });
      b.addEventListener("mouseleave", function () {
        var pressed = btns.filter(function (x) { return x.getAttribute("aria-pressed") === "true"; })[0];
        art.setAttribute("data-active", pressed ? pressed.dataset.part : "");
      });
    });
    $$(".wd-node", art).forEach(function (n) {
      n.addEventListener("click", function () { set(n.getAttribute("data-parts")); });
      n.style.cursor = "pointer";
    });
  });

  // ---------- Contact form: builds a message and opens WhatsApp or email ----------
  var form = $("#contact-form");
  if (form) {
    var status = $("#form-status");
    var val = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; };

    // Pre-select the interest from ?package=
    var pkg = new URLSearchParams(location.search).get("package");
    if (pkg) $$('input[name="interest"]', form).forEach(function (r) { if (r.dataset.key === pkg) r.checked = true; });

    var check = function (el) {
      var ok = el.checkValidity();
      el.closest(".field").classList.toggle("is-invalid", !ok);
      el.setAttribute("aria-invalid", String(!ok));
      return ok;
    };
    var fields = $$("input[required], textarea[required], input[type=email], input[type=tel]", form);
    fields.forEach(function (el) {
      el.addEventListener("blur", function () { if (el.value) check(el); });
      el.addEventListener("input", function () { if (el.closest(".field").classList.contains("is-invalid")) check(el); });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      fields.forEach(function (el) { if (!check(el) && !firstBad) firstBad = el; });
      if (firstBad) { firstBad.focus(); return; }

      var via = (e.submitter && e.submitter.value) || "whatsapp";
      var interest = ($('input[name="interest"]:checked', form) || {}).value || "";
      var details = [
        "Name: " + val("name"),
        "I am: " + val("who"),
        val("organisation") && "Organisation: " + val("organisation"),
        val("city") && "City: " + val("city"),
        val("phone") && "Phone: " + val("phone"),
        val("email") && "Email: " + val("email"),
        interest && "Interested in: " + interest
      ].filter(Boolean);
      var text = "Hi WingBound,\n\n" + val("message") + "\n\n" + details.join("\n");

      if (via === "whatsapp") {
        window.open("https://wa.me/" + form.dataset.wa + "?text=" + encodeURIComponent(text), "_blank", "noopener");
        status.className = "form-status is-success";
        status.textContent = "WhatsApp is opening with your message. Press send there to reach us.";
      } else {
        var subject = "WingBound enquiry from " + val("name") + (val("organisation") ? ", " + val("organisation") : "");
        location.href = "mailto:" + form.dataset.to + "?cc=" + form.dataset.cc + "&subject=" +
          encodeURIComponent(subject) + "&body=" + encodeURIComponent(text);
        status.className = "form-status is-success";
        status.textContent = "Your email app is opening with the message. If nothing opens, email " + form.dataset.to + " or use WhatsApp.";
      }
    });
  }
})();
