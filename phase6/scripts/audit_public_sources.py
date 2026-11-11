#!/usr/bin/env python3
"""Inspect obtained Phase 6 files; do not turn cartographic pixels into flood truth."""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "phase6"
RAW = P6 / "data/raw"
PROC = P6 / "data/processed"
RESULTS = P6 / "results"
PROC.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

URLS = {
    "sentinel_asia_product_page.html": "https://sentinel-asia.org/EO/2018/article20180809IN.html",
    "sentinel_asia_eos_alos2_20180812.kmz": "https://sentinel-asia.org/EO/2018/article20180809IN/09Aug2018_India_Flood_after_Product-EOS%28Data%29_12Aug2018_002.kmz",
    "ifi_district_flooded_area_v3.csv": "https://zenodo.org/records/11275211/files/District_FloodedArea.csv?download=1",
    "ifi_district_flood_impact_v3.csv": "https://zenodo.org/records/11275211/files/District_FloodImpact.csv?download=1",
    "ifi_india_flood_inventory_v3.csv": "https://zenodo.org/records/11275211/files/India_Flood_Inventory_v3.csv?download=1",
    "zenodo_11275211_metadata.json": "https://zenodo.org/api/records/11275211",
    "kerala_go_flood_notification_2018_20181003.pdf": "https://keralaagriculture.gov.in/wp-content/uploads/2021/07/GO-Flood-Notification-2018-3102018_1-additional-VIllage-1.pdf",
    "europepmc_7437901_fulltext.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7437901/fullTextXML",
    "pmc7437901_metadata.json": "https://pmc-oa-opendata.s3.amazonaws.com/metadata/PMC7437901.1.json",
    "tiwari_pone_0237324_s001.7z": "https://pmc-oa-opendata.s3.amazonaws.com/PMC7437901.1/pone.0237324.s001.7z",
}


def read_csv(path: Path, encoding: str = "utf-8") -> list[dict[str, str]]:
    with path.open(newline="", encoding=encoding) as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


metadata = json.loads((RAW / "zenodo_11275211_metadata.json").read_text())
assert metadata["id"] == 11275211
assert metadata["metadata"]["license"]["id"] == "cc-by-4.0"
zenodo_md5 = {f["key"]: f["checksum"].removeprefix("md5:") for f in metadata["files"]}
zenodo_name = {
    "ifi_district_flooded_area_v3.csv": "District_FloodedArea.csv",
    "ifi_district_flood_impact_v3.csv": "District_FloodImpact.csv",
    "ifi_india_flood_inventory_v3.csv": "India_Flood_Inventory_v3.csv",
}
pmc_metadata = json.loads((RAW / "pmc7437901_metadata.json").read_text())
assert pmc_metadata["pmcid"] == "PMC7437901"
assert pmc_metadata["license_code"] == "CC BY"
assert any("pone.0237324.s001.7z?md5=ecb20eb014e3d83dade6ede12e242766" in u
           for u in pmc_metadata["media_urls"])
assert digest(RAW / "tiwari_pone_0237324_s001.7z", "md5") == "ecb20eb014e3d83dade6ede12e242766"
files = []
for name, url in URLS.items():
    path = RAW / name
    assert path.is_file(), path
    md5 = digest(path, "md5")
    expected = zenodo_md5.get(zenodo_name.get(name, ""), "")
    if name == "tiwari_pone_0237324_s001.7z":
        expected = "ecb20eb014e3d83dade6ede12e242766"
    assert not expected or md5 == expected, (name, md5, expected)
    files.append({"file": f"data/raw/{name}", "source_url": url,
                  "bytes": path.stat().st_size, "sha256": digest(path, "sha256"),
                  "md5": md5, "source_expected_md5": expected,
                  "checksum_verified": "yes" if expected else "sha256_recorded"})
write_csv(RESULTS / "raw_file_provenance.csv", files)

with ZipFile(RAW / "sentinel_asia_eos_alos2_20180812.kmz") as kmz:
    assert kmz.testzip() is None
    names = kmz.namelist()
    assert names == ["doc.kml", "Layer0.png", "Layer2.png", "Layer3.png", "legend0.png"]
    kml = ET.fromstring(kmz.read("doc.kml"))
    ns = {"k": "http://www.opengis.net/kml/2.2"}
    overlays = []
    for node in kml.findall(".//k:GroundOverlay", ns):
        box = node.find("k:LatLonBox", ns)
        values = {a: float(box.find(f"k:{a}", ns).text)
                  for a in ("west", "south", "east", "north")}
        overlays.append({"name": node.find("k:name", ns).text,
                         "image": node.find("k:Icon/k:href", ns).text, **values})
    assert len(overlays) == 3
    geometry_types = {tag: len(kml.findall(f".//k:{tag}", ns))
                      for tag in ("Point", "LineString", "Polygon", "MultiGeometry")}
    assert all(v == 0 for v in geometry_types.values())
    layer0 = Image.open(BytesIO(kmz.read("Layer0.png")))
    assert layer0.mode == "RGBA"
    # These are rendered overlay pixels, not a surveyed negative/valid frame.
    alpha = layer0.getchannel("A")
    hist = alpha.histogram()
    assert sum(hist) == layer0.width * layer0.height
    colored = sum(hist[1:])
    pilot = {"west": 76.35, "south": 9.45, "east": 76.60, "north": 9.75}
    box = overlays[0]
    intersects = not (box["east"] <= pilot["west"] or box["west"] >= pilot["east"]
                      or box["north"] <= pilot["south"] or box["south"] >= pilot["north"])
    assert not intersects
    kmz_summary = {"archive_members": names, "ground_overlays": overlays,
                   "vector_geometry_counts": geometry_types,
                   "layer0_pixel_width": layer0.width, "layer0_pixel_height": layer0.height,
                   "layer0_nontransparent_visual_pixels": colored,
                   "layer0_transparent_visual_pixels": hist[0],
                   "layer0_alpha_values": [i for i, n in enumerate(hist) if n],
                   "phase4_pilot_intersection": intersects,
                   "interpretation": "georeferenced KML GroundOverlay PNG; transparency is unknown, not surveyed non-flood"}
    (RESULTS / "sentinel_asia_kmz_structure.json").write_text(
        json.dumps(kmz_summary, indent=2) + "\n")

