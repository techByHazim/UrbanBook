# Environnement scientifique

- Python / Conda : voir `requirements.yml` à la racine.
- QGIS : version utilisée (indiquer).
- Exécution des notebooks : **locale avec sorties sauvegardées**.
- Côté site : `execute_notebooks: "off"` dans `_config.yml`.

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


# **Création et utilisation de l’environnement virtuel**

En complément de la section précédente, je vais vous montrer comment créer et utiliser mon environnement virtuel **`geo_env`** sur **Windows**, **macOS** et **Linux**.

````{admonition} Pourquoi un environnement virtuel ?
:class: important

Un environnement virtuel permet d'isoler les dépendances d'un projet des autres projets et de l'environnement système. Cela garantit que les bibliothèques utilisées par un projet ne perturbent pas celles d'un autre projet.

````
---

## **Outils de gestion d'environnement**

* **conda** (gestionnaire d’environnements et de paquets)
* **mamba** (alternative à conda, **beaucoup plus rapide**). Si `mamba` n’est pas disponible, on peut **tout** faire avec `conda` en remplaçant `mamba` par `conda` dans les commandes.

---

## **Installation de conda/mamba**

````{admonition} Étapes nécessaires
:class: important

1. **Installer Miniforge/Mambaforge** (recommandé) ou Miniconda.  
   - **macOS Apple Silicon (M1/M2/M3)** : installeur **ARM64**  
   - **macOS Intel** : installeur **x86_64**  
   - **Windows** : installeur **x86_64**

2. **Où taper les commandes ?**  
   - **Windows** : *Anaconda Prompt*, *Miniforge Prompt* ou *PowerShell* (après `conda init`)  
   - **macOS / Linux** : application **Terminal**

3. **Initialiser conda** (macOS/Linux, une seule fois) :

   ```bash
   conda init zsh    # si vous utilisez zsh (par défaut sur macOS récents)
   conda init bash   # sinon
   ```

   Fermez et **rouvrez** le terminal.

4. **Installer mamba** (si absent) :

   ```bash
   conda install -n base -c conda-forge mamba
   ```

5. **Placer** le fichier **`requirements.yml`** à la **racine du projet**.

````

````{admonition} Bonnes pratiques conda-forge
:class: tip

Utilisez **conda-forge** en priorité (meilleure compatibilité des libs géospatiales) :

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

````

---

## **Création de l’environnement**

Ouvrir un terminal et se placer dans le **dossier racine** du projet (là où se trouve `requirements.yml`).

```bash
mamba env create -f requirements.yml
```

Cela crée un environnement nommé **`geo_env`** avec toutes les dépendances (conda + pip) définies dans le fichier.

````{admonition} Mettre à jour un environnement existant
:class: tip

```bash
mamba env update -n geo_env -f requirements.yml --prune
```

````

L’option `--prune` désinstalle ce qui n’est plus listé.

## **Activer / désactiver l’environnement**

* **Activer** :

```bash
mamba activate geo_env   # ou: conda activate geo_env
```

* **Désactiver** :

```bash
mamba deactivate         # ou: conda deactivate
```

* **Vérifier** l’environnement actif :

```bash
conda info --envs # ou: conda env list
```

**C’est identique sur Windows, macOS et Linux** une fois conda/mamba correctement installés.

---

## **Ajouter le noyau Jupyter**

Pour pouvoir choisir `geo_env` et utiliser cet environnement dans **Jupyter Notebook/Lab** :

```bash
python -m ipykernel install --user --name geo_env --display-name "Python (geo_env)"
```

Ensuite, dans Jupyter, sélectionnez le noyau **Python (geo_env)**.

---

## **Mettre à jour / ajouter des paquets**

* Ajouter un paquet **conda** (ex. `geopy`) :

  ```bash
  mamba install -n geo_env geopy -c conda-forge
  ```

* Ajouter un paquet **pip** ponctuellement :

  ```bash
  python -m pip install <nom-du-paquet>
  ```

* Répercuter ces changements dans le fichier :

  ```bash
  mamba env export -n geo_env --no-builds > requirements.yml
  ```

---

## **Réparer ou recréer l’environnement (au besoin)**

* **Lister** les environnements :

  ```bash
  conda info --envs
  ```

* **Supprimer** puis **recréer** :

  ```bash
  mamba remove -n geo_env --all
  mamba env create -f requirements.yml
  ```

---

## **Liste des paquets et versions**

Le fichier `requirements.yml` décrit l’environnement complet du projet (priorité **conda-forge** pour les libs géospatiales). Il est disponible à la **racine** du dépôt.

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

---

```{admonition} Conseil
:class: success

On pense à **activer `geo_env`** à chaque session pour bénéficier des bonnes versions de bibliothèques.

```


