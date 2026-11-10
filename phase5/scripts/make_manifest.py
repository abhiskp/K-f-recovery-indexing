#!/usr/bin/env python3
"""Hash Phase 5 source, script, report and output files deterministically."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
SKIP = {OUT / "checksums.csv", OUT / "file_manifest.csv"}


def purpose(path: Path) -> str:
    relative = path.relative_to(ROOT)
    if relative.parts[0] == "data":
        return "Phase 5 source status/transcription or raw Earth Engine export"
    if relative.parts[0] == "results":
        return "Executed numerical QA, task status or missing-evidence status"
    if relative.parts[0] == "figures":
        return "Source-class or support/reference QA figure; not a flood map"
    if relative.parts[0] == "scripts":
        return "Reproduction, QA, manifest or package script"
    if path.suffix == ".js":
        return "Earth Engine Code Editor source"
    return "Phase 5 methodology, access, limitations or handoff report"


def main() -> None:
    rows = []
    for p in sorted(ROOT.rglob("*")):
        if (not p.is_file() or p in SKIP or p.name == ".DS_Store"
                or "__pycache__" in p.parts):
            continue
        h = hashlib.sha256()
        with p.open("rb") as stream:
            for block in iter(lambda: stream.read(1 << 20), b""):
                h.update(block)
        rows.append({"file": str(p.relative_to(ROOT)), "bytes": p.stat().st_size,
                     "sha256": h.hexdigest(), "purpose": purpose(p)})
    for target, fields in ((OUT / "checksums.csv", ["file", "bytes", "sha256"]),
                           (OUT / "file_manifest.csv", ["file", "bytes", "sha256", "purpose"])):
        with target.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore",
                                    lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    print(f"Hashed {len(rows)} Phase 5 files")


if __name__ == "__main__":
    main()
