# Phase 6 experimental results — 10 November 2026

## Source-file audit

| Executed check | Result |
|---|---:|
| Sentinel Asia activation product links | 17: 15 JPEG, 1 PDF, 1 KMZ |
| Downloaded ALOS-2 KMZ internal members | 5; three WGS84 image overlays; zero KML vector geometries |
| ALOS-2 overlay/pilot intersection | none; overlay 11.2461–12.1404° N versus pilot 9.45–9.75° N |
| Tiwari S1 checksum | MD5 `ecb20eb014e3d83dade6ede12e242766`, equals NIH/PMC metadata |
| Tiwari S1 contents | 11 GeoTIFFs; 3,286 daily CHIRPS rows at six sites; one R rainfall plotting script; no validation-point file |
| Tiwari GeoTIFF classes | every raster has positive value 1 and declared NoData 0; no observed negative class |
| IFI inventory / 2018 Kerala-mention rows | 6,876 / 11 |
| IFI 2018 Kerala missingness | 11/11 lack latitude, area affected, displaced; 8/11 lack fatalities |
| IFI district static tables | two 732-row historical/model tables, no event-year key |
| Official notification | 1,260 flood/landslide villages in 13 districts in amended 3 October order; seven entire districts |

The IFI statewide event UEI-IMD-FL-2018-0036 records `08-01-2018` to `30-08-2018` and 30 days, an internal chronology discrepancy. The earlier PDNA references 1,259 villages from the 29 September order; the amended order adds one. These discrepancies remain visible in the saved observations and audit, not corrected by assumption.

## Geospatial same-source screen

On the Phase 4 pilot grid (1,023,231 total cells), Tiwari's water-positive cells count **197,432** on 5 January 2018, **343,430** on 28 July, **361,562** on 9 August and **394,423** on 21 August. The 21 August Tiwari positives intersect **218,573** Phase 4 strict-QA cells, of which **126,941** are Phase 4 candidate-positive (58.0772%). This conditional comparison is **not an accuracy, flood-area, or flood-growth estimate**. The two analyses share Sentinel-1 observations, their water definitions differ, and zero/NoData provides no observed negative/valid footprint. See [the exact grid-aligned table](results/tiwari_phase4_positive_overlap.csv).

## Official notification × rice screen

The [district join](data/processed/notification_rice_join.csv) has 378 rows from the 252-row Phase 3 panel. For the 2018-19 autumn harvest, production percent deviations from 2014-15–2017-18 means average **−65.3911%** in six `all_villages` districts with nonzero baselines and **−15.2396%** in six `some_villages` districts, a **−50.1515 percentage-point** descriptive contrast. Wayanad has a zero autumn baseline and is not in the percent contrast. Group absolute deviations are −42,604.75 and −13,997.50 tonnes. Exact label permutation `p=0.017316` is a descriptive enumeration only because the official categories are nonrandom and nonexchangeable. Leave-one-district-out differences range −57.1707 to −44.1645 pp.

| Autumn metric/comparison | All-villages mean % change | Some-villages mean % change | Difference, pp |
|---|---:|---:|---:|
| Production, 2017-18 placebo vs 2014-15–2016-17 | +5.9603 | −13.2977 | +19.2580 |
| Production, 2018-19 vs 2014-15–2017-18 | −65.3911 | −15.2396 | −50.1515 |
| Harvested area, 2018-19 vs baseline | −5.4945 | −9.7947 | +4.3001 |
| Yield, 2018-19 vs baseline | −59.0573 | −7.2576 | −51.7996 |
| Production, 2019-20 vs baseline | −44.5103 | −18.1902 | −26.3201 |

The pre-event placebo difference warns against treating the groups as parallel controls. The 2019-20 value is confounded by the 2019 flood. The results show district-output disruption associated with an administrative flood/landslide designation, **not measured rice-area exposure, causal flooding effects or recovery time**. Full results and undefined percent cells are in [the contrasts CSV](results/notification_rice_contrasts.csv). The [figure](figures/notification_autumn_rice_screen.svg) shows each usable district.

## Beyond agriculture

The [domain register](data/processed/recovery_source_register.csv) records actual observations and gaps. DES offers additional district-season rice reports after 2019-20, but they are not yet harmonized. The official 2019 biodiversity report is a post-event riparian assessment rather than repeated pre/post measurements. Phase 4's executed availability screen found **0.19% clear-any Landsat pilot coverage in August 2018** and mean VIIRS cloud-free counts **0.113/0.353 per pixel in July/August 2018**; no NDVI, EVI, NDMI or light-recovery trajectory is justified. Kerala's Economic Review 2019 reports that KSEBL met **99.99% of its statewide restoration target by 31 August 2018**, but no district × date service-function panel was obtained. Damage and planned reconstruction expenditure are not observed recovery.

**Completed:** source downloads/checks, raster/CSV audit, same-source positive overlap, district administrative/rice screen, domain audit. **Unavailable/untested:** independently validated event flood area, inundated rice area, matched spatial exposure–recovery observation, recovery duration, causal effect, recovery-adjusted rankings, and held-out ranking improvement.
