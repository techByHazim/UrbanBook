# Structure du projet

## Arborescence générale

Pour faciliter la reproductibilité et la compréhension du pipeline de traitement, l’architecture du projet suit une logique, séparant les **données**, le **code source**, les **notebooks** et la **configuration** de l’environnement. 

<style>
/* ===== Couleurs adaptatives (clair/sombre) ===== */
:root{
  --bg: #ffffff;
  --fg: #1f2937;         /* gris ardoise foncé */
  --muted: #6b7280;      /* gris moyen pour les notes */
  --line: #c7cdd4;       /* lignes d'arbre */
  --badge-border:#d1d5db;
  --badge-bg:#f9fafb;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg: #0b0f14;
    --fg: #6480b8ff;       /* texte principal clair */
    --muted: #9aa4b2;    /* notes lisibles en sombre */
    --line: #3a4856;     /* lignes plus douces en sombre */
    --badge-border:#334155;
    --badge-bg:#0f172a;
  }
}

/* ===== Reset léger pour ce bloc ===== */
.tree, .tree ul { list-style: none; margin: 0; padding-left: 1rem; position: relative; color: var(--fg); }
.kicker { margin:.5rem 0 .25rem; font-size:.95rem; color: var(--fg); }
.badge { display:inline-block; font-size:.75rem; padding:.1rem .4rem; border:1px solid var(--badge-border); border-radius:.4rem; background: var(--badge-bg); color: var(--fg); }
.note { color: var(--muted); font-style: italic; }
.folder { font-weight: 600; color: var(--fg); }
.file { font-weight: 500; color: var(--fg); }
hr.soft { border:0; border-top:1px dashed var(--line); margin:1rem 0; }

/* ===== Lignes de l'arbre ===== */
.tree:before, .tree ul:before {
  content: "";
  position: absolute;
  left: 0.5rem;
  border-left: 1px solid var(--line);
  top: 0; bottom: 0;
}
.tree li {
  margin: .25rem 0 .25rem 1rem;
  padding-left: .5rem;
  position: relative;
}
.tree li:before {
  content: "";
  position: absolute;
  left: -0.5rem;
  top: 0.75rem;
  width: 0.5rem;
  border-top: 1px solid var(--line);
}
/* Masque la ligne verticale résiduelle au dernier enfant,
   avec une couleur de fond adaptée au thème */
.tree li:last-child:after {
  content: "";
  position: absolute;
  left: 0.5rem;
  bottom: -0.25rem;
  height: calc(100% - 0.75rem);
  background: var(--bg);
  width: 2px;
}

</style>
<div class="kicker">Voici la structure générale du projet :</div>

<ul class="tree">
  <li class="folder">📦 Dev
    <ul>
      <li class="folder">📂 Proximity <span class="badge">Indicateurs de proximité</span>
        <ul>
          <li class="folder">📂 data
            <ul>
              <li class="folder">📂 raw <span class="note">données brutes (INSEE, OSM, GTFS, etc.)</span></li>
              <li class="folder">📂 processed <span class="note">données nettoyées et intermédiaires</span></li>
              <li class="folder">📂 final <span class="note">résultats finaux : indicateurs, cartes, agrégats</span></li>
            </ul>
          </li>
          <li class="folder">📂 envs <span class="note">environnements et dépendances (fichier <code>requirements.yml</code>)</span></li>
          <li class="folder">📂 notebooks <span class="note">exploration, analyses et prototypage</span></li>
          <li class="folder">📂 src <span class="note">scripts et modules Python du pipeline (préparation, traitement, calculs, etc.)</span></li>
        </ul>
      </li>
    </ul>
  </li>
</ul>

```{admonition} En résumé
:class: success
Chaque dossier a un rôle bien défini :
- **data** : stockage des données à chaque étape du processus ;  
- **envs** : configuration logicielle et gestion de l’environnement Conda ;  
- **notebooks** : travaux exploratoires et visualisations ;  
- **src** : code principal du pipeline, organisé par module fonctionnel.
```


## Fichiers essentiels pour le calcul

Pour lancer des calculs, on s'interessera uniquement sur ces trois fichiers :  

- **`data/raw/insee/services_features.xlsx`** : définit les catégories d’équipements et leurs poids.  
  - Feuille *Categories of Amenities*  
  - Chaque ligne = un type d’équipement (ex. école, boulangerie)  
  - Colonnes = fonction sociale (`fs`), identifiant (`service_id`), poids (`wi`).  
  - Vous pouvez modifier les poids ou ajouter de nouvelles catégories.  

- **`src/config.py`** : tous les paramètres du calcul (zone, fichiers d’entrée, rayon de diversité, largeur de bande, etc.).  

- **`src/main.py`**:  lance tous le calcul avec les paramètres définis dans `config.py`.  

La section suivante (voir [comment produire un calcul](comment_reproduire.md)) montrera en détails comment lancer un calul paramètrés à partir du projet.