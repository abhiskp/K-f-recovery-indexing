#!/usr/bin/env python3
"""Deterministic SHA-256 inventory of Phase 4 files; standard library only."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results' / 'checksums.csv'
SKIP = {OUT, ROOT / 'results' / 'file_manifest.csv'}

def purpose(path: Path) -> str:
    name = path.name
    if path.parent == ROOT:
        return 'Phase 4 report or Earth Engine script'
    if name.endswith('_styled.tif') or name.endswith('_wms.png'):
        return 'Styled Bhuvan pilot WMS rendering; not flood truth'
    if path.parts[-2] == 'figures':
        return 'Deterministic vector chronology from scene inventory and NRSC dates'
    if name == 'phase4_kerala_2016_2018_s1_pilot_full_scene_inventory.csv':
        return 'Actual Earth Engine Sentinel-1 pilot granule metadata export'
    if name.startswith('phase4_s1_2018_pilot_'):
        return 'Actual Earth Engine exploratory export; not validated flood extent'
    if path.parts[-2] == 'raw':
        return 'Original public source snapshot or access diagnostic'
    if path.parts[-2] == 'processed':
        return 'Deterministically parsed source metadata or candidate geometry'
    if path.parts[-2] == 'results':
        return 'Executed source-screen result or explicitly missing experiment status'
    if path.parts[-2] == 'scripts':
        return 'Reproduction or QA script'
    return 'Phase 4 supporting file'

def main() -> None:
    rows = []
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path in SKIP or '__pycache__' in path.parts:
            continue
        h = hashlib.sha256()
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
        rows.append({'file': str(path.relative_to(ROOT)), 'bytes': path.stat().st_size,
                     'sha256': h.hexdigest(), 'purpose': purpose(path)})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    for target, fields in ((OUT, ['file','bytes','sha256']),
                           (ROOT / 'results' / 'file_manifest.csv',
                            ['file','bytes','sha256','purpose'])):
        with target.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    print(f'Hashed {len(rows)} Phase 4 files')

if __name__ == '__main__':
    main()
