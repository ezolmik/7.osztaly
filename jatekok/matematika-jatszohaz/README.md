# Matematika Játszóház

Hetedikes szakköri feladatgyűjtemény. A diákok az `index.html`-t nyitják meg böngészőben. A feladatsorok külön JSON-fájlban szerkeszthetők, a build pedig egyetlen, offline is működő HTML-fájlba rendezi őket.

## Új feladatsor hozzáadása

1. **Készítsd elő a feladatlapot.** Ha a ChatGPT-vel viszed fel, küldd el a feladatlapot és a meglévő megoldókulcsot, ha van. Kérj a Játszóházhoz illő JSON-fájlt megoldásokkal, feladatonként két segítséggel, témákkal, címkékkel és válaszmezőkkel. Ha hiányzik a kulcs, ezt is kérd hozzá. Új beszélgetésben mellékelj egy meglévő JSON-fájlt mintának.
2. **Másold be a JSON-fájlt** a [`forras/feladatsorok/`](forras/feladatsorok/) mappába. A build fájlnév szerint rendezi a sorokat, ezért használunk az elejükön sorszámot. A négy kezdő sor után az első új fájl neve például `05-uj-feladatsor.json` lehet. Egy build előtt több feladatsort is bemásolhatsz.
3. **Generáld újra az oldalt.** A repó gyökeréből lépj be a játék mappájába, majd futtasd a buildet Python 3-mal.

   ```bash
   cd jatekok/matematika-jatszohaz
   python3 forras/build.py
   ```

4. **Ellenőrizd és commitold.** Nyisd meg az `index.html`-t, keresd meg az új sort témára és címkére szűrve, majd próbáld ki a válaszellenőrzést, a segítséget és a megoldást. Az új JSON-t és a generált `index.html`-t együtt commitold.

A build a JSON-hibáknál, hiányzó kötelező mezőknél és ismétlődő azonosítóknál megjelöli az érintett fájlt. Hibás adat esetén az előző `index.html` használható marad.

## Meglévő feladatsor javítása

A meglévő JSON-fájlt szerkeszd, majd futtasd újra a buildet. A feladatsor, a feladatok és a válaszmezők `id` mezőit tartsd meg, hogy a böngésző a mentett haladást a megfelelő feladatokhoz társítsa.

Kézi szerkesztéshez a [Logikai szita](forras/feladatsorok/01-logikai-szita.json) jó minta. A feladatsor azonosítója legyen egyedi a gyűjteményben, a feladatazonosítók pedig a saját feladatsorukon belül legyenek egyediek. A fő témák azonosítói `logika`, `geometria`, `szamelmelet` és `merlegeles`.

## Fájlok a Git-repóban

| Fájl vagy mappa | Szerepe |
|---|---|
| [`index.html`](index.html) | A kész, böngészőben futó Játszóház |
| [`forras/feladatsorok/`](forras/feladatsorok/) | A feladatsorok szerkeszthető JSON-fájljai |
| [`forras/index.template.html`](forras/index.template.html) | A felület, a játéklogika és az ábrák sablonja |
| [`forras/build.py`](forras/build.py) | Ellenőrzi az adatokat és újragenerálja az `index.html`-t |
| `README.md` | Ez az útmutató |

## Telepítés ZIP-ből

A `matematika-jatszohaz-refaktor.zip` fájlt másold a játék mappájába, a meglévő `index.html` mellé. A mappában futtasd:

```bash
unzip -tq matematika-jatszohaz-refaktor.zip && unzip -o matematika-jatszohaz-refaktor.zip
```

A parancs ellenőrzi a csomagot, majd felülírja az `index.html`-t és kicsomagolja a `forras/` mappát. Sikeres telepítés után a ZIP törölhető a játék mappájából.
