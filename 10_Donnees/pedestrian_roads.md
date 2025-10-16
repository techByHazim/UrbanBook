
# Extraction du réseau piéton 

```{note}
**Hypothèse de travail :**  
*Tout segment de voie praticable à pied appartient au réseau piéton, qu’il soit public ou privé.*
```

## Notions de base sur les graphes et leur représentation géométrique

Avant d’aborder la construction du réseau piéton à partir d’OpenStreetMap, il est utile de rappeler brièvement quelques notions fondamentales de [**théorie des graphes**](https://fr.wikipedia.org/wiki/Th%C3%A9orie_des_graphes), afin de comprendre ce que représente concrètement un graphe urbain.

### Définition générale

Un **graphe** est un objet mathématique formellement défini comme un couple :

```{math}
G = (V, E)
```
où :

* (V) est l’ensemble des **sommets** (ou *nœuds*),
* (E) est l’ensemble des **arêtes** reliant ces sommets.

Une arête ( (u, v) \in E ) indique simplement qu’il existe une **connexion** entre les nœuds (u) et (v).
Le graphe décrit donc la **structure des relations**, sans aucune notion de distance ou de position.

**Exemple simple :**

```{math}
V = \{A, B, C\}, \quad E = \{(A, B), (B, C)\}
```

→ (A) est relié à (B), et (B) à (C).
Cette structure peut se dessiner de multiples façons : le dessin n’a pas de valeur géométrique, seule la **connectivité** compte.

> *Réf. :* Harary, F. (1969). *Graph Theory*. Addison-Wesley.

> *Réf. :* West, D. B. (2001). *Introduction to Graph Theory*. Prentice Hall.

### Graphes orientés et non orientés

Un graphe peut être :

* **Non orienté** : les liens sont symétriques ((A - B \equiv B - A)).

* **Orienté** : chaque lien possède un **sens** ((A \to B)).
  Typique des réseaux routiers ou des flux dirigés (ex. circulation à sens unique).

En Python, les graphes orientés sont souvent représentés par des objets `DiGraph` ou `MultiDiGraph` (NetworkX / OSMnx).

### Graphes topologiques et géographiques

La **théorie des graphes** est d’abord abstraite : elle décrit *qui relie qui*.
Mais pour modéliser un réseau urbain, on ajoute une **dimension géométrique** :

* chaque nœud reçoit des **coordonnées** ((x, y)) (longitude, latitude),
* chaque arête reçoit une **géométrie** (souvent une courbe `LineString`),
* la distance entre deux nœuds peut alors être mesurée dans l’espace réel.

Ainsi, un **graphe géographique** est un **graphe topologique plongé dans l’espace**.
Il conserve la logique relationnelle du graphe abstrait, tout en permettant des analyses spatiales : calculs de distance, itinéraires, accessibilité, etc.

> *Réf. :* Boeing, G. (2017). *OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks.* *Computers, Environment and Urban Systems*, 65, 126–139.

### Application : le réseau piéton

Dans le cadre de cette étude, le graphe représente :

* les **nœuds** : intersections, bifurcations ou extrémités de voies ;
* les **arêtes** : segments de voie praticables à pied.

Chaque arête possède à la fois :

* une **structure topologique** : connexion entre deux nœuds `u` et `v` ;
* une **géométrie spatiale** : forme de la voie.

L’analyse du réseau repose donc sur une double lecture :

1. **Topologique** : comprendre la structure du graphe (connectivité, continuité).
2. **Géographique** : interpréter le graphe dans l’espace réel (distances, tracés, accessibilité, etc.).

## Outils d'extraction du réseau

Deux outils majeurs permettent de travailler sur un réseau piéton issu d’OpenStreetMap :

1. **[OSMnx](https://osmnx.readthedocs.io/en/stable/)**
   → bibliothèque Python pour **télécharger**, **construire** et **analyser** des graphes urbains (piéton, vélo, voiture, etc.).

2. **[OSRM](https://project-osrm.org/)**
   → moteur de **routage** capable de calculer des itinéraires selon des profils (`car`, `bike`, `foot`, …).

Ces outils utilisent des **profils prédéfinis** qui filtrent automatiquement les types de voies selon les modes de déplacement autorisés.

## construction du réseau piéton à partir d'OSMnx

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

Ce code permet d'obtenir le graphe du réseau routier piéton dans notre zone d'analyses.
Le graphe `G` obtenu est par defaut un **MultiDiGraph** : un graphe **orienté** où plusieurs arêtes peuvent relier les mêmes nœuds (ex. deux sens de circulation).

Les arguments :

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

* Les arêtes possèdent des **attributs** : `oneway`, `length`, `name`, `highway`, `geometry`, etc.
* `u` = nœud origine, `v` = nœud destination.

  * Si `oneway=False`, deux arêtes sont créées (`u→v` et `v→u`).

**Astuce:**
On lit d’abord la **structure topologique** (qui relie quoi), puis la **géométrie spatiale** (où cela se trouve réellement).

### Visualisation du graphe

Pour la réprensation du graphe, je ne présente pas le graphe sur toute la zone d'étude (trop grand) mais j'extrais une petite 
partie pour l'illustration.

```python
# Trouver un nœud central
center_node = list(G.nodes())[len(G)//2]

# Extraire un sous-graphe dans un rayon de 1 km
subG = ox.truncate.truncate_graph_dist(G, center_node, max_dist=1000)
```
Cela permet d'obtenir un sous graphe de rayon 600m centré au milieu de ma zone d'étude. 

#### a) Graphe topologique orienté

Pour tracer le graphe topologique, la fonction `nx.draw()` le fait rapidement.

```python
plt.figure(figsize=(7,6))
nx.draw(subG, node_size=20, edge_color='gray', node_color='red')
plt.show()
```

::: {card}

```{figure} ../images/graph_topo.png
:alt: Graphe topologique du réseau piéton à Marseille
:width: 100%
```
**Extrait du Graphe topologique (orienté) (OSMnx, “walk”)**
:::

Les points rouges représentent les intersections, les traits gris les connexions et leurs sens.

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
**Extrait du Graphe topologique (non orienté) (OSMnx, “walk”)**
:::

Ici, les arêtes ne sont plus directionnelles : elles indiquent simplement qu’une connexion existe entre deux nœuds. 

#### c) Graphe géographique

De la meme manière, on peut representer le grpahe en prenant compte des coordonées GPS des nodes et des egdes.
La fonction `ox.plot_graph` contient les outils necessaires pour cette tache.

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
**Extrait du Graphe géographique (non orienté) (OSMnx, “walk”)**
:::
`ox.plot_graph()` ne trace pas les flèches de direction sur les routes

### Export du réseau 

On peut extraire les nœuds et arêtes du graphe sous forme de GeoDataFrames.

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

> Le réseau obtenu, construit à partir du paramètre `network_type="walk"` dans la fonction `ox.graph_from_polygon`, est **géométriquement cohérent**.
> Toutefois, il reste **incomplet sur le plan topologique**, car certaines voies semi-publiques ou internes ne sont pas incluses par ce filtre.
> Une phase d’enrichissement du réseau est donc nécessaire pour garantir la **continuité du maillage piéton**.

## Définition d’un filtre piéton personnalisé

### Profil  piéton OSRM `foot.lua`

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

> Dans une logique d’**accessibilité réelle**, je m’intéresse à ce qu’il est **physiquement possible de parcourir à pied**, indépendamment des restrictions administratives.
> Le réseau piéton est donc construit à partir d’OpenStreetMap en suivant la logique du profil `foot.lua` d’OSRM : je conserve les types de voies habituellement praticables à pied, j’exclus celles explicitement interdites (`foot=no`), j’inclus les accès restreints mais franchissables (zones privées ou résidentielles), et j’écarte les objets non routables comme les quais ou les surfaces (`platform`, `area=yes`).

| Règle                                            | Décision | Pourquoi                                                                 |
| ------------------------------------------------ | -------- | ------------------------------------------------------------------------ |
| Inclure la **liste blanche OSRM** `highway_whitelist` | OK        | Couverture des structures marchables (rues, sentiers, escaliers,...) |
| Exclure `foot=no`                               | OK        | Interdiction explicite aux piétons                                       |
| Inclure `access=private` et `service=private`    | OK        | Espaces résidentiels/semi-publics                  |
| Exclure `platform` et `area=yes`                 | OK        | Surfaces non topologiques (quais, places) pour un graphe routable        |

**Implémentation technique (OSMnx)**

**Mon filtre personnalisé** 

```python
custom_filter = (
    '["highway"~"primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|'
    'unclassified|residential|road|living_street|service|track|path|steps|pedestrian|'
    'footway|pier"]'
    '["highway"!~"platform"]'
    '["area"!~"yes"]["foot"!~"no"]'
)
```

**Construction du **graphe** pièton**

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

A la fin, j'exporte les `nodes` et `egdes` que je peux visualiser dans QGIS.

::: {card}

```{figure} ../images/extr_nodes_egdes.png
:alt: Extrait du graphe généré.
:width: 100%
```
**Extrait des noeuds et tronçons de route (OSMnx, filtre “personalisé”)**
:::

> Ce profil personnalisé combine la logique des filtres d’OSMnx et d’OSRM afin de construire un **réseau piéton cohérent avec la marche**.
> Le réseau obtenu couvre la grande majorité des espaces accessibles, y compris certaines zones semi-privées, ce qui permet de réaliser des calculs d’accessibilité **depuis n’importe quelle adresse de la ville**. Je mets à dispostion dans section suivante, le notebook exploratoire [graph_OSMnx.ipynb](graph_OSMnx.ipynb) qui détaille la structure du graphe.


