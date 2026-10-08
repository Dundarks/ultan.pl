// Menu na telefonie, cień nagłówka, mapa ładowana na życzenie, podgląd dyplomów.
(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("menu");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Mapa Google dopiero po kliknięciu — bez tego strona nie łączy się z Google.
  document.querySelectorAll("[data-map]").forEach(function (box) {
    var btn = box.querySelector("button");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.src = box.getAttribute("data-map");
      frame.title = "Mapa dojazdu do gabinetu Ultan";
      frame.loading = "lazy";
      frame.referrerPolicy = "no-referrer-when-downgrade";
      box.innerHTML = "";
      box.appendChild(frame);
    });
  });

  var box = document.querySelector(".lightbox");
  if (box) {
    var img = box.querySelector("img");
    document.querySelectorAll("[data-full]").forEach(function (b) {
      b.addEventListener("click", function () {
        img.src = b.getAttribute("data-full");
        img.alt = b.getAttribute("data-alt") || "";
        box.showModal();
      });
    });
    box.querySelector(".lightbox__close").addEventListener("click", function () { box.close(); });
    box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
