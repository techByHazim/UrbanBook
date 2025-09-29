# Rôle du calcul de densité

L’étape finale du pipeline consiste à transformer le réseau enrichi par projection des équipements (Note 3) en un **indicateur continu d’attractivité piétonne**. Pour ce faire, on applique une méthode d’**estimation de densité par noyau sur réseau** (*Network Kernel Density Estimation, NKDE*), qui permet de mesurer l’intensité des opportunités accessibles autour de chaque lixel.  

Cette approche s’écarte des mesures euclidiennes classiques en prenant en compte la **structure réelle du réseau piéton**, et en intégrant une **fonction de décroissance exponentielle**, adaptée à la marche, qui reflète le fait que les opportunités perdent rapidement de leur attractivité avec la distance de marche.  

---

## Méthodologie et algorithme

Le calcul de la NKDE repose sur trois éléments principaux :  
1. **Les équipements (POI)** pondérés et enrichis par la diversité fonctionnelle (Note 1).  
2. **Le réseau piéton lixelisé** servant de support spatial (Note 2).  
3. **La projection des équipements sur le réseau** pour assurer une correspondance topologique entre les deux dimensions (Note 3).  

Une fois ces prérequis établis, l’algorithme suivant est appliqué pour diffuser l’influence de chaque POI sur le réseau :  

**Algorithme : Calcul de l’indice d’attractivité piétonne (NKDE sur réseau)**

1. Construire un graphe non orienté : chaque lixel devient une arête reliant ses extrémités.  
2. Pour chaque point d’intérêt (POI) :  
   a. Identifier le lixel le plus proche du POI.  
   b. Projeter le POI sur ce lixel pour obtenir un point sur l’arête.  
   c. Fractionner le lixel à ce point projeté.  
   d. Ajouter un nœud temporaire à la position du point projeté.  
   e. Connecter ce nœud temporaire aux deux segments du lixel fractionné.  
   f. Calculer les distances-réseau (Dijkstra) depuis le nœud temporaire vers tous les autres nœuds du graphe, jusqu’à une distance seuil (cutoff).  
   g. Pour chaque arête (lixel) atteinte par les chemins calculés :  
      - Récupérer la distance \(d\) entre le POI et cette arête le long du graphe.  
      - Calculer la contribution selon la fonction noyau \(F(d)\) (exponentielle décroissante).  
      - Pondérer cette contribution par le poids du POI.  
      - Ajouter cette densité au lixel concerné.  
   h. Supprimer le nœud temporaire du graphe et restaurer le lixel initial.  
3. **Sortie** : un GeoDataFrame contenant chaque lixel avec son score d’attractivité.  

---

## Fonction de noyau et décroissance

Le calcul de la contribution d’un POI à un lixel est basé sur une **fonction exponentielle décroissante** :

$$
F(d) = \exp\!\left(-\frac{d}{\lambda}\right), \quad d \leq d_\text{cutoff}
$$

où :

* $d$ est la distance-réseau entre le POI et le lixel,
* $\lambda$ est la distance caractéristique de décroissance (par exemple 300 à 500 m pour la marche quotidienne),
* $d_\text{cutoff}$ est une distance seuil au-delà de laquelle le POI n’exerce plus d’influence.

Cette formulation est directement inspirée des travaux sur l’accessibilité piétonne, qui soulignent que la probabilité d’utiliser un équipement décroît de manière rapide avec la distance de marche (O’Sullivan et al., 2000 ; Sevtsuk & Mekonnen, 2012).

---

## Sorties et indicateur final

La sortie du calcul est un **GeoDataFrame** contenant chaque lixel avec son score d’attractivité.
Ce score reflète :

1. La **proximité effective** des équipements sur le réseau.
2. Leur **importance fonctionnelle** (pondération).
3. Leur **contribution à la diversité locale**.

L’indicateur obtenu peut ensuite être agrégé à des échelles plus larges (carreaux de 200 m, IRIS, quartiers) pour produire des cartes d’accessibilité piétonne et analyser les inégalités spatiales.

---

## Discussion méthodologique

### Atouts

* Représentation réaliste de l’accessibilité, en intégrant la structure du réseau et un noyau comportemental.
* Combinaison des dimensions quantitatives (nombre d’équipements), qualitatives (poids fonctionnels) et structurelles (réseau piéton).
* Haute résolution grâce à la lixelisation.

### Limites

* Paramètres sensibles ($\lambda$, $d_\text{cutoff}$) qui peuvent influencer fortement les résultats.
* Dépendance à la qualité des données OSM pour le réseau.
* Complexité algorithmique élevée, nécessitant des choix d’optimisation.

---

## Références bibliographiques

* O’Sullivan, D., Morrison, A., & Shearer, J. (2000). *Using desktop GIS for the investigation of accessibility by public transport: an isochrone approach*. International Journal of Geographical Information Science, 14(1), 85–104.
* Okabe, A., & Sugihara, K. (2012). *Spatial Analysis Along Networks: Statistical and Computational Methods*. Wiley.
* Sevtsuk, A., & Mekonnen, M. (2012). *Urban network analysis: A new toolbox for ArcGIS*. Revue Internationale de Géomatique, 22(2), 287–305.
* Neutens, T. (2015). *Accessibility, equity and health care: review and research directions for transport geographers*. Journal of Transport Geography, 43, 14–27.

