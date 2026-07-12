"""CSV import helpers."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator

from .normalize import normalize_ani

RISK_LEVEL_DEFAULTS = {
    "critical": 100,
    "high": 90,
    "medium": 55,
    "low": 20,
    "info": 5,
    "none": 0,
}


def _to_int(value: str | int | None, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def _to_active(value: str | int | None) -> int:
    if value is None or str(value).strip() == "":
        return 1
    return 0 if str(value).strip().lower() in {"0", "false", "no", "n", "inactive"} else 1


def load_risk_csv(csv_path: str | Path) -> Iterator[dict]:
    """Load a generic ANI risk CSV.

    The only required columns are ``ani`` and ``source_name``. Other columns are
    optional and are defaulted safely.
    """
    with Path(csv_path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV file has no header row")

        lowered = {name.lower().strip(): name for name in reader.fieldnames}
        if "ani" not in lowered:
            raise ValueError("CSV must include an 'ani' column")

        for raw in reader:
            ani = (raw.get(lowered["ani"]) or "").strip()
            normalized = normalize_ani(ani)
            if not normalized:
                continue

            source_name = (raw.get(lowered.get("source_name", ""), "") or "CustomSource").strip()
            source_type = (raw.get(lowered.get("source_type", ""), "") or "custom").strip()
            risk_level = (raw.get(lowered.get("risk_level", ""), "") or "low").strip().lower()
            risk_score_raw = raw.get(lowered.get("risk_score", ""), "")
            risk_score = _to_int(risk_score_raw, RISK_LEVEL_DEFAULTS.get(risk_level, 0))
            risk_score = max(0, min(100, risk_score))

            yield {
                "ani": ani,
                "normalized_ani": normalized,
                "source_name": source_name or "CustomSource",
                "source_type": source_type or "custom",
                "risk_level": risk_level,
                "risk_score": risk_score,
                "reason": (raw.get(lowered.get("reason", ""), "") or "").strip(),
                "first_seen": (raw.get(lowered.get("first_seen", ""), "") or "").strip(),
                "last_seen": (raw.get(lowered.get("last_seen", ""), "") or "").strip(),
                "active": _to_active(raw.get(lowered.get("active", ""), "1")),
                "notes": (raw.get(lowered.get("notes", ""), "") or "").strip(),
            }
