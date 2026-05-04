# Architecture overview

> High-level description of the codebase to help you (or a contributor)
> orient yourself before diving into the ~24 000 lines of `src/raman_gui.py`.
> *This document is intentionally informal and will evolve as the codebase
> is refactored into smaller modules.*

---

## Source code layout (this repository)

```
src/
├── raman_gui.py        ← MONOLITHIC — both Plot Builder and Match Search GUIs
├── raman_db.py         ← static dictionary of mineral Raman modes (with
│                         positions, intensities, references) used for
│                         peak-mode tooltips and identification hints
└── build_exe.py        ← cross-platform build helper (PyInstaller wrapper)
```

The application is intentionally distributed as a single Python file at
v1.0.0 to make distribution and packaging trivial. Modular refactoring is
planned for v2.0 (see *Future work* below).

---

## Runtime folder layout (on the user's machine)

The application reads from and writes to the following folders, **all
located next to `raman_gui.py` (or next to the bundled `.exe`)**:

| Folder              | Provided by  | Role                                                                       |
|---------------------|--------------|----------------------------------------------------------------------------|
| `SAMPLES/`          | user         | experimental spectra, browsed by Plot Builder                              |
| `Raw_Spectrum/`     | user         | raw spectra to preprocess, browsed by Match Search                         |
| `DATABASE_RRUFF/`   | user         | RRUFF reference library (per-mineral subfolders)                           |
| `MODELS/`           | user         | PyTorch checkpoints `cdae_best.pth` and `cbrae_best.pth`                   |
| `PROJETS/`          | auto-created | saved projects (`PlotBuilder/*.rpm` and `MatchSearch/*.rms`)               |
| `SAUVEGARDE/`       | auto-created | exports (`Figures/`, `Save CSV/`, `Rapports/`)                             |

The folder names are defined as constants at the top of `raman_gui.py`:

```python
SUBDIR_SAMPLES        = "SAMPLES"
SUBDIR_RAW_SPECTRUM   = "Raw_Spectrum"
SUBDIR_RRUFF          = "DATABASE_RRUFF"
SUBDIR_MODELS         = "MODELS"
SUBDIR_PROJETS        = "PROJETS"
SUBDIR_PROJETS_PLOT   = "PlotBuilder"     # → PROJETS/PlotBuilder/
SUBDIR_PROJETS_MATCH  = "MatchSearch"     # → PROJETS/MatchSearch/
SUBDIR_SAVE           = "SAUVEGARDE"
SUBDIR_FIGURE_SAVE    = "Figures"         # → SAUVEGARDE/Figures/
SUBDIR_CSV_SAVE       = "Save CSV"        # → SAUVEGARDE/Save CSV/
SUBDIR_RAPPORTS_SAVE  = "Rapports"        # → SAUVEGARDE/Rapports/
```

If you want to rename them globally (e.g. translate `SAUVEGARDE` to
`BACKUP` for an English deployment), change these constants once and
the whole application follows.

---

## Logical sections of `raman_gui.py`

The file is organized top-to-bottom in roughly the following order. Use
your editor's "Go to symbol" / outline view to jump quickly.

| Lines (approx.) | Section                                  | Purpose                                                       |
|-----------------|------------------------------------------|---------------------------------------------------------------|
| 1 –   115       | Imports + constants                      | All third-party imports, version, paths, feature flags        |
| 116 –  154      | `apply_academic_style()`                 | Matplotlib publication-quality style                          |
| 155 –  535      | Peak-fitting kernels                     | `_peak_gaussian/_lorentzian/_pseudovoigt`, `_fit_single_peak` |
| 537 –  620      | Peak evaluation helpers                  | `_eval_peak_profile`, `_eval_peak_baseline`                   |
| 621 –  920      | Matching / scoring                       | `_match_peaks`, `_compute_match_scores`, `_optimize_offset`   |
| 922 – 1100      | RRUFF cache                              | Local cache of detected peaks per RRUFF file                  |
| 1099 – 1230     | Mineral-mode helpers                     | Diagnostic-mode tooltips                                      |
| 1230 – 1300     | Figure save helpers                      | `_save_fig_multiformat`                                       |
| 1310 – 1720     | Cross-toolkit widget shims               | `_Button`, `_Frame`, … (CTk / ttk fallback)                   |
| 1721 – 1800     | `class Tooltip`                          | Shared tooltip widget                                         |
| 1819 – 2010     | Spectrum I/O + LaTeX → Unicode helpers   | `load_spectrum`, `latex_to_unicode`                           |
| 2010 – 4500     | i18n: `LANG = {'fr': {...}, 'en': {...}}` | The bilingual translation dictionary (~1000 keys × 2)         |
| 4500 – 5300     | i18n logic                               | `set_language`, `t()`, `_save_language`                       |
| 5305 – 5837     | `class StartupDialog`                    | Splash / launcher window                                      |
| 5838 – 13156    | `class RamanPlotGUI`                     | Plot Builder main window                                      |
| 13157 – 13234   | `class _TabState`                        | State of one open tab in Match Search                         |
| 13235 – end     | `class RamanMatchSearchGUI`              | Match Search main window (largest class)                      |

