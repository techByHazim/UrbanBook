# Construction du réseau piéton

## Introduction  

L’objectif est de construire un réseau piéton cohérent pour l’analyse de l’accessibilité à l’échelle de la marche.  
En effet, il n’existe pas de base de données ouverte regroupant l’ensemble du réseau de voirie piétonne pour Marseille.  
Les données disponibles (OSMnx, IGN, etc.) présentent souvent des lacunes ou des incohérences :  
- routes mal classées,  
- escaliers manquants,  
- tronçons inadaptés,  
- ou encore mélange d’usages (routes partagées voiture/vélo/piéton).  

La démarche adoptée vise donc à **reconstruire un réseau piéton fiable** en plusieurs étapes, depuis les données OpenStreetMap jusqu’au traitement topologique.  


## Téléchargement des données OSM  

Les données OpenStreetMap (OSM) sont libres et collaboratives : des bénévoles enrichissent continuellement la base en ajoutant routes, bâtiments et infrastructures.  

Le 25 mai 2025, j’ai téléchargé le fichier **`.pbf`** de la région Provence-Alpes-Côte d’Azur via le site **[Geofabrik](https://download.geofabrik.de/europe/france.html)**.  
Ce fichier contient l’ensemble des données OSM de la région et constitue la base de départ pour l’extraction du réseau routier.  


## Définir ce qu’est un chemin piéton  

Une question clé est : *qu’est-ce qu’un chemin piéton et comment le filtrer dans OSM ?*  

Pour y répondre, je m’appuie sur les moteurs de calcul d’itinéraires (ex. Google Maps, Waze) qui adaptent les trajets au profil de l’usager (voiture, vélo, marche, etc.).  

De manière équivalente, le projet libre et open source **OSRM (Open Source Routing Machine)** utilise OSM pour générer des itinéraires.  
Son dépôt officiel contient un fichier **`foot.lua`** ([https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua](https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua)) décrivant les règles de filtrage du profil piéton.  

Ce profil définit les routes accessibles aux piétons et celles qui doivent être exclues (autoroutes, tunnels, certains accès restreints, etc.).  


## Adaptation du profil piéton OSRM  

Je ne cherche pas à calculer des itinéraires, mais à **extraire le réseau piéton**.  
Pour cela, je me réfère aux règles de `foot.lua` afin d’exclure :  
- les tronçons explicitement interdits aux piétons (`foot=no`),  
- les plateformes non pertinentes (`highway=platform`),  
- les autoroutes et routes majeures interdites à la marche.  

En revanche, je conserve tous les chemins explicitement piétonniers (`footway`, `path`, `pedestrian`, `steps`, etc.), ainsi que certaines routes partagées (résidentielles, tertiaires, etc.) adaptées à la marche.  


## Extraction avec Osmium et Python  

L’extraction est réalisée à l’aide de la bibliothèque **[pyosmium](https://osmcode.org/pyosmium/)**, qui permet de parcourir efficacement le fichier `.pbf`.  

Un script Python a été développé pour :  
1. Compter le nombre total de *ways* présents.  
2. Filtrer les tronçons en fonction des attributs `highway`, `foot`, `access` et autres tags OSM.  
3. Convertir les géométries en **`LineString` Shapely**.  
4. Sauvegarder les données dans un **GeoDataFrame (GeoPandas)**.  

```python
import osmium
import shapely.wkb as wkblib
import geopandas as gpd
from tqdm import tqdm

def extract_reseau(input_pbf):
    wkbfab = osmium.geom.WKBFactory()
    ways = []
    # ...
    # Filtrage selon le profil piéton (foot.lua adapté)
    # Construction du GeoDataFrame
    gdf = gpd.GeoDataFrame(ways, crs="EPSG:4326")
    return gdf
```


## Filtrage spatial sur Marseille

Le fichier OSM téléchargé couvre toute la région PACA.
Un **filtrage spatial** est appliqué pour conserver uniquement les tronçons situés à l’intérieur du périmètre de Marseille (bounding box ou shapefile de cadrage).

```python
# Exemple simplifié de filtrage spatial
cadre = gpd.read_file("cadre_marseille.shp")
gdf = gdf.to_crs(cadre.crs)
roads_mrs = gdf[gdf.geometry.within(cadre.iloc[0].geometry)]
```

## Conclusion

Cette méthodologie permet de passer d’un fichier brut OSM de la région PACA à un réseau piéton **adapté à l’analyse de la marche urbaine**.
Les étapes clés sont :

1. téléchargement des données OSM,
2. filtrage selon le profil piéton d’OSRM,
3. extraction avec Osmium,
4. sélection de la zone d’étude (Marseille),

Le réseau extrait reste brut et comporte encore des incohérences (géométries isolées, intersections mal définies, doublons, etc.). Ces problèmes seront corrigés dans la section suivante dédiée au traitement et à la simplification du réseau.



