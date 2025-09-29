# Méthodologie - NKDE sur réseau (lixels)

## Résumé

Cette note décrit l'implémentation du caclul de l'indicateur de proximité sur un réseau **lixelisé** par **NKDE**. L’objectif est d’estimer, pour chaque lixel, une **un score** issue des équipements (points d’intérêt (POIs)), en utilisant des distances **le long du réseau** et un **noyau** (gaussien ou exponentiel) avec **distance de coupure** (cuttoff).
Cette méthode garantit **au plus une contribution par POI et par lixel** (via la sélection de la meilleure distance), évitant les doubles-comptes.


## Contexte 

On considère un réseau (piéton, voirie, etc.) découpé en *lixels* (segments élémentaires). On souhaite calculer un score sur ce réseau à partir d’équipements ponctuels (POI), en mesurant la proximité **selon la métrique du graphe** (et non à vol d’oiseau).
L’estimation repose sur un noyau $K$ avec **bandwidth** $h$ (distance caractéristique) et un **facteur de coupure** $c$ (distance effectif (cutoff) $c \cdot h$).

## Données d’entrée et paramètres

* **POI** : points géolocalisés, chacun avec deux poids $w_i$ (poids intrinsèque) et $w_{efs}$ (poids extrinsèque).
  Le poids total d’un POI : $w = w_i + w_{efs}$.
* **Lixels** : segments du réseau, chacun avec un identifiant unique $j$ et une géométrie linéaire.
* **Paramètres** :
  
  * `lixel_size` 
  * `bandwidth` $h$
  * `kernel_type` ∈ {`gaussian`, `exponential`}
  * `cutoff_factor` $c>0$ (cutoff $=\ c\,h$)

**Sortie** : une table/GeoDataFrame des lixels avec une colonne **`score[j]`**.


## Prétraitements indispensables

1. **CRS commun et métrique** : projeter **POI** et **lixels** dans le même système projeté (**EPSG:2154**) pour avoir des longueurs en mètres.
2. **Identifiants** : assigner un **id** $j$ à chaque lixel.
3. **Index spatial** : construire un index spatial sur les lixels (recherche du lixel le plus proche).


## Construction du graphe de lixels

Construire un graphe non orienté $G=(V,E)$ :

* $V$ = extrémités des lixels (nœuds),
* pour chaque lixel, ajouter une arête $(u,v)$ avec attributs :

  * `length` = longueur du lixel,
  * `lixel_id` = identifiant $j$.


## Définition du noyau $K(d;h,\texttt{type},c)$

Soit $t = d/h$.

* **Gaussien** : $K(d) = \exp(-\tfrac{1}{2} t^2)$ si $t \le c$, sinon $0$.
* **Exponentiel** : $K(d) = \exp(-t)$ si $t < c$, sinon $0$.

> Le **cutoff** limite le calcul aux distances $d \le c\,h$.


## Algorithme principal (pseudocode)

