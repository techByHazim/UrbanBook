# Construction d’un réseau piéton pour l’analyse

## Pourquoi construire un réseau piéton ?

Pour analyser la **proximité urbaine à pied**, il faut disposer d’un **réseau piéton structuré**.  
L’idée est de représenter la ville sous la forme d’un **graphe**, c’est-à-dire une structure composée :

- de **nœuds** (intersections, jonctions, extrémités de voies) ;
- d’**arcs** (tronçons praticables reliant ces nœuds).

Ce type de représentation, issu de la [**théorie des graphes**](https://fr.wikipedia.org/wiki/Th%C3%A9orie_des_graphes), permet de modéliser :
- la **connectivité** entre les voies ;
- la **continuité spatiale** du réseau ;
- et de calculer des **distances réelles** ou des **chemins les plus courts** à pied.

En résumé, le **graphe piéton** est la base de toute analyse de **proximité spatiale** et de **mobilité locale**.


## Les sources de données

J'ai consulté deux grandes bases ouvertes qui décrivent le réseau viaire :

- **[BD TOPO de l’IGN](https://geoservices.ign.fr/route500)** : une base officielle très précise géométriquement ;
- **[OpenStreetMap (OSM)](https://www.openstreetmap.org/)** : une base open source et collaborative.

Dans OSM, chaque élément du réseau (route, sentier, passage, escalier…) est décrit par des **balises (“tags”)** comme :
`highway=*`, `footway=*`, `access=*`, etc.  
Voir la documentation complète : [OSM Tags](https://wiki.openstreetmap.org/wiki/Tags).

::: {card}
```{figure} ../images/osm_bruit.png
:alt: Extrait du réseau routier issu d’OpenStreetMap (Marseille)
:width: 100%
```

**Réseau OSM - maillage participatif, très fin pour les espaces piétons**
:::

::: {card}

```{figure} ../images/route_ign.png
:alt: Extrait du réseau routier issu de la BD TOPO (IGN)
:width: 100%
```
**Réseau IGN - géométrie précise mais lacunaire pour la marche**
:::

*Figure : comparaison du réseau viaire selon OpenStreetMap et la BD TOPO sur un même secteur de Marseille.*

:::{important}
La **BD TOPO** offre des tracés précis mais **omet** des routes importantes pour la marche (escaliers, passages internes, ruelles, etc.).
À l’inverse, **OpenStreetMap** couvre **l’espace public et résidentiel**, incluant sentiers, passages et zones semi-publiques.

C’est donc à partir d’**OpenStreetMap** que je construis le **graphe piéton**, afin de garantir une **connectivité** et une **couverture complète** des voies praticables à pied.
:::
