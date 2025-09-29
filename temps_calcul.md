# Optimisation du temps de calcul 

Jusqu'à récemment, le calcul via NKDE (Network Kernel Density Estimation) était extrêmement lent, rendant son utilisation peu pratique pour des réseaux de grande taille. Après analyse, j'ai identifié et optimisé la partie la plus coûteuse du pipeline : la recherche du lixel le plus proche pour chaque POI.

## Le problème initial

Dans la version précédente, la recherche de lixel le plus proche était réalisée de manière naïve, avec une approche brute-force. Pour chaque POI, on calculait la distance à tous les lixels, puis on retenait celui qui minimisait la distance :

```python
nearest_lixel_idx = lixels_gdf.distance(point).idxmin()
```
##  Complexité de l'approche naïve

```{admonition} Definition 
:class: tip
La complexité est une mesure de la quantité de ressources (temps, espace) qu'un algorithme utilise en fonction de la taille de l'entrée. Elle est souvent exprimée en notation Big O, qui décrit le comportement asymptotique de l'algorithme lorsque la taille de l'entrée tend vers l'infini.
```
Comment cela se traduit-il en termes de complexité ?

Dans notre cas, pour chaque POI, on doit parcourir tous les lixels pour trouver le plus proche. Si `N` est le nombre de POIs et `M` le nombre de lixels, la complexité de cette opération est `O(N × M)`. Autrement dit, pour chaque POI, on parcourt **tous les lixels du réseau**.
Si l’on a `N` POIs et `M` lixels, cela fait `N × M` calculs de distance.

Par exemple avec 1 POI et sur mes 1253901 lixels de 10 m ou 678999 lixels de 20 m, cela revient à **1,25 millions de distances** ou **678999 distances** évaluées par Shapely.
Résultat : un seul passage du calcul pouvait prendre plusieurs minutes. Par exemple, pour 3571 POIs pour `s'approvisionner`, le temps de calcul était d'environ 1h26. Ce qui est clairement inacceptable pour une utilisation pratique.

## Analyse et diagnostic

Dans un premier temps, j'ai tenté d’optimiser les paramètres du noyau (bande passante, cutoff) pour réduire le nombre de lixels à considérer. Cependant, cela n’a eu qu’un impact limité sur le temps de calcul. C'était dans les memes ordres de grandeur. Ce qui m'a conduit à suspecter que le véritable goulot d’étranglement résidait ailleurs. Le temps était necessairment consommé ailleurs en dehors de l’application du noyau.

C'est là que j'ai réalisé que j'effectuais la recherche du lixel le plus proche de manière inefficace. En effet, la méthode `distance` de Shapely que j'ai utilisé est enfaite très coûteuse. De plus, l’appel répété pour chaque POI amplifiait ce coût de manière exponentielle.

## La solution : utiliser un index spatial

Pour remédier à ce problème, j'ai remplacé cette recherche linéaire par l’utilisation d’un index spatial, basé sur `STRtree` (fournie par Shapely ≥ 2.0).

Le principe :

* on construit une structure d’arbre spatial **une seule fois** à partir de toutes les géométries des lixels,
* puis on interroge directement cet arbre pour obtenir le lixel le plus proche d’un POI.

En pratique, cela revient à :

```python
from shapely.strtree import STRtree

# Construire l’index une seule fois
geoms = list(lixels_gdf.geometry)
tree = STRtree(geoms)

# Pour chaque POI, trouver le lixel le plus proche
# renvoie directement l’index du lixel le plus proche
nearest_idx = tree.nearest(point)  
```

La complexité passe ainsi de `O(N × M)` à `O(N log M)` car l’interrogation de l’arbre est logarithmique par rapport au nombre de lixels (voir [source](https://shapely.readthedocs.io/en/stable/manual/strtree.html#shapely.strtree.STRtree.nearest)).

## Résultats

* **Avant (méthode naïve)** : 

| Fonction     | Nb de points (Itérations) | Vitesse (it/s) |     Durée(hh:mm:ss) |
| ------------ | --------------------: |  -------------: | --------: |
| care         |                 5 031 |           1,26 | \~01:06:33 |
| provisioning |                 3 671 |           1,30 | \~00:47:04 |
| entrainment  |                   434 |           1,16 | \~00:06:14 |
| education    |                   415 |           1,23 | \~00:05:37 |
| working      |                   861 |           1,21 | \~00:11:52 |
| living       |                 3 498 |           1,28 | \~00:45:33 |
| Transport    |                 5 579 |           1,39 | \~01:06:54 |

Soit un total d’environ **4 h 09 min 46 s** pour l’ensemble des fonctions (pour environ **19098** équipements).

* **Après optimisation (STRtree)** : 

| Fonction     | Nb de points (Itérations) | Vitesse (it/s) |   Durée (hh:mm:ss) |
| ------------ | --------------------: | -------------: |  -------------: |      
| care         |                 5 031 |           8,59 | \~00:09:45 |
| provisioning |                 3 671 |           7,35 | \~00:08:19 |
| entrainment  |                   434 |           9,49 | \~00:00:45 |
| education    |                   415 |           9,12 | \~00:00:45 |
| working      |                   861 |           8,94 | \~00:01:36 |
| living       |                 3 498 |           8,43 | \~00:06:54 |
| Transport    |                 5 579 |          10,60 | \~00:08:46 |

Soit un total d’environ **36 minutes 46 secondes** pour l’ensemble des fonctions (pour environ **19098** équipements). Cela représente une **amélioration d’un facteur ~7** sur le temps total de calcul.

* **Paramètres prise en compte dans le calcul**

  * Lixels : **20 m**
  * Rayon diversité **d=80 m**, bande passante **bw=250 m**, **cut=750 m**
  * Réseau piéton :  **678999 lixels** de 20 m



### Conclusion

Cette optimisation montre que, dans les algorithmes de géomatique computationnelle, le choix de la structure de données est souvent plus crucial que la puissance brute de calcul.

Grâce à l’utilisation de l’index spatial, la recherche du lixel le plus proche est désormais quasi instantanée, rendant l’algorithme NKDE **scalable et applicable à des réseaux urbains de grande taille**.

La prochaine étape sera d’optimiser la diffusion des distances (actuellement réalisée par un Dijkstra indépendant pour chaque POI), afin de réduire encore davantage les temps de traitement.

