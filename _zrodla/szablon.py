"""Składa strony z _zrodla/strony/*.html + wspólny nagłówek i stopkę.

Uruchomienie (z katalogu repozytorium):  python _zrodla/szablon.py
Każdy plik strony zaczyna się od bloku:
    <!-- tytul: ... -->
    <!-- opis: ... -->
    <!-- adres: o-mnie/ -->        (pusty dla strony głównej)
    <!-- menu: o-mnie -->          (który punkt menu podświetlić)
Wynik ląduje w katalogu głównym (index.html, o-mnie/index.html itd.).
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_zrodla" / "strony"
DOMENA = "https://ultan.pl/"
TEL = "692 132 978"
TEL_LINK = "tel:+48692132978"

IKONY = {
    "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "auto": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14M5 17a2 2 0 1 0 4 0M15 17a2 2 0 1 0 4 0M3 17V11l2-5h14l2 5v6"/><path d="M3 11h18"/></svg>',
    "dom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
    "kalendarz": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "sport": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="13" cy="4" r="2"/><path d="m4 22 4-6 3 2 2-5 4 3 3-2"/><path d="m8 11 3-3 4 1 2 4"/></svg>',
    "uraz": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><g transform="rotate(-45 12 12)"><rect x="2" y="8" width="20" height="8" rx="4"/><path d="M8 8v8M16 8v8"/><path d="M11 11h.01M13 13h.01M13 11h.01M11 13h.01"/></g></svg>',
    "mozg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.5 2A2.5 2.5 0 0 0 7 4.5v.1A3 3 0 0 0 4.5 8 3 3 0 0 0 3 10.5 3 3 0 0 0 5 13.4V15a3 3 0 0 0 3 3h1.5V2z"/><path d="M14.5 2A2.5 2.5 0 0 1 17 4.5v.1A3 3 0 0 1 19.5 8 3 3 0 0 1 21 10.5a3 3 0 0 1-2 2.9V15a3 3 0 0 1-3 3h-1.5V2z"/><path d="M9.5 18v4M14.5 18v4"/></svg>',
    "operacja": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M12 8v6M9 11h6"/></svg>',
    "kropla": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.7s6 6.3 6 11.3a6 6 0 0 1-12 0c0-5 6-11.3 6-11.3z"/></svg>',
    "staw": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M12 2v6.8M12 15.2V22M4 6l5.5 4M14.5 14 20 18"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
    "mapa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/></svg>',
}

ZNAK = ('<svg class="logo__mark" viewBox="0 0 40 40" aria-hidden="true">'
        '<rect width="40" height="40" rx="12" fill="#1f5a43"/>'
        '<circle cx="20" cy="11.5" r="3.6" fill="#b9d03c"/>'
        '<path d="M11 31c2.5-6 5.5-10 9-12.5 3.5 2.5 6.5 6.5 9 12.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
        '<path d="M12.5 20.5c2.6 1.4 5.1 2 7.5 2s4.9-.6 7.5-2" fill="none" stroke="#b9d03c" stroke-width="3.2" stroke-linecap="round"/>'
        '</svg>')

MENU = [("", "Start", "start"), ("o-mnie/", "O mnie", "o-mnie"), ("uslugi/", "Usługi", "uslugi"),
        ("cennik/", "Cennik", "cennik"), ("kontakt/", "Kontakt", "kontakt")]


def logo(pre):
    return (f'<a class="logo" href="{pre or "./"}" aria-label="Ultan — strona główna">{ZNAK}'
            '<span><span class="logo__name">Ultan</span>'
            '<span class="logo__sub">Fizjoterapia · Gdańsk Osowa</span></span></a>')


def naglowek(pre, aktywny):
    biezacy = ' aria-current="page"'
    pozycje = "".join(
        f'<li><a href="{pre}{href}"{biezacy if klucz == aktywny else ""}>{nazwa}</a></li>'
        for href, nazwa, klucz in MENU)
    return f"""<a class="skip" href="#tresc">Przejdź do treści</a>
<header class="site-header">
  <div class="wrap site-header__in">
    {logo(pre)}
    <nav class="nav" id="menu" aria-label="Menu główne"><ul>{pozycje}</ul></nav>
    <a class="btn btn--primary header-call" href="{TEL_LINK}">{IKONY["tel"]}{TEL}</a>
    <button class="menu-toggle" type="button" aria-controls="menu" aria-expanded="false" aria-label="Otwórz menu">{IKONY["menu"]}</button>
  </div>
