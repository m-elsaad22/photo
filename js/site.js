(function () {
  "use strict";

  var cfg = window.RUKN || {};
  var phone = cfg.phone || "+971586634710";
  var waBase = cfg.whatsapp || "https://wa.me/971586634710";
  var waMsg = cfg.whatsappMessage || "السلام عليكم، أرغب في طلب خدمة من ركن التطور في الإمارات.";

  function waUrl(extra) {
    var msg = waMsg;
    if (extra) {
      msg = "السلام عليكم، أرغب في طلب خدمة من ركن التطور في " + extra + ".";
    }
    return waBase + "?text=" + encodeURIComponent(msg);
  }

  function waCustom(text) {
    return waBase + "?text=" + encodeURIComponent(text);
  }

  document.querySelectorAll("[data-whatsapp]").forEach(function (el) {
    var custom = el.getAttribute("data-wa-text");
    el.setAttribute("href", custom ? waCustom(custom) : waUrl());
    el.setAttribute("target", "_blank");
    el.setAttribute("rel", "noopener");
  });

  document.querySelectorAll("[data-area]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      window.open(waUrl(btn.getAttribute("data-area")), "_blank", "noopener");
    });
  });

  var quoteForm = document.getElementById("quoteForm");
  if (quoteForm) {
    quoteForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var service = (quoteForm.querySelector("[name=service]") || {}).value || "خدمة منزلية";
      var emirate = (quoteForm.querySelector("[name=emirate]") || {}).value || "الإمارات";
      var text = "السلام عليكم، أرغب في عرض سعر لخدمة «" + service + "» في " + emirate + ".";
      window.open(waCustom(text), "_blank", "noopener");
    });
  }

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
    menuBtn.setAttribute("aria-label", open ? "إغلاق القائمة" : "فتح القائمة");
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
    var label = btn.getAttribute("data-caption") || "صورة";
    btn.setAttribute("aria-label", "عرض الصورة: " + label);
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
    lightboxImg.src = el.getAttribute("data-src");
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
    if (e.key === "ArrowLeft") show(index + 1);
    if (e.key === "ArrowRight") show(index - 1);
    if (e.key === "Escape") closeLightbox();
  });

  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "80px 0px 10% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
    setTimeout(function () {
      revealEls.forEach(function (el) { el.classList.add("is-in"); });
    }, 1400);
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  void phone;
})();
