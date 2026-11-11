# Phase 6 file manifest

The complete per-file byte lengths and SHA-256 hashes (including every extracted S1 GeoTIFF, script, report, figure and the read-only Phase 3 rice input) are in [results/checksums.csv](results/checksums.csv). `scripts/checksums.py verify` checks them. This document and the checksum file are excluded from the hash list to avoid a recursive digest.

| Files | Purpose |
|---|---|
| `data/raw/sentinel_asia_product_page.html`, `sentinel_asia_eos_alos2_20180812.kmz` | Exact public listing and georeferenced ALOS-2 visual source; no verified pilot label. |
| `data/raw/tiwari_pone_0237324_s001.7z`, `pmc7437901_metadata.json`, `europepmc_7437901_fulltext.xml`, `tiwari_s1/` | CC BY paper supplement, NIH checksum/licence metadata, article XML and exact extracted 11 rasters/rainfall/R script. |
| `data/raw/ifi_*.csv`, `zenodo_11275211_metadata.json` | Exact IFI v3 event and district tables with published checksum metadata. |
| `data/raw/kerala_go_flood_notification_2018_20181003.pdf` | Official amended village order transcribed at district level. |
| `data/processed/sentinel_asia_*_visual.png` | KMZ image/legend extracted for visual QA, not class validation. |
| `data/processed/ifi_2018_kerala_event_screen.csv`, `ifi_kerala_historical_district_metrics.csv` | Kerala event screen and deliberately labelled historical static district data. |
| `data/processed/official_district_notification_status.csv`, `notification_rice_join.csv`, `recovery_source_register.csv` | Administrative district categories, 378 row rice join, cross-domain longitudinal availability audit. |
| `results/raw_file_provenance.csv`, `ifi_source_audit.json`, `sentinel_asia_kmz_structure.json` | Source URLs, checksums and archive/IFI inspection results. |
| `results/tiwari_s1_raster_inventory.csv`, `tiwari_phase4_positive_overlap.csv`, `tiwari_s1_audit.json` | Exact raster metadata/counts and same-source positive-only pilot overlap. |
| `results/notification_rice_contrasts.csv`, `notification_rice_summary.json` | 27 descriptive district contrasts, placebo and later-year results. |
| `figures/notification_autumn_rice_screen.svg`, `.png` | Static chart from the saved district join. |
| `scripts/audit_public_sources.py`, `audit_tiwari_s1.py`, `notification_rice_screen.py`, `checksums.py` | Executed reproducible scripts; no credentials or personal paths except project-relative resolution. |
| `README.md`, `results_phase6.md`, `data_access_audit.md`, `recovery_linkage.md`, `decision_gate.md`, `methods_and_limitations.md`, `data_dictionary.md`, `DATA_REQUESTS.md`, `REPRODUCE.md` | Methods, evidence, limitations, source access and exact rerun instructions. |

**External read-only inputs:** `../phase3/data/processed/district_season_rice_2014_2020.csv` and `../phase4/data/raw/phase4_s1_2018_pilot_exploratory_candidate_bands.tif` are required for the executed join and overlap respectively. Their original contents were not modified. The Phase 3 input is hashed in the checksum CSV; the Phase 4 GeoTIFF is hashed there as well.
