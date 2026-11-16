#!/usr/bin/env python3
"""Descriptive Phase 7 panel diagnostics; no exposure or causal model."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[2]
P7 = ROOT / "phase7"
PANEL = P7 / "data/processed/district_season_rice_2014_2025.csv"
STATUS = ROOT / "phase6/data/processed/official_district_notification_status.csv"
OUT = P7 / "results"
OUT.mkdir(exist_ok=True)
METRICS = ("area_ha", "production_tonnes")
PRE = ("2014-15", "2015-16", "2016-17", "2017-18")

def read(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader(); w.writerows(rows)

panel = read(PANEL)
status = {r["district"]: r["notification_status"] for r in read(STATUS)}
lookup = {(r["district"], r["season"], r["year"]): r for r in panel}
districts = sorted(status)
seasons = ("Autumn", "Winter", "Summer")
assert len(panel) == 462 and len(lookup) == 462
assert len(districts) == 14

# Independent recomputation from the Phase 3 source panel, not the Phase 6
# precomputed join or contrast. Group labels come from the official order.
def deviation(district, season, metric, target, years):
    baseline = mean(float(lookup[district, season, y][metric]) for y in years)
    observed = float(lookup[district, season, target][metric])
    return None if baseline == 0 else 100 * (observed / baseline - 1)

groups = {g: [deviation(d, "Autumn", "production_tonnes", "2018-19", PRE)
              for d in districts if status[d] == g]
          for g in ("all_villages", "some_villages")}
group_means = {g: mean(v for v in values if v is not None)
               for g, values in groups.items()}
contrast = group_means["all_villages"] - group_means["some_villages"]
assert abs(contrast - (-50.15151)) < 0.00001, contrast

trends = []
baseline_rows = []
for district in districts:
    for season in seasons:
        for metric in METRICS:
            vals = [float(lookup[district, season, y][metric])
                    if lookup[district, season, y][metric] != "" else None for y in PRE]
            if any(v is None for v in vals):
                trends.append({"district": district, "season": season, "metric": metric,
                               "pre_years": "2014-15..2017-18", "n_observed": sum(v is not None for v in vals),
                               "ols_slope_per_agricultural_year": "", "pre_mean": "",
                               "pre_cv": "", "interpretation": "insufficient_pre_observations"})
                continue
            premean = mean(vals)
            # Four equally spaced annual points, x=0..3; denominator 5.
            slope = sum((i-1.5)*v for i,v in enumerate(vals)) / 5
            variance = sum((v-premean)**2 for v in vals) / 4
            pre_cv = variance**0.5/premean if premean else None
            trends.append({"district": district, "season": season, "metric": metric,
                           "pre_years": "2014-15..2017-18", "n_observed": 4,
                           "ols_slope_per_agricultural_year": f"{slope:.6f}",
                           "pre_mean": f"{premean:.6f}",
                           "pre_cv": f"{pre_cv:.6f}" if pre_cv is not None else "",
                           "interpretation": "descriptive_four_point_slope"})
            baselines = {
                "pre4_mean": premean,
                "pre4_median": median(vals),
                "pre3_mean": mean(vals[:3]),
                "pre4_linear_extrapolation": premean + 2.5*slope,
            }
            obs = float(lookup[district, season, "2018-19"][metric])
            for name, base in baselines.items():
                baseline_rows.append({"district": district, "notification_status": status[district],
                                      "season": season, "metric": metric,
                                      "target_year": "2018-19", "baseline_method": name,
                                      "baseline_value": f"{base:.6f}", "observed_value": f"{obs:.6f}",
                                      "absolute_deviation": f"{obs-base:.6f}",
                                      "percent_deviation": f"{100*(obs/base-1):.6f}" if base > 0 else "",
                                      "percent_undefined_reason": "" if base > 0 else "baseline_nonpositive",
                                      "interpretation": "descriptive_not_flood_attributable"})

write(OUT / "pre2018_trend_diagnostics.csv", trends)
write(OUT / "baseline_sensitivity_2018_19.csv", baseline_rows)

summary = []
for method in ("pre4_mean", "pre4_median", "pre3_mean", "pre4_linear_extrapolation"):
    rr = [r for r in baseline_rows if r["season"] == "Autumn" and
          r["metric"] == "production_tonnes" and r["baseline_method"] == method]
    a = [float(r["percent_deviation"]) for r in rr if r["notification_status"] == "all_villages" and r["percent_deviation"]]
    b = [float(r["percent_deviation"]) for r in rr if r["notification_status"] == "some_villages" and r["percent_deviation"]]
    summary.append({"baseline_method": method, "n_all_defined": len(a), "n_some_defined": len(b),
                    "all_mean_percent_change": f"{mean(a):.6f}",
                    "some_mean_percent_change": f"{mean(b):.6f}",
                    "difference_all_minus_some_pp": f"{mean(a)-mean(b):.6f}",
                    "all_sum_absolute_deviation_tonnes": f"{round(sum(float(r['absolute_deviation']) for r in rr if r['notification_status']=='all_villages'),3):.3f}",
                    "some_sum_absolute_deviation_tonnes": f"{round(sum(float(r['absolute_deviation']) for r in rr if r['notification_status']=='some_villages'),3):.3f}",
                    "interpretation": "descriptive_not_causal"})
write(OUT / "autumn_production_baseline_group_sensitivity.csv", summary)

placebo_a = [deviation(d,"Autumn","production_tonnes","2017-18",PRE[:3])
             for d in districts if status[d] == "all_villages"]
placebo_b = [deviation(d,"Autumn","production_tonnes","2017-18",PRE[:3])
             for d in districts if status[d] == "some_villages"]
placebo_diff = mean(v for v in placebo_a if v is not None) - mean(v for v in placebo_b if v is not None)

state = []
for year in sorted({r["year"] for r in panel}):
    for season in seasons:
        rr = [lookup[d, season, year] for d in districts]
        area = sum(float(r["area_ha"]) for r in rr)
        prod = sum(float(r["production_tonnes"]) for r in rr)
        state.append({"year": year, "season": season, "district_rows": len(rr),
                      "published_seasonal_paddy_area_ha": f"{area:.3f}", "published_or_total_rice_production_tonnes": f"{prod:.3f}",
                      "interpretation": "district_sum_descriptive_separate_scopes"})
write(OUT / "state_season_trajectory.csv", state)

flood_years = [
    ("2018-19", "2018", "documented_flood_or_landslide", "2018 Kerala notification", "https://keralaagriculture.gov.in/wp-content/uploads/2021/07/GO-Flood-Notification-2018-3102018_1-additional-VIllage-1.pdf"),
    ("2019-20", "2019", "documented_flood_or_landslide", "23 August 2019 notified 1038 villages", "https://sdma.kerala.gov.in/wp-content/uploads/2019/08/GO-Flood-Landslide-Notification-2019-1.pdf"),
    ("2020-21", "2020", "documented_flood_map_exists", "KSDMA 2020 flood inundation cartographic PDF; no district-season linkage", "https://sdma.kerala.gov.in/wp-content/uploads/2020/11/Flood-Inundation-Map_2020.pdf"),
    ("2021-22", "2021", "documented_flood_or_landslide", "KSDMA October 2021 event report", "https://sdma.kerala.gov.in/wp-content/uploads/2022/05/Event-report_October-2021.pdf"),
    ("2022-23", "2022", "not_systematically_classified", "KSDMA archives exist; no district-season exposure classification in this audit", "https://sdma.kerala.gov.in/archives/"),
    ("2023-24", "2023", "not_systematically_classified", "absence of an identified event is not evidence of no flood", "https://sdma.kerala.gov.in/archives/"),
    ("2024-25", "2024", "documented_other_hazard_flood_unknown", "KSDMA notified 2024 Meppadi landslide; flood incidence not systematically classified", "https://sdma.kerala.gov.in/disaster-notifications/"),
]
write(OUT / "later_event_flags.csv", [dict(zip(("agricultural_year","calendar_event_year","event_flag","evidence_note","source_url"), x)) for x in flood_years])

result = {"panel_rows": len(panel), "panel_years": sorted({r['year'] for r in panel}),
          "phase6_join_rows_are_unique_long_format": 378,
          "independently_reproduced_2018_19_autumn_production": {
              "all_mean_percent": round(group_means['all_villages'], 5),
              "some_mean_percent": round(group_means['some_villages'], 5),
              "all_minus_some_pp": round(contrast, 5),
              "n_defined_all": sum(v is not None for v in groups['all_villages']),
              "n_defined_some": sum(v is not None for v in groups['some_villages'])},
          "pre_event_2017_18_placebo_all_minus_some_pp": round(placebo_diff, 5),
          "interpretation": "descriptive administrative-category contrast; not flood-attributable recovery"}
(OUT / "descriptive_summary.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
