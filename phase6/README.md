# Phase 6 — alternative evidence and first district screen

**Status (10 November 2026): spatial exposure–recovery success gate not met.** Phase 6 found a previously unexamined, downloadable Sentinel-1 water-positive GeoTIFF series in Tiwari et al. (2020) S1 and a georeferenced ALOS-2 cartographic overlay. The former overlaps the Phase 4 pilot but lacks a valid observed non-water/scene-footprint layer and shares Sentinel-1 source imagery with the pilot. The latter does not overlap the pilot. Neither supplies independent flood labels. A separate district-level association between the official 2018 flood/landslide village notification and rice production is descriptive, not a flooded-rice or recovery estimate.

## Completed work

- Downloaded and verified the [Sentinel Asia ALOS-2 KMZ](data/raw/sentinel_asia_eos_alos2_20180812.kmz), [Tiwari S1 archive](data/raw/tiwari_pone_0237324_s001.7z) and extracted GeoTIFFs, the three IFI-Impacts v3 CSVs, and the official 3 October 2018 Kerala village notification. MD5 checks agree with the NIH/PMC and Zenodo metadata where published.
- Inspected 11 S1 GeoTIFFs, their coordinate systems, class/nodata values and Phase 4 pilot overlap. Saved [raster inventory](results/tiwari_s1_raster_inventory.csv), [positive-only overlap](results/tiwari_phase4_positive_overlap.csv), and [archive audit](results/tiwari_s1_audit.json). No accuracy or inundation-area estimate was made.
- Screened 11 IFI records that mention Kerala in 2018, including missingness and inconsistent published event chronology. Saved [event screen](data/processed/ifi_2018_kerala_event_screen.csv).
- Transcribed the district-level status of Kerala's flood/landslide village notification and joined it to the Phase 3 252-row seasonal rice panel. Saved [joined observations](data/processed/notification_rice_join.csv), [27 descriptive contrasts](results/notification_rice_contrasts.csv), and [figure](figures/notification_autumn_rice_screen.svg). The Phase 3 panel was read, not edited.
- Audited longitudinal prospects across agriculture, ecology, economic activity and infrastructure in [the source register](data/processed/recovery_source_register.csv).

## Read first

1. [Results](results_phase6.md) — exact numeric findings and their interpretation.
2. [Data access audit](data_access_audit.md) — source-by-source provenance and suitability.
3. [Recovery linkage](recovery_linkage.md) — observational design and executed district screen.
4. [Decision gate](decision_gate.md) — explicit A–E go/no-go decisions.
5. [Reproduction](REPRODUCE.md) — commands, dependencies, and checksums.
6. [Data requests](DATA_REQUESTS.md) — precise unsent requests for missing files and QA.

`data/raw/tiwari_s1/` is an exact extraction of the CC BY supplementary archive; the archive itself is retained for byte-level verification. `data/processed/sentinel_asia_*_visual.png` are extracted cartographic images for inspection, not validated class layers. The original Phases 2–5 were preserved unchanged. No ranking experiment or manuscript conclusion was produced.
