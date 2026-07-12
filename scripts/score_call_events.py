#!/usr/bin/env python3
"""Score call-event CSV records and export decisions.

Input columns: ani,dnis,timestamp. Additional columns are preserved when possible.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from antispam_robocall_toolkit.scoring import validate_ani


def main() -> int:
    parser = argparse.ArgumentParser(description="Score call-event CSV records")
    parser.add_argument("--input", required=True, help="Input call-event CSV")
    parser.add_argument("--output", default="data/output/scored_call_events.csv", help="Output scored CSV")
    parser.add_argument("--db", default="data/output/ani_risk.sqlite", help="SQLite ANI risk database")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8-sig", newline="") as src, output_path.open("w", encoding="utf-8", newline="") as dst:
        reader = csv.DictReader(src)
        if not reader.fieldnames or "ani" not in [h.lower() for h in reader.fieldnames]:
            raise ValueError("Input CSV must include an ani column")

        ani_field = next(h for h in reader.fieldnames if h.lower() == "ani")
        dnis_field = next((h for h in reader.fieldnames if h.lower() == "dnis"), None)
        fields = reader.fieldnames + ["normalized_ani", "risk_score", "decision", "source_hits", "reason"]
        writer = csv.DictWriter(dst, fieldnames=fields)
        writer.writeheader()

        count = 0
        for row in reader:
            result = validate_ani(row.get(ani_field, ""), db_path=args.db, dnis=row.get(dnis_field) if dnis_field else None, source="batch", write_log=False)
            row.update({
                "normalized_ani": result.normalized_ani,
                "risk_score": result.risk_score,
                "decision": result.decision,
                "source_hits": ";".join(result.source_hits),
                "reason": result.reason,
            })
            writer.writerow(row)
            count += 1

    print(f"Scored {count} call event(s): {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
