# Traitement du réseau routier

## Introduction  

Comme je l’ai évoqué dans la section précédente, le réseau OSM n’est pas toujours cohérent avec la réalité du terrain. Certaines routes sont incomplètes, d’autres se superposent ou ne sont pas connectées correctement.

Avant de pouvoir l’utiliser pour des analyses (par exemple pour construire un graphe piéton cohérent). Il faut donc nettoyer et corriger le réseau afin d’en éliminer les incohérences.

Voici la suite du pipeline de traitement que j’ai mis en place :


```{figure} ../images/traitement_roads.png
:name: fig-extraction-reseau-pieton
:alt: Schéma des étapes principales d’extraction du réseau piéton
:width: 80%
:align: center
```

## Validation des géométries

**Idée :**
Avant tout traitement, on s’assure que les géométries soient valides.

**Pseudo-code :**

```
pour chaque géométrie :
    si géométrie est vide OU invalide :
        supprimer
    sinon :
        conserver
```

Cela permet d’éviter que des objets corrompus fassent planter les étapes suivantes.

## Extraction des lignes

**Idée :**
OSM peut contenir des `LineString` (simple) ou des `MultiLineString` (plusieurs segments regroupés).
On transforme tout en une liste de lignes simples.

**Pseudo-code :**

```
lignes = []
pour chaque géométrie dans le réseau :
    si LineString :
        ajouter directement
    si MultiLineString :
        découper en plusieurs LineString et les ajouter
```

## Indexation spatiale

**Idée :**
Pour éviter de comparer toutes les lignes entre elles (coût énorme), on utilise un **index spatial (R-tree)** qui permet de trouver rapidement les candidates à une intersection.

**Pseudo-code :**

```
créer index R-tree
pour chaque ligne :
    insérer sa bounding box dans l’index
```

## Détection des intersections

C’est l’étape la plus délicate.
On parcourt chaque paire de lignes **potentiellement en intersection** (détectée via l’index spatial), puis on applique des règles.

### Règles principales

* Si les lignes se croisent au **milieu**, elles ne sont connectées que si :

  * leurs `layer` sont compatibles (ex : 0 et 0, ou 0 et 1 avec tolérance).
  * ni tunnel/ni pont incohérent.

* Si elles se rejoignent à une **extrémité** :

  * intersection acceptée même si les `layer` diffèrent légèrement (`tolérance = ±1`).

* Cas particuliers :

  * **Escaliers (`steps`)** → toujours connectés.
  * **Ponts vs tunnels** → jamais connectés sauf aux extrémités.

**Pseudo-code :**

```
pour chaque paire de lignes (i, j) candidate :
    calculer intersection géométrique
    
    si aucune intersection :
        passer
    
    si intersection est un point :
        vérifier règles :
            - si escaliers → accepter
            - si intersection à une extrémité ET layers compatibles → accepter
            - si intersection au milieu ET layers strictement égaux → accepter
            - sinon → ignorer
        ajouter point si accepté
```

## Découpage des lignes

Une fois les intersections identifiées, on **découpe les lignes** aux points de croisement.
Cela permet de représenter correctement les nœuds dans un futur graphe.

### Détails techniques

* Avant de couper, on **"snap"** les lignes aux points proches pour éviter des erreurs numériques (tolérance très petite : `1e-7`).
* Chaque segment hérite des attributs de la ligne d’origine (`osm_id`, `highway`, etc.).

**Pseudo-code :**

```
pour chaque ligne :
    chercher les points d’intersection proches (via index de points)
    si intersections :
        snap la ligne sur ces points
        découper la ligne en plusieurs segments
        conserver chaque segment avec attributs
    sinon :
        conserver ligne telle quelle
```

## Suppression des doublons

Certaines lignes sont parfaitement superposées (mêmes coordonnées).
On les supprime pour éviter de compter deux fois la même route.

**Pseudo-code :**

```
convertir chaque géométrie en WKB (représentation binaire unique)
supprimer doublons
```

## Sauvegarde du réseau simplifié

On obtient un **GeoDataFrame** :

* geom valide,
* découpé,
* nettoyé,
* sans doublons.

Il est sauvegardé au format **GeoPackage**.

## Illustration avant / après

Une comparaison graphique permet de voir l’impact du traitement (Voir QGIS)

## Conclusion

Cette deuxième étape est très importante car c'est ce qui va rendre le calcul des distances sur le réseau fiable. 

> Le réseau obtenu constitue la base pour construire un graphe piéton cohérent. 
> Le notebook détaillé permettant de réaliser ce nettoyage est présenté dans la section suivante : [*Nettoyage et simplification du réseau piéton*](simplified_roads).


