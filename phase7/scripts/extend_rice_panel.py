#!/usr/bin/env python3
"""Extract wet-paddy district-season cells from DES PDF text and audit totals.

Input .txt files are pdftotext -layout derivatives of the archived official PDFs.
The parser is deliberately restricted to the first rice table of each kind.
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P7 = ROOT / "phase7"
RAW = P7 / "data/raw"
OUT = P7 / "data/processed"
RESULTS = P7 / "results"
BASE = ROOT / "phase3/data/processed/district_season_rice_2014_2020.csv"
OUT.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

YEARS = {"2020-21": 622, "2021-22": 664, "2022-23": 1720, "2023-24": 1822}
DISTRICTS = ["Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha",
             "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad",
             "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"]
NAMES = {"Trivandrum": "Thiruvananthapuram", "Eranakulam": "Ernakulam",
         "Kasaragode": "Kasaragod", "Kasargod": "Kasaragod"}
NUM = re.compile(r"\d+(?:\.\d+)?")
ROW = re.compile(r"^\s*(\d{1,2})\s+([A-Za-z]+)\s+(.*)$")

def write(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader(); w.writerows(rows)

def page(text: str, offset: int) -> int:
    return text[:offset].count("\f") + 1

def table(text: str, year: str, kind: str):
    marker = ("AREA UNDER CROPS " if kind == "area" else
              "PRODUCTION OF IMPORTANT CROPS ") + year
    start = text.find(marker, 1000)
    if kind == "production":
        # The later PDFs put a paddy-grain production table immediately before
        # the rice-output table. The historical Phase 3 panel uses RICE.
        while start >= 0 and not re.search(r"Rice \(Wet land\)", text[start:start+700], re.I):
            start = text.find(marker, start + len(marker))
    if start < 0:
        raise ValueError((year, kind, "table not found"))
    tail = text[start:]
    state = re.search(r"(?:KERALA STATE|State Total)\s+([\d.\s]+)", tail, re.I)
    if not state:
        raise ValueError((year, kind, "state row not found"))
    block = tail[:state.end()]
    values = {}
    components = {}
    line_sources = {}
    for line in block.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        idx, raw_name, rest = int(m[1]), m[2], m[3]
        if not 1 <= idx <= 14:
            continue
        name = NAMES.get(raw_name, raw_name)
        if name != DISTRICTS[idx-1]:
            continue
        vals = [float(x) for x in NUM.findall(rest)]
        if len(vals) < 3:
            raise ValueError((year, kind, name, line))
        # DES 2021-22 Table 3 places these two winter cells on the preceding line.
        # They are checked against the printed wet-paddy annual row totals below.
        if year == "2021-22" and kind == "area" and name in {"Kollam", "Pathanamthitta"}:
            winter = {"Kollam": 1177.08, "Pathanamthitta": 217.24}[name]
            vals = [vals[0], winter, vals[1], *vals[2:]]
        if kind == "production":
            if len(vals) < 11:
                raise ValueError((year, kind, name, "expected wet,dry,total rice columns", line))
            components[name] = {"wet": vals[:3], "dry": vals[4:7]}
            values[name] = vals[8:11]  # Rice (Total), same scope as Phase 3 Rice
        else:
            values[name] = vals[:3]  # Wet Paddy; same seasonal cells as Phase 3
        line_sources[name] = line.strip()
    if set(values) != set(DISTRICTS):
        raise ValueError((year, kind, "district coverage", sorted(set(DISTRICTS)-set(values))))
    statevals = [float(x) for x in NUM.findall(state[1])]
    state3 = statevals[8:11] if kind == "production" else statevals[:3]
    if len(state3) != 3:
        raise ValueError((year, kind, "state values"))
    return values, state3, page(text, start), line_sources, components

with BASE.open(newline="", encoding="utf-8") as f:
    old = list(csv.DictReader(f))
assert len(old) == 252 and len({(r['district'],r['year'],r['season']) for r in old}) == 252

rows = []
for r in old:
    area_id = Path(r["area_source_url"]).name
    prod_id = Path(r["production_source_url"]).name
    area_table = {"626.pdf": "Table 17: seasonal paddy area", "3.pdf": "Table 3: wet-paddy area"}.get(area_id, "Phase3 audited source table")
    prod_table = {"626.pdf": "Table 41: seasonal rice production", "3.pdf": "Table 4: wet-land rice production",
                  "247.pdf": "Table 4: wet-land rice production correction"}.get(prod_id, "Phase3 audited source table")
    area_page = {("626.pdf", "55"): 64, ("626.pdf", "56"): 65,
                 ("3.pdf", "38"): 51}.get((area_id, r["area_source_printed_page"]), "")
    prod_page = {("626.pdf", "87"): 96, ("626.pdf", "88"): 97,
                 ("3.pdf", "142"): 155, ("247.pdf", "143"): 150}.get((prod_id, r["production_source_printed_page"]), "")
    rows.append({"district": r["district"], "year": r["year"], "season": r["season"],
                 "area_ha": r["area_ha"], "production_tonnes": r["production_tonnes"],
                 "yield_tonnes_per_ha": "",
                 "wet_rice_production_tonnes": "", "dry_rice_production_tonnes": "",
                 "production_component_status": "not_reported_in_source",
                 "legacy_phase3_ratio_tonnes_per_ha": r["yield_tonnes_per_ha"],
                 "area_scope": "wet_paddy_explicit" if area_id == "3.pdf" else "seasonal_paddy_component_unspecified",
                 "production_scope": "published_rice_component_unspecified",
                 "yield_status": "not_identifiable_from_legacy_scope",
                 "area_status": "reported_zero" if r["area_ha"] == "0" else "observed",
                 "production_status": "reported_zero" if r["production_tonnes"] == "0" else "observed",
                 "crop_definition": "published_seasonal_paddy_area_and_rice_production_scope_not_explicit",
                 "area_source_pdf": area_id,
                 "area_source_table": area_table,
                 "area_source_printed_page": r["area_source_printed_page"],
                 "area_source_pdf_page": area_page,
                 "area_source_url": r["area_source_url"],
                 "production_source_pdf": prod_id,
                 "production_source_table": prod_table,
                 "production_source_printed_page": r["production_source_printed_page"],
                 "production_source_pdf_page": prod_page,
                 "production_source_url": r["production_source_url"],
                 "source_decision": r["source_decision"]})

qa = []
for year, pdfid in YEARS.items():
    source = (RAW / f"kerala_des_{pdfid}.txt").read_text(encoding="utf-8")
    areas, area_state, area_pdf_page, area_lines, _ = table(source, year, "area")
    prod, prod_state, prod_pdf_page, prod_lines, prod_components = table(source, year, "production")
    # The printed page labels are at the bottom of the same PDF pages.
    area_print = {"2020-21": 42, "2021-22": 38, "2022-23": 42, "2023-24": 43}[year]
    prod_print = {"2020-21": 146, "2021-22": 144, "2022-23": 201, "2023-24": 222}[year]
    for j, season in enumerate(("Autumn", "Winter", "Summer")):
        for metric, vals, official, unit in (("area_ha", areas, area_state, "ha"),
                                            ("production_tonnes", prod, prod_state, "tonnes")):
            summed = sum(vals[d][j] for d in DISTRICTS)
            qa.append({"year": year, "season": season, "metric": metric, "unit": unit,
                       "district_sum": f"{summed:.3f}", "printed_state_total": f"{official[j]:.3f}",
                       "difference_district_minus_state": f"{summed-official[j]:.3f}",
                       "state_control_basis": "printed_source_row",
                       "source_pdf": f"kerala_des_{pdfid}.pdf",
                       "source_printed_page": area_print if metric == "area_ha" else prod_print,
                       "source_pdf_page": area_pdf_page if metric == "area_ha" else prod_pdf_page})
        for district in DISTRICTS:
            a, p = areas[district][j], prod[district][j]
            wet = prod_components[district]["wet"][j]
            dry = prod_components[district]["dry"][j]
            rows.append({"district": district, "year": year, "season": season,
                         "area_ha": f"{a:.2f}" if year != "2020-21" else f"{a:g}",
                         "production_tonnes": f"{p:.3f}",
                         "yield_tonnes_per_ha": f"{wet/a:.6f}" if a else "",
                         "wet_rice_production_tonnes": f"{wet:.3f}",
                         "dry_rice_production_tonnes": f"{dry:.3f}",
                         "production_component_status": "source_printed_mismatch" if abs(p-wet-dry) > 0.01 else "reconciles_within_0.01_t",
                         "legacy_phase3_ratio_tonnes_per_ha": "",
                         "area_scope": "wet_paddy_explicit", "production_scope": "all_rice_wet_plus_dry",
                         "yield_status": "wet_rice_per_wet_paddy" if a else "undefined_zero_wet_area",
                         "area_status": "reported_zero" if a == 0 else "observed",
                         "production_status": "reported_zero" if p == 0 else "observed",
                         "crop_definition": "wet_paddy_area_and_all_rice_production",
                         "area_source_pdf": f"kerala_des_{pdfid}.pdf",
                         "area_source_table": "Table 3: Area under crops, wet paddy",
                         "area_source_printed_page": area_print,
                         "area_source_pdf_page": area_pdf_page,
                         "area_source_url": f"https://www.ecostat.kerala.gov.in/storage/publications/{pdfid}.pdf",
                         "production_source_pdf": f"kerala_des_{pdfid}.pdf",
                         "production_source_table": "Table 4: Production of important crops, Rice (Total)" if year != "2023-24" else "Table 8: Production of important crops, Rice (Total)",
                         "production_source_printed_page": prod_print,
                         "production_source_pdf_page": prod_pdf_page,
                         "production_source_url": f"https://www.ecostat.kerala.gov.in/storage/publications/{pdfid}.pdf",
                         "source_decision": "contemporaneous_DES_annual_report"})

def final_estimate_page(index: int):
    page_text = (RAW / "kerala_des_1824.txt").read_text(encoding="utf-8").split("\f")[index-1]
    vals = {}
    for line in page_text.splitlines():
        m = ROW.match(line)
        if m and 1 <= int(m[1]) <= 14:
            name = NAMES.get(m[2], m[2])
            if name == DISTRICTS[int(m[1])-1]:
                numbers = [float(x) for x in NUM.findall(m[3])]
                if len(numbers) >= 2:
                    vals[name] = numbers[:2]
        else:
            # PDF page 3 wraps a few row numbers above their district names.
            m2 = re.match(r"^\s*([A-Za-z]+)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)", line)
            if m2:
                name = NAMES.get(m2[1], m2[1])
                if name in DISTRICTS:
                    vals[name] = [float(m2[2]), float(m2[3])]
    state = re.search(r"STATE\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)", page_text)
    if set(vals) != set(DISTRICTS) or not state:
        raise ValueError(("2024-25", index, "incomplete official page"))
    return vals, [float(state[1]), float(state[2])]

autumn_wet, autumn_wet_state = final_estimate_page(4)
autumn_dry, autumn_dry_state = final_estimate_page(3)
winter_wet, winter_wet_state = final_estimate_page(2)
winter_dry, winter_dry_state = final_estimate_page(1)
def transcribed(season):
    with (RAW / f"kerala_des_1844_summer_{season}_transcription.csv").open(newline="", encoding="utf-8") as f:
        source = list(csv.DictReader(f))
    values = {r["district"]: [float(r["area_ha"]), float(r["production_tonnes"])]
              for r in source if r["district"] != "STATE"}
    state = next([float(r["area_ha"]), float(r["production_tonnes"])]
                 for r in source if r["district"] == "STATE")
    assert set(values) == set(DISTRICTS)
    return values, state
summer_wet, summer_wet_state = transcribed("wet")
summer_dry, summer_dry_state = transcribed("dry")
for season, wet, wet_state, dry, dry_state, pdfid, wetpage, drypage in (
    ("Autumn", autumn_wet, autumn_wet_state, autumn_dry, autumn_dry_state, 1824, 4, 3),
    ("Winter", winter_wet, winter_wet_state, winter_dry, winter_dry_state, 1824, 2, 1),
    ("Summer", summer_wet, summer_wet_state, summer_dry, summer_dry_state, 1844, 1, 2)):
    vals = {d: [wet[d][0], wet[d][1]+dry[d][1]] for d in DISTRICTS}
    state = [wet_state[0], wet_state[1]+dry_state[1]]
    # Verify the separate printed wet/dry controls before combining production.
    assert abs(sum(wet[d][1] for d in DISTRICTS)-wet_state[1]) < 0.01
    assert abs(sum(dry[d][1] for d in DISTRICTS)-dry_state[1]) < 0.01
    for j, (metric, unit) in enumerate((("area_ha", "ha"), ("production_tonnes", "tonnes"))):
        summed = sum(vals[d][j] for d in DISTRICTS)
        qa.append({"year": "2024-25", "season": season, "metric": metric, "unit": unit,
                   "district_sum": f"{summed:.3f}", "printed_state_total": f"{state[j]:.3f}",
                   "difference_district_minus_state": f"{summed-state[j]:.3f}",
                   "state_control_basis": "printed_wet_area" if j == 0 else "sum_of_printed_wet_and_dry_rice",
                   "source_pdf": f"kerala_des_{pdfid}.pdf", "source_printed_page": "unpaginated",
                   "source_pdf_page": wetpage if j == 0 else f"{wetpage}+{drypage}"})
    for district in DISTRICTS:
        a, p = vals[district]
        wet_prod, dry_prod = wet[district][1], dry[district][1]
        url = f"https://www.ecostat.kerala.gov.in/storage/publications/{pdfid}.pdf"
        rows.append({"district": district, "year": "2024-25", "season": season,
                     "area_ha": f"{a:g}", "production_tonnes": f"{p:.3f}",
                     "yield_tonnes_per_ha": f"{wet_prod/a:.6f}" if a else "",
                     "wet_rice_production_tonnes": f"{wet_prod:.3f}",
                     "dry_rice_production_tonnes": f"{dry_prod:.3f}",
                     "production_component_status": "derived_sum_of_two_final_estimates",
                     "legacy_phase3_ratio_tonnes_per_ha": "",
                     "area_scope": "wet_paddy_explicit", "production_scope": "all_rice_wet_plus_dry",
                     "yield_status": "wet_rice_per_wet_paddy" if a else "undefined_zero_wet_area",
                     "area_status": "reported_zero" if a == 0 else "observed",
                     "production_status": "reported_zero" if p == 0 else "observed",
                     "crop_definition": "wet_paddy_area_and_all_rice_production",
                     "area_source_pdf": f"kerala_des_{pdfid}.pdf",
                     "area_source_table": f"2024-25 final {season.lower()} wet-paddy estimate",
                     "area_source_printed_page": "unpaginated", "area_source_pdf_page": wetpage,
                     "area_source_url": url,
                     "production_source_pdf": f"kerala_des_{pdfid}.pdf",
                     "production_source_table": f"2024-25 final {season.lower()} wet+dry rice estimates combined",
                     "production_source_printed_page": "unpaginated", "production_source_pdf_page": f"{wetpage}+{drypage}",
                     "production_source_url": url,
                     "source_decision": "final_DES_seasonal_estimate" + ("_visual_transcription" if season == "Summer" else "")})

assert len(rows) == 462 and len({(r['district'],r['year'],r['season']) for r in rows}) == 462
write(OUT / "district_season_rice_2014_2025.csv", rows)
write(RESULTS / "state_total_reconciliation.csv", qa)
component_qa = []
for r in rows[252:]:
    difference = float(r["production_tonnes"]) - float(r["wet_rice_production_tonnes"]) - float(r["dry_rice_production_tonnes"])
    component_qa.append({"district": r["district"], "year": r["year"], "season": r["season"],
                         "printed_or_derived_total_rice_tonnes": r["production_tonnes"],
                         "wet_rice_tonnes": r["wet_rice_production_tonnes"],
                         "dry_rice_tonnes": r["dry_rice_production_tonnes"],
                         "difference_total_minus_components_tonnes": f"{difference:.3f}",
                         "component_status": r["production_component_status"],
                         "source_pdf": r["production_source_pdf"],
                         "source_pdf_page": r["production_source_pdf_page"]})
write(RESULTS / "rice_component_reconciliation.csv", component_qa)
print(f"rows={len(rows)} new=210 QA={len(qa)} max_abs_state_difference={max(abs(float(q['difference_district_minus_state'])) for q in qa):.3f}")
