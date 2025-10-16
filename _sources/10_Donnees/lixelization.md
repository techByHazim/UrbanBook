# Lixelisation et graphe du réseau 

## Lixelisation du réseau routier 

Cette étape consiste à **lixeliser le réseau routier**, c’est-à-dire à découper chaque tronçon en petits segments de longueur fixe (*lixels*). Cela permet d’obtenir un réseau régulier, mieux adapté aux calculs de distance, d’accessibilité ou de densité le long des voies.  

### Méthode 1 : Lixelisation via QGIS Processing  

Dans une première version, la lixelisation était effectuée directement à l’aide de l’algorithme intégré de QGIS : [`native:splitlinesbylength`](https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#split-lines-by-maximum-length) 
.  
Cette méthode repose sur le moteur **Processing**, qui exécute les outils géométriques de QGIS depuis un script Python.  

**Pseudo-code :**
```

1. Initialiser l’environnement QGIS et les chemins nécessaires.
2. Charger le réseau routier nettoyé (GeoPackage ou Shapefile).
3. Exécuter l’algorithme "Split Lines by Length"
   avec la taille de lixel souhaitée (ex. 10 m).
4. Sauvegarder le réseau découpé dans un nouveau fichier.

```

````{dropdown} Afficher / masquer le code 
```python
# # -*- coding: utf-8 -*-
# # =============================================================================
# # Author : Hazim
# # Date of creation : March 2025
# # -*- coding: utf-8 -*-
# # =============================================================================
# # Author : Hazim
# # Date of creation : March 2025

# # =============================================================================
# # Description :
# # This script contains functions for lixelising a road network using QGIS Processing tools.
# # The lixelisation process involves splitting the road network into smaller segments (lixels) based on a specified size.
# # =============================================================================

# import os
# import sys
# from tqdm import tqdm

# # Paths QGIS/Processing
# PROCESSING_PATHS = [
#     'c:/Program Files (x86)/sDNA',
#     'C:/Users/hazim/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/sdna',
#     'C:/Users/hazim/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/morpheo/gui',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv/Library/python',
#     'C:/Users/hazim/AppData/Roaming/QGIS/QGIS3/profiles/default/python',
#     'C:/Users/hazim/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv/Library/python/plugins',
#     'C:/Users/hazim/Desktop/TheseUrbanScience',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv/python39.zip',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv/DLLs',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv/lib',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv/Library/bin',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv',
#     'C:/Users/hazim/AppData/Local/anaconda3/envs/pynkdv/lib/site-packages',
#     'C:/Users/hazim/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/HCMGIS/forms',
#     'C:/Users/hazim/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/mmqgis/forms'
# ]

# def set_processing_path():
#     for path in tqdm(PROCESSING_PATHS, desc="Adding QGIS paths"):
#         if path not in sys.path:
#             sys.path.append(path)

# def initialiser_processing():
#     set_processing_path()
#     import processing
#     from processing.core.Processing import Processing

#     print("Initializing QGIS Processing...")
#     Processing.initialize()
#     print("Processing initialized.")

# def lixeliser_reseau(roads_simplify_file, roads_lixels_file, lixel_size):
#     import processing
#     if not os.path.exists(roads_simplify_file):
#         raise FileNotFoundError(f"File not found: {roads_simplify_file}")

#     print(f"Lixelisation on process (size: {lixel_size}m)...")
#     processing.run("native:splitlinesbylength", {
#         'INPUT': roads_simplify_file,
#         'LENGTH': lixel_size,
#         'OUTPUT': roads_lixels_file
#     })
#     print("Lixelisation completed.")

```
````

Cette approche donne de bons résultats, mais elle dépend d’une installation complète de QGIS et de sa configuration interne, ce qui la rend peu portable.

### Méthode 2 : Lixelisation en Python   

Pour lever cette contrainte, je propose une version **entièrement Python**.  
J'utilise les bibliothèques **GeoPandas** et **Shapely** pour les opérations géométriques,  
et **ProcessPoolExecutor** pour paralléliser le traitement.  

**Pseudo-code :**

```

1. Charger le réseau routier nettoyé.
2. Vérifier que le CRS est projeté en mètres (ex. EPSG:2154).
3. (Optionnel) Simplifier les lignes si elles sont très détaillées.
4. Pour chaque ligne :

   * Parcourir la géométrie à intervalles réguliers.
   * Extraire chaque segment (lixel) de longueur définie.
   * Conserver les attributs du tronçon d’origine.
5. Exécuter ces opérations en parallèle sur plusieurs cœurs.
6. Rassembler les lixels dans un GeoDataFrame.
7. Enregistrer le résultat (au format GeoPackage).

```

C'est **plus portable**, **plus rapide** et **plus flexible**. 
Le code Python détaillé de réaliser ce decoupage avec les étapes pré-cités peut etre consulter ci dessous : 

````{dropdown} Afficher / masquer le code Python
```python
# # -*- coding: utf-8 -*-
# # =============================================================================
# # Author : Hazim
# # Date of creation : March 2025

from __future__ import annotations 

from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
import math
import os
# from config import roads_lixels_file, roads_simplify_file

import geopandas as gpd
from shapely.geometry import LineString, MultiLineString
from shapely.ops import substring
from shapely import wkb
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from typing import Tuple, Optional, Union

# utilitaires

def _parse_path_layer(p: Union[str, Path]) -> Tuple[Path, Optional[str]]:
    """Accepts Path OR 'file.gpkg|layername=...'. Returns (pure_path, layer_or_None)."""
    s = str(p)  # handle WindowsPath etc.
    if "|layername=" in s:
        f, layer = s.split("|layername=", 1)
        return Path(f), layer.strip()
    return Path(s), None

def _check_projected(gdf: gpd.GeoDataFrame) -> None:
    if gdf.crs is None:
        raise ValueError("CRS manquant. Reprojetez en mètres (ex: EPSG:2154) avant la lixelisation.")
    if getattr(gdf.crs, "is_geographic", False) or getattr(gdf.crs, "is_geodetic", False):
        raise ValueError(
            f"CRS géographique détecté ({gdf.crs.to_string()}). "
            "Utilisez un CRS projeté en mètres (ex: EPSG:2154)."
        )

def _split_line(line: LineString, step: float) -> List[LineString]:
    L = line.length
    if L <= 0:
        return []
    out, d = [], 0.0
    # boucle le long de la ligne par pas "step"
    while d < L:
        d2 = min(d + step, L)
        seg = substring(line, d, d2, normalized=False)
        if isinstance(seg, LineString) and len(seg.coords) >= 2:
            out.append(seg)
        d = d2
    return out

def _split_any(geom, step: float) -> List[LineString]:
    if isinstance(geom, LineString):
        return _split_line(geom, step)
    if isinstance(geom, MultiLineString):
        res = []
        for ls in geom.geoms:
            res.extend(_split_line(ls, step))
        return res
    return []


# worker parallèle

def _worker_split_batch(tasks: List[Tuple[bytes, Dict[str, Any], float, bool]]) -> Tuple[List[Dict[str, Any]], List[LineString]]:
    """
    Traite un paquet de géométries sérialisées en WKB.
    tasks: liste de (wkb_geom, attrs, step, keep_attrs)
    Return (records, geoms)
    """
    recs, geoms = [], []
    for wkb_geom, attrs, step, keep_attrs in tasks:
        geom = wkb.loads(wkb_geom)
        parts = _split_any(geom, step)
        base = attrs if keep_attrs else {}
        for i, seg in enumerate(parts):
            rec = dict(base)
            rec["lixel_idx"] = i
            rec["lx_len"] = float(seg.length)
            recs.append(rec)
            geoms.append(seg)
    return recs, geoms


# fonction principale 
def lixelize_roads(
    roads_simplify_file: Union[str, Path],
    roads_lixels_file: Union[str, Path],
    lixel_size: float,
    *,
    n_jobs: Optional[int] = None,
    chunk_size: int = 2000,
    keep_attrs: bool = True,
    simplify_tolerance: Optional[float] = None,  # ex: 0.2 à 1.0 m pour lisser les lignes (facultatif)
    progress: bool = True,
) -> gpd.GeoDataFrame:
    """
    Lixelisation parallèle d'un réseau linéaire.

    Paramètres
    ----------
    roads_simplify_file : str
        Fichier d'entrée (shp/geojson/gpkg...). Supporte 'file.gpkg|layername=roads'.
    roads_lixels_file : str
        Fichier de sortie. Supporte 'file.gpkg|layername=lixels'. Recommandé: .gpkg
    lixel_size : float
        Taille des lixels en mètres (le dernier segment d'une ligne peut être plus court).
    n_jobs : int | None
        Nombre de processus. Par défaut, tous les cœurs dispo (os.cpu_count()).
    chunk_size : int
        Nombre de lignes source par paquet pour chaque worker (2000 est un bon compromis).
    keep_attrs : bool
        Conserver les attributs d'origine sur chaque lixel.
    simplify_tolerance : float | None
        Tolérance Douglas-Peucker (mètres) pour simplifier les lignes AVANT découpe (accélère beaucoup si lignes très détaillées).
    progress : bool
        Afficher estimations et barres de progression.

    Return
    ------
    GeoDataFrame des lixels, CRS conservé, avec colonnes ajoutées :
      - src_id     : index de la géométrie source
      - lixel_idx  : rang du lixel au sein de la source
      - lx_len     : longueur du lixel (m)
    """
    if lixel_size <= 0:
        raise ValueError("`lixel_size` doit être > 0 (mètres).")
    
    in_path, in_layer   = _parse_path_layer(roads_simplify_file)
    out_path, out_layer = _parse_path_layer(roads_lixels_file)
    if not in_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {in_path}")

    # Lecture entrée
    gdf = gpd.read_file(in_path, layer=in_layer) if in_layer else gpd.read_file(in_path)
    if gdf.empty:
        raise ValueError("Aucune géométrie en entrée.")
    _check_projected(gdf)

    # Option : simplification géométrique (gain énorme si lignes très denses)
    if simplify_tolerance and simplify_tolerance > 0:
        # preserve_topology=True évite de casser les formes de façon agressive
        gdf = gdf.set_geometry(gdf.geometry.simplify(simplify_tolerance, preserve_topology=True))

    # Estimation du nombre de lixels
    total_len_m = float(gdf.length.sum())
    est_lixels = int(total_len_m / float(lixel_size)) if lixel_size > 0 else 0
    if progress:
        print(f"Réseau ≈ {total_len_m/1000:.2f} km ; pas = {lixel_size} m ; "
              f"estimation ≈ {est_lixels:,} lixels")

    # Préparer les tâches en WKB (picklable, rapide à passer aux workers)
    def row_to_task(row) -> Tuple[bytes, Dict[str, Any], float, bool]:
        d = row._asdict()
        geom = d.pop("geometry")
        src_id = d.get("Index", row.Index) if hasattr(row, "Index") else row[0]
        d["src_id"] = src_id
        return wkb.dumps(geom), d if keep_attrs else {"src_id": src_id}, float(lixel_size), keep_attrs

    rows = list(gdf.itertuples(index=True))
    tasks = [row_to_task(r) for r in rows]

    # Parallélisation
    if n_jobs is None:
        n_jobs = max(1, (os.cpu_count() or 2) - 0)  # tous les cœurs

    # Découper en paquets pour limiter l’overhead d’ordonnancement
    def chunks(seq, size):
        for i in range(0, len(seq), size):
            yield seq[i:i+size]

    recs_all, geoms_all = [], []
    batches = list(chunks(tasks, chunk_size))

    if progress:
        pbar = tqdm(total=len(batches), desc=f"Découpage parallèle ({n_jobs} workers)")

    with ProcessPoolExecutor(max_workers=n_jobs) as ex:
        futures = [ex.submit(_worker_split_batch, batch) for batch in batches]
        for fut in as_completed(futures):
            recs, geoms = fut.result()
            recs_all.extend(recs)
            geoms_all.extend(geoms)
            if progress:
                pbar.update(1)

    if progress:
        pbar.close()

    if not recs_all:
        raise RuntimeError("Aucun lixel produit : vérifiez le CRS projeté et la taille.")

    out = gpd.GeoDataFrame(recs_all, geometry=geoms_all, crs=gdf.crs)

    # Écriture
    if out_path.suffix.lower() == ".gpkg":
        out.to_file(out_path, layer=(out_layer or "lixels"), driver="GPKG")
    else:
        out.to_file(out_path)

    if progress:
        print(f"Le réseau à {len(out):,} lixels sauvegardés dans {out_path} (couche: {out_layer or 'lixels'})")
        try:
            print(f"Lixel moyen: {out['lx_len'].mean():.2f} m")
        except Exception:
            pass

    return out

# if __name__ == "__main__":
#     lixelize_roads(roads_simplify_file=roads_simplify_file, roads_lixels_file=roads_lixels_file, lixel_size=10)
```
````

### Discussion sur les limites du découpage

Dans cette méthode, chaque tronçon est découpé en segments de longueur fixe, ce qui rend le réseau plus homogène.  
Mais ce choix n’est pas sans conséquences.  

* Le **dernier lixel** de chaque ligne est souvent plus court que les autres, car la longueur totale du tronçon n’est pas toujours un multiple exact de la taille de découpe.  
Ce “reste” est systématiquement attribué au dernier segment, ce qui crée de **légères inégalités de longueur** entre les lixels.  

* Les **tronçons plus courts que la taille du lixel** ne sont pas découpés du tout : ils conservent leur longueur d’origine, parfois bien inférieure à celle des autres segments.  
Cela introduit une petite hétérogénéité dans le réseau, mais qui reste acceptable (9.34m lixel moyen pour un pas de 10m).  

* La lixelisation ne prend pas en compte la géométrie locale (courbures, intersections, type de voie).  
Elle s’appuie uniquement sur la distance parcourue le long des lignes, ce qui peut légèrement décaler les points de coupure dans les zones très sinueuses.  
 

## Creation d'un graphe du réseau lixelisé

Pour exploiter le réseau lixelisé dans des analyses d’accessibilité, il est utile de le convertir en un **graphe**.
Je propose une fonction simple pour créer un graphe NetworkX à partir du GeoDataFrame des lixels.

````{dropdown} Afficher le code Python
```python
def create_graph_from_lixels(lixels_gdf):
    """Create a graph from the lixelized network"""
    G = nx.Graph()  # ou nx.DiGraph() si orienté
    for _, row in lixels_gdf.iterrows():
        line = row["geometry"]
        start = (line.coords[0][0], line.coords[0][1])
        end = (line.coords[-1][0], line.coords[-1][1])

        G.add_edge(
            start,
            end,
            length=line.length,
            lixel_id=row["id"],
            # geometry=line  
        )
    return G
```
````

Je prends les lixels et pour chaque segment, j’ajoute une arête entre ses points de début et de fin grâce à la fonction `add_edge` de NetworkX.
Ensuite, je stocke d'autres informations utiles dans le graphe (ID du lixel, longueur, type de voie,  etc.).
L’argument `geometry=line` permet de conserver la géométrie du lixel dans le graphe, ce qui est utile pour des analyses spatiales (calculs de distances , visualisation, etc.).