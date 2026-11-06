# Kerala recovery-priority research: exploratory pilot (21 October 2026)

## What is actually measured

* Agricultural production for 14 Kerala districts, three crops, four annual periods: 168 official report values.
* Published district vulnerability scores from Kendagannaswamy et al (2026), attached Meenachil.pdf, Table 9.
* Sensitivity experiments involving **hypothetical weighted combinations**, descriptive pseudo-holdout, and rank changes.

## NOT yet measured / must NOT claim

* No recovery durations or flood-attributable loss estimates. Annual production is affected by cropping area, yield, rainfall, prices, interventions and repeat disasters.
* No independent Kerala-wide economic, housing, infrastructure, social or environmental recovery data extracted.
* No machine learning flood or recovery predictions trained.
* `gee_recovery_proxies_UNEXECUTED.js` is a proposal for Earth Engine and has **not been run**; it requires access, authentication and validation.
* Baseline vulnerability was published in 2026, so analyses of years 2018–2021 with that score are ex post and cannot be characterized as leak-free temporal validation.
* Ranking changes are sensitive to the scaling rule and weights and do NOT demonstrate a superior priority policy.

## Sources

Official Kerala Dept of Economics & Statistics agricultural PDFs:
* 2017–18 https://ecostat.kerala.gov.in/storage/publications/247.pdf
* 2018–19 https://ecostat.kerala.gov.in/storage/publications/239.pdf
* 2019–20 https://www.ecostat.kerala.gov.in/storage/publications/3.pdf
* 2020–21 https://ecostat.kerala.gov.in/storage/publications/622.pdf

Baseline: Kendagannaswamy et al (2026), https://doi.org/10.1007/s12524-026-02440-y , Table 9.

The district_crop_panel.csv rows preserve source PDF URLs and page numbers. Manual transcription should be checked independently against the published PDF tables before journal submission.

## Reproduce

    python experiment.py
    python robustness.py
    python make_comparison_figure.py

Python packages: numpy, scipy, matplotlib, pandas (view optional).

## Files

* `district_crop_panel.csv`: source data
* `district_descriptive_ranks.csv`: district rank and output-shortfall sensitivity
* `experiment_results.json`: numeric checks and methods
* `robustness_results.json`, `sensitivity_grid.csv`: robustness results
* `figure_01_*`, `figure_02_*`, `figure_03_*`, `figure_04_*`: visual diagnostics
* `gee_recovery_proxies_UNEXECUTED.js`: **draft only**, not empirical data
* `Kerala_Flood_Recovery_Experimental_Findings.docx` (at /mnt/data level) research report.

## Why this is only a pilot

One earlier 2017–18 agricultural season is NOT a suitable estimate of normal function, and one-year observations cannot establish time to recovery. Event-level flood footprints and two or more independently measured functional recovery dimensions are necessary before testing the paper's central hypothesis.
