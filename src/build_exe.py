"""
================================================================================
  Raman Plot|Match Builder — PyInstaller build script
================================================================================

Cross-platform build helper for packaging the application into a standalone
executable bundle (Windows .exe, Linux ELF, macOS .app).

Usage
-----
1. Install PyInstaller in your Python environment:
       pip install pyinstaller

2. Place this file next to `raman_gui.py` (i.e. inside the `src/` folder of
   the GitHub repository, or at the application root for development).

3. From that folder, run:
       python build_exe.py

The bundled application is produced under `dist/RamanPlotMatchBuilder/`,
together with the runtime folders (`SAMPLES/`, `MODELS/`, `DATABASE_RRUFF/`,
`PROJETS/`, `SAUVEGARDE/`, `Raw_Spectrum/`) — each containing a bilingual
`README.txt` that tells the end-user what to put inside.

NOTE on the deep-learning models and the RRUFF database
-------------------------------------------------------
The trained PyTorch checkpoints (`MODELS/cdae_best.pth`, `MODELS/cbrae_best.pth`)
and the RRUFF reference database are NOT bundled by this script:
  - the model checkpoints are large and have a separate distribution archive
    (Zenodo — link in the thesis);
  - the RRUFF database is licensed CC-BY by the RRUFF Project and must be
    downloaded by the end-user from https://rruff.info.
The corresponding folders (`MODELS/` and `DATABASE_RRUFF/`) are nevertheless
created empty, with a README explaining where to obtain the assets.
================================================================================
"""
from __future__ import annotations

import os
import sys
import shutil
import subprocess
from pathlib import Path

# ----------------------------------------------------------------------------
# Configuration — edit these constants if you rename files or move things
# ----------------------------------------------------------------------------
HERE       = Path(__file__).parent
APP_NAME   = "RamanPlotMatchBuilder"
APP_VERSION = "1.0.0"
MAIN_FILE  = HERE / "raman_gui.py"          # main entry point
ICON_FILE  = HERE / "Raman_GUI.ico"         # optional; ignored if missing

# Files that must be bundled INSIDE the .exe (read-only at runtime).
# Format: (source path relative to HERE, destination relative to bundle root)
BUNDLED_DATA: list[tuple[str, str]] = [
    ("raman_db.py",   "."),
    ("Raman_GUI.ico", "."),    # ignored if file does not exist
]

# Folders that must be created NEXT TO the .exe (writable at runtime).
# Each gets a small README.txt explaining its purpose to the end user.
RUNTIME_DIRS: list[str] = [
    "SAMPLES",
    "Raw_Spectrum",
    "DATABASE_RRUFF",
    "MODELS",
    "PROJETS",
    "PROJETS/PlotBuilder",
    "PROJETS/MatchSearch",
    "SAUVEGARDE",
    "SAUVEGARDE/Figures",
    "SAUVEGARDE/Save CSV",
    "SAUVEGARDE/Rapports",
]

