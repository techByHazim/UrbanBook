# =============================================================================
# Author : Hazim
# Date of creation : June 2025

# =============================================================================
# Description :
# This file contains all the configuration parameters for the project.
# The input/output files for the databases used (BPE, OSM, network, etc.)
# , the results obtained in the calculations, the calculation parameters
# Modifying this file allows adapting the processing pipeline to needs
# =============================================================================

# =============================================================================
# COORDINATE SYSTEM
# =============================================================================

epsg = 2154  # Lambert 93 for France
city = "Marseille"  # Study city

# =============================================================================
# GENERAL INPUT/OUTPUT FOLDERS
# =============================================================================
import json
from pathlib import Path 

input_folder = Path("..") / "proxy" / "data" / "raw" / "insee"
output_folder = Path("..") / "proxy" / "data" / "processed"
output_final = Path("..") / "proxy" / "data" / "final"

output_merge = output_final / "merged_score.gpkg"  # Output file for merged scores
# =============================================================================
# STUDY AREA : MARSEILLE (can be modified for other cities)
# =============================================================================

cadre_file = input_folder / f"Cadre{city}.shp" # Here a bbox around Marseille made with QGIS but it can be any geometry study area

# =============================================================================
# FOR THE EQUIPMENT OF THE BPE 2023 (BASE PERMANENTE DES EQUIPEMENTS, INSEE)
# =============================================================================

# Input/output files for the BPE POIs (INSEE)
poi_file_parquet = input_folder / "bpe23.parquet"  # Parquet file containing BPE 2023 points (France)
poi_file = output_folder / f"bpe23_{city}.gpkg" # Output file for BPE 2023 points filtered on the study area (Marseille)
# poi_list_file = input_folder / "services_features2509081130.xlsx" # Excel table with equipments features for social functions and associated weights
poi_list_file = input_folder / "services_features2509121322.xlsx"

# =============================================================================
# LIST OF RETAINED URBAN SOCIAL FUNCTIONS
# =============================================================================

# FS_LIST = ['provisioning', 'entrainment', 'care', 'education', 'working', 'living', 'Transport'] # This list can be modified to include or exclude other categories
FS_LIST = ['Entrainment', 'Mobility', 'Food', 'Active_living', 'Community', 'Health_and_wellbeing', 'Education']
# =============================================================================
# PARAMETERS FOR CALCULATING THE DIVERSITY OF SOCIAL FUNCTIONS
# =============================================================================

# The social function to analyze
# Radius (in meters) for calculating diversity
div_radius = 80

# Dynamic output files for each social function with diversity
poi_proj_files = {
    fs: output_folder / f"bdd_div_{fs}_{div_radius}m_{city}.gpkg"
    for fs in FS_LIST
}

# Output file for points projected onto the road network
output_filename_projections = {
    fs: output_folder / f"bdd_div_{fs}_{div_radius}m_proj_{city}.gpkg"
    for fs in FS_LIST
}

# =============================================================================
# ROAD NETWORK FOR PEDESTRIANS
# =============================================================================

# Input/output files for the road network
input_pbf = input_folder / "provence-alpes-cote-d-azur-latest.osm.pbf" # OSM data (PACA) from geofabrik in PBF format
output_gpkg = output_folder / "osm_roads_network_paca_footlua.gpkg"  # OSM pedestrian road network (PACA) in GPKG format after processing

# File for the pedestrian road network filtered on Marseille
roads_file_mrs = output_folder / f"osm_foot_network_{city}.gpkg"

# Pedestrian network in the study area (Marseille) simplified (contains only the osm_id and the geometries of the roads)
roads_simplify_file = f"C:/Users/hazim/Desktop/AttractiveCity/proxy/data/processed/osm_foot_network_{city}_simplified.gpkg" # absolute path because post-QGIS

# =============================================================================
# LIXELISATION OF THE ROAD NETWORK
# =============================================================================

# To lixelize the pedestrian road network, we use the simplified road geometries
# and cut them into fixed-size lixels using QGIS.

lixel_size = 10 # lixel size in meters, it's can be adjusted according

# Output file for lixelized road network 
roads_lixels_file = f"C:/Users/hazim/Desktop/AttractiveCity/proxy/data/processed/osm_foot_network_{city}_simplified_lixels{lixel_size}m.shp" # absolute path because post-QGIS

# =============================================================================
# PARAMETERS FOR THE CALCULATION 
# =============================================================================

# Kernel type 
kernel_type = "exponential"  # "gaussian" or "exponential"
# The bandwidth in meters (to be adjusted according to the area of interest)
bandwidth = 100
# Kernel cutoff (a factor to multiply by the bandwidth for cutoff)
cutoff_factor = 5 # for example, 5 for 600m cutoff at bandwidth 200m

# =============================================================================
# OUTPUTS AND RESULT FILES
# =============================================================================

# Path where the lixel graph will be saved or loaded 
# to avoid recalculating it each time, too time-consuming especially with small lixels
graph_path = output_final / f"graph_lixels_network_{city}{lixel_size}m.pkl"

# Output path for calculation results for each social function
output_paths = {
    fs: output_final / f"score_{fs}_d{div_radius}m_bw{bandwidth}m_Cut{cutoff_factor*bandwidth}_lxl_{lixel_size}m_{city}.gpkg"
    for fs in FS_LIST
}

# =============================================================================
# CONFIGURATION FOR OSM Overpass API (To extract equipment not in the BPE)
# =============================================================================
CONFIG_PATH = input_folder /"overpass_config.json"  # json file with list of tags (key, value) to extract
OUTPUT_DIR = output_folder / f"overpass_results_{city}"  # output folder

# =============================================================================
# FILES FOR SAVING OVERPASS RESULTS AND ADDITIONAL POIS
# =============================================================================

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

# list of output files for each tag in the JSON config file
poi_file_additional = [
    OUTPUT_DIR / f"{eq['key']}_{eq['value']}_{city}.gpkg"
    for eq in config["tags"]
    if (OUTPUT_DIR / f"{eq['key']}_{eq['value']}_{city}.gpkg").exists()
]

# =============================================================================
# FOR PUBLIC TRANSPORT
# =============================================================================

# For Public Transport, we use the GTFS (General Transit Feed Specification) data
# from MAMP (Métropole Aix-Marseille-Provence) available here : https://transport.data.gouv.fr/datasets/reseau-rtm-gtfs/

base_path = Path("..") / "proxy" / "data" / "raw" /"transport" / "mamp-all.gtfs"
