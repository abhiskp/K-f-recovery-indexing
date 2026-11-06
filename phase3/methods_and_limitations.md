# Methods and limitations

## Study design and calculations

Experiment A is an **observational descriptive analysis** of official district/season agricultural statistics. Its unit is one district × DES harvest season × agricultural year. The event of interest is the August 2018 Kerala flood. The administrative season reflects the major *harvest* window, not a field-level flood or planting date. The pre-event reference is the mean of matching seasons over 2014–15, 2015–16, 2016–17 and 2017–18; the median and pre-period minimum/maximum are also stored to make sensitivity visible.

For each unit and metric (area, production, calculated yield), the reported percent deviation is `100 × (observed / pre-event same-season mean − 1)`, undefined when the denominator is zero. The descriptive shortfall is `max(0, reference mean − observed)`. The two-observation shortfall adds the 2018–19 and 2019–20 shortfalls for each district/season/metric. Because the observations are annual seasonal estimates, this addition is **not** an integral over months or a flood-attributable cumulative deficit. No numerical recovery duration is estimated from two post-event observations.

State area and production are district sums. State yield is the quotient of those sums, not the mean of district yields. 2018–19 changes versus 2017–18 are separately shown to reproduce the official report; the four-year reference is used for primary descriptive comparison. The main series uses integers printed in the historical compendium through 2018–19, with the documented Idukki correction. The 2019–20 series uses the contemporaneous annual report because the compendium has material arithmetic and cell conflicts. All source choices are retained at row level.

Summing area across harvest seasons counts cropping episodes, so a field cultivated more than once can contribute more than once to an annual area total. It must not be interpreted as unique hectares of farmland exposed to floodwater.

## What the design cannot identify

- **Causation.** There is no flood exposure measurement linked to these districts or an unexposed comparison group. Rainfall outside inundated areas, seasonal weather, 2019 flooding, crop management, irrigation, land-use change, prices and long-term trends can produce the same statistics. The pre-event four-year mean removes gross season mismatch, but it does not estimate a counterfactual 2018–19 or 2019–20 trajectory.
- **Timing.** The July–October Autumn harvest window overlaps August 2018, but records are not dated within the season. A decline may represent pre-flood crop conditions, post-flood losses, later harvest disruption or reporting changes. Winter and Summer gains need not mean an autumn-affected farm recovered.
- **Spatial ecological inference.** District aggregates can mix flooded and non-flooded farmland. No field or block-level exposure or crop map was available to disaggregate the estimates. Ranking a district by aggregate autumn deviation could misrepresent its flooded farming communities.
- **Measurement uncertainty.** Official seasonal area/production cells have no accessible district-season standard errors here. Source discrepancies are explicitly logged, and median/range sensitivity is supplied; neither is a calibrated confidence interval. Wayanad's zero autumn reference makes a percent change undefined.
- **Recovery definition.** Returning above a historical mean would not prove restoration of land, livelihood or household income. No directly observed return-to-functioning dates or infrastructure restoration panel exists. The two post-event years do not establish persistence past 2019–20.
- **Later-event validation.** The published 2026 vulnerability ranking is retrospective to 2018. It cannot be framed as a pre-2018 prediction. No spatially and temporally independent later-event outcome was used. We did not claim ranking improvement.

## Next defensible design

Obtain 2018 inundation and/or depth observations with geographic coordinates, date, footprint and measurement quality; validate a same-orbit SAR candidate layer against independent labels. Join exposure to stable cultivated-area units or clearly defined districts. Build comparable pre/post seasonal observations for exposed and suitably matched less-exposed units, explicitly accounting for 2019 flooding and baseline trends. Estimate uncertainty from source errors, image coverage and model choices. Only then calculate flood-associated recovery trajectories and test an *a priori* ranking recipe. Validate retrospective priority against an independent functional-disruption outcome and keep any future-event prediction fully separated by time and geography.
