# Phase 6 data access and independence audit

## Sentinel Asia, 2018 activation

The [activation page](https://sentinel-asia.org/EO/2018/article20180809IN.html) lists 17 public products: 15 JPEG maps, one PDF and one KMZ. The HTML listing was saved as `data/raw/sentinel_asia_product_page.html`; the EOS ALOS-2 KMZ was downloaded as `data/raw/sentinel_asia_eos_alos2_20180812.kmz`. The page calls this a Google KMZ product under an 8 August heading, while its file name says 12 August; its embedded ALOS-2 image layer names include **11 August 2018** and **28 July 2018**. The heading is not an acquisition date. Exact UTC, scene ID, sensor footprint and processing QA were not found in the archive.

The verified KMZ contains `doc.kml`, `Layer0.png`, `Layer2.png`, `Layer3.png` and `legend0.png`. The KML has **three WGS84 `GroundOverlay` elements and zero point/line/polygon geometries**. The flood-colored layer is an RGBA PNG (10,000 × 9,566 pixels) with 185,688 nontransparent rendered pixels. Its KML bounding rectangle is 75.988872–76.923673° E, 11.246086–12.140387° N. This rectangle does **not** intersect the Phase 4 pilot (76.35–76.60° E, 9.45–9.75° N). Transparent pixels cannot be called observed non-flood or even sensor coverage. There is no independent QA/negative class, so it is not usable as pixel-label validation of the pilot. It uses ALOS-2, potentially an independent sensor from Sentinel-1, but the public product's observation and interpretation frame is incomplete. See `results/sentinel_asia_kmz_structure.json`.

The other 16 public products are map JPEG/PDF files, not downloadable GIS layers in that listing. [Sentinel Asia's FAQ](https://sentinel-asia.org/faq/Faq.html) discusses data distribution under domestic legislation; explicit redistribution permission for the KMZ has not been confirmed. Keep the raw KMZ in a local research handoff unless that permission is clarified.

## Tiwari et al. (2020), PLOS ONE S1

The [article and S1 link](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0237324) identify a 7z supplement. PLOS's file redirect failed from this environment, but the **public, no-login NIH/PMC cloud service** supplied `pone.0237324.s001.7z`; its MD5 `ecb20eb014e3d83dade6ede12e242766` matches the PMC JSON metadata saved in `data/raw/pmc7437901_metadata.json`. NIH's [AWS access documentation](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) gives the retrieval route. The article and PMC metadata identify CC BY; acknowledge the paper's authors and NLM/PMC for the archive route.

S1 contains **11 GeoTIFFs**, a 3,286-day CSV of CHIRPS rainfall at six named points (2010-01-01 through 2018-12-30), and one R plotting script with an author's local Windows path. There are **no validation-point labels, full Earth Engine processing scripts, Sentinel-1 acquisition IDs/UTC, class key, or valid scene-footprint raster** in S1. All 11 GeoTIFFs have one uint8 band, value **1** on positive water-class pixels and **0 as declared NoData**. Zero is therefore unknown in the supplied files, not an observed negative. The filename dates are 2015-08-13, 2016-08-17, 2017-08-14, 2018-01-05, 04-11, 07-28, 08-09, 08-21, 09-02, 09-14, and 09-26; the exact acquisition UTC is unavailable. Six 2018 rasters are EPSG:4326 with a common 76.165278–77.236519° E, 8.688595–10.305832° N bounding box; some others are EPSG:32642. See `results/tiwari_s1_raster_inventory.csv` for every file's exact CRS, grid, classes and checksum.

The paper says maps are generated from Sentinel-1 VV/Otsu and that reference samples in cloud-obscured Sentinel-2 regions were selected using Sentinel-1 itself. Its optical images are 10 and 20 August versus SAR on 9 and 21 August. Thus the published map is **same-sensor evidence**, and parts of its reported validation are measurement-dependent. Its 21 August positive mask overlaps our pilot, but it cannot independently validate our Sentinel-1 threshold mask or supply precision/specificity without surveyed non-flood cells. The abstract gives 94.3/94.1% overall accuracy, whereas the body gives 94.73/94.71%; neither number is adopted for our pilot. The source maps classify water, not flood-specific new water or rice-area exposure. See the [methods and validation text](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0237324).

## India Flood Inventory–Impacts v3

All three CSVs from [Zenodo record 11275211](https://zenodo.org/records/11275211) were downloaded and matched to the record's MD5 checksums. The Zenodo metadata gives **CC BY 4.0**. The event inventory has 6,876 rows; 11 records mention Kerala with a 2018 start date. All 11 lack latitude and area affected, all 11 lack displaced counts and eight lack fatality counts. Event UEI-IMD-FL-2018-0036 reports `08-01-2018` to `30-08-2018` yet 30 days; these published fields cannot all be correct. They were retained verbatim and flagged rather than silently repaired. Two major statewide records name all 14 districts, so they do not differentiate event exposure within Kerala.

The two 732-row district CSVs have **no event year or 2018 acquisition date**. Their flooded-area/duration and impact values are historical/model aggregates, not 2018 district measurements. The 14 Kerala rows were joined by name to the Phase 3 district list only for source auditing; they were not used as 2018 exposure or recovery labels. CSVs have no projected geometry or valid event footprint.

## Kerala official village order and KSDMA

The downloaded [G.O.(P) No.6/2018/DMD, 3 October 2018](https://keralaagriculture.gov.in/wp-content/uploads/2021/07/GO-Flood-Notification-2018-3102018_1-additional-VIllage-1.pdf) amends the 29 September order from 1,259 to **1,260 flood/landslide-affected villages in 13 districts** after adding Peruvayal. Seven districts have all villages listed: Alappuzha, Ernakulam, Idukki, Kottayam, Pathanamthitta, Thrissur, Wayanad. Six have some villages listed; Kasaragod is not listed in the annexure, which is **not a measured zero flood exposure**. The order gives names and administrative status, not GIS polygons, satellite coverage, water depth, crop footprint, duration or restoration trajectory. A [KSDMA/UNDP PDNA](https://sdma.kerala.gov.in/wp-content/uploads/2019/03/PDNA-report-FINAL-FEB-2019_compressed.pdf) quotes the earlier 1,259 figure; the date/version discrepancy is documented.

[KSDMA reports](https://sdma.kerala.gov.in/crowd-sourcing-flood-2018/) about 13,000 crowdsourced depth points, but no licensed downloadable geocoded point table with collection times and selection/QA frame was obtained. The same remains true of the underlying NRSC/KSDMA RADARSAT-2 21 August raster, its 11–21 August duration GIS layer, and a season-specific 2018 paddy layer from the Phase 5 audit. Access requests are in `DATA_REQUESTS.md`. Official source documents here have no explicit redistribution licence identified; local research possession is not a grant for public raw-file redistribution.

## Suitability summary

| Source | Independent from Phase 4 Sentinel-1? | Pilot overlap | Surveyed negatives/valid footprint | 2018 rice exposure use |
|---|---|---:|---:|---:|
| Sentinel Asia ALOS-2 KMZ | Sensor potentially yes; processing dependence unclear | No | No | No |
| Tiwari S1 GeoTIFFs | No; Sentinel-1 and partly Sentinel-1-derived reference | Yes | No | No |
| IFI event CSV | Source partly independent but district event resolution inadequate | Names only | No | No |
| Official village notification | Administrative source independent of imagery | District names | Not a satellite observation | Broad descriptive grouping only |
| KSDMA/NRSC protected GIS | Potentially yes | Unknown until received | Unknown | Pending access and QA |
