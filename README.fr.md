# Raman Plot|Match Builder

> Application de bureau pour la visualisation, le prétraitement, le fit des
> pics et l'identification automatique de spectres Raman par comparaison
> avec la base RRUFF — conçue pour la caractérisation minéralogique en
> astrobiologie et l'étude des analogues martiens.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Plateforme](https://img.shields.io/badge/plateforme-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Licence](https://img.shields.io/badge/licence-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Statut](https://img.shields.io/badge/statut-recherche-blueviolet)

🇬🇧 **An English version of this README is available**:
[README.md](README.md)

---

## ✨ Présentation

**Raman Plot|Match Builder** est une application graphique autonome qui
réunit deux modules complémentaires autour d'un workflow Raman unifié :

- **Plot Builder** — annoter les pics, superposer des références RRUFF, et
  exporter des rapports PDF prêts à publier.
- **Match Search** — prétraiter les spectres avec des algorithmes
  classiques (AsLS, Polynomial, SNIP) ou de deep learning (CDAE, CBRAE),
  fitter individuellement chaque pic avec un profil pseudo-Voigt, et
  identifier automatiquement les minéraux en scannant toute la base RRUFF
  avec un classement multi-critères basé sur le F1-score.

L'application a été développée dans le cadre d'une thèse de master sur la
**caractérisation minéralogique de gossans de l'Arctique canadien comme
analogues martiens**, et est mise à disposition pour assurer la
reproductibilité de l'analyse publiée.

---

## 📷 Captures d'écran

