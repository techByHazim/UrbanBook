# Catalogue des données

## Objectif

Les équipements structurent la proximité urbaine : ils matérialisent l’accès effectif aux fonctions du quotidien (se soigner, s’approvisionner, apprendre, se divertir, se déplacer, etc.). Avant d’engager des calculs d’accessibilité, il est indispensable d’explorer les jeux de données, d’en comprendre la structure et d’en vérifier la cohérence avec le périmètre analytique. Cette étape prépare le terrain : nettoyage, normalisation, et mise en forme pour des analyses reproductibles.

Concrètement, je cherche à :

* identifier quels types d’équipements sont recensés et comment ils sont décrits ;
* repérer d’éventuelles spécificités (champs manquants, doublons, géocodage imprécis) ;
* harmoniser les taxonomies pour relier des sources hétérogènes dans une grille d’analyse commune.

J’utilise trois grandes familles de données ouvertes et complémentaires.

## Base Permanente des Équipements (BPE, INSEE)

* **Référence** : INSEE - *Base permanente des équipements*  ([documentation officielle](https://www.insee.fr/fr/metadonnees/source/serie/s1161)).
* **Millésime utilisé** : **2024** *(Date de téléchargement:  le 06/10/2025)*.
* **Couverture** : France métropole.
* **Unité d’observation** : équipement individuel, géolocalisé.
* **Contenu** : typologie fine des équipements et services (santé, commerce, éducation, sport-loisirs, services publics, etc.).
* **Forces** :

  * **homogénéité nationale** de la structure et de la nomenclature ;
  * **stabilité** interannuelle permettant les comparaisons territoriales.
* **Limites** :

  * délai de mise à jour (décalage possible vs. terrain) ;
  * certains équipements très récents peuvent ne pas être saisis au millésime courant.

* **Pré-traitements réalisés** :

  * contrôle des coordonnées ; reprojection en **EPSG:2154 (Lambert-93)** ;
  * normalisation des libellés (encodage, accents, casse) ;
  * sélection des catégories pertinentes pour les **fonctions sociales** retenues (cf. cadre théorique) ;
  * création d’une **clé de correspondance** entre la typologie BPE et ma taxonomie cible.

## Données OpenStreetMap (OSM)

* **Référence** : projet collaboratif OSM (*Map Features* pour la sémantique des tags).
* **Extraction** :

  * **extrait régional** au format `.osm.pbf` *([source](https://download.geofabrik.de/europe/france/provence-alpes-cote-d-azur.html) et date du dump : 20/05/2025)*,
 
* **Périmètre sémantique** : tags clés `amenity=*`, `shop=*`, `leisure=*`, `healthcare=*`, `office=*`, etc.
* **Forces** :

  * **granularité fine** (niveau point/poignée d’attributs) ;
  * **fraîcheur locale** potentiellement élevée dans les zones à forte communauté contributive.
* **Limites** :

  * **hétérogénéité** spatiale de la complétude ;
  * variabilité dans l’usage des tags ; risque de **doublons** (ex. POI dupliqués).

* **Pré-traitements réalisés** :

  * filtrage par **ensemble de tags** cohérent avec les fonctions étudiées ;
  * nettoyage des géométries (validité topologique, retrait des nœuds isolés aberrants) ;
  * **dé-duplication spatiale** (agrégation par distance seuil `d≤x m` + heuristiques sur le nom/adresse) ;
  * **mapping sémantique** des tags vers la **taxonomie cible** (table de correspondance OSM → catégories analytiques) ;
  * reprojection en **EPSG:2154**.

## Données GTFS (General Transit Feed Specification)

* **Référence** : jeux de données publiés par l’**AOM/opérateur** (*Métropole Aix-Marseille-Provence*, [portail transport.data](https://transport.data.gouv.fr/datasets/reseau-rtm-gtfs/)).
* **Version** : **GTFS statique** *(indiquer l’archive et sa période de validité, ex. : du 06/06/2025 au 05/08/2025)*.
* **Fichiers clés** : `stops.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, `calendar(.txt)`, `shapes.txt`.
* **Usage dans la thèse** :

  * repérage des **arrêts** (points d’accès) et de la **structure d’offre** (lignes, dessertes) ;
  * intégration d’une **fonction “mobilité”** qui conditionne l’accès aux autres fonctions (chaînes intermodales).
* **Limites** :

  * absence d’horaires en temps réel ; la validité est **bornée** par la période GTFS ;
  * hétérogénéité des politiques d’**identifiants stables** et de la **qualité d’adressage**.

* **Pré-traitements réalisés** :

  * validation de schéma (présence des fichiers requis) ;
  * harmonisation des **identifiants d’arrêt** et suppression des arrêts inactifs hors période ;
  * conversion des `stops` en couche géographique et reprojection en **EPSG:2154** ;
  * A faire : **fusion d’arrêts proches** (pôles d’échange) pour coller à l’échelle piétonne (seuil `d≤x m`).