```text
Algorithme 1 : Calcul NKDE sur lixels (une contribution par POI et par lixel)

Entrées :
  P              ← ensemble des POI ; chaque p ∈ P possède wi, wefs, géométrie (point)
  L              ← ensemble des lixels ; chaque ℓ ∈ L possède id, géométrie (ligne)
  G              ← graphe du réseau construit à partir de L
                    (nœuds = extrémités de lixels ; arêtes (u,v) avec attributs: length, lixel_id)
  h              ← bandwidth (distance caractéristique du noyau)
  kernel_type    ← "gaussian" ou "exponential"
  c              ← cutoff_factor  (cutoff = c × h)

Sorties :
  density[j]     ← densité estimée pour chaque lixel j ∈ L

Initialisation :
  pour chaque lixel j ∈ L : density[j] ← 0
  cutoff ← c × h

Procédure :
  pour chaque POI p ∈ P faire
      w ← p.wi + p.wefs (somme poids intrinsèque et extrinsèque)
      x ← géométrie (point) de p

      # 1) Lixel support le plus proche (recherche spatiale)
      ℓ*  ← argmin_{ℓ ∈ L} dist_euclidienne(x, ℓ)
      id* ← identifiant(ℓ*)

      # 2) Insertion d’un nœud temporaire relié aux deux extrémités de ℓ*
      p̃ ← ajouter_noeud_temporaire(G, x, ℓ*)
           (relier p̃ aux deux extrémités de ℓ* avec des arêtes de longueur euclidienne)

      # 3) Distances réseau limitées depuis p̃
      D ← Dijkstra(G, source = p̃, poids = "length", cutoff = cutoff)
          (D : nœud → distance minimale)

      # 4) Meilleure distance par lixel atteint
      best_distance_by_lixel ← {}
      pour chaque (v, d_v) dans D faire
          si d_v > cutoff : continuer
          pour chaque voisin u de v dans G faire
              e ← arête (v,u)
              si e.lixel_id = j alors
                  si j ∉ best_distance_by_lixel ou d_v < best_distance_by_lixel[j] alors
                      best_distance_by_lixel[j] ← d_v
                  fin si
              fin si
          fin pour
      fin pour

      # 5) Sécurité : garantir une contribution au lixel support
      si id* ∉ best_distance_by_lixel alors
          d_proj ← dist_euclidienne(x, ℓ*)
          si d_proj ≤ cutoff alors
              best_distance_by_lixel[id*] ← d_proj
          fin si
      fin si

      # 6) Accumulation (une seule contribution par lixel et par POI)
      pour chaque (j, d_j) dans best_distance_by_lixel faire
          val ← w × K(d_j ; h, kernel_type, c)
          density[j] ← density[j] + val
      fin pour

      # 7) Nettoyage
      supprimer_noeud(G, p̃)
  fin pour

Retourner density
```


## Post-traitements et export

* Arrondir les densités (p. ex. 3 décimales).
* Conserver les attributs utiles : `osm_id, highway, name, incline, lit, score, geometry`.
* Exporter en **GPKG** (ou tout format géospatial adapté).


## Complexité (ordre de grandeur)

Pour $N$ POI, chaque Dijkstra **borné** à $c\,h$ coûte \~$O(E' \log V')$ sur le **sous-graphe atteint** ($V' \ll V$, $E' \ll E$ grâce à la coupure).
La recherche du lixel le plus proche avec index spatial est \~$O(\log M)$, $M$ = nb. de lixels.


## Bonnes pratiques / points d’attention

* **CRS unique et métrique** pour toutes les couches.
* **Cutoff** $c\,h$ indispensable pour maîtriser le coût.
* **Poids des POI** : vérifier présence/cohérence de $w_i$ et $w_{efs}$.
* **Unicité des contributions** : une seule contribution par lixel et par POI (via `best_distance_by_lixel`).


## Possibles extensions

* **Graphes orientés** : coûts asymétriques, sens de circulation.
* **Noyaux alternatifs** : triangulaire, Epanechnikov, **bandwidth adaptatif**.
* **Parallélisation** : paralléliser la boucle sur les POI si mémoire OK.


## Références bibliographiques

* O’Sullivan, D., Morrison, A., & Shearer, J. (2000). *Using desktop GIS for the investigation of accessibility by public transport: an isochrone approach*. International Journal of Geographical Information Science, 14(1), 85–104.
* Okabe, A., & Sugihara, K. (2012). *Spatial Analysis Along Networks: Statistical and Computational Methods*. Wiley.
* Sevtsuk, A., & Mekonnen, M. (2012). *Urban network analysis: A new toolbox for ArcGIS*. Revue Internationale de Géomatique, 22(2), 287–305.
* Neutens, T. (2015). *Accessibility, equity and health care: review and research directions for transport geographers*. Journal of Transport Geography, 43, 14–27.
