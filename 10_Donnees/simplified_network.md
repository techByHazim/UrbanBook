# Traitement et simplification du réseau piéton

## Introduction  

Une fois le réseau piéton extrait d’OpenStreetMap, il reste brut et contient de nombreuses incohérences :  
- tronçons non valides (vides ou mal définis),  
- lignes qui se croisent sans être connectées,  
- géométries dupliquées ou superposées,  
- erreurs liées aux tunnels, ponts ou couches (`layer`).  

Pour obtenir un réseau exploitable en analyse (par exemple pour construire un graphe piéton cohérent), il est nécessaire de le **traiter et le simplifier**.  

L’approche suit un pipeline bien précis :  

```{mermaid}
flowchart TD
    A[OSM - Réseau brut] --> B[Validation des géométries]
    B --> C[Extraction des lignes]
    C --> D[Construction d'un index spatial]
    D --> E[Détection des intersections]
    E --> F[Découpage des lignes aux intersections]
    F --> G[Suppression des doublons]
    G --> H[Réseau simplifié]
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

On obtient un **GeoDataFrame propre** :

* validé,
* découpé,
* nettoyé,
* sans doublons.

Il est sauvegardé au format **GeoPackage**.

## Illustration avant / après

Une comparaison graphique permet de voir l’impact du traitement :

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

roads.plot(ax=axes[0], color="red", linewidth=0.5)
axes[0].set_title("Réseau piéton brut")

final_network_gdf.plot(ax=axes[1], color="green", linewidth=0.5)
axes[1].set_title("Réseau piéton simplifié")

plt.show()
```

## Conclusion

Cette étape transforme le réseau brut OSM en un **réseau piéton exploitable** :

* chaque intersection est définie selon des règles précises,
* les tronçons sont découpés proprement,
* les erreurs topologiques sont corrigées,
* les doublons sont supprimés.

Ce réseau simplifié constitue la base pour construire un **graphe piéton cohérent**, indispensable pour les analyses d’accessibilité, de connectivité et de mobilité urbaine.

