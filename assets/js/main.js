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

  // Pre-select the interest from ?package= on the contact page
  var pkg = new URLSearchParams(location.search).get("package");
  var pkgSelect = document.getElementById("interest");
  if (pkg && pkgSelect) {
    Array.prototype.forEach.call(pkgSelect.options, function (o) {
      if (o.dataset.key === pkg) o.selected = true;
    });
  }

  // Contact form: builds a message and opens email or WhatsApp
  var form = document.getElementById("contact-form");
  if (form) {
    var status = document.getElementById("form-status");
    var val = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; };
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var via = (e.submitter && e.submitter.value) || "email";
      var lines = [
        "Hi WingBound,",
        "",
        val("message"),
        "",
        "Name: " + val("name"),
        "I am: " + val("who"),
        val("organisation") && "Organisation: " + val("organisation"),
        val("city") && "City: " + val("city"),
        val("phone") && "Phone: " + val("phone"),
        val("email") && "Email: " + val("email"),
        "Interested in: " + val("interest")
      ].filter(function (l) { return l !== "" && l !== false; });
      // keep blank lines after the greeting and message
      var text = lines[0] + "\n\n" + lines[1] + "\n\n" + lines.slice(2).join("\n");
      if (via === "whatsapp") {
        window.open("https://wa.me/918332032455?text=" + encodeURIComponent(text), "_blank", "noopener");
        status.className = "form-status is-success";
        status.textContent = "WhatsApp is opening with your message. Press send there to reach us.";
      } else {
        var subject = "WingBound enquiry from " + val("name") + (val("organisation") ? ", " + val("organisation") : "");
        location.href = "mailto:writetonikhilkalyan@gmail.com?cc=thoranprakash23@gmail.com&subject=" +
          encodeURIComponent(subject) + "&body=" + encodeURIComponent(text);
        status.className = "form-status is-success";
        status.textContent = "Your email app is opening with the message. If nothing opens, email writetonikhilkalyan@gmail.com or use WhatsApp.";
      }
    });
  }
})();
