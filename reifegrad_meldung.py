#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verarbeitet eine Reifegrad-Meldung (GitHub-Issue-Formular „Reifegrad melden")
und aktualisiert reifegrad.json.

Aufruf:
  python3 reifegrad_meldung.py vorschau  meldung.txt  ISSUE-NUMMER
  python3 reifegrad_meldung.py anwenden  meldung.txt  ISSUE-NUMMER

Schreibt immer:  kommentar.md   (Text für den Issue-Kommentar)
Bei "anwenden" zusätzlich:  reifegrad.json (aktualisiert) und commitmsg.txt

Rückgabewert 0 = in Ordnung, 1 = Meldung fehlerhaft (kommentar.md erklärt warum).
"""
import json
import re
import sys
from datetime import date, datetime

MARKER = "<!-- reifegrad-vorschau -->"
AWF_OK = {f"a{n:03d}" for n in range(10, 150, 10)}
STUFEN = {0: "nicht begonnen", 1: "geplant", 2: "Pilot", 3: "im Einsatz", 4: "Standard · Vorreiter"}


def heute():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Berlin")).date().isoformat()
    except Exception:
        return date.today().isoformat()


def parse_body(text):
    """Zerlegt den Issue-Text des Formulars: '### Überschrift' + Antwort darunter."""
    felder = {}
    key = None
    buf = []
    for line in text.splitlines():
        m = re.match(r"^###\s+(.+?)\s*$", line)
        if m:
            if key is not None:
                felder[key] = "\n".join(buf).strip()
            key = m.group(1).strip().lower()
            buf = []
        elif key is not None:
            buf.append(line)
    if key is not None:
        felder[key] = "\n".join(buf).strip()

    def get(*teile):
        for k, v in felder.items():
            if all(t in k for t in teile):
                v = v.strip()
                if v in ("_No response_", "None"):
                    v = ""
                return re.sub(r"\s+", " ", v).strip()
        return ""

    return {
        "awf_roh": get("anwendungsfall"),
        "ort": get("niederlassung"),
        "stufe_roh": get("stufe"),
        "person": get("ansprechperson"),
        "kontakt": get("mail"),
        "projekt": get("projekt"),
        "hinweis": get("hinweis"),
    }


def pruefe(d, daten):
    fehler = []
    m = re.search(r"a\d{3}", d["awf_roh"])
    awf = m.group(0) if m and m.group(0) in AWF_OK else None
    if not awf:
        fehler.append(f"Anwendungsfall nicht erkannt: „{d['awf_roh'] or 'leer'}“ (erwartet a010 … a140)")
    orte = daten.get("standorte", [])
    ort = d["ort"] if d["ort"] in orte else None
    if not ort:
        fehler.append(f"Niederlassung nicht erkannt: „{d['ort'] or 'leer'}“ (Schreibweise wie in reifegrad.json)")
    m2 = re.search(r"[0-4]", d["stufe_roh"])
    stufe = int(m2.group(0)) if m2 else None
    if stufe is None:
        fehler.append(f"Stufe nicht erkannt: „{d['stufe_roh'] or 'leer'}“ (0 bis 4)")
    for mail in re.split(r"\s*[·,;]\s*", d["kontakt"] or ""):
        if mail and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", mail):
            fehler.append(f"E-Mail sieht ungültig aus: „{mail}“")
    return awf, ort, stufe, fehler


def stufe_von(wert):
    if wert is None:
        return 0
    if isinstance(wert, dict):
        return int(wert.get("stufe", 0))
    return int(wert)


def anwenden(daten, awf, ort, stufe, d):
    """Trägt die Meldung ein. Leere Formularfelder lassen vorhandene Angaben unverändert.
    Stufe 0 ohne weitere Angaben entfernt den Eintrag."""
    karte = daten.setdefault("reifegrad", {}).setdefault(awf, {})
    alt = karte.get(ort)
    neu = dict(alt) if isinstance(alt, dict) else ({} if alt is None else {"stufe": alt})
    neu["stufe"] = stufe
    for feld in ("person", "kontakt", "projekt", "hinweis"):
        if d[feld]:
            neu[feld] = d[feld]
    extra = [k for k in ("person", "kontakt", "projekt", "hinweis") if str(neu.get(k, "")).strip()]
    if stufe == 0 and not extra:
        karte.pop(ort, None)
        wert = None
    elif not extra:
        karte[ort] = stufe
        wert = stufe
    else:
        wert = {"stufe": stufe}
        for k in ("person", "kontakt", "projekt", "hinweis"):
            if str(neu.get(k, "")).strip():
                wert[k] = neu[k]
        karte[ort] = wert
    daten["stand"] = heute()
    return alt, wert


def schreibe(pfad, text):
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    modus = sys.argv[1]
    body = open(sys.argv[2], encoding="utf-8").read()
    nummer = sys.argv[3] if len(sys.argv) > 3 else "?"

    with open("reifegrad.json", encoding="utf-8") as f:
        daten = json.load(f)

    d = parse_body(body)
    awf, ort, stufe, fehler = pruefe(d, daten)

    if fehler:
        text = MARKER + "\n**Diese Meldung kann noch nicht übernommen werden:**\n\n"
        text += "\n".join("- " + f for f in fehler)
        text += "\n\nBitte die Meldung oben über **Edit** (Stift beim ersten Beitrag) korrigieren — die Vorschau aktualisiert sich dann von selbst."
        schreibe("kommentar.md", text)
        sys.exit(1)

    alt_stufe = stufe_von(daten.get("reifegrad", {}).get(awf, {}).get(ort))

    # Für die Vorschau auf einer Kopie arbeiten, bei "anwenden" auf den echten Daten.
    ziel = daten if modus == "anwenden" else json.loads(json.dumps(daten))
    alt, wert = anwenden(ziel, awf, ort, stufe, d)

    zeile = f"**{awf} · {ort}:** {STUFEN[alt_stufe]} ({alt_stufe}) → {STUFEN[stufe]} ({stufe})"
    if wert is None:
        eintrag = "Der Eintrag wird entfernt (Stufe 0 ohne weitere Angaben)."
    else:
        eintrag = "Neuer Eintrag in `reifegrad.json`:\n```json\n" + json.dumps({ort: wert}, ensure_ascii=False, indent=2) + "\n```"

    if modus == "vorschau":
        text = MARKER + "**Vorschau der Meldung**\n\n" + zeile + "\n\n" + eintrag
        if alt_stufe == stufe and json.dumps(alt, sort_keys=True, ensure_ascii=False) == json.dumps(wert, sort_keys=True, ensure_ascii=False):
            text += "\n\nHinweis: Die Karte steht bereits auf diesem Stand."
        text += "\n\nLeere Formularfelder lassen vorhandene Angaben (Person, Projekt …) unverändert."
        text += "\n\n**Freigabe:** Ein Mitglied des Kernteams kommentiert hier `/freigeben` — danach trägt die Automatik die Änderung selbst ein und die Karte ist etwa eine Minute später aktuell."
        schreibe("kommentar.md", text)
        return

    # modus == "anwenden"
    with open("reifegrad.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(daten, ensure_ascii=False, indent=2) + "\n")
    schreibe("commitmsg.txt", f"Reifegrad: {awf} {ort} → Stufe {stufe} (#{nummer})")
    text = ("**Übernommen.** " + zeile +
            "\n\nDie Karte zeigt die Änderung in etwa einer Minute: einfach die Seite neu laden. Danke für die Meldung!")
    schreibe("kommentar.md", text)


if __name__ == "__main__":
    main()
