#!/usr/bin/env python3
"""Extract the duration-map WMS lead from the saved Phase 4 Bhuvan HTML."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / "phase4/data/raw/bhuvan_flood_page_2026-11-06.html"
html = source.read_text(encoding="utf-8", errors="replace")
match = re.search(r'parent\.loadmap\("aggre_kerala","([^"]+)","([^"]+)"\)', html)
assert match, "Duration layer reference missing from saved public viewer"
endpoint, layer = match.groups()
assert layer == "aggregate_flood_kerala_2018"
assert endpoint.startswith("https://bhuvan-ras2.nrsc.gov.in/cgi-bin/mapserv.exe?")
record = {
    "source_html": str(source.relative_to(root)),
    "viewer_label": "Flood Duration Map (11-21 Aug 2018) : Kerala",
    "wms_endpoint_as_exposed": endpoint,
    "wms_layer_as_exposed": layer,
    "wms_capabilities_probe_2026_11_08": "browser net::ERR_BLOCKED_BY_CLIENT; no service response obtained",
    "underlying_class_file_status": "not obtained",
    "valid_footprint_status": "not obtained",
    "interpretation": "WMS viewer reference, not class raster or independent pixel label"
}
out = root / "phase5/results/duration_viewer_reference.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, indent=2))
