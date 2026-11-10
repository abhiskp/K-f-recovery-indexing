# Flood mask and label quality assurance

## Current state

**No independently validated flood mask or confusion matrix exists.** The 3 Bhuvan pilot GeoTIFFs are styled RGBA WMS responses, not raw categorical rasters. The source viewer's zoom rectangles cannot establish valid observation coverage. The 16 July and 9 August NRSC products used Sentinel-1, and the 21 August 18Hr product combined Sentinel-1 with Radarsat-2; comparing a Sentinel-1-derived candidate to these would share measurement and interpretation errors. The 21 August 06Hr Radarsat-2 GIS-ready layer reported as sent to KSDMA is a better independent-sensor candidate, subject to its processing provenance and temporal/footprint limits.

## Source checks actually completed

1. Parsed 16 unique Kerala 2018 Bhuvan layer IDs from the public viewer snapshot. Flagged `kl_2018_10_08`: viewer says 09/08/2018; and `kl_2018_21_07_18`: viewer says 21/07/2018-06Hr. Neither mismatch was silently corrected.
2. Requested the same 512 × 512 EPSG:4326 pilot bounding box for 16 July, viewer-labeled 9 August, and 21 August 18Hr, in PNG and GeoTIFF. Checked TIFF signature, 4-channel RGBA structure, EPSG tag, model transform and exact requested bbox. Each image is a **rendering**; white/transparent output is not a confirmed non-flood observation.
3. Tried WMS 1.3 and 1.1.1 `GetCapabilities`; both saved responses contain malformed XML / `TransformerException: Translator error`. Layer metadata, class semantics and coverage therefore remain unresolved from capabilities.
   The viewer-listed 21 August 06Hr Radarsat-2 `GetMap` layer failed for both GeoTIFF and PNG with `ServiceException java.lang.NullPointerException`; no independent-sensor WMS image or raster label was obtained.
4. Screened the complete public GFD v1 event inventory and QC polygons. Zero 2018 event bounding boxes intersect Kerala's broad search rectangle, so no GFD label can be aligned to this case.
5. Ran an authenticated Earth Engine pilot query for all IW/VV Sentinel-1 granules from June 2016 through mid-October 2018 and obtained the full local CSV. Checked all 134 unique records. The 51 granules in 2018 form 27 acquisitions; 24 have two adjacent granules. This corrects the earlier unexecuted mask template's mistaken treatment of two granules as two independent dates. Six matched S1A descending orbit-165 acquisitions were selected for exploratory comparison; their exact IDs and times are in `results/selected_2018_pilot_acquisitions.csv`. Their reference dates precede the first dated NRSC July flood map, but dry status remains unverified.
6. Transcribed NRSC's 21 August 06Hr Radarsat-2 district table: five printed rows total 36,657 ha versus its printed 36,658 ha. The report marks two districts as partly covered and omits districts below 100 ha. The table is a source QA check, not a pixel confusion matrix.
7. Submitted acquisition-level Earth Engine QA and candidate-band exports. The first multiband GeoTIFF export failed because Float64 and Float32 bands were mixed; the corrected script casts all bands to Float32 and its export completed. Both original exported files are now in `data/raw/`. The exact six-row QA CSV matches the independent console transcription for all numerical values and the 134-granule inventory for IDs/orbits. Date-mosaic VV validity is approximately 0.998946–0.998967 and angle means 40.7739–40.7812°.
8. Opened the actual 45-band GeoTIFF with Rasterio 1.4.3. It is 921 × 1111 pixels at 30 m in EPSG:32643, with Float32 bands, named descriptions and LZW compression. The fixed pilot has 1,011,610 pixel centers. The JRC water-history bands have finite values at only 369,590 (36.53%) pilot centers; strict QA support is 238,460 pixels (23.57%) for 9 August and 238,477 (23.57%) for 21 August. The export has **no explicit nodata value**, its GDAL band mask says all pixels are valid even where analytic floats are NaN, and candidate-mask zeros occur outside strict QA. Analysis therefore tests finite values and the explicit QA band; treating all candidate zeros as true negatives would be erroneous.

## Descriptive mask sensitivity on the exported pixels

All rows below use the **unverified** 10/22 June reference and the strict analysis support. The August dates are separate acquisitions. Counts and approximate 30 m pixel areas are candidate classifications, **not verified inundation**. See the complete [sensitivity table](results/sar_candidate_pixel_sensitivity.csv) for late-reference and no-water-exclusion variants.

| Date | VV drop rule | Strict support pixels | Candidate pixels | Share of support | Approx. candidate pixel area |
|---|---:|---:|---:|---:|---:|
| 9 Aug | ≥2 dB | 238,460 | 75,225 | 31.55% | 67.70 km² |
| 9 Aug | ≥3 dB | 238,460 | 60,958 | 25.56% | 54.86 km² |
| 9 Aug | ≥4 dB | 238,460 | 49,509 | 20.76% | 44.56 km² |
| 21 Aug | ≥2 dB | 238,477 | 146,205 | 61.31% | 131.58 km² |
| 21 Aug | ≥3 dB | 238,477 | 128,003 | 53.68% | 115.20 km² |
| 21 Aug | ≥4 dB | 238,477 | 110,722 | 46.43% | 99.65 km² |

At ≥3 dB, changing to the 22 June/4 July reference yields 55,326 versus 120,241 candidate pixels on 9/21 August. Removing the water-history exclusion increases eligible support to about 78.3% of the pilot and gives 100,597 versus 214,081 candidate pixels. These variants have **different denominators**. The large JRC missing area, unverified reference dryness, backscatter responses from non-flood processes and absence of independent labels prevent interpreting these counts as event extent or accuracy.

## Validation protocol once independent geospatial labels arrive

Before scoring, freeze the event time interval and scene selection from acquisition UTC, orbit/pass, angle, polarization, and AOI validity. The 21 August S1A descending acquisition began about 06:10 IST; this is close to the NRSC 06Hr Radarsat-2 product label but **not proof of exact coincidence**. Mask each candidate to the intersection of its pre/event scene footprints and the independent source's **valid surveyed footprint**. Use a time tolerance stated in hours/days; avoid comparing products from different flood stages without a sensitivity check. Report how much paddy and non-paddy area falls inside the evaluated footprint.

At the valid comparison pixels or an appropriate spatial aggregate, report TP, FP, FN, TN; precision, recall, F1, IoU and balanced accuracy, plus evaluated coverage fraction. Compute uncertainty with spatially blocked resampling (not iid pixels) and repeat under positional buffers reflecting label geolocation error. Stratify by open water, backwater margins, settlements, forest and slope. Evaluate the exported 2/3/4 dB candidate thresholds, early (10/22 June) versus late (22 June/4 July) reference mosaics, separate 9 versus 21 August acquisitions, matching-orbit alternatives if available, and permanent-water exclusion. Report the denominator and unknown/missing areas. Do not tune a threshold on held-out labels; reserve geographic blocks or an independent event for final checks.

KSDMA depth points, if obtained, are point samples with their own reporting bias and geolocation error. A positive depth point can test local detection, but unless a sampled negative set and valid sampling frame exist, it cannot yield an unbiased statewide specificity or precision. A PDF map's colored pixels should not be digitized into apparent ground truth without documented cartographic georeferencing and an independent field/sensor provenance assessment.

## Outcome

Confusion metrics: **NA**. Validated flood area: **NA**. Rice area affected: **NA**. Held-out validation: **NA**. These are missing evidence, not zero values.
