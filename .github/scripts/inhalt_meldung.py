#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verarbeitet eine Inhalts-Meldung (GitHub-Issue-Formular „Inhalt melden")
und aktualisiert inhalte.json: fügt einen Link hinzu und/oder ändert das Status-Badge.

Aufruf:
  python3 inhalt_meldung.py vorschau  meldung.txt  ISSUE-NUMMER
  python3 inhalt_meldung.py anwenden  meldung.txt  ISSUE-NUMMER

Schreibt immer:  kommentar.md   (Text für den Issue-Kommentar)
Bei "anwenden" zusätzlich:  inhalte.json (aktualisiert) und commitmsg.txt

Rückgabewert 0 = in Ordnung, 1 = Meldung fehlerhaft (kommentar.md erklärt warum).
"""
import json
import re
import sys
from datetime import date, datetime

MARKER = "<!-- inhalt-vorschau -->"
STATUS_TEXT = {"b": "In Bearbeitung", "g": "Geprüft", "f": "Freigegeben"}


def heute():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Berlin")).date().isoformat()
    except Exception:
        return date.today().isoformat()


def parse_body(text):
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
            if k == "bereich" and teile != ("bereich",):
                continue
            if all(t in k for t in teile):
                v = v.strip()
                if v in ("_No response_", "None"):
                    v = ""
                return re.sub(r"\s+", " ", v).strip()
        return ""

    return {
        "bereich_roh": felder.get("bereich", "").strip() if felder.get("bereich", "").strip() not in ("_No response_", "None") else "",
        "titel": get("link", "titel"),
        "text": get("link", "beschreibung"),
        "link": get("link", "adresse"),
        "status_roh": get("status"),
        "beschreibung": get("beschreibung", "bereichs"),
    }


def pruefe(d, daten):
    fehler = []
    inhalte = daten.get("inhalte", {})
    schluessel = d["bereich_roh"].split("·")[0].strip().split()[0] if d["bereich_roh"] else ""
    bereich = schluessel if schluessel in inhalte else None
    if not bereich:
        fehler.append(f"Bereich nicht erkannt: „{d['bereich_roh'] or 'leer'}“ (Kennung wie a010, vdc, vorlagen …)")

    status = None
    s = d["status_roh"].strip().lower()
    if s and not s.startswith("keine"):
        m = re.match(r"^([bgf])\b", s)
        if m:
            status = m.group(1)
        else:
            fehler.append(f"Status nicht erkannt: „{d['status_roh']}“ (b, g oder f)")

    will_link = bool(d["titel"] or d["link"] or d["text"])
    if will_link:
        if not d["titel"]:
            fehler.append("Für einen neuen Link fehlt der Link-Titel.")
        if not d["link"]:
            fehler.append("Für einen neuen Link fehlt die Link-Adresse.")
        elif not re.match(r"^https?://\S+$", d["link"]):
            fehler.append(f"Die Link-Adresse sieht ungültig aus: „{d['link']}“ (sie muss mit https:// beginnen)")
    if not will_link and status is None and not d["beschreibung"]:
        fehler.append("Die Meldung enthält nichts zum Übernehmen: bitte einen Link eintragen, einen Status wählen oder eine Beschreibung schreiben.")

    link_schon_da = False
    if bereich and will_link and d["link"]:
        vorhandene = [e.get("link", "") for e in inhalte.get(bereich, {}).get("links", [])]
        if d["link"] in vorhandene:
            link_schon_da = True
            will_link = False
            if status is None and not d["beschreibung"]:
                fehler.append("Dieser Link ist in dem Bereich schon eingetragen — sonst enthält die Meldung nichts Neues.")
    d["link_schon_da"] = link_schon_da

    return bereich, status, will_link, fehler


def anwenden(daten, bereich, status, will_link, d):
    knoten = daten.setdefault("inhalte", {}).setdefault(bereich, {})
    neu_eintrag = None
    if will_link:
        eintrag = {"titel": d["titel"]}
        if d["text"]:
            eintrag["text"] = d["text"]
        eintrag["link"] = d["link"]
        knoten.setdefault("links", []).append(eintrag)
        neu_eintrag = eintrag
    alt_status = knoten.get("status")
    if status is not None:
        knoten["status"] = status
    if d["beschreibung"]:
        knoten["beschreibung"] = d["beschreibung"]
    daten["stand"] = heute()
    return neu_eintrag, alt_status


def schreibe(pfad, text):
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    modus = sys.argv[1]
    body = open(sys.argv[2], encoding="utf-8").read()
    nummer = sys.argv[3] if len(sys.argv) > 3 else "?"

    with open("inhalte.json", encoding="utf-8") as f:
        daten = json.load(f)

    d = parse_body(body)
    bereich, status, will_link, fehler = pruefe(d, daten)

    if fehler:
        text = MARKER + "\n**Diese Meldung kann noch nicht übernommen werden:**\n\n"
        text += "\n".join("- " + f for f in fehler)
        text += "\n\nBitte die Meldung oben über **Edit** (Stift beim ersten Beitrag) korrigieren — die Vorschau aktualisiert sich dann von selbst."
        schreibe("kommentar.md", text)
        sys.exit(1)

    ziel = daten if modus == "anwenden" else json.loads(json.dumps(daten))
    neu_eintrag, alt_status = anwenden(ziel, bereich, status, will_link, d)

    zeilen = []
    if d.get("link_schon_da"):
        zeilen.append(f"Hinweis: Der Link „{d['titel']}“ ist in **{bereich}** bereits eingetragen und wird übersprungen.")
    if neu_eintrag:
        zeilen.append(f"Neuer Link in **{bereich}**:\n```json\n" + json.dumps(neu_eintrag, ensure_ascii=False, indent=2) + "\n```")
    if status is not None:
        alt_t = STATUS_TEXT.get(alt_status, "kein Badge")
        zeilen.append(f"Status-Badge in **{bereich}**: {alt_t} → **{STATUS_TEXT[status]}**")
    if d["beschreibung"]:
        zeilen.append(f"Beschreibung in **{bereich}**:\n> " + d["beschreibung"])
    kern = "\n\n".join(zeilen)

    if modus == "vorschau":
        text = (MARKER + "**Vorschau der Meldung**\n\n" + kern +
                "\n\n**Freigabe:** Ein Mitglied des Kernteams kommentiert hier `/freigeben` — danach übernimmt die Automatik die Änderung selbst, und die Seite zeigt sie etwa eine Minute später.")
        schreibe("kommentar.md", text)
        return

    with open("inhalte.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(daten, ensure_ascii=False, indent=2) + "\n")
    kurz = []
    if neu_eintrag:
        kurz.append(f"Link „{d['titel']}“")
    if status is not None:
        kurz.append(f"Status {STATUS_TEXT[status]}")
    if d["beschreibung"]:
        kurz.append("Beschreibung")
    schreibe("commitmsg.txt", f"Inhalt: {bereich} — {' · '.join(kurz)} (#{nummer})")
    text = "**Übernommen.**\n\n" + kern + "\n\nDie Seite zeigt die Änderung in etwa einer Minute — einfach neu laden. Danke für die Meldung!"
    schreibe("kommentar.md", text)


if __name__ == "__main__":
    main()
