# Tests

This folder is intentionally empty in v1.0.0 — automated tests are part
of the v2.x roadmap (see [`docs/architecture.md`](../docs/architecture.md#future-work)).

## Planned test layout

```
tests/
├── conftest.py
├── unit/
│   ├── test_peak_fitting.py        # Gaussian / Lorentzian / pseudo-Voigt
│   ├── test_peak_matching.py       # M1, M2, M3 score computation
│   ├── test_spectrum_io.py         # load_spectrum, normalize_in_window
│   └── test_i18n.py                # ensure FR / EN keys are aligned
├── integration/
│   └── test_end_to_end.py          # tiny synthetic spectrum → fit → match
└── fixtures/
    ├── synthetic_gaussian.txt
    └── synthetic_two_peaks.txt
```

## Running tests (once they exist)

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
pytest -v --cov=src --cov-report=html
```

## Contributing tests

If you fix a bug, the most useful contribution is a regression test that
fails on `main` before your fix and passes after. Even a single test for
your fix is a great PR.
