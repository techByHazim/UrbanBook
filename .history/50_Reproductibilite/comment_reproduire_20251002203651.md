# Produire les indicateurs

Le projet sera organisé en deux dépôts GitHub complémentaires :  
- **UrbanProximity** : le code et les scripts d’analyse  
- **UrbanBook** : la documentation associée  

Pour reproduire les calculs :  
- Cloner ou télécharger **UrbanProximity**.  
- Se placer dans le dossier principal du projet.  
- Installer puis activer l’environnement (voir [Environnement du projet](environnement.md)).

Une fois l’environnement `geo_env` activé, le pipeline est prêt à être exécuté.

## Paramètres de configuration

Le fichier `config.py` centralise la configuration. Voici les principaux paramètres à connaître et modifier si besoin :

### Général
- `epsg = 2154` : système de coordonnées (Lambert 93 pour la France).  
- `city = "Marseille"` : ville étudiée.  
- `year = 2023` : millésime de la BPE utilisé (2019, 2020, 2021, 2023, 2024 disponibles).  
- `date = "2025-10-01"` : date de génération des fichiers (sert à nommer les sorties).  
- `region = "PACA"` : région pour l’extraction OSM.  

### Données d’entrée/sortie
- `input_folder` : chemin vers les données brutes (`data/raw`).  
- `output_folder` : dossier pour les résultats intermédiaires (`data/processed`).  
- `output_final` : dossier pour les résultats finaux (`data/final`).  
- `cadre_file` : fichier GPKG représentant la zone d’étude (bbox autour de la ville).  

### Fonctions sociales

- `FS_LIST` : liste des fonctions sociales retenues (`education`, `provisioning`, `care`, etc.).  
  - Vous pouvez en ajouter ou en retirer selon vos besoins.  
- `poi_list_file` : fichier Excel des équipements (`services_features.xlsx`).  

```{admonition} Remarque
:class: important

`FS_LIST` et `poi_list_file` sont complémentaires.  
Les fonctions sociales listées dans `FS_LIST` doivent être préalablement définies dans le fichier `services_features.xlsx`, sinon elles seront ignorées lors du calcul.
```

### Diversité
- `div_radius` : rayon (mètres) utilisé pour mesurer la diversité autour de chaque équipement.  
- `poi_proj_files` : fichiers générés contenant les diversités calculées pour chaque fonction sociale.  

### Réseau piéton
- `input_pbf` : fichier OSM (format `.pbf`) téléchargé depuis Geofabrik.  
- `roads_file_mrs` : réseau piéton filtré sur la zone d’étude.  
- `roads_simplify_file` : version simplifiée du réseau.  

### Lixelisation
- `lixel_size` : longueur d’un lixel en mètres (plus petit = plus précis mais plus lourd).  
- `roads_lixels_file` : fichier contenant le réseau découpé en lixels.  

### Paramètres de calcul de proximité
- `kernel_type = "exponential"` : type de noyau utilisé (`exponential` ou `gaussian`).  
- `bandwidth` : largeur de bande (mètres). Plus elle est grande, plus l’influence des équipements s’étend loin.  
- `cutoff_factor` : facteur de coupure (`cutoff_factor` × `bandwidth`  = `cutoff`).  
- `graph_path` : chemin du graphe lixelisé (évite de le recalculer à chaque fois).  

### OSM Overpass
- `CONFIG_PATH` : fichier JSON définissant quels tags OSM extraire (ex. `amenity=pharmacy`).  
- `poi_file_additional` : fichiers générés contenant les équipements extraits via Overpass.  

### Transports publics
- `base_path` : fichier GTFS de la métropole Aix-Marseille-Provence (MAMP).  

### Résultats
- `output_paths` : fichiers finaux contenant les scores de proximité par fonction sociale.  



## Lancer le pipeline

Une fois tout paramétré, exécuter :  

```bash
python src/main.py
```
