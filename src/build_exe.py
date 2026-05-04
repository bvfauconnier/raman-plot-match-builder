#!/usr/bin/env python3
"""
Build PyInstaller — Raman Plot|Match Builder

Script Python multiplateforme pour générer l'exécutable.
Fonctionne sur Windows, Linux et macOS.

Usage :
    python build_exe.py

Pré-requis (à installer une fois) :
    pip install customtkinter pyinstaller numpy scipy matplotlib
    pip install pillow openpyxl reportlab
    pip install tkinterdnd2     (optionnel : drag & drop)
    pip install torch           (optionnel : CDAE/CBRAE)

Sortie :
    dist/RamanPlotMatchBuilder/RamanPlotMatchBuilder(.exe)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


# ============================================================
# Configuration du build
# ============================================================
APP_NAME = "RamanPlotMatchBuilder"
ENTRY_POINT = "raman_gui.py"
REQUIRED_FILES = ["raman_gui.py", "raman_db.py"]
ICON_FILE = "Raman_GUI.ico"  # optionnel

# Fichiers/dossiers de données à embarquer
ADD_DATA = [
    ("raman_db.py", "."),
]

# Packages dont on doit collecter les données (themes, fonts, ressources)
COLLECT_DATA = [
    "customtkinter",
    "tkinterdnd2",
]

# Modules à importer explicitement (chargés dynamiquement, non détectés par
# l'analyse statique de PyInstaller)
HIDDEN_IMPORTS = [
    "customtkinter",
    "tkinterdnd2",
    "scipy.signal",
    "scipy.optimize",
    "scipy.interpolate",
    "scipy.sparse",
    "scipy.sparse.linalg",
    "matplotlib.backends.backend_tkagg",
    "matplotlib.backends.backend_agg",
    "PIL._tkinter_finder",
    "openpyxl",
    "reportlab",
    "reportlab.pdfgen",
    "reportlab.lib",
    "reportlab.platypus",
]

# Modules à exclure pour réduire la taille (jamais utilisés à runtime)
EXCLUDE_MODULES = [
    "pytest",
    "IPython",
    "jupyter",
    "notebook",
    "pylint",
    "sphinx",
]


# ============================================================
# Fonctions utilitaires
# ============================================================
# Codes ANSI pour la couleur (fonctionnent sur Linux/macOS et Windows 10+)
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"


def cprint(msg, color=""):
    """Print avec couleur (fallback gracieux si terminal sans couleur)."""
    print(f"{color}{msg}{Color.RESET}")


def section(title):
    """Affiche un titre de section bien visible."""
    bar = "=" * 60
    cprint(f"\n{bar}", Color.CYAN)
    cprint(f"  {title}", Color.BOLD + Color.CYAN)
    cprint(bar, Color.CYAN)


def check_prerequisites():
    """Vérifie que les fichiers requis et PyInstaller sont disponibles."""
    section("Vérification des prérequis")

    # 1. Fichiers source obligatoires
    missing = [f for f in REQUIRED_FILES if not Path(f).is_file()]
    if missing:
        cprint(f"✕ ERREUR : fichier(s) manquant(s) : {', '.join(missing)}",
               Color.RED)
        cprint("  Lance ce script depuis le dossier qui contient "
               f"{', '.join(REQUIRED_FILES)}", Color.RED)
        return False
    cprint(f"✓ Fichiers source présents : {', '.join(REQUIRED_FILES)}",
           Color.GREEN)

    # 2. Icône (optionnelle)
    if Path(ICON_FILE).is_file():
        cprint(f"✓ Icône détectée : {ICON_FILE}", Color.GREEN)
    else:
        cprint(f"ℹ Icône {ICON_FILE} introuvable — exe sans icône custom.",
               Color.YELLOW)

    # 3. PyInstaller installé ?
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            cprint(f"✓ PyInstaller installé (version {version})",
                   Color.GREEN)
        else:
            raise FileNotFoundError("PyInstaller non disponible")
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        cprint("✕ ERREUR : PyInstaller n'est pas installé.", Color.RED)
        cprint("  Installe-le avec : pip install pyinstaller", Color.RED)
        return False

    return True


def cleanup_old_builds():
    """Supprime les anciens dossiers build/ et dist/."""
    section("Nettoyage des anciens builds")
    for folder in ["build", "dist"]:
        path = Path(folder)
        if path.exists():
            cprint(f"  Suppression de {folder}/...", Color.YELLOW)
            shutil.rmtree(path)
    cprint("✓ Nettoyage terminé", Color.GREEN)


def build_pyinstaller_command():
    """Construit la liste d'arguments pour PyInstaller."""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",       # produit un dossier (plus rapide à lancer
                            # qu'onefile) ; tu peux passer à --onefile
                            # si tu veux un exe unique mais lent
        "--windowed",     # pas de console (Tk app)
        "--name", APP_NAME,
    ]

    # Icône
    if Path(ICON_FILE).is_file():
        cmd += ["--icon", ICON_FILE]

    # Datas embarquées : sur Windows le séparateur est ';',
    # sur Linux/macOS c'est ':'
    sep = ";" if sys.platform == "win32" else ":"
    for src, dst in ADD_DATA:
        cmd += ["--add-data", f"{src}{sep}{dst}"]

    # Collect datas des packages (themes, fonts, etc.)
    for pkg in COLLECT_DATA:
        cmd += ["--collect-data", pkg]

    # Hidden imports
    for mod in HIDDEN_IMPORTS:
        cmd += ["--hidden-import", mod]

    # Excludes
    for mod in EXCLUDE_MODULES:
        cmd += ["--exclude-module", mod]

    # Point d'entrée
    cmd.append(ENTRY_POINT)
    return cmd


