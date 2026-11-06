# Reproducing the completed Kerala Phase 2 experiments

## Scope

This archive freezes the Phase 2 files and their inherited inputs as they stood at handoff. It contains the actual CSV, JSON and SVG outputs. The completed computational work is (1) a four-year pre-flood agricultural baseline and descriptive output/rank sensitivity analysis and (2) an independent deterministic reproduction of the inherited agricultural ranking grid. The Earth Engine pilot is explicitly **unexecuted**. No 2018 event exposure raster, satellite recovery panel, flood-attributable recovery duration, multidimensional index or predictive validation exists in this package.

## Directory layout and exact commands

Extract the ZIP without changing directory names. From the extracted archive root:

```sh
python3 --version
python3 phase2/analysis.py
python3 phase2/reproduce_legacy.py
```

`analysis.py` reads `Kerala_Flood_Recovery_Codex_Package_Fixed(1)/kerala_recovery_investigation/district_crop_panel.csv`, `experiment_results.json`, and `district_descriptive_ranks.csv`. It writes the seven-year combined crop panel, the pre-2018 crop file, five analysis outputs in `phase2/results/` (annual deviations, area/yield decomposition, rank sensitivity, leave-one-pre-year-out sensitivity, and summary), and the SVG figure. `reproduce_legacy.py` additionally reads the inherited `sensitivity_grid.csv` and `robustness_results.json`, then writes `phase2/results/legacy_reproduction.json`. The archived results are included so an auditor can compare before and after rerunning. These commands will overwrite **outputs in the extracted copy**; retain the ZIP as the immutable reference.

The Phase 2 scripts require only Python's standard library (`csv`, `itertools`, `json`, `pathlib`, `statistics`). No `pip install`, network access, Earth Engine login, or random seed is needed. The original execution was on macOS 15.3 arm64 with Python 3.9.6; Python 3.9 or newer is appropriate. Floating-point text at very low-order decimals may differ across Python versions, so compare the reported rounded metrics rather than only byte-for-byte regenerated output.

Expected deterministic checks from the included outputs: 168 inherited district/crop/year rows; 126 new pre-flood rows; 294 combined rows (14 districts × 3 crops × 7 years); 126 post-event output-deviation rows; 6 ranking specifications; 4 leave-one-pre-year-out specifications; 84 inherited sensitivity-grid specifications reproduced with **zero discrepancies**; three pseudo-holdout top-five capture values reproduced with absolute difference 0. The 2020–21 pseudo-holdout is a descriptive diagnostic, not a leak-free prediction.

## Original scripts and seeds

The original `experiment.py`, `robustness.py`, `make_comparison_figure.py`, report builder, source data and archived figures are included for inspection. Running the original scripts is **not required** to reproduce Phase 2 and will rewrite files in the extracted inherited directory. If rerunning them separately, use a disposable copy and install compatible NumPy, SciPy and Matplotlib; `build_report.py` also needs `python-docx`. The old report/manuscript builders retain historical `/mnt/data` paths and are not portable as-is.

The inherited scripts use NumPy `default_rng(101)` for 4,000 rank-displacement permutations in `experiment.py`. `robustness.py` uses `default_rng(1937 + int(alpha*100))` with 10,000 permutations per alpha: seeds 1947, 1962 and 1987 for alpha 0.10, 0.25 and 0.50. Phase 2 independently reran the **deterministic** grid and capture calculations; it did not rerun those stochastic draws. The archived permutation results remain in the inherited JSON files and should not be mistaken for newly validated findings.

## Data provenance and limits

The new 2014–15 to 2016–17 observations are transcribed from Kerala Department of Economics and Statistics, *Agriculture Statistics 2005–20*, Table 41 (rice, PDF page 95), Table 44 (banana, page 101), and Table 45 (plantain, page 102): https://www.ecostat.kerala.gov.in/storage/publications/626.pdf. The 2017–18 through 2020–21 rows are the inherited annual-report transcription, with source URL and PDF page on every row. All nine newly transcribed crop/year district sums match the official state totals. The full 168 inherited cells have **not** been checked individually against the source PDFs. Official PDFs are not embedded in this archive; the included transcriptions and provenance suffice to reproduce calculations, while independent transcription verification requires the linked official reports.

`phase2/gee_2018_pilot_UNEXECUTED.js` is only a prepared Earth Engine Code Editor script. Syntax checking is not image processing. It requires an authenticated registered Earth Engine account, enabled Cloud project, scene QA, exports, and independent flood-map validation. Do not report its candidate output as an executed experiment.

See `DATA_DICTIONARY.md` for units and missingness, `EXPERIMENT_SUMMARY.md` for numerical findings, and `MANIFEST.md` for file inventory and SHA-256 checksums. The archived `phase2/results/original_input_manifest.csv` contains one `.DS_Store` entry from the original workspace; that Finder metadata file is intentionally excluded from this handoff. `MANIFEST.md` is authoritative for the ZIP contents.
