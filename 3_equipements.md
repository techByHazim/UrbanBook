---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# **Les équipements urbains et leur ressource de données**

Les équipements urbains (ou aménités) sont des **points d’intérêt** qui structurent les pratiques quotidiennes et influencent la qualité de vie locale. Ils incluent : 
* les commerces (boulangerie, supermarché, pharmacie, etc.),
* les services (écoles, crèches, bureaux de poste, etc.),
* les équipements publics (parcs, bibliothèques, équipements sportifs, etc.),
* les infrastructures de transport (arrêts de bus, stations de vélo en libre-service, etc.).

## **Rôle des équipements dans l’indicateur**

Dans le calcul de l'indicateur de proximité (voir chapitre [Indicateurs de proximité](11_indicateur.md)), les équipements jouent un rôle crucial en tant que **destinations** vers lesquelles les distances piétonnes sont mesurées. Leur présence et leur accessibilité influencent directement le score de proximité d'une adresse donnée.

## **Sources de données**

* **La Base Permanente des Équipements (BPE, INSEE)** :

  * couverture nationale homogène,
  * classification fine des équipements,
  * mise à jour régulière.

* **OpenStreetMap** :
* **Fichier Excel des équipementsds** :

  * attribution d’une valeur relative aux équipements selon leur rôle social,
  * hiérarchisation des besoins quotidiens (ex. boulangerie > cinéma).
* Ces deux sources combinées permettent d’enrichir la base brute pour refléter les **priorités sociales et fonctionnelles**.


## **Catégories des aménités**

