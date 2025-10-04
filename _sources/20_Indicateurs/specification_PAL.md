# Spécification de l’indicateur PAL

## Définition
- Unité d’observation : segment du **réseau piéton**.
- Entrées : liste d’aménités catégorisées, **pondérations**, distances à pied, diversité locale.
- Sortie : score **PAL ∈ [0,1]** par segment.

## Schéma (informel)
PAL(s) = F(∑_a w_a · G(dist(s,a)), Diversité, Densité)

## Paramètres par défaut
- Rayon de marche : 800 m
- Décroissance avec la distance : exponentielle (λ = à préciser)
- Normalisation : min–max à l’échelle de la zone d’étude

## Limites
- Sensibilité aux **lacunes OSM**
- Effets d’**agrégation** (MAUP) lors des regroupements
- Choix **arbitraires** de pondérations → prévoir analyses de sensibilité