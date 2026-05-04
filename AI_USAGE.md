# AI assistance disclosure

This document discloses the use of AI tooling during the development of
**Raman Plot|Match Builder**, in line with current best practices of
academic transparency and the reproducibility expectations of master's
research.

---

## What was assisted by AI

This software was developed with the assistance of **Anthropic's Claude
(Opus 4.7)**, used as a **coding-acceleration tool** under the direct
supervision of the author. Claude contributed to:

- **Translation of UI strings** between French and English (~1000 keys
  in both languages, validated against the original FR text).
- **Refactoring of code** (renaming variables, extracting helpers,
  splitting long functions, applying consistent formatting).
- **Generation of repetitive boilerplate** (widget shims for the
  CTk / ttk fallback layer, dialog scaffolds, Tooltip definitions,
  matplotlib styling).
- **Debugging of regression bugs** introduced during refactoring (e.g.
  identifying mismatched variable names, broken dictionary keys,
  duplicated translation entries).
- **Writing of project metadata** (this `README`, `CHANGELOG`,
  `LICENSE`, `pyproject.toml`, `.gitignore`, and the present file).
- **Drafting of inline documentation strings** (subsequently reviewed
  and corrected by the author).

---

## What was NOT assisted by AI

The following — i.e. everything that constitutes the **scientific value**
of this work — is the sole contribution of the author:

- **The research question and hypothesis** of the underlying master's
  thesis (gossan mineralogy as a Mars analog).
- **Sample collection, preparation, and Raman acquisition** (laboratory
  work performed at the Université de Sherbrooke).
- **The choice of methodology**: peak-fitting model (pseudo-Voigt with
  optional linear baseline), matching scores (M1 / M2 / M3), offset
  optimization strategy, RRUFF database integration approach.
- **The architecture of the application** (Plot Builder + Match Search
  modules, Tab/Fit/Curve data hierarchy, persistence formats `.rpm` and
  `.rms`).
- **The deep-learning models** (CDAE and CBRAE) — their architecture,
  training data preparation, hyperparameter tuning and validation.
- **The interpretation of results**: every mineral identification, every
  peak-mode assignment, every published figure has been independently
  verified by the author against the literature and the geochemical
  context of the samples.
- **Final scientific claims** in the thesis and any companion paper.

---

## How the assistance was conducted

- All AI-generated code was **reviewed line-by-line** by the author
  before being kept in the codebase.
- Bugs introduced by AI suggestions (and there were several, e.g.
  duplicated dictionary entries silently overriding values, undefined
  variable names from search-and-replace) were **detected through
  manual testing on real data and through static analysis with
  `pyflakes`**.
- No AI-generated content describing **scientific results**, mineral
  interpretations, or experimental conclusions appears in this codebase
  or in the associated thesis.

---

## Why this disclosure matters

This is a research artifact. Reviewers, future contributors, and
readers of the companion thesis are entitled to know which parts of the
software were authored under what conditions, so they can:

1. **Place appropriate trust** in different layers of the codebase
   (the scientific kernels are author-validated; the UI scaffolding
   was AI-accelerated and should be treated as such).
2. **Reproduce the work** with full understanding of the development
   process.
3. **Cite the work** appropriately (the **author** is the scientific
   author; AI assistance is a development tool, not a co-author).

---

*Last updated: 2026-05-04*
