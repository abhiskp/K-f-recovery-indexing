# Reproduction and environment

Run from the project root, using the supplied raw snapshots and Earth Engine exports. The executed local environment was Python **3.9.6**, NumPy **2.0.2**, Rasterio **1.4.3**, Matplotlib **3.9.4**, and Node **26.0.0** on macOS arm64. The source screen and chronology SVG need only Python 3.9+ standard library; the raster audit and scientific figure use the pinned requirements below. JavaScript syntax checks need Node.js. Earth Engine re-exports require a signed-in registered account and enabled Cloud project. No random numbers are used, so there is no seed.

```sh
python3 phase4/scripts/screen_public_sources.py
python3 phase4/scripts/check_domain_feasibility.py
python3 phase4/scripts/check_nrsc_report_table.py
python3 phase4/scripts/review_gee_inventory.py
python3 phase4/scripts/select_pilot_acquisitions.py
python3 phase4/scripts/check_selected_qa.py
python3 phase4/scripts/make_chronology_figure.py
python3 -m venv /tmp/phase4-qa-venv
/tmp/phase4-qa-venv/bin/python -m pip install -r phase4/requirements_raster_qa.txt
/tmp/phase4-qa-venv/bin/python phase4/scripts/validate_gee_exports.py
MPLCONFIGDIR=/tmp/phase4-matplotlib /tmp/phase4-qa-venv/bin/python phase4/scripts/plot_sar_qa.py
python3 phase4/scripts/make_manifest.py
node --check phase4/gee_scene_inventory_UNEXECUTED.js
node --check phase4/gee_scene_inventory_EXECUTED.js
node --check phase4/gee_candidate_masks_UNEXECUTED.js
node --check phase4/gee_candidate_masks_EXECUTED.js
node --check phase4/gee_other_domain_feasibility.js
```

Expected screen summary: 913 GFD objects/QC records; 32 events beginning in 2018, 12 overlapping July–September; zero candidate bounding boxes intersecting the Kerala search rectangle; 16 Bhuvan WMS layers; 14 candidate district polygons; 3 pilot WMS GeoTIFFs. One date and one hour discrepancy are flagged. The NRSC table check reproduces 36,657 ha as the five-row sum versus 36,658 ha printed total. The exact six-row QA CSV matches the console transcription; the raster audit checks 45 bands, 30 m EPSG:32643, candidate-mask nesting and explicit QA denominators. `results/checksums.csv` gives SHA-256 hashes for every Phase 4 file except itself and the generated manifest.

## Earth Engine task already executed

