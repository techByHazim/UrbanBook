# **Définition de l'indicateur de proximité**


## **Contexte et objectif**
Les villes modernes construites autour de la dépendance à la voiture laissent des territoires urbains très hétérogènes en matière d'accessibilité et d'aménagement urbain. Or cette hétérogénéité n'est pas sans conséquences sur nos pratiques quotidiennes. Pour deceler ces disparités, souvent invisbles à l'échelle de la ville, on propose une approche bottom-up qui prendra en compte de la description fine de l'espace urbain. Le but c'est de mesurer la proximité locale (à l’échelle piétonne) des équipements urbains accessibles aux habitants. On croit que cette **mesure fine et localisée** permettra de mieux comprendre les inégalités territoriales en matière d'accessibilité, d'aménagement urbain et de comportements liés à cette proximité.

## **Définition de l'indicateur**

   * **Proximité** : notion relative, subjective, multidimensionnelle.
   * **Équipements urbains** : services et infrastructures de proximité (écoles, commerces, santé, loisirs, etc.).
   * **Accessibilité piétonne** : importance de la marche à pied dans les déplacements quotidiens.
   * **Indice de proximité** : mesure composite de la proximité des équipements urbains.

La mesure de la proximité sera quantifiée par un **indicateur composite** qu'on va appeler **"indice de proximité"** qui combine :

   * l’offre d’équipements (quantité, diversité),
   * la structure spatiale du réseau de route (piéton).
   * L'accessibilité aux équipements urbains (via distance-réseau).

## **Problématique scientifique**

   * Limites des indicateurs classiques (euclidiens, trop agrégés).
   * Nécessité d’intégrer la logique du réseau et la notion de coût de déplacement.
   * Importance de la diversité.

## **Logique du pipeline**

   * Deux grandes briques :

     1. **Offre d’équipements** : extraction, pondération, diversité.
     2. **Réseau piéton** : extraction, simplification, lixelisation, graphe.
   * Point de jonction : projection des équipements sur le réseau.
   * Résultat final : un **indice de proximité à l'échelle piétonne** calculé  sur des tronçons de route (adresse).

## **Intérêts**

   * Croisement entre approche morphologique (réseau piéton) et fonctionnelle (diversité d’équipements).
   * Approche multi-échelle (lixel de 10-20 m etc.).
   * Indicateur reproductible et transférable à d’autres territoires.

## **Références**

   * Moreno et al. (2020) sur la ville du quart d’heure.
   * Geurs & van Wee (2004) sur les quatre composantes de l’accessibilité.
   * Jacobs (1961) sur la diversité urbaine.
   * O’Sullivan et al. (2000), Okabe & Sugihara (2012) sur les méthodes de densité spatiale.
   * Neutens (2015) sur l’incertitude des mesures d’accessibilité.


