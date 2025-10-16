# Déploiement d’un Jupyter Book avec GitHub Pages

## Préparer le projet

* J'ai mon dossier **UrbanBook** avec :

  * fichiers `.md` (notes) et `.ipynb` (notebooks avec sorties exécutées)
  * fichiers de config : `_config.yml`, `_toc.yml`
  * un dossier `images/` pour les logos et illustrations
* J'ajouter un fichier `.gitignore` pour exclure `_build/`, `__pycache__/`, etc.

## Initialiser GitHub

* Je crée un repo sur GitHub → **UrbanBook** (public pour que le site soit visible).
* Je lis mon projet local :

  ```bash
  git init
  git remote add origin https://github.com/techByHazim/UrbanBook.git
  git branch -M main
  git push --set-upstream origin main
  ```

## Configurer Jupyter Book

Dans `_config.yml` :

```yaml
title: Proximité urbaine
author: Hazim Moindze
logo: images/carte.png
language: fr

execute:
  execute_notebooks: "off"   # GitHub n’exécute pas mon code
```

Les notebooks doivent être **exécutés localement** et sauvegardés avec leurs sorties.

## Ajouter le workflow GitHub Actions

Dans `.github/workflows/deploy-book.yml` :

```yaml
name: Deploy Jupyter Book

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install Jupyter Book
      run: pip install jupyter-book ghp-import
    - name: Build the book
      run: jupyter-book build .
    - name: Deploy to GitHub Pages
      run: ghp-import -n -p -f _build/html
```

## Activer GitHub Pages

* Aller dans **Settings > Pages**
* Choisir :

  * **Source** → `Deploy from a branch`
  * **Branch** → `gh-pages`
* Le site sera disponible à :

  ```
  https://techByHazim.github.io/UrbanBook/
  ```
  
## Routine de travail

1. Je modifie mes `.md` ou `.ipynb` localement.
2. J'exécutes mes notebooks localement (pour avoir les sorties).
3. Je sauvegarde et pushe :

   ```bash
   git add .
   git commit -m "Mise à jour"
   git push
   ```
4. GitHub Actions rebuild et publie le site automatiquement 


Résultat :

* Je travaille **localement** (avec mes bibliothèques installées).
* GitHub ne fait que **mettre en ligne** ce que j'ai produit → pas d’erreurs pandas/numpy.
* Chaque `git push` = nouvelle version du site.


Pour supprimer un dossier suivi par Git

```bash
   ggit rm -r --cached .history
   ```

# Construction d’un réseau piéton

## Objectif

L’objectif est de construire un **réseau piéton cohérent** pour analyser l’accessibilité à l’échelle de la marche.

À ce jour, je n'ai trouvé aucune base ouverte complète regroupant l’ensemble du réseau piéton de Marseille.
Les sources disponibles présentent des lacunes et des incohérences :

* routes mal classifiées,
* trottoirs manquants,
* escaliers ou passages oubliés,
* tronçons partagés (voiture, vélo, piéton) difficiles à interpréter.

Cette section détaille ma démarche pour reconstruire un réseau praticable à pied, à partir des données **OpenStreetMap (OSM)**.


## Téléchargement des données OSM

Les données **OpenStreetMap** sont libres et collaboratives : des contributeurs enrichissent continuellement la base en ajoutant routes, bâtiments, équipements, etc.