---

## Key data structures

### `_TabState` (Match Search, one per open tab)

```python
class _TabState:
    spectrum_path: str              # absolute path of the raw .txt
    spectrum_name: str              # display label
    frame: ttk.Frame                # tab's tk widget
    curves: list[dict]              # [{'name', 'x', 'y', 'visible',
                                    #   'is_source', 'history', ...}, ...]
    fits: list[dict]                # peak-fitting sessions
```

### Curve dict (preprocessing chain)

```python
{
    'id':        int,                    # unique within tab
    'name':      str,                    # 'CDAE+CBRAE+AsLS'
    'x':         np.ndarray,
    'y':         np.ndarray,
    'visible':   bool,
    'is_source': bool,                   # the radio • for next algo
    'history':   list[str],              # ['CDAE', 'CBRAE', 'AsLS']
}
```

### Fit dict (one fit session inside a tab)

```python
{
    'id':              int,
    'name':            str,
    'source_history':  list[str],
    'source_x':        np.ndarray,       # frozen copy at creation
    'source_y':        np.ndarray,
    'peaks':           list[dict],       # see Peak below
    'references':      list[dict],       # RRUFF refs added to this fit
    'match_results':   dict | None,      # current match analysis
    'user_notes':      str,
    'modified_at':     str,              # ISO timestamp
    'xlim':            tuple | None,     # user-saved zoom
}
```

### Peak dict

```python
{
    'id':         int,
    'position':   float,                 # cm⁻¹
    'origin':     'auto' | 'manual',
    'fitted':     dict | None,           # fit results
    'fit_error':  str | None,
    'fit_warning': bool,
    'window_xmin': float | None,         # manual fit window
    'window_xmax': float | None,
    'shape':      'gaussian' | 'lorentzian' | 'pseudovoigt',
    'label':      str,                   # user-overridable
    'offset':     float,                 # per-peak calibration shift
}
```

---

## Persistence formats

### `.rpm` — Plot Builder project (JSON)

Serialized state of one Plot Builder session: open spectra, references,
peaks, view settings, comments. Loaded back as-is.

### `.rms` — Match Search project (JSON)

Serialized state of one Match Search session: every open tab, every
computed curve, every fit, every match result. Larger than `.rpm` but
fully reproducible across machines.

### User config — `~/.raman_plot_builder.cfg`

Persistent user preferences (theme, language, recent projects, user
profile, library paths). **Not** committed to Git (see `.gitignore`).

### RRUFF peak cache — `<rruff_root>/.pic_cache.json`

Auto-generated cache of `find_peaks` results per RRUFF reference, indexed
by file path. Speeds up auto-identification by ~10× on subsequent runs.

---

## i18n / language switching

- Translation dict: `LANG = {'fr': {key: text}, 'en': {key: text}}`
- Lookup function: `t(key, **kwargs)` (with format-string interpolation)
- Hot-switch: `set_language(lang)` updates `CURRENT_LANG` and re-saves
  the user config.
- **Limitation**: tkinter does not re-render already-built static labels;
  newly-opened dialogs use the new language, but visible labels stay in
  the original language until the app is restarted. This is documented
  in the `View > Language` menu action.

---

## RRUFF integration

The application expects a local copy of the RRUFF "Excellent peaks"
dataset, organized as:

```
<rruff_root>/
├── <Reference_folder>/
│   ├── MineralName_Rxxxxxx.txt
│   └── ...
└── ...
```

Files are 2-column (Raman shift, intensity) ASCII. The path is
configured per-session in the application settings.

The dataset is **not redistributed** with this software. It can be
downloaded from [https://rruff.info](https://rruff.info) (CC-BY).

---

## Deep-learning models (CDAE / CBRAE)

Two PyTorch models are loaded on demand from `MODELS/`:

- `MODELS/cdae_best.pth` — Convolutional Denoising AutoEncoder, applied
  to the raw spectrum to remove shot/read noise while preserving peak
  shape.
- `MODELS/cbrae_best.pth` — Convolutional Baseline Removal AutoEncoder,
  applied (typically) on top of CDAE output to estimate and subtract the
  fluorescence baseline.

Both models share a similar 1D-convolutional encoder/decoder topology,
trained on a large set of synthetic Raman spectra augmented with
real-world noise and baselines. **Training scripts and datasets are not
part of this repository** — they belong to the thesis appendix archive.

When `torch` is not installed, the application detects it at startup and
disables the CDAE / CBRAE buttons; the classical algorithms (AsLS,
Polynomial, SNIP) remain fully functional.

---

## Future work

Planned for v2.x (no concrete date):

1. **Modular refactoring** — split `raman_gui.py` into `core/`, `ui/`,
   `i18n/`, `pdf/`, `ml/` subpackages.
2. **Unit tests** — currently absent; targeting `core/peak_fitting.py`,
   `core/peak_matching.py`, and `core/spectrum_io.py` first.
3. **CI** — GitHub Actions workflow running `pytest` on push and
   building a Windows `.exe` on tagged releases.
4. **Sphinx docs** — auto-generated API documentation hosted on
   ReadTheDocs.
