# Environnement du projet

## Environnement Python

Toutes les analyses hors QGIS (scripts et notebooks) s’appuient sur un **environnement virtuel Python dédié**.
Celui-ci est décrit dans le fichier `requirements.yml` (placé à la racine du projet).

Ce fichier liste toutes les bibliothèques et leurs versions. Il garantit :

* la **reproductibilité** (mêmes résultats sur n’importe quelle machine),
* la **portabilité** (facilité à partager ou réinstaller l’environnement).

## Pourquoi un environnement virtuel ?

```{admonition} Important
:class: important
Un environnement virtuel permet d’isoler les dépendances d’un projet de celles des autres projets ou du système. Ainsi, deux projets peuvent utiliser des versions différentes d’une même bibliothèque sans conflit.
```

## Outils de gestion d’environnement

Plusieurs gestionnaires d’environnement existent :  

- **venv** (natif à Python, simple et léger)  
- **Conda** (gestionnaire d’environnements et de paquets)  
- **Mamba** (alternative à Conda, beaucoup plus rapide)  
- **Poetry** (gestionnaire moderne de dépendances et de packaging)  
- **Pipenv** (similaire à Poetry, aujourd’hui moins répandu)  
- **Docker** (solution plus lourde, basée sur des conteneurs pour une portabilité complète)  

Dans ce projet, je recommande **Conda** (ou **Mamba**) car c’est la solution la plus simple et la plus robuste pour installer et gérer les bibliothèques géospatiales (*GDAL*, *PROJ*, *Rasterio*, *Fiona*, *Shapely*), qui nécessitent des dépendances systèmes difficiles à compiler avec `pip` seul.


## Installation de Conda/Mamba

1. **Installer Miniforge ou Mambaforge** (recommandé) ou Miniconda :

   * macOS Apple Silicon (M1/M2/M3) → installeur **ARM64**
   * macOS Intel → installeur **x86_64**
   * Windows → installeur **x86_64**

2. **Ouvrir un terminal** :

   * Windows → *Anaconda Prompt*, *Miniforge Prompt* ou *PowerShell*
   * macOS/Linux → application *Terminal*

3. **Initialiser conda** (à faire une seule fois sur macOS/Linux) :

   ```bash
   conda init zsh   # si vous utilisez zsh (par défaut sur macOS récents)
   conda init bash  # sinon
   ```

   → Fermez et rouvrez le terminal.

4. **Installer mamba** si nécessaire :

   ```bash
   conda install -n base -c conda-forge mamba
   ```

5. **Configurer conda-forge comme canal principal** (conseillé pour la géo) :

   ```bash
   conda config --add channels conda-forge
   conda config --set channel_priority strict
   ```

## Création de l’environnement virtuel

Depuis un terminal, placez-vous dans le dossier racine du projet et lancez :

```bash
conda env create -f requirements.yml  # ou mamba env create -f requirements.yml
```

Cela installe automatiquement un environnement nommé **`geo_env`**.

*Pré-requis :*

