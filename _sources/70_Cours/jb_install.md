# Déploiement d’un Jupyter Book avec GitHub Pages

## Préparer le projet

* J'ai mon dossier **UrbanBook** avec :

  * fichiers `.md` (notes) et `.ipynb` (notebooks avec sorties exécutées)
  * fichiers de config : `_config.yml`, `_toc.yml`
  * un dossier `images/` pour les logos et illustrations
* J'ajouter un fichier `.gitignore` pour exclure `_build/`, `__pycache__/`, etc.

## Initialiser GitHub

* Je crée un repo sur GitHub → **UrbanBook** (public pour que le site soit visible).
* Je lis mon projet local :

  ```bash
  git init
  git remote add origin https://github.com/techByHazim/UrbanBook.git
  git branch -M main
  git push --set-upstream origin main
  ```

## Configurer Jupyter Book

Dans `_config.yml` :

```yaml
title: Proximité urbaine
author: Hazim Moindze
logo: images/carte.png
language: fr

execute:
  execute_notebooks: "off"   # GitHub n’exécute pas mon code
```

Les notebooks doivent être **exécutés localement** et sauvegardés avec leurs sorties.

## Ajouter le workflow GitHub Actions

Dans `.github/workflows/deploy-book.yml` :

```yaml
name: Deploy Jupyter Book

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install Jupyter Book
      run: pip install jupyter-book ghp-import
    - name: Build the book
      run: jupyter-book build .
    - name: Deploy to GitHub Pages
      run: ghp-import -n -p -f _build/html
```

## Activer GitHub Pages

* Aller dans **Settings > Pages**
* Choisir :

  * **Source** → `Deploy from a branch`
  * **Branch** → `gh-pages`
* Le site sera disponible à :

  ```
  https://techByHazim.github.io/UrbanBook/
  ```
  
## Routine de travail

1. Je modifie mes `.md` ou `.ipynb` localement.
2. J'exécutes mes notebooks localement (pour avoir les sorties).
3. Je sauvegarde et pushe :

   ```bash
   git add .
   git commit -m "Mise à jour"
   git push
   ```
4. GitHub Actions rebuild et publie le site automatiquement 


Résultat :

* Je travaille **localement** (avec mes bibliothèques installées).
* GitHub ne fait que **mettre en ligne** ce que j'ai produit → pas d’erreurs pandas/numpy.
* Chaque `git push` = nouvelle version du site.


Pour supprimer un dossier suivi par Git

```bash
   ggit rm -r --cached .history
   ```

  