</header>"""


def stopka(pre):
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        {logo(pre)}
        <p>Fizjoterapia i rehabilitacja w gabinecie w Gdańsku Osowej oraz z dojazdem do pacjenta. Marek Piask, w zawodzie od 2008 roku.</p>
      </div>
      <div>
        <h2>Strony</h2>
        <ul>{"".join(f'<li><a href="{pre}{h}">{n}</a></li>' for h, n, _ in MENU)}</ul>
      </div>
      <div>
        <h2>Gabinet</h2>
        <p>ul. Nike 3<br>80-299 Gdańsk Osowa</p>
        <p><a href="https://www.google.com/maps/dir/?api=1&amp;destination=ul.+Nike+3,+80-299+Gda%C5%84sk" rel="noopener">Wyznacz trasę</a></p>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul>
          <li><a href="{TEL_LINK}">{TEL}</a></li>
          <li><a href="mailto:ultan.reh@gmail.com">ultan.reh@gmail.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Ultan Marek Piask</span>
      <a href="{pre}polityka-prywatnosci/">Polityka prywatności</a>
    </div>
  </div>
</footer>
<a class="btn btn--lime callbar" href="{TEL_LINK}">{IKONY["tel"]}Zadzwoń: {TEL}</a>"""


SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Physiotherapy",
  "name": "Ultan — fizjoterapia Marek Piask",
  "url": "https://ultan.pl/",
  "image": "https://ultan.pl/assets/img/gabinet-stol-1200.webp",
  "telephone": "+48 692 132 978",
  "email": "ultan.reh@gmail.com",
  "founder": { "@type": "Person", "name": "Marek Piask", "jobTitle": "Fizjoterapeuta" },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ul. Nike 3",
    "postalCode": "80-299",
    "addressLocality": "Gdańsk",
    "addressRegion": "pomorskie",
    "addressCountry": "PL"
  },
  "areaServed": "Gdańsk i okolice",
  "priceRange": "70–150 zł"
}
</script>"""


def zbuduj(plik):
    tekst = plik.read_text(encoding="utf-8")
    meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", tekst.split("\n\n", 1)[0]))
    tresc = re.sub(r"^(<!--.*?-->\s*)+", "", tekst, flags=re.S)
    adres = meta.get("adres", "")
    pre = "/" if plik.stem == "404" else "../" * adres.count("/")
    tresc = tresc.replace("{{pre}}", pre).replace("{{tel}}", TEL).replace("{{tel_link}}", TEL_LINK)
    for k, v in IKONY.items():
        tresc = tresc.replace("{{ikona:" + k + "}}", v)
    html = f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta["tytul"]}</title>
<meta name="description" content="{meta["opis"]}">
<link rel="canonical" href="{DOMENA}{adres}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{meta["tytul"]}">
<meta property="og:description" content="{meta["opis"]}">
<meta property="og:url" content="{DOMENA}{adres}">
<meta property="og:image" content="{DOMENA}assets/img/gabinet-szeroki-1920.webp">
<meta name="theme-color" content="#1f5a43">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{pre}assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pre}assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/css/styl.css">
{SCHEMA if adres == "" else ""}
</head>
<body>
{naglowek(pre, meta.get("menu", ""))}
<main id="tresc">
{tresc.strip()}
</main>
{stopka(pre)}
<script src="{pre}assets/js/strona.js" defer></script>
</body>
</html>
"""
    cel = ROOT / adres / "index.html" if adres else ROOT / "index.html"
    if plik.stem == "404":
        cel = ROOT / "404.html"
    cel.parent.mkdir(parents=True, exist_ok=True)
    cel.write_text(html, encoding="utf-8", newline="\n")
    print("zapisano", cel.relative_to(ROOT))


if __name__ == "__main__":
    for p in sorted(SRC.glob("*.html")):
        zbuduj(p)
    (ROOT / "favicon.svg").write_text(ZNAK.replace(' class="logo__mark"', ' xmlns="http://www.w3.org/2000/svg"').replace(' aria-hidden="true"', ""), encoding="utf-8", newline="\n")
