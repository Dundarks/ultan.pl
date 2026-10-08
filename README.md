# ultan.pl

Strona gabinetu fizjoterapii Ultan (Marek Piask, Gdańsk Osowa). Statyczny HTML hostowany na GitHub Pages.

## Jak edytować

Treść podstron jest w `_zrodla/strony/*.html`, wspólny nagłówek, stopka i ikony w `_zrodla/szablon.py`.
Po zmianie zbuduj strony:

```
python _zrodla/szablon.py
```

Skrypt nadpisze `index.html`, `o-mnie/index.html` itd. — tych plików nie edytuj ręcznie.
Wygląd: `assets/css/styl.css`. Zdjęcia: `assets/img/` (WebP).

Podgląd lokalny: `python -m http.server 8765` i http://127.0.0.1:8765/

Katalogi zaczynające się od `_` nie są publikowane przez GitHub Pages.
