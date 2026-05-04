# Changelog

All notable changes to **Raman Plot|Match Builder** are documented in this
file. The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-05-04

First public release accompanying the master's thesis of Basile-Vladimir
Fauconnier (Université de Liège / Université de Sherbrooke, 2026):
*Mineralogical characterization of gossan samples from the Canadian Arctic
as a Mars analog environment.*

### Added — Plot Builder module

- Multi-spectrum visualization with grouping (sample / reference)
- Peak annotation with editable position, label, and per-peak offset
- RRUFF reference overlay with per-reference offset and color
- Reference search by mineral name with fuzzy matching
- Drag-and-drop spectrum loading (requires `tkinterdnd2`)
- PDF report export with full layout and metadata
- Project save/load to `.rpm` format
- Recent projects menu

### Added — Match Search module

- Spectrum preprocessing with multiple algorithms:
  - **CDAE** (Convolutional Denoising AutoEncoder) — deep-learning denoising
  - **CBRAE** (Convolutional Baseline Removal AutoEncoder) — deep-learning
    baseline estimation
  - **AsLS** (Asymmetric Least Squares) — classical baseline correction
  - **Polynomial** baseline fit
  - **SNIP** (Statistical sensitive Non-linear Iterative Peak-clipping)
- Multi-tab parallel processing of independent spectra
- Computed-curves chaining (e.g. CDAE → CBRAE → AsLS) with full traceability
- Per-tab fit window with pseudo-Voigt / Gaussian / Lorentzian peak fitting
- Live peak detection (auto + manual click)
- Match analysis against a single RRUFF reference (M1 / M2 / M3 scores,
  Δν statistics, offset optimization)
- Automatic identification: full RRUFF database scan with ranking by F1-score
- Side-by-side tab comparison view with synchronized axes
- Multi-tab Excel export (`.xlsx`) with metadata sheet
- Project save/load to `.rms` format
- Hierarchical undo/redo per fit window

### Added — Cross-cutting features

- **Bilingual interface (FR / EN)** with hot-switch via `View > Language`
- Modern custom menu bar (theme-aware, replaces native `tk.Menu`)
- Light / dark / system theme switching
- User profile dialog (used as author metadata in PDF reports)
- First-launch tutorial with 5 illustrated steps
- About dialog
- Tab-level right-click / middle-click context menu
- Keyboard shortcuts (Ctrl+S, Ctrl+Z, Ctrl+Y, Ctrl+W, Ctrl+Tab, etc.)

### Added — Build & packaging

- Cross-platform build script (`build_exe.py`) using PyInstaller
- Custom `.spec` file with icon embedding

### Development methodology

This release was developed with the assistance of **Anthropic's Claude
(Opus 4.7)** as a coding-acceleration tool for UI scaffolding, FR/EN
translation, refactoring, and debugging. All scientific decisions,
methodological choices, and result interpretation are the work of the
author. See [`AI_USAGE.md`](AI_USAGE.md) for the full disclosure.

### Known limitations

- The native `tk.Menu` popups (when clicking on the custom menu bar buttons)
  do not follow the CTk theme — only the bar itself does.
- Hot-switching language (`View > Language`) updates new dialogs but not
  labels of the already-built window — a restart is required to retranslate
  every static label.
- The Excel multi-tab export requires `openpyxl`; without it, the menu
  entry is shown but produces an explicit error message.
- Deep-learning models (CDAE / CBRAE) require `torch`; without it, classical
  algorithms (AsLS, Polynomial, SNIP) remain fully functional.
- The trained `MODELS/cdae_best.pth` and `MODELS/cbrae_best.pth` checkpoints
  are not bundled with the source repository and must be obtained from the
  thesis archive (link forthcoming).
