# Simmer Rezepte

Rezeptdaten für die iOS-App **Simmer**. Die App prüft beim Start `version.json` und lädt
`recipes_de.json` / `recipes_en.json` neu, wenn die Version höher ist als ihre eigene.

- Nur Inhalte, kein Code.
- `version` bei jeder Änderung um 1 erhöhen (macht `publish.py` automatisch).
- `format` nur erhöhen, wenn sich die JSON-Struktur inkompatibel ändert (ältere Apps ignorieren das Update dann).
- Neue Rezepte ohne `"free": true` gehören zur Freischaltung; es bleiben genau 100 gratis.
- Rezepttexte immer in eigenen Worten, keine Köch:innen-Namen.
