"""
IFC-Export: Proxy-Elemente als CSV
Liest alle IfcBuildingElementProxy aus einer IFC-Datei und schreibt
Name, GUID und Klassifikation in eine CSV-Datei.

Voraussetzung:  pip install ifcopenshell
Aufruf:         python ifc_proxy_export.py modell.ifc ausgabe.csv
"""
import csv
import sys

try:
    import ifcopenshell
except ImportError:
    sys.exit("ifcopenshell fehlt: pip install ifcopenshell")


def klassifikation(element):
    """Erste zugeordnete Klassifikationsreferenz (falls vorhanden)."""
    for rel in getattr(element, "HasAssociations", []) or []:
        if rel.is_a("IfcRelAssociatesClassification"):
            ref = rel.RelatingClassification
            return getattr(ref, "Identification", None) or getattr(ref, "Name", "") or ""
    return ""


def main(ifc_pfad, csv_pfad):
    modell = ifcopenshell.open(ifc_pfad)
    elemente = modell.by_type("IfcBuildingElementProxy")
    with open(csv_pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Name", "GUID", "Klassifikation"])
        for e in elemente:
            w.writerow([e.Name or "", e.GlobalId, klassifikation(e)])
    print(f"{len(elemente)} Elemente nach {csv_pfad} geschrieben.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Aufruf: python ifc_proxy_export.py modell.ifc ausgabe.csv")
    main(sys.argv[1], sys.argv[2])
