#!/usr/bin/env python3
"""Query the local ANI risk database."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from antispam_robocall_toolkit.scoring import validate_ani


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an ANI against the local risk database")
    parser.add_argument("--ani", required=True, help="Caller ANI to validate")
    parser.add_argument("--dnis", default=None, help="Optional called number")
    parser.add_argument("--source", default="cli", help="Optional source name")
    parser.add_argument("--db", default="data/output/ani_risk.sqlite", help="SQLite database path")
    args = parser.parse_args()

    result = validate_ani(args.ani, db_path=args.db, dnis=args.dnis, source=args.source)
    print(json.dumps(result.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
