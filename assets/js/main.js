/* WingBound — site scripts. Everything works without JS; this adds polish. */
(function () {
  "use strict";

  // Lucide icons (loaded from CDN with defer)
  if (window.lucide) window.lucide.createIcons({ attrs: { "aria-hidden": "true" } });

  // Footer year
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Scroll progress plane in the header
  var trail = document.querySelector(".fp-trail");
  var fpPlane = document.querySelector(".fp-plane");
  if (trail && fpPlane) {
    var ticking = false;
    var update = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, window.scrollY / max) : 0;
      trail.style.transform = "scaleX(" + p + ")";
      fpPlane.style.transform = "translateX(" + (p * (window.innerWidth - 20)) + "px)";
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // Pause the flying planes when they are off-screen (or if the user prefers less motion)
  var skies = document.querySelectorAll("svg.sky");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  skies.forEach(function (svg) { if (reduce && svg.pauseAnimations) svg.pauseAnimations(); });
  if (!reduce && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.target.pauseAnimations) return;
        if (e.isIntersecting) e.target.unpauseAnimations(); else e.target.pauseAnimations();
      });
    });
    skies.forEach(function (svg) { io.observe(svg); });
  }

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    window.matchMedia("(min-width: 1140px)").addEventListener("change", function (mq) {
      if (mq.matches) setOpen(false);
    });
  }

  // Pre-select package from ?package= on the booking page
  var pkg = new URLSearchParams(location.search).get("package");
  var pkgSelect = document.getElementById("package");
  if (pkg && pkgSelect) {
    Array.prototype.forEach.call(pkgSelect.options, function (o) {
      if (o.dataset.key === pkg) o.selected = true;
    });
  }

  // Booking form — submit to Web3Forms with fetch, fall back to normal POST
  var form = document.getElementById("booking-form");
  if (form) {
    var status = document.getElementById("form-status");
    var btn = form.querySelector("button[type=submit]");
    form.addEventListener("submit", function (e) {
      if (!form.checkValidity()) return; // let the browser show errors
      var key = form.querySelector("[name=access_key]").value;
      if (!key || key.indexOf("YOUR_") === 0) {
        e.preventDefault();
        status.className = "form-status is-error";
        status.textContent = "The form is not connected yet. Please call or WhatsApp +91 83320 32455, or email writetonikhilkalyan@gmail.com.";
        return;
      }
      e.preventDefault();
      var original = btn.innerHTML;
      btn.disabled = true;
      btn.textContent = "Sending…";
      status.className = "form-status";
      fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form)
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.success) {
            form.reset();
            status.className = "form-status is-success";
            status.textContent = "Thank you. We have your request and will get back to you soon.";
          } else {
            throw new Error(data.message || "Failed");
          }
        })
        .catch(function () {
          status.className = "form-status is-error";
          status.textContent = "Sorry, something went wrong. Please call or WhatsApp +91 83320 32455, or email writetonikhilkalyan@gmail.com.";
        })
        .finally(function () {
          btn.disabled = false;
          btn.innerHTML = original;
          status.setAttribute("tabindex", "-1");
          status.focus();
        });
    });
  }
})();
