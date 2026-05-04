# Setup Git & GitHub — guide pas-à-pas

> Tu n'as **jamais utilisé Git** ou seulement un compte GitHub sans avoir
> rien installé en local ? Ce guide t'amène de zéro à ton premier
> `git push` en ~30 minutes. Pas de jargon, juste des étapes à suivre.
>
> *Ce fichier ne fait pas partie du dépôt — supprime-le après ton premier
> push pour garder le repo propre, ou bien laisse-le dans un dossier
> `notes/` privé si tu trouves utile d'y revenir.*

---

## ⚙️ Étape 1 — Installer Git sur ton ordinateur

### Windows

1. Télécharge le programme officiel : <https://git-scm.com/download/win>
2. Lance l'installeur. **Tu peux laisser TOUTES les options par défaut**
   sauf une : à l'écran *"Adjusting your PATH environment"*, sélectionne
   **"Git from the command line and also from 3rd-party software"**.
3. Pour vérifier que c'est bon, ouvre **PowerShell** (Win + R, tape
   `powershell`, Entrée) et tape :
   ```powershell
   git --version
   ```
   Tu dois voir quelque chose comme `git version 2.45.0.windows.1`.

### Linux (Ubuntu, Debian)

```bash
sudo apt update && sudo apt install git
git --version
```

### macOS

```bash
brew install git
git --version
```

---

## ⚙️ Étape 2 — Configurer Git (une seule fois, à vie)

Git a besoin de savoir qui tu es pour signer tes commits.

```bash
git config --global user.name "Basile-Vladimir Fauconnier"
git config --global user.email "bvfauconnier@gmail.com"
git config --global init.defaultBranch main
```

**Important** : utilise **le même email** que celui de ton compte GitHub,
sinon GitHub ne saura pas associer tes commits à ton profil.

---

## ⚙️ Étape 3 — Créer le dépôt sur GitHub (en privé)

1. Va sur <https://github.com> et connecte-toi avec ton compte
   `bvfauconnier`.
2. En haut à droite, clique sur **"+" → "New repository"**.
3. Remplis :
   - **Repository name** : `raman-plot-match-builder`
   - **Description** : *Desktop application for Raman spectroscopy
     preprocessing, peak fitting and mineral identification against the
     RRUFF database.*
   - **Visibility** : ✅ **Private** (tu pourras le rendre public plus
     tard avec un seul clic dans `Settings → General → Danger Zone →
     Change visibility`).
   - **❌ NE coche PAS** "Add a README", "Add .gitignore", "Add license"
     — on a déjà tout préparé en local, donc on ne veut pas que GitHub
     en crée des doublons.
4. Clique sur **"Create repository"**.
5. La page suivante affiche des instructions. **Garde cet onglet
   ouvert**, on va revenir dessus dans deux minutes.

---

## ⚙️ Étape 4 — Préparer le projet en local

Sur ton ordinateur, crée le dossier et copie tous les fichiers que je
t'ai préparés.

### Arborescence finale attendue

```
C:\Users\bvfau\Desktop\raman-plot-match-builder\        ← (par exemple)
├── .gitignore
├── LICENSE
├── README.md
├── README.fr.md
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── raman_gui.py
│   ├── raman_db.py
│   └── build_exe.py
├── docs/
│   ├── architecture.md
│   └── screenshots/
│       └── README.md
├── examples/
│   └── sample_spectra/
│       └── README.md
└── tests/
    └── README.md
```

> **Tu dois copier toi-même** :
>
> - `src/raman_gui.py` (la version finale livrée par Claude)
> - `src/raman_db.py` (depuis tes uploads)
> - `src/build_exe.py` (depuis tes uploads)
>
> Tout le reste (README, LICENSE, .gitignore, etc.) est généré dans le
> skeleton que je t'ai préparé.

---

## ⚙️ Étape 5 — Initialiser Git en local et lier au dépôt GitHub

Ouvre PowerShell (Windows) ou un terminal (Linux/macOS) **dans le dossier
du projet** :

```bash
cd C:\Users\bvfau\Desktop\raman-plot-match-builder
```

> Sur Windows, tu peux faire un clic droit dans l'Explorateur sur le
> dossier et choisir *"Open in Terminal"* ou *"Git Bash here"*.

### Initialise le dépôt local

