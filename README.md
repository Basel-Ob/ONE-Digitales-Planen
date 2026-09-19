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

## Reifegrad-Karte

Die Karte öffnet sich oben rechts über **Reifegrad-Karte**, über den Link in der Legende oder direkt mit der Adresse `…/#reifegrad` (für einen Anwendungsfall: `…/#reifegrad=a010`).

- **Gesamtbild:** Farbe = höchste Stufe am Standort, Zahl im Punkt = Anwendungsfälle im Einsatz
- **Anwendungsfall links wählen:** Farbe = Stufe für genau diesen AwF, rechts die Ansprechpersonen
- **Standort anklicken:** alle Einträge des Standorts und die Mitglieder des BIM-Clusters
- **Matrix:** alle 20 Niederlassungen × 14 Anwendungsfälle auf einen Blick

### Stufen

| Stufe | Bedeutung | Vorschlag für die Einstufung |
|---|---|---|
| 0 | nicht begonnen | Noch keine Anwendung am Standort |
| 1 | geplant | In einem Projekt vorgesehen, noch nicht umgesetzt |
| 2 | Pilot | In einem Projekt erprobt, Erfahrungen liegen vor |
| 3 | im Einsatz | In laufenden Projekten regelmäßig genutzt |
| 4 | Standard · Vorreiter | Etabliert, der Standort kann andere anleiten |

Die Kriterien in der rechten Spalte sind ein Vorschlag und sollten im Kernteam bestätigt werden.

### Aktualisieren – Weg 0: Melden (empfohlen)

Niemand bearbeitet dabei eine Datei — die Automatik übernimmt das Eintragen.

1. Auf der Karte **Melden** klicken (oder in GitHub: **Issues › New issue › Reifegrad melden**)
2. Formular ausfüllen: Anwendungsfall, Niederlassung, Stufe — optional Person, E-Mail, Projekt
3. Absenden. Die Automatik prüft die Meldung und zeigt eine **Vorschau** als Kommentar
4. Jemand aus dem Kernteam kommentiert **`/freigeben`** — die Automatik trägt die Änderung selbst in `reifegrad.json` ein, committet und schließt die Meldung
5. Nach etwa einer Minute sehen alle die neue Karte

Hinweise: Melden braucht ein kostenloses GitHub-Konto (Ansehen weiterhin nicht). Leere Formularfelder lassen vorhandene Angaben (Person, Projekt …) unverändert. Stufe 0 ohne weitere Angaben entfernt den Eintrag. Wer im Seiten-Editor genau eine Änderung vorbereitet hat, bekommt über **Als Meldung senden** das fertig ausgefüllte Formular.

Technik: `.github/ISSUE_TEMPLATE/reifegrad-meldung.yml` (Formular), `.github/workflows/meldung-verarbeiten.yml` und `.github/scripts/reifegrad_meldung.py` (Automatik). Für offene Fragen gibt es zusätzlich das Formular **Wissenslücke melden** (`wissensluecke.yml`).

### Aktualisieren – Weg 1: in der Seite (Rückfallweg ohne Formular)

1. Seite öffnen → **Reifegrad-Karte** → **Bearbeiten**
2. Standort auf der Karte oder Zelle in der Matrix anklicken (oder rechts auswählen)
3. Stufe, Ansprechperson, E-Mail, Projekt eintragen → **Übernehmen** (die Karte zeigt die Änderung sofort, gespeichert ist sie noch nicht)
4. **Kopieren** → **GitHub öffnen** → dort Strg+A, Strg+V → **Commit changes**
5. Nach etwa einer Minute sehen alle die neue Karte. Das Datum „Stand“ setzt die Seite automatisch.

Wer kein Schreibrecht im Repository hat, klickt statt Schritt 4 auf **Als Vorschlag senden**. Das öffnet ein vorausgefülltes GitHub-Issue für das Kernteam.

### Aktualisieren – Weg 2: direkt in der Datei

`reifegrad.json` → Stift → Zeile ändern → **Commit changes**.

```json
"a010": {
  "Essen": { "stufe": 4, "person": "Vorname Nachname", "kontakt": "vorname.nachname@obermeyer-group.com", "projekt": "Bad Bevensen", "hinweis": "kurz" },
  "Erfurt": 2
}
```

- Kurzform `"Erfurt": 2` reicht, wenn es (noch) keine Ansprechperson gibt.
- Nicht genannte Standorte gelten als Stufe 0.
- Mehrere Personen oder E-Mails mit ` · ` trennen.
- Zwischen zwei Einträgen steht ein Komma, nach dem letzten keins.
- `"stand"` auf das heutige Datum setzen (JJJJ-MM-TT).

### Neue Niederlassung

Name in `"standorte"` ergänzen und die Lage angeben:

```json
"koordinaten": { "Rostock": [12.10, 54.09] }
```

(Längengrad, Breitengrad). Danach erscheint der Punkt auf der Karte und in der Matrix.

### Automatische Prüfung

`.github/workflows/json-pruefung.yml` prüft nach jeder Änderung alle JSON-Dateien: Schreibfehler, Stufen außerhalb 0–4, falsch geschriebene Standorte, ungültige E-Mails. Ein roter Haken im Repository zeigt die Stelle. Die Seite selbst meldet eine fehlerhafte `reifegrad.json` oben in der Karte.

Falls der Ordner `.github` beim Hochladen fehlt: **Add file › Create new file**, als Name `.github/workflows/json-pruefung.yml` eingeben und den Inhalt der Datei einfügen.

### Lokal geöffnet

Per Doppelklick geöffnet (ohne GitHub Pages) zeigt die Seite Beispieldaten. Mit **reifegrad.json öffnen** in der Kopfzeile der Karte lässt sich die echte Datei laden.
