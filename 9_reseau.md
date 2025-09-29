# Construction et traitement du réseau piéton

## Rôle du réseau dans l’indicateur

Le second bloc méthodologique du pipeline vise à préparer le **réseau piéton** qui constitue le support spatial de l’indicateur d’accessibilité. Contrairement aux mesures euclidiennes (distance à vol d’oiseau), l’analyse par réseau permet d’évaluer l’accessibilité **réelle**, en tenant compte de la structure urbaine, des discontinuités et de la connectivité des rues.

Cette étape répond ainsi à une exigence théorique forte : mesurer l’accessibilité non pas comme une simple proximité géographique, mais comme une **relation spatiale contrainte par l’infrastructure de mobilité** (Geurs & van Wee, 2004).


## Extraction des données

Les données du réseau proviennent d’**OpenStreetMap (OSM)**, une base libre et collaborative particulièrement riche en informations sur la voirie, y compris les sentiers piétons, escaliers, passages souterrains et autres éléments essentiels pour la mobilité douce.

L’extraction se fait sur le périmètre d’étude (ici, la commune de Marseille), afin de concentrer le traitement sur la zone pertinente.


## Préparation et simplification

Le réseau extrait est soumis à plusieurs étapes de traitement :

* **Simplification topologique** : élimination des redondances géométriques, correction des erreurs et harmonisation des attributs.
* **Nettoyage du graphe** : suppression des segments isolés ou non pertinents (culs-de-sac non piétonniers, tronçons privés, etc.).
* **Uniformisation spatiale** : recentrage du réseau sur la zone d’analyse.

Ces étapes garantissent que le réseau obtenu reflète de manière fiable et cohérente la structure réelle de la voirie piétonne.


## Lixelisation du réseau

Une étape clé du traitement est la **lixelisation** du réseau, c’est-à-dire sa découpe en segments de longueur fixe (généralement 10 à 20 mètres). Chaque **lixel** devient ainsi une unité d’observation homogène sur laquelle les calculs de densité et d’accessibilité seront appliqués.

Les avantages de la lixelisation sont multiples :

* Elle assure une **granularité régulière** et facilite la comparaison entre tronçons.
* Elle permet de produire des mesures continues d’accessibilité sur l’ensemble du réseau, plutôt que ponctuelles ou agrégées.
* Elle prépare la mise en œuvre de la **Network Kernel Density Estimation (NKDE)**, méthode de densité adaptée aux réseaux (Okabe & Sugihara, 2012).


## Construction du graphe

Une fois lixelisé, le réseau est représenté sous forme de **graphe** (nœuds et arêtes) :

* Les **nœuds** correspondent aux intersections.
* Les **arêtes** correspondent aux lixels.

Cette représentation graph-théorique est essentielle pour modéliser les distances sur réseau, rechercher les plus courts chemins et projeter les équipements sur le support piéton. Elle garantit la cohérence topologique de l’analyse.


## Conclusion et rôle dans le pipeline

Le traitement du réseau piéton fournit un support homogène, topologiquement cohérent et adapté aux méthodes de densité. La lixelisation en fait une **unité d’analyse de haute résolution**, directement comparable aux équipements pondérés et diversifiés construits dans le premier bloc.

Ainsi, la **dimension “réseau”** complète la **dimension “offre”** issue de la Note 1. Le point de jonction entre ces deux dimensions sera la **projection des équipements sur le réseau**, abordée dans la Note 3.


## Références bibliographiques

* Geurs, K. T., & van Wee, B. (2004). *Accessibility evaluation of land-use and transport strategies: Review and research directions*. Journal of Transport Geography, 12(2), 127–140.
* Okabe, A., & Sugihara, K. (2012). *Spatial Analysis Along Networks: Statistical and Computational Methods*. Wiley.
* Borruso, G. (2005). *Network Density Estimation: analysis of point patterns over a network*. Lecture Notes in Computer Science, 3643, 126–136.
* Porta, S., Crucitti, P., & Latora, V. (2006). *The network analysis of urban streets: A dual approach*. Physica A, 369(2), 853–866.

