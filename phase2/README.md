# Kerala flood recovery Phase 2 audit and first executed experiments

Run from the project root with the system Python standard library:

```sh
python3 phase2/analysis.py
python3 phase2/reproduce_legacy.py
```

This regenerates `data/pre2018_crop_production.csv`, the combined
`data/crop_panel_2014_2021.csv`, every CSV and JSON in
`results/` except `original_input_manifest.csv` and
`legacy_reproduction.json`, and the vector SVG in
`figures/`. It uses the untouched Phase 1 `district_crop_panel.csv` as input.
The second command independently reproduces the complete 84-specification
deterministic Phase 1 sensitivity grid and pseudo-holdout capture values.
The supplied package is recorded by SHA-256 in `results/original_input_manifest.csv`.

The new official pre-flood observations come from [Kerala DES, Agriculture
Statistics 2005–20](https://www.ecostat.kerala.gov.in/storage/publications/626.pdf):
Table 41 (rice, PDF page 95), Table 44 (banana, page 101), and Table 45
(plantain, page 102). Each of 2014–15, 2015–16 and 2016–17 has 14 district
values for all three crops; all nine district sums match the printed state
totals. The 2017–18 through 2020–21 observations and source-page fields are
read from the original CSV. The 2018–19 statewide crop-area comparison is
from [DES Agricultural Statistics 2018–19, printed page 126](https://ecostat.kerala.gov.in/storage/publications/239.pdf).

`gee_2018_pilot_UNEXECUTED.js` is a **prepared, syntax-checked, unexecuted**
Earth Engine Code Editor pilot. It exports a candidate Sentinel-1 change layer,
Landsat 8 quarterly vegetation indices with QA, and VIIRS monthly radiance with
coverage. No satellite result or recovery duration was obtained in this run.
The script prints scene counts and common relative orbits; stop if those are
empty, and independently validate any flood map before analysis.

Read `results_phase2.md`, `methods_and_limitations.md`, and
`data_availability_and_gaps.md` before interpreting output. The new crop
quantities are **annual output deviations**, not flood-caused damage or actual
post-flood recovery.
