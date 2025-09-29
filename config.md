# Annexe X – Fichier de configuration 

Le fichier `config.py` rassemble l’ensemble des paramètres nécessaires à la préparation, au traitement et à l’analyse des données. Sa modification permet d’adapter le pipeline à d’autres contextes urbains ou à d’autres jeux de données.

* **Cadre général** : le système de coordonnées utilisé est le Lambert 93 (EPSG:2154). La ville étudiée par défaut est Marseille, mais ce paramètre peut être modifié pour d’autres territoires.
* **Organisation des répertoires** : les données brutes (INSEE, OSM, GTFS) sont stockées dans un dossier `raw`, les traitements intermédiaires dans `processed`, et les résultats finaux dans `final`.

* **Sources de données** :

  * *Équipements BPE (INSEE, 2023)* : filtrés sur la zone d’étude et enrichis par une table Excel décrivant les fonctions sociales et leurs poids.
  * *Équipements complémentaires (OSM via Overpass)* : jardins, boîtes aux lettres, marchés, location de vélos, parcs, etc.
  * *Réseau piéton (OSM)* : extrait en format `.pbf` (PACA), filtré et simplifié avant lixelisation.
  * *Transport public* : données GTFS fournies par la Métropole Aix-Marseille-Provence (réseau RTM).
  
* **Fonctions sociales retenues** : soins, approvisionnement, loisirs, éducation, travail, habitat, transport.
* **Paramètres de calcul** :

  * Diversité locale calculée dans un rayon de 80 m.
  * Réseau piéton découpé en lixels de 20 m.
  * Lissage spatial par noyau exponentiel (bande passante 200 m, coupure à 600 m).
* **Sorties** : scores d’accessibilité pour chaque fonction sociale (fichiers GPKG), ainsi qu’un fichier fusionné. Le graphe des lixels est également sauvegardé afin d’éviter les recalculs coûteux.


