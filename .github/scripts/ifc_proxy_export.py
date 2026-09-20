"""
IFC-Export: Proxy-Elemente als CSV
Liest Elemente eines IFC-Typs aus einer IFC-Datei und schreibt
die gewünschten Attribute in eine CSV-Datei.

Voraussetzung:  pip install ifcopenshell
Aufruf:         python ifc_proxy_export.py modell.ifc ausgabe.csv
"""
import csv
import sys

# =====================================================================
# EINSTELLUNGEN — hier darf jede Niederlassung anpassen
# =====================================================================
IFC_TYP       = "IfcBuildingElementProxy"          # welcher Elementtyp
SPALTEN       = ["Name", "GUID", "Klassifikation"]  # welche Attribute
TRENNZEICHEN  = ";"                                 # ; für Excel (DE), , für Excel (EN)
NUR_MIT_KLASSIFIKATION = False                      # True = Elemente ohne Klassifikation überspringen
# =====================================================================
# LOGIK — bitte nicht ändern (Änderungen über Pull Request an das Kernteam)
# =====================================================================

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


def wert(element, spalte):
    if spalte == "Name": return element.Name or ""
    if spalte == "GUID": return element.GlobalId
    if spalte == "Klassifikation": return klassifikation(element)
    # weitere Attribute aus den Property-Sets
    for definition in getattr(element, "IsDefinedBy", []) or []:
        if definition.is_a("IfcRelDefinesByProperties"):
            pset = definition.RelatingPropertyDefinition
            for prop in getattr(pset, "HasProperties", []) or []:
                if prop.Name == spalte and hasattr(prop, "NominalValue") and prop.NominalValue:
                    return prop.NominalValue.wrappedValue
    return ""


def main(ifc_pfad, csv_pfad):
    modell = ifcopenshell.open(ifc_pfad)
    elemente = modell.by_type(IFC_TYP)
    with open(csv_pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=TRENNZEICHEN)
        w.writerow(SPALTEN)
        n = 0
        for e in elemente:
            zeile = [wert(e, s) for s in SPALTEN]
            if NUR_MIT_KLASSIFIKATION and "Klassifikation" in SPALTEN and not zeile[SPALTEN.index("Klassifikation")]:
                continue
            w.writerow(zeile); n += 1
    print(f"{n} Elemente nach {csv_pfad} geschrieben.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Aufruf: python ifc_proxy_export.py modell.ifc ausgabe.csv")
    main(sys.argv[1], sys.argv[2])
