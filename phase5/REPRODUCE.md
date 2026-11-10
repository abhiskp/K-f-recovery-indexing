# Reproducing Phase 5

Run from the project root on macOS or Linux. The executed local environment used Python 3.9.6 and the Phase 4 pinned `numpy==2.0.2`, `rasterio==1.4.3`, `matplotlib==3.9.4`; Node.js 26.0.0 checked the Earth Engine script syntax. The core input is the unmodified `phase4/data/raw/phase4_s1_2018_pilot_exploratory_candidate_bands.tif` (SHA-256 `44d794576bd7628dda3b3c6b80f0e939a1bb7bf4af8d4f6ac0f516f6bfd6e89f`). No stochastic procedure is used, so there is no seed. No Phase 2 or 3 experiment is rerun.

```sh
python3 -m venv /tmp/phase5-qa-venv
/tmp/phase5-qa-venv/bin/python -m pip install -r phase4/requirements_raster_qa.txt
/tmp/phase5-qa-venv/bin/python phase5/scripts/audit_reference_and_jrc.py
python3 phase5/scripts/check_ee_console_transcription.py
python3 phase5/scripts/check_duration_viewer.py
MPLCONFIGDIR=/tmp/phase5-matplotlib /tmp/phase5-qa-venv/bin/python phase5/scripts/plot_reference_qa.py
MPLCONFIGDIR=/tmp/phase5-matplotlib /tmp/phase5-qa-venv/bin/python phase5/scripts/plot_jrc_annual_classes.py
node --check phase5/gee_jrc_yearly_audit.js
node --check phase5/gee_jrc_integer_counts.js
python3 phase5/scripts/make_manifest.py
python3 phase5/scripts/make_phase5_zip.py
```

Expected local result: pilot 1,011,610 pixel centers; finite Phase 4 JRC count bands 369,590; missing 642,020; reference median difference −0.2540207 dB and absolute >3 dB at 127,377 cells; strict 3 dB candidate-reference Jaccard 0.6472455 (9 August), 0.7640738 (21 August). The annual GeoTIFF must have four Byte bands, EPSG:32643, transform `[30,0,648060,0,-30,1078200]`, and shape 1111 × 921. All 369,590 finite Phase 4 water-history count cells must match the annual classes. The local pilot includes 370 extra code-255 source-masked cells in each year relative to the independently transcribed Earth Engine polygon reduction (1,011,240 cells); observed codes 0–3 must match exactly. The local composite counts must be 642,043/7,077/242,722/118,764/1,004 for states 0–4. The two figures are deterministic. Check exact hashes in `results/checksums.csv` after the manifest command.

The researcher-supplied `phase5/data/raw/phase5_jrc_waterclass_2014_2017_pilot.tif` is included in the handoff. The audit asserts its exact grid, permitted codes {0,1,2,3,255}, agreement with Phase 4 count bands, and count agreement with Earth Engine. It writes `results/jrc_annual_class_counts.csv`, `results/jrc_composite_state_counts.csv`, `data/processed/jrc_composite_state_pilot.tif` and `results/jrc_annual_export_status.json`. **Read raw bands**: GDAL presents the fourth 2017 waterClass band as alpha in this four-band Byte export. Rasterio `masked=True` would incorrectly suppress 65 class-0 pilot cells from bands 1–3. The script checks this condition. If alignment or count checks fail, the script stops; do not silently resample.

## Earth Engine execution already performed

In the signed-in [Earth Engine Code Editor](https://code.earthengine.google.com/) with an enabled Cloud project, `gee_jrc_yearly_audit.js` was run on 8 November 2026. It queried one JRC YearlyHistory image each for 2014–17 and exported a four-band Byte GeoTIFF named `phase5_jrc_waterclass_2014_2017_pilot` to Drive. Task `GIHCX7SEC7VIJ4XHL6IRMAOQ` **completed**; its exact [source snapshot](https://code.earthengine.google.com/752ddb6dbeffb753bde616587b40f43c) and task status are recorded in `results/earth_engine_jrc_task.json`. Class 0 is source no-data; 255 was assigned to masked source pixels explicitly. The export uses the Phase 4 EPSG:32643 grid transform `[30,0,648060,0,-30,1078200]` and pilot rectangle `[76.35,9.45,76.60,9.75]`. Its first console histograms used Earth Engine's weighted reducer and contained fractional boundary weights; **do not treat them as pixel counts**.

The second executed script, `gee_jrc_integer_counts.js`, used `ee.Reducer.frequencyHistogram().unweighted()` with the same grid to obtain integer *Earth Engine polygon-reduction* counts, saved verbatim in `data/processed/jrc_ee_console_transcription.json`. They are not the exact same denominator as the local Phase 4 raster mask. The source scripts and counts are included for independent re-query. Re-authentication is needed only to repeat Earth Engine queries/exports, not to reproduce the completed local audit. Do not share credentials, tokens or private keys.

## Manual public-source checks

`data/processed/source_access_status.csv` and `reference_evidence.csv` are date-stamped human source screens, not automated downloads. Visit the primary URLs in those files and the cited pages in `DATA_REQUESTS.md`/`reference_qa.md` to recheck them. The direct Bhuvan duration WMS capabilities attempt was blocked by the browser client in this session; the Phase 4 21 August 06Hr WMS GetMap attempts returned a server `NullPointerException`. Neither error establishes a usable label. There are no raw GIS labels to reproduce an accuracy or exposure analysis.
