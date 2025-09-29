# Projection des équipements sur le réseau piéton

## Rôle de la projection dans le pipeline

Après avoir construit la base enrichie des équipements (Note 1) et préparé le réseau piéton lixelisé (Note 2), l’étape suivante consiste à **projeter les POI sur le réseau**. Cette opération vise à ancrer chaque équipement à un **segment de rue (lixel)** afin que son accessibilité puisse être mesurée en termes de distance réelle à pied, plutôt qu’en distance euclidienne.

Sans cette étape, les calculs de densité et d’accessibilité resteraient déconnectés de la réalité des déplacements urbains, qui s’effectuent toujours par l’intermédiaire d’un réseau.


## Méthodologie de projection

La projection repose sur un algorithme qui associe chaque POI à son **point le plus proche sur le réseau lixelisé** :

* Chaque équipement est affecté à une arête (lixel) en fonction de la distance perpendiculaire minimale.
* L’information du poids et de la diversité de l’équipement est transférée au lixel support.
* Si plusieurs équipements sont projetés sur le même segment, ils sont traités séparément. Il n'y a pas d'ambiguïté à ce niveau, car chaque équipement conserve son identité.

Cette opération transforme le réseau en un **support porteur d’attributs** (intensité fonctionnelle, diversité locale), prêt à être utilisé dans le calcul de l'indicateur de proximité.

Le fichier qui execute cette tache c'est `../scr/project_to_network.py`. Dans ce fichier, on trouve les details sur les outils et les methodes utilises. Chaque étape dans le code est bien commentée pour faciliter la compréhension et la réutilisation du code.

L’ancrage des POI sur le réseau correspond à une exigence méthodologique largement discutée dans la littérature sur l’accessibilité :

* **Différence entre distance euclidienne et distance-réseau** : les mesures euclidiennes sous-estiment ou surestiment l’accessibilité réelle en ignorant les contraintes de circulation (Geurs & van Wee, 2004).
* **Accessibilité structurelle** : les infrastructures déterminent la faisabilité effective des déplacements (Handy & Niemeier, 1997).
* **Projection comme étape d’intégration fonctionnelle et morphologique** : elle permet de faire dialoguer la dimension « offre » (services) et la dimension « réseau » (infrastructure piétonne).


## Résultats de la projection

La sortie de ce bloc est un réseau piéton enrichi :

* Chaque lixel dispose désormais d’attributs fonctionnels liés aux équipements (poids, diversité).
* La distribution des équipements suit la topologie du réseau, permettant un calcul ultérieur de densité spatiale cohérent.
* Les lixels deviennent les **unités de mesure** de l’accessibilité, en combinant données morphologiques (structure du réseau) et données fonctionnelles (offre de services).


## Conclusion et rôle dans le pipeline

Cette étape constitue un **pivot méthodologique** : elle relie la base d’équipements enrichie (dimension « offre ») au réseau piéton lixelisé (dimension « structure »).

À ce stade, le pipeline dispose d’un **réseau fonctionnalisé**, prêt pour le calcul de la **densité de proximité** (NKDE), qui sera détaillé dans la Note 4.


## Références bibliographiques

* Geurs, K. T., & van Wee, B. (2004). *Accessibility evaluation of land-use and transport strategies: Review and research directions*. Journal of Transport Geography, 12(2), 127–140.
* Handy, S. L., & Niemeier, D. A. (1997). *Measuring accessibility: an exploration of issues and alternatives*. Environment and Planning A, 29(7), 1175–1194.
* Sevtsuk, A., & Mekonnen, M. (2012). *Urban network analysis: A new toolbox for ArcGIS*. Revue Internationale de Géomatique, 22(2), 287–305.


