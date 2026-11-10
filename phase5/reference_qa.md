# Reference-scene and JRC water-history audit

## Scene chronology and independent context

The six matched Phase 4 S1A descending relative-orbit-165 acquisitions, including reference candidates on 10/22 June and 4 July 2018, are documented with exact granule IDs and UTC/IST starts in `../phase4/results/selected_2018_pilot_acquisitions.csv`. No reference has a site-matched independent dry observation. The [IMD 2018 monsoon assessment](https://sdma.kerala.gov.in/wp-content/uploads/2020/08/IMD-Monsoon-Extreme-Rainfall-2018.pdf) reports June active spells peaking around 14–20 June and cumulative above-normal rainfall from the week ending 11 June. Thus 22 June follows an active rain spell; 10 June precedes its peak but is not proven dry. The 4 July scene precedes the [NRSC 16 July inundation observation](https://ndem.nrsc.gov.in/documents/Disaster_Document/2018/KL/klheavyrains50dsc16072018/klheavyrains50dsc16072018_map.pdf), yet that later observation does not prove 4 July was unflooded. CWC's [August 2018 report](https://sdma.kerala.gov.in/wp-content/uploads/2020/08/CWC-Report-on-Kerala-Floods.pdf) records statewide June rainfall 749.6 mm against 649.8 mm normal; its broad statement of flood onset toward end July conflicts with the dated NRSC 16 July map in part of central Kerala. Source scope and location must be respected. `data/processed/reference_evidence.csv` gives one row per candidate date.

This context establishes *wet-season uncertainty*, not an inundation classification at 06:10 IST in the pilot. We did not obtain daily pilot gauge/river-stage observations or verified dated maps for 10 June, 22 June, or 4 July.

## Direct SAR reference-pair comparison from the Phase 4 raster

The Phase 4 export contains the median of 10/22 June and the median of 22 June/4 July, not the three individual backscatter bands. On 1,011,610 pilot pixel centers, later minus earlier pair has median **−0.254 dB**, fifth percentile **−3.957 dB**, and 95th percentile **+2.514 dB**. **127,377 cells (12.59%)** differ by more than 3 dB in absolute value. Because the two pairs share 22 June, this is a damped indicator of reference instability; it cannot identify which date or mechanism changed. Crop stage, rain-wet soil, wind-roughened water, speckle/processing, vegetation and terrain can all alter VV backscatter. Matched orbit and near-identical mean angle address only part of geometric variation.

For the *same* strict valid-support pixels and fixed 3 dB rule, the early versus late reference-pair candidate Jaccard is **0.647** on 9 August and **0.764** on 21 August. There are **24,902** and **33,200** pixels, respectively, classified positive by just one reference pair. These are classification disagreements, not flood-change observations or validation errors. Full two-by-two counts are in `results/reference_candidate_overlap.csv`, reproduced by `scripts/audit_reference_and_jrc.py`. The original 2/3/4 dB Phase 4 masks are preserved untouched. No threshold was fitted to labels.

## JRC annual classes and denominator

The [JRC YearlyHistory catalog](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_YearlyHistory) defines `waterClass`: **0 no data, 1 not water, 2 seasonal water, 3 permanent water** (source attribution: EC JRC/Google; Pekel et al., *Nature* 2016, DOI 10.1038/nature20584). The Phase 4 45-band export contains 2014–17 *counts of years with class >0* and *counts of permanent years*, but not the individual 1-versus-2 classes. Its count bands are finite for **369,590 / 1,011,610 = 36.53%** of pilot centers and absent for **642,020 = 63.47%**. The original 9/21 August strict mask supports **238,460 / 238,477 cells**, each about **23.57%** of this local pilot denominator. Unknown water history cannot be assigned to non-water.

An authenticated Earth Engine Code Editor query executed `gee_jrc_integer_counts.js` on 8 November 2026. Its unweighted pixel-center reductions on the specified UTM grid yield the following class counts. `255` is source masked after explicit unmasking, distinct from source class 0. The Earth Engine polygon-reduction denominator is **1,011,240**, **370 fewer than Phase 4's Rasterio pilot mask**. The downloaded GeoTIFF matches all EE class-0/1/2/3 counts exactly; all 370 additional local cells are source-masked 255. The two AOI selection conventions therefore have different explicit denominators but no discrepancy in observed class counts. The exact console transcription and definitions are in `data/processed/jrc_ee_console_transcription.json`.

| Year | 0 no data | 1 not water | 2 seasonal | 3 permanent | 255 source masked |
|---|---:|---:|---:|---:|---:|
| 2014 | 507 | 30,392 | 214,614 | 123,251 | 642,476 |
| 2015 | 22 | 44,572 | 154,525 | 170,471 | 641,650 |
| 2016 | 35 | 39,085 | 213,053 | 117,417 | 641,650 |
| 2017 | 65 | 36,404 | 214,642 | 118,479 | 641,650 |

The local composite has **642,043** cells with fewer than three source-valid years; **7,077** classed not-water in all four years; **242,722** with observed seasonal water and at least three valid years but fewer than three permanent years; **118,764** with permanent water in at least three years; and **1,004** other mixed known histories. The EE insufficient-data count is 641,673, exactly 370 lower; every other composite count agrees. These groups are descriptive JRC states, **not independent 2018 flood labels**. A stable not-water screen would keep less than 1% of the local pilot and could preferentially omit rice paddies, which may be seasonally wet. It is not adopted as the agricultural analysis mask.

The four-band annual-class GeoTIFF was downloaded to `data/raw/` on 9 November. `scripts/audit_reference_and_jrc.py` verified **exact EPSG:32643, 30 m transform, 1111 × 921 shape, and all 369,590 Phase 4 finite count-band cells**. It wrote `results/jrc_annual_class_counts.csv`, `results/jrc_composite_state_counts.csv` and `data/processed/jrc_composite_state_pilot.tif`. The [annual source-class map](figures/phase5_jrc_annual_classes.png) shows each year separately; the earlier [support/reference figure](figures/phase5_support_reference_qa.png) still maps count-band availability and unvalidated SAR disagreement.

The export's fourth Byte band is **2017 `waterClass`**, but GDAL tags a four-band Byte GeoTIFF as RGBA. As a result, Rasterio `read_masks()`/`masked=True` interprets 2017 class-0 values as transparent and would suppress **65 valid pilot cells** from bands 1–3. The audit reads **raw** band values, checks this exact condition, and reproduces the independent EE class counts. This is a file interpretation issue, not evidence of 2018 flooding.

## Mask treatment fixed before label access

- Primary exploratory comparison remains the Phase 4 ≥3 dB VV-drop plus event VV <−15 dB rule, matched descending orbit, slope <5°, >=3/4 JRC valid years, and <3 permanent years. The 2 and 4 dB rules and alternate June/July pair are predeclared sensitivity checks, not tuned results.
- Any future annual-class stratum report must keep source class 0 and 255 as unknown; show class 1, 2 and 3 separately; and report valid-support counts by class and acquisition date. Seasonal water is not automatically either permanent or dry land.
- The no-water-exclusion Phase 4 variant yielded 39,639 (9 August) and 86,078 (21 August) additional candidate positives **outside strict support**. These are not added to flood area. Broadening eligibility without verified water history is an uncertainty scenario only.
- No JRC category substitutes for a verified 2018 paddy/rice map or independent flood label.

The [figure](figures/phase5_support_reference_qa.png) makes the spatial concentration of missing support and reference disagreement visible while labeling the SAR output unvalidated.