Le **25 mai 2025**, j’ai téléchargé le fichier **`.pbf`** de la région Provence-Alpes-Côte d’Azur via **[Geofabrik](https://download.geofabrik.de/europe/france.html)**.
Ce fichier contient l’ensemble des données OSM de la région, y compris le réseau routier.


## Définir ce qu’est un chemin piéton

Ma question était :  

> *Qu’est-ce qu’un “chemin piéton”, et comment le filtrer correctement ?*

### Premiers tests : OSMnx et BDTOPO

J’ai d’abord testé **[OSMnx](https://osmnx.readthedocs.io/en/stable/)** pour extraire le réseau piéton :  

```python
import osmnx as ox

G = ox.graph_from_place("Marseille, France", network_type="walk")
nodes, edges = ox.graph_to_gdfs(G)
edges.to_file("marseille_walk_edges.gpkg", layer="edges", driver="GPKG")
nodes.to_file("marseille_walk_nodes.gpkg", layer="nodes", driver="GPKG")
```

Mais le mode `walk` s’est révélé trop **approximatif** :  

- certaines routes principales étaient incluses,  
- des escaliers ou petits chemins manquaient,  
- et de nombreux tronçons ne correspondaient pas à la réalité du terrain.  

J’ai ensuite testé le réseau de l’**[IGN - BDTOPO](https://geoservices.ign.fr/route500)**.  
Les géométries y sont plus précises, mais la base est **incomplète** pour la marche : beaucoup de passages piétons, d’escaliers ou de ruelles locales n’y figurent pas. En pratique, la BDTOPO décrit surtout les grands axes (autoroutes, nationales, départementales) et des éléments adaptés à une lecture à l’échelle régionale ou nationale.

Finalement, parmi toutes les sources ouvertes testées, le réseau **brut d’OSM** est **le plus complet**. Le seul enjeu est d’apprendre à filtrer intelligemment les données pour isoler ce qui correspond réellement à un chemin piéton.

### Inspiration : le profil *piéton* d’[OSRM](https://map.project-osrm.org/)

Pour définir mes propres règles de filtrage, je me suis appuyé sur le projet **[OSRM (Open Source Routing Machine)](https://github.com/Project-OSRM/osrm-backend)**,
un moteur de calcul d’itinéraires libre utilisant OSM.

OSRM propose un **profil “piéton”**, défini dans le fichier [https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua](https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua),
qui spécifie quelles routes sont autorisées ou interdites pour la marche.

````{dropdown} Cliquez ici pour afficher le profil piéton *foot.lua* d'OSRM
```lua
-- Foot profile

api_version = 2

Set = require('lib/set')
Sequence = require('lib/sequence')
Handlers = require("lib/way_handlers")
find_access_tag = require("lib/access").find_access_tag

function setup()
  local walking_speed = 5
  return {
    properties = {
      weight_name                   = 'duration',
      max_speed_for_map_matching    = 40/3.6, -- kmph -> m/s
      call_tagless_node_function    = false,
      traffic_signal_penalty        = 2,
      u_turn_penalty                = 2,
      continue_straight_at_waypoint = false,
      use_turn_restrictions         = false,
    },

    default_mode            = mode.walking,
    default_speed           = walking_speed,
    oneway_handling         = 'specific',     -- respect 'oneway:foot' but not 'oneway'

    barrier_blacklist = Set {
      'yes',
      'wall',
      'fence'
    },

    access_tag_whitelist = Set {
      'yes',
      'foot',
      'permissive',
      'designated'
    },

    access_tag_blacklist = Set {
      'no',
      'agricultural',
      'forestry',
      'private',
      'delivery',
    },

    restricted_access_tag_list = Set { },

    restricted_highway_whitelist = Set { },

    construction_whitelist = Set {},

    access_tags_hierarchy = Sequence {
      'foot',
      'access'
    },

    -- tags disallow access to in combination with highway=service
    service_access_tag_blacklist = Set { },

    restrictions = Sequence {
      'foot'
    },

    -- list of suffixes to suppress in name change instructions
    suffix_list = Set {
      'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'North', 'South', 'West', 'East'
    },

    avoid = Set {
      'impassable',
      'proposed'
    },

    speeds = Sequence {
      highway = {
        primary         = walking_speed,
        primary_link    = walking_speed,
        secondary       = walking_speed,
        secondary_link  = walking_speed,
        tertiary        = walking_speed,
        tertiary_link   = walking_speed,
        unclassified    = walking_speed,
        residential     = walking_speed,
        road            = walking_speed,
        living_street   = walking_speed,
        service         = walking_speed,
        track           = walking_speed,
        path            = walking_speed,
        steps           = walking_speed,
        pedestrian      = walking_speed,
        platform        = walking_speed,
        footway         = walking_speed,
        pier            = walking_speed,
      },

      railway = {
        platform        = walking_speed
      },

      amenity = {
        parking         = walking_speed,
        parking_entrance= walking_speed
      },

      man_made = {
        pier            = walking_speed
      },

      leisure = {
        track           = walking_speed
      }
    },

    route_speeds = {
      ferry = 5
    },

    bridge_speeds = {
    },

    surface_speeds = {
      fine_gravel =   walking_speed*0.75,
      gravel =        walking_speed*0.75,
      pebblestone =   walking_speed*0.75,
      mud =           walking_speed*0.5,
      sand =          walking_speed*0.5
    },

    tracktype_speeds = {
    },

    smoothness_speeds = {
    }
  }
end

function process_node(profile, node, result)
  -- parse access and barrier tags
  local access = find_access_tag(node, profile.access_tags_hierarchy)
  if access then
    if profile.access_tag_blacklist[access] then
      result.barrier = true
    end
  else
    local barrier = node:get_value_by_key("barrier")
    if barrier then
      --  make an exception for rising bollard barriers
      local bollard = node:get_value_by_key("bollard")
      local rising_bollard = bollard and "rising" == bollard

      if profile.barrier_blacklist[barrier] and not rising_bollard then
        result.barrier = true
      end
    end
  end

  -- check if node is a traffic light
  local tag = node:get_value_by_key("highway")
  if "traffic_signals" == tag then
    -- Direction should only apply to vehicles
    result.traffic_lights = true
  end
end

-- main entry point for processsing a way
function process_way(profile, way, result)
  -- the intial filtering of ways based on presence of tags
  -- affects processing times significantly, because all ways
  -- have to be checked.
  -- to increase performance, prefetching and intial tag check
  -- is done in directly instead of via a handler.

  -- in general we should  try to abort as soon as
  -- possible if the way is not routable, to avoid doing
  -- unnecessary work. this implies we should check things that
  -- commonly forbids access early, and handle edge cases later.

  -- data table for storing intermediate values during processing
  local data = {
    -- prefetch tags
    highway = way:get_value_by_key('highway'),
    bridge = way:get_value_by_key('bridge'),
    route = way:get_value_by_key('route'),
    leisure = way:get_value_by_key('leisure'),
    man_made = way:get_value_by_key('man_made'),
    railway = way:get_value_by_key('railway'),
    platform = way:get_value_by_key('platform'),
    amenity = way:get_value_by_key('amenity'),
    public_transport = way:get_value_by_key('public_transport')
  }

  -- perform an quick initial check and abort if the way is
  -- obviously not routable. here we require at least one
  -- of the prefetched tags to be present, ie. the data table
  -- cannot be empty
  if next(data) == nil then     -- is the data table empty?
    return
  end

  local handlers = Sequence {
    -- set the default mode for this profile. if can be changed later
    -- in case it turns we're e.g. on a ferry
    WayHandlers.default_mode,

    -- check various tags that could indicate that the way is not
    -- routable. this includes things like status=impassable,
    -- toll=yes and oneway=reversible
    WayHandlers.blocked_ways,

    -- determine access status by checking our hierarchy of
    -- access tags, e.g: motorcar, motor_vehicle, vehicle
    WayHandlers.access,

    -- check whether forward/backward directons are routable
    WayHandlers.oneway,

    -- check whether forward/backward directons are routable
    WayHandlers.destinations,

    -- check whether we're using a special transport mode
    WayHandlers.ferries,
    WayHandlers.movables,

    -- compute speed taking into account way type, maxspeed tags, etc.
    WayHandlers.speed,
    WayHandlers.surface,

    -- handle turn lanes and road classification, used for guidance
    WayHandlers.classification,

    -- handle various other flags
    WayHandlers.roundabouts,
    WayHandlers.startpoint,

    -- set name, ref and pronunciation
    WayHandlers.names,

    -- set weight properties of the way
    WayHandlers.weights
  }

  WayHandlers.run(profile, way, result, data, handlers)
end

function process_turn (profile, turn)
  turn.duration = 0.

  if turn.direction_modifier == direction_modifier.u_turn then
     turn.duration = turn.duration + profile.properties.u_turn_penalty
  end

  if turn.has_traffic_light then
     turn.duration = profile.properties.traffic_signal_penalty
  end
  if profile.properties.weight_name == 'routability' then
      -- penalize turns from non-local access only segments onto local access only tags
      if not turn.source_restricted and turn.target_restricted then
          turn.weight = turn.weight + 3000
      end
  end
end

return {
  setup = setup,
  process_way =  process_way,
  process_node = process_node,
  process_turn = process_turn
}
```

````

Ce profil m’a servi de référence conceptuelle :  
- exclure les tronçons interdits (`foot=no`, `access=private`, `highway=platform`, etc.),  
- conserver les voies explicitement piétonnes (`footway`, `path`, `pedestrian`, `steps`, etc.),  
- et tolérer certaines routes partagées (`residential`, `living_street`, `service`, …).  


## Extraction avec Osmium

Pour extraire le réseau piéton, j’utilise la bibliothèque **[Osmium pour Python](https://osmcode.org/pyosmium/)**, familièrement appelée *PyOsmium*.  
C’est une interface Python de la bibliothèque C++ Osmium, qui permet de lire et filtrer les fichiers OpenStreetMap au format `.pbf`.

Contrairement à des outils comme **OSMnx**, Osmium ne charge pas tout le fichier en mémoire : il lit les données en continu (*streaming*). C’est beaucoup plus rapide et stable quand on travaille sur des bases de grande taille comme celle de la région PACA.

```{admonition} Note technique
:class: tip
Le terme **Osmium** peut désigner trois choses :
- **Osmium** : la bibliothèque C++ d’origine,  
- **PyOsmium** : son interface Python (importée sous le nom `osmium`),  
- **osmium-tool** : un outil en ligne de commande pour manipuler les fichiers OSM.  
```

Ici, j’utilise bien la **bibliothèque Python `osmium`**.


### Étapes principales

Voici les principales opérations réalisées lors de l’extraction du réseau piéton :

```{figure} ../images/roads_osm_foot.png
:name: fig-extraction-reseau-pieton
:alt: Schéma des étapes principales d’extraction du réseau piéton
:width: 80%
:align: center
```

````{dropdown} Afficher / masquer le code Python
```python
import osmium
import shapely.wkb as wkblib
import geopandas as gpd
from tqdm import tqdm

from config import (
    input_pbf
)

def extract_reseau():
    wkbfab = osmium.geom.WKBFactory()
    ways = []
    total_ways = 0

    class WayCounter(osmium.SimpleHandler):
        def way(self, w):
            nonlocal total_ways
            total_ways += 1

    print("Counting ways...")
    counter = WayCounter()
    counter.apply_file(str(input_pbf), locations=False)
    print(f"Total number of ways: {total_ways}")

    print("Extracting pedestrian network...")
    pbar = tqdm(total=total_ways, desc="Processing ways")

    class FootwayHandler(osmium.SimpleHandler):
        def way(self, w):
            try:
                tags = w.tags
                highway = tags.get('highway', '')
                access = tags.get('access', '')
                foot = tags.get('foot', '')
                
                highway_whitelist = [
                    'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary',
                    'tertiary_link', 'unclassified', 'residential', 'road', 'living_street',
                    'service', 'track', 'path', 'steps', 'pedestrian', 'platform',
                    'footway', 'pier'
                ]
                if highway not in highway_whitelist:
                    pbar.update(1)
                    return
                
                # Filtrer foot=no
                if foot == 'no':
                    pbar.update(1)
                    return

                # Filtrer highway=platform
                if highway == 'platform':
                    pbar.update(1)
                    return
                
                wkb = wkbfab.create_linestring(w)
                geom = wkblib.loads(wkb, hex=True)

                way_info = {
                    'osm_id': w.id,
                    'geometry': geom,
                    'highway': highway,
                    'name': tags.get('name', ''),
                    'access': access,
                    'foot': foot,
                    'surface': tags.get('surface', ''),
                    'incline': tags.get('incline', ''),
                    'smoothness': tags.get('smoothness', ''),
                    'width': tags.get('width', ''),
                    'sidewalk': tags.get('sidewalk', ''),
                    'crossing': tags.get('crossing', ''),
                    'lit': tags.get('lit', ''),
                    'bridge': tags.get('bridge', ''),
                    'tunnel': tags.get('tunnel', ''),
                    'layer': tags.get('layer', '0'),  # '0' par défaut si non renseigné
                    'oneway': tags.get('oneway', 'no')  # 'no' par défaut si non renseigné
                }
                ways.append(way_info)

            except Exception as e:
                print(f"Error processing way {w.id}: {e}")
            finally:
                pbar.update(1)

    handler = FootwayHandler()
    handler.apply_file(str(input_pbf), locations=True)
    pbar.close()

    gdf = gpd.GeoDataFrame(ways, crs="EPSG:4326")
    return gdf
```

````

## Filtrage spatial sur Marseille  

Le fichier `.pbf` couvre toute la région PACA.  
J’applique ensuite un **filtrage spatial** pour ne garder que les tronçons à l’intérieur du périmètre de Marseille :

```python
# Filtrage spatial
cadre = gpd.read_file("data/raw/personal/CadreMarseille.gpkg")
gdf = gdf.to_crs(cadre.crs)
roads_mrs = gdf[gdf.geometry.within(cadre.geometry.iloc[0])]
```

## Conclusion
J'ai montré la d"marche me permettant de passer d’un fichier brut `.pbf` OSM couvrant toute la région PACA à un **réseau piéton** inspiré de OSRM centré sur Marseille. 

```{admonition} À venir
:class: note
Le réseau obtenu présente encore quelques imperfections (tronçons isolés, doublons ou intersections manquantes, etc) qu’il ne faut pas négliger pour les analyses de proximité sur le réseau.  
La prochaine étape consistera donc à **nettoyer et simplifier le réseau** afin de le rendre exploitable pour les calculs de distance et de d'accessiblité piétonne.
```