#!/usr/bin/env python3
"""Experiment A: descriptive, season-matched official rice panel.

Reads hand-transcribed DES table cells and the original PDFs under data/raw.
Writes only under phase3. Uses Python's standard library; no stochastic steps.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = HERE / "data" / "raw"
PROCESSED = HERE / "data" / "processed"
RESULTS = HERE / "results"
FIGURES = HERE / "figures"
SEASONS = ("Autumn", "Winter", "Summer")
YEARS = ("2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20")
PRE = YEARS[:4]
DISTRICTS = (
    "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha",
    "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad",
    "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod",
)
NAME_MAP = {"Eranakulam": "Ernakulam", "Kozhicode": "Kozhikode", "Kasaragode": "Kasaragod"}
SOURCE_626 = "https://www.ecostat.kerala.gov.in/storage/publications/626.pdf"
SOURCE_239 = "https://ecostat.kerala.gov.in/storage/publications/239.pdf"
SOURCE_3 = "https://www.ecostat.kerala.gov.in/storage/publications/3.pdf"
SOURCE_247 = "https://ecostat.kerala.gov.in/storage/publications/247.pdf"
FILES = (
    ("area", ("2014-15", "2015-16", "2016-17"), 55, 64, "table17_area_2014_2016.txt"),
    ("area", ("2017-18", "2018-19", "2019-20"), 56, 65, "table17_area_2017_2019.txt"),
    ("production", ("2014-15", "2015-16", "2016-17"), 87, 96, "table41_production_2014_2016.txt"),
    ("production", ("2017-18", "2018-19", "2019-20"), 88, 97, "table41_production_2017_2019.txt"),
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def clean_name(name: str) -> str:
    return NAME_MAP.get(name, name)


def read_table(path: Path, years: tuple[str, ...], metric: str,
               printed_page: int, pdf_page: int) -> dict:
    out = {}
    seen = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 13:
            raise ValueError(f"{path.name}:{line_no}: expected district + 12 integers, got {len(parts)}")
        district = clean_name(parts[0])
        if district in seen:
            raise ValueError(f"Duplicate district {district} in {path.name}")
        seen.add(district)
        values = [int(x) for x in parts[1:]]
        if min(values) < 0:
            raise ValueError(f"Negative value in {path.name}:{line_no}")
        for yi, year in enumerate(years):
            v = values[4 * yi:4 * yi + 4]
            out[(metric, district, year)] = {
                "seasons": dict(zip(SEASONS, v[:3])),
                "printed_total": v[3],
                "printed_page": printed_page,
                "pdf_page": pdf_page,
                "transcription_file": path.name,
            }
    if seen != set(DISTRICTS) | {"State"}:
        raise ValueError(f"Unexpected district coverage in {path.name}: {sorted(seen)}")
    return out


def read_2018_report() -> dict:
    path = RAW / "tables5_7_2018_19_crosscheck.txt"
    out = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 4:
            raise ValueError(f"{path.name}:{line_no}: expected four fields")
        season, raw_district, area, production = parts
        key = (clean_name(raw_district), season)
        if season not in SEASONS or key in out:
            raise ValueError(f"Unexpected or duplicate key in {path.name}:{line_no}")
        out[key] = {"area": Decimal(area), "production": Decimal(production)}
    if set(out) != {(d, s) for d in (*DISTRICTS, "State") for s in SEASONS}:
        raise ValueError("Incomplete independent 2018-19 annual-report crosscheck")
    return out


def read_2019_report() -> dict:
    path = RAW / "tables3_4_2019_20_crosscheck.txt"
    out = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 9:
            raise ValueError(f"{path.name}:{line_no}: expected district + eight integers")
        district = clean_name(parts[0])
        if district in out:
            raise ValueError(f"Duplicate district in {path.name}:{line_no}")
        values = [int(v) for v in parts[1:]]
        out[district] = {"area": dict(zip((*SEASONS, "All"), values[:4])),
                         "production": dict(zip((*SEASONS, "All"), values[4:]))}
    if set(out) != set(DISTRICTS) | {"State"}:
        raise ValueError("Incomplete 2019-20 annual-report crosscheck")
    return out


def pct(value: float | None, baseline: float | None) -> float | None:
    return 100 * (value / baseline - 1) if value is not None and baseline and baseline > 0 else None


def rounded(v: Decimal) -> int:
    return int(v.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    data = {}
    for metric, years, printed_page, pdf_page, name in FILES:
        block = read_table(RAW / name, years, metric, printed_page, pdf_page)
        if data.keys() & block.keys():
            raise ValueError("Overlapping table blocks")
        data.update(block)
    if len(data) != 2 * 15 * 6:
        raise ValueError("Incomplete table-by-district-by-year panel")

    qa = []
    for metric in ("area", "production"):
        for year in YEARS:
            for district in (*DISTRICTS, "State"):
                x = data[(metric, district, year)]
                computed = sum(x["seasons"].values())
                delta = computed - x["printed_total"]
                if delta:
                    qa.append({"check": "printed_annual_vs_seasons", "metric": metric, "year": year,
                               "district": district, "season": "All", "calculated": computed,
                               "reported": x["printed_total"], "difference": delta,
                               "source": f"626.pdf printed p.{x['printed_page']}"})
            for season in SEASONS:
                computed = sum(data[(metric, d, year)]["seasons"][season] for d in DISTRICTS)
                state = data[(metric, "State", year)]
                reported = state["seasons"][season]
                if computed != reported:
                    qa.append({"check": "district_sum_vs_state_season", "metric": metric, "year": year,
                               "district": "State", "season": season, "calculated": computed,
                               "reported": reported, "difference": computed - reported,
                               "source": f"626.pdf printed p.{state['printed_page']}"})
            computed = sum(data[(metric, d, year)]["printed_total"] for d in DISTRICTS)
            state = data[(metric, "State", year)]
            if computed != state["printed_total"]:
                qa.append({"check": "printed_district_totals_vs_state_total", "metric": metric,
                           "year": year, "district": "State", "season": "All", "calculated": computed,
                           "reported": state["printed_total"], "difference": computed-state["printed_total"],
                           "source": f"626.pdf printed p.{state['printed_page']}"})

    annual_report = read_2018_report()
    annual_2019 = read_2019_report()
    qa.append({"check": "compendium_vs_2017_annual_report", "metric": "production",
               "year": "2017-18", "district": "Idukki", "season": "Winter",
               "calculated": 1809, "reported": 1808, "difference": 1,
               "source": "626.pdf p.88; 247.pdf p.143"})
    verified_2019_checks = 0
    for metric in ("area", "production"):
        for district in (*DISTRICTS, "State"):
            row = annual_2019[district][metric]
            if sum(row[s] for s in SEASONS) != row["All"]:
                raise ValueError(f"2019 annual report row total mismatch: {metric}, {district}")
            verified_2019_checks += 1
        for season in (*SEASONS, "All"):
            if sum(annual_2019[d][metric][season] for d in DISTRICTS) != annual_2019["State"][metric][season]:
                raise ValueError(f"2019 annual report state total mismatch: {metric}, {season}")
            verified_2019_checks += 1
    annual_2018_state_differences = {}
    for season in SEASONS:
        for metric in ("area", "production"):
            district_sum = sum(annual_report[(d, season)][metric] for d in DISTRICTS)
            state_cell = annual_report[("State", season)][metric]
            annual_2018_state_differences[f"{season}_{metric}"] = str(district_sum - state_cell)
    crosscheck = []
    for district in (*DISTRICTS, "State"):
        for season in SEASONS:
            row = {"district": district, "season": season}
            for metric in ("area", "production"):
                compendium = data[(metric, district, "2018-19")]["seasons"][season]
                annual = annual_report[(district, season)][metric]
                row[f"compendium_{metric}"] = compendium
                row[f"annual_report_{metric}"] = str(annual)
                row[f"annual_report_rounded_{metric}"] = rounded(annual)
                row[f"difference_{metric}"] = compendium - rounded(annual)
                if abs(Decimal(compendium) - annual) > Decimal("0.501"):
                    qa.append({"check": "compendium_vs_2018_annual_report", "metric": metric,
                               "year": "2018-19", "district": district, "season": season,
                               "calculated": compendium, "reported": str(annual),
                               "difference": str(Decimal(compendium) - annual),
                               "source": f"626.pdf pp.56/88; 239.pdf pp.{182 + SEASONS.index(season)}"})
            crosscheck.append(row)
    write_csv(RESULTS / "annual_report_2018_crosscheck.csv", crosscheck, list(crosscheck[0]))

    crosscheck_2019 = []
    for district in (*DISTRICTS, "State"):
        for season in (*SEASONS, "All"):
            row = {"district": district, "season": season}
            for metric in ("area", "production"):
                compendium = data[(metric, district, "2019-20")]
                old = compendium["printed_total"] if season == "All" else compendium["seasons"][season]
                annual = annual_2019[district][metric][season]
                row[f"compendium_{metric}"] = old
                row[f"annual_report_{metric}"] = annual
                row[f"difference_{metric}"] = old - annual
                if old != annual:
                    qa.append({"check": "compendium_vs_2019_annual_report", "metric": metric,
                               "year": "2019-20", "district": district, "season": season,
                               "calculated": old, "reported": annual, "difference": old - annual,
                               "source": f"626.pdf pp.56/88; 3.pdf pp.{38 if metric == 'area' else 142}"})
            crosscheck_2019.append(row)
    write_csv(RESULTS / "annual_report_2019_crosscheck.csv", crosscheck_2019, list(crosscheck_2019[0]))

    panel = []
    for district in DISTRICTS:
        for year in YEARS:
            a = data[("area", district, year)]
            p = data[("production", district, year)]
            for season in SEASONS:
                if year == "2019-20":
                    area = annual_2019[district]["area"][season]
                    prod = annual_2019[district]["production"][season]
                    area_page, prod_page, area_url, prod_url = 38, 142, SOURCE_3, SOURCE_3
                    source_decision = "contemporaneous_annual_report"
                elif year == "2017-18" and district == "Idukki" and season == "Winter":
                    correction = (RAW / "table4_2017_18_correction.txt").read_text(encoding="utf-8").splitlines()[-1].split()
                    if correction != ["Idukki", "298", "1808", "187", "2293"] or p["seasons"][season] != 1809:
                        raise ValueError("2017-18 Idukki correction source no longer matches expected values")
                    area, prod = a["seasons"][season], 1808
                    area_page, prod_page, area_url, prod_url = a["printed_page"], 143, SOURCE_626, SOURCE_247
                    source_decision = "annual_report_production_correction"
                else:
                    area = a["seasons"][season]
                    prod = p["seasons"][season]
                    area_page, prod_page, area_url, prod_url = a["printed_page"], p["printed_page"], SOURCE_626, SOURCE_626
                    source_decision = "historical_compendium"
                if area == 0 and prod:
                    qa.append({"check": "positive_production_at_zero_area", "metric": "yield",
                               "year": year, "district": district, "season": season,
                               "calculated": prod, "reported": area, "difference": prod,
                               "source": "626.pdf tables 17 and 41"})
                panel.append({"district": district, "year": year, "season": season,
                              "area_ha": area, "production_tonnes": prod,
                              "yield_tonnes_per_ha": round(prod / area, 6) if area else "",
                              "area_source_printed_page": area_page,
                              "production_source_printed_page": prod_page,
                              "area_source_url": area_url, "production_source_url": prod_url,
                              "source_decision": source_decision})
    write_csv(PROCESSED / "district_season_rice_2014_2020.csv", panel, list(panel[0]))

    by_key = {(r["district"], r["season"], r["year"]): r for r in panel}
    deviations = []
    for district in DISTRICTS:
        for season in SEASONS:
            for metric, col in (("area", "area_ha"), ("production", "production_tonnes"),
                                ("yield", "yield_tonnes_per_ha")):
                pre = [by_key[(district, season, y)][col] for y in PRE]
                pre = [float(v) for v in pre if v != ""]
                baseline = statistics.mean(pre) if pre else None
                median = statistics.median(pre) if pre else None
                for year in YEARS[4:]:
                    value = by_key[(district, season, year)][col]
                    value = float(value) if value != "" else None
                    deviations.append({"district": district, "season": season, "year": year,
                                       "metric": metric, "observed": value if value is not None else "",
                                       "baseline_mean_2014_2017": round(baseline, 6) if baseline is not None else "",
                                       "baseline_median_2014_2017": round(median, 6) if median is not None else "",
                                       "pre_min": min(pre) if pre else "", "pre_max": max(pre) if pre else "",
                                       "n_pre": len(pre),
                                       "pct_vs_mean": round(pct(value, baseline), 4) if pct(value, baseline) is not None else "",
                                       "pct_vs_median": round(pct(value, median), 4) if pct(value, median) is not None else "",
                                       "below_pre_min": int(value < min(pre)) if value is not None and pre else "",
                                       "descriptive_shortfall": round(max(0, baseline - value), 6) if value is not None and baseline is not None else "",
                                       "attributable_to_2018_flood": "not_established"})
    write_csv(RESULTS / "seasonal_deviations.csv", deviations, list(deviations[0]))

    trajectories = []
    for district in DISTRICTS:
        for season in SEASONS:
            sample = {(r["year"], r["metric"]): r for r in deviations
                      if r["district"] == district and r["season"] == season}
            for metric in ("area", "production", "yield"):
                e = sample[("2018-19", metric)]
                n = sample[("2019-20", metric)]
                v18 = float(e["observed"]) if e["observed"] != "" else None
                v19 = float(n["observed"]) if n["observed"] != "" else None
                b = float(e["baseline_mean_2014_2017"]) if e["baseline_mean_2014_2017"] != "" else None
                col = {"area": "area_ha", "production": "production_tonnes",
                       "yield": "yield_tonnes_per_ha"}[metric]
                prior_raw = by_key[(district, season, "2017-18")][col]
                v17 = float(prior_raw) if prior_raw != "" else None
                p18_17 = pct(v18, v17)
                p19_18 = pct(v19, v18)
                trajectories.append({
                    "district": district, "season": season, "metric": metric,
                    "baseline_mean_2014_2017": b if b is not None else "",
                    "observed_2018_19": v18 if v18 is not None else "",
                    "observed_2019_20": v19 if v19 is not None else "",
                    "pct_2018_vs_baseline": e["pct_vs_mean"],
                    "pct_2019_vs_baseline": n["pct_vs_mean"],
                    "pct_2018_vs_2017": round(p18_17, 4) if p18_17 is not None else "",
                    "pct_2019_vs_2018": round(p19_18, 4) if p19_18 is not None else "",
                    "two_observation_shortfall": round(sum(max(0, b - v) for v in (v18, v19)), 6)
                        if b is not None and v18 is not None and v19 is not None else "",
                    "attributable_to_2018_flood": "not_established",
                })
    write_csv(RESULTS / "district_season_trajectories.csv", trajectories, list(trajectories[0]))

    state = []
    for year in YEARS:
        for season in SEASONS:
            a = sum(by_key[(d, season, year)]["area_ha"] for d in DISTRICTS)
            p = sum(by_key[(d, season, year)]["production_tonnes"] for d in DISTRICTS)
            state.append({"year": year, "season": season, "area_ha": a, "production_tonnes": p,
                          "yield_tonnes_per_ha": round(p / a, 6) if a else ""})
    pre_state = defaultdict(list)
    for r in state:
        if r["year"] in PRE:
            for metric, col in (("area", "area_ha"), ("production", "production_tonnes"),
                                ("yield", "yield_tonnes_per_ha")):
                pre_state[(r["season"], metric)].append(r[col])
    state_out = []
    for r in state:
        for metric, col in (("area", "area_ha"), ("production", "production_tonnes"),
                            ("yield", "yield_tonnes_per_ha")):
            baseline = statistics.mean(pre_state[(r["season"], metric)])
            state_out.append({"year": r["year"], "season": r["season"], "metric": metric,
                              "observed": r[col], "baseline_mean_2014_2017": round(baseline, 6),
                              "pct_vs_baseline": round(pct(r[col], baseline), 4)})
    write_csv(RESULTS / "state_season_series.csv", state_out, list(state_out[0]))

    annual_state = []
    for year in YEARS:
        rows = [r for r in state if r["year"] == year]
        area = sum(r["area_ha"] for r in rows)
        prod = sum(r["production_tonnes"] for r in rows)
        annual_state.append({"year": year, "area_ha": area, "production_tonnes": prod,
                             "yield_tonnes_per_ha": round(prod / area, 6)})
    annual_pre = {col: statistics.mean(r[col] for r in annual_state if r["year"] in PRE)
                  for col in ("area_ha", "production_tonnes", "yield_tonnes_per_ha")}
    for row in annual_state:
        for col in annual_pre:
            row[f"{col}_pct_vs_pre_mean"] = round(pct(row[col], annual_pre[col]), 4)
    write_csv(RESULTS / "state_annual_comparison.csv", annual_state, list(annual_state[0]))

    # Explicitly compare the seasonal reconstruction with the Phase 2 annual rice panel.
    phase2 = {}
    with (ROOT / "phase2" / "data" / "crop_panel_2014_2021.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["crop"].lower() == "rice":
                phase2[(clean_name(row["district"]), row["agricultural_year"])] = row
    annual_comparison = []
    for district in DISTRICTS:
        for year in YEARS:
            seasonal = sum(by_key[(district, season, year)]["production_tonnes"] for season in SEASONS)
            row = phase2.get((district, year))
            if row:
                value = float(row["production_tonnes"])
                annual_comparison.append({"district": district, "year": year,
                                          "seasonal_sum_tonnes": seasonal,
                                          "phase2_annual_tonnes": value,
                                          "difference_tonnes": round(seasonal - value, 6)})
    write_csv(RESULTS / "phase2_annual_comparison.csv", annual_comparison, list(annual_comparison[0]))

    write_csv(RESULTS / "data_quality_findings.csv", qa,
              ["check", "metric", "year", "district", "season", "calculated", "reported", "difference", "source"])
    source_files = [RAW / name for *_, name in FILES] + [RAW / "tables5_7_2018_19_crosscheck.txt",
                   RAW / "tables3_4_2019_20_crosscheck.txt",
                   RAW / "table4_2017_18_correction.txt",
                   RAW / "des_agriculture_statistics_2005_2020_626.pdf",
                   RAW / "des_agricultural_statistics_2018_19_239.pdf",
                   RAW / "des_agricultural_statistics_2019_20_3.pdf",
                   RAW / "des_agricultural_statistics_2017_18_247.pdf"]
    summary = {
        "rows": len(panel), "districts": len(DISTRICTS), "years": list(YEARS),
        "qa_findings": len(qa), "annual_report_2018_crosscheck_rows": len(crosscheck),
        "annual_report_2019_crosscheck_rows": len(crosscheck_2019),
        "verified_2019_annual_row_and_state_checks": verified_2019_checks,
        "annual_2018_decimal_district_minus_state": annual_2018_state_differences,
        "phase2_annual_comparison_rows": len(annual_comparison),
        "state_post_event": [r for r in state_out if r["year"] in YEARS[4:]],
        "data_status": "observed administrative rice statistics; no flood attribution",
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    output_files = ([PROCESSED / "district_season_rice_2014_2020.csv", RESULTS / "summary.json"]
                    + [p for p in RESULTS.glob("*.csv")
                       if p.name not in ("checksums.csv", "file_manifest.csv")])
    checksums = [{"file": str(path.relative_to(HERE)), "sha256": sha256(path), "bytes": path.stat().st_size}
                 for path in sorted(source_files + output_files)]
    write_csv(RESULTS / "checksums.csv", checksums, ["file", "sha256", "bytes"])
    print(json.dumps({k: v for k, v in summary.items() if k != "state_post_event"}, indent=2))


if __name__ == "__main__":
    main()
