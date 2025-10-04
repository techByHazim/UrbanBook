# Catalogue des données

## Objectif de la section

Avant de se lancer dans les calculs, il est toujours utile de prendre un moment pour explorer les données.
Cette étape permet de se familiariser avec leur contenu, de comprendre comment elles sont organisées et de vérifier qu’elles correspondent bien à ce que l’on attend.

L’exploration sert par exemple à voir quels types d’équipements sont recensés, comment ils sont décrits et s’il y a des particularités à garder en tête pour la suite.
C’est aussi l’occasion de préparer le terrain : nettoyer, organiser et mettre en forme les données afin qu’elles soient directement exploitables pour l’analyse.

Jusqu'à présent, j'utilise 3 grandes familles de jeux de données :

## La base permanante des équipements (BPE, INSEE)

- Millésime : 2023 (indiquer la date de récolte)
- Contenu : équipements/services géolocalisés (typologie fine)
- Usage : structure homogène, comparaisons intercommunales
- Référence : INSEE BPE

## Les données d'OpenStreetMap (OSM)

- Extrait : date du dump ou Overpass
- Tags clés : `amenity=*`, `shop=*`, `leisure=*`, etc.
- Usage : granularité, fraîcheur locale
- Référence : wiki OSM (Map features)

## Les données GTFS (General Transit Feed Specification)
- Producteur : AOT/opérateur
- Périmètre : lignes, arrêts, horaires
- Usage : fonctions “mobilité”
- Référence : GTFS Reference