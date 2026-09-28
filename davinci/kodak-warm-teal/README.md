# Kodak Warm Teal – DaVinci Resolve Look

Ein warmer Kodak-Print-Look im Content-Creator-Stil mit Teal-Schatten: Grün kippt nach Teal, die Haut bleibt sauber warm, die Lichter werden cremig.
Funktioniert in **Resolve Free und Studio**.

`preview_vorher_nachher.png` zeigt oben das Original und unten den kompletten Look (Graustufen, Hauttöne, Grün, Himmel, Farbverlauf).

## Dateien

| Datei | Zweck |
|---|---|
| `KWT_1_Hue.cube` | Grün → Teal, Blau → Cyan, Haut geschützt |
| `KWT_2_Split.cube` | Teal in den Schatten, warme Lichter (Helligkeit bleibt gleich) |
| `KWT_3_Print.cube` | Kodak-Print: S-Kurve, Dichte, weicher Highlight-Rolloff |
| `KWT_Full.cube` | Alles in einer LUT (Variante mit nur einem Node) |
| `KodakWarmTeal_Apply.py` | Setzt die LUTs in die Nodes und kopiert den Grade auf alle Clips |
| `make_luts.py` | Erzeugt die LUTs neu (Werte im Code anpassbar) |

Alle LUTs erwarten **Rec.709 (Gamma 2.4) als Eingang und geben Rec.709 aus**.

## 1. Installieren

**LUTs:** Die 4 `.cube`-Dateien in einen Ordner `KodakWarmTeal` im LUT-Ordner von Resolve kopieren:
- Windows: `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT\KodakWarmTeal\`
- macOS: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/KodakWarmTeal/`

Danach in Resolve: Color-Page → LUTs-Panel → Rechtsklick → **Refresh**.

**Skript:** `KodakWarmTeal_Apply.py` kopieren nach:
- Windows: `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Color\`
- macOS: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Color/`

## 2. Node-Tree einmal bauen (Template-Clip)

Einen typischen Clip auswählen und auf der Color-Page 13 serielle Nodes anlegen (`Alt+S` bzw. `Option+S`).
Die Nodes beschriften (Rechtsklick → Node Label):

| # | Label | Inhalt |
|---|---|---|
| 01 | CST IN | Color Space Transform: Kamera-Log → DaVinci Wide Gamut / DaVinci Intermediate |
| 02 | EXPO | Belichtung (HDR-Wheels Global Exposure oder Offset) |
| 03 | WB | Weißabgleich, Temp leicht warm (+200 bis +400) |
| 04 | CONTRAST | Contrast 1.05–1.15, Pivot 0.336 |
| 05 | SAT | Sättigung, Grün im Hue-vs-Sat etwas absenken |
| 06 | SKIN | HSL-Qualifier auf Haut, nur leichte Korrekturen |
| 07 | CST OUT | DWG/DI → Rec.709 Gamma 2.4, Tone Mapping „DaVinci“ |
| 08 | HUE | ← `KWT_1_Hue.cube` (setzt das Skript) |
| 09 | SPLIT | ← `KWT_2_Split.cube` (setzt das Skript) |
| 10 | KODAK | ← `KWT_3_Print.cube` (setzt das Skript) |
| 11 | VIGNETTE | Runde Power Window, invertiert, Exposure −0.3 |
| 12 | FX | Glow / Halation / Lens Blur (OpenFX, meist nur in Studio) |
| 13 | GRAIN | Film Grain 35 mm, niedrige Stärke (Studio) |

**Rec.709-Material** (Handy, nicht Log): Node 01 und 07 auf Bypass stellen (Node auswählen, `Strg+D`).

## 3. Skript starten

Playhead auf den Template-Clip setzen und **Workspace → Scripts → Color → KodakWarmTeal_Apply** aufrufen.
Das Skript setzt die LUTs in die Nodes 08–10 und kopiert den ganzen Grade auf alle Clips der Timeline.
Die Ausgabe siehst du unter Workspace → Console.

Danach pro Clip nur noch **02 EXPO** und **03 WB** anpassen.

## Stärke dosieren

Jeder Look-Node hat eine eigene Stärke: Key-Panel → **Key Output Gain** (1.0 = voll, 0.5 = halb).
Empfehlung für den Anfang: HUE 1.0, SPLIT 0.7, KODAK 0.8.

## Werte ändern

In `make_luts.py` z. B. die Teal-Stärke (`0.040 * w_sh`) oder die Wärme (`0.038 * w_hi`) ändern, dann
`python3 make_luts.py` ausführen (braucht `numpy`) und die neuen `.cube`-Dateien wieder kopieren.