* Avoir installé Conda (via [Anaconda](https://www.anaconda.com/download) ou [Miniconda](https://docs.conda.io/en/latest/miniconda.html)).

* Être dans le dossier du projet contenant `requirements.yml`.

## Mise à jour de l’environnement

Pour mettre à jour l'environnement `geo_env` existant :

  ```bash
  mamba env update -n geo_env -f requirements.yml --prune
  ```

  (l’option `--prune` supprime les dépendances devenues inutiles)

On peut **tout** faire avec `conda` en remplaçant `mamba` par `conda` dans les commandes.

## Gestion au quotidien

* **Activer / désactiver**

  ```bash
  mamba activate geo_env   # ou conda activate geo_env
  mamba deactivate         # ou conda deactivate
  ```

* **Lister les environnements disponibles**

  ```bash
  conda env list
  ```

## Utiliser l’environnement dans Jupyter

Pour exécuter les notebooks avec l’environnement `geo_env`, ajoutez-le à Jupyter :

```bash
python -m ipykernel install --user --name geo_env --display-name "Python (geo_env)"
```

Ensuite, dans Jupyter Notebook/Lab, choisissez le noyau **Python (geo_env)**.


## Modifier ou réparer l’environnement

* **Ajouter un paquet** :

  ```bash
  mamba install -n geo_env <nom-du-paquet> -c conda-forge
  ```

* **Installer via pip (au besoin)** :

  ```bash
  python -m pip install <nom-du-paquet>
  ```

* **Exporter les changements dans `requirements.yml`** :

  ```bash
  mamba env export -n geo_env --no-builds > requirements.yml
  ```

* **Supprimer puis recréer l’environnement** :

  ```bash
  mamba remove -n geo_env --all
  mamba env create -f requirements.yml
  ```


## Liste des paquets et versions

Voici le description complète de l'environnement utilisé dans le projet (fichier `requirements.yml`, priorité **conda-forge** pour les libs géospatiales). 

````{dropdown} **Cliquez ici pour afficher / masquer la liste des paquets**
<br>

```yaml
name: geo_env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9.19
  - pip
  # Paquets lourds via conda (plus stable)
  - numpy
  - pandas
  - geopandas
  - shapely
  - fiona
  - rtree
  - pyproj
  - gdal
  - rasterio
  - matplotlib
  - scikit-learn
  - statsmodels
  - jupyter
  - ipykernel
  - seaborn
  - networkx
  - contextily
  - dask
  - xarray
  - rioxarray
  - pysal
  - libpysal
  - momepy
  - tobler
  - esda
  - giddy
  - segregation
  - spopt
  - spreg
  - spint
  - spglm
  - spaghetti
  - splot
  - mgwr
  - quantecon
  - pip:
      # Pip : paquets non ou mal gérés par conda
      - access==1.1.9
      - affine==2.4.0
      - alabaster==0.7.13
      - altair==5.1.2
      - anyio==4.2.0
      - appdirs==1.4.4
      - argon2-cffi==23.1.0
      - argon2-cffi-bindings==21.2.0
      - arrow==1.3.0
      - asgiref==3.7.2
      - asttokens==2.4.0
      - async-lru==2.0.4
      - attrs==23.1.0
      - Babel==2.14.0
      - backcall==0.2.0
      - beautifulsoup4==4.12.2
      - binaryornot==0.4.4
      - bleach==6.1.0
      - blinker==1.6.2
      - branca==0.6.0
      - Brotli==1.1.0
      - build==1.0.3
      - CacheControl==0.13.1
      - cachetools==5.3.1
      - cenpy==1.0.1
      - certifi==2023.7.22
      - cffi==1.16.0
      - chardet==5.2.0
      - charset-normalizer==3.3.0
      - click==8.1.7
      - click-plugins==1.1.1
      - cligj==0.7.2
      - cloudpickle==3.0.0
      - colorama==0.4.6
      - colorcet==3.0.1
      - comm==0.1.4
      - cookiecutter==2.5.0
      - cycler==0.12.1
      - datashader==0.16.0
      - deprecation==2.1.0
      - Django==4.2.7
      - docopt==0.6.2
      - docutils==0.20.1
      - folium==0.14.0
      - fuzzywuzzy==0.18.0
      - geographiclib==2.0
      - geopy==2.4.0
      - gitpython==3.1.37
      - import-ipynb==0.1.4
      - ipywidgets==7.8.1
      - jupyterlab==4.0.9
      - keplergl==0.3.2
      - mapclassify==2.6.1
      - mdit-py-plugins==0.4.0
      - mercantile==1.2.1
      - myst-nb==1.0.0
      - myst-parser==2.0.0
      - nkdv==0.0.6
      - notebook==7.0.6
      - osmnx==1.7.1
      - osmium==4.1.1
      - pillow==10.0.1
      - pipreqs==0.5.0
      - pipreqsnb==0.2.4
      - plotly==5.18.0
      - pointpats==2.4.0
      - pulp==2.7.0
      - py7zr==0.20.6
      - pyarrow==13.0.0
      - pydeck==0.8.1b0
      - pynkdv==0.0.21
      - pynsee==0.1.5
      - pyppmd==1.0.0
      - requests==2.31.0
      - rasterstats==0.19.0
      - rich==13.6.0
      - simplejson==3.19.2
      - streamlit==1.27.2
      - sympy==1.12
      - tabulate==0.9.0
      - texttable==1.7.0
      - tqdm==4.66.1
      - tzlocal==5.1
      - Unidecode==1.3.7
      - validators==0.22.0
      - watchdog==3.0.0
      - xlrd==2.0.1
      - xyzservices==2023.10.0
```

````


```{admonition} Conseil
:class: success

On pense à **activer `geo_env`** à chaque session pour bénéficier des bonnes versions de bibliothèques.

```


