# Choix de la fonction d’étalement spatial et calage du paramètre

## Objectif

Définir une **fonction d’étalement** autour des équipements urbains (pour la marche) et **calibrer son paramètre** à partir de la littérature et d’observations, de façon à reproduire l’histogramme empirique des distances/piétons.

## Notations

* $K(d)=e^{-\beta d}$ : noyau exponentiel (décroissant) en fonction de la distance-réseau $d$.
* $\beta$ (km$^{-1}$) : **taux de décroissance** (paramètre).
* $\lambda=\beta^\* = 1/\beta$ (km) : **distance caractéristique** (à laquelle le poids est divisé par $e$).
* $\varepsilon$ (m$^{-1}$) : même paramètre en mètres ($\varepsilon=\beta/1000$).
* $\gamma$ (miles$^{-1}$) : même paramètre en miles ($\gamma=\beta/1.609$).
* $\tau$ (min$^{-1}$) : paramètre temporel si l’on écrit $K(t)=e^{-\tau t}$ avec $t$ en minutes.
* $d_{\text{cutoff}}$ : portée maximale (au-delà, contribution nulle).

## Forme fonctionnelle : pourquoi l’exponentielle ?

Les études de marche montrent que la **propension décroît en continu** avec la distance; les fonctions exponentielles s’ajustent **mieux** que les lois en puissance ou gaussiennes pour les distances de marche (p. ex. Yang & Diez-Roux, 2012; Roper et al., 2023). En outre, l’exponentielle :

* respecte la logique gravitaire (effet de distance continu),
* évite les seuils arbitraires (400 m « tout ou rien »),
* est simple, robuste et lisible.

## Justification **mathématique** du cutoff à $3\lambda$ (≈ 95 %)

Soit le noyau non normalisé $K(d)=e^{-d/\lambda}$. La « masse » totale est $\int_{0}^{\infty} e^{-d/\lambda}\,dd=\lambda$.
La part **cumulative** contenue dans un rayon $R$ vaut :

$$
\frac{\int_{0}^{R} e^{-d/\lambda}\,dd}{\int_{0}^{\infty} e^{-d/\lambda}\,dd}
= \frac{\lambda\big(1-e^{-R/\lambda}\big)}{\lambda}
= 1-e^{-R/\lambda}.
$$

* Pour $R=3\lambda$ : $1-e^{-3}=0{,}9502 \approx 95\%$.
* Plus généralement, pour conserver une fraction $\alpha$ (p. ex. 0,95) :

$$
R_\alpha \;=\; -\,\lambda\ln(1-\alpha).
$$

Exemples utiles :

* $86{,}5\%$ à $R=2\lambda$,
* $95{,}0\%$ à $R\approx 3\lambda$,
* $98{,}2\%$ à $R\approx 4\lambda$,
* $99{,}3\%$ à $R\approx 5\lambda$.

> **Conclusion** : fixer $d_{\text{cutoff}}=3\lambda$ est **exactement** cohérent avec l’objectif de conserver \~95 % de l’influence pour un noyau exponentiel. (À noter : la règle « 3σ » est gaussienne; pour l’exponentielle, **3 $\lambda$** ⇒ 95 %.)

## Calage de $\beta$ (et $\lambda$) : recettes directes

Selon l’information empirique dont tu disposes, tu peux calibrer $\beta$ ainsi :

* **À partir de la médiane** $\tilde d$ (50 % des marches sous $\tilde d$) :

  $$
  \tilde d = \lambda\ln 2 \quad\Rightarrow\quad 
  \beta = \frac{\ln 2}{\tilde d}, \;\; \lambda=\frac{\tilde d}{\ln 2}.
  $$

* **À partir de la moyenne** $\bar d$ (pour l’exponentielle, $\bar d = \lambda$) :

  $$
  \beta=\frac{1}{\bar d}, \;\; \lambda=\bar d.
  $$

* **À partir d’un percentile** $d_p$ (ex. 95 %) :

  $$
  p=1-e^{-d_p/\lambda}\;\Rightarrow\; \lambda=\frac{d_p}{-\ln(1-p)},\quad
  \beta=\frac{-\ln(1-p)}{d_p}.
  $$

* **À partir d’un « rayon d’influence » souhaité** $d_{\text{cutoff}}$ couvrant $\alpha$ :

  $$
  \beta \;=\; \frac{-\ln(1-\alpha)}{d_{\text{cutoff}}}
  \quad (\alpha=0{,}95 \Rightarrow -\ln(0{,}05)\approx 2{,}996).
  $$