```bash
git init
git branch -M main
```

### Vérifie ce que Git voit

```bash
git status
```

Tu dois voir une longue liste de fichiers en rouge, marqués
*"Untracked files"*. C'est normal, Git vient de découvrir ton projet.

### Premier commit

```bash
git add .
git status      # tout doit être en vert maintenant
git commit -m "Initial commit: Raman Plot|Match Builder v1.0.0"
```

### Lier au dépôt GitHub

Reviens sur l'onglet GitHub que tu as gardé ouvert. Tu y vois une URL
qui ressemble à :

```
https://github.com/bvfauconnier/raman-plot-match-builder.git
```

Copie-la et fais :

```bash
git remote add origin https://github.com/bvfauconnier/raman-plot-match-builder.git
git push -u origin main
```

GitHub te demandera de t'authentifier. **Important** : depuis 2021,
GitHub n'accepte plus le mot de passe classique. Tu dois utiliser un
**Personal Access Token (PAT)**.

---

## ⚙️ Étape 6 — Créer un Personal Access Token

1. Va sur <https://github.com/settings/tokens?type=beta>
2. Clique **"Generate new token"** → **"Fine-grained token"**.
3. Remplis :
   - **Token name** : `raman-plot-match-builder-local`
   - **Expiration** : 90 days (renouvelable)
   - **Resource owner** : ton compte
   - **Repository access** : *"Only select repositories"* →
     `raman-plot-match-builder`
   - **Permissions** :
     - **Contents** → *Read and Write*
     - **Metadata** → *Read* (auto-coché)
4. Clique **"Generate token"** et **copie immédiatement la chaîne**
   (tu ne pourras plus la voir après).
5. Quand `git push` te demande le mot de passe, **colle ce token** à la
   place du mot de passe.

> Sur Windows, Git va te proposer de *"Sign in with browser"* via Git
> Credential Manager — c'est plus simple, accepte. Tu te connectes sur
> ton navigateur, et tout est mémorisé pour les prochains push.

---

## ⚙️ Étape 7 — Créer la première release (`v1.0.0`)

Une fois que ton premier `git push` est passé :

```bash
git tag -a v1.0.0 -m "First public release"
git push --tags
```

Puis sur GitHub :

1. Page de ton dépôt → onglet **Releases** (à droite).
2. **"Draft a new release"**.
3. **"Choose a tag"** → sélectionne `v1.0.0`.
4. **Release title** : `v1.0.0 — First public release`
5. **Release notes** : copie-colle le contenu de la section
   `[1.0.0]` de ton `CHANGELOG.md`.
6. Si tu as construit l'`.exe` Windows, **fais-le glisser** dans la zone
   *"Attach binaries"*.
7. Clique **"Publish release"** (ou *"Save draft"* si tu veux le finir
   plus tard).

---

## ⚙️ Étape 8 — Workflow quotidien

Une fois tout ça fait, voici les 4 commandes que tu utiliseras 99 % du
temps :

```bash
# Voir ce qui a changé
git status

# Sauvegarder tes modifications avec un message clair
git add .
git commit -m "Fix: typo in user profile dialog"

# Envoyer sur GitHub
git push
```

Et si tu as bossé sur une autre machine et que tu veux récupérer :

```bash
git pull
```

---

## 🛟 Que faire si tu casses quelque chose

- **Tu veux annuler des modifications non commitées** :
  ```bash
  git checkout -- .
  ```

- **Tu veux annuler le dernier commit (mais garder les changements)** :
  ```bash
  git reset --soft HEAD~1
  ```

- **Tu veux complètement effacer ton dernier commit** (⚠ destructif) :
  ```bash
  git reset --hard HEAD~1
  ```

- **Quelque chose merde, tu paniques** : ne fais **rien**, copie-colle le
  message d'erreur dans une nouvelle conversation Claude — Git a presque
  toujours moyen de récupérer la situation tant que tu n'as pas tapé
  `git reset --hard`.

---

## 📚 Pour aller plus loin

- [Pro Git](https://git-scm.com/book/en/v2) — le livre de référence,
  gratuit en ligne
- [GitHub Skills](https://skills.github.com/) — petits tutos
  interactifs sur le site
- [Oh Shit, Git!?!](https://ohshitgit.com/) — solutions concrètes aux
  catastrophes Git courantes
