# Comment reproduire

1. Cloner **UrbanProximity** (code) et **UrbanBook** (doc).
2. Créer l’environnement : `mamba env create -f requirements.yml`.
3. Lancer le pipeline : `python scripts/run_pal.py --config configs/pal_v01.yml`.
4. Vérifier les sorties (hash, tailles, métadonnées).
5. Ouvrir UrbanBook pour consulter les résultats et la traçabilité.