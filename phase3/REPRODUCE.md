# Reproduction

Run from the **project root**, with the supplied `phase2/data/crop_panel_2014_2021.csv` intact. The scripts write only inside `phase3/`.

```sh
python3 --version
python3 phase3/experiment_a.py
python3 phase3/make_figures.py
node --check phase3/gee_2018_flood_exposure_UNEXECUTED.js
python3 phase3/make_manifest.py
```

Tested with Python 3.11, Node 22, macOS. Experiment A, figures and manifest use **Python standard library only**; no package installation, Earth Engine account, environment variables or secrets are needed. All calculations are deterministic; **no random seed** is used. The raw official PDFs and checked table transcriptions are already included. `experiment_a.py` rebuilds the processed panel and all Experiment A result CSVs/JSON. `make_figures.py` rebuilds two SVGs from those CSVs. `make_manifest.py` must run last. It excludes its own output to avoid a self hash. Line endings, Python version and CSV writer behavior can alter file hashes on another platform while numerical content remains the same.

Independent checks implemented in `experiment_a.py`:

1. Require all 14 district and state rows for every compendium block; reject duplicate keys and negative values.
2. Compare each printed compendium annual total with its three seasons, each state seasonal total with its 14 districts, and each state annual total with printed district totals. Differences go to `data_quality_findings.csv`.
3. Compare the 2018–19 compendium seasonal cells with the separate contemporaneous report at decimal precision; compare every 2019–20 district, state, season and annual cell with the separate report.
4. Require all 2019–20 annual-report rows and state columns to reconcile exactly: 38 checks.
5. Compare 84 district annual rice totals with the inherited Phase 2 panel.

**Earth Engine status:** the JavaScript was syntax checked, not run against Earth Engine. To execute, use a Google account with a Cloud project registered for Earth Engine, the API enabled, and permission to use that project; see [Google's access guide](https://developers.google.com/earth-engine/guides/access). Open [Code Editor](https://code.earthengine.google.com/), select the project, paste the script, and run once to inspect scene inventory. Enter exact pre/event scene IDs that share relative orbit, IW mode, pass and polarization and cover the pilot rectangle at suitable dates. Run again, inspect QA; only then set `START_EXPORTS=true`. Run and start the two Drive export tasks. Retain the exported metadata CSV and GeoTIFF with the research record. A validated independent 2018 flood layer is still needed before interpreting candidate change as inundation. No password, OAuth token or private project configuration belongs in this repository.

The original source documents and their direct URLs are in [sources.md](sources.md). The 2018–19 raw table transcription retains decimal values for crosscheck; the main six-year panel uses the integer compendium cells for that year, explaining a one-tonne annual difference in two districts against Phase 2. For the 2019–20 panel, all area and production cells instead come from the contemporaneous annual report because of substantive compendium errors. There is no hidden download step.
