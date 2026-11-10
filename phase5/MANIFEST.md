# Phase 5 file inventory and checksums

`results/file_manifest.csv` lists each Phase 5 file, purpose, byte count and SHA-256. `results/checksums.csv` gives the compact checksum view. The generated CSVs exclude themselves to avoid recursive hashes; `scripts/make_manifest.py` regenerates both. Source/processed files, scripts, figures, reports and the Earth Engine task-status record are included. The original Phase 4 input's SHA-256 is stated in `REPRODUCE.md` and verified by the ZIP script against the unchanged Phase 4 manifest.

Important groups:

| Group | Files and purpose |
|---|---|
| Source access and chronology | `data/processed/source_access_status.csv`, `reference_evidence.csv`: audited custodian/file/licence status and official rainfall/flood context. |
| JRC evidence | `data/raw/phase5_jrc_waterclass_2014_2017_pilot.tif`: actual four-band export; `data/processed/jrc_composite_state_pilot.tif`: derived conservative water-history states; `jrc_ee_console_transcription.json`: independently executed EE counts; `results/earth_engine_jrc_task.json`: task/source snapshot. |
| Numerical/source QA | `results/phase4_water_valid_permanent_crosstab.csv`, `reference_and_support_summary.json`, `reference_candidate_overlap.csv`, `jrc_annual_class_counts.csv`, `jrc_composite_state_counts.csv`, `jrc_annual_export_status.json`, `duration_viewer_reference.json`. No accuracy or affected-area output is present. |
| Figures | `figures/phase5_support_reference_qa.png`/`.svg`: count-band support and reference-pair disagreement; `phase5_jrc_annual_classes.png`/`.svg`: actual annual water-history classes. Neither is a validated flood map. |
| Executable source | `scripts/audit_reference_and_jrc.py`, `check_ee_console_transcription.py`, `check_duration_viewer.py`, `plot_reference_qa.py`, `plot_jrc_annual_classes.py`, `make_manifest.py`, `make_phase5_zip.py`, and both `gee_jrc_*.js` scripts. |
| Interpretation | `README.md`, `DATA_REQUESTS.md`, `reference_qa.md`, `validation_protocol.md`, `data_dictionary.md`, `methods_and_limitations.md`, `results_phase5.md`, `decision_gate.md`, `REPRODUCE.md`. |

The four-band JRC GeoTIFF has been supplied, checked, hashed and included. The ZIP script refuses unexpected future Phase 5 raw files until their licence is reviewed.
