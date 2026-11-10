#!/usr/bin/env python3
"""Make a vector chronology from executed scene metadata and official dates."""
import csv
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = ROOT / "results/gee_2018_acquisition_groups.csv"
OFFICIAL = ROOT / "data/processed/official_event_chronology.csv"
OUTPUT = ROOT / "figures/2018_pilot_acquisition_chronology.svg"
OUTPUT.parent.mkdir(exist_ok=True)

with GROUPS.open(newline="") as stream:
    groups = list(csv.DictReader(stream))
with OFFICIAL.open(newline="") as stream:
    official = list(csv.DictReader(stream))
start, end = date(2018, 6, 1), date(2018, 9, 30)
left, right = 175, 1010
width = right - left
def xpos(day):
    return left + width * (day - start).days / (end - start).days
def label(x, y, value, cls="label", anchor="middle"):
    return (f'<text x="{x:.1f}" y="{y}" text-anchor="{anchor}" '
            f'class="{cls}">{escape(value)}</text>')
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="525" '
    'viewBox="0 0 1120 525" role="img" aria-label="2018 Kerala pilot '
    'Sentinel-1 acquisition chronology">',
    '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#172b3a}'
    '.title{font-size:22px;font-weight:bold}.subtitle{font-size:13px}'
    '.lane{font-size:14px;font-weight:bold}.tick{font-size:13px}'
    '.label{font-size:12px}.note{font-size:12px;fill:#3a5260}'
    '.grid{stroke:#d9e2e8;stroke-width:1}.axis{stroke:#6b7b87;stroke-width:1.2}'
    '</style>',
    label(35, 42, "Sentinel-1 acquisitions and dated flood products, Kerala pilot",
          "title", "start"),
    label(35, 65, "Pilot: 76.35–76.60°E, 9.45–9.75°N · acquisition dates in IST",
          "subtitle", "start"),
]
for month, caption in [(6,"June"),(7,"July"),(8,"August"),(9,"September")]:
    d = date(2018,month,1)
    x = xpos(d)
    parts += [f'<line x1="{x:.1f}" y1="102" x2="{x:.1f}" y2="363" class="grid"/>',
              label(x,92,caption,"tick")]
parts += [
    f'<line x1="{left}" y1="365" x2="{right}" y2="365" class="axis"/>',
    label(35,151,"S1A descending", "lane","start"),
    label(35,169,"orbit 165", "note","start"),
    label(35,239,"Other S1", "lane","start"),
    label(35,257,"geometry differs", "note","start"),
    label(35,327,"NRSC dated", "lane","start"),
    label(35,345,"products", "note","start"),
]
selected = {
    "2018-06-10": ("10 Jun", "reference"),
    "2018-06-22": ("22 Jun", "reference"),
    "2018-07-04": ("4 Jul", "reference"),
    "2018-07-16": ("16 Jul", "chronology"),
    "2018-08-09": ("9 Aug", "event"),
    "2018-08-21": ("21 Aug", "event"),
}
for row in groups:
    d = date.fromisoformat(row["acquisition_date_ist"])
    if not start <= d <= end:
        continue
    x = xpos(d)
    primary = row["platform_number"] == "A" and (
        row["pass_direction"] == "DESCENDING" and row["relative_orbit"] == "165.0")
    y = 160 if primary else 248
    is_selected = primary and row["acquisition_date_ist"] in selected
    color = ("#154e75" if selected.get(row["acquisition_date_ist"],("",None))[1]
             == "reference" else "#ba5a24") if is_selected else "#9aaab3"
    radius = 8 if is_selected else 5
    parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="{radius}" '
                 f'fill="{color}" stroke="white" stroke-width="1.5"/>')
    if is_selected:
        text, _ = selected[row["acquisition_date_ist"]]
        parts.append(label(x,133,text))
# Only the three directly relevant NRSC key dates; all dates remain in the CSV.
key_official = {"2018-07-16", "2018-08-09", "2018-08-21"}
assert key_official.issubset({r["observation_date_local"] for r in official})
for ds in sorted(key_official):
    x = xpos(date.fromisoformat(ds))
    points = f'{x:.1f},308 {x+7:.1f},316 {x:.1f},324 {x-7:.1f},316'
    parts.append(f'<polygon points="{points}" fill="#742c63"/>')
    parts.append(label(x,346,date.fromisoformat(ds).strftime("%-d %b")))
parts += [
    label(35,402,"Circles = one acquisition (often two adjacent granules); "
          "filled blue = reference candidate, orange = dated event/check.",
          "note","start"),
    label(35,423,"Diamonds = dated NRSC products. The 16 July product documents "
          "July flooding; June/4 July dry status is unverified.","note","start"),
    label(35,444,"9 and 21 August are separate observations. Matching orbit "
          "does not prove flood causation or independent label agreement.",
          "note","start"),
    label(35,480,"Sources: Earth Engine COPERNICUS/S1_GRD inventory; "
          "NRSC/NDEM dated products (see phase4/sources.md).","note","start"),
    '</svg>',
]
OUTPUT.write_text("\n".join(parts) + "\n")
print(OUTPUT)
