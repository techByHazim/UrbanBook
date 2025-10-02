---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# UrbanBook 

**UrbanBook** est le **carnet numérique instrumenté** de ma thèse.  
Il documente de bout en bout la construction d’un indicateur local de proximité (PAL), du choix des données et paramètres jusqu’aux protocoles, expériences, décisions et résultats. L’objectif est double : **traçabilité scientifique** et **reproductibilité**.

```{admonition} Positionnement
:class: important
Ce livre n’est pas une simple vitrine. C’est un outil de travail versionné : il fixe les conventions (données, pondérations, échelles), consigne les choix, standardise les protocoles et relie chaque expérience à des artefacts vérifiables.
```

## Comment lire

* Commencer par **Méthodologie en bref** pour le cadre général.
* Lire **Spécification du PAL** puis **Paramétrages** (pondérations, rayons, fonctions de décroissance).
* Parcourir les **Expériences** pour les analyses de sensibilité, validations et décisions.
* Utiliser **Reproductibilité** pour rejouer les calculs avec l’environnement fourni.
* Le **code exécutable** (pipelines, scripts) est maintenu dans le dépôt compagnon *UrbanProximity*.

## Ce que contient UrbanBook

* **Données** : catalogue (BPE, OSM, GTFS), millésimes, limites, dictionnaire des variables.
* **Indicateurs** : définition formelle du PAL, mapping des aménités vers fonctions sociales, paramètres.
* **Protocoles** : calcul, validation, qualité des données, contrôles cartographiques.
* **Expériences** : une page par expérience avec objectif, méthode, résultats, conclusion et liens vers artefacts.
* **Traçabilité** : journal de décision, changelog, références et modalités de citation.

```{admonition} Reproductibilité
:class: tip
Les notebooks sont **exécutés localement** et sauvegardés avec leurs sorties ; l’exécution côté site est **désactivée** (`execute_notebooks: "off"`).  
Les scripts et workflows sont disponibles dans *UrbanProximity* ; l’environnement est décrit dans `requirements.yml`.
```

## Méthodologie en bref

* **Sources ouvertes** : BPE (INSEE), OpenStreetMap, GTFS.
* **Unité d’analyse** : segment du réseau piéton.
* **Principe** : mesure de la proximité fonctionnelle via densité, diversité et accessibilité à pied des aménités, pondérées par rôle social.
* **Contrôles** : analyses de sensibilité (rayons, poids), croisement de sources, effets d’agrégation, vérifications cartographiques.

## Navigation

* Projet : objectifs, questions, hypothèses
* Données : catalogue, dictionnaire
* Indicateurs : spécification PAL, mapping, paramétrages
* Protocoles : calcul, validation
* Expériences : carnet synthétique, fiches XP
* Reproductibilité : environnement, comment reproduire
* Méta : journal de décision, changelog, à propos & citation

```{admonition} Citer ce livre
Moindze H. (2025). *UrbanBook - Proximité urbaine et inéquités*. Version 0.1.  
URL : https://techByHazim.github.io/UrbanBook/  
DOI à ajouter dès l’archivage (Zenodo).
```

## Sommaire

```{tableofcontents}
```
