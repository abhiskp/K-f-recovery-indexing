#!/usr/bin/env python3
"""Audit public NRSC WMS inventory, GFD event metadata, and district geometry.

No flood mask or accuracy metric is inferred from these source inventories.
Standard library only; all outputs stay under phase4.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import struct
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
RESULTS = ROOT / 'results'
for directory in (PROCESSED, RESULTS):
    directory.mkdir(parents=True, exist_ok=True)

KERALA_SCREEN_BBOX = (74.8, 8.0, 77.5, 12.8)  # Broad search box, not state geometry.
PILOT_BBOX = (76.35, 9.45, 76.60, 9.75)
EXPECTED_DISTRICTS = {
    'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha',
    'Kottayam', 'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad',
    'Malappuram', 'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod',
}

def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def intersects(a, b) -> bool:
    return a[0] <= b[2] and a[2] >= b[0] and a[1] <= b[3] and a[3] >= b[1]

def gfd_screen() -> dict:
    catalog = json.loads((RAW / 'gfd_bucket_catalog.json').read_text())
    assert not catalog.get('nextPageToken'), 'GFD catalog listing is incomplete'
    objects = {}
    for item in catalog['items']:
        match = re.fullmatch(r'DFO_(\d+)_From_(\d{8})_to_(\d{8})\.zip', item['name'])
        if not match:
            raise ValueError(f'Unexpected GFD object name: {item["name"]}')
        objects[match.group(1)] = item
    with (RAW / 'gfd_qcdatabase_2019_08_01.csv').open(newline='', encoding='utf-8-sig') as f:
        qc = list(csv.DictReader(f))
    assert len(objects) == len(qc) == 913
    assert set(objects) == {r['ID'] for r in qc}, 'GFD catalog/QC IDs disagree'
    out = []
    monsoon_overlap = []
    for row in qc:
        began = datetime.strptime(row['Began'], '%m/%d/%Y')
        ended = datetime.strptime(row['Ended'], '%m/%d/%Y')
        if began < datetime(2018,10,1) and ended >= datetime(2018,7,1):
            monsoon_overlap.append(row['ID'])
        year = began.year
        if year != 2018:
            continue
        coords = [tuple(map(float, pair.split(',')[:2])) for pair in
                  re.findall(r'[-+]?\d+(?:\.\d+)?,[-+]?\d+(?:\.\d+)?', row['geometry'])]
        if not coords:
            raise ValueError(f'No polygon coordinates for DFO {row["ID"]}')
        xs, ys = zip(*coords)
        bbox = (min(xs), min(ys), max(xs), max(ys))
        obj = objects[row['ID']]
        out.append({
            'dfo_id': row['ID'], 'country': row['Country'],
            'other_country': row['OtherCountry'], 'began': row['Began'],
            'ended': row['Ended'], 'centroid_lon': row['long'],
            'centroid_lat': row['lat'],
            'dfo_polygon_bbox_min_lon': bbox[0], 'dfo_polygon_bbox_min_lat': bbox[1],
            'dfo_polygon_bbox_max_lon': bbox[2], 'dfo_polygon_bbox_max_lat': bbox[3],
            'bbox_intersects_kerala_search_box': int(intersects(bbox, KERALA_SCREEN_BBOX)),
            'object_name': obj['name'], 'object_bytes': obj['size'],
        })
    write_csv(RESULTS / 'gfd_2018_event_screen.csv', out, list(out[0]))
    hits = [r for r in out if r['bbox_intersects_kerala_search_box']]
    if not set(monsoon_overlap).issubset({r['dfo_id'] for r in out}):
        raise ValueError('A 2018 monsoon event began outside 2018; extend screen')
    return {'catalog_events': len(objects), 'qc_events': len(qc),
            'events_began_2018': len(out),
            'events_overlapping_2018_july_september':len(monsoon_overlap),
            'kerala_bbox_candidates': len(hits),
            'kerala_monsoon_overlap_candidates':sum(r['bbox_intersects_kerala_search_box']
                for r in out if r['dfo_id'] in monsoon_overlap),
            'search_bbox_lonlat': KERALA_SCREEN_BBOX,
            'interpretation': 'No matching 2018 GFD event in the published 913-event catalog; no Kerala raster selected.'}

def bhuvan_screen() -> dict:
    source = (RAW / 'bhuvan_flood_page_2026-11-06.html').read_text(errors='replace')
    pattern = r'loadfloodmap\("([^"]+)","([^"]+)","(kl_2018_[^"]+)"\)'
    rows = []
    for match in re.finditer(pattern, source):
        tail = source[match.end():source.find('</div>', match.end())]
        label_match = re.search(r";\s*'\s*>(.*?)&nbsp;<img", tail, re.S)
        bbox_match = re.search(r'zoom_to_layer\(([^)]*)\)', tail)
        if not label_match or not bbox_match:
            raise ValueError(f'Could not parse label/bbox for {match.group(3)}')
        label = html.unescape(label_match.group(1).strip())
        bbox = tuple(float(v.strip()) for v in bbox_match.group(1).split(','))
        label_date = re.match(r'(\d{2})/(\d{2})/2018', label)
        id_date = re.match(r'kl_2018_(\d{2})_(\d{2})(?:_|$)', match.group(3))
        date_discrepancy = (int(label_date.group(1) != id_date.group(1) or
                                label_date.group(2) != id_date.group(2))
                            if label_date and id_date else '')
        label_hour = re.search(r'-(\d{2})Hr', label)
        id_hour = re.search(r'_(\d{2})$', match.group(3))
        hour_discrepancy = (int(label_hour.group(1) != id_hour.group(1))
                            if label_hour and id_hour else '')
        rows.append({
            'layer_id': match.group(3), 'viewer_date_label': label,
            'wms_endpoint': match.group(2),
            'viewer_zoom_bbox_min_lon': bbox[0], 'viewer_zoom_bbox_min_lat': bbox[1],
            'viewer_zoom_bbox_max_lon': bbox[2], 'viewer_zoom_bbox_max_lat': bbox[3],
            'viewer_bbox_intersects_pilot': int(intersects(bbox, PILOT_BBOX)),
            'single_date_label_id_mismatch': date_discrepancy,
            'hour_label_id_mismatch': hour_discrepancy,
            'per_pixel_valid_footprint_available': 'no',
            'validation_role': 'styled WMS reference only; sensor dependence must be checked',
        })
    if len(rows) != 16 or len({r['layer_id'] for r in rows}) != 16:
        raise ValueError('Expected 16 unique Kerala 2018 Bhuvan event layers')
    unavailable = (RAW / 'bhuvan_2018_08_21_06_wms_exception.xml').read_text()
    if 'java.lang.NullPointerException' not in unavailable:
        raise ValueError('21 August 06Hr WMS access diagnostic changed')
    write_csv(PROCESSED / 'bhuvan_kerala_2018_wms_layers.csv', rows, list(rows[0]))
    return {'kerala_2018_wms_layers': len(rows),
            'viewer_bbox_intersects_pilot': sum(r['viewer_bbox_intersects_pilot'] for r in rows),
            'single_date_label_id_mismatches': [r['layer_id'] for r in rows
                                               if r['single_date_label_id_mismatch'] == 1],
            'hour_label_id_mismatches': [r['layer_id'] for r in rows
                                         if r['hour_label_id_mismatch'] == 1],
            'radarsat_21aug06_wms_getmap_status':'ServiceException java.lang.NullPointerException for both GeoTIFF and PNG'}

def tiff_info(path: Path) -> dict:
    b = path.read_bytes()
    endian = '>' if b[:2] == b'MM' else '<' if b[:2] == b'II' else None
    if not endian or struct.unpack(endian+'H', b[2:4])[0] != 42:
        raise ValueError(f'Not classic TIFF: {path.name}')
    offset = struct.unpack(endian+'I', b[4:8])[0]
    n = struct.unpack(endian+'H', b[offset:offset+2])[0]
    tags = {}
    for i in range(n):
        tag, typ, count, value = struct.unpack(endian+'HHII', b[offset+2+12*i:offset+14+12*i])
        tags[tag] = (typ, count, value)
    width = tags[256][2] if tags[256][0] == 4 else tags[256][2] >> 16
    height = tags[257][2] if tags[257][0] == 4 else tags[257][2] >> 16
    channels = tags[277][2] if tags[277][0] == 4 else tags[277][2] >> 16
    transform = struct.unpack(endian+'16d', b[tags[34264][2]:tags[34264][2]+128])
    geo = struct.unpack(endian+'16H', b[tags[34735][2]:tags[34735][2]+32])
    if (width,height,channels) != (512,512,4) or geo[-1] != 4326:
        raise ValueError(f'Unexpected WMS TIFF structure: {path.name}')
    bbox = (transform[3], transform[7]+height*transform[5],
            transform[3]+width*transform[0], transform[7])
    if any(abs(a-c)>1e-8 for a,c in zip(bbox, PILOT_BBOX)):
        raise ValueError(f'TIFF geotransform does not match requested pilot bbox: {path.name}')
    return {'file': str(path.relative_to(ROOT)), 'width_px': width, 'height_px': height,
            'channels': channels, 'epsg': 4326,
            'bbox_min_lon': bbox[0], 'bbox_min_lat': bbox[1],
            'bbox_max_lon': bbox[2], 'bbox_max_lat': bbox[3],
            'sha256': sha(path), 'bytes': len(b),
            'data_type': 'styled WMS RGBA GeoTIFF, not raw classification or valid-footprint mask'}

def boundary_screen() -> dict:
    source = json.loads((RAW / 'kerala_districts_osm_snapshot.geojson').read_text())
    selected = []
    for feature in source['features']:
        props = feature['properties']
        if props.get('admin_level') != '5' or feature['geometry']['type'] not in ('Polygon','MultiPolygon'):
            continue
        name = props.get('name','').removesuffix(' district')
        if name not in EXPECTED_DISTRICTS:
            continue
        selected.append({'type': 'Feature', 'properties': {
            'district': name, 'source': 'OpenStreetMap via Open Data Kerala',
            'source_osm_id': props.get('@id',''),
            'source_osm_timestamp': props.get('@timestamp',''),
            'boundary_year_2018_verified': False},
            'geometry': feature['geometry']})
    names = [f['properties']['district'] for f in selected]
    if len(selected) != 14 or set(names) != EXPECTED_DISTRICTS:
        raise ValueError(f'Expected 14 unique district polygons, got {names}')
    selected.sort(key=lambda f: f['properties']['district'])
    out = {'type':'FeatureCollection', 'features': selected}
    (PROCESSED / 'kerala_districts_osm_candidate.geojson').write_text(
        json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(',',':'))+'\n',
        encoding='utf-8')
    return {'raw_features': len(source['features']), 'selected_district_polygons': len(selected),
            'temporal_status': 'OSM snapshot includes 2021 edits; not verified as 2018 boundaries'}

def main() -> None:
    summary = {'gfd': gfd_screen(), 'bhuvan': bhuvan_screen(),
               'district_boundaries': boundary_screen()}
    tiffs = [tiff_info(p) for p in sorted(RAW.glob('*pilot_wms_styled.tif'))]
    if len(tiffs) != 3:
        raise ValueError('Expected three dated pilot WMS GeoTIFFs')
    write_csv(PROCESSED / 'bhuvan_pilot_wms_geotiff_metadata.csv', tiffs, list(tiffs[0]))
    summary['pilot_wms_tiffs'] = len(tiffs)
    (RESULTS / 'source_screen_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    main()
