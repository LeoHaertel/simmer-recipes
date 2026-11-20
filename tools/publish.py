#!/usr/bin/env python3
"""Neue Rezepte für Simmer online stellen.

Aufruf:  python3 publish.py <ordner-mit-recipes_de.json-und-recipes_en.json> <repo-ordner>

Prüft beide Dateien, kopiert sie ins Repo und erhöht die Versionsnummer in version.json,
wenn sich etwas geändert hat. Danach im Repo committen und pushen.
"""
import json, os, shutil, sys

SECTIONS = {"gemuese", "brot", "fleisch", "kuehl", "trocken", "konserven", "gewuerze", "tiefkuehl", "vorrat"}
REQUIRED = ["id", "title", "emoji", "summary", "minutes", "servings", "difficulty", "vegetarian", "ingredients", "steps"]

def check(path):
    data = json.load(open(path, encoding="utf-8"))
    assert isinstance(data, list) and data, f"{path}: leer oder kein Array"
    for r in data:
        for k in REQUIRED:
            assert k in r, f"{path}: {r.get('id')} fehlt '{k}'"
        assert r["steps"], f"{path}: {r['id']} hat keine Schritte"
        for st in r["steps"]:
            t = st.get("timer")
            assert t is None or (isinstance(t, int) and t > 0), f"{path}: {r['id']} Timer muss ganze Minuten sein"
        for i in r["ingredients"]:
            assert i.get("section") in SECTIONS, f"{path}: {r['id']} unbekannte Abteilung {i.get('section')}"
            assert "id" in i and "name" in i and "unit" in i, f"{path}: {r['id']} Zutat unvollständig"
    ids = [r["id"] for r in data]
    assert len(ids) == len(set(ids)), f"{path}: doppelte IDs"
    return data

src, repo = sys.argv[1], sys.argv[2]
de = check(os.path.join(src, "recipes_de.json"))
en = check(os.path.join(src, "recipes_en.json"))
assert [r["id"] for r in de] == [r["id"] for r in en], "DE und EN haben unterschiedliche IDs/Reihenfolge"
free = sum(1 for r in de if r.get("free"))
assert free == 100, f"Es müssen genau 100 Gratis-Rezepte sein, sind {free}"

changed = False
for name in ("recipes_de.json", "recipes_en.json"):
    a, b = os.path.join(src, name), os.path.join(repo, name)
    if not os.path.exists(b) or open(a, "rb").read() != open(b, "rb").read():
        shutil.copyfile(a, b)
        changed = True

vpath = os.path.join(repo, "version.json")
manifest = json.load(open(vpath)) if os.path.exists(vpath) else {"version": 0, "format": 1}
if changed:
    manifest["version"] += 1
    json.dump(manifest, open(vpath, "w"), indent=1)
    print(f"Neue Version {manifest['version']}: {len(de)} Rezepte ({free} gratis)")
else:
    print(f"Keine Änderung, bleibt Version {manifest['version']}")