> *Captures à ajouter dans [`docs/screenshots/`](docs/screenshots/) — voir
> la section [Captures](#-captures) de ce README pour les vues recommandées.*

| Welcome — Fenêtre principale                  |
|-----------------------------------------------|
| ![Welcome — main view](https://github.com/bvfauconnier/raman-plot-match-builder/blob/e231d0346c794be9ff0a99a384b5ffe36020a642/docs/screenshots/rpmb_welcome.png) |

| Plot Builder — Fenêtre principale             |
|-----------------------------------------------|
| ![Welcome — main view](https://github.com/bvfauconnier/raman-plot-match-builder/blob/e231d0346c794be9ff0a99a384b5ffe36020a642/docs/screenshots/plot_builder_main.png) |

| Match Search — Fenêtre principale             |
|-----------------------------------------------|
| ![Welcome — main view](https://github.com/bvfauconnier/raman-plot-match-builder/blob/e231d0346c794be9ff0a99a384b5ffe36020a642/docs/screenshots/match_search_main.png) |

| Match Search — Fenêtre du Fit                 |
|-----------------------------------------------|
| ![Welcome — main view](https://github.com/bvfauconnier/raman-plot-match-builder/blob/e231d0346c794be9ff0a99a384b5ffe36020a642/docs/screenshots/match_search_fitwindow.png) |

| Résultats de l'identification AUTO            |
|-----------------------------------------------|
| ![Welcome — main view](https://github.com/bvfauconnier/raman-plot-match-builder/blob/e231d0346c794be9ff0a99a384b5ffe36020a642/docs/screenshots/auto_identify.png) |

| Rapport sous forme PDF                        |
|-----------------------------------------------|
| ![Welcome — main view](https://github.com/bvfauconnier/raman-plot-match-builder/blob/e231d0346c794be9ff0a99a384b5ffe36020a642/docs/screenshots/pdf_report.png) |

---

## 🚀 Démarrage rapide

### Installation depuis les sources

```bash
git clone https://github.com/bvfauconnier/raman-plot-match-builder.git
cd raman-plot-match-builder
python -m venv venv
# Windows : venv\Scripts\activate
# Linux/macOS : source venv/bin/activate
pip install -r requirements.txt
python src/raman_gui.py
```

### Exécutable autonome (Windows)

Un `.exe` pré-compilé sera attaché à chaque release taggée sur la page
**Releases** (lorsque le dépôt deviendra public).

Pour le construire toi-même :

```bash
pip install pyinstaller
python src/build_exe.py
```

Le binaire est généré dans `dist/`.

---

## 📁 Arborescence d'exécution requise

L'application attend les dossiers suivants **à côté de l'exécutable
ou de `raman_gui.py`** sur la machine de l'utilisateur. Ils sont créés
automatiquement au premier lancement s'ils manquent, *sauf `MODELS/`
et `DATABASE_RRUFF/`* qui contiennent des ressources que l'utilisateur
doit fournir lui-même.

```
<racine de l'application>/
├── raman_gui.py        (ou RamanPlotMatchBuilder.exe)
│
├── SAMPLES/                   ← spectres expérimentaux (Plot Builder)
│   └── <mon_échantillon>/
│       ├── spec0001.txt
│       └── ...
│
├── Raw_Spectrum/              ← spectres à prétraiter (Match Search)
│   └── <session_ou_sample>/
│       ├── spec0001.txt
│       └── ...
│
├── DATABASE_RRUFF/            ← base RRUFF de référence (à fournir)
│   ├── <Référence_dossier>/
│   │   ├── NomMinéral_Rxxxxxx.txt
│   │   └── ...
│   └── ...
│
├── MODELS/                    ← checkpoints deep-learning (à fournir)
│   ├── cdae_best.pth          ← modèle de débruitage CDAE
│   └── cbrae_best.pth         ← modèle de baseline CBRAE
│
├── PROJETS/                   ← projets sauvegardés (auto-créé)
│   ├── PlotBuilder/           ← fichiers .rpm
│   └── MatchSearch/           ← fichiers .rms
│
└── SAUVEGARDE/                ← exports (auto-créé à la 1ère sauvegarde)
    ├── Figures/               ← figures PNG / PDF / SVG
    ├── Save CSV/              ← exports Excel multi-onglets
    └── Rapports/              ← rapports PDF multi-pages
```

### À propos des dossiers `MODELS/` et `DATABASE_RRUFF/`

Pour des raisons de licence et de taille, **ni les checkpoints des
modèles entraînés ni la base RRUFF ne sont distribués avec ce dépôt**.
Tu dois te les procurer séparément :

- **`MODELS/cdae_best.pth` et `MODELS/cbrae_best.pth`** — ce sont les
  checkpoints PyTorch des modèles de débruitage / suppression de
  baseline entraînés sur des données Raman synthétiques et
  expérimentales. Ils seront publiés avec la thèse de master sur une
  archive publique (MatheO ou similaire — *lien à venir*). Sans eux,
  l'application fonctionne quand même mais les options de prétraitement
  CDAE / CBRAE sont désactivées. Les algorithmes classiques (AsLS,
  Polynomial, SNIP) restent pleinement fonctionnels.

- **`DATABASE_RRUFF/`** — télécharge le sous-ensemble "Excellent peaks"
  depuis [https://rruff.info/zipped_data_files/raman/](https://rruff.info/zipped_data_files/raman/), décompresse les.

### Format des fichiers de spectres

Tous les fichiers de spectres (dans `SAMPLES/`, `Raw_Spectrum/` et
`DATABASE_RRUFF/`) doivent être en ASCII 2 colonnes :

```
# Lignes de commentaires optionnelles commençant par '#'
100.0    1234.5
100.4    1242.1
...
```

- Colonne 1 — Raman shift en cm⁻¹
- Colonne 2 — Intensité (u.a.)
- Séparateur : espaces, tabulations ou virgules
- Les lignes commençant par `#` sont ignorées

---

## 🧭 Aperçu du workflow

```
   ┌─────────────────┐    ┌──────────────────┐    ┌───────────────────┐
   │ Spectres bruts  │ ─► │  Prétraitement   │ ─► │  Fit des pics     │
   │ (.txt 2-col)    │    │  (CDAE / CBRAE / │    │  (pseudo-Voigt)   │
   │                 │    │   AsLS / SNIP)   │    │                   │
   └─────────────────┘    └──────────────────┘    └─────────┬─────────┘
                                                            │
                          ┌─────────────────────────────────┘
                          ▼
                ┌──────────────────────┐    ┌──────────────────────────┐
                │  Analyse de match    │ ─► │  Identification auto     │
                │  (vs. 1 référence)   │    │  (base RRUFF complète)   │
                └──────────────────────┘    └──────────┬───────────────┘
                                                       ▼
                                            ┌──────────────────────┐
                                            │   Rapport PDF/Excel  │
                                            └──────────────────────┘
```

---

## 📂 Structure du projet (ce dépôt)

```
raman-plot-match-builder/
├── README.md                     ← (anglais)
├── README.fr.md                  ← tu es ici
├── LICENSE                       ← MIT
├── CHANGELOG.md                  ← historique des versions
├── AI_USAGE.md                   ← divulgation de l'usage d'IA
├── requirements.txt              ← dépendances Python
├── pyproject.toml                ← métadonnées du projet
├── .gitignore
├── src/
│   ├── raman_gui.py              ← application principale (~24 000 lignes)
│   ├── raman_db.py               ← base interne des modes minéralogiques
│   └── build_exe.py              ← script de build PyInstaller
├── docs/
│   ├── architecture.md           ← description haut niveau du code
│   └── screenshots/              ← captures d'écran pour les README
├── examples/
│   └── sample_spectra/           ← quelques spectres .txt d'exemple
└── tests/                        ← (placeholder pour les futurs tests)
```

> Note : les dossiers d'exécution (`SAMPLES/`, `MODELS/`,
> `DATABASE_RRUFF/`, `PROJETS/`, `SAUVEGARDE/`, `Raw_Spectrum/`) ne font
> **pas** partie de ce dépôt source. Ils sont créés ou attendus sur la
> machine de l'utilisateur à la racine de l'application (voir
> [Arborescence d'exécution requise](#-arborescence-dexécution-requise)
> ci-dessus).

---

## 🔬 Méthodologie

Le pipeline de fit et de matching est décrit en détail dans la thèse
associée (lien à venir). En résumé :

1. **Les spectres** sont chargés depuis des fichiers `.txt` à 2 colonnes
   (Raman shift en cm⁻¹, intensité en unités arbitraires).
2. **Le prétraitement** est entièrement traçable : chaque algorithme
   appliqué est inscrit dans l'historique de la courbe (ex.
   `[CDAE+CBRAE+AsLS]`).
3. **Le fit des pics** utilise des profils pseudo-Voigt avec une baseline
   linéaire optionnelle. Position, FWHM, aire et η (fraction
   gaussienne/lorentzienne) sont rapportés avec leurs incertitudes
   combinées (calibration ± 2 cm⁻¹, pas spectral, erreur statistique du
   fit).
4. **Le matching** calcule trois scores :
   - **M1** (couverture) = pics matchés / total des pics du spectre
   - **M2** (signature) = pics matchés / total des pics de la référence
   - **M3** (F1-score) = moyenne harmonique de M1 et M2
5. **L'identification auto** scanne toute la base RRUFF, optimise un
   offset par référence (dans ± 30 cm⁻¹), et classe les candidats par M3.

---

## 📷 Captures

Tu peux recréer les captures recommandées pour ce README de la manière
suivante :

| Nom de fichier                        | Ce qu'il faut capturer                                       |
|---------------------------------------|--------------------------------------------------------------|
| `plot_builder_main.png`               | Plot Builder avec 2–3 spectres et des pics annotés           |
| `match_search_main.png`               | Match Search avec 2–3 onglets ouverts                        |
| `match_search_fitwindow.png`          | Une fenêtre Fit montrant le fit + l'analyse de match         |
| `auto_identify.png`                   | Le dialog des résultats d'identification auto avec Top 10    |
| `pdf_report.png`                      | Une page d'un rapport PDF généré (page 2 ou 3)               |

Enregistre-les en PNG (1200–1600 px de large) dans
[`docs/screenshots/`](docs/screenshots/).

---

## 📜 Citation

Si tu utilises ce logiciel dans un travail académique, merci de citer à
la fois la release du logiciel et la thèse sous-jacente :

```bibtex
@software{fauconnier_raman_2026,
  author = {Fauconnier, Basile-Vladimir},
  title  = {Raman Plot{\textbar}Match Builder : un outil pour le
            prétraitement, le fit des pics et l'identification de spectres
            Raman par comparaison avec la base RRUFF},
  year   = {2026},
  version = {1.0.0},
  url    = {https://github.com/bvfauconnier/raman-plot-match-builder}
}

@mastersthesis{ARRIVE PROCHAINEMENT}
```

---

## 📄 Licence

Ce projet est publié sous la **licence MIT** — voir [LICENSE](LICENSE).
Tu es libre d'utiliser, modifier et redistribuer le code, y compris à des
fins commerciales, à condition de conserver la mention de copyright.

La base de données spectrale RRUFF **n'est pas distribuée** avec ce
logiciel et reste la propriété de ses contributeurs respectifs et du
projet RRUFF ([https://rruff.info](https://rruff.info)).

---

## 🤖 Divulgation de l'usage d'IA

Ce logiciel a été développé avec l'assistance de **Claude d'Anthropic
(Opus 4.7)** comme outil d'accélération du codage (échafaudage de l'UI,
traduction FR/EN, refactoring, débogage). Toutes les décisions
scientifiques, les choix méthodologiques, l'analyse des données et
l'interprétation des résultats sont l'œuvre exclusive de l'auteur.
Voir [`AI_USAGE.md`](AI_USAGE.md) pour la divulgation complète.

---

## 👤 Auteur

**Ir. Basile-Vladimir Fauconnier**
 - Bio Ingénieur en Sciences et Technologie de l'Environnement de l'Agro-Bio Tech de Gembloux ULiège 
 - Master en Sciences Spatiales — Université de Liège (ULiège)
 - Mémoire de master en Astrobiologie — Université de Sherbrooke (UdeS)

📧 [bvfauconnier@gmail.com](mailto:bvfauconnier@gmail.com)
🐙 [github.com/bvfauconnier](https://github.com/bvfauconnier)

---

## 🙏 Remerciements

- **Projet RRUFF** — pour la base ouverte de spectres Raman de référence
  ([rruff.info](https://rruff.info))
- **Université de Liège** — Département d'Astrophysique, de Géophysique et d'Océanographie
- **Université de Sherbrooke** — Département de Géomatiques Appliquées — Équipe T-Mars
- **Promoteur** — Pr. Myriam Lemelin (UdeS) — Département de Géomatiques Appliquées — Équipe T-Mars
- **Co-Promoteur** — Pr. Bernard Charlier (ULiège) — Département de Géologie

---

## 🛠 Contribuer

Il s'agit d'une release de recherche associée à une thèse spécifique. Les
**issues et pull requests sont les bienvenues**, mais la priorité de
fusion est donnée aux corrections de bugs liés à la reproductibilité des
résultats publiés. Pour des features ou changements de design plus
importants, ouvre d'abord une discussion.
