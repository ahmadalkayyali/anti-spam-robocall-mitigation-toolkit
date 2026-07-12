"""Cisco CUBE blocklist configuration generator."""

from __future__ import annotations

import csv
from pathlib import Path

from .importer import load_risk_csv
from .normalize import cube_regex_for_ani


def generate_cube_blocklist(
    input_csv: str | Path,
    output_path: str | Path,
    rule_id: int = 901,
    profile_name: str = "SPAM_CALL_BLOCK",
    dial_peer: int = 100,
    min_score: int = 90,
) -> int:
    rows = [row for row in load_risk_csv(input_csv) if int(row["risk_score"]) >= min_score and row["active"] == 1]
    rows = sorted(rows, key=lambda r: r["normalized_ani"])

    lines: list[str] = []
    lines.append(f"voice translation-rule {rule_id}")
    if not rows:
        lines.append(" ! No numbers met the selected risk threshold")
    for idx, row in enumerate(rows, start=1):
        lines.append(f" rule {idx} reject {cube_regex_for_ani(row['normalized_ani'])}")
    lines.extend(
        [
            "!",
            f"voice translation-profile {profile_name}",
            f" translate calling {rule_id}",
            "!",
            f"dial-peer voice {dial_peer} voip",
            " description *** INBOUND FROM PSTN PROVIDER - REVIEW BEFORE PRODUCTION ***",
            f" call-block translation-profile incoming {profile_name}",
            " call-block disconnect-cause incoming call-reject",
            "!",
        ]
    )

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(rows)