```{code-cell} python
:tags: [hide-input]

import pandas as pd, json
from pathlib import Path
from IPython.display import HTML

# --- CONFIG ---
excel_path = Path("../proxy/data/raw/insee/services_features2509121322.xlsx")
sheet_name = "Categories of Amenities"   # ou index: 0
max_rows_preview = 200                   # garde un aperçu performant
MAX_UNIQUE_FOR_FILTER = 40               # seuil pour proposer un filtre par liste
ONLY_OBJECT_FOR_SELECT = True            # True = filtres liste seulement pour dtype=object

# Lecture et sous-échantillon d’affichage
df = pd.read_excel(excel_path, sheet_name=sheet_name)
df_view = df.head(max_rows_preview).copy()

# Détecte les colonnes catégorielles (peu de modalités) → <select multiple>
cat_cols = []
for col in df_view.columns:
    nunique = df_view[col].nunique(dropna=True)
    if nunique and nunique <= MAX_UNIQUE_FOR_FILTER:
        if (not ONLY_OBJECT_FOR_SELECT) or (df_view[col].dtype == "object"):
            cat_cols.append(col)

# Options par colonne (triées), "(Tous)" = vide (= pas de filtre)
col_options = {
    c: ["(Tous)"] + sorted(df_view[c].dropna().astype(str).unique().tolist())
    for c in cat_cols
}

# Table HTML légère
table_html = df_view.to_html(
    index=False, border=0, classes="gtfs-table", escape=False
)

# JS reçoit les options & l’ordre des colonnes
payload = {
    "columns": df_view.columns.tolist(),
    "options": col_options,
}
js_payload = json.dumps(payload)

html = f"""
<div class="table-wrapper">

  <div class="toolbar">
    <div class="search">
      <input type="text" id="global-search" placeholder="Rechercher (toutes colonnes)…" />
      <button id="reset-filters" title="Réinitialiser">⟲</button>
    </div>
    <div class="meta">
      Aperçu de <code>{excel_path.name}</code> — {len(df)} lignes au total (affiché {len(df_view)})
    </div>
  </div>

  <div class="scrollbox">
    {table_html}
  </div>
</div>

<style>
  .table-wrapper {{ font-size: .95rem; }}
  .toolbar {{ display: grid; gap: .5rem; margin: 0 0 .5rem 0; }}
  .toolbar .search {{ display:flex; gap:.5rem; align-items:center; }}
  .toolbar input[type="text"], .toolbar select {{
    padding:.45rem .6rem; border:1px solid #e5e7eb; border-radius:6px; background:#fff; color:#111827;
  }}
  .toolbar button {{ padding:.45rem .6rem; border:1px solid #e5e7eb; border-radius:6px; background:#f3f4f6; cursor:pointer; }}
  .toolbar .meta {{ font-size:.85rem; opacity:.85; }}

  .scrollbox {{ max-height: 460px; overflow:auto; border:1px solid #e5e7eb; border-radius:8px; }}

  .gtfs-table {{ border-collapse: collapse; width:max-content; min-width:60%; }}
  .gtfs-table th, .gtfs-table td {{
    padding:.5rem .75rem; border:1px solid #e5e7eb; white-space:nowrap; text-align:left;
  }}
  .gtfs-table thead th {{ position: sticky; top:0; background:#f7f7f7; color:#111827; z-index:3; }}
  /* ligne des filtres sous l'entête */
  .gtfs-table thead tr.filters-row th {{
    position: sticky; top: 40px; background:#fafafa; z-index:2; padding:.35rem .5rem;
  }}
  .col-filter, .col-text-filter {{ width: 100%; box-sizing: border-box; font-size:.9rem; }}
  .col-filter[multiple] {{ height: 2.2rem; }} /* compact multi-select */

  /* Mode sombre */
  @media (prefers-color-scheme: dark) {{
    .toolbar input[type="text"], .toolbar select {{ background:#111827; border-color:#374151; color:#e5e7eb; }}
    .toolbar button {{ background:#1f2937; border-color:#374151; color:#e5e7eb; }}
    .scrollbox {{ border-color:#374151; }}
    .gtfs-table th, .gtfs-table td {{ border-color:#374151; color:#e5e7eb; background:#0b1220; }}
    .gtfs-table thead th {{ background:#1f2937; color:#f3f4f6; }}
    .gtfs-table thead tr.filters-row th {{ background:#162033; }}
    .toolbar .meta {{ color:#c7d2fe; }}
  }}
</style>

<script>
(() => {{
  const DATA = {js_payload};
  const table = document.querySelector('.gtfs-table');
  if (!table) return;

  const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
  const tbodyRows = Array.from(table.querySelectorAll('tbody tr'));

  // Insère une ligne de filtres juste sous l'entête
  const thead = table.querySelector('thead');
  const filterRow = document.createElement('tr');
  filterRow.className = 'filters-row';

  headers.forEach((colName, idx) => {{
    const th = document.createElement('th');
    th.style.padding = '0.25rem 0.4rem';

    if (DATA.options[colName]) {{
      // Sélecteur multi-valeurs sur colonnes catégorielles
      const sel = document.createElement('select');
      sel.className = 'col-filter';
      sel.setAttribute('data-col', colName);
      sel.setAttribute('multiple', '');
      // Ajoute l'option "(Tous)" + valeurs
      DATA.options[colName].forEach(v => {{
        const opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        if (v === '(Tous)') opt.selected = true; // sélectionne "(Tous)" au départ
        sel.appendChild(opt);
      }});
      th.appendChild(sel);
    }} else {{
      // Champ texte (filtre "contient")
      const inp = document.createElement('input');
      inp.type = 'text';
      inp.placeholder = 'filtrer…';
      inp.className = 'col-text-filter';
      inp.setAttribute('data-col', colName);
      th.appendChild(inp);
    }}
    filterRow.appendChild(th);
  }});
  thead.appendChild(filterRow);

  const searchInput = document.getElementById('global-search');
  const resetBtn = document.getElementById('reset-filters');

  function getSelected(sel) {{
    // renvoie un Set des valeurs sélectionnées (hors "(Tous)")
    const vals = Array.from(sel.selectedOptions).map(o => o.value);
    const filtered = vals.filter(v => v !== '(Tous)');
    return new Set(filtered);
  }}

  function rowMatches(tr, term) {{
    const t = term.toLowerCase();
    if (t) {{
      const any = Array.from(tr.cells).some(td => (td.textContent || '').toLowerCase().includes(t));
      if (!any) return false;
    }}
    // Filtres par colonne
    const colFilters = Array.from(document.querySelectorAll('.col-filter'));
    for (const sel of colFilters) {{
      const col = sel.getAttribute('data-col');
      const selected = getSelected(sel);
      if (selected.size === 0) continue; // "(Tous)" sélectionné → pas de filtre
      const idx = headers.indexOf(col);
      const cellText = (tr.cells[idx]?.textContent || '').trim();
      if (!selected.has(cellText)) return false;
    }}
    // Filtres texte par colonne
    const txtFilters = Array.from(document.querySelectorAll('.col-text-filter'));
    for (const inp of txtFilters) {{
      const col = inp.getAttribute('data-col');
      const val = (inp.value || '').toLowerCase().trim();
      if (!val) continue;
      const idx = headers.indexOf(col);
      const cellText = (tr.cells[idx]?.textContent || '').toLowerCase();
      if (!cellText.includes(val)) return false;
    }}
    return true;
  }}

  function applyFilters() {{
    const term = (searchInput?.value || '').trim();
    for (const tr of tbodyRows) {{
      tr.style.display = rowMatches(tr, term) ? '' : 'none';
    }}
  }}

  // Écouteurs
  searchInput?.addEventListener('input', applyFilters);
  document.querySelectorAll('.col-filter').forEach(sel => sel.addEventListener('change', applyFilters));
  document.querySelectorAll('.col-text-filter').forEach(inp => inp.addEventListener('input', applyFilters));
  resetBtn?.addEventListener('click', () => {{
    if (searchInput) searchInput.value = '';
    document.querySelectorAll('.col-filter').forEach(sel => {{
      // remet "(Tous)" sélectionné uniquement
      Array.from(sel.options).forEach(o => o.selected = (o.value === '(Tous)'));
    }});
    document.querySelectorAll('.col-text-filter').forEach(inp => inp.value = '');
    applyFilters();
  }});

  applyFilters(); // premier passage
}})();
</script>
"""

HTML(html)
```