def run_build():
    """Lance PyInstaller et affiche sa sortie en temps réel."""
    section("Lancement de PyInstaller (~3-10 minutes)")
    cmd = build_pyinstaller_command()

    # Affichage de la commande pour debug
    cprint("Commande exécutée :", Color.CYAN)
    cprint("  " + " ".join(cmd) + "\n")

    try:
        # On laisse PyInstaller écrire directement dans le terminal
        # pour voir la progression en temps réel
        result = subprocess.run(cmd)
        return result.returncode == 0
    except KeyboardInterrupt:
        cprint("\n✕ Build interrompu par l'utilisateur.", Color.RED)
        return False
    except Exception as e:
        cprint(f"\n✕ Erreur pendant le build : {e}", Color.RED)
        return False


def verify_output():
    """Vérifie que l'exe a bien été produit et affiche son emplacement."""
    section("Vérification du résultat")

    # Chemin de l'exe selon la plateforme
    exe_name = f"{APP_NAME}.exe" if sys.platform == "win32" else APP_NAME
    exe_path = Path("dist") / APP_NAME / exe_name

    if exe_path.is_file():
        # Calculer la taille du dossier dist/<APP_NAME>/
        dist_folder = Path("dist") / APP_NAME
        total_size = sum(f.stat().st_size for f in dist_folder.rglob("*")
                            if f.is_file())
        size_mb = total_size / (1024 * 1024)

        cprint(f"✓ BUILD RÉUSSI", Color.BOLD + Color.GREEN)
        cprint(f"\nExécutable : {exe_path}", Color.GREEN)
        cprint(f"Taille totale du dossier : {size_mb:.1f} MB", Color.GREEN)
        cprint(f"\nPour distribuer : zip tout le dossier {dist_folder}/",
               Color.CYAN)
        cprint(f"Pour tester localement : lance {exe_path}", Color.CYAN)
        return True
    else:
        cprint(f"✕ BUILD ÉCHOUÉ", Color.BOLD + Color.RED)
        cprint(f"Fichier attendu introuvable : {exe_path}", Color.RED)
        cprint("Vérifie les messages d'erreur de PyInstaller ci-dessus.",
               Color.RED)
        return False


# ============================================================
# Main
# ============================================================
def main():
    # Activer la couleur sur Windows 10+ (sinon les codes ANSI s'affichent
    # comme du texte brut)
    if sys.platform == "win32":
        try:
            os.system("")  # active le mode VT100 dans le terminal Windows
        except Exception:
            pass

    cprint("\n" + "=" * 60, Color.CYAN)
    cprint(f"  Raman Plot|Match Builder — build PyInstaller",
           Color.BOLD + Color.CYAN)
    cprint("=" * 60, Color.CYAN)

    # 1. Vérifier les prérequis
    if not check_prerequisites():
        sys.exit(1)

    # 2. Nettoyer les anciens builds
    cleanup_old_builds()

    # 3. Lancer le build
    if not run_build():
        cprint("\n✕ Le build PyInstaller a échoué.", Color.RED)
        sys.exit(1)

    # 4. Vérifier le résultat
    if not verify_output():
        sys.exit(1)

    cprint("\n✓ Tout est OK ! 🎯\n", Color.BOLD + Color.GREEN)


if __name__ == "__main__":
    main()
