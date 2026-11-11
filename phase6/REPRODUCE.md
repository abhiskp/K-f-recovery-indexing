# Reproduce Phase 6

## Environment and inputs

Run from the project root on Python **3.9.4** or a compatible 3.9+ interpreter. Executed dependency versions were `numpy==2.0.2`, `rasterio==1.4.3`, `Pillow==11.3.0`, `matplotlib==3.9.4`; the remaining imports are Python standard library. The exact raw archives, IFI CSVs, government order, and extracted S1 files are included in `phase6/data/raw/`. The only required file outside Phase 6 is the preserved Phase 3 input `phase3/data/processed/district_season_rice_2014_2020.csv`. The Phase 4 exploratory 45-band GeoTIFF is also read, without changes: `phase4/data/raw/phase4_s1_2018_pilot_exploratory_candidate_bands.tif`. The archive-extraction step below is optional because the extracted S1 directory is included. No Earth Engine login, API credentials or network connection is required to rerun the saved-file analyses.

No stochastic estimation is used. The label permutation enumerates every combination exactly; **no random seed is needed**. The SVG identifier salt is fixed in the plotting script. Figure font rendering can vary across systems; numeric CSV/JSON results use deterministic calculation and rounding.

```bash
cd '/Users/abhijithshaji/Documents/Flood  Recovery'
python3 -m venv /private/tmp/phase6-repro-venv
/private/tmp/phase6-repro-venv/bin/python -m pip install 'numpy==2.0.2' 'rasterio==1.4.3' 'Pillow==11.3.0' 'matplotlib==3.9.4'
```

For an independent copy in another path, substitute that project root in the `cd` command. Python wheels depend on operating system and architecture; retain the exact versions above and record platform-specific build details if a wheel is unavailable.

## Rerun the completed analyses

```bash
cd '/Users/abhijithshaji/Documents/Flood  Recovery'
export MPLCONFIGDIR=/private/tmp/phase6-mpl-repro
/private/tmp/phase6-repro-venv/bin/python phase6/scripts/audit_public_sources.py
/private/tmp/phase6-repro-venv/bin/python phase6/scripts/audit_tiwari_s1.py
/private/tmp/phase6-repro-venv/bin/python phase6/scripts/notification_rice_screen.py
/private/tmp/phase6-repro-venv/bin/python phase6/scripts/checksums.py verify
```

`audit_public_sources.py` reads the source files and verifies NIH/PMC and Zenodo MD5s; Pillow may issue a harmless large-image warning for the 95.66-million-pixel KMZ overlay. `audit_tiwari_s1.py` scans all 11 GeoTIFFs, reprojects positive value-1 cells to the Phase 4 grid, and writes counts. `notification_rice_screen.py` transcribes the order's district categories, joins Phase 3, writes 378 joined rows and 27 contrasts, and creates the SVG/PNG figure. `checksums.py verify` checks every file in Phase 6 other than the manifest/checksum file plus the Phase 3 input. The figure's checksum should match in the same software/font environment; on other platforms, compare numeric CSVs/JSONs and inspect the figure visually.

To re-extract S1 from the verified original archive on macOS:

```bash
mkdir -p phase6/data/raw/tiwari_s1
bsdtar -xf phase6/data/raw/tiwari_pone_0237324_s001.7z -C phase6/data/raw/tiwari_s1
```

The original public sources, should downloads need to be rechecked, are listed with exact URLs and checksums in `results/raw_file_provenance.csv`; NIH's [PMC cloud instructions](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) explain the changed 2026 retrieval route for S1. The official source document is retained as downloaded. `results/checksums.csv` includes SHA-256 for the Phase 3 input and every Phase 6 file. To regenerate it **after intentional edits**, run `.../python phase6/scripts/checksums.py write` last. This does not rerun any analysis.

## What reproduction does not establish

These commands reproduce source inspections, same-sensor positive overlap and the administrative district/rice comparison. They do **not** generate independent flood labels, flooded-rice hectares, a recovery duration, a causal flood effect, a ranking, or a held-out validation score. Such results require the external files and permissions in `DATA_REQUESTS.md`.
