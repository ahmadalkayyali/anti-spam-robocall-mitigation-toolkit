"""SQLite database helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = """
CREATE TABLE IF NOT EXISTS ani_risk_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ani TEXT NOT NULL,
    normalized_ani TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_type TEXT DEFAULT 'custom',
    risk_level TEXT DEFAULT 'low',
    risk_score INTEGER DEFAULT 0,
    reason TEXT DEFAULT '',
    first_seen TEXT DEFAULT '',
    last_seen TEXT DEFAULT '',
    active INTEGER DEFAULT 1,
    notes TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_ani_risk_sources_normalized
ON ani_risk_sources(normalized_ani);

CREATE INDEX IF NOT EXISTS idx_ani_risk_sources_active_score
ON ani_risk_sources(active, risk_score);

CREATE TABLE IF NOT EXISTS validation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ani TEXT NOT NULL,
    normalized_ani TEXT NOT NULL,
    dnis TEXT DEFAULT '',
    source TEXT DEFAULT '',
    decision TEXT NOT NULL,
    risk_score INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def insert_risk_records(db_path: str | Path, rows: Iterable[dict]) -> int:
    init_db(db_path)
    count = 0
    sql = """
        INSERT INTO ani_risk_sources
        (ani, normalized_ani, source_name, source_type, risk_level, risk_score,
         reason, first_seen, last_seen, active, notes)
        VALUES
        (:ani, :normalized_ani, :source_name, :source_type, :risk_level,
         :risk_score, :reason, :first_seen, :last_seen, :active, :notes)
    """
    with connect(db_path) as conn:
        for row in rows:
            conn.execute(sql, row)
            count += 1
        conn.commit()
    return count


def fetch_matches(db_path: str | Path, normalized_ani: str) -> list[sqlite3.Row]:
    init_db(db_path)
    with connect(db_path) as conn:
        return conn.execute(
            """
            SELECT * FROM ani_risk_sources
            WHERE normalized_ani = ? AND active = 1
            ORDER BY risk_score DESC, source_name ASC
            """,
            (normalized_ani,),
        ).fetchall()


def log_validation(
    db_path: str | Path,
    ani: str,
    normalized_ani: str,
    dnis: str | None,
    source: str | None,
    decision: str,
    risk_score: int,
) -> None:
    init_db(db_path)
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO validation_log
            (ani, normalized_ani, dnis, source, decision, risk_score)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ani, normalized_ani, dnis or "", source or "", decision, risk_score),
        )
        conn.commit()
