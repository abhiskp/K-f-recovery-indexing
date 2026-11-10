#!/usr/bin/env python3
"""Make a checked handoff ZIP with Phase 5 and its unchanged Phase 4 input."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[2]
P5 = ROOT / "phase5"
ARCHIVE = ROOT / "kerala_flood_recovery_phase5_2026-11-09.zip"
P3_CONTEXT = [
    ROOT / "phase3/data/processed/district_season_rice_2014_2020.csv",
    ROOT / "phase3/data_dictionary.md",
    ROOT / "phase3/sources.md",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    # Prevent accidental redistribution of future restricted raw files.
    allowed_raw = {"README.md", "phase5_jrc_waterclass_2014_2017_pilot.tif"}
    unexpected = {p.name for p in (P5 / "data/raw").iterdir() if p.is_file()} - allowed_raw
    if unexpected:
        raise RuntimeError("Review licence before packaging Phase 5 raw files: " +
                           ", ".join(sorted(unexpected)))
    files = []
    for folder in (ROOT / "phase4", P5):
        files.extend(p for p in folder.rglob("*") if p.is_file()
                     and p.name != ".DS_Store" and "__pycache__" not in p.parts)
    files.extend(P3_CONTEXT)
    files = sorted(set(files))
    for p in files:
        if not p.is_file():
            raise FileNotFoundError(p)
        if any(part.lower() in {".aws", ".ssh", ".config", "credentials", "tokens"}
               for part in p.parts) or p.name.startswith(".env"):
            raise RuntimeError("Private-looking path blocked: " + str(p))
    # Verify Phase 4 against its own existing research manifest, without edits.
    with (ROOT / "phase4/results/checksums.csv").open(newline="") as stream:
        for row in csv.DictReader(stream):
            p = ROOT / "phase4" / row["file"]
            if p.name == ".DS_Store":
                continue  # Finder metadata changes when the folder is browsed.
            if not p.is_file() or digest(p) != row["sha256"]:
                raise RuntimeError("Phase 4 checksum mismatch: " + row["file"])
    handoff = """# Phase 5 handoff — 9 November 2026

Read `phase5/README.md`, `results_phase5.md`, `reference_qa.md`, `decision_gate.md`, and `REPRODUCE.md` first. The archive includes all current Phase 5 files, the unchanged Phase 4 folder required for reproduction, and three small Phase 3 panel context files. Phase 2 and the rest of Phase 3 are unchanged and not needed to reproduce Phase 5's completed checks.

No validated flood labels, 2018 rice-area GIS layer, flood-exposure/outcome join, recovery duration, or ranking benefit exists in this archive. The four-band JRC annual-class Earth Engine export and exact-grid local audit are complete. The raster, local class-count CSVs, conservative water-history raster and annual-class figure are included. Source-access requests are drafts only; no emails were sent. Candidate SAR maps are unvalidated. `phase5/results/checksums.csv` lists Phase 5 SHA-256 digests.
"""
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=6,
                 allowZip64=True) as z:
        z.writestr("PHASE5_HANDOFF.md", handoff)
        for p in files:
            z.write(p, p.relative_to(ROOT))
    with ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(files) + 1
        for p in files:
            if hashlib.sha256(z.read(str(p.relative_to(ROOT)))).hexdigest() != digest(p):
                raise RuntimeError("Archive content mismatch: " + str(p))
    print(f"Archive {ARCHIVE.name}: {ARCHIVE.stat().st_size} bytes, {len(files)+1} files")
    print("SHA-256 " + digest(ARCHIVE))


if __name__ == "__main__":
    main()