# Bilingual READMEs (FR + EN) for each top-level runtime folder.
# Sub-folders of PROJETS/ and SAUVEGARDE/ are auto-populated and don't need
# their own README — the parent's README explains the role of the children.
RUNTIME_READMES: dict[str, str] = {

    # ------------------------------------------------------------------------
    "SAMPLES": """\
# SAMPLES/

🇫🇷  Place ici les spectres expérimentaux que tu veux ouvrir avec
    « Plot Builder ». Organise-les en sous-dossiers par échantillon :

        SAMPLES/
        ├── CR-G3-05/
        │   ├── spec0001.txt
        │   ├── spec0002.txt
        │   └── ...
        └── CR-G3-03/
            └── ...

    Chaque fichier .txt doit avoir 2 colonnes :
      • colonne 1 : Raman shift (cm⁻¹)
      • colonne 2 : intensité (u.a.)
    Les lignes commençant par '#' sont ignorées.

🇬🇧  Drop here the experimental spectra you want to open with
    “Plot Builder”. Organize them in subfolders, one per sample:

        SAMPLES/
        ├── CR-G3-05/
        │   ├── spec0001.txt
        │   ├── spec0002.txt
        │   └── ...
        └── CR-G3-03/
            └── ...

    Each .txt file must be 2-column ASCII:
      • column 1: Raman shift (cm⁻¹)
      • column 2: intensity (a.u.)
    Lines starting with '#' are ignored.
""",

    # ------------------------------------------------------------------------
    "Raw_Spectrum": """\
# Raw_Spectrum/

🇫🇷  Place ici les spectres BRUTS à pré-traiter avec « Match Search »
    (débruitage CDAE, baseline CBRAE/AsLS/Polynomial/SNIP, fit des pics,
    identification automatique).

    L'arborescence est libre — tu peux organiser par sample, par session,
    par date :

        Raw_Spectrum/
        ├── CR-G3-05/
        │   └── 22042026/
        │       ├── spec0001.txt
        │       └── ...
        └── ma_session_du_jour/
            └── ...

    Format : .txt 2 colonnes (Raman shift, intensité), comme SAMPLES/.

🇬🇧  Drop here the RAW spectra to preprocess with “Match Search”
    (CDAE denoising, CBRAE/AsLS/Polynomial/SNIP baseline, peak fitting,
    auto identification).

    Free folder layout — organize by sample, session, or date:

        Raw_Spectrum/
        ├── CR-G3-05/
        │   └── 22042026/
        │       ├── spec0001.txt
        │       └── ...
        └── todays_session/
            └── ...

    Format: 2-column .txt (Raman shift, intensity), same as SAMPLES/.
""",

    # ------------------------------------------------------------------------
    "DATABASE_RRUFF": """\
# DATABASE_RRUFF/

🇫🇷  Place ici la bibliothèque RRUFF de spectres de référence.

    Le sous-ensemble recommandé est « Raman — Excellent (Oriented or
    Unoriented) », téléchargeable gratuitement depuis :

        https://rruff.info/zipped_data_files/raman/

    Décompresse l'archive et organise les fichiers en sous-dossiers PAR
    MINÉRAL, en suivant la convention « NomMineral_Rxxxxxx.txt » :

        DATABASE_RRUFF/
        ├── Anatase/
        │   ├── Anatase__R070582.txt
        │   ├── Anatase__R060277.txt
        │   └── ...
        ├── Hematite/
        │   └── ...
        └── ...

    L'application scanne automatiquement la structure au démarrage.

    ⚠ La base RRUFF n'est PAS distribuée avec l'application : elle est
    sous licence CC-BY et appartient au projet RRUFF.

🇬🇧  Drop here the RRUFF reference spectrum library.

    The recommended subset is “Raman — Excellent (Oriented or Unoriented)”,
    freely downloadable from:

        https://rruff.info/zipped_data_files/raman/

    Unzip the archive and organize the files in PER-MINERAL subfolders,
    following the “MineralName_Rxxxxxx.txt” naming convention:

        DATABASE_RRUFF/
        ├── Anatase/
        │   ├── Anatase__R070582.txt
        │   ├── Anatase__R060277.txt
        │   └── ...
        ├── Hematite/
        │   └── ...
        └── ...

    The application scans the folder structure automatically at startup.

    ⚠ The RRUFF database is NOT distributed with the application: it is
    licensed CC-BY and belongs to the RRUFF Project.
""",

    # ------------------------------------------------------------------------
    "MODELS": """\
# MODELS/

🇫🇷  Place ici les checkpoints PyTorch des modèles deep-learning utilisés
    par « Match Search » :

        MODELS/
        ├── cdae_best.pth      ← Convolutional Denoising AutoEncoder
        └── cbrae_best.pth     ← Convolutional Baseline Removal AE

    Ces fichiers sont publiés dans l'archive de la thèse de master
    associée (Zenodo — lien à venir).

    Sans ces fichiers, l'application fonctionne quand même : les modules
    CDAE / CBRAE seront simplement désactivés. Les algorithmes classiques
    AsLS, Polynomial et SNIP restent pleinement utilisables.

🇬🇧  Drop here the PyTorch checkpoints for the deep-learning models used
    by “Match Search”:

        MODELS/
        ├── cdae_best.pth      ← Convolutional Denoising AutoEncoder
        └── cbrae_best.pth     ← Convolutional Baseline Removal AE

    These files are published in the companion master's thesis archive
    (Zenodo — link forthcoming).

    Without them, the application still runs: the CDAE / CBRAE buttons
    are simply disabled. The classical AsLS, Polynomial and SNIP
    algorithms remain fully functional.
""",

    # ------------------------------------------------------------------------
    "PROJETS": """\
# PROJETS/

🇫🇷  Ce dossier reçoit AUTOMATIQUEMENT les projets que tu sauvegardes
    depuis l'application :

        PROJETS/
        ├── PlotBuilder/       ← fichiers .rpm  (Plot Builder)
        └── MatchSearch/       ← fichiers .rms  (Match Search)

    Chaque projet est un fichier JSON qui restaure intégralement l'état
    de la session : spectres ouverts, prétraitements appliqués, pics
    fittés, références RRUFF chargées, notes utilisateur, position du
    zoom, thème, etc.

    Tu peux copier librement ces fichiers entre machines : ils sont
    autonomes (les chemins de spectres sont relatifs au dossier
    Raw_Spectrum/ ou SAMPLES/ correspondant).

🇬🇧  This folder AUTOMATICALLY receives the projects you save from the
    application:

        PROJETS/
        ├── PlotBuilder/       ← .rpm files  (Plot Builder)
        └── MatchSearch/       ← .rms files  (Match Search)

    Each project is a JSON file that fully restores a session state:
    open spectra, applied preprocessing, fitted peaks, loaded RRUFF
    references, user notes, zoom position, theme, etc.

    You can freely copy these files between machines: they are
    self-contained (spectrum paths are relative to the corresponding
    Raw_Spectrum/ or SAMPLES/ folder).
""",

    # ------------------------------------------------------------------------
    "SAUVEGARDE": """\
# SAUVEGARDE/

🇫🇷  Dossier d'EXPORT (pas de chargement). Trois sous-dossiers seront
    créés au fur et à mesure de tes exports :

        SAUVEGARDE/
        ├── Figures/        ← exports PNG / PDF / SVG (bouton SAUVEGARDER)
        ├── Save CSV/       ← exports Excel multi-onglets (.xlsx)
        └── Rapports/       ← rapports PDF multi-pages (auto-générés)

    Tu peux supprimer ce dossier à tout moment, l'application le
    recréera lors du prochain export.

🇬🇧  EXPORT folder (no loading from here). Three subfolders are populated
    as you export from the application:

        SAUVEGARDE/
        ├── Figures/        ← PNG / PDF / SVG exports (SAVE button)
        ├── Save CSV/       ← multi-tab Excel exports (.xlsx)
        └── Rapports/       ← multi-page PDF reports (auto-generated)

    Feel free to delete this folder at any time — the application will
    recreate it on the next export.
""",
}


