# Automatisation du processus d'extraction du réseau

Après avoir exploré les données et compris la structure du graphe, j’ai souhaité **automatiser tout le processus de construction du réseau piéton**.  
L’objectif est simple : **tout faire en une seule exécution**, depuis le téléchargement des données jusqu’à la sauvegarde finale des fichiers sans avoir à répéter manuellement chaque étape.

## Principe général

L’idée est d’encapsuler toutes les étapes dans une classe Python :  

1. **Télécharger** le réseau piéton depuis OpenStreetMap à partir d’un polygone d’emprise (ex. la ville de Marseille).  
2. **Construire** un graphe piéton sans tenir compte du sens de circulation (puisqu’à pied, on peut circuler librement dans les deux sens).  
3. **Convertir** ce graphe en GeoDataFrames (nœuds et arêtes).  
4. **Reprojeter** les couches dans le bon système de coordonnées (EPSG).  
5. **Sauvegarder** automatiquement :
   - les nœuds et arêtes en **GeoPackage** (pour QGIS),
   - le graphe complet en **Pickle** (pour les analyses en Python).


:::{toggle} **Afficher le code complet (masqué par défaut)**
```python
# -*- coding: utf-8 -*-
# =============================================================================
# Author : Hazim
# Date   : Oct 2025
# =============================================================================
# Description :
# Build and export a pedestrian network from OpenStreetMap, with automatic
# saving of nodes, edges (GeoPackage) and the full graph (Pickle).
# =============================================================================

import osmnx as ox
import logging
from tqdm import tqdm
from data_io import load_bbox_polygon, save_graph
# from config import (
#     edges_roads_file, nodes_roads_file, custom_filter,
#     epsg, cadre_file, graph_path_lixel
# )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

class PedestrianNetwork:
    """Build, process, and export a pedestrian network from OpenStreetMap."""

    def __init__(self, area_file, custom_filter, epsg,
                 output_nodes, output_edges, output_graph=None):
        self.area_file = area_file
        self.custom_filter = custom_filter
        self.epsg = epsg
        self.output_nodes = output_nodes
        self.output_edges = output_edges
        self.output_graph = output_graph
        self.graph = None
        self.nodes = None
        self.edges = None

    def build_graph(self, simplify=True, retain_all=False):
        """Download and build an undirected pedestrian graph from OSM."""
        logger.info("Loading area polygon and downloading network...")
        try:
            polygon = load_bbox_polygon(self.area_file)
            G = ox.graph_from_polygon(
                polygon,
                custom_filter=self.custom_filter,
                simplify=simplify,
                retain_all=retain_all
            )
            self.graph = ox.utils_graph.get_undirected(G)
            logger.info(
                f"Graph built successfully: {len(self.graph.nodes)} nodes, "
                f"{len(self.graph.edges)} edges."
            )
        except Exception as e:
            logger.error(f"Error while building graph: {e}")
            raise

    def to_geodataframes(self):
        """Convert the graph to GeoDataFrames and reproject to target CRS."""
        if self.graph is None:
            raise ValueError("Graph not built yet.")

        self.nodes, self.edges = ox.graph_to_gdfs(self.graph)
        self.nodes = self.nodes.to_crs(self.epsg)
        self.edges = self.edges.to_crs(self.epsg)
        logger.info(f"Converted and reprojected to {self.epsg}.")

    def save(self):
        """Save nodes and edges to GeoPackage files."""
        if self.nodes is None or self.edges is None:
            raise ValueError("GeoDataFrames not available. Run to_geodataframes() first.")

        for gdf, path in tqdm(
            zip([self.nodes, self.edges],
                [self.output_nodes, self.output_edges]),
            total=2, desc="Saving layers", ncols=80
        ):
            gdf.to_file(path, driver="GPKG")
            logger.info(f"Saved: {path}")

    def save_graph_pickle(self):
        """Save the NetworkX graph as a pickle file, reprojected to self.epsg."""
        if not self.graph:
            logger.warning("No graph to save.")
            return

        try:
            target_crs = f"EPSG:{self.epsg}" if not str(self.epsg).startswith("EPSG:") else self.epsg
            graph_crs = self.graph.graph.get("crs")

            # Project if needed
            if graph_crs != target_crs:
                logger.info(f"Projecting graph to {target_crs} before saving...")
                self.graph = ox.project_graph(self.graph, to_crs=target_crs)
                self.graph.graph["crs"] = target_crs

            if self.output_graph:
                save_graph(self.graph, self.output_graph)
                logger.info(f"Graph saved (projected to {target_crs}): {self.output_graph}")
            else:
                logger.warning("No graph path provided. Skipping pickle save.")
        except Exception as e:
            logger.error(f"Error while saving graph: {e}")
            raise

    def run(self):
        """Execute the full pipeline."""
        logger.info("=== Pedestrian network extraction started ===")
        try:
            self.build_graph()
            self.to_geodataframes()
            self.save()
            self.save_graph_pickle()
            logger.info("Extraction completed successfully.")
        except Exception as e:
            logger.exception(f"Pipeline failed: {e}")
        finally:
            logger.info("=== Process finished ===")

# if __name__ == "__main__":
#     network = PedestrianNetwork(
#         area_file=cadre_file,
#         custom_filter=custom_filter,
#         epsg=epsg,
#         output_nodes=nodes_roads_file,
#         output_edges=edges_roads_file,
#         output_graph=graph_pickle_file
#     )
#     network.run()
```
:::

## Explications 

1. **Création de la classe `PedestrianNetwork`**
   Elle contient toutes les étapes nécessaires : construction, conversion, projection et sauvegarde.

2. **Méthode `build_graph()`**
   Elle télécharge le réseau piéton à partir d’un polygone (`area_file`) et applique un filtre personnalisé pour ne garder que les voies praticables à pied.
   Ensuite, le graphe est rendu **non orienté**, car à pied il n’est pas nécessaire de tenir compte du sens de circulation.

3. **Méthode `to_geodataframes()`**
   Elle transforme le graphe en **GeoDataFrames** pour pouvoir les manipuler ou les afficher dans QGIS.

4. **Méthode `save()`**
   Elle sauvegarde les nœuds et arêtes au format **GeoPackage (.gpkg)**, parfait pour une intégration dans un SIG.

5. **Méthode `save_graph_pickle()`**
   Elle sauvegarde le graphe complet en **Pickle (.pkl)** pour le réutiliser directement en Python, sans avoir à le reconstruire.

6. **Méthode `run()`**
   C’est la fonction principale : elle enchaîne toutes les étapes automatiquement.

## En pratique

Une fois les chemins et paramètres définis dans un fichier `config.py`,
il suffit d’exécuter **une seule ligne** pour tout faire :

```python
network = PedestrianNetwork(
    area_file=cadre_file,
    custom_filter=custom_filter,
    epsg=epsg,
    output_nodes=nodes_roads_file,
    output_edges=edges_roads_file,
    output_graph=graph_pickle_file
)
network.run()
```

Les fichiers obtenus peuvent ensuite être visualisées directement dans QGIS.


