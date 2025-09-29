# Note 5 – Discussion générale et perspectives

## 1. Forces de l’approche

Le pipeline proposé présente plusieurs atouts méthodologiques :

* **Intégration fonctionnelle et structurelle** : l’indicateur combine la diversité et l’importance des équipements (dimension fonctionnelle) avec la structure réelle du réseau piéton (dimension morphologique).
* **Granularité fine** : la lixelisation du réseau permet une analyse très détaillée, apte à mettre en évidence des micro-inégalités spatiales.
* **Réalisme comportemental** : l’utilisation d’une fonction de décroissance exponentielle s’accorde avec les observations empiriques sur la marche (les individus privilégient les opportunités accessibles dans un rayon de 5 à 10 minutes).
* **Reproductibilité** : le pipeline repose sur des bases de données ouvertes (BPE, OSM) et des méthodes transparentes, donc transférables à d’autres territoires.

---

## 2. Limites et points de vigilance

* **Qualité des données** :

  * Les données OSM peuvent être incomplètes ou hétérogènes.
  * La BPE ne reflète pas toujours la vitalité réelle des équipements (certains sont fermés, d’autres sous-utilisés).

* **Paramétrisation sensible** :

  * Choix du paramètre de décroissance $\lambda$.
  * Détermination du seuil $d_\text{cutoff}$.
  * Pondération des équipements, qui repose en partie sur des choix experts.

* **Complexité algorithmique** :

  * La NKDE sur réseau est coûteuse en calcul (répétition de Dijkstra pour chaque POI).
  * Des solutions d’optimisation (indexation spatiale, pré-calculs, parallélisation) peuvent être nécessaires.

---

## 3. Ouvertures et applications

L’indicateur produit ouvre de nombreuses pistes d’application :

* **Analyse des inégalités spatiales** : identifier les zones sur-dotées ou sous-dotées en accessibilité de proximité.
* **Urbanisme et planification** : fournir une aide à la décision pour l’implantation d’équipements ou la requalification d’espaces publics.
* **Politiques de mobilité douce** : relier l’offre de proximité aux choix modaux (marche, vélo).
* **Recherche académique** :

  * croiser l’indicateur avec des données socio-économiques (revenu, pauvreté, logement social),
  * étudier les effets sur la santé et le bien-être (marche quotidienne, activité physique).

---

## 4. Perspectives de recherche

Plusieurs axes d’approfondissement méthodologique peuvent être envisagés :

* **Accessibilité multimodale** : intégrer les arrêts de transport en commun pour mesurer une accessibilité élargie.
* **Accessibilité temporelle** : introduire les horaires d’ouverture et la disponibilité des équipements.
* **Approches probabilistes** : traiter l’incertitude liée à la qualité des données et aux comportements effectifs des usagers.
* **Agrégation dynamique** : adapter le mode d’agrégation (médiane, quartiles, profils statistiques) selon la structure interne des carreaux de population.

---

## Références bibliographiques

* Geurs, K. T., & van Wee, B. (2004). *Accessibility evaluation of land-use and transport strategies: Review and research directions*. Journal of Transport Geography, 12(2), 127–140.
* Jacobs, J. (1961). *The Death and Life of Great American Cities*. Random House.
* Moreno, C., Allam, Z., Chabaud, D., Gall, C., & Pratlong, F. (2020). *Introducing the “15-Minute City”*. Smart Cities, 4(1), 93–111.
* Neutens, T. (2015). *Accessibility, equity and health care: review and research directions for transport geographers*. Journal of Transport Geography, 43, 14–27.
* O’Sullivan, D., Morrison, A., & Shearer, J. (2000). *Using desktop GIS for the investigation of accessibility by public transport: an isochrone approach*. IJGIS, 14(1), 85–104.

