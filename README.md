# Raman Plot|Match Builder

> A desktop application for visualizing, preprocessing, peak-fitting, and
> identifying Raman spectra against the RRUFF reference database — designed
> for mineralogical characterization in astrobiology and Mars analog studies.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.0-orange)
![Status](https://img.shields.io/badge/status-research%20release-blueviolet)

🇫🇷 **Une version française de ce README est disponible** :
[README.fr.md](README.fr.md)

---

## ✨ Overview

**Raman Plot|Match Builder** is a standalone GUI application that bundles two
complementary modules around a unified Raman-spectroscopy workflow:

- **Plot Builder** — annotate peaks, overlay RRUFF references, and export
  publication-ready PDF reports.
- **Match Search** — preprocess spectra with classical (AsLS, Polynomial,
  SNIP) or deep-learning (CDAE, CBRAE) algorithms, fit individual peaks
  with pseudo-Voigt profiles, and identify minerals automatically by scanning
  the entire RRUFF database with multi-criteria F1-score ranking.

The application was developed as part of a master's thesis on the
**mineralogical characterization of gossan samples from the Canadian Arctic
as a Mars analog environment**, and is released to support reproducibility
of the published analysis.

---

## 📷 Screenshots

> *Screenshots to be added in [`docs/screenshots/`](docs/screenshots/) — see
> the section [Screenshots](#-screenshots-1) of this README for the recommended
> captures to take.*

| Welcome — main view                           | Plot Builder — main view                        |
|-----------------------------------------------|-------------------------------------------------|
| `docs/screenshots/plot_builder_welc.png`      | `docs/screenshots/plot_builder_main.png`        |

| Match Search — main view                      | Match Search — fit window                       |
|-----------------------------------------------|-------------------------------------------------|
| `docs/screenshots/match_search_fitwindow.png` | `docs/screenshots/match_search_fitwindow.png`   |

| Auto-identification results                   | PDF report (excerpt)                            |
|-----------------------------------------------|-------------------------------------------------|
| `docs/screenshots/auto_identify.png`          | `docs/screenshots/pdf_report.png`               |

---

## 🚀 Quick start

### Installation from source

```bash
git clone https://github.com/bvfauconnier/raman-plot-match-builder.git
cd raman-plot-match-builder
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python src/raman_gui.py
```

### Stand-alone executable (Windows)

A pre-built `.exe` will be attached to each tagged release on the
**Releases** page (when the repository becomes public).

To build it yourself:

```bash
pip install pyinstaller
python src/build_exe.py
```

The resulting executable is placed under `dist/`.

---

## 📁 Required runtime folder layout

The application expects the following folders **next to the executable
or `raman_gui.py`** on the user's machine. They are created automatically
on first launch if missing, *except for `MODELS/` and `DATABASE_RRUFF/`*
which contain assets the user must provide themselves.

```
<application root>/
├── raman_gui.py        (or RamanPlotMatchBuilder.exe)
│
├── SAMPLES/                   ← experimental spectra (Plot Builder)
│   └── <my_sample>/
│       ├── spec0001.txt
│       └── ...
│
├── Raw_Spectrum/              ← spectra to preprocess (Match Search)
│   └── <session_or_sample>/
│       ├── spec0001.txt
│       └── ...
│
├── DATABASE_RRUFF/            ← RRUFF reference library (user-provided)
│   ├── <Reference_folder>/
│   │   ├── MineralName_Rxxxxxx.txt
│   │   └── ...
│   └── ...
│
├── MODELS/                    ← deep-learning checkpoints (user-provided)
│   ├── cdae_best.pth          ← CDAE denoising model
│   └── cbrae_best.pth         ← CBRAE baseline-removal model
│
├── PROJETS/                   ← saved projects (auto-created)
│   ├── PlotBuilder/           ← .rpm files
│   └── MatchSearch/           ← .rms files
│
└── SAUVEGARDE/                ← exports (auto-created on first save)
    ├── Figures/               ← PNG / PDF / SVG figures
    ├── Save CSV/              ← Excel multi-tab exports
    └── Rapports/              ← multi-page PDF reports
```

### About the `MODELS/` and `DATABASE_RRUFF/` folders

For licensing and size reasons, **neither the trained model checkpoints
nor the RRUFF database are distributed with this repository**. You will
need to obtain them separately:

- **`MODELS/cdae_best.pth` and `MODELS/cbrae_best.pth`** — these are the
  PyTorch checkpoints of the deep-learning denoising / baseline-removal
  models trained on synthetic and experimental Raman data. They will be
  released alongside the master's thesis on a public archive (MatheO or
  similar — *link to be added*). Without them, the application still
  runs, but the CDAE / CBRAE preprocessing options are disabled. The
  classical algorithms (AsLS, Polynomial, SNIP) remain fully functional.

- **`DATABASE_RRUFF/`** — download the "Excellent peaks" subset from
[https://rruff.info/zipped_data_files/raman/](https://rruff.info/zipped_data_files/raman/), unzip it.

### Spectrum file format

All spectrum files (in `SAMPLES/`, `Raw_Spectrum/`, and `DATABASE_RRUFF/`)
must be 2-column ASCII:

```
# Optional comment lines starting with '#'
100.0    1234.5
100.4    1242.1
...
```

- Column 1 — Raman shift in cm⁻¹
- Column 2 — Intensity (a.u.)
- Separator: whitespace or comma
- Header lines starting with `#` are ignored

---

## 🧭 Workflow at a glance

```
   ┌─────────────────┐    ┌──────────────────┐    ┌───────────────────┐
   │ Raw spectra     │ ─► │  Preprocessing   │ ─► │  Peak fitting     │
   │ (.txt 2-col)    │    │  (CDAE / CBRAE / │    │  (pseudo-Voigt)   │
   │                 │    │   AsLS / SNIP)   │    │                   │
   └─────────────────┘    └──────────────────┘    └─────────┬─────────┘
                                                            │
                          ┌─────────────────────────────────┘
                          ▼
                ┌──────────────────────┐    ┌──────────────────────┐
                │  Match analysis      │ ─► │  Auto identification │
                │  (vs. one reference) │    │  (RRUFF database)    │
                └──────────────────────┘    └──────────┬───────────┘
                                                       ▼
                                            ┌──────────────────────┐
                                            │   PDF / Excel report │
                                            └──────────────────────┘
```

---

## 📂 Project structure (this repository)

```
raman-plot-match-builder/
├── README.md                     ← you are here
├── README.fr.md                  ← French version
├── LICENSE                       ← MIT
├── CHANGELOG.md                  ← release history
├── AI_USAGE.md                   ← disclosure of AI tooling used
├── requirements.txt              ← Python dependencies
├── pyproject.toml                ← project metadata
├── .gitignore
├── src/
│   ├── raman_gui.py              ← main application (~24 000 lines)
│   ├── raman_db.py               ← internal mineral mode database
│   └── build_exe.py              ← PyInstaller build script
├── docs/
│   ├── architecture.md           ← high-level code description
│   └── screenshots/              ← UI screenshots for the README
├── examples/
│   └── sample_spectra/           ← a few example .txt spectra
└── tests/                        ← (placeholder for future unit tests)
```

> Note: the runtime folders (`SAMPLES/`, `MODELS/`, `DATABASE_RRUFF/`,
> `PROJETS/`, `SAUVEGARDE/`, `Raw_Spectrum/`) are **not** part of this
> source repository. They are created or expected on the user's machine
> at the application root (see [Required runtime folder layout](#-required-runtime-folder-layout) above).

---

## 🔬 Methodology

The peak-fitting and matching pipeline is described in detail in the
companion master's thesis (link forthcoming). In short:

1. **Spectra** are loaded from 2-column `.txt` files
   (Raman shift in cm⁻¹, intensity in arbitrary units).
2. **Preprocessing** is fully traceable: every applied algorithm is recorded
   in the curve's history (e.g. `[CDAE+CBRAE+AsLS]`).
3. **Peak fitting** uses pseudo-Voigt profiles with optional linear baseline.
   Position, FWHM, area, and η (Gaussian/Lorentzian fraction) are reported
   with combined uncertainties (calibration ± 2 cm⁻¹, spectral step,
   statistical fit error).
4. **Matching** computes three scores:
   - **M1** (coverage) = matched peaks / total spectrum peaks
   - **M2** (signature) = matched peaks / total reference peaks
   - **M3** (F1-score) = harmonic mean of M1 and M2
5. **Auto identification** scans the entire RRUFF database, optimizes a
   per-reference offset (within ± 30 cm⁻¹), and ranks candidates by M3.

---

## 📷 Screenshots

You can recreate the recommended screenshots for this README as follows:

| File name                             | What to capture                                           |
|---------------------------------------|-----------------------------------------------------------|
| `plot_builder_main.png`               | Plot Builder window with 2–3 spectra and annotated peaks  |
| `match_search_main.png`               | Match Search main window with 2–3 tabs open               |
| `match_search_fitwindow.png`          | A Fit window showing peak fitting + match analysis        |
| `auto_identify.png`                   | The auto-identification results dialog with Top-10 hits   |
| `pdf_report.png`                      | One page of a generated PDF report (page 2 or 3)          |

Save these as PNG (1200–1600 px wide) into [`docs/screenshots/`](docs/screenshots/).

---

## 📜 Citation

If you use this software in academic work, please cite both the software
release and the underlying thesis:

```bibtex
@software{fauconnier_raman_2026,
  author = {Fauconnier, Basile-Vladimir},
  title  = {Raman Plot{\textbar}Match Builder: a tool for Raman spectroscopy
            preprocessing, peak fitting and mineral identification against
            the RRUFF database},
  year   = {2026},
  version = {1.0.0},
  url    = {https://github.com/bvfauconnier/raman-plot-match-builder}
}

@mastersthesis{COMING SOON}
```

---

## 📄 License

This project is released under the **MIT License** — see [LICENSE](LICENSE).
You are free to use, modify, and redistribute the code, including for
commercial purposes, provided the copyright notice is preserved.

The RRUFF spectral database is **not** distributed with this software and
remains the property of its respective contributors and the RRUFF Project
([https://rruff.info](https://rruff.info)).

---

## 🤖 AI assistance disclosure

This software was developed with assistance from **Anthropic's Claude
(Opus 4.7)** for coding acceleration (UI scaffolding, FR/EN translation,
refactoring, debugging). All scientific decisions, methodological choices,
data analysis, and result interpretation are the sole work of the author.
See [`AI_USAGE.md`](AI_USAGE.md) for the full disclosure.

---

## 👤 Author

**Ir. Basile-Vladimir Fauconnier**
Master in Space Sciences — Université de Liège (ULiège)
Master's thesis in Astrobiology — Université de Sherbrooke (UdeS)

📧 [bvfauconnier@gmail.com](mailto:bvfauconnier@gmail.com)
🐙 [github.com/bvfauconnier](https://github.com/bvfauconnier)

---

## 🙏 Acknowledgments

- **RRUFF Project** — for the open Raman reference database
  ([rruff.info](https://rruff.info))
- **Université de Liège** — Department of Astrophysics, Geophysics & Oceanography
- **Université de Sherbrooke** — Departement of Applied Geomatics — T-Mars Team

---

## 🛠 Contributing

This is a research-oriented release tied to a specific thesis. **Issues and
pull requests are welcome** but priority of merge is given to bug fixes
related to reproducibility of the published results. For larger features
or design changes, please open a discussion first.
