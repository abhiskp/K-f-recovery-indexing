# Reproduce Phase 7

Run from the project root, or extract the Phase 7 ZIP and run from the extraction directory. The scripts use Python **3.9 or newer**, standard library only, deterministic arithmetic, and **no random seeds**. All required source PDFs, their extracted text and the visually transcribed scanned summer table are in `phase7/data/raw/`. The two read-only upstream inputs are `phase3/data/processed/district_season_rice_2014_2020.csv` and `phase6/data/processed/official_district_notification_status.csv`; their SHA-256 hashes are in `phase7/results/checksums.csv`. No Earth Engine account, credentials or network connection is required for the completed analyses.

For the ZIP handoff, first run `unzip kerala_flood_recovery_phase7_2026-11-16.zip -d phase7_handoff` and then `cd phase7_handoff`. For a Git checkout, run the following commands from the repository root.

```sh
python3 phase7/scripts/checksums.py verify
python3 phase7/scripts/extend_rice_panel.py
python3 phase7/scripts/descriptive_diagnostics.py
python3 phase7/scripts/validate_phase7.py
python3 phase7/scripts/checksums.py verify
```

Expected terminal checks: `rows=462 new=210 QA=30 max_abs_state_difference=0.074`; descriptive summary includes `all_minus_some_pp: -50.15151` and 2017–18 placebo `19.25802`. The validation script checks the unchanged Phase 3 source values, new keys, 30 state controls and three flagged 2020–21 component mismatches. The first and last checksum checks protect archived inputs and regenerated outputs. Scripts overwrite only Phase 7 processed/results files with deterministic content; previous phases are untouched. `checksums.py write` is for intentionally refreshing the manifest after a documented change and should **not** be run as a verification step.

For a fresh extraction from the archived official PDFs, use Poppler's `pdftotext -layout` (the cached text is already included):

```sh
for id in 622 664 1720 1822 1824; do
  pdftotext -layout "phase7/data/raw/kerala_des_${id}.pdf" "phase7/data/raw/kerala_des_${id}.txt"
done
```

`kerala_des_1844.pdf` is image-only; `kerala_des_1844_summer_{wet,dry}_transcription.csv` records the district cells read from PDF pages 1 and 2. Compare them visually with the archived PDF/page PNGs and their separate printed state controls. No OCR inference is required. The official PDFs came from `https://www.ecostat.kerala.gov.in/storage/publications/{622,664,1720,1822,1824,1844}.pdf`; the server presented an expired TLS certificate during this retrieval, so the archived PDFs and hashes provide the repeatable source snapshot. Source printed and PDF page numbers are in each new panel row and in `state_total_reconciliation.csv`.

`source_access_matrix.csv`, `nonagricultural_coverage_matrix.csv`, the independent audit copy and the unsent request drafts are research documentation, not executable exposure results. No spatial overlap or validation command exists because the gate inputs have not arrived.
