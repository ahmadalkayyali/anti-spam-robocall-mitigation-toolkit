from pathlib import Path

from antispam_robocall_toolkit.database import insert_risk_records
from antispam_robocall_toolkit.scoring import validate_ani


def test_validate_ani_block(tmp_path: Path):
    db = tmp_path / "test.sqlite"
    insert_risk_records(db, [
        {
            "ani": "+15551234567",
            "normalized_ani": "+15551234567",
            "source_name": "UnitTest",
            "source_type": "internal",
            "risk_level": "high",
            "risk_score": 95,
            "reason": "Test high risk",
            "first_seen": "",
            "last_seen": "",
            "active": 1,
            "notes": "",
        }
    ])
    result = validate_ani("5551234567", db_path=db, write_log=False)
    assert result.decision == "BLOCK"
    assert result.risk_score == 95
    assert result.source_hits == ["UnitTest"]
