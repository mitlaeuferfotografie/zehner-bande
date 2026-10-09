# Die Zehner-Bande – Anweisung für Claude Code

Stand: 09.10.2026. Diese Datei ist die Übergabe aus der Entwicklung in Claude (Cowork) an Claude Code.

## Deine Rolle
Du arbeitest für eine Grundschullehrkraft in NRW (Musik und Deutsch, unterrichtet auch Mathe). Antworte auf **Deutsch** und sprich sie mit **Du** an. **Hinterfrage Ideen kritisch** und beschönige nichts. Die Kinder sind in Klasse 2 (7–8 Jahre). Texte in der App: kurz, kindgerecht, fehlerfrei. Zahlwörter und Rechenwege genau prüfen.

## Was die App ist
Lern-App für Zahlen bis 100 (Klasse 2), angelehnt an die *Idee* des Blitzrechnens: kurze, tägliche Übungen zu Grundvorstellungen. Inhalte und Gestaltung sind eigene, nichts von Klett übernehmen und den Namen „Blitzrechnen“ nicht verwenden. Figuren: **Zacki Zehner** (blaue Zehnerstange) und **Emil Einer** (grüner Einerwürfel, gibt die Tipps).

- Live: https://mitlaeuferfotografie.github.io/zehner-bande/ (mit Spracherkennung: `?sprache=1`)
- Repo: https://github.com/mitlaeuferfotografie/zehner-bande, Branch `main`. **Das Repo ist der maßgebliche Stand.**
- Lokaler Ordner der Lehrkraft: `C:\Users\BrandschP\Documents\ClaudeArbeitsordner\Matheunterricht\Zehner-Bande App\` mit Sicherungen (`ZehnerBande TT_MM_JJ.txt`), Unterlagen und `Anweisung_Cowork_Zehner-Bande.md` (ausführliche fachliche Beschreibung, gern lesen). Der Ordner kann hinter dem Repo zurückliegen.
- Schwester-Apps (gleiche Technik, gleiches Belohnungsschema): `redezeichen-helden`, `verben_expedition`, `pronomen-magie`, `AdjektiveDetektiv`, `MatheAgent`. Gemeinsame Regeln: `…\ClaudeArbeitsordner\Deutschunterricht\Anweisung_Cowork_Lern-Apps_Allgemein.md`.

## Feste Regeln (nicht verhandelbar)
1. **Datenschutz:** keine Drittanbieter. Kein CDN, kein Google Fonts, keine Analyse, keine externen Bilder oder Skripte. Kein Backend, **kein localStorage**, keine Cookies, keine Namen. **Es wird kein Fortschritt gespeichert** (Sterne nur pro Runde, Banden-Code am 09.10.2026 entfernt). Beim Laden und Spielen dürfen nur Dateien von `mitlaeuferfotografie.github.io` abgerufen werden.
2. **Spracherkennung und Vorlesen nur auf dem Gerät.** Keine Web Speech API zur Erkennung (die schickt Audio an Google, Apple oder Microsoft) und keine Online-Stimmen.
3. **Vor jedem Push mit der Lehrkraft absprechen.** Sie testet vorher (lokal bauen und ihr zeigen) und gibt frei.
4. **Rechtstext** (`ImpressumModal`) nur nach ausdrücklicher Freigabe ändern. Offene Vorschläge stehen unten.
5. **Kein Punkte- oder Speichersystem wieder einbauen**, ohne die Lehrkraft zu fragen (bewusste Entscheidung, siehe „Zahlenraum und Sterne“).
6. Tailwind-Klassen immer **vollständig** ausschreiben (nie `` `bg-${farbe}-500` ``), sonst fehlen sie im Build.
7. Nach jeder Änderung `src/App.jsx` als Sicherung `ZehnerBande TT_MM_JJ.txt` (bei mehreren am Tag `… V2.txt`) in den lokalen Ordner legen und bei grundlegenden Änderungen diese Datei und `Anweisung_Cowork_Zehner-Bande.md` nachführen.

## Technik
- React 18, **eine Datei** `src/App.jsx` (ca. 2.300 Zeilen), Icons `lucide-react@^0.577.0`, Tailwind CSS v3 beim Bauen erzeugt. Schriften Fredoka und Bangers lokal in `public/fonts/`.
- Bauen und Veröffentlichen: `.github/workflows/pages.yml` (esbuild + Tailwind CLI). Er kopiert `public/fonts`, `public/vosk` und `public/audio` nach `_site`. Nach dem Push ist die Seite in ca. 2 Minuten live (`gh run watch`).
- **Lokal bauen und testen** (gleiche Befehle wie in `pages.yml`, Schritt „App bauen“):
  ```
  mkdir build _site && cp -r src build/src && cd build && npm init -y
  npm install react@18.1.0 react-dom@18.1.0 lucide-react@^0.577.0 esbuild tailwindcss@3
  npx esbuild src/index.js --bundle --minify --loader:.js=jsx --jsx=automatic --define:process.env.NODE_ENV='"production"' --outfile=../_site/bundle.js
  npx tailwindcss@3 -i src/tailwind-input.css -o ../_site/tailwind.css --content "src/**/*.{js,jsx},../public/index.html" --minify
  ```
  Dann `public/fonts`, `public/vosk`, `public/audio` nach `_site/` kopieren, `index.html` wie in `pages.yml` erzeugen und `_site` über einen lokalen Webserver öffnen (z. B. `npx serve _site`). Mikrofon funktioniert nur über `localhost` oder https.
- Lehrer-Bereich: Zahnrad, Passwort **`Bande100`** (vor dem echten Einsatz ändern, Konstante `ADMIN_PASSWORD`).

## Aufbau von `src/App.jsx` (Suchbegriffe)
| Bereich | Suchbegriff |
|---|---|
| Farben (Dienes: **Einer grün, Zehner blau, Hunderter rot**, Lösungen violett) | `const COL` |
| Zahlwörter, Bausteine, Zahlendreher | `zahlwort`, `zahlwortParts`, `zahlwortDistractors`, `isDreher` |
| Zufallszahlen | `pickNumbers`, `practiceNumbers` (ca. 80 % Zahlen mit möglichem Zahlendreher; bis 10: 1–10) |
| Einstellungen und Link-Parameter | `readUrlSettings` (`?zr=10/20/100` → `zrFromLink`, `?blitz=0–3`, `?stimme=thorsten/ramona/geraet`, `?sprache=1`) |
| Zahlenraum | `ZAHLENRAEUME`, `GAMES_BIS_10`, `gameAllowed`, Startbild `gameState === 'zahlenraum'`, `chooseZahlenraum` |
| Zahlen-Ansage | `FILE_VOICES`, `playNumber`, `useSpeak` (MP3 aus `public/audio/<stimme>/<n>.mp3`, sonst Gerätestimme) |
| Darstellungen | `HundredField` (5er-Lücke), `TensOnes` (Dienes inkl. Hunderterplatte), `ColorNumber`, `ZEExplain` |
| Eingabe | `NumPad`, `HandwriteNumber` / `WritePad` / `recognizeDigit` / `DIGIT_NET` (Handschrift, MLP 784–128–10) |
| Übungen | `BlitzblickGame` („Wie viele sind es?“), `ZeigenGame`, `LegenGame` (Ziehen vom Material-Tisch), `SchreibenGame`, `HoerenGame`, `DiktatGame`, `ZahlwortGame`, `SprechenGame` |
| Spracherkennung (Test) | `loadVoskModel`, `grammarFor`, `parseSpokenNumber`, `MIN_CONF`, `useNumberListener` |
| Liste der Übungen, Lernpfade | `GAMES`, `PATHS` (im Menü gefiltert: `visiblePaths`), `UNLOCK_REQ = {}` (alles frei, so gewünscht) |
| Lehrer-Bereich, Impressum | `AdminControlModal`, `ImpressumModal` |
| Arbeitsblätter (A4, Druck-CSS) | `SHEETS`, `makeSheetItems`, `SheetContent`, `SheetStudio` |
| Hilfe-Texte | `GAME_HELP` |

## Zahlenraum und Sterne (seit 09.10.2026)
- Startbild: Das Kind wählt **bis 10 / bis 20 / bis 100**. „Bis 50“ gibt es nicht mehr. Mit `?zr=` im Link entfällt das Startbild. Wechsel über den Knopf „bis …“ oben rechts.
- **Bis 10** nur 5 Übungen (`GAMES_BIS_10`): Wie viele sind es?, Zahlen zeigen (Zehnerstreifen), Hör-Detektiv (Falschangebote ±1/±2), Zahlen-Diktat (Z-Feld optional), Sprech-Probe. Legen, Schreiben und Zahlwort-Baukasten sind ausgeblendet. Tipps und Arbeitsblatt-Texte haben eigene Fassungen (`task10`).
- **Punktefeld je Zahlenraum** (`fieldRows`): bis 10 Zehnerstreifen, bis 20 Zwanzigerfeld (2 Reihen), bis 100 Hunderterfeld – in „Wie viele sind es?“, „Zahlen zeigen“ und auf den Arbeitsblättern (`task20`, `desc20`). Bis 20 wird immer das ganze Feld gezeigt, auch in der Streifen-Ansicht (`fullField`).
- **Schreibfelder** (`WritePad`, `side`): H/Z/E liegen ohne Abstand nebeneinander, schmaler als hoch (Breite 0,8 × size), zarte Rahmen in der Stellenwert-Farbe, dazwischen nur eine gestrichelte Linie – die Ziffern sollen als *eine Zahl* wirken (Wunsch der Lehrkraft).
- **Nur Runden-Sterne:** kein Banden-Code, keine Abzeichen, kein „Das kann ich schon:“, keine Gesamt-Sterne. Menü-Karten zeigen den besten Wert dieser Sitzung im aktuellen Zahlenraum, beim Wechsel wird er zurückgesetzt. Grund: Die App lebt vom täglichen Wiederholen; Sterne aus verschiedenen Zahlenräumen wären nicht vergleichbar; der Code war für Klasse 2 eine Hürde.

## Die 8 Übungen (je 10 Aufgaben, max. 10 Sterne, Sterne = beim ersten Versuch richtig)
1. `blitzblick` **Wie viele sind es?** – Bild 3 s, „Nochmal ansehen“ bis 3×, danach bleibt es stehen. Antwort mit dem Finger (H/Z/E) oder tippen. Bei richtiger Antwort wird das Zahlwort vorgesprochen (+ „Nochmal hören“).
2. `zeigen` **Zahlen zeigen** – im Punktefeld tippen. Die Zahl wird bei jeder Aufgabe vorgesprochen (Knopf „Hören“ zum Wiederholen) und bei richtiger Lösung noch einmal. Die Anzahl erscheint erst nach „Prüfen“ (so gewünscht).
3. `legen` **Zahl legen** – Material-Tisch mit 10 Zehnerstangen und 10 Einerwürfeln, auf die Lege-Matte ziehen (Pointer-Events) oder antippen. 10 Einer → Tausch-Knopf.
4. `schreiben` **Zahl schreiben** – Material, Stellentafel, Z/E-Angaben (auch vertauscht, Bündel-Aufgabe). Antwort mit dem Finger. Bei richtiger Antwort wird das Zahlwort vorgesprochen (+ „Nochmal hören“).
5. `hoeren` **Hör-Detektiv** – Zahl hören, aus 4 wählen (Zahlendreher, ±10, ±1).
6. `diktat` **Zahlen-Diktat** – Zahl hören und mit dem Finger schreiben.
7. `zahlwort` **Zahlwort-Baukasten** – Zahlwort aus Bausteinen mit Falsch-Bausteinen.
8. `sprechen` **Sprech-Probe** – laut sprechen, Selbstkontrolle. Optional Spracherkennung (TEST).

## Wichtige Formate
- **Spracherkennung:** vosk-browser (`public/vosk/vosk.js`), deutsches Modell in **zwei Teilen** `public/vosk/vosk-model-small-de-0.15.tar.gz.teil1/.teil2` (je ca. 23 MB, werden im Browser zusammengesetzt; GitHub-Weboberfläche erlaubt max. 25 MB pro Datei). Pro Aufgabe eine **kleine Wortliste** (`grammarFor`: Zielzahl, Zahlendreher, ±1, ±10, ein paar andere), Sicherheitsschwelle `MIN_CONF = 0.8`, Mikrofon bleibt an und puffert 1 s. Messung mit Computerstimme: 28/34 richtig, 1–2 falsch, Zahlendreher 16/16, nie fälschlich „richtig“. **Mit echten Kinderstimmen noch nicht ausreichend getestet.** Die graue „Test-Info“-Zeile ist für die Auswertung gedacht und muss vor dem echten Einsatz weg oder in den Lehrer-Bereich.
- **Zahlen-Ansage:** `public/audio/thorsten/1–100.mp3` (**Standard, von der Lehrkraft bevorzugt**), `public/audio/ramona/…`. 0,35 s Stille vorne, damit Tablets den Anfang nicht abschneiden. Neu erzeugen: `werkzeuge/stimmen_erzeugen.py`.

## Eigene Stimme (geplant)
Die Lehrkraft möchte später ihre eigene Stimme verwenden. Vorgehen: Sie nimmt eins bis hundert auf (eine Datei mit Pausen oder 100 Einzeldateien). Dann schneiden (z. B. ffmpeg `silencedetect`), jedes Wort mit dem Filter aus `stimmen_erzeugen.py` (`AF`) bearbeiten, als `public/audio/<name>/<n>.mp3` speichern, in `FILE_VOICES` eintragen, gegebenenfalls als Standard setzen (`readUrlSettings` → `voiceChoice`) und jede Datei anhören bzw. mit Vosk prüfen.

## Offene Punkte
- **Impressum/Datenschutz** am 09.10.2026 mit Freigabe aktualisiert: Banden-Code-Satz ersetzt („Sterne nur für die aktuelle Runde“), neuer Abschnitt 3 „Mikrofon, Spracherkennung und Vorlesen“, Lizenzzeilen (vosk-browser/Vosk-Modell Apache 2.0, Piper MIT, Thorsten-Voice CC0, M-AILABS-Lizenz, MNIST CC BY-SA 3.0 mit Urhebern), Stand Oktober 2026. Ändert sich an Mikrofon, Stimmen oder Speicherung etwas, muss dieser Text mit (nur nach Freigabe).
- **Übungspass** (Papier zum Ausmalen nach jeder Runde) als Ersatz für das Speichern: von der Lehrkraft gewünscht, noch nicht gebaut.
- Spracherkennung mit Kindern testen. Die Lehrkraft meldet die Test-Info-Zeilen, damit lässt sich `MIN_CONF` einstellen.
- Handschrift 1/7: Seit 09.10.2026 prüft `refineOneSeven` bei 1 oder 7 zusätzlich den Schreibweg (Querstrich bzw. flacher Strich oben → 7; steiler Aufstrich unterhalb der Spitze oder senkrechter Strich → 1). Mit simulierten Strichen getestet (8/8 richtig, 0/2/3/4/9 unverändert). **Mit echten Kinderschriften auf dem iPad noch testen.**
- Eintrag der App in `Anweisung_Cowork_Lern-Apps_Allgemein.md` (Tabelle „Die Apps“) und neue Aufgabentypen in `Baukasten_Aufgabentypen.md` stehen noch aus.
- Auf echten iPads testen: Ziehen, Fingerschreiben, Ton, Mikrofon, Ladezeit (ca. 50 MB bei eingeschalteter Spracherkennung).

## Prüfliste nach Änderungen
- Betroffene Übung einmal komplett durchspielen, keine Fehler in der Browser-Konsole.
- Alle drei Zahlenräume (10, 20, 100) kurz prüfen: richtige Übungen im Menü, passende Zahlen.
- Handybreite (390 px): kein waagerechtes Scrollen.
- Arbeitsblätter: Druckvorschau A4, jede Übung, mit Lösungsblatt.
- Netzwerk: nur eigene Dateien.