The pilot area is lon/lat `[76.35, 9.45, 76.60, 9.75]`. The Code Editor ran the exact local `gee_scene_inventory_EXECUTED.js` on 6 November 2026 with `COPERNICUS/S1_GRD`, `filterBounds`, `filterDate('2016-06-01','2018-10-15')` (exclusive end), `instrumentMode == IW`, `VV` polarization, and UTC sorting. For every granule, it computed scene ID, UTC acquisition, platform, absolute/relative orbit, pass, mode, polarizations, resolution, AOI footprint fraction, approximate valid VV fraction at 30 m, and approximate incidence angle min/max/mean at 1000 m. The query returned **134 granules**. `Export.table.toDrive` finished under task ID `LMCGG75TSBJP6WZWRKV3MTZ2`, task name `phase4_kerala_2016_2018_s1_pilot_full_scene_inventory`. The full downloaded CSV is included at `data/raw/phase4_kerala_2016_2018_s1_pilot_full_scene_inventory.csv`. [Earth Engine's saved source snapshot](https://code.earthengine.google.com/29968f090b29abe9c993f6cf84dc0223) also records the executed editor code. The annotated `gee_scene_inventory_UNEXECUTED.js` has additional explanatory output/map display and was not itself run.

To repeat it, sign into a registered Earth Engine account and an enabled Cloud project at the [Code Editor](https://code.earthengine.google.com/). Paste and run `gee_scene_inventory_EXECUTED.js`; open **Tasks**, start its table export, and download the CSV from your Drive into `phase4/data/raw/`. The supplied CSV allows independent local checking without re-authentication. Do not share credentials, tokens, or private keys.

The local inventory review finds **51 2018 granules in 27 acquisitions**. It writes a granule-level scene screen and an acquisition-level grouping table. The fixed six-date selection script asserts two adjacent granules, S1A descending relative orbit 165, and near-full summed validity for each date, then writes `results/selected_2018_pilot_acquisitions.csv`. Summed granule fractions are **not union coverage**. Dry status remains unverified, even for the 10/22 June and 4 July reference dates. The 16 July observation is a chronology check, never a baseline. The 9 and 21 August event dates are analyzed separately.

On 7 November 2026, the Code Editor ran `gee_candidate_masks_INITIAL_FAILED.js`: its six-row `acquisitionQA` table export completed under task `3RLMJCJNATOXPRLQ4MPHD3KI`; the GeoTIFF task `EXUF6T6FBLQX23OGF4E2USUJ` failed with “Exported bands must have compatible data types; found inconsistent types: Float64 and Float32.” The corrected `gee_candidate_masks_EXECUTED.js` casts the multiband output to float and suppresses the already-completed duplicate table export. Its GeoTIFF task `XZNENJ6GNT6VN5W7X6F2FKMB` **completed** in approximately two minutes. The original QA CSV and GeoTIFF were downloaded to `phase4/data/raw/` on 8 November. The six date-level coverage/angle QA values were separately transcribed from the computed Code Editor table to `results/gee_selected_acquisition_qa_console_transcription.csv`; `validate_gee_exports.py` confirms exact numerical agreement with the downloaded CSV and scene/orbit IDs against the inventory. `gee_candidate_masks_UNEXECUTED.js` is the corrected template with `START_EXPORTS=false`; set it true in a saved executed copy to reproduce both exports. The exploratory thresholds are fixed 2/3/4 dB sensitivity checks, not fitted classifiers. **No candidate is a validated flood extent.**

The local raster audit reprojects the fixed pilot rectangle to the GeoTIFF's CRS and counts 30 m pixel centers inside it. It checks each candidate is binary, nested across 2/3/4 dB thresholds and wholly inside its QA support. The output `sar_candidate_pixel_sensitivity.csv` uses each variant's own support denominator; approximate candidate pixel area is count × 900 m² and is **not measured inundation**. Float NaNs in analytic bands are treated as missing even though the GeoTIFF's GDAL mask marks all pixels valid. Candidate zeros outside QA support are never counted as negatives. `sar_band_diagnostics.csv` reports within-pilot finite-value distributions, and `plot_sar_qa.py` produces the PNG/PDF directly from executed result tables.

The exact local `gee_other_domain_feasibility.js` was also run in the Code Editor on 6 November 2026. Expand its 8-feature result table to reproduce `results/pilot_2017_2018_optical_viirs_feasibility.csv`; the CSV was transcribed from that computed table with full displayed numeric precision, then checked by `check_domain_feasibility.py`. It uses the same pilot AOI and June–September of 2017 and 2018. Landsat 8 L2 QA_PIXEL bits 0–5 must all be zero for the clear-any fraction; Sentinel-2 SR SCL classes 4/5/6 are accepted; Sentinel-2 TOA QA60 opaque-cloud/cirrus bits 10/11 must both be zero for a **cloud-only upper bound**, not a full clear-sky mask. Monthly pixels count as available if at least one scene passes. VIIRS `cf_cvg` and `avg_rad` are mean values at approximately 500 m; `cf_cvg` is the cloud-free source observation count per pixel. These are data availability metrics only. No random seed is used.

## Raw public-source snapshots

- GFD QC CSV: `https://raw.githubusercontent.com/cloudtostreet/MODIS_GlobalFloodDatabase/main/data/gfd_qcdatabase_2019_08_01.csv`.
- GFD object listing: `https://storage.googleapis.com/storage/v1/b/gfd_v1_4/o?maxResults=1000&fields=items(name,size,md5Hash,mediaLink),nextPageToken`.
- Bhuvan viewer HTML: `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php?uname=empty`.
- District GeoJSON: `https://raw.githubusercontent.com/opendatakerala/kl_district/main/Kerala_districts.geojson` (OpenStreetMap/ODbL, attribution required).
- WMS pilot requests use `SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG:4326&BBOX=76.35,9.45,76.60,9.75&WIDTH=512&HEIGHT=512&TRANSPARENT=TRUE` at `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms`. Use `LAYERS=kl_2018_16_07`, `kl_2018_10_08`, or `kl_2018_21_08_18` and `FORMAT=image/geotiff` or `image/png`. The TIFF metadata/extent is checked by the screening script. These are styled maps, not raw labels. The listed `kl_2018_21_08_06` layer returned `ServiceException java.lang.NullPointerException` for **both** formats; its GeoTIFF error response is preserved as `data/raw/bhuvan_2018_08_21_06_wms_exception.xml`.

Two WMS `GetCapabilities` responses are retained because the service returned malformed XML with `javax.xml.transform.TransformerException: Translator error` appended; they are not usable layer metadata. The small GFD listing probe is retained as an access diagnostic, whereas the complete listing is used for analysis.

No held-out evaluation was executable: independent labels, verified per-pixel footprints, 2018 paddy polygons and an exposure-to-outcome join are absent. Re-running Phase 3 is unnecessary for the Phase 4 source screen; Phase 3's fixed rice panel is referenced in [methods_and_limitations.md](methods_and_limitations.md).
