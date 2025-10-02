# **Comment reproduire**

Le projet sera organisé en deux dépôts GitHub complémentaires :  
- **UrbanProximity** : le code et les scripts d’analyse  
- **UrbanBook** : la documentation associée  

Pour reproduire les calculs :  
- Cloner ou télécharger **UrbanProximity**.  
- Se placer dans le dossier principal du projet.  
- Installer puis activer l’environnement (voir [section precedente](environnement.md)).

Une fois l’environnement `geo_env` activé, le pipeline est prêt à être exécuté.

## **Structure du projet**

Voici l’arborescence générale :  

<style>
/* ===== Couleurs adaptatives (clair/sombre) ===== */
:root{
  --bg: #ffffff;
  --fg: #1f2937;         /* gris ardoise foncé */
  --muted: #6b7280;      /* gris moyen pour les notes */
  --line: #c7cdd4;       /* lignes d'arbre */
  --badge-border:#d1d5db;
  --badge-bg:#f9fafb;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg: #0b0f14;
    --fg: #6480b8ff;       /* texte principal clair */
    --muted: #9aa4b2;    /* notes lisibles en sombre */
    --line: #3a4856;     /* lignes plus douces en sombre */
    --badge-border:#334155;
    --badge-bg:#0f172a;
  }
}

/* ===== Reset léger pour ce bloc ===== */
.tree, .tree ul { list-style: none; margin: 0; padding-left: 1rem; position: relative; color: var(--fg); }
.kicker { margin:.5rem 0 .25rem; font-size:.95rem; color: var(--fg); }
.badge { display:inline-block; font-size:.75rem; padding:.1rem .4rem; border:1px solid var(--badge-border); border-radius:.4rem; background: var(--badge-bg); color: var(--fg); }
.note { color: var(--muted); font-style: italic; }
.folder { font-weight: 600; color: var(--fg); }
.file { font-weight: 500; color: var(--fg); }
hr.soft { border:0; border-top:1px dashed var(--line); margin:1rem 0; }

/* ===== Lignes de l'arbre ===== */
.tree:before, .tree ul:before {
  content: "";
  position: absolute;
  left: 0.5rem;
  border-left: 1px solid var(--line);
  top: 0; bottom: 0;
}
.tree li {
  margin: .25rem 0 .25rem 1rem;
  padding-left: .5rem;
  position: relative;
}
.tree li:before {
  content: "";
  position: absolute;
  left: -0.5rem;
  top: 0.75rem;
  width: 0.5rem;
  border-top: 1px solid var(--line);
}
/* Masque la ligne verticale résiduelle au dernier enfant,
   avec une couleur de fond adaptée au thème */
.tree li:last-child:after {
  content: "";
  position: absolute;
  left: 0.5rem;
  bottom: -0.25rem;
  height: calc(100% - 0.75rem);
  background: var(--bg);
  width: 2px;
}
</style>

<div class="kicker"> Arborescence :</div>

<ul class="tree">
  <li class="folder">📦 AttractiveCity
    <ul>
      <li class="folder">📂 proxy <span class="badge">Indicateurs de proximité</span>
        <ul>
          <li class="folder">📂 data
            <ul>
              <li class="folder">📂 raw <span class="note">données brutes</span></li>
              <li class="folder">📂 processed <span class="note">données nettoyées/intermédiaires</span></li>
              <li class="folder">📂 final <span class="note">résultats finaux (cartes, indicateurs)</span></li>
            </ul>
          </li>
          <li class="folder">📂 notebooks <span class="note">exploration &amp; prototypage</span></li>
          <li class="folder">📂 src <span class="note">scripts &amp; modules réutilisables</span>
            <ul>
              <li class="file">📄 bpe_prep.py <span class="note">préparation des données BPE</span></li>
              <li class="file">📄 config.py <span class="note">fichier de configuration</span></li>
              <li class="file">📄 diversity.py <span class="note">calcul de la diversité des équipements</span></li>
              <li class="file">📄 extract_pedestrian_roads.py <span class="note">extraction du réseau piéton</span></li>
              <li class="file">📄 main.py <span class="note">point d’entrée principal du pipeline</span></li>
              <li class="file">📄 osm_overpass.py <span class="note">requêtes OSM via Overpass API</span></li>
              <li class="file">📄 pipeline.py <span class="note">orchestration du pipeline</span></li>
              <li class="file">📄 project_to_network.py <span class="note">projection des équipements sur le réseau</span></li>
              <li class="file">📄 PyNkde.py <span class="note">implémentation NKDE (Network Kernel Density Estimation)</span></li>
              <li class="file">📄 read_data.py <span class="note">lecture et écriture des données</span></li>
              <li class="file">📄 simplified_roads.py <span class="note">simplification du réseau routier</span></li>
              <li class="file">📄 split_roads.py <span class="note">découpage du réseau en lixels</span></li>
              <li class="file">📄 transport_gtfs.py <span class="note">traitement des données GTFS</span></li>
            </ul>
          </li>
        </ul>
      </li>
      <li class="file">📄 requirements.yml <span class="note">environnement &amp; dépendances</span></li>
    </ul>
  </li>
