#!/usr/bin/env python3
"""Descriptive district screen: administrative notification versus rice harvests.

The notification is not a remotely observed flood layer. No result from this
script estimates rice-area inundation, recovery duration, or a causal effect.
"""
from __future__ import annotations

import csv
import json
from itertools import combinations
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "phase6"
PANEL = ROOT / "phase3/data/processed/district_season_rice_2014_2020.csv"
OUT = P6 / "data/processed"
RES = P6 / "results"
FIG = P6 / "figures"
for d in (OUT, RES, FIG):
    d.mkdir(parents=True, exist_ok=True)

SOURCE = "https://keralaagriculture.gov.in/wp-content/uploads/2021/07/GO-Flood-Notification-2018-3102018_1-additional-VIllage-1.pdf"
# G.O.(P) No.6/2018/DMD, 3 October 2018, Annexure. The classification is
# transcribed at district level; the notification covers floods AND landslides.
ALL = {
    "Alappuzha": 93, "Ernakulam": 127, "Idukki": 67,
    "Kottayam": 100, "Pathanamthitta": 70, "Thrissur": 255,
    "Wayanad": 49,
}
PARTIAL = {"Kannur", "Kollam", "Kozhikode", "Malappuram",
           "Palakkad", "Thiruvananthapuram"}
NOT_LISTED = {"Kasaragod"}
assert len(ALL) + len(PARTIAL) + len(NOT_LISTED) == 14


def write_csv(path: Path, rows: list[dict]) -> None:
    assert rows
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


status = []
for district in sorted(ALL.keys() | PARTIAL | NOT_LISTED):
    category = ("all_villages" if district in ALL else
                "some_villages" if district in PARTIAL else "not_listed")
    status.append({"district": district, "notification_status": category,
                   "notified_village_count_if_all": ALL.get(district, ""),
                   "source_order": "G.O.(P) No.6/2018/DMD, 2018-10-03",
                   "source_url": SOURCE,
                   "exposure_interpretation": "administrative flood_or_landslide; no inundation denominator"})
write_csv(OUT / "official_district_notification_status.csv", status)

with PANEL.open(newline="", encoding="utf-8") as stream:
    panel = list(csv.DictReader(stream))
assert len(panel) == 252
assert {r["district"] for r in panel} == {r["district"] for r in status}
assert len({(r["district"], r["year"], r["season"]) for r in panel}) == 252

lookup = {(r["district"], r["year"], r["season"]): r for r in panel}
pre4 = ["2014-15", "2015-16", "2016-17", "2017-18"]
pre3 = pre4[:3]
metrics = {"area_ha": "ha", "production_tonnes": "tonnes",
           "yield_tonnes_per_ha": "tonnes_per_ha"}
joined = []
for s in status:
    d = s["district"]
    for season in ("Autumn", "Winter", "Summer"):
        for metric, unit in metrics.items():
            vals = {year: (float(lookup[d, year, season][metric])
                           if lookup[d, year, season][metric] != "" else None) for year in
                    pre4 + ["2018-19", "2019-20"]}
            pre4_valid = [vals[y] for y in pre4 if vals[y] is not None]
            pre3_valid = [vals[y] for y in pre3 if vals[y] is not None]
            baseline = mean(pre4_valid) if pre4_valid else None
            placebo_base = mean(pre3_valid) if pre3_valid else None
            for label, observation, base, baseyears in (
                ("pre_event_placebo_2017_18", vals["2017-18"], placebo_base, "2014-15..2016-17"),
                ("event_year_2018_19", vals["2018-19"], baseline, "2014-15..2017-18"),
                ("later_year_2019_20", vals["2019-20"], baseline, "2014-15..2017-18"),
            ):
                joined.append({"district": d, "notification_status": s["notification_status"],
                               "season": season, "metric": metric, "unit": unit,
                               "comparison": label, "baseline_years": baseyears,
                               "baseline_mean": round(base, 6) if base is not None else "",
                               "observed": round(observation, 6) if observation is not None else "",
                               "absolute_deviation": round(observation-base, 6) if observation is not None and base is not None else "",
                               "percent_deviation": round(100*(observation/base-1), 6) if base not in (None, 0) and observation is not None else "",
                               "baseline_zero": int(base == 0) if base is not None else "",
                               "attributable_to_flood": "not_established"})
write_csv(OUT / "notification_rice_join.csv", joined)


def exact_permutation_p(values: list[float], n_all: int, observed_diff: float) -> float:
    """Two-sided, district-label permutation, purely descriptive."""
    n = len(values)
    extreme = 0
    total = 0
    for chosen in combinations(range(n), n_all):
        aset = set(chosen)
        diff = mean(values[i] for i in range(n) if i in aset) - mean(
            values[i] for i in range(n) if i not in aset)
        extreme += abs(diff) >= abs(observed_diff) - 1e-12
        total += 1
    return extreme / total


