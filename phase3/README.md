# Phase 3: seasonal rice observations and 2018 exposure feasibility

**Status: Experiment A executed; Experiment B prepared but not executed; causal recovery and ranking tests remain open.** All new work is under `phase3/`. Phase 2 and the manuscript are unchanged.

Experiment A reconstructs 14 districts × 3 rice harvest seasons × 6 agricultural years (2014–15 through 2019–20) from official Kerala DES tables. It compares 2018–19 and 2019–20 area, production and calculated yield with four earlier years in the *same season*. The [processed panel](data/processed/district_season_rice_2014_2020.csv), [calculated deviations](results/seasonal_deviations.csv), [trajectories](results/district_season_trajectories.csv), [QA findings](results/data_quality_findings.csv) and two vector figures are included.

The later compendium contains material 2019–20 inconsistencies. The contemporaneous annual report supplies all 2019–20 values after its internal district/season/state totals were independently checked. The original 2017–18 report supplies one corrected Idukki winter production cell. These source choices are recorded on each processed row. Read [data_quality.md](data_quality.md) before interpretation.

The [Earth Engine pilot](gee_2018_flood_exposure_UNEXECUTED.js) is a revised Sentinel-1 scene-inventory and candidate change script. It has passed `node --check` only. There is **no Earth Engine execution, flood mask or independently validated exposure measurement** in these outputs.

Start with [results_phase3.md](results_phase3.md), [methods_and_limitations.md](methods_and_limitations.md) and [decision_gate.md](decision_gate.md). [REPRODUCE.md](REPRODUCE.md) has exact local commands. [data_dictionary.md](data_dictionary.md) lists all generated columns. [sources.md](sources.md) records official URLs and printed pages. `results/file_manifest.csv` records SHA-256 checksums.
