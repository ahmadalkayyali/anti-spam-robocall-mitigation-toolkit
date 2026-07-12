#!/usr/bin/env python3
"""Build a local SQLite ANI risk database from one or more CSV files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from antispam_robocall_toolkit.database import init_db, insert_risk_records
from antispam_robocall_toolkit.importer import load_risk_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ANI risk SQLite database")
    parser.add_argument("--source", action="append", required=True, help="CSV source file. Repeat for multiple files.")
    parser.add_argument("--db", default="data/output/ani_risk.sqlite", help="SQLite output database path")
    args = parser.parse_args()

    init_db(args.db)
    total = 0
    for source in args.source:
        rows = list(load_risk_csv(source))
        count = insert_risk_records(args.db, rows)
        total += count
        print(f"Imported {count} rows from {source}")

    print(f"Done. Total imported rows: {total}")
    print(f"Database: {args.db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
