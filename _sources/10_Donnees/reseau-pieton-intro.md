# Construction d’un réseau piéton pour l’analyse

Pour analyser la **proximité urbaine à pied**, il faut disposer d’un **réseau piéton structuré**.  

## Les sources de données

J'ai interogé deux grandes bases de données ouvertes qui décrivent le réseau viaire :

- **[BD TOPO de l’IGN](https://geoservices.ign.fr/route500)** : une base officielle très précise géométriquement ;
- **[OpenStreetMap (OSM)](https://www.openstreetmap.org/)** : une base open source et collaborative.

Dans OSM, chaque élément du réseau (route, sentier, passage, escalier, etc.) est décrit par des **balises (“tags”)** comme :
`highway=*`, `footway=*`, `access=*`, etc.  
Voir la documentation complète : [OSM Tags](https://wiki.openstreetmap.org/wiki/Tags).

::: {card}
```{figure} ../images/osm_bruit.png
:alt: Extrait du réseau routier issu d’OpenStreetMap (Marseille)
:width: 100%
```
**Réseau OSM - maillage participatif**
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

C’est donc à partir d’**OpenStreetMap** que je vais construire le **réseau de route piéton**.
:::
