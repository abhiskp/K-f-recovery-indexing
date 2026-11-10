# Phase 5 executed results (8–9 November 2026)

## Public-source access screen

The [NRSC 21 August letter](https://ndem.nrsc.gov.in/documents/Disaster_Document/2018/KL/klflood50dsc21082018/klflood50dsc21082018_report.pdf) explicitly says the 06Hr RADARSAT-2 GIS-ready inundation layer was transmitted to KSDMA. No such source file, class key, valid surveyed footprint, exact scene UTC or licence is local. The prior Phase 4 attempt to fetch its public Bhuvan WMS view returned `java.lang.NullPointerException` in both PNG and GeoTIFF, while successful other WMS views were only styled RGBA imagery.

The [NRSC duration PDF](https://ndem.nrsc.gov.in/documents/Disaster_Document/2018/KL/klflood50dsc11_21082018_cumulative/klflood50dsc11_21082018_cumulative_map.pdf) identifies Map ID **2018/14**, issued 22 August, with RADARSAT-2 acquisitions on **11, 14, 18 and 21 August** and classes **0–3, 4–6, 7–9, >10 days**. It names 6 March 2018 ResourceSat-2 AWiFS pre-flood imagery, NRC land-cover data, and International Charter **Call ID-667**. It says rapid mapping and no ground verification. The Bhuvan viewer exposes a styled layer `aggregate_flood_kerala_2018` through a MapServer WMS; an attempted direct capabilities request in this session was blocked by the browser client, so service availability cannot be established from that attempt. Neither PDF nor styled viewer provides class/footprint files or duration-estimation method. Four discrete acquisition dates do not themselves prove continuous flood duration at a location. This product is a hazard-duration lead, not post-flood recovery.

KSLUB lists a [wetland/paddy-land map](https://kslub.kerala.gov.in/en/faq/) and says to request data by letter with possible payment; its [resource page](https://kslub.kerala.gov.in/?lang=en&page_id=338) describes a 1:12,500-scale map. No public file was shown to be a 2018 *cultivated rice-by-season* layer. KSREC's listed paddy/wetland project begins in 2020, so it cannot establish pre-August-2018 crop extent without provenance. KSDMA's [depth page](https://sdma.kerala.gov.in/crowd-sourcing-flood-2018/) says about **13,000** points were gathered within two months and links a PDF map, not the dated point table. The Phase 4 OSM district polygons are candidate boundaries only. The exact statuses and missing fields are in `data/processed/source_access_status.csv`; drafted requests are in `DATA_REQUESTS.md`. No messages have been sent.

## Reference and water-history QA

| Executed check | Result | Interpretation |
|---|---:|---|
| Phase 4 pilot pixel centers | 1,011,610 | Local Rasterio AOI denominator |
| JRC 2014–17 water-count bands finite | 369,590 (36.53%) | 642,020 are missing/NaN, not non-water |
| Strict 9 August candidate support | 238,460 (23.57%) | Only this support underlies original strict counts |
| Strict 21 August candidate support | 238,477 (23.57%) | Separate acquisition/denominator |
| Early versus late reference-pair absolute difference >3 dB | 127,377 (12.59%) | Reflects reference instability, not verified flooding |
| 9 August early/late 3 dB candidate Jaccard | 0.647 | 24,902 discordant supported cells |
| 21 August early/late 3 dB candidate Jaccard | 0.764 | 33,200 discordant supported cells |

The independent [IMD June-rain account](https://sdma.kerala.gov.in/wp-content/uploads/2020/08/IMD-Monsoon-Extreme-Rainfall-2018.pdf) gives active rain spells around 14–20 June and above-normal cumulative rainfall from week ending 11 June, but no pilot-specific dry confirmation for 10/22 June or 4 July. All remain **unverified**. `reference_qa.md` and `results/reference_candidate_overlap.csv` document the calculation.

Earth Engine's executed, **unweighted** annual JRC class reductions use a **1,011,240**-cell AOI denominator. The source 2015 count is 22 class-0, 44,572 class-1 not-water, 154,525 class-2 seasonal, 170,471 class-3 permanent, and 641,650 source-masked. The downloaded annual-class GeoTIFF was checked on the exact Phase 4 EPSG:32643, 30 m, 1111 × 921 grid. On the local **1,011,610**-cell pilot mask, all annual codes 0–3 match EE counts exactly and each year has **370 additional code-255 source-masked cells**. Phase 4's finite water-history counts agree with the annual raster on **369,590/369,590** cells. The local conservative water-history groups are **642,043 insufficient data**, **7,077 all-four-years not-water**, **242,722 seasonal observed**, **118,764 permanent in at least three years**, and **1,004 other known histories**. These are pre-2018 water-history descriptors, not flood labels. Exact counts are in `results/jrc_annual_class_counts.csv` and `results/jrc_composite_state_counts.csv`.

The four-band Byte GeoTIFF is tagged as RGBA by GDAL, making the 2017 class band look like alpha. Raw values show **65 genuine 2017 class-0 pilot cells**; reading bands 1–3 with an automatic mask would hide them. The local audit reads raw values and checks this artifact. [Annual class figure](figures/phase5_jrc_annual_classes.png) maps all four years with class 0 and source-masked 255 separated.

## Validation and recovery result status

| Measure | Status | Reason |
|---|---|---|
| Independent confusion matrix, precision, recall, IoU | NA — not executed | No licensed geospatial label, class key, true-negative frame or surveyed footprint |
| Validated 9/21 August flood extent and duration | NA — not executed | SAR change candidates unvalidated; duration PDF not data |
| Flood-exposed 2018 paddy/rice hectares | NA — not executed | No credible flood layer or dated cultivated-rice map |
| Flood-associated seasonal rice trajectory | NA — not executed | Exposure/outcome join and controls absent |
| Recovery duration, deficit, ranking benefit | NA — not executed | Prior gates unmet |

The Phase 3 252-row official rice panel remains available in `../phase3/`, but it cannot be used to infer pixel-level recovery or flood attribution from the current Phase 5 evidence. The [QA figure](figures/phase5_support_reference_qa.png) is a support/reference diagnostic, not a flood map.
