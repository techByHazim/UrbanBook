# Installation

## Environnement Python

Pour travailler en dehors de QGIS, j’ai crée un **environnement virtuel** à ce projet.
Il est défini dans le fichier `requirements.yml`, que je garde dans le dossier `envs/` à la racine du projet.
Ce fichier contient toutes les bibliothèques utilisées, avec leurs versions, pour m’assurer que le projet reste stable et reproductible sur n’importe quelle machine.

```{admonition} Important
:class: important
Un environnement virtuel permet d’isoler les dépendances d’un projet de celles des autres projets ou du système. Ainsi, deux projets peuvent utiliser des versions différentes d’une même bibliothèque sans conflit. (*[Python Documentation - Virtual Environments](https://docs.python.org/3/tutorial/venv.html)*)
```

## Outils de gestion d’environnement

Plusieurs gestionnaires d’environnement existent :  

- **[Venv](https://docs.python.org/3/library/venv.html)** : outil natif de Python, simple et léger pour créer des environnements virtuels. (*Python Software Foundation, [Python 3 Documentation - venv](https://docs.python.org/3/library/venv.html)*) 

- **[Conda](https://docs.conda.io/projects/conda/en/latest/index.html)** : Gestionnaire d’environnements et de paquets multiplateforme. (*Anaconda, Inc., [Conda Documentation](https://docs.conda.io/projects/conda/en/latest/index.html)*)  

- **[Mamba](https://mamba.readthedocs.io/en/latest/)** : Alternative à Conda, compatible mais beaucoup plus rapide grâce à son moteur en C++. (*Mamba Developers, [Mamba Documentation](https://mamba.readthedocs.io/en/latest/)*)  

- **[Poetry](https://python-poetry.org/docs/)** : Gestionnaire moderne de dépendances et d’emballage (packaging) pour Python. (*Python Poetry Project, [Poetry Documentation](https://python-poetry.org/docs/)*)  

- **[Pipenv](https://pipenv.pypa.io/en/latest/)** : Outil de gestion combinant `pip` et `virtualenv`, historiquement populaire mais moins utilisé aujourd’hui. (*Python Packaging Authority (PyPA), [Pipenv Documentation](https://pipenv.pypa.io/en/latest/)*)  

- **[Docker](https://docs.docker.com/)** : Solution plus lourde, basée sur des conteneurs, garantissant une portabilité et une reproductibilité complètes. (*Docker, Inc., [Docker Documentation](https://docs.docker.com/)*) 


## Recommandation 

Dans ce projet, j’utilise et recommande fortement **Conda** (ou son alternative optimisée **Mamba**) comme solution de gestion d’environnements virtuels. C'est le plus adapté pour installer et gérer parfaitement les bibliothèques géospatiales (*GDAL*, *PROJ*, *Rasterio*, *Fiona*, *Shapely*, *GeoPandas*) qui reposent sur des dépendances systèmes compliqués (bibliothèques C/C++) à compiler avec `pip` seul.

Ma recommandation s'appui sur plusieurs documentations :

- Dans la docs de **GeoPandas**, ils précisent :  
  > “To install GeoPandas and all its dependencies, we recommend to use the conda package manager.” *[GeoPandas Documentation - Installation](https://geopandas.org/en/stable/getting_started/install.html)*  

- Dans la docs **Rasterio**, on souligne :  
  > “Many users find Anaconda and conda-forge a good way to install Rasterio and get access to more optional format drivers (like TileDB and others).” *[Rasterio Documentation - Installation](https://rasterio.readthedocs.io/en/latest/installation.html)*  

- Tout de meme pour **Fiona** :  
  > “Many users find Anaconda and conda-forge a good way to install Fiona and get access to more optional format drivers (like GML).” *[Fiona Documentation - Installation](https://fiona.readthedocs.io/en/latest/README.html#installation)*  


```{admonition} Pour aller plus loin
:class: note
Consultez le guide *"Comparing Python environment management tools"* (Real Python, 2024) :  
[https://realpython.com/python-virtual-environments-a-primer/](https://realpython.com/python-virtual-environments-a-primer/)
```

## Installation de Conda via Anaconda

### Pourquoi Anaconda ?
**Anaconda** est une distribution complète de Python qui inclut déjà **Conda**, le gestionnaire d’environnements et de paquets que j'utilise. C’est la méthode la plus simple et la plus fiable pour débuter, car elle installe directement les outils scientifiques essentiels (*NumPy*, *Pandas*, *Matplotlib*, etc.) et gère automatiquement les dépendances.


### Étapes d’installation

1. **Télécharger Anaconda** depuis le site officiel :  
    [https://www.anaconda.com/download](https://www.anaconda.com/download)

   Choisissez la version correspondant à votre système d’exploitation :
   - **Windows** (64 bits)  
   - **macOS Intel ou Apple Silicon (M1/M2/M3)**  
   - **Linux**

2. **Lancer l’installateur** et suivre les instructions par défaut.  
   - Acceptez les options proposées (notamment *“Add Anaconda to PATH”* si vous y êtes invité).  
   - À la fin, démarrer/redémarrez votre terminal.

3. **Vérifier l’installation :**
   ```bash
   conda --version
   ```
   Si tout fonctionne, vous verrez s’afficher une version comme :
   ```
   conda 25.5.1 # c'est ma version mais ça peut etre une autre.
   ```


### (Optionnel) Installer Mamba
**Mamba** est une version plus rapide de Conda, compatible à 100 %.  
Vous pouvez l’installer ultérieurement si vous le souhaitez :

```bash
conda install -n base -c conda-forge mamba
```

### Pour aller plus loin
- Documentation officielle : [Conda User Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html)  
- Installation Anaconda : [Anaconda Documentation - Installing Anaconda](https://docs.anaconda.com/anaconda/install/)  
- Mamba (optionnel) : [Mamba Documentation](https://mamba.readthedocs.io/en/latest/)


```{admonition} Astuce
Plus besoin de télécharger quoi que ce soit d’autre : **Anaconda installe déjà Conda**.
```

## Création et gestion de l’environnement Conda

Une fois **Anaconda** installé, voici comment créer un environnement virtuel avec `conda`.

### Créer l’environnement à partir du fichier `requirements.yml`

Ouvrez votre terminal (MacOS, Linux) ou Anaconda Prompt (Windows) et placer vous dans le dossier `envs/` du projet (là où se trouve un fichier nommé `requirements.yml`) et exécutez :

```bash
conda env create -f requirements.yml
```

Cela crée automatiquement un environnement nommé **`geo_env`** contenant toutes les bibliothèques utilisées dans ce projet.

> *Remarque :* vous pouvez remplacer `conda` par `mamba` si celui-ci est installé. C’est plus rapide et 100 % compatible.

### Activer l’environnement

```bash
conda activate geo_env
```

Dès lors, toutes les commandes Python, Jupyter ou pip utiliseront les bibliothèques de cet environnement.

### Utiliser l’environnement dans Jupyter

Pour exécuter les notebooks avec cet environnement, ajoutez-le à Jupyter :

```bash
python -m ipykernel install --user --name geo_env --display-name "Python (geo_env)"
```

Vous pourrez ensuite le sélectionner dans le menu (**Kernel - Change kernel**) de JupyterLab ou Jupyter Notebook.

### Mettre à jour ou réparer l’environnement

Si le fichier `requirements.yml` change (nouveaux paquets, mises à jour) :

```bash
conda env update -n geo_env -f requirements.yml --prune
```

- `--prune` supprime les dépendances devenues inutiles.  
- En cas de problème majeur, on peut supprimer puis recréer l’environnement :  
  ```bash
  conda remove -n geo_env --all
  conda env create -f requirements.yml
  ```

### Commandes utiles au quotidien

| Action | Commande |
|:--|:--|
| Activer l’environnement | `conda activate geo_env` |
| Désactiver l’environnement | `conda deactivate` |
| Lister les environnements disponibles | `conda env list` |
| Ajouter un paquet | `conda install -n geo_env <nom-du-paquet> -c conda-forge` |
| Exporter les changements | `conda env export -n geo_env --no-builds > requirements.yml` |

### Référence utile
Pour approfondir la gestion d’environnements Conda :  
[Gérer son environnement avec Conda - Université Grenoble Alpes](https://gricad-doc.univ-grenoble-alpes.fr/hpc/softenv/conda/#:~:text=Conda%20est%20un%20syst%C3%A8me%20de,environnements%20sur%20votre%20ordinateur%20local.)

### Liste des paquets utilisés dans le projet

Ci-dessous le contenu du fichier `requirements.yml`.

````{dropdown} **Cliquez ic pour Afficher / Masquer requirements.yml**
```yaml
name: geo_env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pip
  - numpy
  - pandas
  - geopandas
  - shapely
  - fiona
  - pyproj
  - openpyxl
  - rtree
  - gdal
  - rasterio
  - scikit-learn
  - statsmodels
  - jupyter
  - jupyterlab
  - ipykernel
  - tqdm
  - matplotlib
  - seaborn
  - contextily
  - networkx
  - momepy
  - tobler
  - esda
  - splot
  - libpysal
  - pysal
  - dask
  - xarray
  - rioxarray
  - pip:
      - osmium==4.1.1
      - osmnx==1.7.1
      - folium==0.14.0
      - rasterstats==0.19.0
      - keplergl==0.3.2
      - myst-nb==1.0.0
      - myst-parser==2.0.0
      - jupyter-book
      - sphinxcontrib-mermaid==1.0.0
```
````

```{admonition} Conseil
:class: success

Pensez à **activer `geo_env`** à chaque session pour pouvoir bénéficier des bonnes versions de bibliothèques.

```


