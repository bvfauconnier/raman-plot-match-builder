# Source code

Drop the application source files here:

- `raman_gui.py` — the main monolithic application (~24 000 lines, latest
  version delivered by Claude as `raman_gui.py`)
- `raman_db.py` — the static mineral-mode database
- `build_exe.py` — PyInstaller build helper

Once these three files are in place, this folder is the entry point of
the application. Run it with:

```bash
python src/raman_gui.py
```

> The current code is intentionally monolithic for v1.0.0. Modular
> refactoring into `core/`, `ui/`, `i18n/`, `pdf/`, `ml/` subpackages is
> tracked in [`docs/architecture.md`](../docs/architecture.md#future-work).
