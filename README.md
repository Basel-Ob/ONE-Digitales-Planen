# ONE Digitales Planen — Navigationsseite und Reifegrad-Karte

Seite: `https://basel-ob.github.io/ONE-Digitales-Planen/`
Pflege-Link (Kernteam): `https://basel-ob.github.io/ONE-Digitales-Planen/?pflege`

Die Seite liest drei Dateien: `reifegrad.json` (Reifegrad-Karte), `inhalte.json` (Links,
Status, Beschreibungen je Bereich) und `skripte.json` (freigegebene Skripte im Ordner
`skripte/`). Niemand bearbeitet diese Dateien von Hand: Änderungen kommen als **Meldung**
(Issue-Formular), die Automatik prüft sie, das Kernteam gibt mit dem Kommentar `/freigeben`
frei, die Automatik trägt ein.

## Datenschutz — die Regeln für diese Seite

Die Seite und dieses Repository sind **öffentlich erreichbar**. Deshalb gilt:

- **Keine E-Mail-Adressen.** Ansprechpersonen stehen nur mit Namen auf der Karte; erreichbar
  sind sie über das Firmenverzeichnis (Outlook, Teams). Das Formular kennt kein E-Mail-Feld
  mehr; die Automatik lehnt Meldungen ab, in denen eine Adresse steht.
- **Keine Kunden- oder Projektnamen** in Meldungen, Hinweisen, Beschreibungen und Link-Titeln.
- **Namen nur mit Einverständnis** der Person. Bis Datenschutz und Kernteam die Nennung
  echter Namen freigegeben haben: Feld „Ansprechperson" leer lassen oder eigene Person.
- Links auf den SharePoint sind unkritisch (ohne Anmeldung nicht erreichbar), verraten aber
  die Ordnerstruktur — bei sensiblen Bereichen lieber den Bibliothekslink als den Dateilink.

## Wer darf was

| Wer | braucht | darf |
|---|---|---|
| Alle Kolleginnen und Kollegen | den Link aus dem SharePoint | ansehen |
| Melden | ein GitHub-Konto | Meldung anlegen (Reifegrad, Inhalt, Wissenslücke) |
| Kernteam | Schreibrecht im Repository (Collaborator) | Meldungen freigeben — nur dann ändert sich etwas |

## Dateien

| Pfad | Aufgabe |
|---|---|
| `index.html` | die Seite, inkl. Pflege-Modus (`?pflege`) |
| `reifegrad.json` | Reifegrad je Anwendungsfall und Standort — Kurzform `"Essen": 3` oder `{"stufe": 4, "person": "…", "hinweis": "…"}` |
| `inhalte.json` | je Bereich: `status` (b/g/f) und `links` (titel, text, link) |
| `skripte.json` · `skripte/` | Skriptkatalog und die Dateien dazu (Änderung per Pull Request) |
| `.github/ISSUE_TEMPLATE/` | die Formulare: Reifegrad melden, Inhalt melden, Wissenslücke melden |
| `.github/workflows/` | die Automatik: Vorschau bei neuer Meldung, Eintragen nach `/freigeben`, JSON-Prüfung |
| `.github/scripts/` | die Python-Skripte der Automatik |

## Stufen der Reifegrad-Karte

0 nicht begonnen · 1 geplant · 2 Pilot · 3 im Einsatz · 4 Standard / Vorreiter.
Stufen werden gemeinsam bestätigt: Der Standort schlägt vor, das Kernteam gibt frei (4·2·2).
