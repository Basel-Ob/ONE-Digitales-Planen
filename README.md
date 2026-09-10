# ONE Digitales Planen — Struktur-Demo

| Datei | Zweck |
|---|---|
| `index.html` | Navigationsseite |
| `inhalte.json` | Titel, Text und Links je Knoten (Anwendungsfälle, VDC, Vorlagen, Agenten …) + Status |
| `skripte.json` | Liste der Skripte |
| `skripte/` | Skript-Dateien |

## Link ergänzen (z. B. bei AwF 020)
`inhalte.json` → Stift → unter `"a020"` in die eckigen Klammern von `"links"` einfügen:
```json
{ "titel": "Steckbrief", "text": "Karte als Markdown", "link": "https://…" }
```
Mehrere Einträge mit Komma trennen. Optional `"status": "b"` / `"g"` / `"f"` für das Badge.

## Kennungen
Anwendungsfälle: `a010` … `a140` · Bereiche: `vdc`, `vorlagen`, `software`, `projekte`, `team`, `dim`, `gis` ·
Agenten: `ps-vertrag`, `ps-fertig`, `ps-monitor`, `ps-analyse`, `ps-praes`, `ps-proto`, `fp-handbuch`, `fp-grundlagen`, `fp-leistung`, `bim-awf`, `bim-workflow`, `bim-daten`, `bim-skript`, `bim-prozess`, `bim-ifc`