</ul>

## **Fichiers essentiels pour le calcul**

Trois fichiers pilotent tout le calcul :  

- **`data/raw/insee/services_features.xlsx`** : définit les catégories d’équipements et leurs poids.  
  - Feuille *Categories of Amenities*  
  - Chaque ligne = un type d’équipement (ex. école, boulangerie)  
  - Colonnes = fonction sociale (`fs`), identifiant (`service_id`), poids (`wi`).  
  - Vous pouvez modifier les poids ou ajouter de nouvelles catégories.  

- **`config.py`** : tous les paramètres du calcul (zone, fichiers d’entrée, rayon de diversité, largeur de bande, etc.).  

- **`main.py`**:  point d’entrée du pipeline (lance tous les traitements avec les paramètres définis dans `config.py`).  

## **Paramètres à configurer dans** `config.py`

Le fichier `config.py` centralise la configuration. Voici les principaux paramètres à connaître et modifier si besoin :

### **Général**
- `epsg = 2154` : système de coordonnées (Lambert 93 pour la France).  
- `city = "Marseille"` : ville étudiée.  
- `year = 2023` : millésime de la BPE utilisé (2019, 2020, 2021, 2023, 2024 disponibles).  
- `date = "2025-10-01"` : date de génération des fichiers (sert à nommer les sorties).  
- `region = "PACA"` : région pour l’extraction OSM.  

### **Données d’entrée/sortie**
- `input_folder` : chemin vers les données brutes (`data/raw`).  
- `output_folder` : dossier pour les résultats intermédiaires (`data/processed`).  
- `output_final` : dossier pour les résultats finaux (`data/final`).  
- `cadre_file` : fichier GPKG représentant la zone d’étude (bbox autour de la ville).  

### **Fonctions sociales**

- `FS_LIST` : liste des fonctions sociales retenues (`education`, `provisioning`, `care`, etc.).  
  - Vous pouvez en ajouter ou en retirer selon vos besoins.  
- `poi_list_file` : fichier Excel des équipements (`services_features.xlsx`).  

```{admonition} Remarque
:class: important

`FS_LIST` et `poi_list_file` sont complémentaires.  
Les fonctions sociales listées dans `FS_LIST` doivent être **préalablement définies** dans le fichier `services_features.xlsx`,  
sinon elles seront **ignorées** lors du calcul.
```

### **Diversité**
- `div_radius` : rayon (mètres) utilisé pour mesurer la diversité autour de chaque équipement.  
- `poi_proj_files` : fichiers générés contenant les diversités calculées pour chaque fonction sociale.  

### **Réseau piéton**
- `input_pbf` : fichier OSM (format `.pbf`) téléchargé depuis Geofabrik.  
- `roads_file_mrs` : réseau piéton filtré sur la zone d’étude.  
- `roads_simplify_file` : version simplifiée du réseau.  

### **Lixelisation**
- `lixel_size` : longueur d’un lixel en mètres (plus petit = plus précis mais plus lourd).  
- `roads_lixels_file` : fichier contenant le réseau découpé en lixels.  

### **Paramètres de calcul de proximité**
- `kernel_type = "exponential"` : type de noyau utilisé (`exponential` ou `gaussian`).  
- `bandwidth` : largeur de bande (mètres). Plus elle est grande, plus l’influence des équipements s’étend loin.  
- `cutoff_factor` : facteur de coupure (`cutoff_factor` × `bandwidth`  = `cutoff`).  
- `graph_path` : chemin du graphe lixelisé (évite de le recalculer à chaque fois).  

### **OSM Overpass**
- `CONFIG_PATH` : fichier JSON définissant quels tags OSM extraire (ex. `amenity=pharmacy`).  
- `poi_file_additional` : fichiers générés contenant les équipements extraits via Overpass.  

### **Transports publics**
- `base_path` : fichier GTFS de la métropole Aix-Marseille-Provence (MAMP).  

### **Résultats**
- `output_paths` : fichiers finaux contenant les scores de proximité par fonction sociale.  



## **Lancer le pipeline**

Une fois tout paramétré, exécuter :  

```bash
python src/main.py
```
