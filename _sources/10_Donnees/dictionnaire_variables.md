# Dictionnaire des variables

| Nom              | Type   | Unité  | Source    | Description                                |
|------------------|--------|--------|-----------|--------------------------------------------|
| segment_id       | str    | –      | réseau    | Identifiant unique du segment piéton       |
| PAL              | float  | [0,1]  | calcul    | Potentiel d’attractivité locale            |
| nb_amenites      | int    | –      | BPE/OSM   | Nombre d’aménités dans le rayon            |
| dist_moy_amen    | float  | m      | calcul    | Distance moyenne aux aménités              |
| diversite_idx    | float  | –      | calcul    | Indice de diversité des fonctions sociales |