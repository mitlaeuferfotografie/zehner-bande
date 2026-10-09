# Die Zehner-Bande

Lern-App für Zahlen bis 100 (Klasse 2): Mengen schnell erfassen, Zahlen zeigen und legen, Zehner und Einer, Zahlen hören, schreiben und sprechen – mit Arbeitsblatt-Generator.

- React 18, Einzeldatei `src/App.jsx`, Tailwind CSS v3 beim Bauen erzeugt, Schriften lokal in `public/fonts/` (SIL OFL).
- Keine Drittanbieter, kein Backend, kein localStorage. Sterne nur pro Runde, es wird nichts gespeichert.
- Beim Start wählt das Kind den Zahlenraum: bis 10, bis 20 oder bis 100.
- Veröffentlichung über GitHub Pages (`.github/workflows/pages.yml`, Quelle „GitHub Actions“).
- Einstellungen per Link: `?zr=10|20|100&blitz=0|1|2|3` (mit `zr` entfällt das Auswahlbild)