# ----------------------------------------------------------------------------
# Build logic
# ----------------------------------------------------------------------------
def _clean_previous_build() -> None:
    """Remove leftover build artifacts from previous runs."""
    for d in ("build", "dist", f"{APP_NAME}.spec"):
        p = HERE / d
        if not p.exists():
            continue
        if p.is_dir():
            print(f"  • removing {p}")
            shutil.rmtree(p)
        else:
            print(f"  • removing {p}")
            p.unlink()


def _build_pyinstaller_command() -> list[str]:
    """Construct the PyInstaller CLI command."""
    cmd: list[str] = [
        "pyinstaller",
        "--name", APP_NAME,
        "--windowed",                       # no console window
        "--onedir",                         # bundle in a folder (faster startup
                                            # than --onefile, mandatory if you
                                            # ship the runtime folders next to
                                            # the .exe)
        "--clean",
        "--noconfirm",
        # CTk and matplotlib have non-Python assets that need bundling
        "--collect-all",        "customtkinter",
        "--collect-submodules", "matplotlib",
        # Hidden imports that PyInstaller may miss
        "--hidden-import", "scipy.signal",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "openpyxl",
    ]

    # Icon — optional, only added if file exists
    if ICON_FILE.exists():
        cmd.append(f"--icon={ICON_FILE}")

    # Bundled data files
    for src, dst in BUNDLED_DATA:
        src_path = HERE / src
        if src_path.exists():
            sep = ";" if sys.platform == "win32" else ":"
            cmd.append(f"--add-data={src_path}{sep}{dst}")

    cmd.append(str(MAIN_FILE))
    return cmd


def _create_runtime_folders(out_dir: Path) -> None:
    """Create the runtime folder layout next to the bundled executable
    and drop a bilingual README.txt in each top-level folder."""
    print(f"\n→ Creating runtime folders inside {out_dir}/")
    for rel in RUNTIME_DIRS:
        target = out_dir / rel
        target.mkdir(parents=True, exist_ok=True)
        print(f"  • {target}")

    print(f"\n→ Writing bilingual README.txt in top-level runtime folders")
    for folder, content in RUNTIME_READMES.items():
        readme_path = out_dir / folder / "README.txt"
        readme_path.write_text(content, encoding="utf-8")
        print(f"  • {readme_path}")


def _print_summary(out_dir: Path) -> None:
    print("\n" + "=" * 78)
    print(f"  ✓ Build successful — {APP_NAME} v{APP_VERSION}")
    print("=" * 78)
    print(f"  Bundle directory : {out_dir}")
    exe_name = APP_NAME + (".exe" if sys.platform == "win32" else "")
    exe_path = out_dir / exe_name
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"  Executable       : {exe_path} ({size_mb:.1f} MB)")
    print(f"  Runtime folders  : {len(RUNTIME_DIRS)} folders created with README")
    print("\n  Next steps:")
    print(f"    1. Open {out_dir} and double-click {exe_name}")
    print(f"    2. Read the README.txt in each runtime folder for setup hints")
    print(f"    3. Drop your spectra in SAMPLES/ or Raw_Spectrum/")
    print(f"    4. (Optional) Drop the trained models in MODELS/")
    print(f"    5. (Optional) Drop the RRUFF library in DATABASE_RRUFF/")
    print()


def build() -> None:
    print(f"Raman Plot|Match Builder — build script v{APP_VERSION}")
    print("-" * 78)

    if not MAIN_FILE.exists():
        print(f"✗ ERROR: main file not found at {MAIN_FILE}")
        print(f"  Make sure {MAIN_FILE.name} is in the same folder as build_exe.py")
        sys.exit(1)

    print("→ Cleaning previous build artifacts")
    _clean_previous_build()

    print("\n→ Running PyInstaller")
    cmd = _build_pyinstaller_command()
    print("  Command:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=HERE)
    if result.returncode != 0:
        print(f"\n✗ PyInstaller failed (exit code {result.returncode})")
        sys.exit(result.returncode)

    out_dir = HERE / "dist" / APP_NAME
    if not out_dir.is_dir():
        print(f"\n✗ Expected output folder not found: {out_dir}")
        sys.exit(1)

    _create_runtime_folders(out_dir)
    _print_summary(out_dir)


if __name__ == "__main__":
    build()
