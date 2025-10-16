## Harmonisation inter-sources

Pour croiser BPE, OSM et GTFS, j’applique une procédure d’intégration en quatre étapes :

1. **Taxonomie commune**

   * Élaboration d’un **dictionnaire de correspondance** entre les catégories BPE, les tags OSM et les classes “mobilité” GTFS.
   * Choix d’un niveau **méso** (ni trop fin, ni trop agrégé) aligné sur les **fonctions sociales** étudiées.

2. **Normalisation géographique**

   * Reprojection systématique en **EPSG:2154**.
   * Contrôles de **cohérence spatiale** (points hors emprise, doublons co-localisés, géométries invalides).
   * Réduction des **doublons inter-sources** par *distance join* + règles sur nom/adresse/type.

3. **Référentiel temporel**

   * Définition d’une **date de référence** *t₀* (ex. : 30/06/2023).
   * Alignement des millésimes :

     * BPE millésime 2023,
     * OSM **snapshot** ou Overpass daté,
     * GTFS valide autour de *t₀*.
   * Marquage des enregistrements hors période (exclusion ou pondération).

4. **Qualité & traçabilité**

   * Scripts reproductibles (hash des fichiers, versions des bibliothèques).
   * **Journal de nettoyage** (quels filtres, quels seuils, combien d’objets retirés/fusionnés).
   * Exports intermédiaires (par couches et par fonctions) pour audit.

## Variables clés mobilisées

* **Identifiants** : `id_source`, `id_normalisé`, provenance (BPE/OSM/GTFS), date d’extraction.
* **Localisation** : géométrie (point), précision, système de coordonnées (EPSG:2154).
* **Sémantique** : catégorie normalisée, sous-catégorie, champs descriptifs (nom, opérateur, horaires si dispo).
* **Contexte** : commune/IRIS/quadrat 200 m (pour agrégation), distance au réseau piéton si exploité.
* **Mobilité** (GTFS) : `stop_id`, `route_type`, fréquence approximative (si calculée à partir de `stop_times`), appartenance à un pôle.

## Contrôles qualité (QC)

* **Complétude** : taux de valeurs manquantes par champ ; couverture spatiale par maille.
* **Cohérence sémantique** : validation par règles (ex. `amenity=school` → catégorie “Éducation”).
* **Cohérence spatiale** : distribution des distances minimales entre POI “homonymes” ; repérage des clusters anormaux.
* **Sensibilité aux seuils** : tests des distances de fusion (`d=20/30/50 m`) et impact sur le nombre d’objets.
* **Comparaison croisée** : BPE vs OSM pour quelques catégories *sentinelles* (ex. pharmacies, écoles).

## Limites et biais (à garder en tête)

* **Décalages temporels** : BPE (millésime annuel) vs OSM (continu) vs GTFS (périodes).
* **Hétérogénéité de complétude** (OSM) et **défauts de géocodage** ponctuels.
* **Définitions catégorielles** : un même lieu peut être typé différemment selon la source.
* **Effets de bord réglementaires** : fermetures/ouvertures non répercutées immédiatement.

Ces limites seront **quantifiées** lorsque possible (ex. écarts BPE/OSM par catégorie) et prises en compte via des **analyses de sensibilité** et/ou des **pondérations**.

## Références et traçabilité (à citer dans le manuscrit)

* **INSEE — BPE** : documentation officielle *(indiquer l’URL et la date de consultation)*.
* **OpenStreetMap — Map Features** : documentation des tags *(indiquer l’URL et la date de consultation)*.
* **GTFS** : spécification et fiches jeux de données (prod. AOM/opérateur, ex. MAMP/RTM via transport.data.gouv.fr, avec **URL** et **licence** exactes).

## Reproductibilité

* Dépôt de scripts (pré-traitement, harmonisation, QC) avec **versions** et **conda env**/`requirements.txt`.
* Archivage des **hashs** des fichiers sources et des **exports** intermédiaires.
* Journal *README* décrivant chaque étape et ses paramètres (seuils, règles de fusion, tables de mapping).

### À compléter par toi (pour figer la traçabilité)

* Date(s) exacte(s) de **téléchargement** des données BPE/OSM/GTFS.
* **URL** de chaque fichier source (ou requêtes Overpass).
* **Licences** précises des jeux GTFS utilisés.
* Les **seuils** retenus (ex. distance de fusion, buffers piétons) et les **tables de correspondance** finales.