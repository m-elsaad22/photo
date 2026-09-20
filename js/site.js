(function () {
  "use strict";

  var cfg = window.NAQI || {};
  var phone = cfg.phone || "+971547341913";
  var waBase = cfg.whatsapp || "https://wa.me/971547341913";
  var waMsg = cfg.whatsappMessage || "Hello NAQI WASH, I would like to book a mobile car wash in Dubai.";

  function waUrl(extra) {
    var msg = extra ? waMsg.replace("in Dubai.", "in " + extra + ".") : waMsg;
    return waBase + "?text=" + encodeURIComponent(msg);
  }

  document.querySelectorAll("[data-whatsapp]").forEach(function (el) {
    el.setAttribute("href", waUrl());
    el.setAttribute("target", "_blank");
    el.setAttribute("rel", "noopener");
  });

  document.querySelectorAll("[data-area]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      window.open(waUrl(btn.getAttribute("data-area")), "_blank", "noopener");
    });
  });

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  var header = document.getElementById("header");
  var onScroll = function () {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  var menuBtn = document.getElementById("menuBtn");
  var drawer = document.getElementById("drawer");
  function setMenu(open) {
    if (!menuBtn || !drawer) return;
    menuBtn.classList.toggle("is-open", open);
    drawer.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      setMenu(!drawer.classList.contains("is-open"));
    });
  }
  if (drawer) {
    drawer.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setMenu(false);
  });

  document.querySelectorAll(".faq-q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq-item");
      var open = item.classList.contains("is-open");
      document.querySelectorAll(".faq-item").forEach(function (el) {
        el.classList.remove("is-open");
        var q = el.querySelector(".faq-q");
        if (q) q.setAttribute("aria-expanded", "false");
      });
      if (!open) {
        item.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  var items = Array.prototype.slice.call(document.querySelectorAll(".gallery-item"));
  items.forEach(function (btn) {
    var img = btn.querySelector("img");
    if (!img) return;
    var label = btn.getAttribute("data-caption") || "Gallery image";
    btn.setAttribute("aria-label", "View image: " + label);
    function hideOptional() {
      if (btn.getAttribute("data-optional") === "true") btn.hidden = true;
    }
    img.addEventListener("error", hideOptional);
    if (img.complete && img.naturalWidth === 0) hideOptional();
  });

  var lightbox = document.getElementById("lightbox");
  var lightboxImg = document.getElementById("lightboxImg");
  var lightboxCap = document.getElementById("lightboxCap");
  var index = 0;

  function visibleItems() {
    return items.filter(function (el) { return !el.hidden; });
  }

  function show(i) {
    var list = visibleItems();
    if (!list.length) return;
    index = (i + list.length) % list.length;
    var el = list[index];
    var src = el.getAttribute("data-src");
    lightboxImg.src = src;
    lightboxImg.alt = el.getAttribute("data-alt") || "";
    lightboxCap.textContent = el.getAttribute("data-caption") || "";
  }

  items.forEach(function (btn, i) {
    btn.addEventListener("click", function () {
      var list = visibleItems();
      var pos = list.indexOf(btn);
      show(pos < 0 ? i : pos);
      if (lightbox && typeof lightbox.showModal === "function") lightbox.showModal();
      else if (lightbox) lightbox.setAttribute("open", "");
    });
  });

  function closeLightbox() {
    if (!lightbox) return;
    if (typeof lightbox.close === "function" && lightbox.open) lightbox.close();
    lightbox.removeAttribute("open");
    lightboxImg.removeAttribute("src");
  }

  var closeBtn = document.getElementById("lightboxClose");
  var prevBtn = document.getElementById("lightboxPrev");
  var nextBtn = document.getElementById("lightboxNext");
  if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
  if (prevBtn) prevBtn.addEventListener("click", function () { show(index - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { show(index + 1); });
  if (lightbox) {
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }
  document.addEventListener("keydown", function (e) {
    if (!lightbox || (!lightbox.open && !lightbox.hasAttribute("open"))) return;
    if (e.key === "ArrowRight") show(index + 1);
    if (e.key === "ArrowLeft") show(index - 1);
    if (e.key === "Escape") closeLightbox();
  });

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
  }

  void phone;
})();
