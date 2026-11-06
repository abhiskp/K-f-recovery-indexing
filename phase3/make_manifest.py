#!/usr/bin/env python3
"""Generate SHA-256 inventory of Phase 3 files after all experiments and figures."""
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / 'results' / 'file_manifest.csv'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

files = sorted(p for p in HERE.rglob('*') if p.is_file() and p != TARGET
               and '__pycache__' not in p.parts and p.suffix != '.pyc')
with TARGET.open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['file', 'bytes', 'sha256'])
    for path in files:
        writer.writerow([str(path.relative_to(HERE)), path.stat().st_size, digest(path)])
print(f'Inventoried {len(files)} files in {TARGET.relative_to(HERE)}')