contrasts = []
for season in ("Autumn", "Winter", "Summer"):
    for metric, unit in metrics.items():
        for comparison in ("pre_event_placebo_2017_18", "event_year_2018_19", "later_year_2019_20"):
            group = [r for r in joined if r["season"] == season and r["metric"] == metric
                     and r["comparison"] == comparison and r["notification_status"] != "not_listed"]
            a = [r for r in group if r["notification_status"] == "all_villages"]
            b = [r for r in group if r["notification_status"] == "some_villages"]
            assert (len(a), len(b)) == (7, 6)
            av = [float(r["percent_deviation"]) for r in a if r["percent_deviation"] != ""]
            bv = [float(r["percent_deviation"]) for r in b if r["percent_deviation"] != ""]
            # Absolute deviations remain computable even when percent is undefined.
            aabs = [float(r["absolute_deviation"]) for r in a if r["absolute_deviation"] != ""]
            babs = [float(r["absolute_deviation"]) for r in b if r["absolute_deviation"] != ""]
            abase = sum(float(r["baseline_mean"]) for r in a if r["baseline_mean"] != "")
            bbase = sum(float(r["baseline_mean"]) for r in b if r["baseline_mean"] != "")
            aobs = sum(float(r["observed"]) for r in a if r["observed"] != "")
            bobs = sum(float(r["observed"]) for r in b if r["observed"] != "")
            if len(av) >= 2 and len(bv) >= 2:
                diff = mean(av) - mean(bv)
                p = exact_permutation_p(av+bv, len(av), diff)
                loo = []
                for i in range(len(av)):
                    loo.append(mean(av[:i]+av[i+1:])-mean(bv))
                for i in range(len(bv)):
                    loo.append(mean(av)-mean(bv[:i]+bv[i+1:]))
                mean_a, mean_b, med_a, med_b = mean(av), mean(bv), median(av), median(bv)
                lo, hi = min(loo), max(loo)
            else:
                diff = p = mean_a = mean_b = med_a = med_b = lo = hi = ""
            contrasts.append({"season": season, "metric": metric, "unit": unit,
                              "comparison": comparison, "n_all": 7, "n_some": 6,
                              "n_defined_percent_all": len(av), "n_defined_percent_some": len(bv),
                              "all_mean_percent_deviation": round(mean_a, 6) if mean_a != "" else "",
                              "some_mean_percent_deviation": round(mean_b, 6) if mean_b != "" else "",
                              "all_median_percent_deviation": round(med_a, 6) if med_a != "" else "",
                              "some_median_percent_deviation": round(med_b, 6) if med_b != "" else "",
                              "difference_of_mean_percent_deviations_pp": round(diff, 6) if diff != "" else "",
                              "exact_label_permutation_p_descriptive": round(p, 6) if p != "" else "",
                              "leave_one_district_out_diff_min_pp": round(lo, 6) if lo != "" else "",
                              "leave_one_district_out_diff_max_pp": round(hi, 6) if hi != "" else "",
                              "all_sum_absolute_deviation": round(sum(aabs), 6),
                              "some_sum_absolute_deviation": round(sum(babs), 6),
                              "all_baseline_sum": round(abase, 6) if metric != "yield_tonnes_per_ha" else "",
                              "all_observed_sum": round(aobs, 6) if metric != "yield_tonnes_per_ha" else "",
                              "some_baseline_sum": round(bbase, 6) if metric != "yield_tonnes_per_ha" else "",
                              "some_observed_sum": round(bobs, 6) if metric != "yield_tonnes_per_ha" else "",
                              "all_aggregate_percent_change": round(100*(aobs/abase-1), 6) if abase and metric != "yield_tonnes_per_ha" else "",
                              "some_aggregate_percent_change": round(100*(bobs/bbase-1), 6) if bbase and metric != "yield_tonnes_per_ha" else "",
                              "inundated_rice_area_ha": "",
                              "flood_effect_established": "no"})
write_csv(RES / "notification_rice_contrasts.csv", contrasts)

key = next(r for r in contrasts if r["season"] == "Autumn" and
           r["metric"] == "production_tonnes" and r["comparison"] == "event_year_2018_19")
summary = {"panel_rows": len(panel), "joined_rows": len(joined), "contrast_rows": len(contrasts),
           "notification_categories": {"all_villages": 7, "some_villages": 6, "not_listed": 1},
           "primary_descriptive_contrast": key,
           "flood_exposure_measure": "administrative flood_or_landslide notification only",
           "spatial_exposure_recovery_success_gate": "not_met"}
(RES / "notification_rice_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

# A static scientific figure, generated from the exact saved CSV.
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "phase6-notification-2018"
import matplotlib.pyplot as plt

rows = [r for r in joined if r["season"] == "Autumn" and
        r["metric"] == "production_tonnes" and r["comparison"] == "event_year_2018_19"]
fig, ax = plt.subplots(figsize=(9, 5.8))
for y, cat, color, marker in ((1, "all_villages", "#1b6a80", "o"),
                               (0, "some_villages", "#bd6038", "s")):
    rr = sorted((r for r in rows if r["notification_status"] == cat and r["percent_deviation"] != ""),
                key=lambda r: float(r["percent_deviation"]))
    for i, r in enumerate(rr):
        x = float(r["percent_deviation"])
        yy = y + (i-(len(rr)-1)/2)*0.105
        ax.scatter(x, yy, s=42, c=color, marker=marker, zorder=3)
        ax.annotate(r["district"], (x, yy), xytext=(4, 0), textcoords="offset points",
                    fontsize=7.5, va="center")
ax.axvline(0, color="#777777", lw=1)
ax.set_yticks([0, 1], ["Some villages listed", "All villages listed"])
ax.set_xlabel("2018–19 autumn rice production change vs 2014–15 to 2017–18 mean (%)")
ax.set_xlim(min(float(r["percent_deviation"]) for r in rows if r["percent_deviation"] != "")-12,
            max(float(r["percent_deviation"]) for r in rows if r["percent_deviation"] != "")+31)
ax.set_title("Administrative flood/landslide notification and rice output")
ax.text(0, -0.22, "Kasaragod not listed; Wayanad has zero autumn baseline. Notification is not inundation.",
        transform=ax.transAxes, fontsize=8, color="#555555")
ax.grid(axis="x", alpha=.25)
fig.tight_layout()
fig.savefig(FIG / "notification_autumn_rice_screen.svg", bbox_inches="tight", metadata={"Date": None})
fig.savefig(FIG / "notification_autumn_rice_screen.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print(json.dumps(summary, indent=2))
