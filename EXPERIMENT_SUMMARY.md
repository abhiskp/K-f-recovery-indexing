# Completed Phase 2 experiments and supported conclusions

## What was measured

The included official-data panel contains 294 district–crop–agricultural-year production observations: 14 Kerala districts, rice/banana/plantain, and seven agricultural years from 2014–15 through 2020–21. Phase 2 added 126 pre-flood observations to the inherited 168. These are annual crop production measurements, **not** flood-attributable losses or recovery times. The 2026 published vulnerability scores are used only for retrospective ranking sensitivity.

The three newly transcribed pre-flood years reproduce all nine printed crop/year state totals exactly. The inherited 12 crop/year state totals were independently recomputed to the stored CSV precision. A separate independent implementation matched all **84** deterministic inherited sensitivity-grid specifications with zero discrepancies and reproduced the three deterministic pseudo-holdout capture values exactly. The inherited stochastic permutations were not rerun.

## State crop totals and change against the four-year pre-flood mean

| Crop | Four-year mean, tonnes | 2018–19, tonnes | 2018–19 vs mean | 2019–20 vs mean | 2020–21 vs mean |
|---|---:|---:|---:|---:|---:|
| Rice | 517,290.0 | 578,256.0 | +11.8% | +13.5% | +21.2% |
| Banana | 534,184.25 | 429,059.672 | −19.7% | +2.7% | +1.9% |
| Plantain | 413,858.75 | 383,102.049 | −7.4% | −1.7% | −0.2% |

The four reference years are 2014–15 through 2017–18. These state changes cannot be attributed to the 2018 flood because event inundation, within-year timing, comparison areas and relevant confounders have not been linked to the crop panel.

The official 2018–19 state area comparison shows that raw production mixes area and yield changes:

| Crop | Area change, 2017–18 to 2018–19 | Calculated yield change | Production change |
|---|---:|---:|---:|
| Rice | +4.7% | +5.9% | +10.9% |
| Banana | −14.9% | −10.9% | −24.2% |
| Plantain | +3.2% | −2.3% | +0.9% |

## Retrospective rank sensitivity

The following 75:25 blends combine separately scaled published 2026 vulnerability with mean annual nonnegative crop-output shortfall. The 25% crop weight is an illustrative inherited comparison setting, not an estimated policy weight. Top-five overlap compares with the published top five; Spearman and Kendall compare the full 14-district order.

| Scaling | Output reference | Spearman | Kendall | Top-five overlap | Mean absolute rank shift |
|---|---|---:|---:|---:|---:|
| Min–max | 2017–18 only | 0.854945 | 0.714286 | 3/5 | 1.429 |
| Min–max | Four-year mean | 0.868132 | 0.714286 | 3/5 | 1.429 |
| Min–max | Four-year median | 0.894505 | 0.736264 | 3/5 | 1.286 |
| Midrank percentile | 2017–18 only | 0.972498 | 0.883991 | 5/5, cutoff tie-sensitive | 0.643 |
| Midrank percentile | Four-year mean | 0.963697 | 0.861892 | 4/5 | 0.786 |
| Midrank percentile | Four-year median | 0.962557 | 0.877832 | 5/5 | 0.786 |

With the four-year mean and min–max scaling, the descriptive top five are Malappuram, Palakkad, Alappuzha, Wayanad and Idukki. Leave-one-pre-year-out checks yield top-five overlap of 3/5, 3/5, 3/5 and 4/5 when omitting 2014–15, 2015–16, 2016–17 and 2017–18 respectively. These changes show dependence on reference and scaling choices; they do **not** establish better prioritisation.

The inherited descriptive 2020–21 pseudo-holdout top-five capture values are 0.3694276459783845 at alpha 0.10, 0.593693368754716 at alpha 0.25, and 0.6484911740908542 at alpha 0.50. Phase 2 reproduced these arithmetic values exactly. They are **not prospective validation**: the risk score was published in 2026, after the outcomes, and the agricultural proxy is temporally autocorrelated and confounded.

## Source discrepancies and interpretation risks

- In 2020–21, the inherited wetland-rice district rows sum to **626,886.087 tonnes**, 1.913 tonnes below the annual report's printed 626,888-tonne state total. Phase 2 retained the district entries and flagged the difference.
- The 2018–19 annual table reports **128,560 tonnes** of Alappuzha rice, while the later historical compendium shows **128,561 tonnes**. The contemporaneous annual-table value remains in the inherited input.
- The published vulnerability score is reconstructed by `0.30 hazard + 0.25 exposure + 0.25 sensitivity + 0.20 adaptive_capacity_as_labelled` with maximum absolute score difference **0.0005**. Reversing the labelled capacity term changes rank order (Spearman **0.375824**, top-five overlap **3/5**). The meaning of that source field requires author/source verification; this is not a proven coding error.
- The complete 168 inherited crop observations have not been independently checked cell by cell against annual PDFs. Historic sources are linked but not bundled.

## Decision

**NO-GO for a claim that a multidimensional recovery-adjusted index improves Kerala flood prioritisation.** This handoff establishes a reproducible official agricultural-output panel and baseline-sensitive retrospective ranking diagnostic. It does not contain a 2018 event-exposure raster, seasonally matched satellite recovery measurements, independent economic/infrastructure recovery series, causal flood attribution, or a leakage-safe later-event test. The prepared Earth Engine file is unexecuted. The existing manuscript was not updated with unsupported recovery claims.
