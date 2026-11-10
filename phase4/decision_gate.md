# Decision gate and next evidence

**Current decision (8 November 2026): NO-GO for recovery or ranking claims.**

## Established through executed work

1. Official evidence fixes a 16 July 2018 flood observation and a sequence of July/August acquisitions. The former Phase 3 July-versus-August scene assumption is invalid without scene-level review.
2. Earth Engine ran an authenticated pilot Sentinel-1 inventory: 134 IW/VV granules from June 2016 to mid-October 2018; the full metadata CSV is local and checked. The 51 2018 granules form 27 acquisitions. Six S1A descending orbit-165 acquisitions were selected for exploratory comparisons and their exact times, IDs, orbit and approximate coverage recorded. None is labeled verified dry; adjacent granules are mosaicked before comparing dates.
3. Public Bhuvan exposes 16 Kerala 2018 WMS views; three styled pilot views were downloaded and their TIFF georeferencing checked. One date and one hour mismatch are logged. They do not provide raw per-pixel valid-coverage labels.
4. The full public GFD v1 catalog contains no 2018 event with a QC polygon bbox intersecting the broad Kerala rectangle. It is unsuitable as this event's validation source.
5. Fourteen OSM-derived district polygons are available as provisional geometry only. No verified 2018 georeferenced rice extent was located.
6. An independent-domain availability query shows poor monsoon optical/VIIRS support in the pilot: zero Sentinel-2 SR scenes in the eight screened months, no July 2018 Landsat scene, 0.19% Landsat clear-any August coverage, and VIIRS mean cloud-free counts below 0.4 per pixel in July/August 2018. Sentinel-2 TOA exists but its QA60 cloud-only screen is insufficient for a recovery map.
7. The NRSC 21 August 06Hr district area table has a 1 ha arithmetic discrepancy between row sum and printed total, and two districts have partial satellite coverage. It cannot substitute for a geospatial valid-footprint layer.
8. The same date's Bhuvan Radarsat-2 WMS layer is listed, but `GetMap` failed for both requested image formats with `java.lang.NullPointerException`. The public service currently supplies no usable independent 06Hr geospatial label.
9. The researcher supplied the exact six-row Earth Engine QA CSV and 45-band GeoTIFF. All six CSV rows match the console transcription and full scene IDs. Local raster checks confirm 30 m EPSG:32643, named bands and threshold nesting. However, JRC 2014–17 history is finite for only 36.53% of pilot pixels; strict QA support is 23.57%. Candidate-mask zeros include unsupported pixels, and no independent pixel label exists. The actual candidate-count table is descriptive only.

## Unmet success gate

An observation-level link between **real, independently checked 2018 flood exposure** and one or more **measured recovery outcomes** is absent. An exploratory SAR change export alone does not satisfy independent validation. No candidate mask was validated; no exposed rice-area denominator or exposed/less-exposed seasonal panel exists. Accordingly no recovery duration, cumulative flood deficit, causal departure, held-out predictive benefit or recovery-adjusted ranking is reported.

## Exact next access/data steps

1. **Reference-state verification:** inspect the 10/22 June and 4 July pilot acquisitions against independent dated evidence of inundation, rainfall, water levels and land-cover change. They precede the first official 16 July flood map but are not verified dry. Resolve JRC pre-event water-history gaps or report a spatially restricted estimand; do not treat missing water-history pixels as known non-water.
2. **KSDMA/NRSC:** obtain the 21 August 2018 06Hr **Radarsat-2 GIS-ready flood layer** mentioned in [NRSC's report](https://ndem.nrsc.gov.in/documents/Disaster_Document/2018/KL/klflood50dsc21082018/klflood50dsc21082018_report.pdf), plus valid acquisition footprint, exact source time/ID, class key, positional/error metadata and research licence. Also request KSDMA's 2018 crowd-sourced depth records as a dated georeferenced table with sampling and quality fields. A web map or PDF alone is insufficient.
3. **KSREC/KSLUB or other data custodian:** obtain a 2018 paddy/rice crop-area layer with season/crop classification, reference date, validation and licence. Verify district/block boundaries as of 2018.
4. After validation, measure flood-exposed rice hectares with coverage and uncertainty; only then build a seasonal exposed/less-exposed outcome comparison using the Phase 3 panel and any harmonized longer DES series. Analyze other domains separately.

A retrospective prioritisation analysis and a prospective ranking evaluation are later gates. Neither should be inferred from a ranking that happens to change.
