# Produire les indicateurs de proximité

```{admonition} Objectif
:class: note
Une fois l’environnement configuré et les fichiers essentiels identifiés, cette section explique comment **paramétrer** et **exécuter** le calcul des indicateurs de proximité.
```

## Préparer l’environnement

Avant toute exécution :
1. Activez votre environnement :
   ```bash
   conda activate geo_env
   ```
2. Placez-vous à la racine du projet :
   ```bash
   cd path/to/Proximity
   ```
3. Vérifiez que les dossiers `data/raw`, `data/processed` et `data/final` existent (sinon créez-les).


## Le fichier `config.py` — centre de pilotage

Le fichier `src/config.py` regroupe **tous les paramètres** du projet : chemins, zones d’étude, paramètres de calcul et sorties.  
C’est **le seul fichier à modifier** pour adapter le pipeline à une autre ville, un autre millésime ou de nouvelles fonctions sociales.

### Configuration générale
- `epsg` : système de coordonnées (Lambert 93 pour la France).  
- `city` : nom de la ville étudiée (ex. `"Marseille"`).  
- `year` : millésime des données BPE (ex. 2023 ou 2024).  
- `region` : région pour les extractions OSM.  
- `date` : date de génération (sert à nommer les sorties).

### Chemins des données
- `input_folder`, `output_folder`, `output_final` : dossiers racine des entrées, sorties intermédiaires et résultats finaux.  
- `cadre_file` : fichier GPKG représentant la zone d’étude (souvent une boîte englobante créée sous QGIS).

### Fonctions sociales et équipements
- `FS_LIST` : liste des fonctions sociales prises en compte (éducation, approvisionnement, soin, etc.).  
- `poi_list_file` : table Excel `services_features.xlsx` listant les équipements et leurs poids par fonction sociale.

```{admonition} Remarque
:class: important
Les fonctions sociales déclarées dans `FS_LIST` doivent être présentes dans le fichier `services_features.xlsx`.  
Sinon, elles seront ignorées lors du calcul.
```

### Réseau piéton et lixels
- `input_pbf` : fichier `.pbf` d’OSM téléchargé (ex. via Geofabrik).  
- `roads_file_mrs`, `roads_simplify_file` : fichiers réseau filtré et simplifié.  
- `lixel_size` : longueur des lixels en mètres (10 m par défaut).

### Calcul de la proximité
- `kernel_type` : type de noyau utilisé (`"exponential"` ou `"gaussian"`).  
- `bandwidth` : largeur de bande (en mètres).  
- `cutoff_factor` : facteur de coupure du noyau (`cutoff = cutoff_factor × bandwidth`).  
- `div_radius` : rayon utilisé pour mesurer la diversité des équipements.  

### Sorties et résultats
- `output_paths` : chemins des fichiers finaux contenant les scores de proximité par fonction sociale.  
- `graph_path` : graphe lixelisé sauvegardé pour accélérer les recalculs.


## Lancer le pipeline

Une fois les paramètres ajustés dans `config.py`, le pipeline complet s’exécute avec :

```bash
python src/main.py
```

Le script lit automatiquement les paramètres définis dans `config.py`, traite les données d’entrée, calcule les indicateurs et enregistre les résultats dans `data/final`.

```{admonition} Astuce
:class: success
Vous pouvez adapter `config.py` à n’importe quelle autre ville ou jeu de données :  
le pipeline se reconfigurera automatiquement sans modifier le code source.
```


## Résultats attendus

À la fin du calcul :
- Les **données intermédiaires** (réseau, points projetés, diversités) sont enregistrées dans `data/processed/`.
- Les **scores finaux de proximité** sont exportés dans `data/final/`, un fichier par fonction sociale (au format GeoPackage).

```{admonition} Exemple
:class: note

`data/final/score_education_d80m_bw200m_Cut800m_lxl_10m_Marseille_2025-10-01.gpkg`

Ce fichier contient les **scores de proximité** calculés pour la fonction sociale **éducation**.  
Le nom du fichier encode directement les principaux **paramètres du calcul**, ce qui permet de retracer les conditions de production des résultats :

| Élément du nom de fichier | Signification |
|----------------------------|----------------|
| `education` | Fonction sociale analysée |
| `d80m` | Rayon de diversité : 80 mètres |
| `bw200m` | Largeur de bande du noyau : 200 mètres |
| `Cut800m` | Rayon de coupure : 800 mètres (soit 4 × 200 m) |
| `lxl_10m` | Taille des lixels du réseau : 10 mètres |
| `Marseille` | Ville étudiée |
| `2025-10-01` | Date de génération du calcul |

Cette convention de nommage rend chaque sortie **auto-descriptive** :  
il est possible de comprendre les paramètres du modèle sans ouvrir le fichier ni consulter le code.