## Traduction **distance → temps** (et effet de circuité)

Si $d = c \cdot v \cdot t$, avec :

* $v$ la vitesse de marche (km/min, soit $v_{\text{km/h}}/60$),
* $c$ un **facteur de circuité** réseau/Euclide (souvent 1.2–1.4 en urbain dense),
  alors $K(t)=e^{-\tau t}$ avec

$$
\tau \;=\; \beta \, c \, v \quad\text{et}\quad 
t_{\text{cutoff}} \;=\; \frac{d_{\text{cutoff}}}{c\,v}.
$$

**Ordres de grandeur** (ex. $d_{\text{cutoff}}=0{,}75$ km) :

* $v=4{,}0$ km/h, $c=1{,}0$ ⇒ $t\simeq 11{,}3$ min.
* $v=3{,}5$ km/h, $c=1{,}2$ ⇒ $t\simeq 12{,}9$ min.
* $v=3{,}0$ km/h, $c=1{,}3$ ⇒ $t\simeq 15{,}4$ min.

> Donc **0,75 km** peut correspondre à **12–15 min** en tenant compte d’une vitesse modérée (3–3,5 km/h) **ou** d’une légère circuité ($c\approx1{,}2{-}1{,}3$).

## Paramétrage adopté (proposition)

Tu proposes de **resserrer** l’étalement pour mieux coller à tes observations (marche utilitaire de proximité) :

* **Distance caractéristique** : $\lambda=0{,}25$ km (**250 m**).
* **Paramètre** : $\beta=1/\lambda = 4$ km$^{-1}$ (soit $\varepsilon=0{,}004$ m$^{-1}$, $\gamma\approx 2{,}49$ miles$^{-1}$).
* **Cutoff** : $d_{\text{cutoff}}=3\lambda=0{,}75$ km ⇒ **95 %** de l’influence conservée.

**Lecture** : à chaque **250 m supplémentaires**, la contribution est divisée par $e$ (\~ 2,72). À **750 m**, il ne reste que \~5 % de l’influence (et on coupe proprement).

## Cohérence avec la littérature et nuances par motif

La littérature « tous motifs » (USA/Canada/France) suggère souvent $\lambda$ autour de **0,7–1,1 km** (donc $\beta\approx 0{,}9{-}1{,}4$ km$^{-1}$) pour la marche globale.
Ton choix **plus court** ($\lambda=0{,}25$ km) se justifie si l’on cible :

* des **usages de très grande proximité** (courses rapides, boulangerie, boîtes aux lettres, etc.),
* des **milieux très denses** où l’offre est abondante (donc choix plus proches),
* un **indicateur volontairement sélectif** (accent sur la proximité forte).

> Recommandation : **documenter** ce choix comme « paramètre par défaut pour la marche utilitaire de proximité » et prévoir un **jeu de paramètres par motif** (ex. travail/étude > loisirs > courses\&repas).

## Sensibilité minimale à rapporter

Pour transparence, reporte un mini-test :

* $\lambda=0{,}20$ km (cutoff 0,60 km) vs $\lambda=0{,}30$ km (cutoff 0,90 km),
* avec carte différentielle (% de variation du score).
  Cela montre la **stabilité** (ou non) de l’indicateur à ce calage.

---

## Encadré — formules pratiques (récap)

* **Couverture** à $R$ : $ \text{cov}(R)=1-e^{-R/\lambda}=1-e^{-\beta R}$.
* **Cutoff pour $\alpha$** (ex. 95 %) : $d_{\text{cutoff}} = -\lambda \ln(1-\alpha) \approx 3\lambda$.
* **Depuis la médiane** $\tilde d$ : $\beta=\ln 2 / \tilde d$.
* **Depuis la moyenne** $\bar d$ : $\beta=1/\bar d$.
* **Depuis un percentile $d_p$** : $\beta = -\ln(1-p)/d_p$.
* **Conversion en temps** : $\tau = \beta c v$, $t_{\text{cutoff}}=d_{\text{cutoff}}/(c v)$.

---

## Bibliographie (rappels de ta note)

\[1] Yang & Diez-Roux (2012) • \[2] Iacono et al. (2010) • \[3] Larsen et al. (2010) • \[4] Millward et al. (2013) • \[5] Arranz-López et al. (2021) • \[6] Roper et al. (2023) • \[7] MTE (2021) • \[8, 11] Zhao et al. (2015) • \[9] Hidalgo (2020) • \[10] Handy & Niemeier (1997).

