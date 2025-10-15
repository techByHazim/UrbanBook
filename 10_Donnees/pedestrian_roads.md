
# Extraction du réseau piéton avec OSMnx

**Hypothèse de travail :**
> *Tout segment de voie praticable à pied appartient au réseau piéton, qu’il soit public ou privé.*

## Les outils disponibles

Deux outils majeurs permettent de travailler sur un réseau piéton issu d’OSM :

1. **[OSMnx](https://osmnx.readthedocs.io/en/stable/)**
   → bibliothèque Python pour **télécharger**, **construire** et **analyser** des graphes urbains (piéton, vélo, voiture, etc.).

2. **[OSRM](https://project-osrm.org/)**
   → moteur de **routage** capable de calculer des itinéraires selon des profils (`car`, `bike`, `foot`, …).

Ces outils utilisent des **profils prédéfinis** qui filtrent automatiquement les types de voies selon les modes de déplacement autorisés.


## Extraction du réseau piéton avec OSMnx

OSMnx propose différents types de réseaux :
`drive` (voitures), `bike` (vélos), `walk` (piétons) ou `all` (toutes voies).

Nous utilisons ici le **profil “walk”**, qui conserve uniquement les voies accessibles aux piétons (trottoirs, allées, chemins, escaliers, etc).

```python
import osmnx as ox
import geopandas as gpd

# Chargement du périmètre d'étude
cadre = gpd.read_file("../../Proximity/data/raw/personal/CadreMarseille.gpkg")
cadre = cadre.to_crs("EPSG:4326")  # Conversion en coordonnées WGS84
polygon = cadre.geometry.iloc[0]

# Extraction du réseau piéton
G = ox.graph_from_polygon(polygon, network_type='walk', simplify=True, retain_all=False)
```

Le graphe `G` est un **MultiDiGraph** : un graphe **orienté** où plusieurs arêtes peuvent relier les mêmes nœuds (ex. deux sens de circulation).

* `simplify=True` fusionne les segments redondants entre intersections.
* `retain_all=False` conserve seulement le **plus grand composant connexe**, assurant la continuité du réseau.

### Les filtres du profil “walk”

OSMnx applique automatiquement un filtre pour sélectionner les voies piétonnes :

```python
["highway"]["area"!~"yes"]["access"!~"private"]
["highway"!~"abandoned|bus_guideway|construction|cycleway|motor|no|planned|platform|proposed|raceway|razed"]
["foot"!~"no"]["service"!~"private"]
```

Ce filtre exclut les autoroutes, zones privées ou pistes cyclables isolées, et conserve les voies ouvertes aux piétons.


### Vérification du graphe obtenu

```python
# Fonction pour afficher quelques infos sur le graphe
def graph_info(G):
    print(f"Type du graphe : {type(G).__name__}")
    print(f"Nombre de nœuds : {G.number_of_nodes()}")
    print(f"Nombre d’arêtes : {G.number_of_edges()}")
    print(f"Est orienté : {G.is_directed()}")
    print(f"Est connexe : {nx.is_weakly_connected(G) if G.is_directed() else nx.is_connected(G)}")

graph_info(G)
```

```
Type du graphe : MultiDiGraph
Nombre de nœuds : 113230
Nombre d’arêtes : 302816
Est orienté : True
Est connexe : True
```

**À retenir :**

* `G` est un **graphe orienté** (chaque arête a un sens) ;
* Les arêtes possèdent des **attributs** : `oneway`, `length`, `name`, `highway`, `geometry`, etc.
* `u` = nœud origine, `v` = nœud destination.

  * Si `oneway=False`, deux arêtes sont créées (`u→v` et `v→u`).

**Astuce:**
On lit d’abord la **structure topologique** (qui relie quoi), puis la **géométrie spatiale** (où cela se trouve réellement).

### Visualisation du graphe

Le graphe peut etre orienté (tient compte du sens de circulation) ou non orienté :

#### a) Graphe topologique orienté

J'extrais une petite partie du graphe et j'affiche le graphe grace à `nx.draw()`.

```python
# Trouver un nœud central
center_node = list(G.nodes())[len(G)//2]

# Extraire un sous-graphe dans un rayon de 600 m
subG = ox.truncate.truncate_graph_dist(G, center_node, max_dist=600)

plt.figure(figsize=(7,6))
nx.draw(subG, node_size=20, edge_color='gray', node_color='red')
plt.show()
```

::: {card}

```{figure} ../images/graph_topo.png
:alt: Graphe topologique du réseau piéton à Marseille
:width: 100%
```

**Graphe topologique orienté (OSMnx, profil “walk”)**
:::

Les points rouges représentent les intersections, les traits gris les connexions (avec un sens implicite).

#### b) Graphe non orienté

On peut ignorer les sens de circulation : 

```python
subG_undirected = subG.to_undirected()

plt.figure(figsize=(7,6))
nx.draw(subG_undirected, node_size=20, edge_color='gray', node_color='red')
plt.show()
```

::: {card}

```{figure} ../images/graph_undirect.png
:alt: Graphe non orienté du réseau piéton à Marseille
:width: 100%
```

**Graphe topologique non orienté (OSMnx, profil “walk”)**
:::

Ici, les arêtes ne sont plus directionnelles : elles indiquent simplement qu’une connexion existe entre deux nœuds. 

#### c) Graphe géographique

Pour visualiser le réseau dans l’espace réel, la fonction `ox.plot_graph` permet de le faire. Il prend en compte des coordonnées GPS des nodes et des egdes.

```python
fig, ax = plt.subplots(figsize=(9, 20))
ox.plot_graph(subG, ax=ax, node_size=20, node_color='red', edge_color='gray', bgcolor='white')
plt.show()
```

::: {card}

```{figure} ../images/graph_geo.png
:alt: Graphe géographique du réseau piéton à Marseille
:width: 100%
```

> Le **graphe géographique** montre les nœuds et arêtes selon leurs **coordonnées GPS**.
> :::

### Export du réseau vers QGIS

On peut extraire les nœuds et arêtes du graphe sous forme de GeoDataFrames et les sauvegarder pour un usage SIG.

```python
nodes, edges = ox.graph_to_gdfs(G)

# Sauvegarde en GeoPackage (format compatible QGIS)
edges.to_file("marseille_walk_edges.gpkg", layer="edges", driver="GPKG")
nodes.to_file("marseille_walk_nodes.gpkg", layer="nodes", driver="GPKG")
```

::: {card}

```{figure} ../images/omsnx_walk.png
:alt: Extrait des arêtes du réseau piéton (profil “walk”)
:width: 100%
```

**Extrait des arêtes du réseau piéton (OSMnx, mode “walk”)**
:::

Le réseau obtenu est **géométriquement précis**, mais certaines voies semi-publiques ou internes manquent à cause du filtre “walk”.
Cela necessite des ajustements manuels ou un profil personnalisé pour améliorer la couverture afin d'obtenrir un réseau piéton complet.
 
## Vers un profil piéton personalisé

### Le profil piéton OSRM `foot.lua`

Le profil `foot.lua` d’OSRM définit trois listes principales pour construire le réseau piéton : 

Extrait (voir le profil complet : [foot.lua](https://github.com/Project-OSRM/osrm-backend/blob/master/profiles/foot.lua)) : 

```lua
highway = {primary,primary_link,secondary,secondary_link,tertiary,tertiary_link,unclassified,residential,road,living_street ,service,track,path,steps,pedestrian,platform,footway,pier}

access_tag_whitelist = { 'yes', 'foot', 'permissive', 'designated' }
access_tag_blacklist = {'no', 'private', 'delivery','agricultural', 'forestry' }
```

- **`highway`** : indique les types de routes considérées comme marchables, depuis les grands axes (`primary`, `secondary`) jusqu’aux voies locales (`residential`, `service`, `path`, `footway`, `pier`).  
- **`access_tag_whitelist`** : répertorie les accès autorisés ou tolérés, comme les rues publiques (`yes`), les itinéraires piétons (`foot`), les accès libres (`permissive`) ou désignés (`designated`).  
- **`access_tag_blacklist`** : regroupe les accès interdits ou restreints, tels que les propriétés privées (`private`), les zones de livraison (`delivery`), les chemins agricoles (`agricultural`) ou forestiers (`forestry`).  

En pratique, OSRM inclut une route si elle figure dans la liste `highway` et que son accès est autorisé (liste blanche). Elle l’exclut si elle correspond à un cas de la liste noire.

### Positionnement

Dans une logique d’**accessibilité potentielle**, je m’intéresse à la faisabilité physique de la marche plutôt qu’à la réglementation. Je  construit le réseau piéton à partir d’OpenStreetMap en s’alignant sur le profil `foot.lua` d'OSRM. Concrètement, je reprends la liste des types highway autorisés par `foot.lua`, j’exclus les tronçons interdits aux piétons (foot=no), j'accepte ceux dont l’accès est restreint (access=|private|delivery|agricultural|forestry, etc.), et j’écarte les objets non routables (platform, area=yes).


| Règle                                            | Décision | Pourquoi                                                                 |
| ------------------------------------------------ | -------- | ------------------------------------------------------------------------ |
| Inclure la **liste blanche OSRM** `highway_whitelist` | OK        | Couverture des structures marchables (rues, sentiers, escaliers,...) |
| Exclure `foot=no`                               | OK        | Interdiction explicite aux piétons                                       |
| Inclure `access=private` et `service=private`    | OK        | Espaces résidentiels/semi-publics                  |
| Exclure `platform` et `area=yes`                 | OK        | Surfaces non topologiques (quais, places) pour un graphe routable        |

### Implémentation technique (OSMnx)

#### Mon filtre personnalisé 

```python
custom_filter = (
    '["highway"~"primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|'
    'unclassified|residential|road|living_street|service|track|path|steps|pedestrian|'
    'footway|pier"]'
    '["highway"!~"platform"]'
    '["area"!~"yes"]["foot"!~"no"]'
)
```

#### Construction du **graphe** pièton

**Implementation (extraction du graphe avec OSMnx)**

```python
import osmnx as ox

G = graph_from_polygon(
    polygon,
    custom_filter=custom_filter,
    simplify=True,
    retain_all=True
)

nodes, edges = ox.graph_to_gdfs(G)
edges.to_file("marseille_walk_edges.gpkg", driver="GPKG")  # les arcs (tronçons)
nodes.to_file("marseille_walk_nodes.gpkg", driver="GPKG")  # les nœuds (intersections)
```

A la fin, j'exporte les `nodes` et `egdes` et je visualise dans QGIS.

::: {card}

```{figure} ../images/extr_nodes_egdes.png
:alt: Extrait du graphe généré.
:width: 100%
```

**Extrait des noeuds et troncçons de route (OSMnx, profil “personalisé”)**
:::

> Le profil personnalisé ajuste les filtres OSMnx (walk) et OSMR (foot) pour contruire un réseau piéton adapté au calcul d'indicateur de proximité à l'echelle de la marche à pied.
> Le reseau obtenu couvre la quasi-totalité des endroits accessibles ou semi-privés, permettant ainsi des calculs à n'importe quel adresse dans une ville.

