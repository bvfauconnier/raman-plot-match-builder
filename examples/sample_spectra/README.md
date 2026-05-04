# Example spectra

Drop 2–3 example raw spectra here so a fresh user can immediately see
the application working without having to provide their own data.

## Format

Each file must be a 2-column ASCII text file:

```
# Optional header lines beginning with '#'
100.0    1234.5
100.4    1242.1
100.8    1250.7
...
```

- Column 1 — Raman shift in **cm⁻¹**
- Column 2 — Intensity (arbitrary units)
- Separator: whitespace (tab or spaces) or comma

## Suggested examples

To showcase the app in different scenarios, the recommended set is:

| File                                | What it demonstrates                                  |
|-------------------------------------|-------------------------------------------------------|
| `anatase_demo.txt`                  | A clean spectrum with characteristic anatase peaks    |
| `hematite_demo.txt`                 | A spectrum showing the diagnostic 2-magnon band       |
| `gossan_noisy_demo.txt`             | A noisy gossan spectrum that benefits from CDAE/CBRAE |

Including raw, **unprocessed** versions makes the deep-learning preprocessing
showcase more impressive.

## Licensing

If your example spectra come from a public source (RRUFF, your own
acquisition, …), make sure their license allows redistribution. Add a
`SOURCES.md` here citing each file's origin.
