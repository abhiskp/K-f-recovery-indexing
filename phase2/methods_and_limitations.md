# Methods and limitations for executed Phase 2 work

## Input audit and provenance

The original package contains 168 district–crop–year production entries
(14 × 3 × 4) for 2017–18 through 2020–21. `analysis.py` reads rather than
rewrites it. Independent aggregation reproduces all 12 archived state totals
to the CSV precision. The original 2017–18 and 2018–19 rice tables and the
2020–21 wetland rice distinction were checked against their [official](https://ecostat.kerala.gov.in/storage/publications/247.pdf)
[annual](https://ecostat.kerala.gov.in/storage/publications/239.pdf)
[reports](https://ecostat.kerala.gov.in/storage/publications/622.pdf). The 2020–21
district wetland-rice sum is 1.913 tonnes below the report's rounded state
total (626,888 tonnes); the source values are retained. This is a tiny
rounding or tabulation discrepancy, not evidence of missing district rows.
The 2018–19 Alappuzha rice value is 128,560 in the annual Table 4 but 128,561
in the later [historical compendium](https://www.ecostat.kerala.gov.in/storage/publications/626.pdf),
so we retain the contemporaneous annual-table value and flag the revision.
The complete 168 entries have **not** been independently checked cell by
cell against annual PDFs; further source QA is needed before publication.
The original `experiment.py` hardcodes production values and rewrites its CSV,
JSON and figures on import; `robustness.py` and the comparison-figure script
execute it again. The report and manuscript builders also contain historical
`/mnt/data` paths. These are reproducibility limitations of the inherited
package. New Phase 2 scripts read the archived CSV and write only under
`phase2/`.

For 2014–15, 2015–16 and 2016–17, we transcribed 126 additional observations
from the official historical compendium. Nine reconstructed crop/year state
totals equal the report's printed totals exactly. These earlier values are
whole tonnes, whereas later annual-report values sometimes have decimals.
The 2014–15 rice state total is 562,092 tonnes; 2015–16 549,275; 2016–17
436,483. That volatility makes a single 2017–18 baseline especially weak.

## Descriptive output measures

For district \(d\), crop \(c\), and annual period \(t\), let \(P_{dct}\) be
reported production. The primary reference \(B_{dc}\) is the arithmetic mean
of the four annual observations in 2014–15 to 2017–18. The observed output
deviation is \(P_{dct}/B_{dc}\), with nonnegative shortfall
\(D_{dct}=\max(0,1-P_{dct}/B_{dc})\). We average nine crop/year shortfalls
equally within each district. The reported cumulative quantity is only the
**sum or mean of annual output shortfall fractions**, not a physical
time-integrated recovery deficit. A median baseline and each leave-one-year-out
mean are sensitivity checks. No missing values were filled.

The official statewide 2018–19 area table lets us calculate
yield = production/area for rice, banana and plantain. Production changes
therefore split into observed area and calculated yield changes, without
claiming that either was caused by the flood.

## Retrospective rank stress test

We reproduce the 2026 published district vulnerability scores as a fixed
historical comparator. For a **hypothetical** 25% crop-output component,
both published score and district mean shortfall are separately scaled by
minimum–maximum or midrank percentile, then combined 75:25. This 25% weight
was selected for comparability with the archived sensitivity experiment,
not to maximize rank changes. Ties at the top-five cutoff use higher original
vulnerability as the deterministic secondary key. We report top-five overlap,
Spearman, Kendall and mean absolute rank movement. No top-five change is
called an improvement. With only 14 districts, top 10% would have a
non-integer cutoff and is not used here.

## What cannot yet be estimated

There is no observed 2018 event-exposure raster in the workspace, so none of
these output changes can be assigned to the flooded portion of a district.
Annual crop reporting cannot locate an August 2018 immediate shock or a
date of restored function. We do not estimate recovery duration, a
flood-attributable cumulative deficit, ecological restoration, economic
recovery, or infrastructure recovery. Different crop areas, yields, weather,
market conditions, replanting, 2019/2021 shocks and COVID can all affect the
annual outcomes. Crop-year definitions and district spelling must be checked
before a finer-scale join.

The 2026 score was published after all analysed outcomes; any apparent
"holdout" using it before 2026 leaks future information. Its Table 9 score
is arithmetically consistent with 0.30 hazard + 0.25 exposure + 0.25
sensitivity + 0.20 of the field labelled adaptive capacity. The source's
meaning of that capacity field needs verification before operational use.

## Next empirical gate

Execute the prepared Earth Engine pilot, inspect actual acquisition dates,
relative orbit and per-pixel coverage, and validate Sentinel-1 candidate
water change against independent georeferenced 2018 observations. Only then
join inundated area to stable units. For vegetation, retain the same-quarter
pre-flood distribution, valid observation fraction and less-affected controls;
for VIIRS, screen cloud-free coverage and background noise. After that,
predeclare event-specific 6/12/24-month deficits, right censoring and how
later shocks are handled. Keep retrospective priority rankings distinct from
predictions using only decision-time information.
