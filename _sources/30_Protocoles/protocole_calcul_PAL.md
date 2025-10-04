# Protocole de calcul du PAL

1. Préparer le **réseau piéton** (OSM, profils OSRM).
2. Charger les **aménités** (BPE millésime, OSM tags → mapping).
3. Appliquer les **pondérations** (table *parametrages.md*).
4. Calculer l’**accessibilité** le long du graphe (distance à pied).
5. Agréger densité/diversité et normaliser → **PAL**.
6. Exporter les résultats (formats, CRS) avec **métadonnées**.
7. Enregistrer versions (données, code, env.) dans *carnet_resultats.md*.