inventory = read_csv(RAW / "ifi_india_flood_inventory_v3.csv", "utf-8-sig")
kerala2018 = []
for row in inventory:
    states = [s.strip() for s in row["State"].split(",")]
    if "Kerala" not in states:
        continue
    try:
        start = datetime.strptime(row["Start Date"], "%d-%m-%Y %H:%M")
        end = datetime.strptime(row["End Date"], "%d-%m-%Y %H:%M")
    except ValueError:
        continue
    if start.year != 2018:
        continue
    span = (end.date() - start.date()).days + 1
    reported = int(row["Duration(Days)"]) if row["Duration(Days)"].strip() else None
    kerala2018.append({"uei": row["UEI"], "start_date_as_published": row["Start Date"],
                       "end_date_as_published": row["End Date"],
                       "reported_duration_days": reported if reported is not None else "",
                       "calendar_span_inclusive_days": span,
                       "reported_duration_matches_calendar": (reported == span) if reported is not None else "",
                       "state_field": row["State"], "districts_as_published": row["Districts"],
                       "districts_listed_n": len([d for d in row["Districts"].split(",") if d.strip()]),
                       "latitude_as_published": row["Latitude"],
                       "longitude_as_published": row["Longitude"],
                       "area_affected_as_published": row["Area Affected"],
                       "human_fatality_as_published": row["Human fatality"],
                       "human_displaced_as_published": row["Human Displaced"],
                       "source": row["Event Source"]})
assert len(kerala2018) == 11
write_csv(PROC / "ifi_2018_kerala_event_screen.csv", kerala2018)

districts = list(dict.fromkeys(r["district"] for r in read_csv(
    ROOT / "phase3/data/processed/district_season_rice_2014_2020.csv")))
assert len(districts) == 14
flooded = {r["Dist_Name"].strip(): r for r in read_csv(RAW / "ifi_district_flooded_area_v3.csv")}
impact = {r["Dist_Name"].strip(): r for r in read_csv(RAW / "ifi_district_flood_impact_v3.csv")}
historical = []
for district in districts:
    assert district in flooded and district in impact, district
    a, b = flooded[district], impact[district]
    historical.append({"district": district,
                       "percent_flooded_area_historical_model": a["Percent_Flooded_Area"],
                       "permanent_water_percent_as_published": a["Parmanent_Water"],
                       "corrected_percent_flooded_area_historical_model": a["Corrected_Percent_Flooded_Area"],
                       "human_fatality_historical_aggregate": b["Human_fatality"],
                       "human_injured_historical_aggregate": b["Human_injured"],
                       "population_as_published": b["Population"],
                       "mean_flood_duration_historical_days": b["Mean_Flood_Duration"],
                       "not_2018_event_exposure": "yes"})
write_csv(PROC / "ifi_kerala_historical_district_metrics.csv", historical)
summary = {"inventory_rows_total": len(inventory), "kerala_mentioned_2018_event_rows": len(kerala2018),
           "kerala_2018_rows_missing_latitude": sum(not r["latitude_as_published"] for r in kerala2018),
           "kerala_2018_rows_missing_area_affected": sum(not r["area_affected_as_published"] for r in kerala2018),
           "kerala_2018_rows_missing_human_displaced": sum(not r["human_displaced_as_published"] for r in kerala2018),
           "kerala_2018_rows_missing_human_fatality": sum(not r["human_fatality_as_published"] for r in kerala2018),
           "kerala_2018_uei_0036_start_date": next(r["start_date_as_published"] for r in kerala2018 if r["uei"].endswith("0036")),
           "kerala_2018_uei_0036_reported_duration_days": next(r["reported_duration_days"] for r in kerala2018 if r["uei"].endswith("0036")),
           "historical_district_rows_matched_to_phase3": len(historical),
           "historical_tables_are_event_agnostic": True,
           "zenodo_license": "CC-BY-4.0"}
(RESULTS / "ifi_source_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({"kmz": {"phase4_pilot_intersection": intersects,
                          "ground_overlays": len(overlays),
                          "vector_geometry_counts": geometry_types},
                  "ifi": summary}, indent=2))
