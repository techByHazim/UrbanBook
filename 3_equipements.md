# Les équipements urbains et les sources de données

Les *équipements urbains* (ou aménités) sont des **points d’intérêt** qui structurent les usages quotidiens et la qualité de vie locale. Ils incluent, par exemple :
- des **commerces** (boulangeries, supermarchés, pharmacies) ;
- des **services** (écoles, crèches, postes) ;
- des **équipements publics** (parcs, bibliothèques, équipements sportifs) ;
- des **infrastructures de transport** (arrêts de bus, stations de vélos en libre service, etc.).

## Rôle dans l’indicateur de proximité

Dans le calcul de l’indicateur (cf. chapitre *Indicateurs de proximité*), les équipements jouent le rôle de **destinations**.  
Leur **présence**, leur **diversité** et leur **accessibilité à pied** conditionnent directement le score de proximité d’un lieu donné.

## Sources de données

Mon objectif étant la **portabilité** (analyser plusieurs territoires) et la **reproductibilité**, je privilégie des sources **ouvertes** et **documentées** :

- **Base permanente des équipements (BPE, INSEE)** : inventaire statistique national des services/équipements, mis à jour **chaque 1er janvier**, avec une **typologie fine** et, pour une large part, une **géolocalisation**. Utile pour les comparaisons territoriales et les analyses multi-échelles.  
  Réf. : INSEE – pages source et millésimes ; fiches et données ouvertes.

- **OpenStreetMap (OSM)** : base **collaborative** et internationale décrivant très finement le tissu urbain (**tags** comme `amenity=*` pour les aménités). Très utile pour capturer des éléments **locaux et récents** non couverts ailleurs, au prix d’un contrôle-qualité à prévoir selon les zones.  
  Réf. : Wiki OSM (tags et bonnes pratiques).

- **GTFS (transports collectifs)** : pour l’offre de **transports en commun** (arrêts, lignes, horaires). Standard ouvert, largement utilisé par les AOT et les opérateurs.  
  Réf. : **GTFS Reference** (spécification officielle).

```{admonition} Bonnes pratiques (qualité et croisement)
:class: tip
- **Croiser** BPE et OSM quand c’est possible : BPE apporte structure et homogénéité ; OSM apporte granularité et fraîcheur.
- **Documenter** les choix de mapping (quels tags OSM pour quelles catégories ?).
- **Tracer** les millésimes (ex. BPE 2024) pour assurer la comparabilité temporell
```

## Catégorisation des aménités

Pour l’analyse, je regroupe les équipements par **fonctions sociales** (ex. *se soigner*, *s’approvisionner*, *se former*, etc.).
Deux approches coexistent :

* **S’appuyer sur des cadres établis**, comme les **fonctions de la “ville du quart d’heure”** (idée de proximité fonctionnelle à 15 minutes à pied/vélo).
* **Adapter/compléter** selon les besoins de l’étude (p. ex. regrouper des sous-catégories BPE ; ajouter une classe *mobilités* ; créer une classe dédiée *bornes de recharge* si l’étude le requiert).

```{admonition} Pondérations (importance relative)
:class: note
Chaque type d’équipement peut recevoir une **pondération** reflétant son rôle social local (ex. *supermarché* > *boulangerie* pour l’approvisionnement de base).  
Ces pondérations doivent être **explicites**, **argumentées** (littérature, usages, concertation), et **testées** (analyses de sensibilité).
```

## Aperçu d’un tableau de correspondances

L’extrait ci-dessous charge un fichier Excel (onglet *Categories of Amenities*) qui documente **comment** les catégories sources (BPE, OSM tags, GTFS, etc.) sont **mappées** vers les fonctions retenues pour l’analyse.

```{code-cell} python
import pandas as pd
from pathlib import Path

# chemin du fichier (adapter au projet)
excel_path = Path("../proxy/data/raw/insee/services_features2509121322.xlsx")
sheet_name = "Categories of Amenities"

# lecture + aperçu
df = pd.read_excel(excel_path, sheet_name=sheet_name)
df.head(30)
```

> *Remarque* : l’aperçu ci-dessus sert uniquement à **visualiser** la table.
> Les scripts de production utilisent ce même fichier pour garantir la **cohérence** entre documentation et calculs.

---

## Références (sélection)

* **BPE / INSEE** – description et méthodologie (source officielle) ; dernières statistiques/millésimes ; portail data : INSEE et data.gouv.
* **OpenStreetMap** – documentation des tags, notamment `amenity=*` et *Map features* (wiki officiel).
* **GTFS** – spécification officielle et ressources MobilityData.
* **Ville du quart d’heure** – article de référence (Moreno, 2021) ; compléments récents.

```

**Sources :** INSEE BPE (vue générale et méthodo) :contentReference[oaicite:0]{index=0} ; data.gouv (jeux BPE) :contentReference[oaicite:1]{index=1} ; OSM amenity & map features (wiki) :contentReference[oaicite:2]{index=2} ; GTFS Reference (officiel) :contentReference[oaicite:3]{index=3} ; Moreno (2021, “15-Minute City”) et compléments récents :contentReference[oaicite:4]{index=4}.
