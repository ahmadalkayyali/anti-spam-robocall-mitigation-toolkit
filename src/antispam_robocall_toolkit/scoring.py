"""Transparent ANI scoring logic."""

from __future__ import annotations

from pathlib import Path

from .database import fetch_matches, log_validation
from .models import ValidationResponse
from .normalize import normalize_ani


def decision_from_score(score: int) -> str:
    if score >= 90:
        return "BLOCK"
    if score >= 75:
        return "SPAM_QUEUE"
    if score >= 50:
        return "CHALLENGE"
    if score >= 25:
        return "WATCH"
    return "ALLOW"


def action_from_decision(decision: str) -> str:
    actions = {
        "ALLOW": "Route normally",
        "WATCH": "Route normally and tag for reporting",
        "CHALLENGE": "Send to IVR verification or enhanced treatment",
        "SPAM_QUEUE": "Route to special handling queue or lower-priority path",
        "BLOCK": "Reject, disconnect, or route to controlled spam treatment after operational review",
    }
    return actions.get(decision, "Review manually")


def validate_ani(
    ani: str,
    db_path: str | Path,
    dnis: str | None = None,
    source: str | None = None,
    write_log: bool = True,
) -> ValidationResponse:
    normalized = normalize_ani(ani)
    if not normalized:
        response = ValidationResponse(
            ani=ani,
            normalized_ani="",
            dnis=dnis,
            source=source,
            risk_score=0,
            decision="REVIEW",
            reason="ANI was blank or could not be normalized",
            source_hits=[],
            matched_records=0,
            recommended_action="Review manually",
        )
        return response

    matches = fetch_matches(db_path, normalized)
    if not matches:
        response = ValidationResponse(
            ani=ani,
            normalized_ani=normalized,
            dnis=dnis,
            source=source,
            risk_score=0,
            decision="ALLOW",
            reason="No active ANI risk match found",
            source_hits=[],
            matched_records=0,
            recommended_action=action_from_decision("ALLOW"),
        )
    else:
        max_score = max(int(row["risk_score"] or 0) for row in matches)
        decision = decision_from_score(max_score)
        source_hits = sorted({row["source_name"] for row in matches})
        reasons = [row["reason"] for row in matches if row["reason"]]
        response = ValidationResponse(
            ani=ani,
            normalized_ani=normalized,
            dnis=dnis,
            source=source,
            risk_score=max_score,
            decision=decision,
            reason="; ".join(reasons[:3]) or "Matched active ANI risk record",
            source_hits=source_hits,
            matched_records=len(matches),
            recommended_action=action_from_decision(decision),
        )

    if write_log:
        log_validation(db_path, ani, normalized, dnis, source, response.decision, response.risk_score)
    return response
