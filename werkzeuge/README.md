# Werkzeuge (werden nicht mit der App ausgeliefert)

- `stimmen_erzeugen.py` – Zahlen-Ansage 1–100 als MP3 erzeugen (Piper) und mit Vosk auf Verständlichkeit prüfen. Mit `--s-stimmhaft` wird das S am Wortanfang weich gemacht, mit `--ziel` landen die Dateien erst zum Anhören in einem anderen Ordner.
- `s_stimmhaft.py` – aus der Fünfer-Bande übernommen: mischt dem scharfen S am Wortanfang ein Summen bei (weich wie in „Sonne“). Freigegebene Werte: Summen 0.55, Zischen 0.25.
- `ziffern_trainieren.py` – Handschrift-Erkennung (DIGIT_NET) neu trainieren.

Die Skripte laufen auf dem Rechner der Lehrkraft (Python 3). Details stehen im jeweiligen Kopfkommentar.
