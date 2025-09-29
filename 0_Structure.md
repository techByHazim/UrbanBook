# **Organisation du projet et outils utilisés**

## **Organisation du projet**
Ma thèse est organisée en plusieurs briques, qu'on peut voir comme des sous-projets indépendants mais complémentaires.
Je les développe dans des dossiers séparés pour éviter les interférences.

Parmis les sous-projets, on trouve par exemple :

- La proximité aux services urbains 
- La mobilité urbaine
- Enquêtes SHS
- Les bornes de recharge pour véhicules électriques
- Le journal de bord
- et d’autres qui peuvent naître au fil du projet.

L'organisation du projet est pensée pour être reproductible, modulaire et maintenable.

---

## **Arborescence générale du dépôt**

Voici la structure générale du dépot du projet. Je détaille le dossier `proxy` ici car c'est le plus abouti, mais les autres suivent une logique similaire.

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

<div class="kicker">Arborescence générale du dépôt :</div>

<ul class="tree">
  <li class="folder">📦 AttractiveCity
    <ul>
      <li class="folder">📂 proxy <span class="badge">Indicateurs de proximité</span>
        <ul>
          <li class="folder">📂 data
            <ul>
              <li class="folder">raw <span class="note">données brutes</span></li>
              <li class="folder">processed <span class="note">données nettoyées/intermédiaires</span></li>
              <li class="folder">final <span class="note">résultats finaux (cartes, indicateurs)</span></li>
            </ul>
          </li>
          <li class="folder">📂 notebooks <span class="note">exploration &amp; prototypage</span></li>
          <li class="folder">📂 src <span class="note">fonctions &amp; modules réutilisables</span></li>
          <li class="folder">📂 Notes <span class="note">méthodo, idées, biblio</span></li>
        </ul>
      </li>
      <li class="folder">📂 eChargeBouygues <span class="badge">Bornes de recharge</span></li>
      <li class="folder">📂 mob / mobility <span class="badge">Mobilité urbaine</span></li>
      <li class="folder">📂 UrbanBook <span class="badge">Journal de bord</span></li>
      <li class="folder">📂 Brouillons <span class="note">zone de tests / vrac</span></li>
      <li class="folder">📂 .history <span class="note">historique des versions</span></li>
      <li class="file">📄 requirements.yml <span class="note">environnement &amp; dépendances</span></li>
    </ul>
  </li>
</ul>

---

## **Outils utilisés**

### **QGIS**

QGIS est un SIG open source pour visualiser, éditer et analyser des données géographiques.  
Téléchargement : <https://qgis.org/en/site/forusers/download.html>

````{admonition} Version utilisée pour ce projet
:class: important
**QGIS 3.38.3 “Grenoble”** — Windows 10 (Version 2009)
````

```{dropdown} Détails techniques de QGIS et extensions Python actives

| Composant              | Version              |
| ---------------------- | -------------------- |
| QGIS code revision     | 37f9e6efee           |
| Qt                     | 5.15.13              |
| Python (embarqué QGIS) | 3.12.6               |
| GDAL/OGR               | 3.9.2                |
| PROJ                   | 9.4.0                |
| EPSG Registry DB       | v11.004 (2024-02-24) |
| GEOS                   | 3.12.2-CAPI-1.18.2   |
| SQLite                 | 3.45.1               |
| PDAL                   | 2.6.3                |
| Client PostgreSQL      | 16.2                 |
| SpatiaLite             | 5.1.0                |
| QWT                    | 6.2.0                |
| QScintilla2            | 2.14.1               |

```{dropdown} Extensions Python actives (plugins)
- BatchHeatmaps-master — 1.1  
- cigeoe_holes_3d — 1.0.0  
- DataPlotly — 4.2.0  
- densityanalysis — 2024.8.28  
- dzetsaka — 3.70  
- esstoolkit — 0.3.10  
- GeometryShapes — 0.7  
- GroupStats — 2.2.7  
- HCMGIS — 25.1.9  
- latlontools — 3.7.3  
- mmqgis — 2024.11.8  
- ORStools — 1.10.0  
- OSMDownloader — 1.0.3  
- osm_sidewalkreator — 1.2.1  
- pointsamplingtool — 0.5.4  
- processing_saga_nextgen — 1.0.0  
- profiletool — 4.2.6  
- Qgis2threejs — 2.8  
- qgis2web — 3.25.0  
- QGIS3_Delft3D_FM — 1.0  
- qgiscloud — 3.9.14  
- QNEAT3 — 1.0.6  
- QuickOSM — 2.3.2  
- quick_map_services — 0.20.0  
- StreetView — 3.3  
- db_manager — 0.1.20  
- MetaSearch — 0.3.6  
- processing — 2.12.99
```

```{note}
Ces informations proviennent de **Aide ▸ À propos de QGIS ▸ Informations système**.  
Elles servent à assurer la **reproductibilité** et à diagnostiquer d’éventuels écarts entre machines (versions de GDAL/PROJ/GEOS, etc.).
```
---

### **Environnement Python**

Pour les analyses hors QGIS (scripts et notebooks), j’utilise un **environnement Python dédié**, décrit dans le fichier `requirements.yml` à la racine du projet. Ce fichier fixe toutes les dépendances et leurs versions, ce qui garantit l’exécution du code, sa **reproductibilité** et sa **portabilité**. À partir de ce fichier, l’environnement peut être recréé à l’identique sur une autre machine.  
Je recommande d’utiliser **Conda/Mamba** pour la gestion de l’environnement : <https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html>.

> Remarque — Le Python embarqué dans QGIS est **3.12.6**. L'environnement conda/mamba est différent (`python=3.9.19`) : ce n’est pas un problème tant que j'exécute les notebooks dans **l’environnement documenté** et que les dépendances sont bien figées dans `requirements.yml`.

Pour créer l'environnement Python, il suffit de lancer la commande suivante dans un terminal :

```bash
conda env create -f requirements.yml
```
Pré-requis :

- Être dans le répertoire racine du projet (là où se trouve `requirements.yml`).
- Avoir Conda installé (Anaconda ou Miniconda).

Pour activer cet environnement, utilisez la commande :

```bash
conda activate geo_env
``` 
où `geo_env` est le nom de l'environnement défini dans le fichier `requirements.yml`. 

Pour le desactiver, utilisez :

```bash
conda deactivate
```

Dans le cas où les pré-requis ne sont pas remplis, la partie suivante explique comment faire.
