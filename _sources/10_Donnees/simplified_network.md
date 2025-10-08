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
Avant tout traitement, je m’assure que les géométries soient valides.

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
Pour éviter de comparer toutes les lignes entre elles (coût énorme), j'utilise un **index spatial (R-tree)** qui permet de trouver rapidement les candidates à une intersection.

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

  * leurs `layer` sont compatibles (ex : 0 et 0, 1 et 1 ou -2 et -2, etc.).
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

## Sauvegarde du réseau traité

On obtient un **GeoDataFrame** :

* geom valide,
* découpé,
* nettoyé,
* sans doublons.

Il est sauvegardé au format **GeoPackage**.

## Illustration avant / après

Une comparaison graphique permet de voir l’impact du traitement (Visualisation sous QGIS).

## Discussion sur les limites du traitement

Certaines décisions que j’ai prises ont permis de simplifier le traitement, mais elles ont aussi leurs limites. Voici les principaux points que je garde en tête :

* **Géométries isolées** : il reste quelques lignes qui ne sont connectées à rien, souvent des chemins piétons indépendants. Il faudra voir si ces segments doivent être conservés ou supprimés.

* **Seuils fixes** : j’ai utilisé une tolérance très faible (`1e-7`) et un buffer constant (`0.001`) pour être précis. Avec le recul, ces valeurs sont peut-être un peu trop strictes et peuvent empêcher la reconnexion de lignes presque jointes. Une tolérance ajustée selon la densité du réseau serait peu etre plus adaptée.

* **Couches (`layer`)** : pour gérer les intersections, j’ai appliqué une règle simple de compatibilité (±1). C’est efficace pour éviter les erreurs, mais ça passe à côté de certains croisements valides sur plusieurs niveaux.

* **Cas particuliers** : j’ai choisi de toujours connecter les `steps`, pour garantir la continuité du graphe piéton. C’est pratique, mais ça peut créer des connexions verticales un peu irréalistes (escaliers, rampes, etc.).

* **Attributs OSM** : après le découpage, chaque segment garde les attributs du tronçon d’origine. C’est simple et lisible, mais ça ne préserve pas toujours la cohérence des champs si on fusionne ou réutilise le réseau plus tard.

* **Performance** : l’index spatial (`R-tree`) m’a permis de réduire les temps de calcul, mais ça reste lent dans les zones très denses. À terme, il faudrait sans doute envisager une approche par tuiles ou du calcul parallèle.

## Conclusion

Cette étape m’a permis de rendre le réseau OSM beaucoup plus cohérent et exploitable, même si tout n’est pas parfait.
J’ai réussi à corriger une grande partie des incohérences géométriques, à identifier les vrais points d’intersection et à découper les tronçons.
Il reste encore des cas particuliers à améliorer mais la base obtenue est déjà solide pour construire un graphe piéton fiable et poursuivre les analyses.

> Le réseau obtenu constitue la base pour construire un graphe piéton cohérent. 
> Le notebook détaillé permettant de réaliser ce nettoyage est présenté dans la section suivante : [*Nettoyage et simplification du réseau piéton*](simplified_roads).


